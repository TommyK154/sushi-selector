# Eval report 2026-08-10-p1-sd-masa-verify

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.9398 | >= 0.97 | FAIL |
| item_precision | 0.8013 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.6745 | >= 0.90 | FAIL |
| price_accuracy | 0.8320 | >= 0.97 | FAIL |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| masa-sushi | 156/133 | 0.940 | 0.801 | 0.674 | 0.832 | 0.984 |

## Token usage and cost

- input: 19512
- cache write: 36062
- cache read: 170658
- output: 13491
- estimated cost: $0.1491

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 2 | 17964 | 0 |
| details_batch_n | 19 | 0 | 170658 |
| index | 2 | 18098 | 0 |

- cache check (details calls 2+): 19/19 had cache reads > 0 [ok]

## Diffs: masa-sushi

- ingredients on 'Edamame': missing=['soybean'] extra=['edamame']
- price mismatch on 'Garlic Edamame / Spicy Garlic Edamame': pred=7.99/'7.99' gold=7.25/'7.25'
- ingredients on 'Garlic Edamame / Spicy Garlic Edamame': missing=['soybean'] extra=['edamame']
- ingredients on 'Green Salad': missing=['ginger dressing'] extra=[]
- ingredients on 'Mixed Tempura': missing=['shrimp'] extra=['tempura', 'vegetable']
- ingredients on 'Vegetable Tempura': missing=[] extra=['tempura', 'vegetable']
- ingredients on 'Gyoza': missing=['cabbage', 'pork'] extra=['gyoza']
- price mismatch on 'Shrimp': pred=9.99/'9.99' gold=6.45/'sushi 6.45'
- ingredients on 'Beach Ball': missing=[] extra=['crab', 'scallop', 'shrimp']
- ingredients on 'D.S. Poppers': missing=[] extra=['jalapeno']
- ingredients on 'Chicken': missing=['teriyaki sauce'] extra=[]
- ingredients on 'Beef Teriyaki': missing=['teriyaki sauce'] extra=[]
- price mismatch on 'Yellowtail Collar': pred=19.99/'19.99' gold=18.99/'18.99'
- price mismatch on 'Oyster Shooter': pred=10.0/'10.00' gold=10.99/'10.99'
- price mismatch on 'Fatty Tuna': pred=None/'M/P' gold=None/'sushi M/P / sashimi M/P'
- price mismatch on 'Bluefin Tuna': pred=None/'M/P' gold=None/'sushi M/P / sashimi M/P'
- price mismatch on 'Sea Urchin': pred=None/'M/P' gold=None/'sushi M/P / sashimi M/P'
- price mismatch on 'Sweet Shrimp': pred=None/'M/P' gold=None/'sushi M/P'
- price mismatch on 'Amberjack': pred=7.95/'7.95' gold=None/'sushi 7.95 / sashimi 25.99'
- price mismatch on 'Spanish Mackerel': pred=7.95/'7.95' gold=None/'sushi 7.95 / sashimi 25.99'
- price mismatch on 'Tuna': pred=6.95/'6.95' gold=None/'sushi 6.95 / sashimi 19.99'
- ingredients on 'Cajun Tuna': missing=['tuna'] extra=['cajun tuna']
- price mismatch on 'Escolar': pred=7.5/'7.50' gold=None/'sushi 7.50 / sashimi 21.99'
- price mismatch on 'Salmon': pred=7.25/'7.25' gold=None/'sushi 7.25 / sashimi 19.99'
- price mismatch on 'Smoked Salmon': pred=7.55/'7.55' gold=None/'sushi 7.55 / sashimi 19.99'
- price mismatch on 'Yellowtail': pred=7.5/'7.50' gold=None/'sushi 7.55 / sashimi 21.99'
- price mismatch on 'Albacore': pred=6.95/'6.95' gold=None/'sushi 6.95 / sashimi 19.99'
- price mismatch on 'Fresh Water Eel': pred=7.25/'7.25' gold=None/'sushi 7.25 / sashimi 21.99'
- price mismatch on 'Mackerel': pred=6.5/'6.50' gold=None/'sushi 6.50 / sashimi 18.99'
- price mismatch on 'Octopus': pred=6.5/'6.50' gold=None/'sushi 6.50 / sashimi 19.99'
- price mismatch on 'Scallop': pred=7.95/'7.95' gold=None/'sushi 7.95 / sashimi 21.99'
- ingredients on 'Quail Egg': missing=['quail egg'] extra=['egg']
- ingredients on 'The Six Dollar Roll': missing=['shrimp tempura', 'spicy tuna'] extra=['crab']
- ingredients on 'Ojai Roll': missing=['crab', 'masago', 'radish sprout', 'shrimp tempura'] extra=['carrot', 'sweet egg']
- ingredients on 'Spicy Lancaster Roll': missing=['crab', 'masago', 'radish sprout', 'shrimp tempura'] extra=[]
- ingredients on 'Cell One Roll': missing=['scallop'] extra=['spicy tuna']
- ingredients on 'Bart Simpson Roll': missing=['crab', 'cucumber', 'masago', 'radish sprout'] extra=['small egg']
- ingredients on 'Chilean Lobster Roll': missing=['crawfish'] extra=['crab']
- ingredients on 'J.M. Roll': missing=['eel sauce'] extra=[]
- ingredients on 'O.B. Roll': missing=['crab'] extra=[]
- ingredients on 'S.O.B. Hand Roll': missing=['crab', 'cucumber', 'jalapeno', 'masago', 'quail egg', 'spicy yellowtail'] extra=['small egg', 'spicy crab']
- ingredients on 'Alaskan Roll': missing=['crab', 'radish sprout', 'salmon'] extra=['cooked salmon', 'roe']
- ingredients on 'A.J. Roll': missing=['eel', 'eel sauce'] extra=['roe']
- ingredients on 'Jeff San Roll': missing=['avocado', 'crab', 'cucumber', 'salmon'] extra=['cooked salmon']
- ingredients on 'Hako Sushi': missing=['eel', 'eel sauce'] extra=['roe']
- ingredients on 'Green Mussel Roll': missing=['avocado', 'crab'] extra=[]
- ingredients on 'Yellowtail Delight': missing=['asparagu', 'avocado', 'cucumber', 'hot sauce', 'yuzu ponzu'] extra=[]
- ingredients on 'Cajun Tuna Roll': missing=['cajun tuna', 'garlic ponzu', 'green onion'] extra=['cajun']
- ingredients on 'Oh! No Roll': missing=['escolar', 'hot sauce', 'jalapeno', 'yuzu ponzu'] extra=['jalapeño']
- ingredients on 'Super Green Roll': missing=['asparagu', 'cucumber', 'gobo'] extra=[]
- ingredients on 'Rainbow Roll': missing=['crab', 'cucumber'] extra=[]
- ingredients on 'Tropical Roll': missing=['crab', 'cucumber', 'orange'] extra=['mango']
- ingredients on 'Omega 3 Roll': missing=['avocado', 'salmon'] extra=[]
- ingredients on 'Ocean Roll': missing=['seaweed salad', 'spicy tuna'] extra=['avocado', 'crab']
- ingredients on 'Fire Cracker Roll': missing=['avocado', 'crunch', 'cucumber', 'jalapeno', 'spicy crab'] extra=['jalapeño']
- ingredients on 'Cucumber Wrap Roll': missing=['cucumber', 'salmon', 'spicy crab', 'tuna'] extra=['spicy tuna', 'yellowtail']
- ingredients on 'Amazon Roll': missing=['avocado', 'salmon', 'tuna'] extra=['spicy tuna']
- ingredients on 'Ventura Roll': missing=['spicy scallop'] extra=['inside spicy tuna on top']
- ingredients on 'Amigo Roll': missing=['jalapeno', 'spicy crab'] extra=['avocado inside', 'spicy crab meat']
- ingredients on '101 Roll': missing=['crunch', 'jalapeno'] extra=['jalapeño inside and on top']
- ingredients on 'Red Dragon Roll': missing=['avocado', 'tuna'] extra=['inside spicy tuna and avocado on top']
- ingredients on 'Play Boy Roll': missing=['avocado', 'cream cheese', 'shrimp', 'smoked salmon'] extra=['cucumber', 'inside spicy tuna and avocado on top', 'spicy tuna']
- ingredients on 'White Tiger Roll': missing=['albacore', 'crunch', 'onion'] extra=['inside spicy tuna and avocado on top']
- ingredients on 'Bryan San Roll': missing=['crab', 'eel', 'tuna'] extra=['crab meat', 'lime on top']
- ingredients on 'Baked Salmon Roll': missing=['avocado', 'crab'] extra=['cream cheese']
- ingredients on 'Snow Roll': missing=['albacore', 'avocado'] extra=['scallop']
- ingredients on 'Lobster Roll': missing=['avocado', 'crawfish', 'cucumber'] extra=[]
- ingredients on 'B.S.C.R.': missing=['avocado', 'crab', 'cucumber'] extra=[]
- ingredients on 'Black Dragon Roll': missing=['crab', 'cucumber'] extra=[]
- ingredients on 'Tiger Roll': missing=['avocado', 'crab', 'cucumber'] extra=[]
- ingredients on 'Daisy Roll': missing=['salmon'] extra=[]
- ingredients on 'Camarillo Roll': missing=['eel'] extra=[]
- ingredients on 'Crunch Roll': missing=['crab', 'crunch', 'cucumber'] extra=['crab meat', 'crab stick']
- ingredients on 'Salmon Tempura Roll': missing=['crab'] extra=['crab meat']
- ingredients on 'Vegas Roll': missing=['avocado', 'crab', 'jalapeno'] extra=['white fish']
- ingredients on 'Masa's 3 Putt Roll': missing=['albacore', 'tuna'] extra=['scallop', 'white fish tuna']
- ingredients on 'Spider Roll': missing=['avocado', 'gobo', 'radish sprout'] extra=['gado', 'spicy tuna']
- ingredients on 'Popcorn Lobster Roll': missing=['crawfish'] extra=['avocado', 'crab stick', 'lobster tail on top']
- ingredients on 'Lumbar Roll': missing=['avocado', 'crab'] extra=['deep fried crab meat']
- ingredients on 'Energy Roll': missing=['crab', 'eel', 'shrimp tempura'] extra=['spicy salmon', 'spicy tuna']
- ingredients on 'Jim San Roll': missing=['asparagu', 'crab', 'shrimp tempura', 'tuna'] extra=['egg', 'shrimp']
- ingredients on 'Shrimp Killer Roll': missing=['avocado', 'crab', 'cucumber', 'shrimp', 'shrimp tempura'] extra=['cream cheese', 'jalapeno', 'spicy tuna']
- ingredients on 'Fantasy Roll': missing=['albacore', 'tuna'] extra=['abalone']
- ingredients on 'California Roll': missing=['crab'] extra=['imitation crab']
- ingredients on 'Spicy California Roll': missing=['crab', 'spicy mayo'] extra=['imitation crab', 'spicy sauce']
- ingredients on 'Spicy Tuna Roll': missing=['spicy tuna'] extra=['spicy sauce', 'tuna']
- ingredients on 'Spicy Scallop Roll': missing=['spicy scallop'] extra=['scallop', 'spicy sauce']
- ingredients on 'Sweet Eel Roll': missing=['eel sauce'] extra=[]
- ingredients on 'Philly Roll': missing=[] extra=['avocado']
- ingredients on 'Vegetable Roll': missing=[] extra=['avocado', 'cucumber']
- ingredients on 'Vegetable Tempura Roll': missing=[] extra=['tempura']
- ingredients on 'Popeye Hand Roll': missing=['masago', 'quail egg', 'scallop', 'spinach', 'tuna'] extra=['mango']
- ingredients on 'Y2K Roll': missing=['avocado', 'crab'] extra=['scallion', 'yellowtail']
- price mismatch on 'Great Jeff Roll': pred=14.99/'14.99' gold=15.99/'15.99'
- ingredients on 'Great Jeff Roll': missing=['avocado', 'crab', 'tuna'] extra=['eel', 'inside spicy tuna and avocado on top']
- MISSED golden item: 'Shishito Pepper'
- MISSED golden item: 'Sesame Tofu'
- MISSED golden item: 'Crispy Rice with Spicy Tuna'
- MISSED golden item: 'Fresh Oyster'
- MISSED golden item: 'Shumai'
- MISSED golden item: 'Halibut'
- MISSED golden item: 'Montgomery Hand Roll'
- MISSED golden item: 'Teriyaki Roll'
- EXTRA predicted item: 'Jalapeno Popper'
- EXTRA predicted item: 'Spicy Tuna'
- EXTRA predicted item: 'Fresh Oyster, 2pcs'
- EXTRA predicted item: 'Oyster, 6pcs'
- EXTRA predicted item: 'Toro'
- EXTRA predicted item: 'Hon Maguro'
- EXTRA predicted item: 'Uni'
- EXTRA predicted item: 'Amaebi'
- EXTRA predicted item: 'Kanpachi'
- EXTRA predicted item: 'White Fish'
- EXTRA predicted item: 'Aji'
- EXTRA predicted item: 'Maguro'
- EXTRA predicted item: 'Ono'
- EXTRA predicted item: 'Sake'
- EXTRA predicted item: 'Sake Gunsai'
- EXTRA predicted item: 'Hamachi'
- EXTRA predicted item: 'Unagi'
- EXTRA predicted item: 'Saba'
- EXTRA predicted item: 'Tako'
- EXTRA predicted item: 'Kaibashira'
- EXTRA predicted item: 'Ikura'
- EXTRA predicted item: 'Masago'
- EXTRA predicted item: 'Hokigai'
- EXTRA predicted item: 'Ika'
- EXTRA predicted item: 'Shrimp'
- EXTRA predicted item: 'Ebi'
- EXTRA predicted item: 'Tamago'
- EXTRA predicted item: 'Inari'
- EXTRA predicted item: 'Uzura'
- EXTRA predicted item: 'Montgomery'
- EXTRA predicted item: 'Teriyaki Roll (chicken or beef)'

