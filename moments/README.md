# HTCP moment clips

The evening post (concept B slot) on Instagram, TikTok, YouTube Shorts and Threads is a short "moment": an 8 to 10 second stock clip with one short phrase on it. Morning posts stay the guide carousel and slideshow.

- `clips.json`: approved clips from Disa's Google Drive "Short videos" folder (calm WCEO desk, planner, home and coffee shots; no alcohol, money, luxury or readable signs).
- `moment.py`: renders the video. Read its docstring.
- `log.json`: one entry per day: date, kind, phrase, clip ids. Used to avoid repeats.

## Rotation
- Kind alternates every day: if the last log entry was `funny`, today is `support`, and the reverse. Start with `funny`.
- Clips: never reuse a clip used in the last 10 days.
- Phrases: never repeat one from the log.

## Writing the phrase
One short line, at most 70 characters, plain words, no dashes, no hashtags. It should feel like a friend texting you, not a poster.

Funny ("Quick nudge") examples of the voice:
- Reminder to switch your laundry.
- Your tabs called. They want to be closed.
- The project is not going to finish itself. Rude, but true.
- Drink some water. Then open the file.
- That email you have been avoiding is two sentences long.

Support ("A little support") examples of the voice:
- You do not have to finish it today. Just open it.
- Ten minutes still counts.
- Starting late is still starting.
- Rest is part of the project too.
- You are not behind. You are in the middle.

Write new ones in this voice; do not copy other people's quotes or memes, and never attribute a line to a real person.
