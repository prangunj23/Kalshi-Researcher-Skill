Compare every possible pair of markets to determine if they could end up being a matching market pair. Use these rules to check if this could possibly happen:

### Deterministic matching checklist

For each market (primarily using `rules_primary`), extract and normalize:
- **Sport/league** (NBA/MLB/NHL/etc.)
- **Teams/participants** (canonical team names when applicable)
- **Event identity** (who vs who, plus round/game qualifiers)
- **Timing** (scheduled date/time window if present)
- **Market type** (future vs single-event vs series; and prop type like totals/spread/moneyline)

Only consider two markets a plausible matching pair if all are true:
- **Same sport and league** after normalization
- **Same underlying event identity**, OR an explicitly equivalent end-condition (for a futures ↔ event convergence case)
- **Compatible market types** (they resolve on the same real-world outcome)

### Do not match unless… (guardrails)

Reject candidate pairs when any of these differ materially:
- League level (e.g., NBA vs NCAA)
- Season/year or scheduled date window (when rule text specifies it)
- Participants/teams (after applying aliases)
- Event stage/round (regular season vs playoffs; Finals Game 7 vs Finals Game 6; etc.)

Treat `rules_secondary` clauses (e.g., postponement/reschedule windows) as settlement mechanics; they typically do not change the underlying event identity.

### Normalization / Alias Map

Kalshi market titles/rules may use different naming conventions for the same underlying league/team.
Before deciding whether two markets are about the *same* sport/league/team, normalize the text (especially inside `rules_primary`) using the alias map.

**Basic normalization (apply before alias lookup):**
- lowercase for comparisons
- strip punctuation and collapse repeated whitespace
- normalize common shorthands where context supports it (e.g., "LA" → "Los Angeles")

**League aliases:**
- "Pro Basketball" → "NBA"
- "Pro Baseball" → "MLB"

**Team aliases:**
- "Los Angeles L" → "Los Angeles Lakers"
- "Los Angeles C" → "Los Angeles Clippers"
- "Los Angeles A" → "Los Angeles Angels"
- "Los Angeles D" → "Los Angeles Dodgers"
- "New York Y" → "New York Yankees"
- "New York M" → "New York Mets"
- "Chicago C" → "Chicago Cubs"
- "Chicago WS" → "Chicago White Sox"

**Notes:**
- Prefer the most specific canonical name (e.g., team full name over shorthand).
- Apply aliases consistently across both markets before comparing.
- If an alias could be ambiguous (e.g., "Los Angeles A"), use league context from the rule text (e.g., "professional baseball" → MLB) to disambiguate.

The actual relationship should go be one where the game market for a particular team/player should be less than or equal to a futures market. Some examples of this are:

- First round of Knockout Tournament vs College Basketball Champion
  - It is clear to see that the probability of winning the championship can't be higher than winning the first game of the tournament
- Team winning their next game vs Team going undefeated in a season 
  - It can be seen that in order for a team to go undefeated, they need to win every game, thus this market should be trading lower than the market for their next game.

## Step 3: Explain Reasoning

When proposing a matching market pair, include:
- the two market `ticker` values
- a short explanation of why they refer to the same underlying event/end condition (using the normalized league/teams/timing/market-type reasoning)

Print each candidate pair on its own, and keep reasoning concise and specific.
