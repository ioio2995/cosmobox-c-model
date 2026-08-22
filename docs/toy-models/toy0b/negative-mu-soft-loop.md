# Toy Model 0B — mode cyclique mou à mu négatif

Statut : **validé pour gel — support analytique / qualification préalable**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `parameter-campaign-structure.md`, `cyclic-tangent-orthogonality.md`, `derivative-control.md`, `truncation-design-qualification.md`

Ce document consigne la structure asymptotique du spectre lorsque `mu -> -infinity` à `delta=0`, ainsi que les conséquences méthodologiques pour la campagne. Les valeurs numériques déjà inspectées sont classées comme qualification de design non confirmatoire.

## 1. Projection de matière pour mu -> -infinity

Le terme de matière est :

```math
2\mu N_{even},
\qquad
N_{even}=n_0+n_2+n_4.
```

Dans le secteur à trois fermions, la valeur maximale :

```math
N_{even}=3
```

est réalisée par une unique configuration :

```math
n_+=(1,0,1,0,1,0).
```

Pour `mu<0`, cette configuration est abaissée de `2|mu|` par unité de `N_even` relativement aux configurations ayant moins d'occupations paires. Ainsi, à `g` fixé et `delta=0` :

```math
\mu\to-\infty
```

projette le sous-espace de basse énergie vers la fibre de flux associée à `n_+`.

## 2. Fibre de flux de n_+

Pour :

```math
n_+=(1,0,1,0,1,0),
```

les charges alternent :

```math
q=(1,-1,1,-1,1,-1).
```

Une paramétrisation compatible avec Gauss est :

```math
E_{even}=e,
\qquad
E_{odd}=e-1.
```

La configuration a `spread=1`, donc le nombre d'états de sa fibre vaut :

```math
2\Lambda+1-1=2\Lambda.
```

Ainsi :

```text
Lambda=2 -> 4 états de fibre
Lambda=3 -> 6 états de fibre
```

Cette différence de cardinalité ne signifie pas que tous ces états sont quasi-dégénérés.

## 3. Coquilles électriques à delta=0

À `delta=0`, l'énergie électrique dans cette fibre vaut :

```math
V_0(e)
=\sum_iE_i^2
=3e^2+3(e-1)^2
=6\left(e-\frac12\right)^2+\frac32.
```

Les deux minima entiers sont :

```text
e=0
e=1
```

avec :

```math
V_0(0)=V_0(1)=3.
```

La paire suivante :

```text
e=-1
e=2
```

est à :

```math
V_0=15,
```

soit une séparation électrique :

```math
\Delta E_{shell}=12g.
```

La paire suivante est encore plus haute.

Donc, pour `g>0` modéré, la structure de basse énergie est un **doublet central de flux**, pas un multiplet quasi-dégénéré contenant toute la fibre.

Lorsque `g` diminue, les séparations de coquilles sont comprimées proportionnellement à `g`; c'est alors que le nombre d'états de fibre dépendant de `Lambda` devient un risque accru pour la troncature.

## 4. Symétrie du doublet central

À `delta=0`, la réflexion `R` est exacte. Dans la fibre `n_+`, elle échange les deux états centraux :

```text
e=0 <-> e=1.
```

Les deux éléments diagonaux de tout Hamiltonien effectif respectant `R` sont donc égaux.

Le splitting du doublet provient du couplage hors-diagonal entre ces deux secteurs de flux.

Dans ce doublet :

```math
\Phi=e-\frac12,
```

et donc les deux états ont :

```math
\Phi=-\frac12,
\qquad
\Phi=+\frac12.
```

À convention de base près :

```math
2\Phi\longrightarrow\sigma_z
```

après projection sur le doublet central.

## 5. Le couplage est un processus cyclique

Passer de `e=0` à `e=1` change tous les liens de la même quantité :

```math
\Delta E_i=+1
\qquad\forall i.
```

C'est précisément un shift uniforme du degré cyclique.

Un hopping élémentaire ne modifie qu'un seul lien. Pour revenir à la même configuration de matière `n_+` tout en augmentant les six liens d'une unité, il faut donc au moins six hoppings.

Ainsi le premier couplage possible entre les deux états centraux est d'ordre opératoriel :

```text
J^6
```

ou supérieur si une annulation supplémentaire intervient.

Pour `mu -> -infinity`, les cinq états intermédiaires d'un processus minimal quittent le sous-espace `N_even=3` et portent des dénominateurs d'énergie d'ordre `|mu|`. Il en résulte la loi d'ordre :

