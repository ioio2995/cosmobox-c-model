# Toy Model 0 — cahier des charges

## 1. Question testée

Le Toy Model 0 doit répondre à une question centrale :

> **Un état quantique collectif peut-il fournir une grandeur relationnelle physique, robuste et invariante de jauge, dont certaines propriétés peuvent être sondées par une quantité opérationnelle \(C_{\mathrm{eff}}\), et dont l’organisation peut éventuellement être interprétée géométriquement sans introduire cette géométrie dans sa définition ?**

Le modèle doit être assez petit pour être calculé exactement et assez riche pour contenir :

- des degrés de liberté de matière ;
- des degrés de liberté de jauge ;
- des observables invariantes de jauge ;
- une notion de perturbation locale ;
- une propagation mesurable par corrélations ;
- un état de référence et des états perturbés ;
- plusieurs relations \((p,q)\) permettant de tester l’identifiabilité et l’organisation collective.

Le Toy Model 0 doit maintenir une séparation stricte entre :

```math
C^{(pq)}
```

qui désigne une **grandeur relationnelle physique candidate** issue de l’état quantique, et :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}
```

qui désigne une **sonde opérationnelle relative** construite à partir d’un temps caractéristique de propagation.

La correspondance entre ces deux objets est un résultat à tester et non une identité posée par définition.

---

## 2. Non-objectifs

Le Toy Model 0 ne cherche pas encore à :

- reproduire toute la relativité générale ;
- construire un espace-temps continu ;
- faire émerger la topologie du graphe ;
- quantifier la gravité ;
- dériver la mécanique quantique ;
- démontrer l’invariance locale de \(c\) ;
- traiter la covariance relativiste complète ;
- postuler d’emblée un tenseur tridimensionnel \(C_{ij}\) ;
- ajuster des paramètres pour reproduire Schwarzschild.

Le modèle doit au contraire permettre à l’hypothèse \(C\) d’échouer tôt.

---

## 3. Structure minimale

On considère un graphe fini :

```math
G=(V,E).
```

où :

- les nœuds \(p\in V\) portent les degrés de liberté de matière ;
- les liens \((p,q)\in E\) portent les degrés de liberté de jauge ;
- la connectivité est imposée ;
- cette connectivité n’est pas interprétée comme une distance physique fondamentale.

Le Hamiltonien doit être invariant de jauge et suffisamment simple pour permettre une diagonalisation exacte ou une évolution temporelle exacte sur de petites tailles.

Pour l’implémentation initiale, la base privilégiée est un **modèle fini U(1)** déjà maîtrisé dans Cosmobox. Ce choix est méthodologique : il permet de tester l’hypothèse \(C\) sans rouvrir simultanément le problème du choix d’une nouvelle théorie de jauge.

Une structure plus minimale ne devra être retenue que si elle conserve les observables relationnelles et les contraintes nécessaires au test.

---

## 4. Étape 0 — identifiabilité de la structure relationnelle

Avant toute définition de \(C_{\mathrm{eff}}\), le modèle doit déterminer si l’information relationnelle recherchée est effectivement identifiable à partir des observables invariantes de jauge accessibles.

La question préalable est :

```math
\text{états physiquement distincts}
\stackrel{?}{\longrightarrow}
\text{signatures relationnelles distinguables}.
```

Pour une famille d’observables choisie, plusieurs états physiquement distincts peuvent produire exactement les mêmes données relationnelles observables.

Dans ce cas, la structure recherchée n’est pas identifiable avec cette famille de sondes.

L’analyse devra notamment :

- identifier les secteurs du modèle qui sont distinguables par les observables retenues ;
- identifier les secteurs qui ne le sont pas ;
- vérifier si des corrélations inter-secteurs sont nécessaires à la reconstruction ;
- enregistrer l’absence de telles corrélations comme une limitation ou un résultat négatif, et non la compenser par l’introduction de variables non observables.

Le Toy Model 0 ne doit poursuivre la construction d’un \(C^{(pq)}\) dans un secteur que si une information relationnelle suffisamment robuste y est effectivement identifiable.

---

## 5. États étudiés

Deux familles d’états sont nécessaires.

### 5.1 État de référence

Un état :

```math
|\Psi_{\mathrm{ref}}\rangle
```

ou, plus généralement, une matrice de densité :

```math
\rho_{\mathrm{ref}}
```

définit l’état de comparaison opérationnel.

Pour une relation donnée \((p,q)\), la sonde est normalisée par construction à :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}=1
```

lorsque l’état étudié est lui-même l’état de référence.

Cet état n’est pas supposé représenter un « vide absolu » ni un état causal maximal.

### 5.2 États perturbés

On construit des états :

```math
|\Psi_{\lambda}\rangle
```

