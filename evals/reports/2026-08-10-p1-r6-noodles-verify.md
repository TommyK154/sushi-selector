# Eval report 2026-08-10-p1-r6-noodles-verify

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.2667 | >= 0.97 | FAIL |
| item_precision | 0.1905 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.3750 | >= 0.90 | FAIL |
| price_accuracy | 0.0000 | >= 0.97 | FAIL |
| consistency_f1_spread_max | 0.2250 | >= 0.03 | FAIL |

## Consistency (--repeat 3)

| Menu | Item counts per run | Identical | Ing F1 per run | Spread |
|---|---|---|---|---|
| km-sushi-noodles-kitchen | 21, 28, 30 | NO | 0.375, 0.250, 0.475 | 0.2250 |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-noodles-kitchen | 21/15 | 0.267 | 0.190 | 0.375 | 0.000 | 1.000 |

## Token usage and cost

- input: 11899
- cache write: 18419
- cache read: 110246
- output: 7509
- estimated cost: $0.0835

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 3 | 9176 | 18352 |
| details_batch_n | 8 | 0 | 73408 |
| index | 3 | 9243 | 18486 |

- cache check (details calls 2+): 8/8 had cache reads > 0 [ok]

## Diffs: km-sushi-noodles-kitchen

- price mismatch on 'Steak Teriyaki': pred=14.5/'14.50' gold=13.99/'13.99'
- ingredients on 'Steak Teriyaki': missing=['beef', 'green cabbage', 'teriyaki sauce'] extra=['steak']
- price mismatch on 'Miso Soup': pred=3.5/'3.50' gold=2.95/'2.95'
- ingredients on 'Miso Soup': missing=['seaweed', 'tofu'] extra=[]
- price mismatch on 'Pork Katsu': pred=16.5/'16.50' gold=19.99/'19.99'
- ingredients on 'Pork Katsu': missing=['katsu sauce', 'panko'] extra=[]
- price mismatch on 'Chicken Katsu': pred=15.5/'15.50' gold=17.99/'17.99'
- ingredients on 'Chicken Katsu': missing=['katsu sauce', 'panko'] extra=[]
- MISSED golden item: 'Chicken Udon'
- MISSED golden item: 'Vegetable Udon'
- MISSED golden item: 'Spicy Beef Udon'
- MISSED golden item: 'Tempura Udon'
- MISSED golden item: 'Donkotsu Ramen'
- MISSED golden item: 'Spicy Seafood Ramen'
- MISSED golden item: 'Yakisoba'
- MISSED golden item: 'Children's Combo'
- MISSED golden item: 'Chicken Teriyaki'
- MISSED golden item: 'Sesame Chicken'
- MISSED golden item: 'Mixed Tempura'
- EXTRA predicted item: 'Sushi & Sashimi Combo'
- EXTRA predicted item: 'Chicken Teriyaki Combo'
- EXTRA predicted item: 'Shrimp Teriyaki'
- EXTRA predicted item: 'Seafood Combination'
- EXTRA predicted item: 'Scallop'
- EXTRA predicted item: 'Black Pepper Pork'
- EXTRA predicted item: 'Crab Tempura'
- EXTRA predicted item: 'Chicken Tempura'
- EXTRA predicted item: 'Vegetable Tempura'
- EXTRA predicted item: 'Shrimp Tempura'
- EXTRA predicted item: 'Gyoza'
- EXTRA predicted item: 'Seaweed Salad'
- EXTRA predicted item: 'Edamame'
- EXTRA predicted item: 'Fried Rice'
- EXTRA predicted item: 'Beef Don'
- EXTRA predicted item: 'Chirashi Don'
- EXTRA predicted item: 'Katsu Don'

