# Eval report 2026-08-10-p1-sd-noodles-verify

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.1333 | >= 0.97 | FAIL |
| item_precision | 0.0800 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.2500 | >= 0.90 | FAIL |
| price_accuracy | 0.0000 | >= 0.97 | FAIL |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-noodles-kitchen | 25/15 | 0.133 | 0.080 | 0.250 | 0.000 | 1.000 |

## Token usage and cost

- input: 4142
- cache write: 18027
- cache read: 26940
- output: 2515
- estimated cost: $0.0419

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 1 | 8980 | 0 |
| details_batch_n | 3 | 0 | 26940 |
| index | 1 | 9047 | 0 |

- cache check (details calls 2+): 3/3 had cache reads > 0 [ok]

## Diffs: km-sushi-noodles-kitchen

- price mismatch on 'Miso Soup': pred=2.5/'2.50' gold=2.95/'2.95'
- ingredients on 'Miso Soup': missing=['miso', 'seaweed', 'tofu'] extra=[]
- price mismatch on 'Chicken Teriyaki': pred=7.99/'7.99' gold=11.95/'11.95'
- ingredients on 'Chicken Teriyaki': missing=['green cabbage', 'teriyaki sauce'] extra=[]
- MISSED golden item: 'Chicken Udon'
- MISSED golden item: 'Vegetable Udon'
- MISSED golden item: 'Spicy Beef Udon'
- MISSED golden item: 'Tempura Udon'
- MISSED golden item: 'Donkotsu Ramen'
- MISSED golden item: 'Spicy Seafood Ramen'
- MISSED golden item: 'Yakisoba'
- MISSED golden item: 'Children's Combo'
- MISSED golden item: 'Chicken Katsu'
- MISSED golden item: 'Pork Katsu'
- MISSED golden item: 'Steak Teriyaki'
- MISSED golden item: 'Sesame Chicken'
- MISSED golden item: 'Mixed Tempura'
- EXTRA predicted item: 'Edamame'
- EXTRA predicted item: 'Gyoza'
- EXTRA predicted item: 'Beef Dumplings'
- EXTRA predicted item: 'Chicken Fried Rice'
- EXTRA predicted item: 'Vegetable Fried Rice'
- EXTRA predicted item: 'Shrimp Fried Rice'
- EXTRA predicted item: 'Combination Fried Rice'
- EXTRA predicted item: 'Pad Thai'
- EXTRA predicted item: 'Pad See Ew'
- EXTRA predicted item: 'Pad Krapow Moo'
- EXTRA predicted item: 'Pad Krapow Gai'
- EXTRA predicted item: 'Drunken Noodles'
- EXTRA predicted item: 'Pad Broccoli'
- EXTRA predicted item: 'Pad Cashew Chicken'
- EXTRA predicted item: 'Green Curry'
- EXTRA predicted item: 'Red Curry'
- EXTRA predicted item: 'Panang Curry'
- EXTRA predicted item: 'Masaman Curry'
- EXTRA predicted item: 'Seafood Soup'
- EXTRA predicted item: 'Chicken Teriyaki'
- EXTRA predicted item: 'Pork'
- EXTRA predicted item: 'Katsu'
- EXTRA predicted item: 'Miso Bowl'

