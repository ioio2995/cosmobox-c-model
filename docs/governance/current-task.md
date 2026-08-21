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
TOY_MODEL_0A                   = CLOSED
TESTS_0A                       = 89 PASS

MODEL0B_SPECIFICATION          = CONSOLIDATED / CLOSURE_REVIEW
MODEL0B_VALIDATION_PLAN        = CONSOLIDATED / CLOSURE_REVIEW
MODEL0B_NUMERICAL_CONTROLS     = OPEN
MODEL0B_FINAL_ACCEPTANCE_RULES = OPEN
IMPLEMENTATION_0B              = NOT_AUTHORIZED

SCIENTIFIC_METHOD_GOVERNANCE   = DRAFT_IN_FEATURES
```

Sources principales :

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
```

Les supports spécialisés de `docs/toy-models/toy0b/` conservent les preuves et qualifications détaillées ; ils ne constituent plus un contexte obligatoire lorsque les deux sources consolidées suffisent.

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

`VALIDATED_FOR_FREEZE` ne vaut pas `FROZEN`. Le gel final relève d'une décision explicite de Lionel ORCIL.

---

## Invariants 0B

```text
TOPOLOGY                  = 6-cycle
BACKGROUND                = (0,1,0,1,0,1)
REFERENCE_TRUNCATION      = Lambda=2
TRUNCATION_CHECK          = Lambda=3
PILOT_TRUNCATION          = Lambda=1
PHYSICAL_DIMENSION        = 40*Lambda - 2
REFERENCE_HAMILTONIAN     = H(g=1,mu=0,delta=0), J=1
PRIMARY_PROPAGATION_PROBE = Kubo density-density
PRIMARY_TIME_ESTIMATOR    = T_grow
SECONDARY_TIME_FAMILY     = T_thr(eta)
PRIMARY_RELATIONAL_SIGNAL = Delta1
GLOBAL_NULL_ORACLE        = Delta2 == 0
```

La réciprocité `chi_pq(t)=chi_qp(t)` ferme l'ancien problème d'orientation source-récepteur.

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
g=0,mu=0 = pure-hopping oracle
g=0.10   = weak-g stress outside nominal domain
delta=0.9 = disclosed qualification/stress outside nominal domain
```

SOFT-LOOP :

```text
g  = 1
mu = {-1.25, -1.5, -2}
```

La grille MAIN mesure une brisure finie ; elle ne sert pas à approximer `Xi1`.

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

Une seule famille de raffinement :

```text
B = {beta_1 > ... > beta_K > 0}
```

avec facteurs analytiques :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

Les valeurs `beta_k` et les tolérances restent ouvertes.

---

## Dernier bloc sectoriel clos

Le canal auto-conjugué `m=0` doit être compté une seule fois en général. Dans le secteur physique 0B, Gauss implique que les six flux déterminent la matière et :

```text
ZERO_GRADE_KUBO_CHANNEL      = INACTIVE_EXACT
ZERO_GRADE_NON_TARGET_WEIGHT = ZERO_EXACT
```

Aucune correction numérique de `P_sector` ou `Purity_direct` n'est requise pour ce canal.

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

Claude Code conserve un rôle critique ; il n'est pas un simple exécutant.

```text
BLOCKING
    contradiction démontrée
    erreur affectant la validité
    définition inexécutable
    défaut pouvant modifier un verdict

NON_BLOCKING_BACKLOG
    amélioration / généralisation / extension non nécessaire à la validité de 0B

REJECTED
    objection fausse, non démontrée ou hors périmètre
```

Principe :

```text
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_NEW_CONCEPTUAL_BRANCHING_WITHOUT_BLOCKING_DEFECT
```

Une objection `BLOCKING` stoppe le lot et revient à l'arbitrage conceptuel. Un élément `NON_BLOCKING_BACKLOG` ne rouvre pas le périmètre.

---

## Lot courant et prochaine action

```text
CURRENT_LOT = Toy Model 0B closure review
PHASE       = READ-ONLY CRITICAL AUDIT
NEXT_STEP   = Claude Code read-only closure audit
```

Mandat de l'audit : rechercher uniquement contradictions, erreurs mathématiques / numériques, définitions inexécutables, ambiguïtés pouvant modifier un verdict, ou incohérences entre `specification.md` et `validation-plan.md`.

Les améliorations non bloquantes sont consignées au backlog et ne provoquent aucune nouvelle branche de recherche.

Après arbitrage de cet audit, les paramètres réellement `OPEN` seront fermés en un seul lot numérique, puis le paquet sera soumis à la revue finale et à la décision explicite de gel.

`IMPLEMENTATION_0B` reste `NOT_AUTHORIZED`.
