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
  style:    optional, "flyer" (the text is the flyer's printed copy, shown only while its picture is
            missing, and read out to screen readers) or "role" (the list shows as three tiles)
The panel's text goes under the picture, short: plain lines are captions, "[...]" lines say what's on
screen, "Name: ..." lines are spoken, and "> ..." lines are paper or a screen, shown close up.
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
source: db391f81
image: flyer-kipsake
style: flyer
> KIPSAKE
> At Kipsake, we rent your sleep.
> You work hard all day. So why should your nights go to waste?
> Each night, you check in, settle into your pod, and drift off. Your sleepwalking self works the night shift for you.
> In the morning, you wake up rested, paid, and remembering nothing at all.
> Our lullaby keeps you sound asleep all night long. Even in a power outage.
> **Earn while you sleep.**
> Sweet dreams, Dreamers.

## The incident
card: The Defiant Jazz Incident
source: 08093bd7
image: scene-3-elevator
where: Kipsake · Sleep Floor
headline: The power went out for five minutes.
When it came back, the supervisor was dead in the elevator, and the woman standing over him was holding the cable that killed him.
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
02:58. Agnes, Bertram and Clement, the three clerks of Deep Sleep Operations, are sleepwalkers on the Sleep Floor's night shift. They met their quota for the quarter.
Their reward was a middle-of-the-night break to sit together and drink hot cocoa, with no music. It started at 03:00, with Mr. Hale, the night supervisor, who stays awake all shift.

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
Mr. Reginald Hale, the night supervisor. He stays awake all shift.

## Clement
at: 77, 67
Clement, the third DSO clerk. Later, he'll call it a wonderful night, until it wasn't.

## Cocoa
at: 94, 37
The reward for meeting the quarter's quota: hot cocoa, and a middle-of-the-night break to sit together, with no music.

## The power cut
image: scene-break-room
dim: yes
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

## Agnes, 1
card: T-A · Agnes · 03:30
source: c3d5d270
image: portrait-agnes
where: An interview at Kipsake · 03:30
headline: Agnes
A DSO clerk, on a chair against a plain wall. You're off camera, asking the questions.
You: Agnes. Where were you when the lights went out?
Agnes: Having cocoa. By the window. Then I was in the elevator, holding a cable.

## Agnes, 2
image: portrait-agnes
where: An interview at Kipsake · 03:30
headline: Agnes
You: And Mr. Hale?
Agnes: I think I was trying to get it off him?
[She rubs her palms together, knuckles out. She avoids eye contact.]

## Agnes, 3
image: portrait-agnes
where: An interview at Kipsake · 03:30
headline: Agnes
[While you take notes, Agnes slips a folded piece of paper behind the badge card in her lanyard holder.]
Agnes: Will someone be taking apart the elevator? The phone panel, I mean?

## The badge card
at: 49, 73
Her Kipsake badge card, on a lanyard around her neck. Tucked behind it in the holder: the folded piece of paper she slipped there while you took notes.

## Bertram, 1
card: T-B · Bertram · 03:40
source: cdeb83b0
image: portrait-bertram
where: An interview at Kipsake · 03:40
headline: Bertram
Another DSO clerk, on the same chair, wearing his lanyard.
You: Bertram. Mr. Hale met you earlier tonight?
Bertram: He said he'd step out during the Cocoa Hour. Something to pick up.
[He looks down and to the left.]

## The ice pack
at: 44, 38
He holds an ice pack to his right shoulder.

## His hand
at: 46, 85
A smudge of flour on the back of his free hand.

## Bertram, 2
image: portrait-bertram
where: An interview at Kipsake · 03:40
headline: Bertram
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

## Clement, 1
card: T-C · Clement · 03:20
source: b6e5e197
image: portrait-clement
where: An interview at Kipsake · 03:20
headline: Clement
The third DSO clerk, on the same chair, wearing his lanyard, hands folded in his lap.
You: Clement. Where were you when the lights went out?
Clement: A wonderful night, until it wasn't.
Clement: The lights blinked, and I was by the speaker. Same as everyone, I expect.

## The scarf
at: 55, 62
A fringed scarf, looped once so both ends hang down his chest. The threads of its fringe are many different colours.

## His hands
at: 49, 86
Folded in his lap. His hands are clean.

## Clement, 2
image: portrait-clement
where: An interview at Kipsake · 03:20
headline: Clement
Clement: Someone was screaming by the elevator.
[He pauses for two beats, then straightens his lanyard.]
Clement: Terrible about Mr. Hale.

