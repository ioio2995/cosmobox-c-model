# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11. Il est mis à jour à chaque jalon important et constitue, avec le reste du dépôt, la mémoire durable du projet.

## État Git

```text
ACTIVE_BRANCH = master
BASE_COMMIT   = fbd6f0967460153dcacd39656808db843c7a675a
```

`BASE_COMMIT` désigne le dernier commit distant précédant le paquet documentaire courant ; il évite l'auto-référence impossible d'un fichier versionné vers le SHA du commit qui le contient.

`fbd6f0967460153dcacd39656808db843c7a675a` est le commit de fusion de la PR #3 (`implementation/model0a`) sur `master`. Il intègre le dernier commit d'implémentation revu et accepté :

```text
a5fc55563db7ee7b06a41e4bfb6b0c8a928f960f
```

## État documentaire

```text
C_HYPOTHESIS               = FROZEN (docs/model/c-hypothesis.md, conceptuellement gelée)
TOY_MODEL_0_SPECIFICATION  = FROZEN (docs/toy-models/toy0/specification.md, conceptuellement gelée)
IMPLEMENTATION_0A_CONTRACT = FROZEN (docs/toy-models/toy0/implementation-design.md, contrat exécuté)
CLOSURE_0A_REPORT          = CLOSED (docs/toy-models/toy0/closure-report.md)
GOVERNANCE_COLLABORATION   = FROZEN (docs/governance/collaboration-governance.md)
GOVERNANCE_DOCUMENTATION   = FROZEN (docs/governance/documentation-governance.md)
GOVERNANCE_SOFTWARE_ARCH   = FROZEN (docs/governance/software-architecture-governance.md)
DOCUMENTATION_ARCHITECTURE = ALIGNED
```

## État du code

```text
CODE_STATUS       = IMPLEMENTED_ACCEPTED
TESTS_STATUS      = PASSED_89
BENCHMARK_0A      = CLOSED
INSTRUMENT_0A     = VALIDATED
```

La suite finale comporte 89 tests passants. Le runner 0A reproduit les oracles analytiques gelés et produit deux sorties JSON successives byte-identiques.

## Dernier jalon

```text
AUDIT_0A_1_FUNCTIONAL      = ACCEPTED
AUDIT_0A_1_TEST_STRATEGY   = ACCEPTED
AUDIT_0A_1_RISK_ANALYSIS   = ACCEPTED
AUDIT_0A_2_ARCHITECTURE    = ACCEPTED
IMPLEMENTATION_0A          = ACCEPTED
REMOTE_REVIEW_0A           = PASS
LOT_0A                     = CLOSED
```

Le premier audit 0A reste valide pour son contenu fonctionnel, son catalogue de tests et son analyse des risques. Sa proposition d'architecture a été supersédée par le second audit architectural, désormais réalisé dans l'implémentation acceptée.

Architecture 0A retenue :

```text
core/
    state_space
    fermions
    ladder
    operators
    identifiability

models/model0a/
    basis_config
    constants
    operators
    observables
    benchmark

tests/
    architecture
    core
    models/model0a
```

## Lot courant

```text
CURRENT_LOT = clôture documentaire du Toy Model 0A
PHASE       = CLOSED
```

## Étape suivante

```text
NEXT_STEP = cadrage et spécification séparés du premier modèle exploratoire ; aucun modèle suivant n'est encore autorisé à l'implémentation.
```

Le prochain modèle devra constituer un nouveau lot et ne doit pas réouvrir 0A sans défaut bloquant nouvellement démontré.

## Questions ouvertes

```text
- aucune question ouverte sur 0A.
```