```math
t_{loop}(\mu)=O\!\left(\frac{J^6}{|\mu|^5}\right),
```

à `g` fixé, sous l'hypothèse standard d'une expansion perturbative régulière.

La non-annulation analytique du coefficient dominant n'est pas déclarée comme théorème tant que ce coefficient n'est pas calculé explicitement.

## 6. Action de delta dans le doublet

Toujours dans la fibre `n_+`, le terme électrique alterné est :

```math
V_\delta
=\sum_i(-1)^iE_i^2.
```

Pour les deux états centraux :

```math
E_{el}(e=0)=3g(1-\delta),
```

```math
E_{el}(e=1)=3g(1+\delta).
```

Le splitting diagonal nu créé par `delta` vaut donc :

```math
\Delta E_\delta=6g\delta.
```

Dans la base du doublet central, la structure effective est donc de la forme :

```math
H_{eff}
=E_c I
+3g\delta\,\sigma_z
+t_{loop}(\mu)\,\sigma_x
+\cdots,
```

à conventions de base près.

À `delta=0`, le gap du doublet vaut au premier ordre effectif :

```math
gap_0=2|t_{loop}|.
```

Le rapport de contrôle naturel est donc :

```math
x
=\frac{3g\delta}{|t_{loop}|}
=\frac{6g\delta}{gap_0}.
```

L'échelle de crossover est :

```math
\boxed{\delta_c=\frac{gap_0}{6g}}.
```

Le régime linéaire local exige :

```math
|\delta|\ll\delta_c,
```

ou équivalemment :

```math
|x|\ll1.
```

Quand `mu -> -infinity`, `delta_c` s'effondre comme `|mu|^-5` si le coefficient dominant de `t_loop` est non nul.

## 7. Prédictions universelles du modèle à deux niveaux

Pour le Hamiltonien effectif réduit ci-dessus, deux quantités ont une forme universelle en fonction de :

```math
x=\frac{6g\delta}{gap_0}.
```

### Gap du doublet

Au premier ordre du modèle à deux niveaux :

```math
\frac{gap(\delta)}{gap_0}
=\sqrt{1+x^2}.
```

### Polarisation cyclique

Comme `2Phi -> sigma_z` dans le doublet central, l'état fondamental effectif donne :

```math
2\langle\Phi\rangle
=-\frac{x}{\sqrt{1+x^2}}.
```

Le signe est fixé : pour `delta>0` (`x>0`), l'état central de flux `e=0` est énergétiquement favorisé, et cet état a `Phi=-1/2`.

Ces deux collapses sont les tests directs de la réduction à deux niveaux. Dans le modèle complet, ils sont des **prédictions asymptotiques de modèle effectif**, pas des identités exactes à `mu` fini.

### Delta_1

`Delta_1` est une quantité dynamique dérivée de réponses de Kubo et de temps caractéristiques. Elle n'est pas l'espérance d'un opérateur fixe du doublet.

Par conséquent, la réduction à deux niveaux ne démontre pas à elle seule une courbe universelle exacte :

```math
\Delta_1(\mu,\delta)=f(x)
```

indépendante de `mu`.

Un collapse de `Delta_1` en fonction de `x` est une **hypothèse secondaire discriminante** à tester. Sa violation n'invalide pas à elle seule le mécanisme de doublet si le gap et la polarisation suivent la réduction effective.

## 8. Qualification numérique divulguée

À `g=1`, `delta=0`, une première qualification avait donné :

| mu | -2 | -1.5 | -1.25 | -1 | -0.75 | -0.5 | 0 | +1 | +2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap_GS | 0.015 | 0.052 | 0.104 | 0.214 | 0.420 | 0.736 | 1.562 | 3.397 | 5.297 |

Une qualification supplémentaire a prolongé l'axe négatif :

| mu | -1.5 | -2 | -3 | -4 | -6 | -8 |
|---:|---:|---:|---:|---:|---:|---:|
| gap_GS | 5.2e-2 | 1.5e-2 | 2.2e-3 | 5.2e-4 | 6.5e-5 | 1.5e-5 |
| pente locale d ln(gap) / d ln|mu| | -3.47 | -4.28 | -4.76 | -5.03 | -5.15 | -5.18 |

Ces valeurs sont `DESIGN_QUALIFICATION`, pas un résultat confirmatoire.

La convergence de la pente locale vers `-5` fournit une confirmation numérique préalable très forte que le terme d'ordre `J^6/|mu|^5` est effectivement non nul dans le régime inspecté. Cette information doit être divulguée et ne peut pas être présentée ultérieurement comme une découverte confirmatoire indépendante.

