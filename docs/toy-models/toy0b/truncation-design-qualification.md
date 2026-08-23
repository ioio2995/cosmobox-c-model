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
GS_ENERGY_CUTOFF_DIFFERENCE_AS_SUFFICIENT_CERTIFICATE = REJECTED
GAP_DESIGN_VALUES_DISCLOSED        = YES
BOUNDARY_WEIGHT_AS_ERROR_ESTIMATE  = REJECTED
G_MIN_FROM_B2_ALONE                = NOT_ESTABLISHED
RITZ_RESIDUAL_TRUNCATION_DIAGNOSTIC= VALIDATED_IN_PRINCIPLE
CONFIRMATORY_OBSERVABLE_CHECK      = MANDATORY
PARAMETER_BOUNDS                   = OPEN
TRUNCATION_STRESS_POINT_SUBSET     = VALIDATED_FOR_FREEZE
```

## 8. Sélection préenregistrée du sous-ensemble de stress de troncature

Cette section fige la sélection exacte des points de stress `Lambda=2 -> 3`, préenregistrée avant toute évaluation confirmatoire `Lambda=3`. Elle ferme UNIQUEMENT le périmètre « où le contrôle complet est obligatoire », pas les tolérances de comparaison :

```text
TRUNCATION_STRESS_POINT_SUBSET = VALIDATED_FOR_FREEZE
TRUNCATION_COMPARISON_TOLERANCES = OPEN
TRUNCATION_STRESS_NEW_SCALAR_TOLERANCE = NONE
```

Portée : points MAIN à `delta` non négatif sélectionnés plus deux points de stress/qualification extérieurs déjà divulgués (`TRUNCATION_STRESS_POINT_SUBSET_SCOPE = MAIN_PLUS_DISCLOSED_OUTER_STRESS`). Cette sélection n'absorbe pas SOFT-LOOP : la porte statique `Lambda=2`/`3` déjà gelée de SOFT-LOOP reste inchangée et hors de cette sélection (`SOFT_LOOP_EXISTING_CUTOFF_OBLIGATIONS = UNCHANGED_AND_OUTSIDE_TRUNCATION_STRESS_SUBSET_SELECTION`) ; ce lot n'impose aucune nouvelle campagne dynamique `Xi1` au cutoff (`SOFT_LOOP_DYNAMIC_XI1_CUTOFF_REQUIREMENT_BY_THIS_LOT = NOT_IMPOSED`). Si `Xi1` est comparé séparément aux deux cutoffs, `SAME_PHYSICAL_H_ACROSS_CUTOFFS = MANDATORY` (déjà défini dans `derivative-control.md`) s'applique.

### 8.1 Ancre de référence obligatoire

```text
theta_ref = (1,0,0)

