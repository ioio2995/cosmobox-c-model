# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11. Il est mis à jour à chaque jalon important et constitue, avec le reste du dépôt, la mémoire durable du projet.

## État Git

```text
ACTIVE_BRANCH = governance/software-architecture
BASE_COMMIT   = 37412e608d41e78109d9d7480f237ca45ef9bf32
```

`BASE_COMMIT` désigne le dernier commit distant précédant le paquet documentaire courant ; il évite l'auto-référence impossible d'un fichier versionné vers le SHA du commit qui le contient.

## État documentaire

```text
C_HYPOTHESIS               = FROZEN (docs/model/c-hypothesis.md, conceptuellement gelée)
TOY_MODEL_0_SPECIFICATION  = FROZEN (docs/toy-models/toy0/specification.md, conceptuellement gelée)
IMPLEMENTATION_0A_CONTRACT = FROZEN_FUNCTIONAL (docs/toy-models/toy0/implementation-design.md, architecture à réauditer)
GOVERNANCE_COLLABORATION   = FROZEN (docs/governance/collaboration-governance.md)
GOVERNANCE_DOCUMENTATION   = FROZEN (docs/governance/documentation-governance.md)
GOVERNANCE_SOFTWARE_ARCH   = FROZEN (docs/governance/software-architecture-governance.md)
DOCUMENTATION_ARCHITECTURE = ALIGNED
```

## État du code

```text
CODE_STATUS  = NOT_STARTED
TESTS_STATUS = NOT_STARTED
```

Aucun code 0A n'a encore été autorisé.

## Dernier jalon

```text
AUDIT_0A_1_FUNCTIONAL      = ACCEPTED
AUDIT_0A_1_TEST_STRATEGY   = ACCEPTED
AUDIT_0A_1_RISK_ANALYSIS   = ACCEPTED
AUDIT_0A_1_ARCHITECTURE    = TO_REVIEW
IMPLEMENTATION_0A          = NOT_AUTHORIZED
```

Le premier audit 0A reste valide pour son contenu fonctionnel, son catalogue de tests et son analyse des risques. Sa proposition d'architecture doit être réévaluée sous `software-architecture-governance.md`.

## Lot courant

```text
CURRENT_LOT = second audit architectural du Toy Model 0A
PHASE       = AUDIT_READ_ONLY
```

## Étape suivante

```text
NEXT_STEP = demander à Claude Code un audit architectural différentiel de 0A sous la nouvelle gouvernance logicielle, sans modification de code ni de documentation.
```

## Questions ouvertes

```text
- classification exacte des briques 0A entre core/ et models/model0a/ ;
- adaptations nécessaires de l'architecture proposée dans implementation-design.md, sans modification de la physique gelée.
```
