# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11 et porte le statut opérationnel courant du projet.

## Git

```text
ACTIVE_BRANCH = documentation/model0b-foundation
BASE_COMMIT   = 08d5ca506ff05e15dd9bc084ea121c3d0a19b662
ERRATA_COMMIT = d00d146
GOVERNANCE_EXECUTION_PREFLIGHT = dec669d90fc01bc998e53ef8cec2bac7a93f5679
```

Aucun code 0B n'est autorisé dans le lot courant.

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
MODEL0B_NUMERICAL_CONTROLS      = CLOSURE_IN_PROGRESS
MODEL0B_FINAL_ACCEPTANCE_RULES  = OPEN
IMPLEMENTATION_0B               = NOT_AUTHORIZED

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

# Delta1 error budget
DELTA1_PROPAGATED_ERROR_BUDGET          = VALIDATED_FOR_FREEZE

# SOFT-LOOP / derivative
A_DELTA_VALUES                          = VALIDATED_FOR_FREEZE
DERIVATIVE_STABILITY_CRITERION          = VALIDATED_FOR_FREEZE
RICHARDSON_USAGE_RULE                   = VALIDATED_FOR_FREEZE
```

Tous ces éléments ont été validés scientifiquement dans ce lot et intégrés
documentairement. Ils ne sont pas encore `FROZEN` : seule une décision explicite
de gel de Lionel ORCIL autoriser le passage à `FROZEN`.

---

## Paramètres encore OPEN avant gel

```text
# temporal / numerical
ARGMAX_TOLERANCES                      = OPEN
DEGENERATE_ROOT_CONTROL                = OPEN

# SOFT-LOOP
STATIC_X_CONTROL_VALUES
STATIC_COLLAPSE_NUMERICAL_CRITERION

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
CURRENT_LOT = Toy Model 0B numerical preregistration closure
PHASE       = CLOSE_ONE_NUMERICAL_CONTROL_AT_A_TIME
CURRENT_PARAMETER = PENDING_NEXT_SELECTION
IMPLEMENTATION_0B = NOT_AUTHORIZED
```

**État** : sept paramètres numériques majeurs viennent d'être fermés et intégrés
documentairement (ROOT_SOLVER_TOLERANCES, SPECTRAL_PRECISION_CONTROL,
SIMPLE_ROOT_CONTROL, DELTA1_PROPAGATED_ERROR_BUDGET, A_DELTA_VALUES,
DERIVATIVE_STABILITY_CRITERION, RICHARDSON_USAGE_RULE).

**Prochaine action** : sélection par ChatGPT / Lionel ORCIL du prochain
paramètre OPEN à fermer. Aucune sélection autonome de paramètre suivant.