TRUNCATION_REFERENCE_ANCHOR = (1,0,0)
TRUNCATION_REFERENCE_ANCHOR_ROLE = MANDATORY_REFERENCE_NOT_STRESS
```

Chaque fois qu'un observable `C_eff`/`Delta`-dérivé sélectionné est évalué à `Lambda=3`, l'objet/temps de référence `Lambda=3` correspondant doit être disponible. Ce point n'est PAS compté dans la taille du sous-ensemble de stress.

### 8.2 Sous-ensemble fixe à 18 points

Représentants physiques à `delta` non négatif uniquement.

**A. Spine `delta` à `g` faible** (`g=1/4`, `mu=0`) :

```text
S_delta_lowg = {(1/4,0,0),(1/4,0,1/10),(1/4,0,1/5),(1/4,0,2/5),(1/4,0,3/5),(1/4,0,4/5)}
```

Compte = 6. Rôle : axe `delta` déclaré complet au plus petit `g` MAIN nominal, sans hypothèse de monotonie en `delta`.

**B. Spine `g` à `mu` négatif, `delta` maximal nominal** (`mu=-1`, `delta=4/5`) :

```text
S_g_negmu = {(1/4,-1,4/5),(1/2,-1,4/5),(1,-1,4/5),(2,-1,4/5)}
```

Compte = 4. Rôle : axe `g` complet sous stress combiné `mu` négatif / brisure finie nominale maximale.

**C. Spine `mu` complète à `g` faible / `delta` maximal nominal** (`g=1/4`, `delta=4/5`) :

```text
S_mu_lowg = {(1/4,-1,4/5),(1/4,-3/4,4/5),(1/4,-1/2,4/5),(1/4,0,4/5),(1/4,+1/2,4/5),(1/4,+1,4/5)}
```

Compte = 6, avec deux recouvrements déjà présents (`(1/4,-1,4/5)` dans B, `(1/4,0,4/5)` dans A) ; contribution unique nouvelle = 4. Rôle : exercer l'axe `mu` déclaré complet, sans hypothèse de covariance de signe ou de monotonie en `mu`.

**D. Ancre intérieure de calibration** :

```text
S_interior = {(1,0,2/5)}
```

Compte = 1. Rôle : point de calibration intérieur bien conditionné à `delta` fini ; garantit aussi une intersection non vide avec la base fixe de l'oracle négatif en `delta`.

**E. Points de stress extérieurs déjà divulgués** :

```text
S_outer = {(1/10,0,0),(1,0,9/10)}
```

Compte = 2. Rôle : `STRESS_DIAGNOSTIC_OUTSIDE_MAIN`. Ces points n'agrandissent pas MAIN.

**F. Ancre de stress de conditionnement** :

```text
S_conditioning = {(1,-1,0)}
```

Compte = 1. Rôle : `CONDITIONING_STRESS_ANCHOR_FROM_DISCLOSED_DESIGN_QUALIFICATION`. Le tableau de qualification divulgué (§2) rapporte un petit gap en ce point (`gap_GS ~= 0.214`), échantillonnant ainsi la direction de conditionnement indépendamment des spines de stress à `delta` élevé. Ceci n'établit ni loi globale de monotonie du gap, ni théorème d'erreur de troncature, ni seuil de petit gap. Aucune extension adaptative classée par gap n'est introduite.

### 8.3 Ensemble et comptage

```text
S_truncation_stress = S_delta_lowg union S_g_negmu union S_mu_lowg union S_interior union S_outer union S_conditioning

6 + 4 + 4 + 1 + 2 + 1 = 18

TRUNCATION_STRESS_MAIN_POINT_COUNT = 16
TRUNCATION_STRESS_OUTER_POINT_COUNT = 2
TRUNCATION_STRESS_POINT_SUBSET_SIZE = 18

