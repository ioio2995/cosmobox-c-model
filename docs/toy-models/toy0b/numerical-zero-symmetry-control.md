# Toy Model 0B — contrôle numérique des zéros, symétries et rangs

Statut : **validé pour gel — support méthodologique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document est la source normative détaillée du DERNIER contrôle numérique majeur préenregistré de Toy Model 0B : `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES`. Il ferme UNIQUEMENT ce paramètre.

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE
```

Ce document n'autorise ni l'implémentation 0B, ni le gel du modèle. `IMPLEMENTATION_0B` reste `NOT_AUTHORIZED` tant que `docs/governance/current-task.md` ne l'autorise pas explicitement.

`GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION` est hors du périmètre de ce contrôle et reste `OPEN` (§AD).

---

## A. Statut scientifique final

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE

ZERO_SYMMETRY_TOLERANCE_VALUES = {1e-9,3e-9,1e-8}

ZERO_SYMMETRY_STRICT     = 1e-9
ZERO_SYMMETRY_MID        = 3e-9
ZERO_SYMMETRY_PERMISSIVE = 1e-8

ZERO_SYMMETRY_GRID_TYPE = ONE_DECADE_NORMALIZED_NUMERICAL_RESOLUTION_FAMILY

ZERO_SYMMETRY_POSTHOC_TOLERANCE_SELECTION = FORBIDDEN

NUMERICALLY_ZERO_COMPATIBLE_IS_EXACT_ZERO = NO

GENERIC_ZERO_TOLERANCE_CREATES_GROUND_STATE_DEGENERACY = NO
```

Aucune famille de tolérance plus stricte spécifique à une classe d'objets n'est introduite.

---

## B. Séparation épistémique

Deux rôles numériques distincts sont utilisés dans tout le protocole 0B.

### B.1 Oracle analytique exact

Une identité exacte est déjà un théorème (par exemple `Delta2=0`, `Delta1(delta=0)=0`, `M1^{pq}=0` pour `d(p,q)>=2`, la covariance de réflexion `R H(+delta) R^dagger = H(-delta)`).

Le contrôle numérique teste uniquement la cohérence du pipeline avec ce théorème.

```text
ROBUST_ORACLE_FAIL = INCOHERENCE_NUMERIQUE_OU_DE_PIPELINE_AVEC_LE_THEOREME
```

Un `ROBUST_ORACLE_FAIL` ne falsifie jamais le théorème analytique lui-même ; il signale un défaut de pipeline/implémentation.

### B.2 Zéro/non-zéro opérationnel

Pour une quantité sans théorème de zéro exact, `NUMERICALLY_ZERO_COMPATIBLE` est une classification de précision finie uniquement. Elle ne devient JAMAIS :

```text
EXACT_ZERO
STRUCTURAL_ZERO
CERTIFIED_ZERO
```

Normatif :

```text
ZERO_SYMMETRY_EXACT_ORACLE_ROLE = IMPLEMENTATION_AND_NUMERICAL_CONSISTENCY_TEST_OF_ANALYTIC_IDENTITY
```

---

## C. Bornes génériques de résidu

Pour un résidu scalaire `R` attendu nul :

```math
R^{(p)},\qquad R^{(2p)},
\qquad
e_{R,p2p}=|R^{(2p)}-R^{(p)}|.
```

Si un budget propagé existant existe :

```math
e_R=\max(e_{R,p2p},e_{R,prop}).
```

Pour une combinaison de termes évalués indépendamment, `e_{R,prop}` doit inclure la somme de leurs budgets existants.

Après normalisation déterministe par une échelle `S_R` :

```math
L_R=\max(0,|R^{(2p)}|-e_R)/S_R,
\qquad
U_R=(|R^{(2p)}|+e_R)/S_R.
```

Les portes de précision sous-jacentes doivent passer. Sinon : `NUMERICALLY_INCONCLUSIVE`.

---

## D. Routage de l'oracle exact

Pour `R=0` exact :

```text
U_R <= 1e-9  -> ROBUST_ORACLE_PASS
L_R > 1e-8   -> ROBUST_ORACLE_FAIL
sinon        -> ORACLE_CONTROL_SENSITIVE
```

`3e-9` sert exclusivement à la publication de sensibilité obligatoire.

L'usage confirmatoire d'un oracle requiert `ROBUST_ORACLE_PASS`.

---

## E. Routage zéro/non-zéro opérationnel

Pour un scalaire non structurel `x` :

```math
L_x=\max(0,|x^{(2p)}|-e_x)/S_x,
\qquad
U_x=(|x^{(2p)}|+e_x)/S_x.
```

```text
L_x > 1e-8  -> ROBUST_NONZERO
U_x <= 1e-9 -> NUMERICALLY_ZERO_COMPATIBLE
sinon       -> ZERO_CONTROL_SENSITIVE
```

Un échec de la porte de précision donne `NUMERICALLY_INCONCLUSIVE`.

---

## F. Registre déterministe des formes de résidu

Normatif :

```text
ZERO_SYMMETRY_RESIDUAL_FORM_REGISTRY = REQUIRED_AND_DETERMINISTIC_BEFORE_EXECUTION
```

