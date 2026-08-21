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

## 4. Gap spectral et conditionnement

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

Cet indicateur exprime le fait que les bornes de perturbation du projecteur fondamental se dégradent lorsque le générateur devient grand par rapport au gap. Il est un diagnostic continu, pas un seuil physique.

Aucun seuil `SMALL_GAP` n'est requis pour le verdict scientifique. Si un drapeau opérationnel est ultérieurement nécessaire pour des raisons numériques, son seuil devra être justifié comme critère de conditionnement numérique et non comme frontière physique.

Le verdict sur la dérivée reste donné par la famille `H_delta` : si l'estimation ne se stabilise pas sous réduction préenregistrée du pas,

```text
DERIVATIVE_CONTROL_SENSITIVE
```

est rapporté, quelle que soit l'origine physique du petit gap.

Une dégénérescence exacte ou une non-régularité du projecteur peut conduire à :

```text
DERIVATIVE_NOT_APPLICABLE.
```

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
GAP_GS_PUBLICATION                = MANDATORY
NEAR_CROSSING_FROM_GAP_ONLY       = REJECTED
KAPPA_DELTA_DIAGNOSTIC            = VALIDATED_IN_PRINCIPLE
SMALL_GAP_PHYSICAL_THRESHOLD      = NOT_REQUIRED
H_DELTA_VALUES                    = OPEN
DERIVATIVE_NUMERICAL_TOLERANCE    = OPEN
SAME_H_DELTA_ACROSS_CUTOFFS       = MANDATORY
CONTROL_FAMILY_COMMON_PRINCIPLE   = VALIDATED_FOR_FREEZE
```
