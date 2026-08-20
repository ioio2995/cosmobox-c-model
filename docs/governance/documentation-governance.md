# Gouvernance normative de la documentation

Statut : **gelé**

Ce document définit l'architecture documentaire normative du dépôt `cosmobox-c-model`.

## 1. Principe

Une information normative possède une seule source de vérité principale. Les index, README, décisions et fichiers de compatibilité peuvent la résumer ou y renvoyer, mais ne doivent pas maintenir une définition divergente.

Le code implémente les documents normatifs. Il ne redéfinit jamais silencieusement une convention scientifique.

## 2. Arborescence cible

```text
docs/
├── governance/
│   ├── collaboration-governance.md
│   ├── documentation-governance.md
│   └── current-task.md
├── model/
│   └── c-hypothesis.md
├── decisions/
│   ├── decisions.md
│   └── Dxxx-*.md
└── toy-models/
    └── toyN/
        ├── specification.md
        ├── implementation-design.md
        ├── validation-plan.md      # lorsqu'il existe
        └── closure-report.md       # lorsqu'il existe

experiments/
└── toyN/

schemas/
└── toyN/
```

Les dossiers vides ne sont pas créés à l'avance. Cette arborescence est la cible normative ; l'écart entre elle et l'état réel du dépôt à un instant donné est décrit en §10.

## 3. Rôle des fonctions documentaires

### `docs/governance/`

Règles transverses du dépôt : architecture documentaire, collaboration, publication, statuts, contrôles, et l'état courant du contrat de continuité.

### `docs/model/`

Hypothèse C générale et conventions communes à plusieurs modèles jouets.

### `docs/decisions/`

Le fichier `decisions.md` conserve le journal historique. Une décision structurante volumineuse peut être portée par un fichier `Dxxx-*.md`, référencé par l'index et par le journal lors de sa prochaine consolidation.

Une ancienne décision gelée n'est jamais réécrite pour masquer l'historique.

### `docs/toy-models/toyN/`

Documentation propre à un modèle jouet : spécification, conception d'implémentation, plan de validation et clôture.

### `experiments/toyN/`

Manifestes et protocoles d'exécution pré-enregistrés.

### `schemas/toyN/`

Contrats de sérialisation versionnés.

### `features/`

Propositions temporaires non gelées. Après validation, leur contenu est migré vers les emplacements fonctionnels puis le brouillon est supprimé.

## 4. Hiérarchie des sources

En cas de divergence :

1. décision gelée la plus récente ;
2. manifeste pré-enregistré pour les valeurs propres à une campagne ou une expérience ;
3. spécification du modèle jouet concerné ;
4. hypothèse C générale (`docs/model/`) ;
5. plan de validation ;
6. schéma de données ;
7. index et README ;
8. document exploratoire.

Cette hiérarchie sert à résoudre temporairement la divergence ; la contradiction doit ensuite être corrigée.

## 5. Statuts

```text
brouillon
revue en cours
validé pour gel
gelé
clos
supersédé
archivé
```

Un document ne peut être gelé si une contradiction de statut ou de valeur subsiste.

## 6. Non-duplication

Les documents secondaires utilisent un renvoi vers la source principale. Les résumés sont autorisés s'ils sont clairement identifiés comme tels et mis à jour dans le même paquet lorsqu'ils changent de sens.

## 7. Modification d'une norme gelée

Toute modification de sens exige :

1. une nouvelle décision ;
2. la mise à jour de la spécification concernée ;
3. la mise à jour du manifeste et du plan de validation si nécessaire ;
4. une nouvelle version de schéma en cas d'incompatibilité ;
5. la mise à jour des index et renvois.

Une correction éditoriale sans changement de sens ne nécessite pas de décision.

## 8. Compatibilité des anciens chemins

Lors d'une migration, un ancien chemin peut être conservé temporairement comme fichier de redirection marqué `supersédé`.

Ce fichier :

- ne contient aucune définition normative ;
- indique uniquement le nouveau chemin canonique ;
- n'est jamais utilisé dans un nouveau document ;
- est supprimé après vérification que plus aucun outil ou document actif ne le référence.

## 9. Contrôle avant publication documentaire

Avant de déclarer une migration terminée :

- vérifier la présence réelle des nouveaux fichiers ;
- vérifier que les anciens chemins ne contiennent plus de source normative dupliquée ;
- vérifier les statuts et valeurs gelées ;
- vérifier les liens des README et index ;
- vérifier le diff global fichier par fichier ;
- identifier explicitement les fichiers de compatibilité restants ;
- fournir le SHA final.

Un succès d'API Git ou une mise à jour de référence ne prouve pas à lui seul que le contenu annoncé est présent.

## 10. État actuel des sources canoniques

L'arborescence réelle est alignée avec la cible du §2. Les sources canoniques sont :

```text
README.md
docs/model/c-hypothesis.md                       — gelé conceptuellement
docs/toy-models/toy0/specification.md             — gelé conceptuellement
docs/toy-models/toy0/implementation-design.md     — gelé, implémentation non démarrée
```

Aucun ancien chemin (`docs/C-HYPOTHESIS.md`, `docs/TOY-MODEL-0.md`, `docs/IMPLEMENTATION-0A.md`) n'est conservé comme fichier de compatibilité au sens du §8 : ces documents n'avaient encore aucune référence externe active, la migration s'est donc faite par renommage direct plutôt que par redirection temporaire.
