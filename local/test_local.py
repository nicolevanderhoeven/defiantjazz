"""Self-check for the local stack's files: no Docker needed, it only reads them.

    python3 -m unittest discover -s local
"""

import json
import os
import re
import unittest

try:
    import yaml
except ImportError:  # PyYAML isn't a dependency of the game
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


def compose():
    return yaml.safe_load(read("docker-compose.yml"))


def env_of(service):
    env = service.get("environment", {})
    if isinstance(env, list):
        env = dict(item.split("=", 1) for item in env)
    return {k: str(v) for k, v in env.items()}


@unittest.skipUnless(yaml, "needs PyYAML")
class ComposeTest(unittest.TestCase):
    def setUp(self):
        self.doc = compose()
        self.services = self.doc["services"]
        self.default = {n: s for n, s in self.services.items() if not s.get("profiles")}

    def test_one_command_starts_the_whole_stack(self):
        self.assertEqual(set(self.default), {"loki", "prometheus", "tempo", "grafana", "loader", "mcp-grafana", "game"})

    def test_grafana_assistant_is_an_optional_profile_that_needs_cloud(self):
        self.assertEqual(self.services["grafana-assistant"]["profiles"], ["assistant"])
        for name, service in self.default.items():
            text = json.dumps(service)
            self.assertNotIn("assistant", text.lower(), name)
            self.assertNotIn("externalServiceAccounts", text, name)
            self.assertNotIn("MANAGED_SERVICE_ACCOUNTS", text, name)
        assistant = env_of(self.services["grafana-assistant"])
        self.assertEqual(assistant["GF_PLUGINS_PREINSTALL"], "grafana-assistant-app")
        self.assertNotIn("GF_AUTH_ANONYMOUS_ENABLED", assistant)   # Assistant doesn't support anonymous access
        # Its own data volume and port, so the default Grafana is untouched.
        self.assertNotEqual(self.services["grafana-assistant"]["ports"], self.services["grafana"]["ports"])
        self.assertNotIn("grafana-data:/var/lib/grafana", self.services["grafana-assistant"]["volumes"])

    def test_nothing_phones_home(self):
        for name in ("grafana", "grafana-assistant"):
            env = env_of(self.services[name])
            for key in ("GF_ANALYTICS_REPORTING_ENABLED", "GF_ANALYTICS_CHECK_FOR_UPDATES", "GF_ANALYTICS_CHECK_FOR_PLUGIN_UPDATES",
                        "GF_NEWS_NEWS_FEED_ENABLED"):
                self.assertEqual(env[key], "false", f"{name} {key}")
        self.assertEqual(env_of(self.services["grafana"])["GF_PLUGINS_PREINSTALL_DISABLED"], "true")
        self.assertEqual(env_of(self.services["mcp-grafana"])["GRAFANA_USAGE_STATS"], "false")
        self.assertRegex(read("loki.yaml"), r"(?m)^analytics:\n  reporting_enabled: false")
        self.assertRegex(read("tempo.yaml"), r"(?m)^usage_report:\n  reporting_enabled: false")
        # No Grafana Cloud address in anything that runs by default.
        for name, service in self.default.items():
            self.assertNotRegex(json.dumps(service), r"grafana\.(net|com)", name)
        for name in ("loki.yaml", "tempo.yaml", "prometheus.yml"):
            self.assertNotRegex(read(name), r"grafana\.(net|com)")

    def test_anonymous_viewers_by_default(self):
        env = env_of(self.services["grafana"])
        self.assertEqual((env["GF_AUTH_ANONYMOUS_ENABLED"], env["GF_AUTH_ANONYMOUS_ORG_ROLE"]), ("true", "Viewer"))
        self.assertIn("kipsake-sleep-floor.json", env["GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH"])

    def test_every_port_is_local_only(self):
        for name, service in self.services.items():
            for port in service.get("ports", []):
                self.assertTrue(str(port).startswith("127.0.0.1:"), f"{name}: {port}")

    def test_images_are_pinned_to_current_versions(self):
        images = {n: s["image"] for n, s in self.services.items() if "image" in s}
        self.assertRegex(images["loki"], r"^grafana/loki:3\.7\.\d+$")
        self.assertRegex(images["tempo"], r"^grafana/tempo:2\.\d+\.\d+$")
        self.assertRegex(images["prometheus"], r"^prom/prometheus:v3\.\d+\.\d+$")
        self.assertRegex(images["grafana"], r"^grafana/grafana:13\.3\.\d+$")
        self.assertEqual(images["grafana"], images["grafana-assistant"])
        self.assertRegex(images["mcp-grafana"], r"^grafana/mcp-grafana:2\.\d+\.\d+$")
        self.assertRegex(images["game"], r"^nginxinc/nginx-unprivileged:\d+\.\d+\.\d+-alpine$")
        for image in images.values():
            self.assertNotIn("latest", image)

    def test_the_loader_waits_loads_the_whole_history_and_does_not_load_twice(self):
        loader = self.services["loader"]
        command = loader["command"]
        self.assertEqual(command[command.index("--incident-date") + 1], "latest")
        for flag in ("--target", "--wait", "--skip-if-loaded"):
            self.assertIn(flag, command)
        self.assertEqual(loader["restart"], "no")
        # The repository's loader and telemetry are mounted read-only; the loader reaches the stores by their service names.
        for mount in ("../loader:/app/loader:ro", "../telemetry:/app/telemetry:ro"):
            self.assertIn(mount, loader["volumes"])
        env = env_of(loader)
        for key in ("LOCAL_LOKI_OTLP", "LOCAL_PROMETHEUS_OTLP", "LOCAL_TEMPO_OTLP"):
            self.assertRegex(env[key], r"^http://(loki|prometheus|tempo):")
        self.assertIn("ENTRYPOINT", read("loader", "Dockerfile"))
        self.assertIn("!loader/requirements.txt", read("loader", "Dockerfile.dockerignore"))

    def test_the_data_survives_a_restart_and_goes_with_down_v(self):
        for name, volume in (("loki", "loki-data"), ("prometheus", "prometheus-data"), ("tempo", "tempo-data"), ("grafana", "grafana-data")):
            self.assertTrue(any(v.startswith(volume + ":") for v in self.services[name]["volumes"]), name)
            self.assertIn(volume, self.doc["volumes"])

    def test_the_game_is_served_from_web_and_the_leaderboard_is_off_by_default(self):
        game = self.services["game"]
        self.assertIn("../web:/usr/share/nginx/html:ro", game["volumes"])
        self.assertEqual(env_of(game)["DJ_LEADERBOARD_URL"], "${DJ_LEADERBOARD_URL:-}")
        self.assertIn("${DJ_GAME_PORT:-8080}", game["ports"][0])
        # The game's own page tells local mode where Grafana's home dashboard is, and Grafana provisions it there.
        board = json.loads(read("grafana", "dashboards", "kipsake-sleep-floor.json"))
        self.assertTrue(env_of(game)["DJ_DASHBOARD_URL"].endswith("/d/%s/kipsake-sleep-floor" % board["uid"]))
        self.assertIn("/etc/grafana/dashboards", read("grafana", "provisioning", "dashboards", "dashboards.yaml"))
        # Off in the example settings too.
        for line in read(".env.example").splitlines():
            self.assertFalse(line.startswith("DJ_LEADERBOARD_URL"), line)
        self.assertIn("# DJ_LEADERBOARD_URL=", read(".env.example"))
        self.assertTrue(os.access(os.path.join(HERE, "game", "16-dj-config.envsh"), os.X_OK), "the nginx image only runs scripts that are executable")