Aucune forme de résidu n'est laissée au choix de l'exécutant.

### F1. Égalité stricte positive

Pour `x,y` strictement positifs attendus égaux :

```math
R=\log(x/y),\qquad S=1.
```

Usage : `T_peak`, `T_grow`, `T_thr(eta)`, `T_down(eta)`, écarts positifs sous égalité/parité, égalité `C_eff` positive, fréquences appariées positives, et autres égalités multiplicatives strictement positives.

Normatif :

```text
ZERO_SYMMETRY_POSITIVE_EQUALITY_RESIDUAL = ABS_LOG_RATIO_COORDINATE
```

### F2. Rééchelonnement positif

Pour `T_s=T_ref/s` :

```math
R=\log(s\,T_s/T_{ref}).
```

Pour `C_eff=s` :

```math
R=\log(C_{eff}/s).
```

`S=1` dans les deux cas.

### F3. Grandeurs signées sans dimension

Pour `Delta1`, `Delta2` et grandeurs signées sans dimension équivalentes :

```text
zéro       : R = x
égalité    : R = x - y
imparité   : R = x_minus + x_plus
```

`S=1`.

### F4. Égalité d'énergie signée / zéro de gap

```math
\bar E=\operatorname{Tr}(H)/d,
\qquad
S_E=\max(J,\|H-\bar E I\|_2),
```

où `||.||_2` est la NORME SPECTRALE D'OPÉRATEUR.

Égalité d'énergie signée : `R=E_1-E_2`, `S=\max(S_{E1},S_{E2})`.

Égalité de gap positif : utiliser F1 (ratio log).

Zéro/non-zéro de gap unique : utiliser le gap additif normalisé par `S_E`.

### F5. Covariance hamiltonienne

```math
D_H=\left\|R\,H(+\delta)\,R^\dagger-H(-\delta)\right\|_2
```

avec la NORME SPECTRALE D'OPÉRATEUR.

```math
S_H=\max\bigl(J,\|H(+\delta)\|_2,\|H(-\delta)\|_2\bigr).
```

Normatif :

```text
ZERO_SYMMETRY_OPERATOR_NORM = OPERATOR_SPECTRAL_NORM
HAMILTONIAN_REFLECTION_COVARIANCE_RESIDUAL = SPECTRAL_OPERATOR_NORM_OVER_S_H
```

### F6. États / projecteurs

Matrice densité : distance de trace directement.

Projecteurs de même rang attendu : `||P1 - P2_mapped||_2` avec norme spectrale d'opérateur, `S=1`.

La compatibilité de rang/catégorie est testée d'abord.

### F7. Grandeurs bornées à échelle unité

Pour `P_0`, `R_path`, pureté normalisée, `C_j` de récurrence bornée, lorsqu'un diagnostic mappé continu est requis :

```text
R = x - y, S = 1.
```

Les statuts catégoriels restent comparés séparément.

### F8. Variance locale

```math
V_j=\operatorname{Var}(n_j),\qquad S_V=1/4.
```

### F9. Espérance de hopping

Pour `<X_i>` :

```math
S_X=\|X_i\|_2.
```

Aucun plancher arbitraire `max(1,...)`.

### F10. Phi

```text
S_Phi = Lambda
S_2Phi = 2*Lambda
```

Aucun plancher arbitraire car `Lambda>=1`.

### F11. Coefficient de court temps / moment

Pour un coefficient `a_r` :

```math
S_{a,r}=\frac1{r!}\sum_{\omega>0}|\text{contribution spectrale signée}|\,\omega^r.
```

Aucun plancher arbitraire. Normatif :

```text
SHORT_TIME_ZERO_SCALE_FLOOR = NONE
SHORT_TIME_ZERO_SCALE       = RAW_ABSOLUTE_SPECTRAL_CONTRIBUTION_MAJORANT
```

Si l'échelle est structurellement nulle : branche zéro structurel. Si l'échelle est numériquement non résolue sans théorème : `NUMERICALLY_INCONCLUSIVE`.

### F12. Amplitudes de ligne de base de chemin

À l'exposant dominant certifié `nu_*` :

```math
A_D=\sqrt{\sum_{\alpha\in DIRECT,\,\nu_\alpha=\nu_*}c_\alpha^2},
\qquad
A_N=\sqrt{\sum_{\alpha\in NON\_DIRECT,\,\nu_\alpha=\nu_*}c_\alpha^2},
\qquad
A_S=\sqrt{A_D^2+A_N^2}.
```

Pour chaque `c_alpha`, utiliser son majorant spectral absolu brut `B_alpha`.

Échelles :

```math
S_{AD}=\sqrt{\sum_{DIRECT}B_\alpha^2},
\qquad
S_{AN}=\sqrt{\sum_{NON\_DIRECT}B_\alpha^2},
\qquad
S_{AS}=\sqrt{S_{AD}^2+S_{AN}^2}.
```

Normatif :

```text
PATH_BASELINE_ZERO_TEST_OBJECT = AMPLITUDE_NORMS_A_D_A_N_AND_A_S_NOT_SQUARED_AMPLITUDES
PATH_BASELINE_ZERO_SCALE       = AGGREGATED_RAW_SPECTRAL_MAJORANT_NORM
```

