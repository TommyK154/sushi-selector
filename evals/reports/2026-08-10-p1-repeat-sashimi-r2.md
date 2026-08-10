# Eval report 2026-08-10-p1-repeat-sashimi-r2

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 1.0000 | >= 0.97 | PASS |
| item_precision | 1.0000 | >= 0.97 | PASS |
| ingredient_f1_macro | 0.9504 | >= 0.90 | PASS |
| price_accuracy | 1.0000 | >= 0.97 | PASS |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-sashimi | 12/12 | 1.000 | 1.000 | 0.950 | 1.000 | 1.000 |

## Token usage and cost

- input: 2437
- cache write: 0
- cache read: 26170
- output: 1226
- estimated cost: $0.0112

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 1 | 0 | 8701 |
| details_batch_n | 1 | 0 | 8701 |
| index | 1 | 0 | 8768 |

- cache check (details calls 2+): 1/1 had cache reads > 0 [ok]

## Diffs: km-sushi-sashimi

- ingredients on 'Special A': missing=['escolar'] extra=['scolar']
- ingredients on 'Special B': missing=['escolar', 'japanese scallop', 'shrimp'] extra=['scallop', 'scolar']
- ingredients on 'Special C': missing=['escolar', 'shrimp'] extra=['scolar']

