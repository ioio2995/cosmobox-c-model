# Gouvernance des échanges et des responsabilités

Statut : **gelé**

Amendement du 21 août 2026 : préflight d'exécution Claude Code, autorisé explicitement par Lionel ORCIL.

Amendement du 21 août 2026 : Sonnet 5 devient le modèle minimal de production versionnée pour la documentation et l'ingénierie courante ; Haiku est retiré du workflow versionné Cosmobox. Modification autorisée explicitement par Lionel ORCIL.

Ce document fixe qui décide, qui produit, qui publie et qui valide dans le dépôt `cosmobox-c-model`.

Il complète `docs/governance/documentation-governance.md`.

## 1. Rôles

### Lionel ORCIL

Superviseur et décideur final. Il fixe les priorités, valide les lots, désigne la branche de travail, arbitre les changements de périmètre et autorise les PR, fusions, releases et gels.

L'autorisation d'implémenter un lot sur une branche désignée comprend, sauf restriction explicite, le commit et le push du diff strictement limité au lot.

### ChatGPT

Responsable scientifique et conceptuel : hypothèses, définitions, conventions, invariants, critères d'acceptation, plans de validation, interprétation et revue du commit distant.

ChatGPT est également responsable de la gouvernance transverse de collaboration et de méthode : règles de rôles, cycle des lots, limites de responsabilité entre participants et règles documentaires de collaboration. Toute évolution de cette gouvernance reste soumise à la validation de Lionel.

ChatGPT distingue toujours : proposé, gelé, implémenté, poussé et accepté.

### Claude Code

Responsable de l'ingénierie : audit du dépôt, architecture interne, code, tests, documentation développeur directement liée au code, commit et push du lot sur la branche autorisée.

Claude Code conserve également un rôle de challenge critique dans les lots scientifiques ou documentaires lorsqu'un mandat le prévoit. Ce droit de challenge n'autorise ni l'ouverture autonome d'une nouvelle branche de recherche ni la modification silencieuse d'une décision scientifique.

Les documents de gouvernance transverse ne font pas partie du périmètre normal de Claude Code. Claude Code ne les modifie que sur demande explicite de Lionel dans un mandat qui l'autorise spécifiquement.

Claude Code ne modifie jamais une convention scientifique, un seuil, un manifeste ou un périmètre sans décision explicite.

## 2. Cycle d'un lot

1. **Cadrage** par ChatGPT : objectif, inclus, hors-périmètre, invariants, validations et documents applicables.
2. **Audit** par Claude Code, sans code sauf autorisation : fichiers, lacunes, architecture, tests et questions.
3. **Revue conceptuelle** par ChatGPT et validation du lancement par Lionel.
4. **Implémentation, tests, commit et push** par Claude Code sur la branche désignée.
5. **Rapport post-push** avec branche, SHA de base, SHA distant, diff exact, tests, limites et état Git résiduel.
6. **Revue du commit distant** par ChatGPT.
7. **Acceptation du lot** et autorisation du lot suivant par Lionel.

Un push ou des tests réussis ne valent pas acceptation scientifique.

## 3. Continuité entre lots et messages de validation

Une validation positive ne génère pas, à elle seule, un message autonome destiné à Claude Code lorsqu'aucune action immédiate n'est requise de sa part.

Après la revue positive d'un commit distant :

- ChatGPT rapporte le verdict à Lionel ;
- Lionel accepte ou non le lot et décide de l'ouverture éventuelle du lot suivant ;
- si un lot suivant est ouvert, la validation du lot précédent est rappelée en tête du nouveau mandat comme **prérequis de continuité** ;
- ce rappel contient au minimum le lot accepté, les SHA de référence utiles, le verdict d'audit et le fait que le lot précédent ne doit pas être rouvert sans défaut bloquant nouvellement identifié.

Ainsi, un `PASS` est normalement transporté par le mandat suivant plutôt que par un échange Claude Code sans action utile.

En revanche, un message autonome à Claude Code reste requis lorsqu'il entraîne une action ou modifie l'état de travail, notamment en cas de :