### F13. Poids spectraux signés

AVANT toute comparaison de poids : exiger la correspondance catégorielle du nombre de clusters, de la multiplicité et de l'identité spectrale mappée du cluster.

Échelle de côté :

```math
S_{C,side}=\sum_{clusters}|C_{cluster,side}|.
```

Partagée : `S_C=\max(S_{C,left},S_{C,right})`. Aucun plancher arbitraire.

Si les deux côtés sont structurellement inactifs : branche structurelle / non applicable.

Correspondance de cluster non résolue : `NUMERICALLY_INCONCLUSIVE`.

### F14. Activité tangente

Pour `D_A=-i[A,rho]`, utiliser :

```math
S_D(A)=2\,\|A\|_2\,\|\rho\|_{HS}.
```

Classifier `||D_A||_HS / S_D(A)` avec la famille zéro/non-zéro (§E).

Ceci s'applique lorsque l'activité tangente numérique doit être résolue, y compris `D_Phi` et `D_{n_p}` là où elle n'est pas structurellement fixée.

Une tangente numériquement zéro-compatible n'est PAS un générateur structurellement inactif.

### F15. Oracle d'orthogonalité de Hilbert-Schmidt

Pour une orthogonalité exacte attendue `<D_A,D_B>_HS=0` :

Si les deux normes de tangente sont `ROBUST_NONZERO` :

```math
R_{HS}=\langle D_A,D_B\rangle_{HS},
\qquad
S_{HS}=\|D_A\|_{HS}\,\|D_B\|_{HS}.
```

Utiliser la règle d'oracle exact normalisée (§D).

Si une tangente est `STRUCTURAL_ZERO` : l'orthogonalité est structurellement triviale ; ce point ne compte pas comme évidence d'oracle indépendante.

Si une tangente est seulement `NUMERICALLY_ZERO_COMPATIBLE` : `NUMERICALLY_INCONCLUSIVE`.

Ne PAS orthogonaliser/projeter (Gram-Schmidt) les vecteurs avant l'oracle.

Normatif :

```text
TANGENT_ORTHOGONALITY_RESIDUAL = NORMALIZED_HILBERT_SCHMIDT_INNER_PRODUCT
```

### F16. Décisions numériques de rang / noyau

Pour toute matrice `A` dont le rang/noyau affecte un verdict scientifique (matrice de Gram/base tangente, restriction `M_F|S`, application dynamique restreinte, oracle numérique de rang de décalage de boucle), utiliser SVD en coordonnées canoniques fixes.

Calculer `A^(p)`, `A^(2p)`. Soit `sigma_k` les valeurs singulières de `A^(2p)`, décroissantes.

```math
e_A=\|A^{(2p)}-A^{(p)}\|_2
```

avec norme spectrale d'opérateur. Soit `sigma_max=sigma_1`.

Si `sigma_max` n'est pas `ROBUST_NONZERO` et qu'aucun théorème structurel de rang-zéro exact ne s'applique : `RANK_NUMERICALLY_INCONCLUSIVE`.

Sinon, normaliser chaque valeur singulière :

```math
L_{\sigma,k}=\max(0,\sigma_k-e_A)/\sigma_{max},
\qquad
U_{\sigma,k}=(\sigma_k+e_A)/\sigma_{max}.
```

Classification :

```text
L_sigma,k > 1e-8  -> SINGULAR_VALUE_ROBUST_NONZERO
U_sigma,k <= 1e-9 -> SINGULAR_VALUE_NUMERICALLY_ZERO_COMPATIBLE
sinon             -> SINGULAR_VALUE_CONTROL_SENSITIVE
```

CRITIQUE : une valeur singulière `NUMERICALLY_ZERO_COMPATIBLE` n'établit PAS un noyau exact.

Normatif :

```text
NUMERICAL_ZERO_SINGULAR_VALUE_CREATES_EXACT_KERNEL = NO
```

---

## G. Routage d'identifiabilité statique/dynamique

La condition mathématique gelée reste :

```text
STATIC PASS  ssi  S_resp intersect ker(M_F) = {0}.
```

Règle numérique opérationnelle :

```text
STATIC = PASS
    uniquement lorsque l'injectivité de M_F|S_resp est numériquement résolue
    par toutes les directions singulières requises ROBUST_NONZERO sous F16.
```

Si l'injectivité n'est pas résolue parce qu'une valeur singulière requise est :
`NUMERICALLY_ZERO_COMPATIBLE`, `CONTROL_SENSITIVE`, ou `NUMERICALLY_INCONCLUSIVE` :

```text
STATIC = NUMERICALLY_INCONCLUSIVE
```

```text
STATIC = FAIL
    uniquement lorsqu'un noyau restreint non trivial est établi par :
    - un certificat analytique structurel ; ou
    - un autre certificat algébrique exact déjà gelé.
```

Une valeur singulière simplement petite ne crée jamais `STATIC FAIL`.

La même règle s'applique à l'application dynamique restreinte lorsque l'évaluation `DYNAMIC` est nécessaire.

Normatif :

