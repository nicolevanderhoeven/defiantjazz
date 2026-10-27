<!--
SPOILERS: human-only. Never give this to the AI.
How the web game tells each story card as full-image panels: the pictures in web/assets/ and the short text on each. The terminal game doesn't use this file, and shows the cards as written.

Each "## ..." card with "image:" is one panel. The panels of a story card follow each other, starting with the one that has "card:":
  card:     the story card these panels tell, by its title. Every card the player sees needs panels.
  source:   with "card:", the fingerprint of the card's text that the panels were written from
  image:    the picture, by its name in IMAGES in web/build.py, or "none" for a black screen. A picture
            that isn't in web/assets/ yet shows as a placeholder panel until its file is added.
  where:    optional, one short line on where and when we are, above the headline
  headline: optional, a few words over the picture
  sound:    optional, what we hear, in a caption on the picture
  dim:      optional, "yes" shows the picture darker (the power cut)
  music:    optional, "yes" plays the jazz while the panel shows, when the build has the track
            (web/README.md says how); otherwise nothing plays
  style:    optional, "role" (the list shows as three tiles)
The panel's text goes under the picture, short: plain lines are captions, "[...]" lines say what's on
screen, "Name: ..." lines are spoken, and "> ..." lines are paper or a screen, shown close up.
A line that starts "(drawn) " is words the picture shows legibly: it isn't repeated under the picture,
but kept as its transcript, behind "Text in the picture" (or for screen readers only, when the panel
has nothing else to say). Write it as the picture has it. Without the picture yet, it shows as text.
If the card's text changes, `python3 web/build.py` stops and prints the new fingerprint: update the
panels to match, then "source:".

