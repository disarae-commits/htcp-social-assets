# HTCP moment clips

The evening post (concept B slot) on Instagram, TikTok, YouTube Shorts and Threads is a short "moment": an 8 to 10 second stock clip with one short phrase on it. Morning posts stay the guide carousel and slideshow.

- `clips.json`: approved clips from Disa's Google Drive "Short videos" folder (calm WCEO desk, planner, home and coffee shots; no alcohol, money, luxury or readable signs).
- `moment.py`: renders the video. Read its docstring.
- `log.json`: one entry per day: date, kind, phrase, clip ids. Used to avoid repeats.
- `eligible.py`: run `python3 eligible.py YYYY-MM-DD` to list the only clips allowed today, and `--check ID ID` before rendering. Never use a clip it blocks.

## Rotation
- Kind alternates every day: if the last log entry was `funny`, today is `support`, and the reverse. Start with `funny`.
- Clips: a video may NOT go out again until at least 30 days after it last went out, even with different words. Clips with the same `group` in clips.json count as the same video. Check every log entry from the last 30 days before picking.
- If there are not enough unused clips to reach 8 seconds, do NOT reuse one early: skip the moment posts that day and say so in the final message so Disa can add clips.
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
