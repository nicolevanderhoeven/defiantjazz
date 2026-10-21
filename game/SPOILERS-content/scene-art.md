<!--
SPOILERS: human-only. Never give this to the AI.
The web game's scene art (web/assets/scene-*.webp) and what goes with it. The terminal game doesn't use this file.

Each "## scene-..." card is one scene image, shown with the story card named in "card:" (by its title):
  where:   one line on where and when we are, above the image
  caption: a short caption under the image
  story:   optional, where the art doesn't match the story: the story's version, in one line
  before:  optional, the image goes above the body line that starts with this text, not at the top
  source:  needed with a body: the fingerprint of the card's text that the body was written from
  body:    optional, the web game's text for that card, in place of the card's own. It leaves out
           what the image shows. Without a body, the web game shows the card as written.
If the card's text changes, `python3 web/build.py` stops and prints the new fingerprint:
update the body to match, then "source:".

The cards after a scene, up to the next scene, are its hotspots, numbered in order: a marker
on the image at "at: x, y" (percent of the image's width and height, from the top left) that
shows its title and text when hovered, focused or tapped. "> ..." lines show as a close-up of
paper. Hotspot text comes from the story cards only, and never from the reveal.
-->

# Scene art

## scene-1-broadcast
card: Kipsake
where: A Kipsake advert
caption: Asleep, and at work.
story: In the story, Dreamers check in at Kipsake and sleep in pods, not at home.
source: db391f81
Hi! I'm with Kipsake.
You work hard all day. So why should your nights go to waste?
At Kipsake, we rent your sleep.
Each night, you check in, settle into your pod, and drift off.
Your sleepwalking self works the night shift for you.
In the morning, you wake up rested, paid, and remembering nothing at all.
And don't worry: our lullaby keeps you sound asleep all night long. Even in a power outage.
**Kipsake. Earn while you sleep.**
Sweet dreams, Dreamers.

## Asleep
at: 14, 55
Each night, you check in, settle into your pod, and drift off.

## Kipsake
at: 66, 32
Kipsake rents your sleep. Earn while you sleep.

## The night shift
at: 85, 69
Your sleepwalking self works the night shift for you. In the morning, you remember nothing at all.

## scene-2-break-room
card: The Defiant Jazz Incident
where: Break Room 2 · Sleep Floor · 03:00
caption: The Cocoa Hour.
story: In the story, it's just the three clerks, Agnes, Bertram and Clement, with Mr. Hale.
before: What happened that night
source: 08093bd7
*The power went out for five minutes. When it came back, the supervisor was dead in the elevator, and the woman standing over him was holding the cable that killed him.*

> Incident File SF-1008
> KIPSAKE · SLEEP FLOOR · OFFICE OF FLOOR SECURITY
> Subject: Death of Mr. Reginald Hale, Night Supervisor

**What happened that night**

- **02:58.** Agnes, Bertram and Clement, the three clerks of Deep Sleep Operations, are sleepwalkers on the Sleep Floor's night shift. They met their quota for the quarter. Their reward was a Cocoa Hour, with no music. It started at 03:00, with the three of them and Mr. Hale, the night supervisor, who stays awake all shift.
- **03:02.** The power went out. The emergency speakers came on, but instead of the lullaby, they played jazz. The jazz woke everyone up. For five minutes, Agnes, Bertram and Clement were their ordinary waking selves, in the dark, somewhere they'd never seen.
- **03:07.** The power came back and the jazz stopped. All three fell back asleep, and their sleepwalking selves remembered none of it. Mr. Hale was found strangled in the elevator, which was stopped at the Sleep Floor with its doors open. Agnes was in the elevator with him, holding a cable.

There are three suspects: **Agnes**, **Bertram** and **Clement**.

**Your role**

You're the investigator. Kipsake wants a name before dawn, when the shift wakes up. Your job is to name who killed Mr. Hale and explain why.

- **ask**: Your AI has read Kipsake's records, and nothing else. It hasn't seen the interviews, the leads you follow, or anything you find. If you want it to know something, tell it.
- **investigate**: you can follow up three leads, in order: a crime scene, a visit to a suspect at home, and one last interview. Each time, you pick one of three options, and you'll only see the one you pick. Use them whenever you like, between questions to the AI. You can accuse before you've used them all.
- **accuse**: when you're ready, name the killer and say why.

## The emergency speaker
at: 10, 11
Break Room 2's emergency speaker. In a power outage, the emergency speakers come on and play the lullaby.

## Cocoa
at: 15, 84
The reward for meeting the quarter's quota: hot cocoa, and a middle-of-the-night break to sit together, with no music.

## Mr. Hale
at: 46, 31
Mr. Reginald Hale, the night supervisor. He stays awake all shift.

## Clement
at: 59, 64
Clement, one of the three sleepwalking clerks of Deep Sleep Operations.

## scene-3-elevator
card: Elevator car 1
where: Elevator car 1 · Sleep Floor · 03:09
caption: Where Mr. Hale was found.
story: In the story, the power is back by 03:09, and Floor Security has laid the evidence out on a cloth.

## The floor indicator
at: 50, 9
Car 1 stopped at the Sleep Floor, with its doors open.

## The car
at: 50, 55
Where Mr. Hale was found. Floor Security's evidence from here is laid out below.

## scene-4-clement-home
card: Clement at home
where: Clement's flat · Port Quiet · 06:40
caption: Clement's waking self, with the folder.
story: In the story, it's morning, he wears no lanyard, and the three things are in a cardboard folder, not a box.
source: 4f4f4ff4
You: Clement? You sleepwalk for Kipsake.
Clement: I don't remember work. That's rather the point.
[In the open folder, three things: a clipping from the local paper, a printed photo of the Sleep Floor's fire-evacuation plan, and a photo of a woman by a lighthouse. Select each one on the picture to look closer.]
You: We read about June.
Clement: Then you know everything I do.
[He closes the folder and holds it against his chest.]

## Clement
at: 22, 42
Clement's waking self, at home. He's wearing the fringed scarf.

## The folder
at: 62, 62
An open cardboard folder, lying flat, with three things inside.

## The clipping
at: 38, 84
A clipping from the local paper, the Port Quiet Gazette, about Procedure Revision 114. "R. Hale" is circled in red.
> PORT QUIET GAZETTE
> … Procedure Revision 114 …
> ( R. Hale )  ← circled in red

## The evacuation plan
at: 50, 73
A printed photo of the Sleep Floor's fire-evacuation plan, taken where it hangs on a wall. Its red "You are here" dot is in Break Room 2. A route is drawn over it in pen: from Break Room 2, along corridor E, to the elevator, which is circled.
> ● You are here: Break Room 2
>   ↓  corridor E, in pen
> ( the elevator )  ← circled

## The photo
at: 48, 46
A photo of a woman standing by a lighthouse.