TRUNCATION_STRESS_POINT_DESIGN = THREE_AXIS_STRESS_CROSS_PLUS_CONDITIONING_INTERIOR_AND_OUTER_ANCHORS
```

Ne pas confondre avec `NEGATIVE_DELTA_ORACLE_BASE_SIZE = 17` : ce sont des objets distincts.

### 8.4 Pourquoi `g=0` est exclu

Ne pas décrire `g=0` comme nécessairement peu stressant. La tendance divulguée en §3 augmente au contraire quand `g` diminue. La raison correcte de l'exclusion :

- `g=0` est hors MAIN ;
- `delta` y est structurellement inactif ;
- l'oracle `d=2` de pur hopping pertinent est une annulation structurelle valide aussi dans le modèle tronqué ;
- il relève donc de son propre oracle structurel séparé, pas de ce sous-ensemble de stress fini.

```text
TRUNCATION_GZERO_ROLE = SEPARATE_STRUCTURAL_ORACLE_NOT_STRESS_SUBSET
```

### 8.5 Séparation `delta` négatif

À chaque `Lambda` : `R H_Lambda(g,mu,delta) R^dagger = H_Lambda(g,mu,-delta)`, car la troncature de flux symétrique est invariante sous `R`. `delta` négatif n'apporte donc aucune évidence de troncature physique indépendante :

```text
TRUNCATION_NEGATIVE_DELTA_ROLE = IMPLEMENTATION_ORACLE_ONLY
```

Le sous-ensemble physique de stress porte uniquement sur `delta` non négatif. Les miroirs `Lambda=3` en `delta` négatif sont fournis par la règle déjà fermée `NEGATIVE_DELTA_ORACLE_SUBSET`. L'intersection entre le sous-ensemble fixe de stress et la base fixe de l'oracle négatif est structurellement non vide ; en particulier `(1,0,2/5)` appartient aux deux :

```text
NEGATIVE_DELTA_ORACLE_LAMBDA3_FALLBACK_STATUS_FOR_CURRENT_TRUNCATION_SUBSET = NOT_TRIGGERED_STRUCTURALLY
```

La règle générique de repli de l'oracle négatif (`parameter-campaign-structure.md` §11.9) n'est pas supprimée ; elle reste une garde de sécurité valide pour le protocole général.

### 8.6 Portée scientifique par point

À chaque point de stress sélectionné, comparer la même fermeture de dépendance scientifique complète applicable à `Lambda=2` et `Lambda=3` (état canonique/`d_GS`, `E_GS`/`gap_GS`, objets spectraux requis, `T_peak`, `T_grow`, `T_thr(eta)` admissibles, `T_down(eta)` requis, `C_eff` d'orbite, `Delta_1` de croissance et de seuil, diagnostics d'oracle à temps court, profils/statuts de pureté de chemin, profils/statuts de récurrence, quantités MAIN dérivées dépendant de ce point) :

```text
TRUNCATION_STRESS_OBSERVABLE_SCOPE = FULL_REQUIRED_SCIENTIFIC_DEPENDENCY_CLOSURE
```

Pour toute comparaison de famille de seuils, utiliser la fermeture de dépendance `eta` commune admissible déjà gelée aux deux cutoffs, sans rétrécissement différencié :

```text
TRUNCATION_THRESHOLD_DOMAIN_RULE = EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE
```

### 8.7 Aucune extension adaptative

Le sous-ensemble à 18 points est fixé avant toute évaluation confirmatoire `Lambda=3`. Interdit :

- ajouter un point parce que `B2` est inhabituellement grand ;
- ajouter un point parce qu'un gap confirmatoire est inhabituellement petit ;
- retirer un point parce que `Lambda=3` diverge ;
- remplacer un point parce qu'un événement est non résolu ;
- sélectionner des points supplémentaires depuis des résultats `Lambda=3` observés ;
- utiliser des résultats de l'oracle négatif pour modifier ce sous-ensemble.

```text
TRUNCATION_STRESS_POSTHOC_SUBSTITUTION = FORBIDDEN
TRUNCATION_STRESS_ADAPTIVE_EXTENSION = REJECTED_FOR_PRIMARY_PREREGISTERED_SUBSET
```

### 8.8 Portée de la revendication

Un sous-ensemble fixe et clairsemé ne peut pas établir une convergence uniforme de cutoff sur tous les points MAIN non échantillonnés :

```text
TRUNCATION_STRESS_CLAIM_SCOPE = PREREGISTERED_STRESS_SUPPORT_NOT_UNIFORM_THEOREM
```

Une fois les tolérances futures fermées, une comparaison réussie sur ce sous-ensemble ne pourra supporter que :

```text
NO_CUTOFF_INSTABILITY_DETECTED_ON_PREREGISTERED_STRESS_SUBSET
```

et ne doit jamais être réécrite en `UNIFORM_CUTOFF_CONVERGENCE_PROVEN_ON_FULL_MAIN_DOMAIN`. Pour tout point MAIN non inclus dans `S_truncation_stress` :

```text
TRUNCATION_CUTOFF_STATUS_FOR_UNSAMPLED_MAIN_POINT = NOT_CERTIFIED_BY_STRESS_SUBSET
```

Ceci n'est pas un `FAIL` ; c'est une absence explicite de certification ponctuelle de cutoff par ce protocole clairsemé.
