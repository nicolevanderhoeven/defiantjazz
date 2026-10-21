/* Human-facing opening testimonies adapted from game/SPOILERS-content/testimonies.md.
 * Never include these scenes in the investigating AI's context. */
(() => {
  const witnesses = [
    { name: 'Agnes', time: '03:30', key: 'agnes', description: 'Agnes wears a plain top and lanyard. She rubs her palms together and avoids eye contact.',
      beats: [
        ['Agnes. Where were you when the lights went out?', 'Having cocoa. By the window. Then I was in the elevator, holding a cable.', 'Her hands keep moving.'],
        ['And Mr. Hale?', 'I think I was trying to get it off him?', 'She rubs her palms together, knuckles out.'],
        ['', 'Will someone be taking apart the elevator? The phone panel, I mean?', 'While you take notes, Agnes slips a folded paper behind her badge card.']
      ] },
    { name: 'Bertram', time: '03:40', key: 'bertram', description: 'Bertram holds an ice pack to his right shoulder. There is flour on the back of his free hand.',
      beats: [
        ['Bertram. Mr. Hale met you earlier tonight?', "He said he'd step out during the Cocoa Hour. Something to pick up.", 'He looks down and to the left.'],
        ['And when the lights went?', 'I was having cocoa.', 'He avoids eye contact.'],
        ['', 'Then I was in the corridor. Sore shoulder.', 'The ice pack stays pressed to his right shoulder.']
      ] },
    { name: 'Clement', time: '03:20', key: 'clement', description: 'Clement wears his fringed scarf and lanyard. His clean hands are folded in his lap.',
      beats: [
        ['Clement. Where were you when the lights went out?', "A wonderful night, until it wasn't.", 'His hands are folded neatly in his lap.'],
        ['', 'The lights blinked, and I was by the speaker. Same as everyone, I expect.', 'He wears a scarf with a fringe of many different colours.'],
        ['', 'Someone was screaming by the elevator.\n\nTerrible about Mr. Hale.', 'He pauses for two beats, then straightens his lanyard.']
      ] }
  ];
  const statement = {
    name: 'The statements', location: 'AFTER THE OUTAGE / FLOOR SECURITY / SELECTED INTERVIEWS',
    layout: 'statements', witnesses,
    frames: ['What they remember.', 'What they cannot explain.', 'What they leave you with.'].map((title, i) => [
      `FLOOR SECURITY / STATEMENTS ${i + 1} OF 3`, title, '',
      'You interviewed all three soon after the power came back. These are their statements, not verified events.\n\n' + witnesses.map(w => `${w.name} · ${w.time}\n${w.beats[i][0] ? 'You: “' + w.beats[i][0] + '”\n' : ''}${w.name}: “${w.beats[i][1]}”\n${w.beats[i][2]}`).join('\n\n')
    ]),
    objects: witnesses.map((w, i) => [w.key, 18 + i * 32, 50, `TALK ${w.key.toUpperCase()}`, w.key === 'clement' ? ['c', 'scarf'] : [], w.description]),
    talk: Object.fromEntries(witnesses.map(w => [w.key, `${w.name}: “${w.beats[0][1]}”`])),
    suggest: ['TALK AGNES', 'TALK BERTRAM', 'TALK CLEMENT', 'NEXT']
  };
  window.COMIC_SCENES.splice(3, 0, statement);
  const ad = window.COMIC_SCENES[0];
  ad.image = 'assets/sleep-self-v4.png';
  ad.alt = 'A double-exposure sequence of one woman: asleep in bed, a transparent version walking in the middle foreground in front of the bed, then solid at her desk working through the night.';
  ad.objects[1] = ['desk', 84, 64, 'EXAMINE DESK', ['workers', 'worker', 'office', 'computer', 'sleepwalker', 'sleepwalkers'], 'The same woman works at a glowing computer beneath the night windows. Kipsake calls it productive sleep. She will remember none of the shift.'];
  ad.objects.push(['self', 48, 40, 'EXAMINE SELF', ['ghost', 'sleeping self', 'dream self', 'double'], 'One woman, three moments: asleep in bed, getting up, working at her desk. The transparent middle image suggests movement through time. Kipsake promises she can do it all without waking.']);
  ad.suggest = ['EXAMINE SELF', 'EXAMINE DESK', 'TALK RECRUITER'];
})();
