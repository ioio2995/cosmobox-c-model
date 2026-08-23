# Toy Model 0B — enregistrement du gel

Ce document enregistre la décision explicite de gel du Toy Model 0B. Il ne
reproduit pas la spécification scientifique complète, dont la source
normative reste `specification.md`.

---

## 1. Statut normatif

```text
MODEL0B_STATUS               = FROZEN
MODEL0B_FREEZE_DECISION      = EXPLICITLY_APPROVED
MODEL0B_FREEZE_DECISION_DATE = 2026-08-24
MODEL0B_FREEZE_BASE_COMMIT   = d796c65d2538eaba2be7882647ba91db5cf93a32
MODEL0B_CLOSURE_REVIEW       = PASS
CLOSED_MAJOR_CONTROLS        = 21
OPEN_MAJOR_CONTROLS          = 0
IMPLEMENTATION_0B            = NOT_AUTHORIZED
```

Lionel ORCIL a explicitement donné la décision de gel. Le Toy Model 0B est
**FROZEN**.

Branche documentaire : `documentation/model0b-foundation`.

Commit de base scientifique/protocolaire gelée :
`d796c65d2538eaba2be7882647ba91db5cf93a32`.

---

## 2. Ce que couvre le gel

- la revue de clôture (`MODEL0B_CLOSURE_REVIEW = PASS`) ;
- les vingt-et-un contrôles numériques majeurs préenregistrés, tous fermés
  (`CLOSED_MAJOR_CONTROLS = 21`, `OPEN_MAJOR_CONTROLS = 0`) ;
- les règles finales d'acceptation (`MODEL0B_FINAL_ACCEPTANCE_RULES =
  VALIDATED_FOR_FREEZE`) ;
- les domaines MAIN, SOFT-LOOP, oracle et de troncature.

Au gel, plus aucun paramètre, tolérance, règle de revendication, règle
d'estimateur, règle de chemin/récurrence, oracle de symétrie, règle de rang ou
porte numérique ne peut être modifié pour convenance d'implémentation.

---

## 3. Ce que le gel ne couvre pas

Le gel ne signifie pas :

- que la campagne confirmatoire a été exécutée ;
- que le modèle a été confirmé empiriquement ;
- que l'implémentation est autorisée ;
- que tout élément spécialisé du backlog est clos.

---

## 4. Backlog du support spectral groupé

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
OUTSIDE_MAJOR_CONTROL_COUNT = YES
```

Le modèle est gelé alors que cet élément reste explicitement un backlog
analytique futur non bloquant. Sa portée scientifique n'est ni close, ni
modifiée par ce gel.

---

## 5. Sémantique de réouverture

Un bloc gelé ne peut être rouvert que sous la gouvernance existante, pour :

- une contradiction avérée ;
- une erreur affectant la validité ;
- une définition inexécutable ;
- un défaut susceptible de changer un verdict.

Les améliorations, extensions, généralisations, estimateurs alternatifs,
diagnostics additionnels ou nouvelles questions de recherche vont au backlog
ou à un niveau de modèle ultérieur.

---

## 6. Pare-feu implémentation

```text
IMPLEMENTATION_0B = NOT_AUTHORIZED
MODEL0B_FREEZE_DOES_NOT_AUTHORIZE_IMPLEMENTATION = YES
NEXT_REQUIRED_GOVERNANCE_ACTION = SEPARATE_IMPLEMENTATION_AUTHORIZATION_DECISION
```

Aucune branche d'implémentation, aucun lot de code, aucun lot de test et
aucun mandat d'exécution n'est créé par ce lot d'enregistrement du gel.

---

## 7. Renvois

```text
docs/toy-models/toy0b/specification.md
docs/toy-models/toy0b/validation-plan.md
docs/toy-models/toy0b/final-acceptance-rules.md
docs/toy-models/toy0b/numerical-zero-symmetry-control.md
docs/governance/current-task.md
```
