# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11. Il constitue, avec le dépôt, la mémoire durable du lot courant.

## État Git

```text
ACTIVE_BRANCH = documentation/model0b-foundation
BASE_COMMIT   = 08d5ca506ff05e15dd9bc084ea121c3d0a19b662
```

`BASE_COMMIT` est le merge canonique de clôture du Toy Model 0A sur `master` et reste le point de départ du lot documentaire 0B.

Aucune modification de code 0B n'est autorisée dans le lot courant.

---

## État documentaire

```text
C_HYPOTHESIS                    = FROZEN
TOY_MODEL_0_SPECIFICATION       = FROZEN
IMPLEMENTATION_0A_CONTRACT      = FROZEN / EXECUTED
CLOSURE_0A_REPORT               = CLOSED
GOVERNANCE_COLLABORATION        = FROZEN
GOVERNANCE_DOCUMENTATION        = FROZEN
GOVERNANCE_SOFTWARE_ARCH        = FROZEN

MODEL0B_SPECIFICATION           = REVIEW_IN_PROGRESS
MODEL0B_VALIDATION_PLAN         = REVIEW_IN_PROGRESS
MODEL0B_PREFREEZE_CONSOLIDATION = ACTIVE_STATUS_INDEX
SCIENTIFIC_METHOD_GOVERNANCE    = DRAFT_IN_FEATURES
```

Sources principales :

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
```

Index courant de consolidation :

```text
docs/toy-models/toy0b/pre-freeze-consolidation.md
```

Cet index ne remplace pas la physique des sources principales. Il donne le statut courant des décisions déjà arbitrées lorsque les anciennes listes `OPEN` de `specification.md` ou `validation-plan.md` sont devenues obsolètes. Il doit être intégré mécaniquement dans les deux sources principales avant gel final.

Le brouillon méthodologique :

```text
features/scientific-method-governance.md
```

reste volontairement hors `docs/governance/` tant que son gel et sa migration n'ont pas été autorisés explicitement.

---

## État du code

```text
CODE_STATUS       = IMPLEMENTED_ACCEPTED_0A_ONLY
TESTS_STATUS      = PASSED_89
BENCHMARK_0A      = CLOSED
INSTRUMENT_0A     = VALIDATED
IMPLEMENTATION_0B = NOT_AUTHORIZED
```

0A ne doit pas être rouvert sans défaut bloquant nouvellement démontré.

---

## État scientifique 0B consolidé

```text
MODEL0B_SYSTEM_AND_GAUSS           = VALIDATED_FOR_FREEZE
MODEL0B_TRUNCATION_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_OBSERVABLES         = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_IDENTIFIABILITY     = VALIDATED_FOR_FREEZE
MODEL0B_DECLARED_SYMMETRIES        = VALIDATED_FOR_FREEZE
MODEL0B_NULL_ORACLES               = VALIDATED_FOR_FREEZE
MODEL0B_KUBO_PROBE                 = VALIDATED_FOR_FREEZE
MODEL0B_PRIMARY_SIGNAL_DELTA1      = VALIDATED_FOR_FREEZE
MODEL0B_PATH_GRADING               = VALIDATED_FOR_FREEZE
MODEL0B_PATH_PURITY_STRUCTURE      = VALIDATED_FOR_FREEZE
MODEL0B_RECURRENCE_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_SHORT_TIME_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_SPECTRAL_TIME_STRUCTURE    = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
MODEL0B_SOFT_LOOP_STRUCTURE        = VALIDATED_FOR_FREEZE
MODEL0B_PARAMETER_CAMPAIGN_SHAPE   = VALIDATED_FOR_FREEZE

MODEL0B_NUMERICAL_CONTROL_VALUES   = OPEN
MODEL0B_FINAL_ACCEPTANCE_RULES     = OPEN
MODEL0B_DOCUMENT_CONSOLIDATION     = IN_PROGRESS
```

Les statuts `VALIDATED_FOR_FREEZE` ne valent pas encore `FROZEN`. Le gel est une décision explicite de Lionel ORCIL après revue du paquet final.

---

## Invariants principaux 0B

```text
TOPOLOGY                  = 6-cycle
BACKGROUND                = (0,1,0,1,0,1)
REFERENCE_TRUNCATION      = Lambda=2
TRUNCATION_CHECK          = Lambda=3
PILOT_TRUNCATION          = Lambda=1
PHYSICAL_DIMENSION        = 40*Lambda - 2
REFERENCE_PHYSICAL_DIM    = 78
CHECK_PHYSICAL_DIM        = 118