class GameServerTest(unittest.TestCase):
    def test_the_server_sets_local_mode_and_loosens_nothing_without_a_leaderboard(self):
        conf = read("game", "default.conf.template")
        self.assertIn("location = /local-config.js", conf)
        self.assertIn("window.DJ_LOCAL_CONFIG = ", conf)
        for key in ("grafanaUrl", "mcpUrl", "dashboardUrl", "leaderboardUrl"):
            self.assertIn(f'"{key}"', conf)
        self.assertIn("""sub_filter "connect-src 'none'" "connect-src ${DJ_CONNECT_SRC}";""", conf)
        script = read("game", "16-dj-config.envsh")
        self.assertIn("""DJ_CONNECT_SRC="'none'\"""", script)
        # The page's policy it rewrites is the one in web/index.html.
        with open(os.path.join(ROOT, "web", "index.html"), encoding="utf-8") as f:
            self.assertIn("connect-src 'none'", f.read())


class DashboardTest(unittest.TestCase):
    def test_home_dashboard_explains_the_stack_without_spoilers(self):
        board = json.loads(read("grafana", "dashboards", "kipsake-sleep-floor.json"))
        self.assertEqual(board["uid"], "kipsake-sleep-floor")
        text = json.dumps(board)
        for needle in ("localhost:8080", "localhost:8000/mcp", "kipsake-sleep-floor", "loki", "prometheus", "tempo"):
            self.assertIn(needle, text)
        for panel in board["panels"]:
            for target in panel.get("targets", []):
                self.assertIn(target["datasource"]["uid"], ("loki", "prometheus", "tempo"))
        self.assertNotRegex(text, r"(?i)grafana\.(net|com)")


if __name__ == "__main__":
    unittest.main()
