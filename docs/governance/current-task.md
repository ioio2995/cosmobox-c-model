# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11 et porte le statut opérationnel courant du projet.

## Git

```text
ACTIVE_BRANCH = implementation/model0b
BASE_COMMIT   = 08d5ca506ff05e15dd9bc084ea121c3d0a19b662
ERRATA_COMMIT = d00d146
GOVERNANCE_EXECUTION_PREFLIGHT = dec669d90fc01bc998e53ef8cec2bac7a93f5679
IMPLEMENTATION_BRANCH_BASE_COMMIT = 42f0b1a01204859b30a332ff7a6b9c5a6bdeb815
```

L'implémentation de Model 0B n'est autorisée que par lots bornés sur
`implementation/model0b`. La spécification/le protocole scientifique gelé
reste immuable. L'exécution confirmatoire reste séparément
`NOT_AUTHORIZED`.

---

## État global

```text
TOY_MODEL_0A                    = CLOSED
TESTS_0A                        = 89 PASS

MODEL0B_SPECIFICATION           = CONSOLIDATED / ERRATA INTEGRATED
MODEL0B_VALIDATION_PLAN         = CONSOLIDATED / ERRATA INTEGRATED
MODEL0B_CLOSURE_AUDIT_ORIGINAL  = BLOCKED (5 consolidation defects)
MODEL0B_CLOSURE_ERRATA          = INTEGRATED 5/5 @ d00d146
MODEL0B_ERRATA_DIFF_REVIEW      = PASS 5/5
MODEL0B_NUMERICAL_CONTROLS      = CLOSED
MODEL0B_FINAL_ACCEPTANCE_RULES  = VALIDATED_FOR_FREEZE
MODEL0B_CLOSURE_REVIEW          = PASS
MODEL0B_FREEZE_READINESS        = COMPLETED_BY_EXPLICIT_FREEZE_DECISION
MODEL0B_STATUS                  = FROZEN
MODEL0B_FREEZE_DECISION         = EXPLICITLY_APPROVED
MODEL0B_FREEZE_DECISION_DATE    = 2026-08-24
MODEL0B_FREEZE_BASE_COMMIT      = d796c65d2538eaba2be7882647ba91db5cf93a32
MODEL0B_FREEZE_RECORD           = docs/toy-models/toy0b/freeze-record.md
MODEL0B_FREEZE_DOES_NOT_AUTHORIZE_IMPLEMENTATION = YES
IMPLEMENTATION_0B               = AUTHORIZED
IMPLEMENTATION_0B_AUTHORIZATION      = EXPLICITLY_APPROVED
IMPLEMENTATION_0B_AUTHORIZATION_DATE = 2026-08-24
IMPLEMENTATION_BRANCH                = implementation/model0b
IMPLEMENTATION_BRANCH_BASE_COMMIT    = 42f0b1a01204859b30a332ff7a6b9c5a6bdeb815
CONFIRMATORY_EXECUTION_0B            = NOT_AUTHORIZED

SCIENTIFIC_METHOD_GOVERNANCE    = DRAFT_IN_FEATURES
```

Les cinq défauts B1-B5 de l'audit de clôture ont été intégrés dans les sources principales et les supports concernés, puis revus indépendamment en lecture seule avec verdict `PASS` pour E1-E5. Le verdict historique de l'audit reste conservé comme trace ; les cinq blocages qu'il avait établis sont considérés corrigés.

Sources principales :

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
```

Trace d'audit :

```text
docs/toy-models/toy0b/closure-audit-errata.md
```

---

## Blocs scientifiques stabilisés

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
PATH_PURITY_STRUCTURE      = VALIDATED_FOR_FREEZE
RECURRENCE_STRUCTURE       = VALIDATED_FOR_FREEZE
SHORT_TIME_STRUCTURE       = VALIDATED_FOR_FREEZE
SPECTRAL_TIME_STRUCTURE    = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
SOFT_LOOP_STRUCTURE        = VALIDATED_FOR_FREEZE
PARAMETER_CAMPAIGN_SHAPE   = VALIDATED_FOR_FREEZE
```

`VALIDATED_FOR_FREEZE` ne vaut pas `FROZEN`.

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
g=0,mu=0   = pure-hopping oracle
g=0.10     = weak-g stress outside nominal domain
delta=0.9  = disclosed qualification/stress outside nominal domain
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

Facteurs de bande :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

Décision scientifique validée et intégrée :

```text
BETA_REFINEMENT_VALUES = VALIDATED_FOR_FREEZE
BETA_VALUES = {1, 1/2, 1/4, 1/8}
BETA_COMMIT = 1b37a96b832f45549bc24e41347a46e68d172db0
```

`beta` contrôle le bracketing initial, pas la précision finale du temps continu.

---

## Contrôles numériques fermés — lot de fermeture mécanique