REFERENCE_HAMILTONIAN     = H(g=1, mu=0, delta=0), J=1
GLOBAL_RESCALING_MODE     = CONTROL_ONLY
PRIMARY_PROPAGATION_PROBE = Kubo(n_p -> n_q)
PRIMARY_TIME_ESTIMATOR    = T_grow
SECONDARY_TIME_FAMILY     = T_thr(eta)
PRIMARY_RELATIONAL_SIGNAL = Delta1
GLOBAL_NULL_ORACLE        = Delta2 == 0
```

La réciprocité imposée par stationnarité + `K` ferme l'ancien problème d'orientation source-récepteur :

```text
chi_pq(t) = chi_qp(t)
ORDERED_RELATION_CONVENTION = CLOSED_BY_K_RECIPROCITY
```

---

## Campagne physique consolidée

Campagne principale :

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

Contrôles séparés :

```text
g=0, mu=0          = pure-hopping oracle
g=0.10             = weak-g stress, outside nominal domain
delta=0.9          = disclosed qualification / stress, outside nominal domain
```

Sous-campagne SOFT-LOOP :

```text
g  = 1
mu = {-1.25, -1.5, -2}
delta around 0 via dimensionless control family
```

La grille MAIN mesure une réponse finie non linéaire ; elle ne sert pas à approximer `Xi1`.

Le sous-ensemble exact de points `delta<0` utilisé comme oracle de covariance et le sous-ensemble exact de contrôles `Lambda=3` restent à préenregistrer.

---

## Architecture temporelle consolidée

La réponse est évaluée par représentation spectrale finie en sinus. Les différences finies temporelles, l'interpolation comme estimateur final et la quadrature nominale des poids sectoriels sont rejetées.

Fonctions de certification :

```text
T_peak
    chi'(t)=0, racine qualifiante donnant le premier maximum de F

T_thr / T_down
    chi(t)-s*2*sqrt(eta)=0 sur le premier lobe

T_grow
    H_grow(t)=chi'(t)^2+chi(t)*chi''(t)=0
    puis choix du premier maximiseur global de F'
```

Une seule famille de raffinement :

```text
B = {beta_1 > ... > beta_K > 0}
```

avec facteur spectral analytique :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

Les valeurs numériques `beta_k` restent ouvertes.

---

## Path / secteurs : dernier défaut bloquant clos

Le canal auto-conjugué `m=0` doit être compté une seule fois en algèbre générale.

Dans le secteur physique 0B, Gauss implique que les six `E_i` déterminent entièrement `n`. La composante `Pi_0(O)` est donc diagonale dans la base physique et :

```text
ZERO_GRADE_KUBO_CHANNEL      = INACTIVE_EXACT
ZERO_GRADE_NON_TARGET_WEIGHT = ZERO_EXACT
```

Il n'existe aucune correction numérique cachée de `P_sector` ou `Purity_direct` due à `m=0`.

---

## SOFT-LOOP consolidé

Le doublet cyclique mou possède la structure :

```math
t_loop=O(J^6/|mu|^5).
```

Les données déjà vues confirmant la pente vers `-5` sont de la qualification non confirmatoire.

Modèle effectif :

```math
H_eff=E_c I+3g delta sigma_z+t_loop sigma_x+...
```

avec :

```math
x=6g delta/gap_0.
```

Porte statique préalable à toute dynamique SOFT-LOOP :

```math
gap(delta)/gap_0 ~= sqrt(1+x^2)
```

```math
2<Phi> ~= -x/sqrt(1+x^2)
```

`Delta1` n'est pas contraint à suivre une courbe universelle exacte en `x`.

La dérivée utilise :

```math
delta_c=gap_0/(6g)
```

et :

```math
h_k=alpha_k*delta_c.
```

Les `alpha_k` ne seront fixés qu'après fermeture du budget numérique dynamique.

---

## Paramètres réellement ouverts avant gel

Cette liste remplace les anciennes listes dispersées pour le pilotage du lot courant.

```text
# contrôle temporel / précision
BETA_REFINEMENT_VALUES
ROOT_SOLVER_TOLERANCES
ARGMAX_TOLERANCES
SPECTRAL_PRECISION_CONTROL
DELTA1_PROPAGATED_ERROR_BUDGET

