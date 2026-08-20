# Contrat de continuité — état courant

Ce document suit `docs/governance/collaboration-governance.md` §11. Il est mis à jour à chaque jalon important et constitue, avec le reste du dépôt, la mémoire durable du projet.

## État Git

```text
ACTIVE_BRANCH = documentation/model0b-foundation
BASE_COMMIT   = 08d5ca506ff05e15dd9bc084ea121c3d0a19b662
```

`BASE_COMMIT` désigne le dernier commit distant canonique précédant le paquet documentaire courant. `08d5ca506ff05e15dd9bc084ea121c3d0a19b662` est le merge de clôture du Toy Model 0A sur `master` et reste le point de départ canonique du lot 0B.

Aucune modification de code n'est autorisée dans le lot documentaire courant.

## État documentaire

```text
C_HYPOTHESIS                    = FROZEN
TOY_MODEL_0_SPECIFICATION       = FROZEN
IMPLEMENTATION_0A_CONTRACT      = FROZEN (contrat exécuté)
CLOSURE_0A_REPORT               = CLOSED
GOVERNANCE_COLLABORATION        = FROZEN
GOVERNANCE_DOCUMENTATION        = FROZEN
GOVERNANCE_SOFTWARE_ARCH        = FROZEN

MODEL0B_SPECIFICATION           = REVIEW_IN_PROGRESS
MODEL0B_VALIDATION_PLAN         = REVIEW_IN_PROGRESS
SCIENTIFIC_METHOD_GOVERNANCE    = DRAFT_IN_FEATURES
DOCUMENTATION_ARCHITECTURE      = ALIGNED
```

Sources nouvelles du lot :

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
features/scientific-method-governance.md
```

Le brouillon de gouvernance méthodologique reste volontairement dans `features/` tant que Lionel ORCIL n'a pas autorisé son gel et sa migration vers `docs/governance/`.

## État scientifique 0B

```text
MODEL0B_SYSTEM_AND_GAUSS       = VALIDATED_FOR_FREEZE
MODEL0B_TRUNCATION             = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_OBSERVABLES     = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_IDENTIFIABILITY = VALIDATED_FOR_FREEZE
MODEL0B_SYMMETRIES             = VALIDATED_FOR_FREEZE
MODEL0B_NULL_ORACLES           = VALIDATED_FOR_FREEZE
MODEL0B_KUBO_PROBE             = VALIDATED_FOR_FREEZE
MODEL0B_PRIMARY_SIGNAL_DELTA1  = VALIDATED_FOR_FREEZE

MODEL0B_TIME_WINDOW_PROTOCOL   = OPEN
MODEL0B_GAMMA_SET              = OPEN
MODEL0B_TIME_SAMPLING          = OPEN
MODEL0B_NUMERICAL_TOLERANCES   = OPEN
MODEL0B_PARAMETER_CAMPAIGN     = OPEN
MODEL0B_ORDERED_RELATIONS      = OPEN
```

Les blocs `VALIDATED_FOR_FREEZE` ne sont pas encore marqués `FROZEN` dans le dépôt. Le gel reste une décision explicite de Lionel ORCIL après revue du paquet documentaire.

## Invariants scientifiques 0B déjà stabilisés

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

Les résultats pilotes de rang connus concernent exclusivement `Lambda=1` et sont enregistrés comme `PILOT_LAMBDA1` dans la spécification. Aucun rang global des familles n'a été calculé à `Lambda=2` dans le présent lot.

## Gouvernance méthodologique en cours de formalisation

Le brouillon `features/scientific-method-governance.md` enregistre notamment les règles suivantes :

```text
- pré-enregistrer avant le calcul confirmatoire ;
- déclarer les résultats pilotes déjà vus ;
- distinguer span linéaire et algèbre engendrée ;
- ne pas enrichir une famille après FAIL pour fabriquer un PASS ;
- cibler l'identifiabilité sur les directions physiques déclarées ;
- vérifier l'activité d'un générateur avant l'identifiabilité ;
- chercher les résultats nuls et le stabilisateur avant de concevoir un signal ;
- inclure les transformations composées dans l'analyse des symétries ;
- accompagner tout verdict de son domaine complet ;
- séparer observabilité statique, dynamique et quantité dérivée ;
- distinguer appariement opératoriel et diagnostic relatif au bord ;
- séparer oracle analytique et signal scientifique ;
- conserver les résultats négatifs et les limitations.
```

Cette liste est un résumé ; la source de vérité du brouillon méthodologique est le fichier `features/scientific-method-governance.md`.

## État du code

```text
CODE_STATUS       = IMPLEMENTED_ACCEPTED_0A_ONLY
TESTS_STATUS      = PASSED_89
BENCHMARK_0A      = CLOSED
INSTRUMENT_0A     = VALIDATED
IMPLEMENTATION_0B = NOT_AUTHORIZED
```

Aucun code 0B n'a été demandé, autorisé ou publié dans ce lot.

## Dernier jalon clos

```text
IMPLEMENTATION_0A = ACCEPTED
REMOTE_REVIEW_0A  = PASS
LOT_0A            = CLOSED
```

0A ne doit pas être rouvert sans défaut bloquant nouvellement démontré.

## Lot courant

```text
CURRENT_LOT = documentation et pré-enregistrement du Toy Model 0B
PHASE       = DOCUMENTATION / SCIENTIFIC SPECIFICATION
```

Objectif du lot courant : déposer dans le dépôt la mémoire scientifique durable des décisions 0B déjà stabilisées et les règles méthodologiques transverses découvertes pendant le cadrage, sans fermer artificiellement les paramètres temporels encore ouverts.

## Prochaine action autorisée

```text
NEXT_STEP = revue documentaire du paquet 0B, puis reprise de la physique pour fermer les paramètres encore OPEN.
```

Aucun audit Claude Code ni aucune implémentation 0B n'est actuellement autorisé.

## Questions ouvertes

```text
1. convention ordonnée source-récepteur des orbites dynamiques ;
2. ensemble Gamma du diagnostic de récurrence ;
3. règle finale de fenêtre temporelle ;
4. grille eta et critère de convergence vers C_short ;
5. stratégie d'échantillonnage / interpolation temporelle ;
6. tolérances numériques ;
7. grille de campagne (g, mu, delta) ;
8. critère formel de cohérence entre T_grow et T_thr(eta) ;
9. validation puis migration de la gouvernance méthodologique depuis features/.
```
