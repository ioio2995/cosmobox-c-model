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

## 2. Famille de pas

Aucun pas unique `h_delta` n'est privilégié.

On préenregistre une famille ordonnée de pas positifs :

```math
\mathcal H_\delta=\{h_1>h_2>\cdots>h_K>0\}.
```

Les valeurs numériques restent `OPEN` jusqu'au gel du protocole numérique.

Pour chaque `h` :

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

## 3. Stabilité plutôt que seuil unique

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

`DERIVATIVE_CONTROL_SENSITIVE` signifie que l'estimation dépend matériellement du pas dans la famille déclarée ; ce n'est pas un échec physique automatique.

`DERIVATIVE_NOT_APPLICABLE` s'applique notamment si le fond canonique n'est pas différentiable par rapport à `delta` au point considéré ou si une dégénérescence exacte empêche de définir la dérivée retenue.

## 4. Croisements évités

À chaque point de campagne, publier :

```text
d_GS
gap_GS = E_1-E_0
```

Un statut :

```text
NEAR_CROSSING
```

peut être déclenché par un seuil de gap préenregistré. Ce seuil reste `OPEN` jusqu'au gel numérique.

`NEAR_CROSSING` est un diagnostic de conditionnement. Il n'annule pas un résultat physique et n'impose pas à lui seul `DERIVATIVE_NOT_APPLICABLE`.

En revanche, toute dérivée évaluée dans un régime `NEAR_CROSSING` doit impérativement satisfaire le contrôle par la famille `H_delta`. En l'absence de plateau/stabilité :

```text
DERIVATIVE_CONTROL_SENSITIVE
```

et non une valeur de dérivée présentée comme robuste.

## 5. Une logique commune de contrôle

Les familles :

```text
eta                  -> seuils de premier lobe
epsilon_path         -> pureté / composition sectorielle
Gamma                -> récurrence hystérétique
H_delta              -> dérivée en delta
```

sont toutes des variables de contrôle préenregistrées, pas des paramètres physiques ajustés après inspection.

Le principe commun est :

```text
- déclarer la famille avant la campagne ;
- publier la sensibilité du résultat à cette famille ;
- ne retenir une interprétation robuste que si elle est stable sur le domaine déclaré ;
- ne jamais déplacer a posteriori la famille pour restaurer un verdict souhaité.
```

Cette unification est méthodologique ; les critères précis de stabilité restent adaptés à la nature de chaque famille.

## 6. Troncature et covariance

La même famille `H_delta` doit être utilisée :

```text
Lambda = 2
Lambda = 3
```

pour tout point soumis au contrôle de troncature.

Un écart de stabilité entre les deux cutoffs ne peut pas être absorbé en choisissant des pas différents.

De même, lorsque les deux signes `+h/-h` sont calculés explicitement, l'oddness :

```math
\Delta_1(-h)=-\Delta_1(+h)
```

est testée avant d'utiliser ces valeurs dans l'estimateur de dérivée.

## 7. Statut

```text
XI1_DELTA0_DEFINITION             = VALIDATED_FOR_FREEZE_IF_DIFFERENTIABLE
DERIVATIVE_STEP_FAMILY            = VALIDATED_FOR_FREEZE
SINGLE_DERIVATIVE_STEP            = REJECTED
DERIVATIVE_STABILITY_REQUIRED     = VALIDATED_FOR_FREEZE
NEAR_CROSSING_DIAGNOSTIC          = VALIDATED_FOR_FREEZE
NEAR_CROSSING_GAP_THRESHOLD       = OPEN
H_DELTA_VALUES                    = OPEN
DERIVATIVE_NUMERICAL_TOLERANCE    = OPEN
SAME_H_DELTA_ACROSS_CUTOFFS       = MANDATORY
CONTROL_FAMILY_COMMON_PRINCIPLE   = VALIDATED_FOR_FREEZE
```
