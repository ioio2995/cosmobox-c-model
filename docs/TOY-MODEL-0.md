# Toy Model 0 — cahier des charges

## 1. Question testée

Le premier modèle jouet doit répondre à une seule question :

> **Un état quantique relationnel peut-il définir une quantité `C` opérationnelle, puis une structure géométrique effective, sans imposer cette géométrie dans la définition de `C` ?**

Le modèle doit être assez petit pour être calculé exactement et assez riche pour contenir :

- des degrés de liberté de matière ;
- des degrés de liberté de jauge ;
- des observables invariantes de jauge ;
- une notion de perturbation locale ;
- une propagation mesurable par corrélations ;
- un état de référence et un état perturbé.

---

## 2. Non-objectifs

Le Toy Model 0 ne cherche pas encore à :

- reproduire toute la relativité générale ;
- construire un espace-temps continu ;
- faire émerger la topologie du graphe ;
- quantifier la gravité ;
- dériver la mécanique quantique ;
- postuler d'emblée un tenseur tridimensionnel `C_ij` ;
- ajuster des paramètres pour reproduire Schwarzschild.

Le modèle doit au contraire permettre à l'hypothèse de `C` d'échouer tôt.

---

## 3. Structure minimale

On considère un graphe fini

\[
G=(V,E),
\]

où :

- les nœuds `p ∈ V` portent les degrés de liberté de matière ;
- les liens `(p,q) ∈ E` portent les degrés de liberté de jauge ;
- la connectivité est imposée et n'est pas interprétée comme une distance physique fondamentale.

Le Hamiltonien doit être invariant de jauge et suffisamment simple pour permettre une diagonalisation exacte ou une évolution temporelle exacte sur de petites tailles.

Le choix précis du groupe de jauge et des espaces locaux reste ouvert au démarrage. Un modèle U(1) fini est une option naturelle car il permet de réutiliser des méthodes déjà éprouvées dans Cosmobox, mais il ne doit pas être imposé si une structure encore plus minimale suffit.

---

## 4. États étudiés

Deux familles d'états sont nécessaires.

### 4.1 État de référence

Un état

\[
|\Psi_{\mathrm{ref}}\rangle
\]

fixe la normalisation opérationnelle

\[
C^{(pq)}_{\mathrm{eff}}=1
\]

pour la relation considérée lorsqu'aucune perturbation supplémentaire n'est introduite.

Cet état de référence ne représente pas un « vide absolu ».

### 4.2 États perturbés

On construit des états

\[
|\Psi_{\lambda}\rangle
\]

ou des Hamiltoniens perturbés `H_λ`, où `λ` contrôle un changement physique identifiable : énergie locale, occupation de matière, couplage, configuration de jauge ou autre perturbation invariante de jauge.

Le paramètre `λ` ne doit pas être interprété a priori comme une densité géométrique.

---

## 5. Observable relationnelle primaire

Le modèle doit partir d'une observable à deux points, invariante de jauge :

\[
G_{pq}(t).
\]

Sa définition exacte reste à sélectionner.

Elle doit satisfaire au minimum :

1. invariance de jauge ;
2. sens physique clair ;
3. réponse mesurable à une perturbation locale ;
4. capacité à comparer plusieurs paires `(p,q)` ;
5. robustesse suffisante pour définir un temps d'arrivée.

Des candidats possibles sont des corrélateurs de matière reliés par un transporteur de jauge, ou d'autres observables relationnelles déjà utilisées dans les niveaux précédents de Cosmobox.

---

## 6. Temps d'arrivée relationnel

Pour chaque paire `(p,q)`, on définit un temps d'arrivée à partir de `G_pq(t)`.

Deux définitions devront au minimum être comparées :

### 6.1 Franchissement de seuil

\[
T^{\mathrm{thr}}_{pq}
=
\inf\{t\mid \Delta G_{pq}(t) \ge \eta\},
\]

où `η` est un seuil défini de manière reproductible.

### 6.2 Maximum de croissance

\[
T^{\mathrm{grow}}_{pq}
=
\operatorname*{arg\,max}_t
\frac{d}{dt}\Delta G_{pq}(t).
\]

Aucune des deux définitions ne doit être déclarée fondamentale avant comparaison de leur stabilité et de leur sens physique.

---

## 7. Première définition opérationnelle de C

Pour une même paire `(p,q)`, on compare l'état étudié à l'état de référence :

\[
\boxed{
C^{(pq)}_{\mathrm{eff}}
=
\frac{T^{\mathrm{ref}}_{pq}}
     {T^{\mathrm{state}}_{pq}}
}
\]

Cette quantité est :

- adimensionnelle ;
- relationnelle ;
- normalisée à `1` dans l'état de référence ;
- calculable sans introduire une distance métrique préalable.

Si

\[
T^{\mathrm{state}}_{pq}>T^{\mathrm{ref}}_{pq},
\]

alors

\[
C^{(pq)}_{\mathrm{eff}}<1.
\]

Cette définition est une **sonde de C**, pas encore une définition fondamentale de l'objet conceptuel `C`.

---

## 8. Contrôle de circularité

Le graphe possède une connectivité donnée. Il est donc interdit d'interpréter automatiquement le nombre de liens, la distance de graphe ou les coordonnées d'affichage comme une géométrie physique émergente.

