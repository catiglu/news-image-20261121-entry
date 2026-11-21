# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/catiglu/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/catiglu/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One 1024×1024 front-page poster that sums up the world's news for Saturday, 21 November 2026: a Russian missile hits Poland (NATO calls it a violation), a magnitude 6.8 quake rattles Lima, the AI stock rout deepens, the ICJ rules Myanmar's Rohingya campaign is genocide — and more, laid out like a broadsheet.

## Run it

```sh
pip install pillow
python make_image.py                     # renders entry.png deterministically (build-time only)
MAKEFUN_OUTPUT_DIR=out python main.py    # the gate entry point: copies entry.png -> out/entry.png
```

`main.py` needs only the Python standard library, runs offline, and produces byte-identical output on every run (`entry.png` is fixed; no timestamps are embedded).

## What's in the image

- EUROPE (lead) — Russian missile hits Poland; NATO calls it a violation (AP · Reuters · BBC)
- AMERICAS — Magnitude 6.8 quake rattles Lima (Reuters)
- MARKETS — AI rout deepens: Nasdaq -5%, S&P -3.7%; Nvidia 52-week low on SEC probe (AP)
- EUROPE — EU and UK sign landmark post-Brexit reset deal (BBC)
- MIDDLE EAST — Houthi missile hits Riyadh's tallest tower (Reuters)
- LAW — ICJ: Myanmar's Rohingya campaign is genocide (AP)
- CLIMATE — COP31 draft slammed: fossil fuels unmentioned (AP)
- ALSO — Kyiv's bridges struck again; Palisades Fire arsonist convicted; NYC to close Rikers by 2032

Headlines reflect world news reported 20–21 Nov 2026 (UTC), via Google News RSS from AP, Reuters and BBC.

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=25pcjtmg&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
