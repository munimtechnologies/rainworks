# 🌧️ Rainworks

A seated, hands-first VR puzzle for the web. A small island floats in front of you under a rain cloud.
Turn the channel tiles so the rain reaches every garden, and watch the flowers bloom.

- **Hands only:** pinch at a tile from a distance, or reach out and touch it with a fingertip. Controllers work too.
- **Seated, short sessions:** 12 islands, each 30 to 90 seconds. Every level is generated from a seeded spanning tree,
  so every level is solvable, and each one has a par number of turns for three stars.
- **Gentle start:** the first island guides every turn with an arrow, and the first four islands turn only a few tiles.
  After that, every tile starts at a random turn.
- **Calm and accessible:** no timer and no fail state. 💡 Hint points at a tile to turn (following the hints always finishes
  the island). Wet channels stand taller as well as turning blue, so the water's path does not depend on colour alone.
- **Runs in the browser:** a single `index.html` (WebXR + three.js from a pinned CDN version). With no headset, click the tiles.

Status: **prototype v0.2**. Not yet tested on a headset.

## What's new in v0.2
- A tutorial arrow on island 1, and a 💡 Hint button (3D and on screen).
- An easier difficulty ramp: islands 1 to 4 start with 2, 3, 5 and 8 turned tiles.
- Flowers open five petals when the water reaches them, and a rainbow rises when every garden blooms.
- Soft synthesized rain that quiets when the island is finished, a sound on/off button, and audio that pauses when the page is hidden.
- The panel shows your star total, and its text shrinks to fit.

## Try it
- Open `index.html` in a browser. On a Meta Quest, open it in the Quest Browser and press **Enter VR**.
- `index.html?emulate` loads Meta's [Immersive Web Emulator](https://github.com/meta-quest/immersive-web-emulation-runtime)
  so hand input can be tested in desktop Chrome.
- `index.html#selftest` checks every level: generation, solvability, par, following the hints, and solving through the 3D code.
- `python test_rainworks.py` runs the static checks, and the level checks too if Node.js is installed.

## Credits and disclosure
Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude): the code, levels and sounds were generated with AI tools,
then reviewed and tested. No third-party art or sound assets are used; everything is drawn and synthesized at runtime.
Built on [three.js](https://threejs.org) (MIT).

Contact: munimversion2@gmail.com

License: MIT.