```text
STATIC_DYNAMIC_NUMERICAL_RANK_RULE = ROBUST_NONZERO_FOR_INJECTIVITY_EXACT_CERTIFICATE_FOR_KERNEL
STATIC_DYNAMIC_NUMERICAL_ZERO_KERNEL_PROMOTION = REJECTED
```

Aucune étude temporelle n'est débloquée par une porte d'identifiabilité numériquement inconclusive.

---

## H. Ligne de base de chemin — correction finale Z1

La trichotomie de ligne de base est évaluée UNIQUEMENT après :

- que `nu_*` certifié soit disponible ;
- qu'au moins un canal actif à `nu_*` soit `ROBUST_NONZERO` / structurellement actif.

Définitions :

```text
DIRECT_DOMINANT_BASELINE ssi :
    - A_D est ROBUST_NONZERO ; ET
    - l'ensemble non direct à nu_* est nul par certificat STRUCTURAL_ANALYTIC / exact.
```

Un `A_N` seulement `NUMERICALLY_ZERO_COMPATIBLE` est insuffisant.

```text
NO_DIRECT_BASELINE ssi :
    - A_N est ROBUST_NONZERO ; ET
    - l'ensemble direct à nu_* est nul par certificat STRUCTURAL_ANALYTIC / exact.
```

Un `A_D` seulement `NUMERICALLY_ZERO_COMPATIBLE` est insuffisant.

```text
MIXED_BASELINE ssi :
    - A_D est ROBUST_NONZERO ; ET
    - A_N est ROBUST_NONZERO.
```

Si `A_D` ou `A_N` est seulement `NUMERICALLY_ZERO_COMPATIBLE`, `ZERO_CONTROL_SENSITIVE`, ou `NUMERICALLY_INCONCLUSIVE`, et qu'aucun théorème de zéro structurel ne résout cette branche :

```text
PATH_BASELINE_STATUS = PATH_CONTROL_NUMERICALLY_INCONCLUSIVE
```

ou le statut de ligne de base fail-closed équivalent déjà existant.

Ne PAS émettre `DIRECT_DOMINANT`/`NO_DIRECT` à partir d'une petitesse numérique.

`NO_ACTIVE_PATH_RESPONSE` : utilisable uniquement sous sa sémantique exacte/structurelle déjà gelée, jamais à partir d'une seule petitesse numérique finie.

Normatif :

```text
PATH_DIRECT_DOMINANCE_NUMERICAL_SMALLNESS_AS_EXACT_ZERO = REJECTED
```

---

## I. Certification d'exposant — correction finale B2

Normatif :

```text
NUMERICAL_ZERO_BRANCH_IS_CERTIFIED = NO
CERTIFIED_EXPONENT_PRECEDING_ZERO_REQUIREMENT = STRUCTURAL_OR_EXACT_CERTIFICATE_ONLY
```

Un `nu=r` confirmatoire exige :

- que tout ordre autorisé inférieur soit nul par certificat structurel/exact ;
- que le coefficient courant soit `ROBUST_NONZERO`.

Si un coefficient autorisé inférieur est seulement `NUMERICALLY_ZERO_COMPATIBLE` :

```text
SHORT_TIME_EXPONENT = NUMERICALLY_INCONCLUSIVE
```

pour tout consommateur confirmatoire.

Un exposant candidat diagnostique peut être publié séparément mais ne peut entrer dans :

- la convergence à temps court ;
- `nu_*` de pureté de chemin ;
- toute interprétation d'événement confirmatoire.

Bord `a1` :

```text
NUMERICALLY_ZERO_COMPATIBLE -> EDGE_SHORT_ORACLE = NUMERICALLY_INCONCLUSIVE_FOR_CERTIFIED_EXPONENT
```

Aucun saut automatique confirmatoire `nu>=3`.

---

## J. Oracle de rééchelonnement — correction finale B3

Fixé :

```text
RESCALING_S_VALUES = {1/2,2}
RESCALING_ORACLE_CUTOFF_SCOPE = {Lambda=2,Lambda=3}
```

Référence uniquement :

```math
H_s = s\,H_{ref}.
```

Ne PAS étendre `C_eff=s` à des fonds physiques arbitraires.

La recomputation générique indépendante est obligatoire.

Relations exactes continues primaires :

```text
T_peak
T_grow
T_thr(eta)
T_down(eta)
C_eff^grow
C_eff^thr(eta)
Delta1=0 à la référence symétrique
```

Couche catégorielle obligatoire :

```text
RESCALING_ORACLE_PATH_RECURRENCE_CATEGORICAL_LAYER = MANDATORY
```

Inclure explicitement :

- le profil d'admissibilité `eta` ;
- le statut d'événement ;
- l'exposant/statut certifié à temps court ;
- `EDGE_SHORT_ORACLE` ;
- le statut terminal `SHORT_TIME_CONVERGENCE_*` où applicable ;
- `DELTA1_SHORT_LIMIT` / statut terminal à temps court où applicable ;
- `PATH_BASELINE_STATUS` ;
- `PATH_CONTROL_STATUS` ;
- `PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE` ;
- `RECURRENCE_RETURN_PREDICATE` ;
- `RECURRENCE_STATUS` ;
- `RECURRENCE_CONTROL_ACCEPTABLE` ;
- l'éligibilité locale d'estimateur ;
- les autres dépendances catégorielles déjà gelées de la même chaîne d'événement confirmatoire.

