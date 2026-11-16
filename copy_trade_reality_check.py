#!/usr/bin/env python3
"""
Copy-Trade Reality Check — does screening a wallet on its PAST record (the "Grok copy-trading"
pitch) actually predict FUTURE profit? Run the numbers.

The viral clip (ai.flow_lab, "Grok copy-trading system that follows 1 trader at a time") sells a
bot that screens a wallet on win rate, 30-day profit, trade count and "consistency," then copies
it. Headline: 81% win rate, $150 -> $3,783, "comment COPY and I'll DM you the setup."

This tool tests the actual claim with math, not a highlight. No wallet connection, no exchange
keys, no orders — it only simulates and does arithmetic.

Three honest results:
  [1] SURVIVORSHIP: if you screen the top past performers out of a crowd whose returns are mostly
      luck (which memecoin copiers are), their FUTURE returns revert to ~average. Screening past
      winners does not buy you future winners. You can crank the 'skill' knob and watch when it
      would work (spoiler: only with persistent skill these wallets don't have).
  [2] WIN RATE != PROFIT: an 81% win rate is a marketing number. With the small-wins/big-losses
      payoff that copy-trading and memecoins actually have, 81% wins is still net-NEGATIVE.
  [3] COPY LAG: you execute AFTER the wallet. On the illiquid tokens these wallets trade, your
      copy buy fills higher and you exit later — you are the exit liquidity.
"""
import argparse, random, statistics


def survivorship(n_wallets=1500, skill_sd=0.0, luck_sd=1.0, screen_top=0.02, runs=500, seed=7):
    """Each wallet has a hidden true edge ~N(0, skill_sd) and per-period luck ~N(0, luck_sd).
    Screen the top `screen_top` by a PAST period, then measure their FORWARD period. Honest: if
    skill_sd is ~0 (memecoin reality), the screen captures luck and forward reverts to ~0."""
    rng = random.Random(seed)
    past_sel, fwd_sel, fwd_all = [], [], []
    k = max(1, int(n_wallets * screen_top))
    for _ in range(runs):
        edges = [rng.gauss(0, skill_sd) for _ in range(n_wallets)]
        past = [e + rng.gauss(0, luck_sd) for e in edges]
        order = sorted(range(n_wallets), key=lambda i: past[i], reverse=True)[:k]
        fwd = [edges[i] + rng.gauss(0, luck_sd) for i in order]
        past_sel.append(statistics.mean(past[i] for i in order))
        fwd_sel.append(statistics.mean(fwd))
        fwd_all.append(statistics.mean(edges[i] + rng.gauss(0, luck_sd) for i in range(0, n_wallets, 8)))
    return {"screened_past": statistics.mean(past_sel), "screened_future": statistics.mean(fwd_sel),
            "everyone_future": statistics.mean(fwd_all),
            "kept_pct": round(100 * statistics.mean(fwd_sel) / statistics.mean(past_sel), 1) if statistics.mean(past_sel) else 0.0}


def win_rate_vs_expectancy(win_rate=0.81, avg_win=1.0):
    """Win rate alone is meaningless — what matters is avg win vs avg loss, which the clip never shows.
    Returns the breakeven average loss (in R = one avg win) and the expectancy if losses average 5R,
    a realistic memecoin figure (small scalp wins, the occasional near-total rug)."""
    p = win_rate
    be_loss = (p * avg_win) / (1 - p)           # avg loss (R) that makes expectancy exactly zero
    loss_5R = p * avg_win - (1 - p) * 5.0 * avg_win
    return {"win_rate_pct": round(100 * p, 1), "breakeven_avg_loss_R": round(be_loss, 1),
            "expectancy_if_losses_5R": round(loss_5R, 2)}


def copy_lag(pump_pct=120, lag_frac=0.35, slippage_pct=6):
    """The wallet buys at the bottom of a pump of `pump_pct`%. A copier detects + executes after
    part of the move (lag_frac) and eats slippage. Compare final P&L if both exit at the top."""
    entry_wallet = 0.0
    top = pump_pct
    entry_copier = pump_pct * lag_frac + slippage_pct     # copier buys this far up, plus slippage
    wallet_gain = top - entry_wallet
    copier_gain = top - entry_copier
    return {"wallet_entry_pct": 0, "copier_entry_pct": round(entry_copier, 1),
            "wallet_gain_pct": round(wallet_gain, 1), "copier_gain_pct": round(copier_gain, 1),
            "copier_keeps_pct_of_wallets_gain": round(100 * copier_gain / wallet_gain, 1) if wallet_gain else 0}


def main():
    ap = argparse.ArgumentParser(description="Test the 'Grok copy-trading' wallet-screening pitch with math.")
    ap.add_argument("--skill", type=float, default=0.0, help="persistent skill SD of the wallet crowd (0 = memecoin reality)")
    ap.add_argument("--runs", type=int, default=500)
    a = ap.parse_args()
    print("=" * 78)
    print("COPY-TRADE REALITY CHECK — does screening a wallet's PAST record predict its FUTURE?")
    print("=" * 78)

    print("\n[1] SURVIVORSHIP — screen the top 2% of the crowd by a PAST period, then watch them FORWARD:")
    for sk, label in [(a.skill, "the crowd as given (--skill=%.2f)" % a.skill),
                      (0.0, "ZERO persistent skill (memecoin copiers)"),
                      (1.0, "HIGH persistent skill (pro desks — not who you're copying)")]:
        r = survivorship(skill_sd=sk, runs=a.runs)
        print("  · %s" % label)
        print("      screened wallets' PAST avg: %+.2f  ->  their FORWARD avg: %+.2f   (they keep %.0f%% of what looked like edge)"
              % (r["screened_past"], r["screened_future"], r["kept_pct"]))
    print("    the past number sells the bot. the forward number is what you'd actually get. with the skill")
    print("    these wallets really have (~0), screening past winners buys you ~nothing — just luck that reverts.")

    w = win_rate_vs_expectancy(0.81)
    print("\n[2] WIN RATE != PROFIT — their 81% is the one number they show, and it tells you the least:")
    print("    at an 81%% win rate you break even only if your average LOSS stays under %.1fR (R = one avg win)."
          % w["breakeven_avg_loss_R"])
    print("    they never show the avg win or loss. copy-trading memecoins is small scalp wins and the odd near-total")
    print("    rug: if the 19%% of losses average 5R, expectancy = %+.2fR per trade — NEGATIVE at an 81%% win rate."
          % w["expectancy_if_losses_5R"])
    print("    a high win rate with undisclosed win/loss size is the oldest tell in trading.")
    print("\n[3] COPY LAG — you execute AFTER the wallet, and you're the exit liquidity:")
    c = copy_lag()
    print("    wallet buys at 0%% and rides a +%d%% pump. you detect+fill %d%% up the move (plus slippage)."
          % (120, c["copier_entry_pct"]))
    print("    wallet gain +%.0f%%, your gain +%.0f%% — you keep %.0f%% of the move the clip is bragging about,"
          % (c["wallet_gain_pct"], c["copier_gain_pct"], c["copier_keeps_pct_of_wallets_gain"]))
    print("    and that's if you both exit at the top. on real memecoins you get the dump, not the top.")

    print("\nVERDICT: screening a wallet's PAST record does not buy future profit — past performance of a mostly-luck")
    print("crowd reverts. '81% win rate' hides the payoff. copy lag hands the wallet your entry. 'Grok' is a label on")
    print("trivial filters. The product is the 'comment COPY -> DM' funnel, not an edge.\n")


if __name__ == "__main__":
    main()