ou des matrices de densité \(\rho_\lambda\), et éventuellement des Hamiltoniens perturbés \(H_\lambda\), où \(\lambda\) contrôle un changement physique identifiable : énergie locale, occupation de matière, couplage, configuration de jauge ou autre perturbation invariante de jauge.

Le paramètre \(\lambda\) ne doit pas être interprété a priori comme une densité géométrique ni comme une valeur de \(C\).

---

## 6. Observable relationnelle primaire

Le modèle doit partir d’une observable à deux points, invariante de jauge :

```math
G_{pq}(t).
```

Sa définition exacte reste à sélectionner.

Elle doit satisfaire au minimum :

1. invariance de jauge ;
2. sens physique clair ;
3. réponse mesurable à une perturbation locale ;
4. capacité à comparer plusieurs paires \((p,q)\) ;
5. robustesse suffisante pour définir une dynamique relationnelle ;
6. capacité à participer au test d’identifiabilité de la section 4.

Des candidats possibles sont des corrélateurs de matière reliés par un transporteur de jauge, ou d’autres observables relationnelles déjà utilisées dans les niveaux précédents de Cosmobox.

La grandeur relationnelle candidate \(C^{(pq)}\) ne doit pas être identifiée d’emblée à \(G_{pq}\). Il faudra déterminer si une fonction de ces observables ou de leurs corrélations peut jouer ce rôle :

```math
\rho_{\mathrm{ensemble}}
\rightarrow
\text{observables invariantes}
\stackrel{?}{\longrightarrow}
C^{(pq)}.
```

---

## 7. Paramètre d’évolution et temps d’arrivée relationnel

Pour chaque paire \((p,q)\), on construit un temps caractéristique à partir de \(G_{pq}(t)\).

Le paramètre \(t\) utilisé dans le Toy Model 0 est **le paramètre d’évolution externe du modèle de calcul**. Dans une évolution hamiltonienne, il pourra par exemple apparaître dans :

```math
|\Psi(t)\rangle
=
e^{-iHt/\hbar}
|\Psi(0)\rangle.
```

Ce paramètre ne doit pas être identifié au temps local que l’hypothèse \(C\) cherche éventuellement à faire émerger.

La construction de \(T_{pq}\) est donc limitée au premier modèle à évolution temporelle fixée. Elle devra être reformulée avant tout test de covariance relativiste ou toute tentative de définition du temps local émergent.

Deux définitions devront au minimum être comparées.

### 7.1 Franchissement de seuil

```math
T^{\mathrm{thr}}_{pq}
=
\inf\left\{
t\mid
\Delta G_{pq}(t)\geq\eta
\right\}.
```

où \(\eta\) est un seuil défini de manière reproductible.

### 7.2 Maximum de croissance

```math
T^{\mathrm{grow}}_{pq}
=
\operatorname*{arg\,max}_t
\frac{d}{dt}\Delta G_{pq}(t).
```

Aucune de ces définitions ne doit être déclarée fondamentale avant comparaison de leur stabilité, de leur sens physique et de leur robustesse numérique.

D’autres définitions pourront être introduites seulement si elles apportent un critère opérationnel distinct et préenregistré avant comparaison des résultats.

---

## 8. Sonde opérationnelle relative \(C_{\mathrm{eff}}\)

Pour une même paire \((p,q)\), on compare l’état étudié à l’état de référence :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}
=
\frac{T^{\mathrm{ref}}_{pq}}
     {T^{\mathrm{state}}_{pq}}.
```

Cette quantité est :

- adimensionnelle ;
- relationnelle ;
- explicitement dépendante du choix de référence ;
- normalisée à \(1\) dans l’état de référence ;
- calculable sans introduire une distance métrique préalable.

Si :

```math
T^{\mathrm{state}}_{pq}
>
T^{\mathrm{ref}}_{pq},
```

alors :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}<1.
```

