# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11 et porte le statut opérationnel courant du projet.

## Git

```text
ACTIVE_BRANCH = documentation/model0b-foundation
BASE_COMMIT   = 08d5ca506ff05e15dd9bc084ea121c3d0a19b662
```

La base est le merge canonique de clôture du Toy Model 0A. Aucun code 0B n'est autorisé dans le lot courant.

---

## État global

```text
TOY_MODEL_0A                    = CLOSED
TESTS_0A                        = 89 PASS

MODEL0B_SPECIFICATION           = CONSOLIDATED / ERRATA PENDING INTEGRATION
MODEL0B_VALIDATION_PLAN         = CONSOLIDATED / ERRATA PENDING INTEGRATION
MODEL0B_CLOSURE_AUDIT           = BLOCKED (5 consolidation defects)
MODEL0B_CLOSURE_ERRATA          = DEFINED 5/5
MODEL0B_NUMERICAL_CONTROLS      = OPEN
MODEL0B_FINAL_ACCEPTANCE_RULES  = OPEN
IMPLEMENTATION_0B               = NOT_AUTHORIZED

SCIENTIFIC_METHOD_GOVERNANCE    = DRAFT_IN_FEATURES
```

Sources scientifiques consolidées :

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
```

Correctif normatif temporaire issu de l'audit de clôture :

```text
docs/toy-models/toy0b/closure-audit-errata.md
```

Jusqu'à intégration mécanique des cinq corrections dans les deux sources consolidées, `closure-audit-errata.md` supersède explicitement toute formulation contradictoire sur ces cinq points seulement.

Les autres supports spécialisés de `docs/toy-models/toy0b/` conservent les preuves et qualifications détaillées ; ils ne sont pas un contexte obligatoire lorsque les sources consolidées et l'errata suffisent.

---

## Blocs scientifiques ayant résisté à l'audit indépendant

```text
SYSTEM_AND_GAUSS           = VALIDATED_FOR_FREEZE
TRUNCATION_STRUCTURE       = VALIDATED_FOR_FREEZE
STATIC_OBSERVABLES         = VALIDATED_FOR_FREEZE
STATIC_IDENTIFIABILITY     = VALIDATED_FOR_FREEZE
DECLARED_SYMMETRIES        = VALIDATED_FOR_FREEZE
NULL_ORACLES               = VALIDATED_FOR_FREEZE
KUBO_PROBE                 = VALIDATED_FOR_FREEZE
PRIMARY_SIGNAL_DELTA1      = VALIDATED_FOR_FREEZE
PATH_GRADING               = VALIDATED_FOR_FREEZE
RECURRENCE_STRUCTURE       = VALIDATED_FOR_FREEZE
SHORT_TIME_STRUCTURE       = VALIDATED_FOR_FREEZE
SPECTRAL_TIME_STRUCTURE    = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
SOFT_LOOP_STRUCTURE        = VALIDATED_FOR_FREEZE
PARAMETER_CAMPAIGN_SHAPE   = VALIDATED_FOR_FREEZE
```

L'audit n'a pas établi de défaut physique bloquant dans ces blocs. `VALIDATED_FOR_FREEZE` ne vaut pas `FROZEN`.

---

## Les cinq défauts de consolidation et leur correction

```text
B1 MEASUREMENT_FAMILIES
    F_edge / F_path / M_F et convention modulo identité incomplets
    -> correction définie dans closure-audit-errata.md §E1

B2 PATH_PURITY_GUARD
    I_max absolu avait remplacé à tort R_path normalisé
    -> correction définie §E2

B3 RECURRENCE_GUARD
    horizon / états / deux bornes perdus ; ancien rectangle Gamma conflictuel
    -> correction définie §E3 ; domaine ordonné retenu

B4 INTERIOR_DIMENSION_DOMAIN
    forme fermée utilisée hors domaine à Lambda=1
    -> correction définie §E4

B5 STATUS_VOCABULARY
    liste de verdicts présentée à tort comme exhaustive
    -> correction définie §E5