- `FAIL` ;
- `STOP` ;
- correctif demandé ;
- demande d'audit complémentaire ;
- remise en conformité ;
- synchronisation ou opération Git explicitement autorisée ;
- absence de lot suivant mais nécessité de transmettre une instruction particulière.

L'absence de message autonome après un `PASS` ne vaut jamais autorisation implicite de poursuivre. Claude Code n'ouvre aucun lot suivant sans mandat explicite.

## 4. Format d'une mission Claude Code

Toute mission commence par un **bloc de préflight**, avant le contexte scientifique ou technique.

Format minimal :

```text
EXECUTION_PROFILE
CLIENT = CLAUDE_CODE_LOCAL
MODEL = <modèle demandé>
EFFORT = <niveau demandé>
SESSION_CONTEXT = CLEAR_REQUIRED | CONTINUE_AUTHORIZED

REPOSITORY_PREFLIGHT
REPOSITORY = ioio2995/cosmobox-c-model
REMOTE = https://github.com/ioio2995/cosmobox-c-model.git
BRANCH = <branche autorisée>
EXPECTED_HEAD = <SHA si requis, sinon ANY_ON_BRANCH>
EXPECTED_WORKTREE = CLEAN | DIRTY_ALLOWED
```

Puis viennent :

```text
Contexte
Branche de travail autorisée
Documents obligatoires
Phase courante du cycle de collaboration
Objectif du lot
Périmètre inclus
Hors-périmètre
Invariants non négociables
Travail demandé
Livrable attendu
Critères d'acceptation
Restrictions Git particulières
```

### 4.1 Préflight utilisateur de session

Sauf continuité explicitement autorisée :

```text
SESSION_CONTEXT = CLEAR_REQUIRED
```

Lionel initialise alors une session Claude Code propre avant d'envoyer le mandat, notamment via `/clear` lorsqu'une session existante est réutilisée.

Le modèle et le niveau d'effort demandés sont réglés **avant** l'exécution du mandat. Ils ne sont jamais laissés implicites lorsqu'ils participent à la stratégie de coût ou de qualité du lot.

Exemple :

```text
MODEL = CLAUDE_SONNET_5
EFFORT = AUTO
SESSION_CONTEXT = CLEAR_REQUIRED
```

Un mandat peut au contraire déclarer :

```text
SESSION_CONTEXT = CONTINUE_AUTHORIZED
```

uniquement lorsque la continuité du contexte courant est intentionnelle et utile au lot.

### 4.2 Préflight dépôt

Avant toute lecture substantielle ou modification, Claude Code vérifie dans une **seule étape de préflight regroupée autant que possible** :

```text
remote effectif
branche courante / branche demandée
HEAD courant
état du worktree
```

Le mandat indique l'état attendu du worktree :

```text
EXPECTED_WORKTREE = CLEAN
```

pour un nouveau lot sans diff préalable, ou :

```text
EXPECTED_WORKTREE = DIRTY_ALLOWED
```

pour une tâche qui doit précisément examiner ou poursuivre un diff non commité déjà autorisé.

`DIRTY_ALLOWED` ne signifie jamais que des modifications arbitraires peuvent être ignorées : le mandat doit identifier le diff ou les fichiers attendus lorsque leur présence importe.

Si le dépôt, le remote, la branche, le HEAD requis ou l'état du worktree ne correspondent pas au préflight déclaré, Claude Code n'entame pas le lot et retourne :

```text
PREFLIGHT = FAILED
```

avec uniquement l'écart constaté et l'action minimale nécessaire pour revenir à l'état attendu.

Claude Code ne substitue jamais un dépôt voisin, un ancien dépôt ou une branche ressemblante au dépôt explicitement déclaré.

### 4.3 Discipline de contexte et de coût

Le dépôt est la mémoire durable du projet. Un mandat ne reconstruit pas l'historique complet de Cosmobox dans le prompt.

Par défaut :

