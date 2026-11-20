# The World Today — Friday, 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun](https://make.fun/badge/news-image-20261120/rezimx-btc/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![make.fun](https://make.fun/badge/news-image-20261120/rezimx-btc/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)

A dense one-page broadsheet newspaper front page summing up 20 November
2026 in a single 1024x1024 image: a big masthead with the date, the
historic first-ever three-way Trump–Xi–Putin meeting in Shenzhen as the
lead story, a world-map strip with numbered markers for every story,
regional headline columns (Americas, Europe, Asia-Pacific), an "Also in
the news" briefs band, and a market ticker at the foot.

Every headline is drawn from real news reported for 20 November 2026:
the APEC three-way summit, the Iran decision pushed to 2027, Voyager 1
passing a light-day, Hayabusa2's abandoned landing, GTA 6 passing
The Odyssey's $1.80bn, Cyclone Akvan, Anthropic's +17% debut, Europe's
readiness for talks with Russia, the ICJ genocide ruling on Myanmar,
Nicholls' 113 not out, the EU–UK Summit, World Children's Day, the
Han Duck-soo verdict, and Fiji's drought disaster declaration.

## Run it

```sh
python3 main.py
```

The program is pure Python 3.13 standard library (no Pillow, no
third-party imports) and writes `entry.png` only into the directory named
by the `MAKEFUN_OUTPUT_DIR` environment variable (default `/output`).
It never writes beside `main.py` or anywhere inside the repository.
Running it twice produces a byte-identical image.
