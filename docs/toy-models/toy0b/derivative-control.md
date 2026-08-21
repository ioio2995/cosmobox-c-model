# Toy Model 0B — contrôle de stabilité des dérivées en delta

Statut : **validé pour gel — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document aligne le traitement des dérivées numériques sur la même logique de familles de contrôle déjà retenue pour `eta`, `epsilon_path` et `Gamma`.

## 1. Objet

Le diagnostic linéaire en la brisure est :

```math
\Xi_1(g,\mu)
=\left.\frac{\partial\Delta_1(g,\mu,\delta)}{\partial\delta}\right|_{\delta=0},
```

lorsque cette dérivée existe.

La covariance exacte :

```math
\Delta_1(g,\mu,-\delta)=-\Delta_1(g,\mu,+\delta)
```

implique :

```math
\Delta_1(g,\mu,0)=0.
```

La campagne principale à `delta` fini et l'estimation de `Xi_1` sont deux objets distincts. Une valeur de `Delta_1` à `delta=0.1`, par exemple, n'est pas interprétée comme une mesure de la dérivée si elle se trouve hors du régime linéaire local.

## 2. Principe général : une famille de pas, jamais un pas unique

Aucun pas unique `h_delta` n'est privilégié.

Pour chaque protocole où `Xi_1` est estimé, on préenregistre une famille ordonnée de pas positifs. Pour un pas physique `h` :

```math
\widehat\Xi_1(h)
=\frac{\Delta_1(+h)-\Delta_1(-h)}{2h}.
```

Grâce à l'oddness exacte :

```math
\widehat\Xi_1(h)=\frac{\Delta_1(+h)}{h}
```

si la covariance `+h/-h` est satisfaite exactement.

Cependant, le pipeline confirmatoire doit conserver un sous-ensemble de calculs explicites à `-h` afin d'exercer l'oracle end-to-end ; la forme réduite ne remplace pas ce test.

Le principe de contrôle est toujours : réduire une coordonnée préenregistrée du pas et vérifier la stabilité de l'estimateur. La manière de paramétrer cette coordonnée peut dépendre d'un régime physique préenregistré, à condition qu'elle soit déterministe et ne dépende pas des valeurs observées de `Delta_1`.

## 3. Famille absolue hors régime cyclique mou

Hors du protocole spécifique de mode cyclique mou, une famille absolue peut être utilisée :

```math
\mathcal H_\delta
=\{h_1>h_2>\cdots>h_K>0\}.
```

Ses valeurs numériques restent `OPEN` jusqu'au gel du protocole numérique.

Cette famille n'est pas transportée automatiquement dans un régime où l'échelle analytique de linéarité s'effondre avec le gap.

## 4. Famille adimensionnée dans la sous-campagne SOFT-LOOP

Dans le doublet cyclique à `mu<0`, le Hamiltonien effectif est :

```math
H_{eff}
=E_c I
+3g\delta\,\sigma_z
+t_{loop}\,\sigma_x
+\cdots.
```

À `delta=0`, le gap du doublet vaut au premier ordre effectif :

```math
gap_0=2|t_{loop}|.
```

Le rapport adimensionné naturel est donc :

```math
\alpha
=\frac{6g\,|\delta|}{gap_0}.
```

Le régime linéaire du doublet correspond à :

```math
\alpha\ll1.
```

On définit l'échelle locale :

```math
\delta_c(g,\mu)
=\frac{gap_{GS}^{(\Lambda_{ref})}(g,\mu,0)}{6g},
```

pour `g>0` et `gap_GS>0`, avec `Lambda_ref=2`.

La famille de contrôle SOFT-LOOP est alors une famille **sans dimension** préenregistrée :

```math
\mathcal A_\delta
=\{\alpha_1>\alpha_2>\cdots>\alpha_K>0\},
```

et les pas physiques sont dérivés par :

```math
h_k(g,\mu)
=\alpha_k\,\delta_c(g,\mu)
=\alpha_k\frac{gap_{GS}^{(2)}(g,\mu,0)}{6g}.
```

Les valeurs de `alpha_k` restent `OPEN` jusqu'au gel numérique.

Cette construction n'est pas un ajustement post-hoc :

- la formule est préenregistrée ;
- le gap utilisé est publié systématiquement ;
- aucune valeur de `Delta_1` n'entre dans le choix du pas ;
- la même famille `A_delta` est utilisée pour tous les `mu` de la sous-campagne.

Si `gap_GS=0` exactement, cette paramétrisation ne fournit aucun pas positif et la dérivée doit être traitée séparément ; elle peut devenir `DERIVATIVE_NOT_APPLICABLE` selon la régularité de l'état canonique.

## 5. Troncature : même point physique aux deux cutoffs

Pour un point soumis au contrôle `Lambda=2 -> 3`, les pas physiques doivent être générés **une seule fois** à partir du gap `Lambda=2` :

```math
h_k
=\alpha_k\frac{gap_{GS}^{(2)}(g,\mu,0)}{6g}.
```

Ces mêmes valeurs numériques de `h_k` sont ensuite utilisées pour :

```text
Lambda = 2
Lambda = 3
```

Il est interdit de recalculer :

