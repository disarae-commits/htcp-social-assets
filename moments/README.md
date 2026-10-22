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

## The words must match the clip
The phrase is about what the viewer SEES. Never put a laundry line over a coffee cup.
1. Pick today's theme from the tags with enough allowed clips (`python3 eligible.py YYYY-MM-DD` prints TAGS).
2. List that tag's clips (`--tag coffee`) and pick 2 that show the same kind of thing.
3. Extract a frame from the middle of each clip and LOOK at it. Note the main thing on screen (a mug, a planner, slippers, a laptop).
4. Write the phrase about that thing. Funny: a nudge tied to it ("Your coffee is cold again. Drink it anyway and open the file."). Support: a kind line tied to it ("Slippers on. Ten minutes counts.").
5. If the clips do not show what the phrase names, change the phrase or the clips. Never ship a mismatch.

## Writing the phrase
One short line, at most 70 characters, plain words, no dashes, no hashtags. It should feel like a friend texting you, not a poster.

Funny ("Quick nudge") examples of the voice:
- (planner clip) That to do list will not cross itself off. Rude.
- (laptop clip) Your tabs called. They want to be closed.
- (coffee clip) Your coffee went cold again. Drink it anyway and open the file.
- (phone clip) That email you have been avoiding is two sentences long.
- (alarm clock clip) Set a 10 minute timer. Go.

Support ("A little support") examples of the voice:
- (notebook clip) You do not have to finish it today. Just open it.
- (slippers or bed clip) Rest is part of the project too.
- (writing clip) One line still counts.
- (sunlit desk clip) Starting late is still starting.
- (candle clip) You are not behind. You are in the middle.

Write new ones in this voice; do not copy other people's quotes or memes, and never attribute a line to a real person.
