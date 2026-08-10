# Eval report 2026-08-10-p1-repeat-noodles-kitchen

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.2000 | >= 0.97 | FAIL |
| item_precision | 0.1071 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.6667 | >= 0.90 | FAIL |
| price_accuracy | 0.3333 | >= 0.97 | FAIL |
| consistency_f1_spread_max | 0.4667 | >= 0.03 | FAIL |

## Consistency (--repeat 3)

| Menu | Item counts per run | Identical | Ing F1 per run | Spread |
|---|---|---|---|---|
| km-sushi-noodles-kitchen | 28, 23, 37 | NO | 0.667, 0.500, 0.200 | 0.4667 |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-noodles-kitchen | 28/15 | 0.200 | 0.107 | 0.667 | 0.333 | 1.000 |

## Token usage and cost

- input: 12750
- cache write: 17469
- cache read: 113247
- output: 7227
- estimated cost: $0.0820

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 3 | 8701 | 17402 |
| details_batch_n | 9 | 0 | 78309 |
| index | 3 | 8768 | 17536 |

- cache check (details calls 2+): 9/9 had cache reads > 0 [ok]

## Diffs: km-sushi-noodles-kitchen

- price mismatch on 'Chicken Teriyaki': pred=14.95/'14.95' gold=11.95/'11.95'
- ingredients on 'Chicken Teriyaki': missing=['green cabbage'] extra=[]
- ingredients on 'Spicy Seafood Ramen': missing=['green mussel', 'ramen noodle'] extra=['seafood']
- price mismatch on 'Steak Teriyaki': pred=14.95/'14.95' gold=13.99/'13.99'
- ingredients on 'Steak Teriyaki': missing=['green cabbage'] extra=[]
- MISSED golden item: 'Miso Soup'
- MISSED golden item: 'Chicken Udon'
- MISSED golden item: 'Vegetable Udon'
- MISSED golden item: 'Spicy Beef Udon'
- MISSED golden item: 'Tempura Udon'
- MISSED golden item: 'Donkotsu Ramen'
- MISSED golden item: 'Yakisoba'
- MISSED golden item: 'Children's Combo'
- MISSED golden item: 'Chicken Katsu'
- MISSED golden item: 'Pork Katsu'
- MISSED golden item: 'Sesame Chicken'
- MISSED golden item: 'Mixed Tempura'
- EXTRA predicted item: 'Sushi Combo'
- EXTRA predicted item: 'Seaweed Chicken'
- EXTRA predicted item: 'Crispy Chicken'
- EXTRA predicted item: 'Chicken Gyoza'
- EXTRA predicted item: 'Crispy Gyoza'
- EXTRA predicted item: 'Seaweed Salad Shrimp'
- EXTRA predicted item: 'Seafood Ramen'
- EXTRA predicted item: 'Spicy Ramen'
- EXTRA predicted item: 'Miso Ramen'
- EXTRA predicted item: 'Spicy Miso Ramen'
- EXTRA predicted item: 'Tempura Soup'
- EXTRA predicted item: 'Wonton Soup'
- EXTRA predicted item: 'Egg Drop Soup'
- EXTRA predicted item: 'Vegetable Soup'
- EXTRA predicted item: 'Beef Doodon'
- EXTRA predicted item: 'Veggie Doodon'
- EXTRA predicted item: 'Chicken Doodon'
- EXTRA predicted item: 'Eel Doodon'
- EXTRA predicted item: 'Chicken Teriyaki'
- EXTRA predicted item: 'Pork'
- EXTRA predicted item: 'Katsu'
- EXTRA predicted item: 'Chirashi'
- EXTRA predicted item: 'Miso Soup and Sushi Combo'
- EXTRA predicted item: 'Seaweed Chicken'
- EXTRA predicted item: 'Crispy Chicken'