Comparaisons complètes continues `R_path(t)`/`C_j(t)` : `DIAGNOSTIC_ONLY`.

Asymétrie de porte de précision induite par le rééchelonnement : `NUMERICALLY_INCONCLUSIVE`, jamais `FAIL`, sauf si une quantité scientifique mappée résolue viole la relation exacte.

---

## K. Indépendance de l'oracle / mode d'évidence — Z3

Chaque point d'oracle numérique publie :

```text
ORACLE_POINT_EVIDENCE_MODE = INDEPENDENT_RECOMPUTATION | SATISFIED_BY_CONSTRUCTION
```

`INDEPENDENT_RECOMPUTATION` : la valeur testée est produite par une voie numérique générique ou indépendante qui n'impose PAS le théorème attendu.

`SATISFIED_BY_CONSTRUCTION` : la représentation/formule d'implémentation force l'identité avant le contrôle.

Exemples :

- copier le partenaire de symétrie ;
- coder en dur un zéro exact ;
- fixer les moments pairs à zéro par formule ;
- inverser le signe d'un scalaire déjà calculé ;
- rééchelonner un événement stocké au lieu de recalculer ;
- canoniser `pq`/`qp` sur une seule réponse stockée ;
- projeter/orthogonaliser des tangentes avant un contrôle d'orthogonalité.

Si une famille REQUIERT une recomputation indépendante et que l'implémentation utilise un partenaire construit :

```text
INVALID_BY_CONSTRUCTION
```

et la famille échoue (`FAIL`).

Un diagnostic structurellement par construction peut être publié, mais :

```text
SATISFIED_BY_CONSTRUCTION ne compte JAMAIS comme évidence de PASS pour la non-vacuité de la famille d'oracle.
```

Normatif :

```text
ZERO_SYMMETRY_INDEPENDENT_EVIDENCE_RULE = SATISFIED_BY_CONSTRUCTION_DOES_NOT_COUNT_AS_PASS_EVIDENCE
```

---

## L. Symétrie catégorielle

```text
même catégorie mappée résolue      -> PASS
catégorie mappée résolue différente -> FAIL
côté requis non résolu              -> NUMERICALLY_INCONCLUSIVE
```

Appliquer la sémantique de correspondance (mapping), pas des étiquettes littérales naïves lorsque l'orientation change.

---

## M. Registre obligatoire des oracles — A–O final

```text
A. DELTA1_DELTA0_MAPPED_ORACLE
B. DELTA2_MAPPED_ORACLE
C. NEGATIVE_DELTA_FULL_MAPPED_ORACLE_CONTINUOUS_LAYER
D. SOFT_LOOP_STATIC_GAP_EVENNESS
E. SOFT_LOOP_STATIC_PHI_ODDNESS_AND_X0_ZERO
F. SOFT_LOOP_DYNAMIC_DELTA1_ODDNESS
G. SHORT_TIME_DELTA1_ZERO_ODDNESS_WHERE_APPLICABLE
H. SYNTHETIC_GLOBAL_RESCALING_ORACLE
I. SOURCE_RECEIVER_REVERSED_RELATION_SUBSET
J. HAMILTONIAN_REFLECTION_COVARIANCE_ORACLE
K. EDGE_SPECTRAL_SUM_RULE_NUMERICAL_ORACLE
L. MOMENT_OPERATOR_SPECTRAL_CROSSCHECK
L2. ZERO_GRADE_AND_EVEN_SECTOR_MOMENT_ORACLES
M. D2_FREE_HOPPING_NUMERICAL_ORACLE
N. CYCLIC_TANGENT_ORTHOGONALITY_ORACLE
O. TRUNCATED_LOOP_SHIFT_RANK_ORACLE
```

---

## N. Familles A/B — oracles Delta mappés

`Delta1(delta=0)` et `Delta2` : FERMETURE COMPLÈTE DE DÉPENDANCE MAPPÉE PLUS SCALAIRE DÉRIVÉ.

La computation d'orbite/relation indépendante est obligatoire.

Une annulation scalaire seule est insuffisante.

Incompatibilité catégorielle mappée résolue : `FAIL`.

Dépendance mappée non résolue : `NUMERICALLY_INCONCLUSIVE`.

`Delta1(delta=0)` : théorème structurel, le contrôle numérique est un oracle de pipeline uniquement.

---

## O. Famille C — delta négatif

Conserver inchangés le sous-ensemble figé / l'extension de branche / la recomputation indépendante.

Les formes de résidu continu proviennent désormais de ce contrôle.

```text
NEGATIVE_DELTA_ORACLE_CONTINUOUS_TOLERANCE_SOURCE = NUMERICAL_ZERO_AND_SYMMETRY_CONTROL
```

Pour les poids spectraux : correspondance d'identité/multiplicité de cluster D'ABORD, puis résidu de poids continu.

Aucun changement de sous-ensemble.

---

## P. Familles D/E/F — SOFT-LOOP

Statique : la parité de gap utilise le ratio log (F1). L'imparité de Phi / `x=0` utilisent des résidus signés normalisés (F3).

