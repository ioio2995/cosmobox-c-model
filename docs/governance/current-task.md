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
NEXT_REQUIRED_GOVERNANCE_ACTION = CHATGPT_REVIEW_I2_B1_THEN_LIONEL_DECISION
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
CURRENT_LOT = Toy Model 0B I2-B1 exact rational and multiprecision Hamiltonian assembly
PHASE       = MODEL0B_IMPLEMENTATION
CURRENT_IMPLEMENTATION_LOT = I2-B1
I2_B1_SCOPE  = EXACT_RATIONAL_PARAMETERS_AND_DIRECT_MULTIPRECISION_H_ASSEMBLY
I2_B1_STATUS = IMPLEMENTED_PENDING_REVIEW
P1_P2_EIGENSYSTEM = NOT_IMPLEMENTED
NEXT_REQUIRED_GOVERNANCE_ACTION = CHATGPT_REVIEW_I2_B1_THEN_LIONEL_DECISION
```

L'implémentation de Model 0B est autorisée uniquement par lots bornés sur
`implementation/model0b`. La spécification/le protocole scientifique gelé
reste immuable. L'exécution confirmatoire reste séparément
`NOT_AUTHORIZED` (`CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED`). Le lot
I2-B1 n'est pas déclaré `ACCEPTED` ni `CLOSED` ; aucun lot ultérieur (I2-B2 ou
suivant) n'est autorisé par ce lot. Ce lot n'implémente ni diagonalisation
haute précision, ni appariement de cluster, ni `d_P`, ni statut de précision
final ; `P1_P2_EIGENSYSTEM = NOT_IMPLEMENTED`.

L'implémentation de Model 0B est autorisée uniquement par lots bornés sur
`implementation/model0b`. La spécification/le protocole scientifique gelé
reste immuable. L'exécution confirmatoire reste séparément
`NOT_AUTHORIZED` (`CONFIRMATORY_EXECUTION_0B = NOT_AUTHORIZED`). Le lot
I2-A n'est pas déclaré `ACCEPTED` ni `CLOSED` ; aucun lot ultérieur (I2-B ou
suivant) n'est autorisé par ce lot. `I2_A_PRECISION_SCOPE = P0_BINARY64_ONLY` :
le contrôle multi-précision gelé (`P1>=106 bits`, `P2>=212 bits`,
stabilité de projecteur `p/2p`) n'est pas implémenté par ce lot
(`P1_P2_PRECISION_CONTROL = NOT_IMPLEMENTED`) et ce lot n'a aucun rôle
confirmatoire (`I2_A_CONFIRMATORY_ROLE = NONE`). Rappel épistémique : un
cluster numérique P0 n'est jamais une dégénérescence physique certifiée.
