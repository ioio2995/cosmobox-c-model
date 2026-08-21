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

La non-annulation du coefficient dominant n'est pas déclarée comme théorème sans calcul analytique explicite du coefficient. La qualification numérique observée est cohérente avec un splitting qui décroît rapidement quand `mu` devient négatif.

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

À `delta=0`, le gap du doublet est contrôlé par le tunnel cyclique. Quand `mu -> -infinity`, ce tunnel devient mou tandis que `delta` continue de coupler linéairement les deux secteurs avec une échelle `g`.

C'est un mécanisme structurel de forte susceptibilité à la brisure `delta`, distinct d'un croisement évité générique entre états de nature non identifiée.

## 7. Qualification numérique divulguée

À `g=1`, `delta=0`, les gaps préalablement inspectés sont :

| mu | -2 | -1.5 | -1.25 | -1 | -0.75 | -0.5 | 0 | +1 | +2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap_GS | 0.015 | 0.052 | 0.104 | 0.214 | 0.420 | 0.736 | 1.562 | 3.397 | 5.297 |

Ces valeurs sont `DESIGN_QUALIFICATION`, pas un résultat confirmatoire.

Elles montrent sur les points inspectés une décroissance régulière du gap côté négatif, cohérente avec le mécanisme asymptotique ci-dessus. Elles ne démontrent pas à elles seules l'absence de tout croisement à `mu` fini.

À `mu=-2`, le spectre inspecté présente un doublet bas séparé du reste par un écart d'ordre 3, ce qui est compatible avec l'identification du premier gap comme splitting du doublet cyclique central.

## 8. Conséquence pour la troncature

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

## 9. Conséquence pour la campagne en mu

Le côté `mu<0` n'est pas seulement une région numériquement difficile. Il contient un mécanisme identifiable de ramollissement du degré cyclique.

Il est donc scientifiquement justifié de l'échantillonner plus finement que le côté positif, à condition que cette asymétrie soit préenregistrée et que les données de qualification utilisées pour la choisir soient divulguées.

Une sous-campagne ciblée sur le mode mou peut être plus efficace qu'un produit cartésien dense de toute la grille `(g,mu,delta)`.

## 10. Statut

```text
NEGATIVE_MU_MATTER_PROJECTION       = VALIDATED_FOR_FREEZE_ASYMPTOTIC
NPLUS_FLUX_FIBER_SIZE               = VALIDATED_FOR_FREEZE
CENTRAL_FLUX_DOUBLET_DELTA0         = VALIDATED_FOR_FREEZE
FULL_FIBER_QUASIDEGENERATE          = REJECTED
LOOP_TUNNEL_MIN_HOP_ORDER           = 6
LOOP_TUNNEL_MU_SCALING              = O(|mu|^-5), COEFFICIENT_OPEN
DELTA_BARE_DOUBLET_SPLITTING        = 6 g delta
SOFT_CYCLIC_MODE_INTERPRETATION     = VALIDATED_FOR_FREEZE_ASYMPTOTIC
FINITE_MU_NO_CROSSING_THEOREM       = NOT_ESTABLISHED
NEGATIVE_MU_REFINEMENT              = SCIENTIFICALLY_JUSTIFIED
TRUNCATION_STRESS_SMALL_G_NEG_MU    = VALIDATED_IN_PRINCIPLE
```