Dynamique : chaque paire explicite `+/-h` de `Delta1` doit passer l'imparité avant usage dans `Xi1`.

Existant : `STATIC_COLLAPSE_TOLERANCE=0.10` reste séparé.

`Xi1=0` n'est pas un `FAIL` : c'est uniquement une publication zéro/non-zéro numérique sous ce contrôle.

---

## Q. Famille G — Delta1 à temps court

Appliquer le zéro exact/imparité là où structurellement applicable.

`Delta1_short` reste un oracle algébrique, pas un estimateur de propagation.

Ne pas utiliser la petitesse numérique pour inventer un exposant certifié.

---

## R. Famille H — rééchelonnement synthétique

Comme section J. À `s={1/2,2}`, `Lambda={2,3}`, référence uniquement.

Diagonalisation/réponse/recomputation d'événement génériques obligatoires.

Ne PAS dériver les sorties rééchelonnées par substitution.

---

## S. Famille I — source / récepteur

Ensemble fixe à six cas à `Lambda=2` :

```text
theta=(1,0,0)    : un représentant d=1, d=2, d=3.
theta=(1,0,2/5)  : un représentant d=1, d=2, d=3.
```

Calculer `pq` et `qp` indépendamment. Aucune réponse partagée canonicalisée ne compte.

Parité temporelle `K` : publier :

```text
K_TIME_PARITY_IMPLEMENTATION_MODE = SINE_ONLY_BY_CONSTRUCTION | INDEPENDENT_GENERIC_TIME_EVOLUTION
```

Si sinus uniquement : aucune évidence indépendante `+/-t` n'est revendiquée.

Aucune implémentation à temps générique n'est requise par 0B.

---

## T. Famille J — covariance hamiltonienne

À chaque paire d'oracle négatif `+/-delta` figée réellement exécutée : assembler `H(+delta)`, `H(-delta)` indépendamment.

Utiliser le résidu F5.

Aucun nouveau point de paramètre.

---

## U. Famille K — règle de somme spectrale de bord

Exact :

```math
\sum_{\omega>0}C(\omega)\,\omega=J\langle X_i\rangle.
```

Cas fixes : `Lambda=2` et `Lambda=3`.

À chaque cutoff :

- référence `(1,0,0)`, une arête représentative ;
- `(1,0,2/5)`, une arête `O1A` ;
- `(1,0,2/5)`, une arête `O1B`.

Total : 6.

Chemins indépendants : moment spectral vs espérance d'opérateur statique.

Échelle correcte de résidu :

```math
S_{M1}=\sum_{\omega>0}|C(\omega)|\,\omega.
```

```math
S_{edge}=\max\bigl(S_{M1},\,J\|X_i\|_2\bigr).
```

Normaliser la différence par `S_edge`.

Normatif :

```text
EDGE_SPECTRAL_SUM_RULE_NUMERICAL_ORACLE = MANDATORY
```

---

## V. Famille L — moments opératoriels / spectraux

Sous-ensemble fixe à `Lambda=2` :

```text
theta_ref   = (1,0,0)
theta_break = (1,0,2/5)
```

À chacun : un représentant `d=1`, `d=2`, `d=3`.

Ordres : `r={1,3,5}`.

CHAQUE ordre est exécuté.

CRITIQUE Z3b : pour `r<d(p,q)`, ne PAS router `NOT_APPLICABLE`.

Ces moments structurellement nuls sont des tests obligatoires de zéro spectral absolu.

Exemples : `M1` à `d=2` et `d=3` DOIT être calculé par la voie spectrale générique et testé contre zéro sous `S_a,1`.

Pour les ordres structurellement autorisés non nuls : comparer les voies opérateur et spectrale indépendantes.

Normatif :

```text
MOMENT_CROSSCHECK_STRUCTURAL_ZERO_ORDERS = MANDATORY_ABSOLUTE_SPECTRAL_ZERO_TEST
MOMENT_CROSSCHECK_NOT_APPLICABLE_FOR_R_LT_D = FORBIDDEN
```

Aucun moment ne peut disparaître de l'ensemble fixe parce que la théorie prédit zéro.

---

## W. Famille L2 — zéro-grade / secteur pair

Même sous-ensemble de relation que V.

Ordres : `r={1,2,3,4,5}`.

Zéro-grade : zéro attendu à chaque ordre applicable.

Moments du secteur physique pair : zéro attendu à `r={2,4}`.

L'implémentation d'exécution de l'oracle doit évaluer la grandeur générique sectoriellement projetée SANS coder en dur le théorème à zéro pour compter comme `INDEPENDENT_RECOMPUTATION`.

Si le code de production utilise une simplification structurelle exacte : publier `SATISFIED_BY_CONSTRUCTION` ; cela ne compte pas comme évidence indépendante de non-vacuité.

L'implémentation de l'oracle doit fournir au moins une voie indépendante générique pour que cette famille passe (`PASS`) globalement.

---

## X. Famille M — hopping pur D2

À `g=0`, `mu=0`, `delta=0`.

`Lambda=2` et `Lambda=3`. Une relation `d=2` représentative.