Le premier test porte sur la possibilité de reconstruire une structure métrique **effective sur une topologie imposée**.

Toute comparaison avec une distance de graphe doit être présentée comme un diagnostic externe, pas comme un ingrédient de la définition de `C`.

---

## 9. Reconstruction géométrique

À partir de l'ensemble

\[
\{C^{(pq)}_{\mathrm{eff}}\},
\]

le modèle doit tester si une structure géométrique cohérente peut être reconstruite.

Cette étape ne doit pas présupposer un tenseur 3D.

Trois résultats sont possibles :

### A. Aucune géométrie stable

Les `C^(pq)` ne satisfont pas les propriétés nécessaires à une interprétation métrique ou quasi-métrique.

C'est un résultat négatif valide.

### B. Géométrie relationnelle scalaire

Les relations définissent une notion cohérente de coût ou de distance effective, mais aucune structure tensorielle locale identifiable.

Cela réfute ou restreint l'hypothèse forte d'un `C_ij` porté localement par chaque particule.

### C. Structure locale anisotrope reconstructible

Les relations autour d'un nœud présentent suffisamment de structure pour reconstruire un objet local qui se comporte comme une forme quadratique ou un tenseur effectif.

Dans ce cas seulement on introduira explicitement une notation du type

\[
C^{(p)}_{ij}.
\]

---

## 10. Critères de cohérence d'une géométrie effective

Une reconstruction candidate devra être testée au minimum sur :

- positivité du coût relationnel ;
- symétrie ou asymétrie contrôlée de `C^(pq)` et `C^(qp)` ;
- stabilité sous changement de base de jauge ;
- composition cohérente sur plusieurs relations ;
- robustesse aux petites perturbations de l'état ;
- comportement homogène dans les états symétriques ;
- capacité à identifier une anisotropie lorsqu'elle est physiquement introduite.

Si une distance effective est construite, l'inégalité triangulaire ne doit pas être imposée par définition : elle doit être testée.

---

## 11. Expériences minimales

### Expérience 0 — référence homogène

Construire un état symétrique et vérifier que les paires équivalentes donnent des `C_eff` compatibles entre elles.

Objectif : établir la normalisation et le bruit numérique intrinsèque.

### Expérience 1 — perturbation locale

Modifier localement un paramètre physique ou l'état de matière et mesurer la variation de `T_pq` et `C_eff^(pq)`.

Objectif : vérifier qu'une perturbation quantique locale produit une réponse relationnelle mesurable.

### Expérience 2 — monotonie

Faire varier progressivement l'intensité de la perturbation.

Objectif : tester, et non supposer, si une perturbation croissante entraîne effectivement une diminution monotone de `C_eff`.

### Expérience 3 — anisotropie

Introduire une perturbation qui brise volontairement une symétrie entre plusieurs relations autour d'un même nœud.

Objectif : déterminer si les `C_eff^(pq)` permettent de détecter et de reconstruire une structure directionnelle.

### Expérience 4 — chemins multiples

Choisir une topologie comportant plusieurs routes relationnelles entre deux régions.

Objectif : observer comment les temps d'arrivée et les corrélations se répartissent et s'interfèrent sans imposer un « chemin le plus court » comme règle fondamentale.

---

## 12. Critères d'échec du Toy Model 0

Le modèle doit être considéré comme non concluant ou négatif si, par exemple :

- `T_pq` dépend fortement d'un choix arbitraire de seuil ;
- les différentes définitions de temps d'arrivée donnent des classements incompatibles ;
- `C_eff` dépend d'une variable de jauge non physique ;
- la valeur extraite est essentiellement déterminée par la connectivité imposée ;
- aucune réponse stable à une perturbation physique n'apparaît ;
- la reconstruction géométrique exige d'injecter les coordonnées que l'on prétend faire émerger ;
- le caractère tensoriel doit être imposé à la main pour obtenir le résultat attendu.

---

## 13. Ce que le Toy Model 0 peut établir

Un résultat positif pourrait établir seulement ceci :

> Sur une topologie quantique donnée, certaines observables relationnelles invariantes de jauge permettent de construire une quantité adimensionnelle `C_eff` dont l'organisation se comporte comme une géométrie effective.

Il ne démontrerait pas que :

- `C` est une propriété fondamentale de la nature ;
- l'espace réel émerge de cette manière ;
- la gravité est dérivée ;
- `c_local = c` est automatiquement expliqué ;
- le continuum relativiste est obtenu.

---

## 14. Étape suivante conditionnelle

On ne passera à un Toy Model 1 que si le Toy Model 0 fournit une observable `C_eff` suffisamment robuste.

Le Toy Model 1 pourrait alors étudier :

1. la reconstruction locale d'un objet tensoriel ;
2. une limite de grande taille / coarse-graining ;
3. l'apparition d'une métrique effective ;
4. les premières contraintes de covariance ;
5. une comparaison avec les limites gravitationnelles faibles.

---

## 15. Chaîne de calcul cible

\[
\boxed{
|\Psi\rangle
\rightarrow
G_{pq}(t)
\rightarrow
T_{pq}
\rightarrow
C^{(pq)}_{\mathrm{eff}}
\rightarrow
\text{géométrie effective ?}
\rightarrow
C^{(p)}_{ij}\ ?
}
\]

Les deux points d'interrogation font partie du protocole expérimental. Ils ne doivent pas être supprimés par construction.