```math
h_k^{(3)}
=\alpha_k\frac{gap_{GS}^{(3)}}{6g}
```

pour la comparaison principale, car les deux cutoffs seraient alors évalués à des Hamiltoniens physiques différents.

Le gap `Lambda=3` est publié comme contrôle de convergence et peut servir à construire a posteriori une coordonnée adimensionnée diagnostique, mais pas une seconde grille de `delta`.

## 6. Stabilité plutôt que seuil unique

La dérivée n'est acceptée comme estimée de manière stable que si les valeurs :

```math
\widehat\Xi_1(h_k)
```

présentent une stabilité sur la famille préenregistrée selon une règle numérique qui sera gelée avec les tolérances générales.

Les statuts conceptuels sont :

```text
DERIVATIVE_STABLE
DERIVATIVE_CONTROL_SENSITIVE
DERIVATIVE_NOT_APPLICABLE
```

`DERIVATIVE_CONTROL_SENSITIVE` signifie que l'estimation dépend matériellement de la famille de pas déclarée ; ce n'est pas un échec physique automatique.

Dans le régime SOFT-LOOP, une absence de plateau lorsque `alpha` diminue signifie que l'estimation de la dérivée n'est pas résolue de manière robuste. À l'inverse, l'échec de pas absolus trop grands dans un régime où `delta_c` est minuscule ne doit pas être interprété comme une propriété physique de `Xi_1`.

## 7. Gap spectral et conditionnement

À chaque point de campagne, publier :

```text
d_GS
gap_GS = E_1-E_0
```

Un petit gap n'implique pas à lui seul un croisement évité. Il peut provenir d'un mode physique mou identifiable, comme le doublet cyclique à `mu<0` décrit dans `negative-mu-soft-loop.md`.

Le terme :

```text
NEAR_CROSSING
```

ne doit donc pas être déclenché par un simple seuil sur `gap_GS`.

La grandeur `gap_GS` est publiée comme diagnostic spectral continu. Pour la sensibilité spécifique à `delta`, on peut également publier un indicateur continu de conditionnement fondé sur le générateur :

```math
\kappa_\delta
=\frac{\|\partial_\delta H\|}{gap_{GS}}
=\frac{g\,\|V_\delta\|}{gap_{GS}},
```

lorsque `gap_GS>0`.

Cet indicateur est continu et n'introduit aucun seuil physique.

Une dégénérescence exacte ou une non-régularité du projecteur peut conduire à :

```text
DERIVATIVE_NOT_APPLICABLE.
```

## 8. Une logique commune de contrôle

Les familles :

```text
eta                  -> seuils de premier lobe
epsilon_path         -> pureté / composition sectorielle
Gamma                -> récurrence hystérétique
H_delta / A_delta    -> dérivée en delta
```

sont toutes des variables de contrôle préenregistrées, pas des paramètres physiques ajustés après inspection.

Le principe commun est :

```text
- déclarer la famille avant la campagne ;
- publier la sensibilité du résultat à cette famille ;
- ne retenir une interprétation robuste que si elle est stable sur le domaine déclaré ;
- ne jamais déplacer a posteriori la famille pour restaurer un verdict souhaité.
```

La sous-campagne SOFT-LOOP ne crée donc pas une nouvelle philosophie de contrôle ; elle utilise la même logique avec une coordonnée de pas rendue adimensionnée par l'échelle spectrale analytique pertinente.

## 9. Covariance

Lorsque les deux signes `+h/-h` sont calculés explicitement, l'oddness :

```math
\Delta_1(-h)=-\Delta_1(+h)
```

est testée avant d'utiliser ces valeurs dans l'estimateur de dérivée.

Les mêmes coefficients `alpha_k` sont utilisés pour les deux signes.

## 10. Statut

```text
XI1_DELTA0_DEFINITION               = VALIDATED_FOR_FREEZE_IF_DIFFERENTIABLE
SINGLE_DERIVATIVE_STEP              = REJECTED
DERIVATIVE_STABILITY_REQUIRED       = VALIDATED_FOR_FREEZE
ABSOLUTE_STEP_FAMILY_H_DELTA         = VALIDATED_FOR_FREEZE_OUTSIDE_SOFT_LOOP
SOFT_LOOP_FIXED_ABSOLUTE_STEPS       = REJECTED
SOFT_LOOP_DIMENSIONLESS_ALPHA        = VALIDATED_FOR_FREEZE
SOFT_LOOP_DELTA_C                    = gap_GS^(Lambda2)/(6g)
SOFT_LOOP_ALPHA_VALUES               = OPEN
SAME_PHYSICAL_H_ACROSS_CUTOFFS       = MANDATORY
GAP_GS_PUBLICATION                   = MANDATORY
NEAR_CROSSING_FROM_GAP_ONLY         = REJECTED
KAPPA_DELTA_DIAGNOSTIC              = VALIDATED_IN_PRINCIPLE
SMALL_GAP_PHYSICAL_THRESHOLD        = NOT_REQUIRED
H_DELTA_VALUES                      = OPEN
DERIVATIVE_NUMERICAL_TOLERANCE      = OPEN
CONTROL_FAMILY_COMMON_PRINCIPLE     = VALIDATED_FOR_FREEZE
```