```text
# temporal / spectral / simple roots
ROOT_SOLVER_TOLERANCES                = VALIDATED_FOR_FREEZE
SPECTRAL_PRECISION_CONTROL             = VALIDATED_FOR_FREEZE
SIMPLE_ROOT_CONTROL                    = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCES                     = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCE                      = 1e-10

# Delta1 error budget
DELTA1_PROPAGATED_ERROR_BUDGET          = VALIDATED_FOR_FREEZE

# SOFT-LOOP / derivative
A_DELTA_VALUES                          = VALIDATED_FOR_FREEZE
DERIVATIVE_STABILITY_CRITERION          = VALIDATED_FOR_FREEZE
RICHARDSON_USAGE_RULE                   = VALIDATED_FOR_FREEZE

# degenerate root fail-closed control
DEGENERATE_ROOT_CONTROL                 = VALIDATED_FOR_FREEZE
DEGENERATE_ROOT_NEW_TOLERANCE           = NONE

# SOFT-LOOP static x grid
STATIC_X_CONTROL_VALUES                 = VALIDATED_FOR_FREEZE
STATIC_X_PRIMARY                        = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES  = {1/4, 1/2, 1, 2}
STATIC_X_SATURATION_DIAGNOSTIC          = {±4}

# SOFT-LOOP static collapse numerical criterion
STATIC_COLLAPSE_NUMERICAL_CRITERION     = VALIDATED_FOR_FREEZE
STATIC_COLLAPSE_TOLERANCE               = 0.10
STATIC_COLLAPSE_NORM                    = POINTWISE_L_INFINITY
STATIC_LAMBDA3_INFORMATION_GUARD        = REQUIRED
STATIC_LAMBDA3_MIN_DISCRIMINATING_MAGNITUDE = 1

# threshold eta grid and admissibility
ETA_GRID_AND_ADMISSIBLE_DOMAIN          = VALIDATED_FOR_FREEZE
THRESHOLD_GLOBAL_F_MAX                  = 1/16
LAMBDA_ETA_VALUES                       = {2^-2,2^-4,2^-6,2^-8,2^-10,2^-12,2^-14,2^-16}
ETA_VALUES                              = {2^-6,2^-10,2^-14,2^-18,2^-22,2^-26,2^-30,2^-34}
THRESHOLD_RELATIVE_TIME_GUARD           = REQUIRED

# short-time threshold convergence rule
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE       = VALIDATED_FOR_FREEZE
SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS    = 3
SHORT_TIME_CONVERGENCE_MAX_PREREGISTERED_NU = 5
SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY     = YES
SHORT_TIME_CONVERGENCE_NEW_SCALAR_TOLERANCE = NONE

# path purity control domain and grid
EPS_PATH_CONTROL_DOMAIN_AND_GRID            = VALIDATED_FOR_FREEZE
EPS_PATH_VALUES                             = {1/32,1/16,1/8,1/4}
EPS_PATH_STRICT                             = 1/32
EPS_PATH_PERMISSIVE                         = 1/4
PATH_CERTIFICATION_OSCILLATORY_FACTOR       = 4
PATH_CONTROL_NEW_SCALAR_NUMERICAL_TOLERANCE = NONE

# recurrence gamma control domain and grid
GAMMA_CONTROL_DOMAIN_AND_GRID   = VALIDATED_FOR_FREEZE
GAMMA_VALUES                    = {(1/8,7/8),(1/4,3/4),(3/8,5/8)}
GAMMA_STRICT                    = (1/8,7/8)
GAMMA_PERMISSIVE                = (3/8,5/8)
GAMMA_GRID_TYPE                 = THREE_POINT_ORDERED_CHAIN

# recurrence hysteresis numerical bounds
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS       = VALIDATED_FOR_FREEZE
RECURRENCE_CERTIFICATION_OSCILLATORY_FACTOR  = 1
RECURRENCE_ROOT_TOLERANCE                    = EXISTING_TAU_ROOT
RECURRENCE_EVENT_TOLERANCE                   = EXISTING_TAU_EVENT
RECURRENCE_HYSTERESIS_NEW_SCALAR_TOLERANCE   = NONE
RECURRENCE_TGROW_PRIMARY_HORIZON             = T_peak

# negative delta MAIN covariance oracle
NEGATIVE_DELTA_ORACLE_SUBSET                 = VALIDATED_FOR_FREEZE
NEGATIVE_DELTA_ORACLE_BASE_SIZE               = 17
NEGATIVE_DELTA_ORACLE_BRANCH_COVERAGE_RULE    = REQUIRED
NEGATIVE_DELTA_ORACLE_TOTAL_SIZE              = DERIVED_BOUNDED_17_TO_120
NEGATIVE_DELTA_ORACLE_INDEPENDENT_RECOMPUTATION = REQUIRED
NEGATIVE_DELTA_ORACLE_NEW_SCALAR_TOLERANCE    = NONE

# truncation Lambda=2/3 stress point subset
TRUNCATION_STRESS_POINT_SUBSET                = VALIDATED_FOR_FREEZE
TRUNCATION_STRESS_POINT_SUBSET_SIZE           = 18
TRUNCATION_STRESS_MAIN_POINT_COUNT            = 16
TRUNCATION_STRESS_OUTER_POINT_COUNT           = 2
TRUNCATION_STRESS_POSTHOC_SUBSTITUTION        = FORBIDDEN
TRUNCATION_STRESS_NEW_SCALAR_TOLERANCE        = NONE

# truncation Lambda=2/3 comparison tolerances
TRUNCATION_COMPARISON_TOLERANCES              = VALIDATED_FOR_FREEZE
TRUNCATION_TOLERANCE_VALUES                   = {0.01,0.02,0.05}
TRUNCATION_DELTA1_DUAL_METRIC                 = REQUIRED_FOR_FINITE_DELTA_PRIMARY_SIGNAL
TRUNCATION_ETA_ADMISSIBILITY_COMPARISON_STAGE = BEFORE_COMMON_INTERSECTION
TRUNCATION_REFERENCE_GATE                     = ROBUST_STABLE_REQUIRED
TRUNCATION_NEW_FLOATING_POINT_TOLERANCE       = NONE

# estimator coherence criterion
ESTIMATOR_COHERENCE_CRITERION                 = VALIDATED_FOR_FREEZE
ESTIMATOR_COHERENCE_OBJECT                    = DELTA1_RELATIONAL_ORDERING
ESTIMATOR_MAGNITUDE_EQUALITY_GATE             = REJECTED
ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL = YES
ESTIMATOR_COHERENCE_CARDINALITY_DIAGNOSTICS   = MANDATORY_PUBLICATION
ESTIMATOR_COHERENCE_NEW_SCALAR_TOLERANCE      = NONE

# numerical zero and symmetry tolerances (last major numerical control)
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES        = VALIDATED_FOR_FREEZE
ZERO_SYMMETRY_TOLERANCE_VALUES                = {1e-9,3e-9,1e-8}
ZERO_SYMMETRY_RESIDUAL_FORM_REGISTRY          = REQUIRED_AND_DETERMINISTIC_BEFORE_EXECUTION
NUMERICAL_ZERO_BRANCH_IS_CERTIFIED            = NO
NUMERICAL_ZERO_SINGULAR_VALUE_CREATES_EXACT_KERNEL = NO
ZERO_SYMMETRY_INDEPENDENT_EVIDENCE_RULE       = SATISFIED_BY_CONSTRUCTION_DOES_NOT_COUNT_AS_PASS_EVIDENCE
ZERO_SYMMETRY_ORACLE_FAMILY_NONVACUITY_RULE   = AT_LEAST_ONE_APPLICABLE_INDEPENDENT_ROBUST_PASS_REQUIRED

# final acceptance rules (closes MODEL0B closure review)
MODEL0B_FINAL_ACCEPTANCE_RULES                = VALIDATED_FOR_FREEZE
MODEL0B_FINAL_ACCEPTANCE_MODE                 = CLAIM_SCOPED_FAIL_CLOSED_DEPENDENCY_CLOSURE
DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY       = CLAIM_RANK_PRIMARY
DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY       = CLAIM_RANK_STRONGER_OPTIONAL
XI1_CONFIRMATORY_SCOPE                        = SOFT_LOOP_ONLY
```