```text
ONE_TASK = ONE_BOUNDED_SCOPE
READ_ONLY_WHAT_IS_NEEDED = TRUE
GLOBAL_AUDIT_BY_DEFAULT = FALSE
```

Les documents à lire et les fichiers autorisés sont bornés par le mandat. Claude Code n'élargit la lecture que si une contradiction bloquante ne peut pas être évaluée autrement.

Le choix du modèle et de l'effort reste proportionné au besoin, avec un plancher de production explicite :

```text
VERSIONED_PRODUCTION_MODEL = CLAUDE_SONNET_5
```

Sonnet 5 est le modèle minimal utilisé pour toute écriture versionnée du projet, y compris les opérations documentaires mécaniques et l'ingénierie courante.

L'optimisation de coût repose donc prioritairement sur :

```text
SESSION_CONTEXT = CLEAR_REQUIRED
ONE_TASK = ONE_BOUNDED_SCOPE
READ_ONLY_WHAT_IS_NEEDED = TRUE
GLOBAL_AUDIT_BY_DEFAULT = FALSE
```

et non sur l'emploi d'un modèle inférieur pour la production versionnée.

Une escalade au-dessus de Sonnet, notamment vers Opus, reste explicite et doit correspondre à un besoin scientifique identifié.

La lecture commence toujours par les documents de gouvernance réellement nécessaires au mandat. Les missions bornées peuvent référencer cette charte au lieu de la relire intégralement lorsque son contenu est déjà disponible dans le contexte propre de projet et qu'aucune modification de gouvernance n'est en jeu.

`docs/governance/current-task.md` et les documents du périmètre concerné sont ensuite utilisés lorsque le mandat dépend de l'état courant du projet.

Une mission ne recopie pas les règles générales déjà définies dans cette charte. Elle les référence, indique explicitement la phase courante du cycle et ne précise que le contexte, le périmètre, les invariants et les restrictions propres au lot.

En cas de contradiction entre un mandat courant et cette gouvernance gelée, Claude Code s'arrête et signale la contradiction. Un mandat ne modifie pas implicitement la gouvernance.

## 5. Rapport d'audit

```text
1. Compréhension du lot
2. Code existant audité
3. Architecture proposée
4. Fichiers concernés
5. Éléments réutilisés
6. Tests et validations
7. Risques et limites
8. Questions bloquantes
9. Actions non réalisées
```

## 6. Rapport de livraison

```text
1. Résumé
2. Branche et SHA distant
3. Diff réel et fichiers poussés
4. Décisions techniques
5. Tests exécutés
6. Résultats
7. Écarts au plan
8. Limites connues
9. État Git résiduel
10. Actions restantes
```

## 7. Autorisation Git par défaut

Pour une implémentation ou un correctif autorisé sur une branche désignée :

```text
modifier → tester → stager explicitement → committer → pousser → vérifier → rapporter
```

Cette autorisation ne couvre jamais :

- un fichier hors périmètre ;
- une autre branche ;
- un force-push ou une réécriture d'historique ;
- une PR, une fusion ou une release ;
- une modification normative non validée ;
- le lot suivant.

En cas de divergence distante non triviale ou de périmètre réel différent, Claude Code s'arrête avant publication.

## 8. Ambiguïtés

- **Scientifique** : Claude Code s'arrête ; ChatGPT propose ; Lionel tranche.
- **Ingénierie** : Claude Code décide et documente dans les limites du contrat.
- **Gouvernance transverse** : ChatGPT propose et maintient ; Lionel valide. Claude Code n'intervient que sur mandat explicite dédié.
- **Périmètre** : hors-périmètre jusqu'à autorisation.
- **Contradiction documentaire** : aucune décision locale dans le code ; correction selon la gouvernance documentaire.

## 9. Rappel de remise en conformité

```text
Applique `docs/governance/collaboration-governance.md` et reprends au dernier jalon validé.
```

Après ce rappel, le participant identifie la règle violée, le dernier jalon réel, ce qui a été fait et la reprise minimale autorisée.

## 10. Langue de collaboration

