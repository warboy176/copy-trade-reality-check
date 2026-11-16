# Copy-Trade Reality Check

A free, open tool that tests the viral **"Grok copy-trading"** pitch with math instead of a highlight.

A clip going around (ai.flow_lab, *"a Grok copy-trading system that follows 1 trader at a time"*) sells a bot that **screens a wallet on its past record** — win rate, 30-day profit, trade count, "consistency" — then copies it. Headline: **81% win rate, 200 trades, 7.9% drawdown, $150 → $3,783 in 2 weeks**, and *"comment COPY and I'll DM you the setup."*

This tool runs the actual claim through the numbers. No wallet connection, no exchange keys, no orders — it only simulates and does arithmetic.

## Run it

```
python3 copy_trade_reality_check.py
```

No dependencies, no API key, Python 3 standard library only. `--skill` sets the crowd's persistent-skill level (default 0 = the memecoin reality); `--runs` sets the sample size.

## What it shows

1. **Survivorship.** Screen the top 2% of a crowd by a *past* period, then watch them *forward*. When the crowd's returns are mostly luck — which memecoin copiers are — the screened "winners" **revert to roughly zero** going forward. Their dazzling past record was luck, and luck doesn't persist. Screening past winners does **not** buy you future winners. (Crank `--skill` up and you'll see screening only pays off if the wallets have real, persistent skill — which the accounts you can copy don't.)
2. **Win rate ≠ profit.** At an 81% win rate you break even only if your average **loss** stays under ~4.3× your average win. The clip never shows the average win or loss — the one pair of numbers that decides everything. With realistic memecoin losses (small scalp wins, the odd near-total rug), 81% wins is **net negative**.
3. **Copy lag.** You execute *after* the wallet. On the illiquid tokens these wallets trade, your copy buy fills higher and you exit later — in the best case you keep ~60% of the move, and on a real rug you're the **exit liquidity**.

## What it is NOT

- **Not a trading bot.** It connects to no wallet, no exchange, no broker; it holds no keys and places no orders.
- **Not financial advice.** Nothing here tells you to buy, sell, or copy anything.
- **Not a claim that nobody ever makes money copying.** People get lucky. The honest point is narrower: screening a wallet's past record doesn't create an edge, and a hidden-loss-size win rate tells you nothing.

## The honest limits

- The survivorship and copy-lag results are **models**, with every assumption at the top of the source. They are built to be fair — the survivorship test *does* reward real skill when you tell it the crowd has some (`--skill`); the point is that the crowd you can copy doesn't.
- Returns are in abstract units / R-multiples (R = one average win), not dollars, so the logic is broker- and chain-agnostic.
- Real memecoin execution (MEV, failed txs, honeypots, liquidity pulls) is *worse* than the clean slippage modeled here, not better.

## The actual takeaway

- **Past wallet performance doesn't predict future wallet performance** when the performance is mostly luck. "Screen the trader first" screens for luck.
- **A high win rate with an undisclosed win/loss size is the oldest tell in trading.** Ask for the average win and average loss. They won't be in the DM.
- **"Grok" does nothing here.** Checking a wallet's win rate and trade count is trivial arithmetic; the AI label is branding.
- The real product is the **"comment COPY → DM"** funnel — the free "setup" is the hook; the money is a paid bot, signals, or an affiliate link on the other side.

Ask for the average win and average loss. Keep your $150.

---

Built and released free by **Warboy** — no DM, no "comment COPY," no wall.
More free rebuilds of what the "gurus" sell: https://github.com/warboy176 · https://www.patreon.com/warboy176
