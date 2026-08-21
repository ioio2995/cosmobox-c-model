# Toy Model 0B — qualification de design de la troncature

Statut : **qualification préalable non confirmatoire**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `parameter-campaign-structure.md`, `validation-plan.md`

Ce document consigne des diagnostics de saturation du flux obtenus avant le gel numérique de la campagne. Ils peuvent informer le choix des bornes et des points de stress, mais ne constituent ni des résultats confirmatoires ni un critère suffisant de validité de la troncature.

## 1. Diagnostic de bord

À `Lambda=2`, on définit le projecteur de bord sur les états physiques tels que :

```math
\max_i |E_i|=2,
```

et :

```math
B_2(\theta)=Tr(\rho_\theta\,\Pi_{\partial,2}).
```

`B_2` mesure la population du bord du cutoff dans l'état canonique. Il est un indicateur de stress de troncature, pas une erreur de troncature.

## 2. Qualification préalable divulguée

Les valeurs suivantes ont été obtenues avant le gel de la campagne et sont donc classées comme information de design non confirmatoire :

| g | mu | delta | B2 = P(max|E|=2) | E_GS(L2)-E_GS(L3) | gap_GS |
|---:|---:|---:|---:|---:|---:|
| 1.00 | 0 | 0.0 | 1.7e-6 | 4e-14 | 1.562 |
| 1.00 | 0 | 0.6 | 1.4e-5 | -1e-14 | 1.415 |
| 1.00 | 0 | 0.9 | 3.9e-5 | 5e-14 | 1.398 |
| 0.50 | 0 | 0.0 | 5.8e-5 | 1e-12 | 0.995 |
| 0.25 | 0 | 0.0 | 7.6e-4 | 1.5e-9 | 0.645 |
| 0.10 | 0 | 0.0 | 7.7e-3 | 1.2e-6 | 0.377 |
| 2.00 | 0 | 0.0 | 1.4e-8 | 4e-14 | 2.532 |
| 1.00 | +1 | 0.0 | 2.6e-8 | 2e-14 | 3.397 |
| 1.00 | -1 | 0.0 | 4.3e-5 | -4e-14 | 0.214 |
| 0.25 | 0 | 0.6 | 1.6e-3 | 1.0e-8 | 0.686 |

## 3. Ce que ces données autorisent à conclure

Elles montrent localement :

```text
- à mu=delta=0, le stress de bord augmente fortement quand g diminue ;
- à g=1, mu=0, l'augmentation de |delta| jusqu'à 0.9 reste faible en comparaison ;
- à g=1, delta=0, le signe de mu produit une forte asymétrie, mu<0 diminuant fortement le gap ;
- le point g=0.25, delta=0.6 est plus stressé que g=0.25, delta=0, cohérent avec le rôle de g_weak=g(1-|delta|).
```

Ces observations sont des informations de design locales. Elles ne doivent pas être extrapolées en lois globales sans campagne préenregistrée.

En particulier :

```text
DELTA_TRUNCATION_EFFECT_GLOBALLY_SMALL = NOT_ESTABLISHED
G_DOMINATES_TRUNCATION_GLOBALLY        = NOT_ESTABLISHED
MU_NEGATIVE_ALWAYS_WORSE               = NOT_ESTABLISHED
```

## 4. Ce que ces données ne permettent pas de conclure

Un poids de bord non nul ne mesure pas directement l'erreur sur les observables ni sur la dynamique. De même, un très petit écart d'énergie fondamentale entre `Lambda=2` et `Lambda=3` ne garantit pas à lui seul la convergence des réponses temporelles.

Il est donc interdit de définir une frontière exacte du type :

```text
g < 0.25 -> Lambda=2 invalide
```

sur la seule base de `B2` ou de l'énergie fondamentale.

Le point `g=0.25` peut être qualifié de région de stress accru ; le point `g=0.10` de stress plus fort encore. La décision de les inclure dans le domaine principal, dans un sous-ensemble de stress, ou de les exclure reste un choix de campagne à préenregistrer.

## 5. Résidu de Ritz comme diagnostic plus direct

Comme l'espace physique `Lambda=2` s'immerge naturellement dans celui de `Lambda=3`, on peut noter :

```math
\iota:\mathcal H_{phys}^{(2)}\hookrightarrow\mathcal H_{phys}^{(3)}.
```

Pour le fondamental `|Omega_2>` de `H_2`, on définit le résidu dans le modèle agrandi :

```math
r_2(\theta)
=\left\|(H_3-E_0^{(2)})\,\iota|\Omega_2\rangle\right\|.
```

Puisque la restriction de `H_3` à l'espace `Lambda=2` reproduit `H_2`, ce résidu provient uniquement du couplage vers les états omis par la troncature `Lambda=2`.

Il est donc un diagnostic a posteriori plus direct de la pression exercée contre le cutoff que la seule population de bord.

Pour un vecteur normalisé, la théorie standard des résidus de Ritz garantit qu'il existe une valeur propre de `H_3` à distance au plus `r_2` de la quotient de Rayleigh. Si la valeur propre cible est isolée des autres par une séparation spectrale connue, le rapport `r_2 / separation` fournit en outre un contrôle sur l'angle entre le vecteur de Ritz et le sous-espace propre correspondant.

Ce diagnostic reste un outil de qualification de troncature ; il ne remplace pas le contrôle final `Lambda=2 -> 3` sur les observables scientifiques elles-mêmes.

## 6. Conséquence méthodologique pour les bornes

Les données actuelles peuvent être utilisées pour choisir des points de stress préenregistrés, mais pas pour créer rétrospectivement un seuil de saturation.

La hiérarchie recommandée est :

```text
1. utiliser B2 et le gap comme diagnostics continus de design ;
2. si disponible, compléter par le résidu de Ritz r2 ;
3. fixer ensuite le domaine principal et les points de stress ;
4. dans la campagne confirmatoire, contrôler directement les observables à Lambda=2 et Lambda=3 sur les points préenregistrés.
```

## 7. Statut

```text
BOUNDARY_WEIGHT_B2                 = DESIGN_DIAGNOSTIC
GS_ENERGY_CUTOFF_DIFFERENCE        = DESIGN_DIAGNOSTIC
GAP_DESIGN_VALUES_DISCLOSED        = YES
BOUNDARY_WEIGHT_AS_ERROR_ESTIMATE  = REJECTED
G_MIN_FROM_B2_ALONE                = NOT_ESTABLISHED
RITZ_RESIDUAL_TRUNCATION_DIAGNOSTIC= VALIDATED_IN_PRINCIPLE
CONFIRMATORY_OBSERVABLE_CHECK      = MANDATORY
PARAMETER_BOUNDS                   = OPEN
```