Les écarts à la pente `-5` vers `mu=-1` ou `-1.5` sont interprétés comme corrections sub-asymptotiques compatibles avec la même structure.

La qualification ne démontre toujours pas l'absence de tout croisement à `mu` fini.

## 9. Conséquence pour la dérivée Xi_1

Dans le régime mou, une famille de pas absolus indépendante de `mu` devient mal dimensionnée parce que :

```math
\delta_c(\mu)=\frac{gap_0(\mu)}{6g}
```

s'effondre rapidement.

Une valeur `h >> delta_c` polarise déjà le doublet et ne sonde plus la pente locale à `delta=0`. Dans ce cas :

```math
\widehat\Xi_1(h)=\frac{\Delta_1(h)}{h}
```

peut varier fortement avec `h` pour une raison de dimensionnement du contrôle.

La sous-campagne SOFT-LOOP doit donc utiliser la famille adimensionnée `A_delta` définie dans `derivative-control.md`, avec :

```math
h_k=\alpha_k\frac{gap_{GS}^{(Lambda=2)}(g,\mu,0)}{6g}.
```

Les mêmes pas physiques sont utilisés à `Lambda=2` et `Lambda=3`.

## 10. Conséquence pour la troncature

La fibre de `n_+` contient `2Lambda` états, mais à `delta=0` et `g>0` ils s'organisent en coquilles électriques séparées.

Il est donc incorrect d'argumenter :

```text
4 états à Lambda=2 contre 6 à Lambda=3
=> tout le multiplet bas dépend du cutoff
```

sans tenir compte des séparations électriques.

Le risque devient plus fort lorsque :

```text
g diminue
|delta| augmente, via g_weak
a région mu<0 concentre la matière dans n_+
```

car les coquilles de flux se rapprochent alors que la fibre disponible dépend du cutoff.

Le coin petit `g`, `mu<0`, grand `|delta|` reste donc un point de stress privilégié, mais pour une raison spectrale plus précise que le seul comptage.

## 11. Conséquence pour la campagne en mu

Le côté `mu<0` n'est pas seulement une région numériquement difficile. Il contient un mécanisme identifiable de ramollissement du degré cyclique.

Il est donc scientifiquement justifié de l'échantillonner plus finement que le côté positif, à condition que cette asymétrie soit préenregistrée et que les données de qualification utilisées pour la choisir soient divulguées.

Une sous-campagne ciblée sur le mode mou peut être plus efficace qu'un produit cartésien dense de toute la grille `(g,mu,delta)`.

Les valeurs numériques exactes de la sous-campagne restent à figer dans le paquet de campagne. Les points déjà inspectés jusqu'à `mu=-8` sont de toute façon marqués comme qualification de design préalable.

## 12. Statut

```text
NEGATIVE_MU_MATTER_PROJECTION       = VALIDATED_FOR_FREEZE_ASYMPTOTIC
NPLUS_FLUX_FIBER_SIZE               = VALIDATED_FOR_FREEZE
CENTRAL_FLUX_DOUBLET_DELTA0         = VALIDATED_FOR_FREEZE
FULL_FIBER_QUASIDEGENERATE          = REJECTED
LOOP_TUNNEL_MIN_HOP_ORDER           = 6
LOOP_TUNNEL_MU_SCALING              = O(|mu|^-5), ANALYTIC ORDER
LOOP_TUNNEL_MU_EXPONENT_NUMERIC     = CONFIRMED_IN_DESIGN_QUALIFICATION
DELTA_BARE_DOUBLET_SPLITTING        = 6 g delta
SOFT_LOOP_DELTA_C                   = gap_0/(6g)
SOFT_LOOP_LINEAR_REGIME             = |delta| << delta_c
SOFT_LOOP_GAP_COLLAPSE              = EFFECTIVE_MODEL_PREDICTION
SOFT_LOOP_PHI_COLLAPSE              = EFFECTIVE_MODEL_PREDICTION
DELTA1_UNIVERSAL_COLLAPSE           = SECONDARY_HYPOTHESIS
SOFT_CYCLIC_MODE_INTERPRETATION     = VALIDATED_FOR_FREEZE_ASYMPTOTIC
FINITE_MU_NO_CROSSING_THEOREM       = NOT_ESTABLISHED
NEGATIVE_MU_REFINEMENT              = SCIENTIFICALLY_JUSTIFIED
TRUNCATION_STRESS_SMALL_G_NEG_MU    = VALIDATED_IN_PRINCIPLE
```
