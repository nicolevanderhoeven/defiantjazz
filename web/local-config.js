/* Local mode's settings. A static server serves this file as it is: not local, nothing set.
 * The local stack's game server (local/) answers /local-config.js itself with window.DJ_LOCAL_CONFIG = { grafanaUrl,
 * mcpUrl, dashboardUrl, leaderboardUrl }, which turns local mode on (see local.js). Adding ?local to the address turns it on anywhere. */
window.DJ_LOCAL_CONFIG = null;
