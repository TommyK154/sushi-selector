# Eval report 2026-08-10-p1-repeat-sashimi-r1

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 1.0000 | >= 0.97 | PASS |
| item_precision | 1.0000 | >= 0.97 | PASS |
| ingredient_f1_macro | 0.9612 | >= 0.90 | PASS |
| price_accuracy | 1.0000 | >= 0.97 | PASS |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-sashimi | 12/12 | 1.000 | 1.000 | 0.961 | 1.000 | 1.000 |

## Token usage and cost

- input: 2437
- cache write: 17469
- cache read: 8701
- output: 1334
- estimated cost: $0.0318

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 1 | 8701 | 0 |
| details_batch_n | 1 | 0 | 8701 |
| index | 1 | 8768 | 0 |

- cache check (details calls 2+): 1/1 had cache reads > 0 [ok]

## Diffs: km-sushi-sashimi

- ingredients on 'Special A': missing=['shrimp'] extra=['ikura']
- ingredients on 'Special B': missing=['japanese scallop', 'shrimp'] extra=['ikura', 'scallop']
- ingredients on 'Special C': missing=['shrimp'] extra=['ikura']