## The scarf
at: 55, 62
A fringed scarf, looped once so both ends hang down his chest. The threads of its fringe are many different colours.

## His hands
at: 49, 86
Folded in his lap. His hands are clean.

## The obituary
card: Outside World handout
source: 64da3e8d
image: scene-outside-world
where: The Outside World
headline: Port Quiet Gazette
These documents come from outside Kipsake. They aren't in Kipsake's telemetry, so the AI has never seen them.
> **Port Quiet Gazette · Obituaries**
> **June, 41.** June died suddenly in March in what her employer, Kipsake, has described as "a workplace incident." She is survived by her brother, Clement. June loved the sea, terrible puns and the smell of waffles on Sunday mornings. A memorial will be held at the Port Quiet lighthouse. Instead of flowers, the family asks for answers.

## The local news
image: scene-outside-world
where: The Outside World
headline: Port Quiet Gazette
> **Port Quiet Gazette · Local**
> **Kipsake quietly settles with dead employee's family.** Kipsake confirmed that an internal "Procedure Revision 114" was withdrawn after the death of a sleepwalker in March. Records obtained by the Gazette show the revision was approved by night supervisor R. Hale. Kipsake declined to comment further.

## The evidence
card: Elevator car 1
source: 072db044
image: scene-elevator-evidence
where: Elevator car 1 · 03:09 · as found
headline: Floor Security's evidence
[Laid out on a dark cloth, filmed from above. Three numbered markers.]
> 1 · A grey cable in an evidence bag. Ligature. Recovered from Agnes's hands.
> 2 · Three folded notes. Phone panel, cover loose. Three folded notes, still tucked inside, unopened.
> 3 · A small evidence bag holding a loose twist of five or six threads, in several different colours. Found in the victim's closed right hand. Not from his own clothing.

## Mr. Hale's route
image: scene-elevator-evidence
where: Elevator car 1 · 03:09 · as found
headline: Mr. Hale's route
> Mr. Hale's route, 03:01: Break Room 2 → corridor E → elevator lobby.
> The corridor E and lobby compliance mics ran on emergency power.
[Close-up of marker 3 in daylight, on a plain light surface: the twist of threads, every colour clear.]

