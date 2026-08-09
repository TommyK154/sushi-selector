# Eval report 2026-08-06-p1-sb2-diag-masa

Model: `claude-haiku-4-5-20251001`

## Gates

| Gate | Measured | Threshold | Result |
|---|---|---|---|
| item_recall | 0.9549 | >= 0.97 | FAIL |
| item_precision | 0.8141 | >= 0.97 | FAIL |
| ingredient_f1_macro | 0.6809 | >= 0.90 | FAIL |
| price_accuracy | 0.8189 | >= 0.97 | FAIL |

## Per-menu breakdown

| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| masa-sushi | 156/133 | 0.955 | 0.814 | 0.681 | 0.819 | 0.969 |

## Token usage and cost

- input: 19507
- cache write: 34938
- cache read: 165319
- output: 13310
- estimated cost: $0.1463

### Cache counters by call kind

| Kind | Calls | Cache write | Cache read |
|---|---|---|---|
| details_batch_1 | 2 | 17402 | 0 |
| details_batch_n | 19 | 0 | 165319 |
| index | 2 | 17536 | 0 |

- cache check (details calls 2+): 19/19 had cache reads > 0 [ok]

## Diffs: masa-sushi

- ingredients on 'Edamame': missing=['soybean'] extra=['edamame']
- price mismatch on 'Garlic Edamame / Spicy Garlic Edamame': pred=7.99/'7.99' gold=7.25/'7.25'
- ingredients on 'Garlic Edamame / Spicy Garlic Edamame': missing=['soybean'] extra=['edamame']
- ingredients on 'Green Salad': missing=['ginger dressing'] extra=[]
- ingredients on 'Mixed Tempura': missing=['shrimp'] extra=['tempura']
- ingredients on 'Vegetable Tempura': missing=[] extra=['tempura']
- ingredients on 'Gyoza': missing=['cabbage'] extra=['vegetable']
- ingredients on 'Shumai': missing=[] extra=['pork']
- ingredients on 'Beach Ball': missing=[] extra=['masago', 'spicy tuna']
- ingredients on 'D.S. Poppers': missing=[] extra=['jalapeno', 'spicy tuna']
- price mismatch on 'Soft Shell Crab': pred=16.99/'16.99' gold=15.99/'15.99'
- ingredients on 'Chicken': missing=['teriyaki sauce'] extra=[]
- ingredients on 'Beef Teriyaki': missing=['teriyaki sauce'] extra=[]
- price mismatch on 'Yellowtail Collar': pred=19.99/'19.99' gold=18.99/'18.99'
- price mismatch on 'Fresh Oyster': pred=10.99/'10.99' gold=None/'2pcs 10.99 / 6pcs 24.99'
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
- price mismatch on 'Yellowtail': pred=7.25/'7.25' gold=None/'sushi 7.55 / sashimi 21.99'
- price mismatch on 'Albacore': pred=6.95/'6.95' gold=None/'sushi 6.95 / sashimi 19.99'
- price mismatch on 'Fresh Water Eel': pred=7.25/'7.25' gold=None/'sushi 7.25 / sashimi 21.99'
- ingredients on 'Fresh Water Eel': missing=['eel'] extra=['fresh water eel']
- price mismatch on 'Mackerel': pred=6.5/'6.50' gold=None/'sushi 6.50 / sashimi 18.99'
- price mismatch on 'Octopus': pred=6.5/'6.50' gold=None/'sushi 6.50 / sashimi 19.99'
- price mismatch on 'Scallop': pred=7.95/'7.95' gold=None/'sushi 7.95 / sashimi 21.99'
- price mismatch on 'Surf Clam': pred=6.95/'6.95' gold=6.25/'sushi 6.25'
- price mismatch on 'Squid': pred=7.25/'7.25' gold=6.25/'sushi 6.25'
- ingredients on 'The Six Dollar Roll': missing=['shrimp tempura', 'spicy tuna'] extra=['crab']
- ingredients on 'Ojai Roll': missing=['masago', 'radish sprout', 'shrimp tempura'] extra=['salmon']
- ingredients on 'Spicy Lancaster Roll': missing=['avocado', 'crab', 'masago', 'radish sprout', 'shrimp tempura'] extra=['jalapeno', 'spicy yellowtail']
- ingredients on 'Cell One Roll': missing=['scallop'] extra=['spicy tuna']
- ingredients on 'Bart Simpson Roll': missing=['avocado', 'cucumber', 'masago', 'radish sprout'] extra=[]
- ingredients on 'Chilean Lobster Roll': missing=['crawfish'] extra=['crab']
- ingredients on 'B.C. Roll': missing=['shrimp'] extra=[]
- ingredients on 'J.M. Roll': missing=['eel'] extra=[]
- ingredients on 'S.O.B. Hand Roll': missing=['avocado', 'crab', 'cucumber', 'jalapeno', 'masago', 'quail egg', 'spicy yellowtail'] extra=['eel sauce', 'scallop', 'spicy']
- ingredients on 'Alaskan Roll': missing=['crab', 'radish sprout', 'salmon'] extra=['cooked salmon']
- ingredients on 'A.J. Roll': missing=['eel', 'eel sauce'] extra=[]
- ingredients on 'Jeff San Roll': missing=['avocado', 'crab', 'cucumber', 'salmon'] extra=['cooked salmon']
- ingredients on 'Hako Sushi': missing=['crab', 'eel', 'eel sauce'] extra=['egg']
- ingredients on 'Green Mussel Roll': missing=['avocado', 'butter sauce', 'crab', 'green mussel'] extra=['butter', 'mussel']
- ingredients on 'Popeye Hand Roll': missing=['avocado', 'cucumber', 'masago', 'quail egg', 'scallop', 'spinach', 'tuna'] extra=['lettuce', 'shrimp', 'toro', 'wasabi']
- ingredients on 'Yellowtail Delight': missing=['asparagu', 'avocado', 'cucumber', 'hot sauce', 'yuzu ponzu'] extra=[]
- ingredients on 'Cajun Tuna Roll': missing=['cajun tuna', 'garlic ponzu', 'green onion'] extra=['cajun']
- ingredients on 'Oh! No Roll': missing=['escolar', 'hot sauce', 'jalapeno', 'yuzu ponzu'] extra=['spicy tuna']
- ingredients on 'Super Green Roll': missing=['asparagu', 'gobo'] extra=[]
- ingredients on 'Rainbow Roll': missing=['crab', 'cucumber'] extra=[]
- ingredients on 'Tropical Roll': missing=['avocado', 'crab', 'cucumber', 'orange', 'tomato'] extra=['mango', 'pineapple', 'tuna']
- ingredients on 'Omega 3 Roll': missing=['avocado', 'cream cheese', 'spicy salmon'] extra=['sweet cheese']
- ingredients on 'Ocean Roll': missing=['seaweed salad', 'spicy tuna'] extra=['avocado', 'tuna']
- ingredients on 'Fire Cracker Roll': missing=['avocado', 'crunch', 'spicy crab'] extra=[]
- ingredients on 'Cucumber Wrap Roll': missing=['cucumber', 'spicy crab', 'tuna'] extra=['avocado', 'cream cheese']
- ingredients on 'Amazon Roll': missing=['avocado', 'crab', 'salmon'] extra=['crab meat']
- ingredients on 'Ventura Roll': missing=['spicy scallop'] extra=['avocado']
- ingredients on 'Amigo Roll': missing=['jalapeno', 'spicy crab'] extra=['spicy crab meat']
- ingredients on '101 Roll': missing=['crunch', 'jalapeno'] extra=[]
- ingredients on 'Red Dragon Roll': missing=['avocado', 'tuna'] extra=[]
- ingredients on 'Play Boy Roll': missing=['avocado', 'cream cheese', 'shrimp', 'smoked salmon'] extra=['cucumber', 'spicy tuna']
- ingredients on 'White Tiger Roll': missing=['albacore', 'crunch', 'onion'] extra=[]
- ingredients on 'Bryan San Roll': missing=['crab', 'eel', 'tuna'] extra=['crab meat']
- ingredients on 'Baked Salmon Roll': missing=['avocado', 'crab'] extra=['cream cheese']
- ingredients on 'Snow Roll': missing=['albacore', 'avocado', 'cream cheese'] extra=['green cheese', 'scallop']
- ingredients on 'Lobster Roll': missing=['crawfish', 'cucumber'] extra=[]
- ingredients on 'B.S.C.R.': missing=['avocado', 'crab', 'cucumber'] extra=[]
- ingredients on 'Black Dragon Roll': missing=['crab', 'cucumber'] extra=[]
- ingredients on 'Tiger Roll': missing=['avocado', 'crab', 'cucumber'] extra=[]
- ingredients on 'Daisy Roll': missing=['salmon'] extra=[]
- ingredients on 'Camarillo Roll': missing=['eel'] extra=[]
- ingredients on 'Crunch Roll': missing=['crab', 'crunch', 'cucumber'] extra=['crab meat']
- ingredients on 'Salmon Tempura Roll': missing=['crab'] extra=['crab meat']
- ingredients on 'Vegas Roll': missing=['avocado', 'crab', 'jalapeno'] extra=['white fish roe']
- ingredients on 'Masa's 3 Putt Roll': missing=['albacore', 'tuna'] extra=['white fish roe']
- ingredients on 'Spider Roll': missing=['avocado', 'gobo', 'radish sprout'] extra=['ginger', 'spicy sauce']
- ingredients on 'Popcorn Lobster Roll': missing=['crawfish'] extra=['inside spicy tuna, deep fried lobster on top']
- ingredients on 'Lumbar Roll': missing=['avocado', 'crab'] extra=['crab meat', 'spicy crab']
- ingredients on 'Energy Roll': missing=['crab', 'eel', 'shrimp tempura'] extra=['spicy salmon', 'spicy tuna']
- ingredients on 'Jalapeno Bomb': missing=['cream cheese'] extra=[]
- ingredients on 'Jim San Roll': missing=['asparagu', 'crab', 'shrimp tempura', 'tuna'] extra=['jalapeno', 'yellowtail']
- ingredients on 'Shrimp Killer Roll': missing=['shrimp', 'shrimp tempura'] extra=['spicy sauce']
- ingredients on 'H.O.T Roll': missing=['jalapeno', 'spicy tuna'] extra=['spicy sauce']
- ingredients on 'Fantasy Roll': missing=['albacore', 'shrimp tempura', 'tuna'] extra=[]
- ingredients on 'California Roll': missing=['crab'] extra=['imitation crab']
- ingredients on 'Spicy California Roll': missing=['crab'] extra=['imitation crab']
- ingredients on 'Spicy Tuna Roll': missing=['spicy tuna'] extra=['spicy mayo', 'tuna']
- ingredients on 'Spicy Scallop Roll': missing=['spicy scallop'] extra=['scallop', 'spicy mayo']
- ingredients on 'Sweet Eel Roll': missing=['eel sauce'] extra=[]
- ingredients on 'Shrimp Tempura Roll': missing=[] extra=['avocado', 'cucumber']
- ingredients on 'Philly Roll': missing=[] extra=['avocado']
- ingredients on 'Vegetable Roll': missing=[] extra=['avocado', 'cucumber']
- ingredients on 'Vegetable Tempura Roll': missing=[] extra=['tempura']
- price mismatch on 'Great Jeff Roll': pred=14.99/'14.99' gold=15.99/'15.99'
- ingredients on 'Great Jeff Roll': missing=['avocado', 'crab', 'tuna'] extra=[]
- ingredients on 'Montgomery Hand Roll': missing=['spicy sauce'] extra=['cucumber']
- MISSED golden item: 'Shishito Pepper'
- MISSED golden item: 'Sesame Tofu'
- MISSED golden item: 'Crispy Rice with Spicy Tuna'
- MISSED golden item: 'Halibut'
- MISSED golden item: 'O.B. Roll'
- MISSED golden item: 'Teriyaki Roll'
- EXTRA predicted item: 'Seaweed Pepper'
- EXTRA predicted item: 'Ika Marinated'
- EXTRA predicted item: 'Tuna Teriyaki / Spicy Tuna'
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
- EXTRA predicted item: 'Ebi'
- EXTRA predicted item: 'Tamago'
- EXTRA predicted item: 'Inari'
- EXTRA predicted item: 'Uzura'
- EXTRA predicted item: 'O B. Roll'
- EXTRA predicted item: 'Teriyaki Roll (chicken or beef)'