À l’inverse, si l’état étudié présente un temps caractéristique plus court que la référence :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}>1
```

est possible sans impliquer :

```math
C>1.
```

La sonde \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\) mesure une **modification globale de la relation causale** entre \(p\) et \(q\).

Elle ne sépare pas a priori :

```math
\text{variation de vitesse}
\qquad\text{et}\qquad
\text{variation de longueur ou de structure effective}.
```

Dans le cadre relationnel, cette séparation peut elle-même ne devenir pertinente qu’après reconstruction d’une géométrie effective.

---

## 9. Barrière entre \(C^{(pq)}\) et \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\)

La sonde opérationnelle ne constitue pas la définition fondamentale de \(C\).

Le Toy Model 0 doit tester explicitement la correspondance :

```math
C^{(pq)}
\stackrel{?}{\longleftrightarrow}
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}.
```

Une variation de \(C_{\mathrm{eff}}\) n’est pertinente pour l’hypothèse \(C\) que si elle suit de manière robuste une propriété relationnelle physique extraite de l’état quantique.

Le test doit notamment vérifier :

- stabilité de la correspondance sous changement de référence ;
- stabilité sous petites perturbations de l’état ;
- invariance de jauge ;
- cohérence du classement des relations entre plusieurs définitions de \(T_{pq}\) ;
- absence de dépendance dominante à un artefact de connectivité ou de seuil.

Si cette correspondance échoue, le Toy Model 0 ne doit pas passer directement à une interprétation géométrique de \(C_{\mathrm{eff}}\).

---

## 10. Contrôle de circularité

Le graphe possède une connectivité donnée.

Il est donc interdit d’interpréter automatiquement :

- le nombre de liens ;
- la distance de graphe ;
- les coordonnées d’affichage ;
- la position d’un nœud dans une représentation graphique ;

comme une géométrie physique émergente.

Le premier test porte uniquement sur la possibilité de reconstruire une structure géométrique **effective sur une topologie imposée**.

Toute comparaison avec la distance de graphe doit être utilisée comme diagnostic externe, jamais comme ingrédient de la définition de \(C^{(pq)}\) ou de \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\).

---

## 11. Reconstruction géométrique

La reconstruction géométrique ne peut être entreprise qu’après les deux étapes suivantes :

```math
\rho_{\mathrm{ensemble}}
\stackrel{?}{\longrightarrow}
C^{(pq)}
```

et :

```math
C^{(pq)}
\stackrel{?}{\longleftrightarrow}
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}.
```

À partir de l’ensemble des relations candidates :

```math
\{C^{(pq)}\},
```

le modèle doit alors tester si une structure géométrique cohérente peut être reconstruite.

Cette étape ne doit pas présupposer un tenseur tridimensionnel.

Trois résultats principaux sont possibles.

### A. Aucune géométrie stable

Les relations candidates ne satisfont pas les propriétés nécessaires à une interprétation métrique ou quasi-métrique.

C’est un résultat négatif valide.

### B. Géométrie relationnelle scalaire

Les relations définissent une notion cohérente de coût, de proximité ou de distance effective, mais aucune structure tensorielle locale identifiable.

Cela restreint l’hypothèse d’une représentation locale \(C_{ij}\).

### C. Structure locale anisotrope reconstructible

Les relations autour d’un nœud présentent suffisamment de structure pour reconstruire un objet local se comportant comme une forme quadratique ou un tenseur effectif.

Dans ce cas seulement, on pourra introduire explicitement une notation du type :

```math
C^{(p)}_{ij}.
```

---

## 12. Critères de cohérence d’une géométrie effective

Une reconstruction candidate devra être testée au minimum sur :

- positivité du coût relationnel lorsqu’un coût est défini ;
- symétrie ou asymétrie contrôlée de \(C^{(pq)}\) et \(C^{(qp)}\) ;
- stabilité sous changement de jauge ;
- composition cohérente sur plusieurs relations ;
- robustesse aux petites perturbations de l’état ;
- comportement homogène dans les états symétriques ;
- capacité à identifier une anisotropie lorsqu’elle est physiquement introduite ;
- indépendance vis-à-vis des coordonnées graphiques du graphe.

Si une distance effective est construite, l’inégalité triangulaire ne doit pas être imposée par définition : elle doit être testée.

---

## 13. Expériences minimales

### Expérience 0A — identifiabilité

Construire plusieurs états physiquement distincts et déterminer si la famille d’observables invariantes retenue permet effectivement de les distinguer.

Objectif : déterminer dans quels secteurs une grandeur relationnelle candidate peut être reconstruite.

Un échec local d’identifiabilité doit être conservé comme résultat.

### Expérience 0B — référence homogène

Construire un état symétrique et vérifier que les relations équivalentes donnent des signatures relationnelles et des \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\) compatibles.

Objectif : établir la normalisation, les symétries attendues et le bruit numérique intrinsèque.

### Expérience 1 — perturbation locale

Modifier localement un paramètre physique ou l’état de matière et mesurer la réponse de \(G_{pq}(t)\), de \(T_{pq}\) et de \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\).

Objectif : vérifier qu’une perturbation quantique locale produit une réponse relationnelle mesurable.

### Expérience 2 — monotonie

Faire varier progressivement l’intensité de la perturbation.

Objectif : tester, et non supposer, si une perturbation croissante entraîne une variation monotone de la grandeur relationnelle candidate ou de sa sonde \(C_{\mathrm{eff}}\).

### Expérience 3 — anisotropie

Introduire une perturbation qui brise volontairement une symétrie entre plusieurs relations autour d’un même nœud.

Objectif : déterminer si les observables relationnelles et \(C_{\mathrm{eff}}\) détectent cette brisure, puis si une structure directionnelle peut être reconstruite sans imposer un tenseur.

### Expérience 4 — chemins multiples, diffusion et retard

Choisir une topologie comportant plusieurs routes relationnelles entre deux régions.

Objectif : observer si la dynamique produit quantitativement :

- un front principal ;
- des contributions secondaires ;
- une redistribution ;
- des retards ;
- des interférences éventuelles.

Aucun « chemin le plus court » ne doit être imposé comme règle fondamentale.

Les contributions diffuses ou retardées doivent être prédites par la dynamique et non invoquées après coup pour expliquer un écart.

---

## 14. Critères d’échec du Toy Model 0

Le Toy Model 0 doit être considéré comme négatif, non concluant ou limité dans un secteur si, par exemple :

- l’information relationnelle n’est pas identifiable avec les observables invariantes disponibles ;
- \(T_{pq}\) dépend fortement d’un choix arbitraire de seuil ;
- les différentes définitions de temps d’arrivée donnent des classements incompatibles ;
- \(C_{\mathrm{eff}}\) dépend d’une variable de jauge non physique ;
- \(C_{\mathrm{eff}}\) ne suit aucune propriété relationnelle robuste pouvant être associée à \(C^{(pq)}\) ;
- la valeur extraite est essentiellement déterminée par la connectivité imposée ;
- aucune réponse stable à une perturbation physique n’apparaît ;
- la reconstruction géométrique exige d’injecter les coordonnées que l’on prétend faire émerger ;
- le caractère tensoriel doit être imposé à la main pour obtenir le résultat attendu ;
- diffusion ou retard ne peuvent être obtenus quantitativement alors qu’ils sont nécessaires pour interpréter les résultats.

Un échec d’une définition particulière de \(T_{pq}\) ou d’une observable candidate n’invalide pas automatiquement l’hypothèse \(C\), mais il doit éliminer cette construction précise.

---

## 15. Ce que le Toy Model 0 peut établir

Un résultat positif pourrait établir seulement ceci :

> Sur une topologie quantique donnée, certaines observables relationnelles invariantes de jauge permettent d’identifier une structure relationnelle candidate \(C^{(pq)}\), et une sonde opérationnelle adimensionnelle \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\) en suit certaines propriétés de manière robuste ; l’organisation de ces relations peut alors être testée pour une interprétation géométrique effective.

Il ne démontrerait pas que :

- \(C\) est une propriété fondamentale de la nature ;
- l’espace réel émerge de cette manière ;
- la topologie elle-même émerge ;
- la gravité est dérivée ;
- \(c_{\mathrm{local}}=c\) est automatiquement expliqué ;
- le continuum relativiste est obtenu ;
- \(C_{\mathrm{eff}}\) est une observable covariante valable au-delà du cadre temporel fixé du Toy Model 0.

---

## 16. Étape suivante conditionnelle

On ne passera à un Toy Model 1 que si le Toy Model 0 fournit simultanément :

1. une information relationnelle identifiable ;
2. une grandeur candidate \(C^{(pq)}\) suffisamment robuste ;
3. une sonde \(C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}\) dont la correspondance avec cette grandeur est établie dans le domaine étudié ;
4. au moins une organisation collective suffisamment stable pour justifier l’étude d’une reconstruction géométrique plus ambitieuse.

Le Toy Model 1 pourrait alors étudier :

- la reconstruction locale d’un objet tensoriel ;
- une limite de grande taille ou un coarse-graining ;
- l’apparition d’une métrique effective ;
- une reformulation de la sonde sans temps externe privilégié ;
- les premières contraintes de covariance ;
- une comparaison avec les limites gravitationnelles faibles.

---

## 17. Chaînes de calcul cibles

Le Toy Model 0 comporte deux chaînes complémentaires.

### 17.1 Chaîne conceptuelle

```math
\rho_{\mathrm{ensemble}}
\rightarrow
\text{observables et corrélations invariantes de jauge}
\stackrel{?}{\longrightarrow}
C^{(pq)}
\stackrel{?}{\longrightarrow}
C^{(p)}\ \text{ou}\ C^{(p)}_{ij}
\stackrel{?}{\longrightarrow}
\text{géométrie effective}.
```

### 17.2 Chaîne opérationnelle

```math
\rho_{\mathrm{ensemble}}
\rightarrow
G_{pq}(t)
\rightarrow
T_{pq}
\rightarrow
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}.
```

La liaison entre les deux chaînes constitue l’un des tests centraux :

```math
C_{\mathrm{eff}}^{(pq\mid\mathrm{ref})}
\stackrel{?}{\longleftrightarrow}
C^{(pq)}.
```

Les points d’interrogation font partie du protocole expérimental. Ils ne doivent pas être supprimés par construction.
