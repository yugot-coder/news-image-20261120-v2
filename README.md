# news-image-20261120-v2

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/yugot-coder/news-image-20261120-v2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/yugot-coder/news-image-20261120-v2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**THE WORLD IN ONE DAY** — Friday 20 November 2026 on one dense broadsheet page, drawn entirely in code: 33 stories, 4 regions, 13 illustrations.

Three illustrated leads — Russia's 110+ missile barrage on Kyiv (three Dnipro bridges hit hours after the Shenzhen peace summit), Cyclone Akvan's landfall at Gopalpur with 300,000+ evacuated, and Asia-Pacific stocks' 7% weekly AI crash — plus a six-number stats strip, ten numbered story cards (the first Trump–Xi–Putin summit, COP31's deadlock in Antalya, Anthropic's record IPO, the $190.4m Van Gogh record, Japan's 2.3% CPI, BepiColombo reaching Mercury, Nicholls' 175* in Wellington, the Crimea bridge strike, the 19-month-high dollar, Europe's rebuke), a "Where it happened" world map with pins, and a 20-story one-line index. Every fact was checked on the day against Reuters, CNN, The Times, IMD, the Statistics Bureau of Japan, Scientific American, Carbon Herald and Cricbuzz, and the page carries a red date-check box to prove it.

`main.py` is pure Python 3 standard library — no network, no installs, deterministic (two runs are byte-identical). It renders the 1024x1024 front page with its own bitmap + stroke type systems and raster illustration engine, and writes `/output/entry.png`.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=za0zfbxx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
