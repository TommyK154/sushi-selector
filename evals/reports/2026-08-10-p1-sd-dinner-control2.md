# Eval report 2026-08-10-p1-sd-dinner-control2

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.3333 | >= 0.97 | FAIL |
| item_precision | 0.1765 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.2222 | >= 0.90 | FAIL |
| price_accuracy | 0.1667 | >= 0.97 | FAIL |
| consistency_f1_spread_max | 0.3944 | >= 0.03 | FAIL |

## Consistency (--repeat 3)

| Menu | Item counts per run | Identical | Ing F1 per run | Spread |
|---|---|---|---|---|
| km-sushi-dinner | 34, 24, 28 | NO | 0.222, 0.617, 0.222 | 0.3944 |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-dinner | 34/18 | 0.333 | 0.176 | 0.222 | 0.167 | 1.000 |

## Token usage and cost

- input: 12666
- cache write: 0
- cache read: 130716
- output: 7463
- estimated cost: $0.0631

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 3 | 0 | 26103 |
| details_batch_n | 9 | 0 | 78309 |
| index | 3 | 0 | 26304 |

- cache check (details calls 2+): 9/9 had cache reads > 0 [ok]

## Diffs: km-sushi-dinner

- ingredients on 'Chirashi Bowl': missing=[] extra=['cucumber', 'radish', 'salmon', 'shrimp', 'tuna', 'yellowtail']
- price mismatch on 'Chicken Teriyaki': pred=None/None gold=None/'2 for 23.00'
- ingredients on 'Chicken Teriyaki': missing=[] extra=['teriyaki sauce']
- price mismatch on 'California Roll': pred=None/None gold=None/'2 for 23.00'
- ingredients on 'California Roll': missing=['crab meat'] extra=['imitation crab']
- price mismatch on 'Vegetable Roll': pred=None/None gold=None/'2 for 23.00'
- ingredients on 'Vegetable Roll': missing=['avocado', 'cucumber'] extra=['various vegetable']
- price mismatch on 'Vegetable Tempura': pred=None/None gold=None/'2 for 23.00'
- ingredients on 'Vegetable Tempura': missing=['green bean', 'onion', 'yam', 'zucchini'] extra=['tempura batter', 'vegetable']
- price mismatch on 'Gyoza': pred=None/None gold=None/'2 for 23.00'
- ingredients on 'Gyoza': missing=['beef'] extra=['gyoza']
- MISSED golden item: 'Sushi Combo (9pcs Sushi + Roll)'
- MISSED golden item: 'Sushi & Sashimi Combo (5pcs Sushi + 6pcs Sashimi + Roll)'
- MISSED golden item: 'Steak Teriyaki'
- MISSED golden item: 'Salmon Teriyaki'
- MISSED golden item: 'Garlic Chicken'
- MISSED golden item: 'Spicy Chicken'
- MISSED golden item: 'Sesame Chicken'
- MISSED golden item: 'Spicy Sesame Chicken'
- MISSED golden item: 'Lemon Shrimp'
- MISSED golden item: 'Mixed Tempura'
- MISSED golden item: 'Assorted Sashimi'
- MISSED golden item: 'Spicy Tuna Roll'
- EXTRA predicted item: 'Sushi Combo'
- EXTRA predicted item: 'Sashimi Assorted Sushi Plate'
- EXTRA predicted item: 'Tempura'
- EXTRA predicted item: 'Udon'
- EXTRA predicted item: 'Poke Bowl'
- EXTRA predicted item: 'Spicy Tuna Poke Sushi Roll'
- EXTRA predicted item: 'Shrimp Tempura Roll'
- EXTRA predicted item: 'Philadelphia Roll'
- EXTRA predicted item: 'Cucumber Roll'
- EXTRA predicted item: 'Spicy Salmon Roll'
- EXTRA predicted item: 'Asparagus Roll'
- EXTRA predicted item: 'Avocado Roll'
- EXTRA predicted item: 'Crab Tempura'
- EXTRA predicted item: 'Deep Fried Soft Shell Crab'
- EXTRA predicted item: 'Spicy Scallop'
- EXTRA predicted item: 'Garlic Shrimp'
- EXTRA predicted item: 'Grilled Beef'
- EXTRA predicted item: 'Fried Scallop'
- EXTRA predicted item: 'Black Teriyaki'
- EXTRA predicted item: 'Beef Teriyaki'
- EXTRA predicted item: 'Shrimp Teriyaki'
- EXTRA predicted item: 'Shrimp Tempura'
- EXTRA predicted item: 'Calamari'
- EXTRA predicted item: 'Edamame'
- EXTRA predicted item: 'Seaweed Salad'
- EXTRA predicted item: 'Sashimi Tuna Salad'
- EXTRA predicted item: 'Sashimi Salmon Salad'
- EXTRA predicted item: 'Cucumber Salad'

