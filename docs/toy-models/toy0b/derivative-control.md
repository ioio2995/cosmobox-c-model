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

Les valeurs préenregistrées pour SOFT-LOOP sont :

```math
\boxed{
\mathcal A_\delta
=
\left\{
\frac12,\frac14,\frac18,\frac1{16}
\right\}.
}
```

Avec l'indexation utilisée pour le contrôle :

```text
alpha_0 = 1/2
alpha_1 = 1/4
alpha_2 = 1/8
alpha_3 = 1/16
```

Les pas physiques restent :

```math
h_k(g,\mu)=\alpha_k\frac{gap_{GS}^{(2)}(g,\mu,0)}{6g}.
```

La famille est dyadique dans la coordonnée naturelle du doublet mou.

`alpha_0=1/2` est conservé comme point grossier de diagnostic. L'estimateur primaire de dérivée publié est construit au pas le plus fin `alpha_3=1/16`.

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

Pour :

```math
X_k = \widehat\Xi_1(\alpha_k),
```

le budget numérique associé est :

```math
e_k = E_\Xi^{num}(\alpha_k),
```

défini dans `derivative-error-budget.md`.

L'estimateur primaire publié est :

```math
X_3 = \widehat\Xi_1(1/16).
```

`X_0` est `DIAGNOSTIC_ONLY` pour le critère final de convergence.

Pour `k=1,2`, définir :

```math
D_k = X_k - X_{k+1}, \quad
e_{D_k} = e_k + e_{k+1}, \quad
m_k = |D_k| - e_{D_k}, \quad
M_k = |D_k| + e_{D_k}.
```

Une différence est résolue numériquement si :

```math
m_k > 0.
```

Lorsque `m_1>0` et `m_2>0`, définir :

```math
Q_{\min} = \frac{m_1}{M_2}, \quad
Q_{\max} = \frac{M_1}{m_2}.
```

La voie de convergence compatible avec le régime quadratique exige simultanément :

```text
m_1 > 0
m_2 > 0
les intervalles signés de D_1 et D_2 ont le même signe
[Q_min, Q_max] ⊂ [2,8]
```

Alors seulement :

```text
DERIVATIVE_STABLE_QUADRATIC
```

La bande `[2,8]` est une bande opérationnelle compatible avec le régime quadratique attendu autour de la limite asymptotique `Q=4`. Elle ne signifie pas que tout `Q` de cette bande constitue une convergence quadratique exacte.

`Q_min` et `Q_max` doivent être publiés.

Si :

```math
|D_2| \le e_{D_2},
```

alors :

```text
DERIVATIVE_NUMERICAL_FLOOR
```

Ce statut signifie uniquement que la variation entre les deux plus petits pas n'est pas résolue au-dessus du budget numérique courant. Il ne constitue pas une preuve de convergence et n'autorise pas Richardson.

Dans tous les autres cas :

```text
DERIVATIVE_CONTROL_SENSITIVE
```

Lorsque la dérivée elle-même n'est pas applicable :

```text
DERIVATIVE_NOT_APPLICABLE
```

Toute valeur primaire `X_3` publiée doit être accompagnée de l'un de ces statuts.

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
SOFT_LOOP_ALPHA_VALUES               = {1/2, 1/4, 1/8, 1/16}
A_DELTA_VALUES                       = VALIDATED_FOR_FREEZE
SAME_PHYSICAL_H_ACROSS_CUTOFFS       = MANDATORY
GAP_GS_PUBLICATION                   = MANDATORY
NEAR_CROSSING_FROM_GAP_ONLY         = REJECTED
KAPPA_DELTA_DIAGNOSTIC              = VALIDATED_IN_PRINCIPLE
SMALL_GAP_PHYSICAL_THRESHOLD        = NOT_REQUIRED
H_DELTA_VALUES                      = OPEN
DERIVATIVE_STABILITY_CRITERION      = VALIDATED_FOR_FREEZE
CONTROL_FAMILY_COMMON_PRINCIPLE     = VALIDATED_FOR_FREEZE
```
