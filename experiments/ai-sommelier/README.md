# AI Sommelier experiment

Purpose: evaluate the open-source AI Sommelier retrieval/recommendation approach as a zero-paid-API component for Wine Intelligence MVP.

## Scope

Use this experiment for recommendation/pairing and Taste DNA, not label recognition.

Target flow:

1. User selects a dish / occasion / preferences.
2. Candidate wines are restricted to the user's cellar when requested.
3. Local semantic retrieval ranks candidates.
4. Return three differentiated choices: best match, discovery, best value.
5. Optional LLM explanation remains a separate enhancement and must not be required for the free core.

## Acceptance test

- Works without a paid LLM API for retrieval/ranking.
- Can rank wines by a natural-language food/occasion query.
- Can later be connected to Wine Tracker's SQLite cellar.
- Keeps upstream license/attribution intact when code is imported.

## Architecture decision

Do not replace the existing Wine Tracker app. Integrate recommendation as a modular service after the recognition experiments are complete.
