# Eval report 2026-08-10-p1-sd-noodles-control

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.3333 | >= 0.97 | FAIL |
| item_precision | 0.1786 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.3400 | >= 0.90 | FAIL |
| price_accuracy | 0.4000 | >= 0.97 | FAIL |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| km-sushi-noodles-kitchen | 28/15 | 0.333 | 0.179 | 0.340 | 0.400 | 1.000 |

## Token usage and cost

- input: 4221
- cache write: 17469
- cache read: 26103
- output: 2558
- estimated cost: $0.0415

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 1 | 8701 | 0 |
| details_batch_n | 3 | 0 | 26103 |
| index | 1 | 8768 | 0 |

- cache check (details calls 2+): 3/3 had cache reads > 0 [ok]

## Diffs: km-sushi-noodles-kitchen

- price mismatch on 'Chicken Teriyaki': pred=12.95/'12.95' gold=11.95/'11.95'
- ingredients on 'Chicken Teriyaki': missing=['green cabbage'] extra=[]
- price mismatch on 'Chicken Katsu': pred=13.99/'13.99' gold=17.99/'17.99'
- ingredients on 'Chicken Katsu': missing=['katsu sauce', 'panko'] extra=[]
- ingredients on 'Miso Soup': missing=['miso', 'seaweed', 'tofu'] extra=[]
- ingredients on 'Vegetable Udon': missing=['soy sauce broth', 'udon noodle'] extra=['vegetable']
- price mismatch on 'Steak Teriyaki': pred=14.5/'14.50' gold=13.99/'13.99'
- ingredients on 'Steak Teriyaki': missing=['beef', 'green cabbage'] extra=['chicken']
- MISSED golden item: 'Chicken Udon'
- MISSED golden item: 'Spicy Beef Udon'
- MISSED golden item: 'Tempura Udon'
- MISSED golden item: 'Donkotsu Ramen'
- MISSED golden item: 'Spicy Seafood Ramen'
- MISSED golden item: 'Yakisoba'
- MISSED golden item: 'Children's Combo'
- MISSED golden item: 'Pork Katsu'
- MISSED golden item: 'Sesame Chicken'
- MISSED golden item: 'Mixed Tempura'
- EXTRA predicted item: 'Chicken Teriyaki Combo'
- EXTRA predicted item: 'Seaweed Salad'
- EXTRA predicted item: 'Edamame'
- EXTRA predicted item: 'Seafood Ramen'
- EXTRA predicted item: 'Pork Ramen'
- EXTRA predicted item: 'Vegetable Ramen'
- EXTRA predicted item: 'Chicken Teriyaki Bowl'
- EXTRA predicted item: 'Beef Dodon'
- EXTRA predicted item: 'Shrimp Tempura'
- EXTRA predicted item: 'Tempura Eel'
- EXTRA predicted item: 'Teriyaki Salmon'
- EXTRA predicted item: 'Seafood Tempura'
- EXTRA predicted item: 'Spicy Tuna Roll'
- EXTRA predicted item: 'Spicy Salmon Roll'
- EXTRA predicted item: 'Spicy Yellowtail Roll'
- EXTRA predicted item: 'Shrimp Tempura Roll'
- EXTRA predicted item: 'Sweetfish Eel Roll'
- EXTRA predicted item: 'Yellowtail Roll'
- EXTRA predicted item: 'Pork Belly Roll'
- EXTRA predicted item: 'Soft Shell Crab Roll'
- EXTRA predicted item: 'Pork'
- EXTRA predicted item: 'Deep Fried Pork Breaded Chicken Teriyaki'
- EXTRA predicted item: 'Katsu'