## 03:01:20
card: Break Room 2
source: b0b1e7a8
image: scene-break-room-camera-1
where: Break Room 2 camera · 03:01:20
headline: Floor Security's own footage
sound: Voices murmuring, cups, no music
[Grainy, filmed from high up, close on the emergency speaker and the chair beside it. It isn't in the telemetry the AI has.]
[Nobody is in the shot. On the chair beside the speaker is a coiled grey cable, with a folded cloth napkin on top. The camera slowly zooms in on the cable and the napkin.]

## 03:02:00
image: none
where: Break Room 2 camera · 03:02:00
headline: Cameras offline.
sound: ♪ Jazz starts playing on the emergency speaker
[The screen is black.]

## 03:07:03
image: scene-break-room-camera-2
where: Break Room 2 camera · 03:07:03
headline: Same angle, same zoom.
[The cable and the napkin are gone from the chair. Clement sits on the floor beside the chair, in his fringed scarf, wearing his lanyard with the badge facing out. Nobody else is in the shot.]

## The waffle
card: Supply Room B
source: 9eae6fd9
image: scene-supply-room
where: Supply Room B · 03:18
headline: Floor Security's evidence
[Laid out on a dark cloth, filmed from above.]
> An evidence bag holding a pale, half-cooked waffle, tagged "SR-B-03 · unregistered appliance (waffle iron) · confiscated."
> Beside it, a printed certificate in a plastic sleeve: "KIPSAKE · THE GOLDEN WAFFLE · Q3 · BERTRAM"

## Circuit C-7
image: scene-supply-room
where: Supply Room B · 03:18
headline: Circuit C-7
> Supply Room B · 03:18. Circuit C-7 (Break Room 2 cocoa urn and lights, Supply Room B): overload. Main breaker tripped, 03:02:00.

## Peggy, 1
card: Agnes at home
source: 965d6d35
image: scene-agnes-home
where: Port Quiet · Peggy's flat · 06:40
headline: Peggy
At home, Agnes goes by Peggy. Her waking self sits on the same chair. No lanyard. Her right wrist is in a crepe bandage.
You: Peggy? You were there last night.
Peggy: A man grabbed my wrist. "You can't be here." I ran.

## Peggy, 2
image: scene-agnes-home
where: Port Quiet · Peggy's flat · 06:40
headline: Peggy
[She holds her bandaged wrist, arms wrapped around herself.]
Peggy: When I came back, he wasn't moving.
You: Anything else?
Peggy: This was in my pocket. It isn't mine.

## The napkin
image: scene-agnes-home
where: Port Quiet · Peggy's flat · 06:40
headline: The napkin
[She holds out a folded cloth napkin. Close-up: on one corner, in laundry marker, a single block capital:]
> C

## Bertram at home, 1
card: Bertram at home
source: 61ef3767
image: scene-bertram-home
where: Port Quiet · Bertram's flat · 06:40
headline: Bertram
Bertram's waking self sits on the same chair. No lanyard.
You: Bertram? You were on that floor last night.
Bertram: Someone trod on me in the dark. I grabbed at them.

## Bertram at home, 2
image: scene-bertram-home
where: Port Quiet · Bertram's flat · 06:40
headline: Bertram
[He opens his hand toward the camera: a tuft of threads in several different colours, twisted together into one piece. Then he touches his right shoulder.]
Bertram: They said sorry. Called me "Waffles". Who's Waffles?
[He looks puzzled.]

## Clement at home, 1
card: Clement at home
source: 4f4f4ff4
image: scene-clement-home
where: Port Quiet · Clement's flat · 06:40
headline: Clement
You: Clement? You sleepwalk for Kipsake.
Clement: I don't remember work. That's rather the point.
[On the table, out of his cardboard folder, three things. Select each one on the picture to look closer.]

## Clement
at: 61, 39
Clement's waking self, at home. No lanyard, but he's wearing the fringed scarf.

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

## Clement at home, 2
image: scene-clement-home
where: Port Quiet · Clement's flat · 06:40
headline: Clement
You: We read about June.
Clement: Then you know everything I do.
[He gathers them back into the folder and holds it against his chest.]

## Agnes pushed, 1
card: Agnes
source: 9676ab5f
image: portrait-agnes-push
where: An interview at Kipsake · 04:30
headline: Agnes
[Wearing her lanyard. Her right wrist is in a crepe bandage from the medical exam. Four notes in evidence bags lie in her lap.]
> One of them is the note found in Mr. Hale's jacket. It begins "If you are reading this, you are me…" and ends "Don't trust them."
You: These were in the elevator phone panel.
Agnes: They're for her. The other me.

## Agnes pushed, 2
image: portrait-agnes-push
where: An interview at Kipsake · 04:30
headline: Agnes
[She takes the folded note from behind her badge card and adds it to the pile.]
You: Why?
Agnes: So she knows who to trust.

## Agnes pushed, 3
image: portrait-agnes-push
where: An interview at Kipsake · 04:30
headline: Who's who
[In tears, she holds one bag up to the camera. The note in it is in joined-up handwriting, with "Waffles" underlined:]
> WHO'S WHO. Mr. Hale: watch him. BERTRAM: tells Mr. Hale things. Careful. (Clement calls him 'Waffles'.) Clement: kind to me.

## Bertram pushed, 1
card: Bertram
source: b3c47a41
image: portrait-bertram-push
where: An interview at Kipsake · 04:30
headline: Bertram
[Wearing his lanyard, the ice pack on his shoulder.]
You: You weren't having cocoa, Bertram.
[His shoulders slump.]
Bertram: Fine. I was making a waffle.

## Bertram pushed, 2
image: portrait-bertram-push
where: An interview at Kipsake · 04:30
headline: Bertram
You: And who brought you the ice?
Bertram: Clement. 'Chill out, Waffles.' He's the only one who calls me that.

## Clement pushed, 1
card: Clement
source: d528783f
image: portrait-clement-push
where: An interview at Kipsake · 04:30
headline: Clement
[Wearing his lanyard and scarf. On his lap is a clipboard with a Kipsake "Incident Statement" form.]
You: For the record, Clement. In your own hand. What did you do after the lights came back?

## Clement pushed, 2
image: portrait-clement-push
where: An interview at Kipsake · 04:30
headline: Incident Statement
[He writes without speaking. What he writes on the form, in block capitals, line by line:]
> 03:07 Lights returned. I was seated by the speaker.
> I went to the corridor and checked on Waffles (shoulder).
> I hope ~~Peggy~~ Agnes is being looked after.

## Clement pushed, 3
image: portrait-clement-push
where: An interview at Kipsake · 04:30
headline: Clement
[The word "Peggy" is crossed out with a single line, but you can still read it. His pen hovers over it for a moment. His hands are clean. He holds out the clipboard to you.]
Clement: Is that all?
