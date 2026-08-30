# Cork Dork comparison experiment

Goal: evaluate the useful parts of BaconWappedBitcoin/ha-wine-cellar against the Wine Intelligence MVP flow.

## What we test
1. Photo-first UX
2. Label recognition path
3. Vivino search/enrichment path
4. Open Food Facts/barcode fallback
5. Returned fields: producer, wine, vintage, appellation, region, rating, price, image, pairing
6. Cost and external dependencies

## Important
This experiment does not copy upstream code. It documents the integration boundary first so we can preserve licensing and avoid coupling the MVP to a brittle scraper.

## Acceptance test
Use the same Giacomo Conterno / Barolo Monfortino bottle image for every candidate. Score: recognition accuracy, vintage accuracy, enrichment completeness, latency, cost, maintainability.