La machinerie générique sectorielle/de chemin doit être exécutée SANS imposer le résultat d'inactivité bipartite pour compter comme évidence indépendante.

Vérifier :

```text
D2_TARGET_TRANSITION_RESPONSE = INACTIVE
```

et si la réponse totale est active : `P_direct=0`, `P_0=0`.

Si la réponse totale est structurellement inactive : utiliser le routage figé `INACTIVE`/`NOT_DEFINED`.

Coder en dur `TARGET_DIRECT` inactif à partir du théorème : `SATISFIED_BY_CONSTRUCTION`, pas une évidence indépendante.

---

## Y. Famille N — orthogonalité tangente cyclique

Théorème exact à `delta=0` :

```math
\langle D_\Phi,D_{n_p}\rangle_{HS}=0\qquad\forall p.
```

Portée : tous les points nominaux MAIN `delta=0` `Lambda=2` où le bloc tangent/statique est déjà évalué.

À `Lambda=3` : uniquement les points où le bloc tangent/statique est déjà requis par les dépendances de troncature/référence existantes ; ne pas créer de nouvelle campagne `Lambda=3`.

Calculer `D_Phi` et `D_{n_p}` à partir de commutateurs génériques. Ne PAS les orthogonaliser/projeter avant de tester.

Appliquer l'activité F14 et l'orthogonalité F15.

Si une tangente est structurellement nulle : relation triviale, pas de comptage d'évidence indépendante.

Si seulement numériquement zéro-compatible : `NUMERICALLY_INCONCLUSIVE`.

Normatif :

```text
CYCLIC_TANGENT_ORTHOGONALITY_ORACLE = MANDATORY
```

---

## Z. Famille O — oracle de rang de décalage de boucle tronqué

Rang analytique exact :

```math
j=2\Lambda-k,
\qquad
r_\Lambda(L^k)=\sum_n\max(0,j+1-spread(n)).
```

Table attendue :

```text
j:    0  1  2  3  4  5
rang: 1 18 38 58 78 98
```

Exécuter l'oracle de rang numérique sur la matrice assemblée `L^k` en utilisant la règle SVD F16.

`Lambda=2` : tous `k=1..4`.
`Lambda=3` : tous `k=1..6`.

Le rang attendu provient de la formule combinatoire analytique. Le rang numérique observé provient de la SVD de `L^k` assemblée.

Ne PAS dériver le rang observé en comptant le même support utilisé pour construire la formule attendue.

Normatif :

```text
TRUNCATED_LOOP_SHIFT_RANK_ORACLE = MANDATORY
TRUNCATED_LOOP_SHIFT_RANK_ORACLE_CUTOFF_SCOPE = {Lambda=2,Lambda=3}
```

---

## AA. Rang/noyau de campagne — consommateur

Distinct de la famille exacte O.

À chaque point de campagne où le rang/noyau de `S_n`, `S_E` ou `M_F|S_resp` entre dans un verdict scientifique : appliquer F16.

Des relations structurelles connues peuvent fournir des bornes supérieures exactes/directions nulles exactes (par exemple `sum_p D_{n_p}=0`).

Des valeurs singulières `ROBUST_NONZERO` établissent des directions indépendantes résolues.

Une valeur singulière `NUMERICALLY_ZERO_COMPATIBLE` n'établit PAS une direction nulle exacte.

Donc :

- `PASS` d'injectivité exige que toutes les directions singulières requises soient robustes-non-nulles ;
- une valeur singulière non résolue/petite non résolue -> `NUMERICALLY_INCONCLUSIVE` ;
- `FAIL` exige un certificat exact/structurel de noyau.

Publier : spectre singulier, bornes inférieures/supérieures normalisées, décompte robuste-non-nul résolu, décompte de nullité structurelle, statut de rang/injectivité.

Aucun seuil SVD post-hoc.

---

## AB. Non-vacuité de la famille d'oracle — Z3 final

Publier par famille :

```text
ORACLE_FAMILY_REQUIRED_POINT_COUNT
ORACLE_FAMILY_APPLICABLE_POINT_COUNT
ORACLE_FAMILY_INDEPENDENT_PASS_COUNT
ORACLE_FAMILY_SATISFIED_BY_CONSTRUCTION_COUNT
ORACLE_FAMILY_FAIL_COUNT
ORACLE_FAMILY_INCONCLUSIVE_COUNT
ORACLE_FAMILY_INVALID_BY_CONSTRUCTION_COUNT
ORACLE_FAMILY_NOT_APPLICABLE_COUNT
```

Routage de famille :

```text
FAIL
    si un point requis quelconque est ROBUST_ORACLE_FAIL ou INVALID_BY_CONSTRUCTION.

NUMERICALLY_INCONCLUSIVE
    si aucun FAIL et qu'un point requis quelconque est ORACLE_CONTROL_SENSITIVE
    ou NUMERICALLY_INCONCLUSIVE.

PASS
    uniquement si :
    ORACLE_FAMILY_INDEPENDENT_PASS_COUNT >= 1
    ET chaque autre point requis est ROBUST_ORACLE_PASS ou NOT_APPLICABLE
    ou SATISFIED_BY_CONSTRUCTION
    ET aucun échec/inconclusif n'existe.

sinon
    NUMERICALLY_INCONCLUSIVE_NO_INDEPENDENT_PASS
```