# SOFT-LOOP
STATIC_X_CONTROL_VALUES
STATIC_COLLAPSE_NUMERICAL_CRITERION
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE

# interprétation temporelle
ETA_GRID_AND_ADMISSIBLE_DOMAIN
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE
EPS_PATH_CONTROL_DOMAIN_AND_GRID
GAMMA_CONTROL_DOMAIN_AND_GRID
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS

# campagne / troncature
NEGATIVE_DELTA_ORACLE_SUBSET
TRUNCATION_STRESS_POINT_SUBSET
TRUNCATION_COMPARISON_TOLERANCES

# verdicts
ESTIMATOR_COHERENCE_CRITERION
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

Ne doivent plus réapparaître comme `OPEN` :

```text
ORDERED_RELATION_CONVENTION
PARAMETER_CAMPAIGN_MAIN_GRID
TIME_INTERPOLATION_AS_FINAL_ESTIMATOR
TIME_FINITE_DIFFERENCE_DERIVATIVES
GLOBAL_FACTOR_TWO_FOR_ALL_EVENTS
NEAR_CROSSING_GAP_THRESHOLD
ZERO_GRADE_PATH_PURITY_CORRECTION
RAW_EIGENVECTOR_NONZERO_COUNT_ORACLE
```

---

## Règle de challenge pour la clôture et l'implémentation

Claude Code conserve un rôle de revue critique. Il n'est pas un simple exécutant.

Toute objection est classée :

```text
BLOCKING
    contradiction démontrée
    erreur mathématique / numérique affectant le protocole
    définition inexécutable
    défaut pouvant modifier un verdict scientifique

NON_BLOCKING_BACKLOG
    amélioration
    généralisation
    nouvelle observable
    preuve ou optimisation non nécessaire à la validité de 0B

REJECTED
    objection incorrecte, non démontrée ou hors périmètre
```

Principe du lot :

```text
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_NEW_CONCEPTUAL_BRANCHING_WITHOUT_BLOCKING_DEFECT
```

Une objection `BLOCKING` stoppe le lot concerné et retourne à l'arbitrage conceptuel. Un élément `NON_BLOCKING_BACKLOG` ne rouvre pas 0B.

---

## Lot courant

```text
CURRENT_LOT = Toy Model 0B pre-freeze consolidation
PHASE       = DOCUMENT CONSOLIDATION / CLOSURE PREPARATION
```

Travail autorisé :

```text
- consolidation des décisions déjà arbitrées ;
- suppression des faux OPEN et contradictions documentaires ;
- audit critique read-only de clôture ;
- fermeture en un lot des contrôles numériques réellement OPEN ;
- revue finale de cohérence / syntaxe.
```

Travail non autorisé sans défaut `BLOCKING` :

```text
- nouvelle famille d'observables ;
- nouvelle extension du modèle ;
- nouvelle campagne scientifique ;
- nouveau mécanisme physique non nécessaire au protocole courant ;
- implémentation 0B.
```

---

## Prochaine action autorisée

```text
NEXT_STEP = intégrer l'index pré-gel dans specification.md et validation-plan.md,
            puis lancer un audit critique read-only de clôture.
```

L'audit Claude Code doit chercher des contradictions, erreurs, ambiguïtés bloquantes ou définitions inexécutables. Les améliorations non bloquantes vont au backlog.

`IMPLEMENTATION_0B` reste `NOT_AUTHORIZED` tant que le paquet n'est pas gelé explicitement par Lionel ORCIL.
