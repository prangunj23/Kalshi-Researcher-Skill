---
name: kalshi-researcher-skill
description: A skill that searches Kalshi markets for arbitrage opportunities
---
# Kalshi Market Arbitrage Finding Skill

Looks for Arbitrage Opportunities in Kalshi where a futures market and a game market are mispriced against each other. 

## Step 0: Install Dependencies

If you haven't installed dependencies yet (or you're in a fresh virtual environment), install them from `requirements.txt` (it's safe to re-run):

```bash
python -m pip install -r requirements.txt
```

## Step 1: Ask for Market Inputs

First check whether the user already provided market codes in their request.

- If market codes are already present, use those exact codes and do not ask again.
- If market codes are not present, ask the user which market codes to scan (one or more).

Valid values are the keys in `scripts/markets.json` (for example: `MPBK`, `NHL`, `EPL`, `MCBK`).

If the user provides multiple values, keep their order and pass all of them to the script as CLI arguments.

### Multi-code execution order

If the user provides multiple market codes, process them strictly one at a time in the order provided.

For each code:
- Run market gathering for that single code.
- Parse output using the OpenClaw parsing rules.
- Run matching/comparison logic for that code only.
- Produce the per-code reasoning output.
- Clear or discard the previous code's raw output from active context before starting the next code.

Only after fully completing the full workflow for the current code should the agent move to the next code.

## Step 2: Gather the Markets

Run the market fetching script with the user-provided market codes:
```bash
python scripts/kalshi_markets.py <MARKET_CODE_1> <MARKET_CODE_2> ...
```

Example:
```bash
python scripts/kalshi_markets.py MPBK NHL
```

This will output all the markets and their primary and secondary rules in a json format. The rules will define the nature of the market.

### OpenClaw output parsing rules

When OpenClaw reads the script output, it must branch based on the status text:

- If the output contains the exact line `Game and Futures Markets are together`, treat the next JSON block under `Game and Futures Markets Combined:` as a single unified market list and follow the combined-market matching logic.
- Otherwise, treat output as split mode: parse the JSON block after `Game Markets:` as the game list and the JSON block after `Futures Markets:` as the futures list, then compare these two lists separately.

Do not assume combined mode unless the exact `Game and Futures Markets are together` text appears.

### Market JSON schema

Assume each market is represented as a JSON object with (at least) the following fields:
- `ticker` (string): unique market identifier
- `rules_primary` (string): main resolution rule text (use this as the primary source of truth)
- `rules_secondary` (string): secondary clauses (often postponements/rescheduling/edge cases)

Example market object:
```json
{
	"ticker": "KXMLBF5TOTAL-26MAR252005NYYSF-7",
	"rules_primary": "If New York Y and San Francisco collectively score more than 6.5 runs in the first 5 innings of the New York Y vs San Francisco professional baseball game originally scheduled for Mar 25, 2026 at 8:05 PM EDT, then the market resolves to Yes.",
	"rules_secondary": "If this game is postponed or delayed, the market will remain open and close after the rescheduled game has finished (within two days)."
}
```

## Step 3: Route to the Correct Comparison Instructions

Check what comparison mode the user asked for:

- If the user asked for **one way** only, read and execute `oneway.md`.
- If the user asked for **equal market** only, read and execute `equal_market.md`.
- If the user asked for **both**, read and execute `oneway.md` first, then `equal_market.md`.

If the user did not clearly specify one way, equal market, or both, ask a clarification question before running comparison logic.

For whichever mode(s) you run, follow that file's full instructions for:
- comparison logic for market pairing
- normalization and alias handling
- guardrails for rejecting mismatches
- required per-pair reasoning output format