Définition normative complète : `docs/toy-models/toy0b/numerical-zero-symmetry-control.md`, `docs/toy-models/toy0b/final-acceptance-rules.md`.

---

## Clôture finale d'acceptation — arbitrage Opus (BL1/BL2/BL3)

```text
MODEL0B_CLOSURE_REVIEW = PASS
```

Le dernier audit de clôture Opus a retourné `MODEL0B_CLOSURE_REVIEW =
BLOCKED` avec trois blocages `BL1`, `BL2`, `BL3`. ChatGPT a arbitré les
trois blocages `ACCEPTED` ; aucun second appel Opus n'a été requis (BL1 =
couche de méta-statut manquante déjà identifiée par Opus ; BL2 = scission en
deux rangs de revendication déjà proposée par Opus, utilisant la sémantique
chemin/récurrence déjà gelée ; BL3 = synchronisation de formulations `OPEN`
obsolètes contre la spécification consolidée déjà normative, pas un nouveau
contenu scientifique).

```text
BL1 = ACCEPTED_AND_INTEGRATED   -> docs/toy-models/toy0b/final-acceptance-rules.md §2
BL2 = ACCEPTED_AND_INTEGRATED   -> docs/toy-models/toy0b/final-acceptance-rules.md §4-§6
BL3 = ACCEPTED_AND_INTEGRATED   -> synchronisation OPEN obsolète (12 fichiers)
```

---

## Clôture des contrôles numériques majeurs

```text
CLOSED_MAJOR_CONTROLS = 21
OPEN_MAJOR_CONTROLS   = 0
```