Normatif :

```text
ZERO_SYMMETRY_ORACLE_FAMILY_NONVACUITY_RULE = AT_LEAST_ONE_APPLICABLE_INDEPENDENT_ROBUST_PASS_REQUIRED
```

`SATISFIED_BY_CONSTRUCTION` ne compte jamais pour la non-vacuité.

---

## AC. Agrégation finale du contrôle

Statut de campagne exécuté :

```text
FAIL
    si une famille d'oracle obligatoire quelconque FAIL.

sinon NUMERICALLY_INCONCLUSIVE
    si :
    - une famille obligatoire quelconque est inconclusive / sans passage indépendant ;
    - une dépendance de rang/noyau nécessaire à une revendication confirmatoire
      est non résolue ;
    - une branche zéro/non-zéro nécessaire à une revendication confirmatoire
      est non résolue.

sinon PASS.
```

`PASS` signifie uniquement :

```text
NO_NUMERICAL_INCONSISTENCY_DETECTED_WITH_MANDATORY_EXACT_ORACLES
AND
REQUIRED_ZERO_NONZERO_AND_RANK_BRANCHES_RESOLVED_UNDER_PREREGISTERED_POLICY
```

Cela ne prouve PAS :

- l'exactitude arithmétique complète ;
- l'absence de tout défaut d'implémentation ;
- que zéro numérique = zéro mathématique ;
- une quelconque hypothèse physique.

---

## AD. Support spectral groupé — exclusion explicite

Préserver exactement :

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
```

Ceci est HORS du décompte des contrôles numériques majeurs.

Ce lot NE :

- ne le dérive pas ;
- ne le ferme pas ;
- ne revendique pas qu'il est inutile.

Il doit être signalé lors du futur audit de clôture du modèle.

---

## AE. Bloc de statut normatif final

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE

ZERO_SYMMETRY_TOLERANCE_VALUES = {1e-9,3e-9,1e-8}

ZERO_SYMMETRY_RESIDUAL_FORM_REGISTRY = REQUIRED_AND_DETERMINISTIC_BEFORE_EXECUTION

ZERO_SYMMETRY_OPERATOR_NORM = OPERATOR_SPECTRAL_NORM

SHORT_TIME_ZERO_SCALE_FLOOR = NONE

NUMERICAL_ZERO_BRANCH_IS_CERTIFIED = NO

CERTIFIED_EXPONENT_PRECEDING_ZERO_REQUIREMENT = STRUCTURAL_OR_EXACT_CERTIFICATE_ONLY

PATH_BASELINE_ZERO_TEST_OBJECT = AMPLITUDE_NORMS_A_D_A_N_AND_A_S_NOT_SQUARED_AMPLITUDES

PATH_DIRECT_DOMINANCE_NUMERICAL_SMALLNESS_AS_EXACT_ZERO = REJECTED

NUMERICAL_ZERO_SINGULAR_VALUE_CREATES_EXACT_KERNEL = NO

STATIC_DYNAMIC_NUMERICAL_RANK_RULE = ROBUST_NONZERO_FOR_INJECTIVITY_EXACT_CERTIFICATE_FOR_KERNEL

RESCALING_ORACLE_PATH_RECURRENCE_CATEGORICAL_LAYER = MANDATORY

ZERO_SYMMETRY_INDEPENDENT_EVIDENCE_RULE = SATISFIED_BY_CONSTRUCTION_DOES_NOT_COUNT_AS_PASS_EVIDENCE

HAMILTONIAN_REFLECTION_COVARIANCE_ORACLE = MANDATORY

EDGE_SPECTRAL_SUM_RULE_NUMERICAL_ORACLE = MANDATORY

MOMENT_OPERATOR_SPECTRAL_CROSSCHECK = MANDATORY_FUTURE_VALIDATION

CYCLIC_TANGENT_ORTHOGONALITY_ORACLE = MANDATORY

TRUNCATED_LOOP_SHIFT_RANK_ORACLE = MANDATORY

D2_FREE_HOPPING_NUMERICAL_ORACLE = MANDATORY_AT_LAMBDA2_AND_LAMBDA3

ZERO_SYMMETRY_ORACLE_FAMILY_NONVACUITY_RULE = AT_LEAST_ONE_APPLICABLE_INDEPENDENT_ROBUST_PASS_REQUIRED

NEGATIVE_DELTA_ORACLE_CONTINUOUS_TOLERANCE_SOURCE = NUMERICAL_ZERO_AND_SYMMETRY_CONTROL

ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL = SATISFIED_BY_THIS_CONTROL

RESCALING_S_VALUES = {1/2,2}

RESCALING_ORACLE_CUTOFF_SCOPE = {Lambda=2,Lambda=3}

ZERO_SYMMETRY_POSTHOC_TOLERANCE_SELECTION = FORBIDDEN

GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
```

Ce document ferme le dernier paramètre numérique majeur préenregistré de Toy Model 0B. Il n'autorise ni l'implémentation, ni le gel du modèle : ces décisions restent exclusivement sous l'autorité explicite de Lionel ORCIL via `docs/governance/current-task.md`.