The cards after a panel, up to the next panel, are its hotspots, numbered in order: a marker on the
picture at "at: x, y" (percent of the picture's width and height, from the top left) that shows its
title and text when hovered, focused or tapped. "> ..." lines show as a close-up of paper. Hotspot
text comes from the story cards only, and never from the reveal. Placeholder panels have none: add
them when the picture lands, by looking at it.
-->

# Scene art

## The flyer
card: Kipsake
source: d466dca6
image: flyer-kipsake
(drawn) > KIPSAKE
(drawn) > WE RENT YOUR SLEEP
(drawn) > Earn while you sleep.
(drawn) > Happy holidays from Kipsake.
(drawn) > Check in. Drift off. Your sleepwalking self takes the night shift.
(drawn) > Wake rested, paid, and remembering nothing.
(drawn) > Our lullaby keeps you asleep.
(drawn) > Sweet dreams, Dreamers.

## The incident
card: The Defiant Jazz Incident
source: 11617c24
image: scene-3-elevator
where: Kipsake · Sleep Floor
headline: We need your help to solve a murder.
Tonight, our night supervisor, Mr. Hale, was found dead in the elevator, and the woman standing over him was holding a cable.
> Incident File SF-1008
> KIPSAKE · SLEEP FLOOR · OFFICE OF FLOOR SECURITY
> Subject: Death of Mr. Reginald Hale, Night Supervisor

## The floor indicator
at: 50, 9
Car 1 stopped at the Sleep Floor, with its doors open.

## The car
at: 50, 55
Where Mr. Hale was found.

## The Cocoa Hour
image: scene-break-room
where: Break Room 2 · Sleep Floor · 03:00
headline: The Cocoa Hour.
Agnes, Bertram and Clement, the three clerks of Deep Sleep Operations, are sleepwalkers on the Sleep Floor's night shift.
Tonight was the end-of-year Cocoa Hour, the floor's holiday party: a middle-of-the-night break to sit together and drink hot cocoa. It started at 03:00, with Mr. Hale, the night supervisor, who stays awake all shift.

## The emergency speaker
at: 36, 8
Break Room 2's emergency speaker. In a power outage, the emergency speakers come on and play the lullaby.

## Agnes
at: 17, 67
Agnes, a DSO clerk. When the power came back, she was the one in the elevator with Mr. Hale, holding a cable.

## Bertram
at: 37, 69
Bertram, another DSO clerk. Mr. Hale met him earlier tonight.

## Mr. Hale
at: 57, 47
Mr. Reginald Hale, the night supervisor, and the victim. He stays awake all shift.

## Clement
at: 77, 67
Clement, the third DSO clerk. Later, he'll call it a wonderful night, until it wasn't.

## Cocoa
at: 94, 37
The floor's holiday party: hot cocoa from the urn and a break to sit together.

## The power cut
image: scene-break-room
dim: yes
music: yes
where: Sleep Floor · 03:02
headline: The power went out.
sound: ♪ Jazz on the emergency speakers
The emergency speakers came on, but instead of the lullaby, they played jazz.
The jazz woke everyone up. For five minutes, Agnes, Bertram and Clement were their ordinary waking selves, in the dark, somewhere they'd never seen.

## The power comes back
image: title-splash
where: Sleep Floor · 03:07
headline: The power came back.
The jazz stopped. All three fell back asleep, and their sleepwalking selves remembered none of it.
Mr. Hale was found strangled in the elevator, which was stopped at the Sleep Floor with its doors open. Agnes was in the elevator with him, holding a cable.

## Your role
image: none
style: role
where: Your role
headline: Kipsake wants a name before dawn.
You're the investigator. There are three suspects: **Agnes**, **Bertram** and **Clement**. Name who killed Mr. Hale, and explain why.
- **ask**: Your AI has read Kipsake's records, and nothing else. It hasn't seen the interviews, the leads you follow, or anything you find. If you want it to know something, tell it.
- **investigate**: follow up three leads, in order: a crime scene, a visit to a suspect at home, and one last interview. Each time, you pick one of three options, and you'll only see the one you pick. Use them whenever you like.
- **accuse**: when you're ready, name the killer and say why. You can accuse before you've used every lead.

## Agnes
card: T-A · Agnes · 03:30
source: c3d5d270
image: portrait-agnes
where: An interview at Kipsake · 03:30
headline: Agnes
A DSO clerk, on a chair against a plain wall. You're off camera, asking the questions.
You: Agnes. Where were you when the lights went out?
Agnes: Having cocoa. By the window. Then I was in the elevator, holding a cable.
You: And Mr. Hale?
Agnes: I think I was trying to get it off him?
[She rubs her palms together, knuckles out. She avoids eye contact.]
[While you take notes, Agnes slips a folded piece of paper behind the badge card in her lanyard holder.]
Agnes: Will someone be taking apart the elevator? The phone panel, I mean?

## The badge card
at: 49, 73
Her Kipsake badge card, on a lanyard around her neck. Tucked behind it in the holder: the folded piece of paper she slipped there while you took notes.

## Bertram
card: T-B · Bertram · 03:40
source: cdeb83b0
image: portrait-bertram
where: An interview at Kipsake · 03:40
headline: Bertram
Another DSO clerk, on the same chair, wearing his lanyard.
You: Bertram. Mr. Hale met you earlier tonight?
Bertram: He said he'd step out during the Cocoa Hour. Something to pick up.
[He looks down and to the left.]
You: And when the lights went?
Bertram: I was having cocoa.
[He avoids eye contact.]
Bertram: Then I was in the corridor. Sore shoulder.

## The ice pack
at: 44, 38
He holds an ice pack to his right shoulder.

## His hand
at: 46, 85
A smudge of flour on the back of his free hand.

## Clement
card: T-C · Clement · 03:20
source: e4417310
image: portrait-clement
where: An interview at Kipsake · 03:20
headline: Clement
The third DSO clerk, on the same chair, wearing his lanyard, hands folded in his lap.
You: Clement. Where were you when the lights went out?
Clement: A wonderful night, until it wasn't.
Clement: The lights blinked, and I was by the speaker. Same as everyone, I expect.
Clement: Someone was screaming by the elevator.
[He pauses for two beats, then straightens his lanyard.]
Clement: Terrible about Mr. Hale.

## The sweater
at: 55, 62
A navy Christmas sweater, knitted with stripes and squares in blue, red, orange, green and white.

## His hands
at: 49, 86
Folded in his lap. His hands are clean.

## The Gazette
card: Outside World handout
source: 64da3e8d
image: scene-outside-world
These documents come from outside Kipsake. They aren't in Kipsake's telemetry, so the AI has never seen them.
(drawn) > **Port Quiet Gazette · Obituaries**
(drawn) > **June, 41.** June died suddenly in March in what her employer, Kipsake, has described as a workplace incident. She is survived by her brother, Clement. June loved the sea, terrible puns and the smell of waffles on Sunday mornings. A memorial will be held at the Port Quiet lighthouse. Instead of flowers, the family asks for answers.
(drawn) > **Port Quiet Gazette · Local**
(drawn) > **Kipsake quietly settles with dead employee's family.** Kipsake confirmed that an internal Procedure Revision 114 was withdrawn after the death of a sleepwalker in March. Records obtained by the Gazette show the revision was approved by night supervisor R. Hale. Kipsake declined to comment further.

## The evidence
card: Elevator car 1
source: 1fbafcfc
image: scene-elevator-evidence
[Floor Security's evidence, already laid out on a dark cloth, filmed from above. Three numbered markers.]
(drawn) > 03:09 · Elevator car 1
(drawn) > 1 · Ligature. Recovered from Agnes's hands.
(drawn) > 2 · Phone panel, cover loose. Three folded notes, still tucked inside, unopened.
(drawn) > 3 · Found in the victim's closed right hand. Not from his own clothing.
(drawn) > Hale's route, 03:01: Break Room 2 → corridor E → elevator lobby.
(drawn) > Corridor E and lobby compliance mics ran on emergency power.

## Marker 1
at: 18, 29
A grey cable in an evidence bag.

## Marker 2
at: 38, 45
Three folded notes, from the elevator's phone panel. Unopened.

## Marker 3
at: 22, 73
A small evidence bag holding a loose twist of five or six yarn threads, in navy, blue, red, orange, green and white.

## In daylight
at: 77, 80
Close-up of marker 3 in daylight, on a plain light surface: the twist of yarn threads, every colour clear.

## Two frames
card: Break Room 2
source: 2da2ea84
image: scene-break-room-camera
[Two frames from the Break Room 2 security camera. This is Floor Security's own footage, so it isn't in the telemetry the AI has. Grainy, filmed from high up, close on the room's emergency speaker and the chair beside it. The camera slowly zooms in on the cable and the napkin.]
(drawn) > BREAK ROOM 2 · SECURITY CAMERA
(drawn) > 03:01:20 · Voices. Cups. No music.
(drawn) > 03:02:00 · CAMERAS OFFLINE · Jazz begins.
(drawn) > 03:07:03

## 03:01:20
at: 21, 59
Nobody is in the shot. On the chair beside the speaker is a coiled grey cable, with a folded cloth napkin on top.

## 03:07:03
at: 77, 59
Same angle, same zoom. The cable and the napkin are gone from the chair.

## Clement
at: 87, 72
Clement sits on the floor beside the chair, in his Christmas sweater, wearing his lanyard with the badge facing out. Nobody else is in the shot.

## The waffle
card: Supply Room B
source: 9eae6fd9
image: scene-supply-room
[Floor Security's evidence, already laid out on a dark cloth, filmed from above.]
(drawn) > SR-B-03 · unregistered appliance (waffle iron) · confiscated
(drawn) > KIPSAKE · THE GOLDEN WAFFLE · Q3 · BERTRAM
(drawn) > Supply Room B · 03:18. Circuit C-7: Break Room 2 cocoa urn and lights, Supply Room B. Overload. Main breaker tripped, 03:02:00.

## The bag
at: 28, 46
An evidence bag holding a pale, half-cooked waffle.

## Peggy
card: Agnes at home
source: 965d6d35
image: scene-agnes-home
At home, Agnes goes by Peggy. Her waking self, Peggy, sits on the same chair. No lanyard.
You: Peggy? You were there last night.
(drawn) > 06:40 · Port Quiet · Peggy's flat
(drawn) Peggy: A man grabbed my wrist. 'You can't be here.' I ran. When I came back, he wasn't moving.
[She holds her bandaged wrist, arms wrapped around herself.]
You: Anything else?
(drawn) Peggy: This was in my pocket. It isn't mine.

## Her wrist
at: 34, 70
Her right wrist is in a crepe bandage.

## The napkin
at: 40, 85
A folded cloth napkin. On one corner, in laundry marker, a single block capital: "C".

## Bertram at home
card: Bertram at home
source: 5d5c0888
image: scene-bertram-home
Bertram's waking self sits on the same chair. No lanyard.
You: Bertram? You were on that floor last night.
(drawn) > 06:40 · Port Quiet · Bertram's flat
(drawn) Bertram: Someone trod on me in the dark. I grabbed at them.
(drawn) Bertram: They said sorry. Called me 'Waffles'. Who's Waffles?
[He looks puzzled.]

## His hand
at: 39, 76
He opens his hand toward the camera: a tuft of yarn threads in navy, blue, red, orange, green and white, twisted together into one piece.

## His shoulder
at: 40, 37
He touches his right shoulder.

## Clement at home
card: Clement at home
source: 92ccf641
image: scene-clement-home
where: Port Quiet · Clement's flat · 06:40
headline: Clement
You: Clement? You sleepwalk for Kipsake.
Clement: I don't remember work. That's rather the point.
[On the table, out of his cardboard folder, three things. Select each one on the picture to look closer.]
You: We read about June.
Clement: Then you know everything I do.
[He gathers them back into the folder and holds it against his chest.]

## Clement
at: 61, 39
Clement's waking self, at home. No lanyard, but he's wearing the Christmas sweater.

## The clipping
at: 43, 87
A clipping from the local paper, the Port Quiet Gazette, about Procedure Revision 114. "R. Hale" is circled in red.
> PORT QUIET GAZETTE
> … Procedure Revision 114 …
> ( R. Hale )  ← circled in red

## The evacuation plan
at: 55, 85
A printed photo of the Sleep Floor's fire-evacuation plan, taken where it hangs on a wall. Its red "You are here" dot is in Break Room 2. A route is drawn over it in pen: from Break Room 2, along corridor E, to the elevator, which is circled.
> ● You are here: Break Room 2
>   ↓  corridor E, in pen
> ( the elevator )  ← circled

## The photo
at: 65, 85
A photo of a woman standing by a lighthouse.

## Agnes pushed
card: Agnes
source: 9676ab5f
image: portrait-agnes-push
[Agnes, wearing her lanyard, in tears. Four notes in evidence bags lie in her lap.]
(drawn) > 04:30 · Kipsake · Agnes
You: These were in the elevator phone panel.
(drawn) Agnes: They're for her. The other me.
[She takes the folded note from behind her badge card and adds it to the pile.]
You: Why?
(drawn) Agnes: So she knows who to trust.
[She holds one bag up to the camera. The note in it is in joined-up handwriting, with "Waffles" underlined:]
(drawn) > WHO'S WHO. Mr. Hale: watch him. BERTRAM: tells Mr. Hale things. Careful. (Clement calls him 'Waffles'.) Clement: kind to me.

## Her wrist
at: 15, 76
Her right wrist is in a crepe bandage from the medical exam.

## Mr. Hale's note
at: 36, 74
One of the notes is the note found in Mr. Hale's jacket. It begins "If you are reading this, you are me…" and ends "Don't trust them."

## Bertram pushed
card: Bertram
source: b3c47a41
image: portrait-bertram-push
[Bertram, wearing his lanyard, the ice pack on his shoulder. His shoulders slump.]
(drawn) > 04:30 · Kipsake · Bertram
(drawn) You: You weren't having cocoa, Bertram.
(drawn) Bertram: Fine. I was making a waffle.
(drawn) You: And who brought you the ice?
(drawn) Bertram: Clement. 'Chill out, Waffles.' He's the only one who calls me that.

## Clement pushed
card: Clement
source: 1bb6e8d0
image: portrait-clement-push
[Clement, wearing his lanyard and Christmas sweater, with a clipboard and a Kipsake "Incident Statement" form.]
(drawn) > 04:30 · Kipsake · Clement
You: For the record, Clement. In your own hand. What did you do after the lights came back?
[He writes without speaking, in block capitals, line by line:]
(drawn) > KIPSAKE · INCIDENT STATEMENT
(drawn) > 03:07 LIGHTS RETURNED. I WAS SEATED BY THE SPEAKER.
(drawn) > I WENT TO THE CORRIDOR AND CHECKED ON WAFFLES (SHOULDER).
(drawn) > I HOPE ~~PEGGY~~ AGNES IS BEING LOOKED AFTER.
[The word "Peggy" is crossed out with a single line, but you can still read it. His pen hovers over it for a moment.]
(drawn) Clement: Is that all?

## His hand
at: 45, 57
His hands are clean. He holds out the clipboard to you.
