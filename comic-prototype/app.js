(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const scenes = window.COMIC_SCENES;
  const descriptions = [
    'A corporate advertisement: peaceful sleep beside rows of office workers.',
    'Clerks and their supervisor at a cocoa celebration in a teal break room.',
    'An open elevator in a dark corridor under red emergency lighting.',
    'Clement in his flat, holding a box, wearing a fringed scarf.'
  ];
  let sceneIndex = 0, frameIndex = 0;
  const scene = () => scenes[sceneIndex];

  function log(text, command = false) {
    const p = document.createElement('p');
    p.textContent = (command ? '❯ ' : '') + text;
    if (command) p.className = 'command';
    $('transcript').append(p);
    $('transcript').scrollTop = $('transcript').scrollHeight;
  }

  function button(text, action) {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = text;
    b.onclick = action;
    return b;
  }

  function renderStatements(s) {
    const panels = s.witnesses.map((w, i) => {
      const beat = w.beats[frameIndex];
      const card = document.createElement('article');
      card.className = 'interview';
      const heading = document.createElement('h2');
      heading.textContent = `${w.name} / ${w.time}`;
      const portrait = document.createElement('div');
      portrait.className = 'portrait';
      portrait.style.backgroundPosition = `${i * 50}% center`;
      portrait.setAttribute('role', 'img');
      portrait.setAttribute('aria-label', w.description);
      const question = document.createElement('p');
      question.className = 'interviewer';
      question.textContent = beat[0] ? `OKONJO / ${beat[0]}` : 'OKONJO / CONTINUED STATEMENT';
      const bubble = document.createElement('blockquote');
      bubble.className = 'speech-bubble';
      bubble.textContent = beat[1];
      const caption = document.createElement('p');
      caption.className = 'action-caption';
      caption.textContent = beat[2];
      const inspect = button(`Inspect ${w.name}`, () => run(`EXAMINE ${w.key}`));
      inspect.className = 'inspect-witness';
      card.append(heading, portrait, question, bubble, caption, inspect);
      return card;
    });
    $('statement-page').replaceChildren(...panels);
  }

  function render() {
    const s = scene(), f = s.frames[frameIndex];
    const statements = s.layout === 'statements';
    $('location').textContent = s.location;
    $('art').style.backgroundImage = `url('${s.image || 'assets/scenes.png'}')`;
    $('art').style.backgroundSize = s.image ? '100% 100%' : '100% 400%';
    $('art').style.backgroundPosition = s.image ? 'center' : `center ${s.art * 100 / 3}%`;
    $('art').setAttribute('aria-label', s.alt || descriptions[s.art] || '');
    $('art').style.filter = s.art === 2 && frameIndex < 2 ? 'brightness(.66) saturate(.8)' : 'none';
    document.querySelector('.comic').classList.toggle('advert', sceneIndex === 0);
    document.querySelector('.comic').classList.toggle('statements', statements);
    $('statement-page').hidden = !statements;
    if (statements) renderStatements(s);
    $('scene-speech').hidden = true;
    $('eyebrow').textContent = f[0];
    $('title').textContent = f[1];
    $('subtitle').textContent = f[2];
    $('sound-caption').textContent = f[4] || '';
    $('sound-caption').hidden = !f[4];
    $('frame-label').textContent = `CHAPTER 0${sceneIndex + 1} / PANEL 0${frameIndex + 1} OF 0${s.frames.length}`;
    $('next').textContent = sceneIndex === scenes.length - 1 && frameIndex === s.frames.length - 1 ? 'Return to opening ↺' : 'Next panel →';
    $('hotspots').replaceChildren();
    if (!statements) s.objects.forEach((o, i) => {
      const b = button(String(i + 1), () => run(o[3]));
      b.className = 'hotspot';
      b.style.left = `calc(${o[1]}% - 15px)`;
      b.style.top = `calc(${o[2]}% - 15px)`;
      b.setAttribute('aria-label', o[3]);
      $('hotspots').append(b);
    });
    $('suggestions').replaceChildren(...s.suggest.map(c => button(c, () => run(c))));
    $('chapters').replaceChildren(...scenes.map((s, i) => {
      const b = button('', () => enter(i));
      const small = document.createElement('small');
      small.textContent = `0${i + 1} / SCENE`;
      b.append(small, document.createTextNode(s.name));
      b.setAttribute('aria-current', String(i === sceneIndex));
      return b;
    }));
  }

  function enter(index, scroll = true) {
    sceneIndex = index;
    frameIndex = 0;
    $('transcript').replaceChildren();
    render();
    log(scene().frames[0][3]);
    if (scroll) document.querySelector('.comic').scrollIntoView({ block: 'start' });
  }

  function next() {
    if (frameIndex < scene().frames.length - 1) {
      frameIndex++;
      render();
      log(scene().frames[frameIndex][3]);
      if (scene().layout === 'statements') document.querySelector('.comic').scrollIntoView({ block: 'start' });
    } else enter((sceneIndex + 1) % scenes.length);
  }

  function showClue(key) {
    const clue = window.COMIC_CLUES[key];
    $('clue-title').textContent = clue.title;
    $('clue-body').innerHTML = clue.body;
    $('clue').showModal();
  }

  function run(raw) {
    const value = raw.trim();
    if (!value) return;
    log(value.toUpperCase(), true);
    const cmd = value.toLowerCase().replace(/[.!?]+$/, '').replace(/\s+/g, ' ');
    if (cmd === 'help') {
      log('LOOK describes the scene. EXAMINE <object> inspects it. TALK <person> starts a conversation. NEXT advances a panel. RESTART returns to the opening. Click numbered markers for the same commands. Statement pages show all three interviews in parallel; NEXT continues their statements. This demo uses authored responses; it has no AI connection.');
      return;
    }
    if (cmd === 'restart') { enter(0); return; }
    if (cmd === 'next') { next(); return; }
    if (cmd === 'look') {
      log(scene().frames[frameIndex][3] + '\nYou can inspect: ' + scene().objects.map(o => o[0]).join(', ') + '.');
      return;
    }
    const talk = cmd.match(/^(?:talk(?: to)?|ask) (.+)$/);
    if (talk) {
      const who = talk[1] === 'c' ? 'clement' : talk[1];
      const witness = scene().witnesses?.find(w => w.key === who);
      const response = witness ? `${witness.name}: “${witness.beats[frameIndex][1]}”` : scene().talk[who];
      log(response || 'No response from that person here. Try: ' + Object.keys(scene().talk).map(n => 'TALK ' + n.toUpperCase()).join(', ') + '.');
      if (response && !scene().witnesses) {
        $('scene-speech').textContent = response;
        $('scene-speech').hidden = false;
      }
      return;
    }
    const inspect = cmd.match(/^(?:examine|inspect|look at) (.+)$/);
    if (inspect) {
      const name = inspect[1].replace(/^the /, '');
      const o = scene().objects.find(o => o[0] === name || o[4].includes(name));
      if (o) { log(o[5]); if (o[6]) showClue(o[6]); return; }
    }
    log('That command is not available here. Try LOOK, HELP, or one of the suggested commands below.');
  }

  $('command-form').onsubmit = e => {
    e.preventDefault();
    const value = $('command').value;
    $('command').value = '';
    run(value);
  };
  $('next').onclick = () => run('NEXT');
  $('restart').onclick = () => run('RESTART');
  $('close-clue').onclick = () => $('clue').close();
  enter(0, false);
})();
