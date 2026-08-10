# Eval report 2026-08-10-p1-repeat-nigiri-r1

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 1.0000 | >= 0.97 | PASS |
| item_precision | 1.0000 | >= 0.97 | PASS |
| ingredient_f1_macro | 0.8976 | >= 0.90 | FAIL |
| price_accuracy | 0.9512 | >= 0.97 | FAIL |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-nigiri | 41/41 | 1.000 | 1.000 | 0.898 | 0.951 | 0.927 |

## Token usage and cost

- input: 5847
- cache write: 17469
- cache read: 43505
- output: 3585
- estimated cost: $0.0500

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 1 | 8701 | 0 |
| details_batch_n | 5 | 0 | 43505 |
| index | 1 | 8768 | 0 |

- cache check (details calls 2+): 5/5 had cache reads > 0 [ok]

## Diffs: km-sushi-nigiri

- ingredients on 'Japanese Scallop': missing=['japanese scallop'] extra=['scallop']
- ingredients on 'Smelt Egg': missing=['masago'] extra=['egg']
- ingredients on 'Bean Curd': missing=['bean curd'] extra=['tofu']
- price mismatch on 'Salmon Skin Roll': pred=7.39/'7.39' gold=7.99/'7.99'
- ingredients on 'Salmon Skin Roll': missing=['cucumber'] extra=[]
- ingredients on 'California Roll': missing=['crab meat'] extra=['imitation crab']
- price mismatch on 'Yellowtail Roll': pred=6.5/'6.50' gold=8.5/'8.50'
- ingredients on 'Philadelphia Roll': missing=['cucumber'] extra=[]
- ingredients on 'Eel Roll': missing=['cucumber'] extra=[]

