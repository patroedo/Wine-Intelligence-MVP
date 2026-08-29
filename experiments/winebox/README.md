# WineBox comparison experiment

Goal: evaluate jdrumgoole/winebox as a data/matching component for Wine Intelligence MVP.

## What we test
1. X-Wines 100k+ catalogue as bootstrap
2. Autocomplete/fuzzy matching
3. Label scan pipeline
4. Free fallback path without paid vision
5. Returned metadata and community ratings
6. MongoDB/FastAPI integration cost versus our existing SQLite/Flask base

## Acceptance test
Same Giacomo Conterno / Barolo Monfortino image and same scorecard used for all candidates.

## Architectural preference
Reuse the catalogue/matching ideas or APIs rather than replacing the current application wholesale unless the benchmark clearly justifies it.
