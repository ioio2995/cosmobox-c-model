# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11. Il est mis à jour à chaque jalon important et constitue, avec le reste du dépôt, la mémoire durable du projet.

## État Git

```text
ACTIVE_BRANCH = master
BASE_COMMIT   = a1706db93acf65e9d75b3b21d3201d27b3445e6b
```

`BASE_COMMIT` désigne le dernier commit distant précédant le paquet documentaire courant ; il évite l'auto-référence impossible d'un fichier versionné vers le SHA du commit qui le contient.

`a1706db93acf65e9d75b3b21d3201d27b3445e6b` est le commit de fusion de la PR #1 (`governance/software-architecture`) sur `master` : il porte la gouvernance d'architecture logicielle gelée et le second audit architectural 0A.

## État documentaire

```text
C_HYPOTHESIS               = FROZEN (docs/model/c-hypothesis.md, conceptuellement gelée)
TOY_MODEL_0_SPECIFICATION  = FROZEN (docs/toy-models/toy0/specification.md, conceptuellement gelée)
IMPLEMENTATION_0A_CONTRACT = FROZEN_FUNCTIONAL (docs/toy-models/toy0/implementation-design.md, contenu fonctionnel gelé ; architecture désormais validée par le second audit, cf. Dernier jalon)
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
AUDIT_0A_2_ARCHITECTURE    = ACCEPTED
IMPLEMENTATION_0A          = NOT_AUTHORIZED
```

Le premier audit 0A reste valide pour son contenu fonctionnel, son catalogue de tests et son analyse des risques. Sa proposition d'architecture est supersédée par le second audit architectural (`AUDIT_0A_2_ARCHITECTURE`), accepté sous `software-architecture-governance.md`. La physique, les oracles et la stratégie fonctionnelle de 0A restent inchangés.

Architecture 0A validée :

```text
core/
    state_space
    fermions
    ladder
    operators
    identifiability

models/model0a/
    configuration
    assemblage
    observables
    benchmark

tests/
    architecture
    core
    models/model0a
```

## Lot courant

```text
CURRENT_LOT = correctif de gouvernance : fermeture du vocabulaire SCIENTIFIC_METADATA.status
PHASE       = GOVERNANCE_CORRECTIF
```

## Étape suivante

```text
NEXT_STEP = ouverture, après revue du commit distant et décision explicite de Lionel, du premier lot d'implémentation du Toy Model 0A selon l'architecture validée par le second audit.
```

L'implémentation n'est pas autorisée par ce lot.

## Questions ouvertes

```text
- aucune.
```