`OPEN_MAJOR_CONTROLS = 0` signifie que tous les paramètres numériques majeurs
préenregistrés de Toy Model 0B sont fermés. Le modèle est désormais gelé par
décision explicite de Lionel ORCIL (`MODEL0B_STATUS = FROZEN` ci-dessous),
mais cela ne signifie pas que tous les statuts spécialisés/backlog du dépôt
sont clos.

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
OUTSIDE_MAJOR_CONTROL_COUNT     = YES
```

Ce paramètre reste explicitement `OPEN` et hors du décompte des contrôles
numériques majeurs ; il ne bloque pas la préparation au gel
(`final-acceptance-rules.md` §11) et devra être surfacé lors du futur audit
de clôture du modèle.

Tous ces éléments ont été validés scientifiquement et intégrés
documentairement. Le modèle est désormais `FROZEN` par décision explicite de
Lionel ORCIL (`MODEL0B_FREEZE_DECISION_DATE = 2026-08-24`), cf.
`docs/toy-models/toy0b/freeze-record.md`.

---

## Paramètres encore OPEN avant gel

```text
# verdicts
(aucun paramètre numérique majeur préenregistré encore OPEN)
```

Tous les paramètres numériques majeurs préenregistrés de Toy Model 0B sont
désormais `VALIDATED_FOR_FREEZE` (`OPEN_MAJOR_CONTROLS = 0`, cf.
« Clôture des contrôles numériques majeurs » ci-dessus). Ceci n'inclut pas
`GROUPED_SPECTRAL_SUPPORT_ORACLE`, qui reste `OPEN_PENDING_SYMMETRY_DERIVATION`
et hors de ce décompte, ni `MODEL0B_FINAL_ACCEPTANCE_RULES`.

---

## Workflow Claude Code courant

La gouvernance de collaboration impose un préflight explicite et un profil d'exécution déclaré pour chaque mandat.

Profils disponibles (cf. `docs/governance/collaboration-governance.md` §12) :

```text
DOCUMENTATION                    = CLAUDE_SONNET_5 / AUTO
REVIEW_OR_ENGINEERING            = CLAUDE_SONNET_5 / AUTO
SCIENTIFIC_ESCALATION            = CLAUDE_OPUS_5 / AUTO
SCIENTIFIC_HARD_BLOCKING         = CLAUDE_OPUS_5 / HIGH
```

Sonnet 5 est désormais le modèle de production standard pour toute documentation versionnée ainsi que pour l'ingénierie courante. Haiku est retiré du workflow versionné Cosmobox. Opus reste une escalade explicite et ciblée pour la contre-expertise scientifique et les blocages scientifiques, jamais un modèle de production par défaut.

Principe :

```text
VERSIONED_PRODUCTION_MODEL = CLAUDE_SONNET_5
HAIKU_FOR_VERSIONED_PRODUCTION = NOT_USED
MODEL_ESCALATION_ABOVE_SONNET = EXPLICIT
```

Chaque mandat déclare aussi :

```text
REPOSITORY
REMOTE
BRANCH
EXPECTED_HEAD
EXPECTED_WORKTREE
```

Autre principe :

```text
ONE_TASK = ONE_BOUNDED_SCOPE
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_GLOBAL_AUDIT_BY_DEFAULT
```

Une objection est classée :

```text
BLOCKING
NON_BLOCKING_BACKLOG
REJECTED
```

Une objection `BLOCKING` peut arrêter le lot. Un élément `NON_BLOCKING_BACKLOG` ne rouvre pas le périmètre courant.

---

## Lot courant

```text
CURRENT_LOT = Toy Model 0B freeze record
PHASE       = MODEL0B_FROZEN
CURRENT_PARAMETER = NONE_MODEL_FROZEN
OPEN_MAJOR_CONTROLS = 0
CLOSED_MAJOR_CONTROLS = 21
MODEL0B_CLOSURE_REVIEW = PASS
MODEL0B_FINAL_ACCEPTANCE_RULES = VALIDATED_FOR_FREEZE
MODEL0B_FINAL_ACCEPTANCE_MODE = CLAIM_SCOPED_FAIL_CLOSED_DEPENDENCY_CLOSURE
MODEL0B_FREEZE_READINESS = COMPLETED_BY_EXPLICIT_FREEZE_DECISION
MODEL0B_STATUS = FROZEN
MODEL0B_FREEZE_DECISION = EXPLICITLY_APPROVED
MODEL0B_FREEZE_DECISION_DATE = 2026-08-24
MODEL0B_FREEZE_BASE_COMMIT = d796c65d2538eaba2be7882647ba91db5cf93a32
MODEL0B_FREEZE_RECORD = docs/toy-models/toy0b/freeze-record.md
MODEL0B_FREEZE_DOES_NOT_AUTHORIZE_IMPLEMENTATION = YES
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
XI1_CONFIRMATORY_SCOPE = SOFT_LOOP_ONLY
IMPLEMENTATION_0B = AUTHORIZED
IMPLEMENTATION_0B_AUTHORIZATION = EXPLICITLY_APPROVED
IMPLEMENTATION_0B_AUTHORIZATION_DATE = 2026-08-24
IMPLEMENTATION_BRANCH = implementation/model0b
IMPLEMENTATION_BRANCH_BASE_COMMIT = 42f0b1a01204859b30a332ff7a6b9c5a6bdeb815
CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED
NEXT_REQUIRED_GOVERNANCE_ACTION = CHATGPT_REVIEW_PERF2_THEN_LIONEL_DECISION
```

**État** : vingt-et-un paramètres numériques majeurs sont fermés et intégrés
documentairement (ROOT_SOLVER_TOLERANCES, SPECTRAL_PRECISION_CONTROL,
SIMPLE_ROOT_CONTROL, ARGMAX_TOLERANCES, DELTA1_PROPAGATED_ERROR_BUDGET,
A_DELTA_VALUES, DERIVATIVE_STABILITY_CRITERION, RICHARDSON_USAGE_RULE,
DEGENERATE_ROOT_CONTROL, STATIC_X_CONTROL_VALUES,
STATIC_COLLAPSE_NUMERICAL_CRITERION, ETA_GRID_AND_ADMISSIBLE_DOMAIN,
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE, EPS_PATH_CONTROL_DOMAIN_AND_GRID,
GAMMA_CONTROL_DOMAIN_AND_GRID, RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS,
NEGATIVE_DELTA_ORACLE_SUBSET, TRUNCATION_STRESS_POINT_SUBSET,
TRUNCATION_COMPARISON_TOLERANCES, ESTIMATOR_COHERENCE_CRITERION,
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES). En complément,
`MODEL0B_FINAL_ACCEPTANCE_RULES = VALIDATED_FOR_FREEZE` ferme le mode
d'acceptation finale des revendications scientifiques (`final-acceptance-rules.md`),
suite à l'arbitrage ChatGPT `ACCEPTED` des trois blocages `BL1`/`BL2`/`BL3` de
la dernière revue de clôture Opus (`MODEL0B_CLOSURE_REVIEW = PASS`, cf.
« Clôture finale d'acceptation — arbitrage Opus » ci-dessus).

Le modèle est désormais `FROZEN` par décision explicite de Lionel ORCIL
(`MODEL0B_FREEZE_DECISION = EXPLICITLY_APPROVED`,
`MODEL0B_FREEZE_DECISION_DATE = 2026-08-24`,
`MODEL0B_FREEZE_BASE_COMMIT = d796c65d2538eaba2be7882647ba91db5cf93a32`),
cf. `docs/toy-models/toy0b/freeze-record.md`. `GROUPED_SPECTRAL_SUPPORT_ORACLE`
reste `OPEN_PENDING_SYMMETRY_DERIVATION` (hors décompte des contrôles majeurs,
`GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG`) : le gel
n'implique ni exécution de la campagne confirmatoire, ni autorisation
d'implémentation (`MODEL0B_FREEZE_DOES_NOT_AUTHORIZE_IMPLEMENTATION = YES`).

**Prochaine action** : la décision d'autorisation d'implémentation séparée a
depuis été explicitement approuvée par Lionel ORCIL
(`IMPLEMENTATION_0B_AUTHORIZATION_DATE = 2026-08-24`) ; cf. « Rôle spécialisé
cosmobox-code » ci-dessous pour l'état courant de l'implémentation bornée sur
`implementation/model0b`.

---

## Rôle spécialisé cosmobox-code

```text
COSMOBOX_CODE_AGENT       = AVAILABLE
COSMOBOX_CODE_PROTOCOL    = COSMOBOX_CODE_PROTOCOL_V1
COSMOBOX_CODE_GOVERNANCE  = docs/governance/agents/cosmobox-code-governance.md
COSMOBOX_CODE_NOMINAL_MODEL = CLAUDE_SONNET_5
```

```text
MODEL0B_STATUS       = FROZEN
IMPLEMENTATION_0B    = AUTHORIZED
IMPLEMENTATION_0B_AUTHORIZATION      = EXPLICITLY_APPROVED
IMPLEMENTATION_0B_AUTHORIZATION_DATE = 2026-08-24
IMPLEMENTATION_BRANCH                = implementation/model0b
IMPLEMENTATION_BRANCH_BASE_COMMIT    = 42f0b1a01204859b30a332ff7a6b9c5a6bdeb815
CONFIRMATORY_EXECUTION_0B            = NOT_AUTHORIZED
```

```text
I1_A_STATUS = ACCEPTED
I1_A_ACCEPTED_HEAD = 2a255529ce6cdbffe124cf46f1c04a43ac75dfab
I1_A_TEST_FILENAME_RATIFICATION = ACCEPTED_EXCEPTION_NO_PRECEDENT
I1_A_RATIFIED_TEST_FILE = tests/models/model0b/test_basis_and_gauss_model0b.py
```

Lionel ORCIL a explicitement accepté le lot I1-A (`I1_A_STATUS = ACCEPTED`,
`I1_A_ACCEPTED_HEAD = 2a255529ce6cdbffe124cf46f1c04a43ac75dfab`) ainsi que
l'exception ponctuelle de nom de fichier de test qu'il avait rendue
nécessaire (`I1_A_TEST_FILENAME_RATIFICATION = ACCEPTED_EXCEPTION_NO_PRECEDENT`) :
cette exception ne crée aucun précédent (`NONE`). Règle préservée pour les
lots futurs : si un chemin exact autorisé doit changer, `cosmobox-code`
doit s'arrêter et demander un arbitrage de périmètre avant d'appliquer un
chemin alternatif.

```text
I1_B_STATUS = ACCEPTED
I1_B_ACCEPTED_HEAD = 1d149361184b4e678cea206bc3982932e1ab6b05
```

Lionel ORCIL a explicitement accepté le lot I1-B (`I1_B_STATUS = ACCEPTED`,
`I1_B_ACCEPTED_HEAD = 1d149361184b4e678cea206bc3982932e1ab6b05`).

```text
I1_C_STATUS = ACCEPTED
I1_C_ACCEPTED_HEAD = 13400aa598ab1d56cab048b7138a23dfb21a8f83
```

Lionel ORCIL a explicitement accepté le lot I1-C (`I1_C_STATUS = ACCEPTED`,
`I1_C_ACCEPTED_HEAD = 13400aa598ab1d56cab048b7138a23dfb21a8f83`).

```text
CURRENT_LOT = Toy Model 0B I2-A P0 eigensystem and numerical ground cluster
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-A
I2_A_SCOPE  = P0_EIGENSYSTEM_BACKWARD_GATE_AND_NUMERICAL_CLUSTER
I2_A_STATUS = IMPLEMENTED_PENDING_REVIEW
I2_A_PRECISION_SCOPE = P0_BINARY64_ONLY
P1_P2_PRECISION_CONTROL = NOT_IMPLEMENTED
I2_A_CONFIRMATORY_ROLE = NONE
I2_A_REVIEW = CORRECTION_REQUIRED_TEST_TOLERANCE_ONLY
I2_A_C1_SCOPE = STRICT_PROJECTOR_TEST_TOLERANCES
I2_A_C1_STATUS = ACCEPTED
I2_A_C1_PRODUCTION_DIFF = NONE
I2_A_STATUS = ACCEPTED
I2_A_ACCEPTED_HEAD = 19d3c7c2473c371cee05f67188889702c1f7ad4b
```

Correction I2-A-C1 : les assertions de test liées aux projecteurs
(`tests/models/model0b/test_eigensystem_model0b.py`) utilisent désormais des
tolérances strictement bornées par `PROJECTOR_STABILITY_TOLERANCE = 1e-10`
(`rtol=0.0` / `rel=0.0` explicite, ou égalité exacte lorsque la valeur
attendue est déterministe bit-à-bit). Défaut de test uniquement ; aucun
changement de production
(`I2_A_C1_PRODUCTION_DIFF = NONE`,
`src/cosmobox_c_model/models/model0b/eigensystem.py` inchangé). Lionel ORCIL
a explicitement accepté I2-A et I2-A-C1
(`I2_A_STATUS = ACCEPTED`, `I2_A_ACCEPTED_HEAD = 19d3c7c2473c371cee05f67188889702c1f7ad4b`).

```text
I2_B_AUDIT = PASS
I2_B_AUDIT_REPOSITORY_DIFF = NONE
I2_B_BACKEND_DECISION = MPMATH
I2_B_BACKEND_VERSION_RANGE = mpmath>=1.4.1,<1.5
I2_B_EXACT_PARAMETER_REPRESENTATION = fractions.Fraction
```

L'audit I2-B-AUDIT (lecture seule, aucune modification versionnée) a
recommandé `mpmath` comme backend multi-précision (échec architectural de
`python-flint`/Arb : `acb_mat.eig()` ne peut pas retourner de vecteurs
propres sous valeurs propres multiples, incompatible avec l'exigence gelée
de projecteurs de cluster). Décision confirmée par revue indépendante
ChatGPT (`BACKEND_DECISION_BASIS = I2-B-AUDIT + ChatGPT independent API
review`).

```text
I2_B1_STATUS = ACCEPTED
I2_B1_ACCEPTED_HEAD = 1e80f8093f3f802e3f0a36fb5f41350d21af6ede
I2_B1_C1_STATUS = ACCEPTED
```

Lionel ORCIL a explicitement accepté le lot I2-B1 (`I2_B1_STATUS = ACCEPTED`,
`I2_B1_ACCEPTED_HEAD = 1e80f8093f3f802e3f0a36fb5f41350d21af6ede`) ainsi que la
correction de gouvernance I2-B1-C1 (`I2_B1_C1_STATUS = ACCEPTED`).

```text
CURRENT_LOT = Toy Model 0B I2-B2-A multiprecision eigensystem per precision level
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-B2-A
I2_B2_A_SCOPE = P1_P2_SINGLE_LEVEL_EIGENSYSTEM_BACKWARD_GATE_AND_CLUSTERS
I2_B2_A_STATUS = ACCEPTED
I2_B2_A_ACCEPTED_HEAD = b7bb94706548514d31c4fbf3527b5d6f48e30f2e
CROSS_PRECISION_CLUSTER_MATCHING = NOT_IMPLEMENTED
D_P = NOT_IMPLEMENTED
PRECISION_ROUTING = NOT_IMPLEMENTED
I2_B2_A_REVIEW = CORRECTION_REQUIRED_IMPORT_TIME_THRESHOLD_PRECISION
I2_B2_A_C1_SCOPE = PRECISION_LOCAL_FROZEN_THRESHOLDS
I2_B2_A_C1_STATUS = ACCEPTED
I2_B2_A_C1_THRESHOLD_VALUES_CHANGED = NO
```

Correction I2-B2-A-C1 : les seuils gelés (`BACKWARD_RESIDUAL_TOLERANCE`,
`BACKWARD_ORTHOGONALITY_TOLERANCE`, `PROJECTOR_STABILITY_TOLERANCE`) sont
désormais représentés canoniquement en `fractions.Fraction` exact
(`1/10^12`, `1/10^12`, `1/10^10` — valeurs inchangées,
`I2_B2_A_C1_THRESHOLD_VALUES_CHANGED = NO`) et matérialisés en `mp.mpf`
uniquement à l'intérieur du contexte `mp.workprec` actif au moment de la
comparaison, via `_fraction_to_mpf_current`. Défaut corrigé : les
constantes étaient auparavant matérialisées en `mp.mpf` au moment de
l'import du module (précision par défaut ~53 bits), puis réutilisées telles
quelles lors d'analyses P1/P2, ce qui pouvait produire un verdict de porte
backward incorrect pour une valeur proche de la frontière gelée. Correction
de fidélité numérique uniquement ; aucun seuil scientifique modifié. Lionel
ORCIL a explicitement accepté I2-B2-A et I2-B2-A-C1
(`I2_B2_A_STATUS = ACCEPTED`, `I2_B2_A_C1_STATUS = ACCEPTED`).

## Arbitrage I2-B2-B (blocage initial résolu)

```text
I2_B2_B_INITIAL_STATUS = BLOCKED
I2_B2_B_INITIAL_BLOCKER = MANDATE_EXPECTED_OUTCOME_CONFLICT
I2_B2_B_FROZEN_SPECIFICATION_CONFLICT = NO
I2_B2_B_ARBITRATION = REVISE_LAMBDA2_TEST_EXPECTATION_TO_FAITHFUL_PRECISION_UNRESOLVED
FROZEN_PROTOCOL_CHANGE = NONE
GROUPED_SPECTRAL_SUPPORT_ORACLE = UNCHANGED_NON_BLOCKING_BACKLOG
REFERENCE_LAMBDA2_PRECISION_QUALIFICATION = PRECISION_UNRESOLVED
```

Le lot I2-B2-B avait initialement été bloqué (`I2_B2_B_INITIAL_STATUS =
BLOCKED`) : le mandat §24 exigeait littéralement `d_p<=1e-10` /
`stability_pass=True` pour la comparaison P0/P1 à Λ=2 (référence g=1,
mu=0, delta=0), alors que l'exécution fidèle du protocole gelé produit
réellement `d_P≈0.0311` (P0/P1) puis `d_P≈4.40e-8` (P1/P2), toutes deux
`> 1e-10`, aboutissant à `PRECISION_UNRESOLVED`. Ceci a été confirmé par
une seconde voie de calcul totalement indépendante (`mp.svd_c`). ChatGPT/
Lionel ont classifié ce point `MANDATE_EXPECTED_OUTCOME_CONFLICT` (et non
`FROZEN_SPECIFICATION_CONFLICT`) : le protocole gelé lui-même n'est pas
modifié (`FROZEN_PROTOCOL_CHANGE = NONE`) ; seule l'attente du mandat pour
Λ=2 était erronée. `GROUPED_SPECTRAL_SUPPORT_ORACLE` reste inchangé en
backlog non bloquant, sans promotion dans ce lot.

```text
CURRENT_LOT = Toy Model 0B I2-B2-B cross-precision projector stability resumed after arbitration
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-B2-B
I2_B2_B_SCOPE = CROSS_PRECISION_CLUSTER_MATCHING_D_P_AND_PRECISION_ROUTING
CROSS_PRECISION_CLUSTER_MATCHING = IMPLEMENTED
D_P = IMPLEMENTED
PRECISION_ROUTING = IMPLEMENTED
FINAL_D_GS = NOT_PUBLISHED
FINAL_GAP_GS = NOT_PUBLISHED
I2_B2_B_STATUS = ACCEPTED
I2_B2_B_ACCEPTED_HEAD = 6f0dca477c841b88befeed8ea0a782144acc2529
```

L'implémentation de Model 0B est autorisée uniquement par lots bornés sur
`implementation/model0b`. La spécification/le protocole scientifique gelé
reste immuable. L'exécution confirmatoire reste séparément
`NOT_AUTHORIZED` (`CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED`). Il
implémente l'appariement de cluster inter-précision par ensembles
d'indices déterministes, `d_P` (norme spectrale, seuil gelé `1e-10`
matérialisé localement à la précision active), et le routage
`PRECISION_STABLE`/`PRECISION_ESCALATED`/`PRECISION_UNRESOLVED` ; aucun
`d_GS`/`gap_GS` final n'est publié par ce lot. Rappel épistémique : un
cluster numérique reste toujours distinct d'une dégénérescence physique
certifiée. La qualification `PRECISION_UNRESOLVED` observée à Λ=2
(référence g=1, mu=0, delta=0) est un résultat de qualification numérique
fidèle et fail-closed, non une revendication physique. Lionel ORCIL a
explicitement accepté I2-B2-B (`I2_B2_B_STATUS = ACCEPTED`,
`I2_B2_B_ACCEPTED_HEAD = 6f0dca477c841b88befeed8ea0a782144acc2529`).

## I2-B2-C — canonical ground-state subspace

```text
CURRENT_LOT = Toy Model 0B I2-B2-C canonical ground-state subspace
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-B2-C
I2_B2_C_STATUS = ACCEPTED
I2_B2_C_ACCEPTED_HEAD = 8e42cd6492c37286287659303ab05011e6810ff6
FINAL_D_GS = NOT_PUBLISHED
FINAL_GAP_GS = NOT_PUBLISHED
SPECTRAL_WEIGHTS = NOT_STARTED
KUBO = NOT_STARTED
REFERENCE_LAMBDA2_PRECISION_QUALIFICATION = PRECISION_UNRESOLVED
REFERENCE_LAMBDA2_GROUND_STATE_BRANCH = GROUND_STATE_UNAVAILABLE_PRECISION
```

Le lot I2-B2-C consomme exclusivement le résultat déjà qualifié par
I2-B2-B (`precision_control.SpectralPrecisionControlResult`) et construit,
lorsque `PRECISION_STABLE` ou `PRECISION_ESCALATED`, le sous-espace
fondamental numérique canonique (`d_GS`, `P_GS`) à partir du clustering
spectral déjà présent au niveau de précision sélectionné — aucun nouveau
clustering, aucun nouvel epsilon, aucune nouvelle diagonalisation, aucun
nouveau contrôle de précision. Pour `PRECISION_UNRESOLVED`, propage
`GROUND_STATE_UNAVAILABLE_PRECISION` (aucun `P_GS`, aucun `d_GS`) : ceci
n'est ni une dégénérescence observée, ni un gap nul, ni une propriété
physique. Toute incohérence de contrat (statut résolvable sans
`selected_level_result`, métadonnées de cluster incohérentes, aucun ou
plusieurs clusters contenant l'indice spectral minimal) échoue
explicitement plutôt que d'être signalée silencieusement comme
indisponibilité numérique. La référence Λ=2 (g=1, mu=0, delta=0) reste
`PRECISION_UNRESOLVED` et se propage donc en
`GROUND_STATE_UNAVAILABLE_PRECISION` ; aucune valeur finale de `d_GS`
n'est publiée pour elle. `precision_control.py` n'a subi aucune
modification (aucun `CONTRACT_GAP` rencontré). Ce lot n'implémente ni
`rho_GS`, ni choix d'état pur, ni gap, ni poids spectraux, ni Kubo, ni
interprétation physique, ni exécution confirmatoire. Lionel ORCIL a
explicitement accepté I2-B2-C (`I2_B2_C_STATUS = ACCEPTED`,
`I2_B2_C_ACCEPTED_HEAD = 8e42cd6492c37286287659303ab05011e6810ff6`).

## I2-B2-D — canonical ground-state density

```text
CURRENT_LOT = Toy Model 0B I2-B2-D canonical ground-state density
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-B2-D
I2_B2_D_STATUS = ACCEPTED
I2_B2_D_ACCEPTED_HEAD = 1b8b573c284ccb64391a87a8c4ae6870eac48755
CANONICAL_GROUND_STATE_DENSITY = IMPLEMENTED_FAIL_CLOSED_ON_UNCERTIFIED_MULTIPLICITY
I2_B2_D_R1_REASON = NUMERICAL_CLUSTER_USED_AS_DEGENERATE_STATE_PREMISE
FINAL_D_GS = NOT_PUBLISHED
FINAL_GAP_GS = NOT_PUBLISHED
SPECTRAL_WEIGHTS = NOT_STARTED
KUBO = NOT_STARTED
REFERENCE_LAMBDA2_PRECISION_QUALIFICATION = PRECISION_UNRESOLVED
REFERENCE_LAMBDA2_GROUND_STATE_BRANCH = GROUND_STATE_UNAVAILABLE_PRECISION
REFERENCE_LAMBDA2_CANONICAL_GROUND_STATE = CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION
```

Le lot I2-B2-D consomme exclusivement `ground_state_branch.GroundStateBranchResult`
(jamais directement `SpectralPrecisionControlResult`, un Hamiltonien, des
valeurs propres ou des vecteurs propres) et applique la règle canonique
unifiée déjà gelée (`specification.md` §4, `exact-spectral-response.md`
§3) : `rho_GS = P_GS / Tr(P_GS) = P_GS / d_GS`, qui couvre automatiquement
`d_GS=1` (`rho_GS=P_GS`, aucune sélection de vecteur propre) et `d_GS>1`
(mélange uniforme). La division est effectuée strictement à l'intérieur du
contexte `mp.workprec(selected_precision_bits)` déjà établi par
`P_GS`, pour éviter toute troncature silencieuse de précision (même classe
de défaut que I2-B2-A-C1, vérifiée empiriquement et corrigée dès
l'implémentation). Pour `GROUND_STATE_UNAVAILABLE_PRECISION`, propage
`CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION` (aucun `rho_GS`, `P_GS`,
`d_GS`) : ceci n'est ni une dégénérescence observée, ni un gap nul, ni une
propriété physique. Toute incohérence de contrat (`p_gs`/`d_gs`/indices
manquants, `d_gs<=0`, `d_gs != len(indices)`, statut inconnu) échoue
explicitement. La référence Λ=2 reste `PRECISION_UNRESOLVED` ->
`GROUND_STATE_UNAVAILABLE_PRECISION` -> `CANONICAL_GROUND_STATE_UNAVAILABLE_PRECISION` ;
aucune nouvelle valeur numérique scientifique n'est figée pour elle. Ni
`ground_state_branch.py`, ni `precision_control.py`, ni `multiprecision.py`
n'ont été modifiés. Ce lot n'implémente ni `gap_GS`, ni certification
physique de dégénérescence, ni projecteurs excités, ni poids spectraux
`C_C^(pq)`, ni Kubo, ni exécution confirmatoire.

### Correction I2-B2-D-R1 : qualification fail-closed de la multiplicité

La revue distante ChatGPT a identifié que l'implémentation initiale
autorisait `rho_GS = P_GS/d_GS` comme état résolu pour tout `d_GS`, y
compris `d_GS > 1`, alors que le protocole gelé distingue explicitement un
fondamental unique (`rho = |Omega><Omega|`) d'un fondamental dégénéré
(`rho = P_GS/Tr(P_GS)`), avec le principe
`NUMERICAL_CLUSTER != PHYSICAL_DEGENERACY` : la dimension `d_gs` fournie
par I2-B2-C est celle d'un cluster spectral numériquement qualifié, pas un
certificat de dégénérescence physique/exacte
(`I2_B2_D_R1_REASON = NUMERICAL_CLUSTER_USED_AS_DEGENERATE_STATE_PREMISE`).

Correction appliquée, strictement dans `ground_state_density.py` :
- `d_gs == 1` : les deux branches de la prescription gelée coïncident
  exactement (`rho = |Omega><Omega| = P_GS/1 = P_GS`) ; `rho_gs` republie
  directement `p_gs`, sans opération arithmétique, statut
  `CANONICAL_GROUND_STATE_RESOLVED` ;
- `d_gs > 1` : aucun certificat structurel/exact de dégénérescence
  n'étant disponible à ce niveau, le pipeline reste fail-closed :
  nouveau statut `CANONICAL_GROUND_STATE_UNAVAILABLE_DEGENERACY_CERTIFICATION`,
  `rho_gs = None` ; `p_gs`/`d_gs`/`ground_cluster_indices`/
  `selected_precision_bits` restent disponibles comme diagnostics de
  sous-espace numérique, jamais comme certification de dégénérescence.

Aucun changement du protocole scientifique gelé
(`FROZEN_PROTOCOL_CHANGE = NONE`). Le futur certificat structurel/exact de
dégénérescence n'est pas inventé dans ce R1 et reste hors périmètre. Ni
`ground_state_branch.py`, ni `precision_control.py`, ni `multiprecision.py`
n'ont été modifiés par cette correction. Lionel ORCIL a explicitement
accepté I2-B2-D (`I2_B2_D_STATUS = ACCEPTED`,
`I2_B2_D_ACCEPTED_HEAD = 1b8b573c284ccb64391a87a8c4ae6870eac48755`).

## PERF-1 — shared real-model test fixtures

```text
CURRENT_LOT = Model 0B PERF-1 shared real-model test fixtures
PHASE = MODEL0B_IMPLEMENTATION_PERFORMANCE
PERF1_STATUS = ACCEPTED
PERF1_ACCEPTED_HEAD = c59539a5981ef513a7ef71b149ce62d285b1b2f7
PERF1_SCOPE = TEST_SESSION_REUSE_ONLY
SCIENTIFIC_CODE_CHANGED = NO
FROZEN_PROTOCOL_CHANGED = NO
SCIENTIFIC_RESULTS_CHANGED = NO
FINAL_D_GS       = NOT_PUBLISHED
FINAL_GAP_GS     = NOT_PUBLISHED
SPECTRAL_WEIGHTS = NOT_STARTED
KUBO             = NOT_STARTED
CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED
```

PERF-1 est une optimisation d'infrastructure de test strictement
intra-session : ajout de `tests/models/model0b/conftest.py` exposant des
fixtures `scope="session"` (`lambda1_components`, `lambda2_components`,
`lambda1_precision_result`, `lambda2_precision_result`,
`lambda1_p2_result`) qui appellent les routes scientifiques déjà acceptées
(`build_physical_basis`, `build_exact_discrete_components`,
`precision_control.run_spectral_precision_control`,
`precision_control._analyze_p2_direct`) exactement comme les tests les
appelaient directement auparavant. Les tests d'intégration réels de
`test_precision_control_model0b.py`, `test_ground_state_branch_model0b.py`
et `test_ground_state_density_model0b.py` consomment désormais ces
résultats partagés au lieu de relancer le ladder P0/P1/P2 complet à
chaque fois. Aucun code de production (`src/cosmobox_c_model/**`)
n'a été modifié ; aucun algorithme, seuil, précision ou verdict attendu
n'a changé (`SCIENTIFIC_CODE_CHANGED = NO`, `FROZEN_PROTOCOL_CHANGED =
NO`, `SCIENTIFIC_RESULTS_CHANGED = NO`). L'exécution complète du ladder
Λ=2 (P0/P1/P2), auparavant répétée 3 fois par session (~524s cumulés sur
un total de 657s), n'est désormais exécutée qu'une seule fois par session
(~187s), avec un gain mesuré `BASELINE_WALL_SECONDS = 657.28s` ->
`OPTIMIZED_WALL_SECONDS = 301.42s` (`SPEEDUP ≈ 2.18`,
`TIME_REDUCTION_PERCENT ≈ 54.1%`), pour un compte de tests inchangé
(`530 passed` avant et après). Les tests synthétiques de
`compare_precision_levels` et le routage forcé par monkeypatch sont
inchangés. Lionel ORCIL a explicitement accepté PERF-1
(`PERF1_STATUS = ACCEPTED`,
`PERF1_ACCEPTED_HEAD = c59539a5981ef513a7ef71b149ce62d285b1b2f7`).

## PERF-2 — projector-distance norm kernel optimization

```text
CURRENT_LOT = Model 0B PERF-2 projector-distance norm optimization
PHASE = MODEL0B_IMPLEMENTATION_PERFORMANCE
PERF2_STATUS = IMPLEMENTED_PENDING_REVIEW
PERF2_SCOPE = PROJECTOR_DISTANCE_NORM_KERNEL_ONLY
SCIENTIFIC_CODE_CHANGED = NO
NUMERICAL_IMPLEMENTATION_CHANGED = YES
FROZEN_PROTOCOL_CHANGED = NO
SCIENTIFIC_RESULTS_CHANGED = NO
FINAL_D_GS       = NOT_PUBLISHED
FINAL_GAP_GS     = NOT_PUBLISHED
SPECTRAL_WEIGHTS = NOT_STARTED
KUBO             = NOT_STARTED
CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED
NEXT_REQUIRED_GOVERNANCE_ACTION = CHATGPT_REVIEW_PERF2_THEN_LIONEL_DECISION
```

PERF-2 optimise exclusivement le noyau numérique du calcul de `d_P` dans
`precision_control.compare_precision_levels`, sans toucher à sa
définition, au matching de clusters, aux projecteurs utilisés, aux
précisions P0/P1/P2, aux seuils gelés, à la logique d'escalade ni aux
verdicts. Profilage local (développement uniquement, non committé) sur les
47 différences de projecteurs réelles P0/P1 de la référence Λ=2 : les 47
matrices sont exactement hermitiennes (vérifié sans tolérance) ; voie A
actuelle (`A†A` puis `eighe` puis `sqrt`) = 75.09s ; voie B SVD directe
(`mp.svd_c`) = 99.51s (plus lente, écartée) ; voie C fast-path hermitien
exact (`eighe(A)` direct puis `max|lambda|`) = 55.36s, avec accord
numérique avec la voie A à ~1e-33/1e-34 près (précision de représentation,
pas une tolérance nouvelle). Nouveau helper privé
`_projector_difference_spectral_norm` : bascule vers le fast-path
uniquement si `_is_exactly_hermitian(A)` est vrai (`A[i,j] ==
conjugate(A[j,i])` exactement, aucun epsilon, aucune symétrisation),
sinon repli inchangé vers `_spectral_norm_general`. Sept tests
d'équivalence synthétiques ajoutés (hermitienne nulle, diagonale, complexe
non diagonale, non-hermitienne générale, différences de projecteurs
rang 1 et rang > 1). `PROJECTOR_STABILITY_TOLERANCE = 1e-10`,
`P0=53`/`P1=106`/`P2=212`, et la priorité des `failure_reason` restent
inchangés. `BASELINE_LAMBDA2_TEST_SECONDS = 163.21s` ->
`OPTIMIZED_LAMBDA2_TEST_SECONDS = 129.92s`
(`LAMBDA2_TEST_SPEEDUP ≈ 1.26`). Suite complète :
`PERF1_FULL_BASELINE_SECONDS = 301.42s` ->
`OPTIMIZED_FULL_WALL_SECONDS = 234.77s`
(`FULL_SUITE_SPEEDUP_VS_PERF1 ≈ 1.28`,
`FULL_TIME_REDUCTION_PERCENT_VS_PERF1 ≈ 22.1%`), `537 passed` (530 + 7
nouveaux tests d'équivalence, aucun skip/xfail). L'oracle indépendant
`mp.svd_c` du test `test_lambda2_full_ladder_and_independent_d_p_oracle`
n'a pas été modifié et continue de confirmer `PRECISION_UNRESOLVED` pour
la référence Λ=2. Aucun autre fichier de production
(`multiprecision.py`, `eigensystem.py`, `ground_state_branch.py`,
`ground_state_density.py`, `exact_assembly.py`) n'a été modifié.
