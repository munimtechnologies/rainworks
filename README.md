# 🌧️ Rainworks

A seated, hands-first VR puzzle for the web. A small island floats in front of you under a rain cloud.
Turn the channel tiles so the rain reaches every garden, and watch the flowers bloom.

- **Hands only:** pinch at a tile from a distance, or reach out and touch it with a fingertip. Controllers work too.
- **Seated, short sessions:** 12 islands, each 30 to 90 seconds. Every level is generated from a seeded spanning tree,
  so every level is solvable, and each one has a par number of turns for three stars.
- **Runs in the browser:** a single `index.html` (WebXR + three.js from a pinned CDN version). With no headset, click the tiles.

Status: **prototype v0.1**. Not yet tested on a headset.

## Try it
- Open `index.html` in a browser. On a Meta Quest, open it in the Quest Browser and press **Enter VR**.
- `index.html?emulate` loads Meta's [Immersive Web Emulator](https://github.com/meta-quest/immersive-web-emulation-runtime)
  so hand input can be tested in desktop Chrome.
- `index.html#selftest` checks every level: generation, solvability, par, and solving through the 3D code.
- `python test_rainworks.py` runs the static checks, and the level checks too if Node.js is installed.

## Credits and disclosure
Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude): the code, levels and sounds were generated with AI tools,
then reviewed and tested. No third-party art or sound assets are used; everything is drawn and synthesized at runtime.
Built on [three.js](https://threejs.org) (MIT).

Contact: munimversion2@gmail.com

License: MIT.