Les rapports, audits, demandes d'arbitrage, comptes rendus et réponses de collaboration destinés à Lionel ou à ChatGPT sont rédigés en français.

Peuvent rester en anglais lorsqu'il est naturel ou conventionnel de le faire :

- le code ;
- les identifiants et noms d'API ;
- les noms de fichiers ;
- les commandes et sorties d'outils ;
- les messages Git ;
- les termes techniques consacrés.

Cette règle porte sur la communication de collaboration et ne modifie pas les conventions internes du code ou des formats techniques.

## 11. Mémoire de session

À chaque jalon important, conserver :

```text
branche
commit de tête
lot courant
dernier jalon validé
documents applicables
travail réalisé
travail non réalisé
prochaine action autorisée
questions ouvertes
```

Le dépôt est la mémoire durable. Une décision devant survivre à la session doit être inscrite dans la documentation.

## 12. Profils d'exécution Claude Code

### 12.1 DOCUMENTATION

```text
MODEL = CLAUDE_SONNET_5
EFFORT = AUTO
```

**Usage** :

- toute intégration documentaire versionnée ;
- synchronisation de statuts ;
- transcription de valeurs, formules ou protocoles déjà arbitrés ;
- corrections documentaires mécaniques ;
- consolidation multi-documents ;
- opérations Git simples attachées à un lot documentaire autorisé ;
- commit / push d'un lot documentaire déjà validé.

Sonnet exécute la décision fournie par le mandat. Le choix de Sonnet comme modèle documentaire ne lui confère aucune autorité scientifique supplémentaire.

Pour le rôle spécialisé `cosmobox-doc`, les règles de `docs/governance/agents/cosmobox-doc-governance.md` restent intégralement applicables.

### 12.2 REVIEW_OR_ENGINEERING

```text
MODEL = CLAUDE_SONNET_5
EFFORT = AUTO
```

**Usage** :

- revue nécessitant un raisonnement non trivial ;
- contrôle de cohérence documentaire ;
- conception ou implémentation logicielle ;
- analyse technique ;
- conception ou implémentation logicielle versionnée ;
- correctifs de code et maintenance courante.

### 12.3 SCIENTIFIC_ESCALATION

```text
MODEL = CLAUDE_OPUS_5
EFFORT = AUTO
```

**Usage** :

- contre-expertise scientifique ciblée ;
- démonstration difficile ;
- recherche de contre-exemple ;
- contradiction conceptuelle bornée.

### 12.4 SCIENTIFIC_HARD_BLOCKING

```text
MODEL = CLAUDE_OPUS_5
EFFORT = HIGH
```

Usage exceptionnel uniquement pour un BLOCKING scientifique précis lorsque le niveau inférieur est insuffisant.

### 12.5 Principe normatif

```text
VERSIONED_PRODUCTION_MODEL = CLAUDE_SONNET_5
DOCUMENTATION_MODEL = CLAUDE_SONNET_5
ENGINEERING_MODEL = CLAUDE_SONNET_5

SCIENTIFIC_ESCALATION_MODEL = CLAUDE_OPUS_5

HAIKU_FOR_VERSIONED_PRODUCTION = NOT_USED
MODEL_ESCALATION_ABOVE_SONNET = EXPLICIT
```

Sonnet 5 constitue le plancher de production du workflow Cosmobox pour la documentation versionnée et l'ingénierie courante.

Haiku n'est plus utilisé pour produire ou modifier des fichiers versionnés du projet.

Opus reste une escalade ciblée pour la contre-expertise scientifique, les démonstrations difficiles, la recherche de contre-exemples et les blocages scientifiques explicitement identifiés.

La discipline de coût ne consiste plus à sélectionner un modèle inférieur à Sonnet pour une modification versionnée. Elle repose sur un contexte propre, un périmètre borné, des lectures ciblées et l'absence d'audit global par défaut.

## 13. Évolution

Toute modification de cette charte exige une décision explicite, la mise à jour des documents qui la référencent si leur sens est affecté, la vérification du diff réel et la validation de Lionel.
