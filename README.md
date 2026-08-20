# Cosmobox C Model

Dépôt de recherche consacré à l'hypothèse **C** : tester si une structure géométrique effective peut être reconstruite à partir de propriétés quantiques relationnelles, sans postuler d'emblée une métrique continue.

## Statut

Ce dépôt contient un **programme exploratoire** et des modèles jouets. Il ne présente pas une théorie physique établie.

Le benchmark analytique **Toy Model 0A est clos**. Il valide l'instrument logiciel d'identifiabilité (construction du secteur physique, observables invariantes de jauge, matrice de mesure, SVD, rang, noyau, projecteur et conditionnement) sur un cas dont les résultats sont connus analytiquement à l'avance. Il ne constitue pas un résultat scientifique exploratoire sur l'hypothèse C.

Le travail est volontairement séparé du dépôt principal Cosmobox afin de pouvoir tester l'hypothèse C avec ses propres postulats, critères d'échec et observables.

## Idée directrice

L'hypothèse de travail est qu'une particule élémentaire possède un état géométrique local noté `C`, dont la manifestation physique dépend de son environnement quantique collectif.

Dans sa forme conceptuelle actuelle :

- `C` représente la géométrie spatiale associée à une unité locale de temps ;
- `C = 1` est une normalisation de référence associée à la borne causale locale `c`, et non l'affirmation d'un vide absolu ;
- la matière et l'état quantique collectif peuvent modifier la géométrie interne de `C` ;
- `C` ne produit pas la mécanique quantique : il en constitue une représentation géométrique hypothétique ;
- les quantités directement testables doivent être relationnelles, adimensionnelles et invariantes de jauge ;
- la géométrie macroscopique est recherchée comme structure effective issue de l'organisation collective de ces relations.

Une première quantité opérationnelle candidate entre deux constituants ou régions `p` et `q` est un rapport de temps d'arrivée :

```text
C_eff(p,q) = T_ref(p,q) / T_state(p,q)
```

Cette définition n'est pas encore postulée comme fondamentale ; elle constitue une sonde minimale à tester dans un modèle jouet.

## Documents

- `docs/model/c-hypothesis.md` — définition conceptuelle consolidée de l'hypothèse C.
- `docs/toy-models/toy0/specification.md` — cahier des charges du premier modèle jouet relationnel.
- `docs/toy-models/toy0/implementation-design.md` — contrat technique d'implémentation du benchmark 0A.
- `docs/toy-models/toy0/closure-report.md` — résultats d'acceptation, limites et décision de clôture de 0A.
- `docs/governance/` — règles de collaboration, de documentation et d'architecture logicielle du dépôt.

## Principe méthodologique

Le dépôt suit une règle simple :

> intuition physique → contraintes conceptuelles → définition opérationnelle → calcul → falsification.

Les outils mathématiques ne doivent pas fixer a priori la signification physique de `C`.