```

Le verdict original reste :

```text
CLOSURE_AUDIT = BLOCKED
```

jusqu'à une future vérification indépendante. Aucun nouvel audit Claude n'est demandé dans le lot courant.

---

## Invariants 0B

```text
TOPOLOGY                  = 6-cycle
BACKGROUND                = (0,1,0,1,0,1)
REFERENCE_TRUNCATION      = Lambda=2
TRUNCATION_CHECK          = Lambda=3
PILOT_TRUNCATION          = Lambda=1
PHYSICAL_DIMENSION        = 40*Lambda - 2 for Lambda>=1
REFERENCE_HAMILTONIAN     = H(g=1,mu=0,delta=0), J=1
PRIMARY_PROPAGATION_PROBE = Kubo density-density
PRIMARY_TIME_ESTIMATOR    = T_grow
SECONDARY_TIME_FAMILY     = T_thr(eta)
PRIMARY_RELATIONAL_SIGNAL = Delta1
GLOBAL_NULL_ORACLE        = Delta2 == 0
```

La réciprocité `chi_pq(t)=chi_qp(t)` ferme le problème d'orientation source-récepteur.

---

## Campagne consolidée

MAIN :

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

Contrôles séparés :

```text
g=0,mu=0  = pure-hopping oracle
g=0.10    = weak-g stress outside nominal domain
delta=0.9 = disclosed qualification/stress outside nominal domain
```

SOFT-LOOP :

```text
g  = 1
mu = {-1.25, -1.5, -2}
```

---

## Architecture temporelle consolidée

```text
TIME_GRID_AS_FINAL_ESTIMATOR       = REJECTED
FINITE_DIFFERENCE_TIME_DERIVATIVE  = REJECTED
NUMERICAL_QUADRATURE_FOR_P_ALPHA   = NOT_NOMINAL
```

Fonctions résolues :

```text
T_peak      -> première racine qualifiante de chi'=0
T_thr/down  -> chi-s*2*sqrt(eta)=0 sur le premier lobe
T_grow      -> candidats H_grow=chi'^2+chi*chi''=0
```

Une seule famille de raffinement `B={beta_k}` est conservée, avec :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

Les valeurs numériques restent ouvertes.

---

## Paramètres réellement OPEN avant gel

```text
# temporal / precision
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

# threshold / interpretation
ETA_GRID_AND_ADMISSIBLE_DOMAIN
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE
EPS_PATH_CONTROL_DOMAIN_AND_GRID
GAMMA_CONTROL_DOMAIN_AND_GRID
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS

# campaign / cutoff
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

## Règle de challenge

```text
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_NEW_CONCEPTUAL_BRANCHING_WITHOUT_BLOCKING_DEFECT
```

Classification :

```text
BLOCKING
    contradiction démontrée, erreur affectant la validité,
    définition inexécutable ou défaut pouvant modifier un verdict

NON_BLOCKING_BACKLOG
    amélioration / généralisation non nécessaire à la validité de 0B

REJECTED
    objection fausse, non démontrée ou hors périmètre
```

Les éléments `NON_BLOCKING_BACKLOG` de l'audit de clôture ne sont pas développés dans le lot courant.

---

## Pause méthodologique

La consommation de contexte / quota observée lors de l'audit de clôture rend le workflow actuel non soutenable.

En conséquence :

```text
CURRENT_LOT = workflow methodology redesign
PHASE       = PAUSE_0B_SCIENTIFIC_WORK
NEXT_STEP   = define a lower-context ChatGPT / Claude / GitHub workflow
```

Pendant cette pause :

```text
NO_NEW_CLAUDE_AUDIT       = TRUE
NO_0B_IMPLEMENTATION       = TRUE
NO_NEW_0B_PHYSICS_BRANCH   = TRUE
```

La prochaine reprise de 0B devra partir du dépôt comme mémoire durable et d'un mandat minimal ciblé, pas d'un prompt reconstruisant tout l'historique de conversation.