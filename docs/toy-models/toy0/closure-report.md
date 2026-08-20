# Toy Model 0A — Rapport de clôture

**Statut : clos**  
**Projet :** Cosmobox C Model  
**Dépôt :** `ioio2995/cosmobox-c-model`  
**Branche de clôture :** `closure/model0a`  
**Merge d'implémentation sur `master` :** `fbd6f0967460153dcacd39656808db843c7a675a`  
**Dernier commit d'implémentation revu :** `a5fc55563db7ee7b06a41e4bfb6b0c8a928f960f`  
**Date de clôture :** 20 août 2026

---

## 1. Objet de la clôture

Le benchmark analytique Toy Model 0A est clôturé après :

1. spécification scientifique et contrat d'implémentation gelés ;
2. audit fonctionnel et audit architectural acceptés ;
3. implémentation complète sur une architecture `core/` + `models/model0a/` ;
4. deux cycles de revue distante et correctifs ciblés ;
5. revue distante finale `PASS` ;
6. fusion de la branche d'implémentation dans `master` ;
7. acceptation finale du lot par Lionel ORCIL.

0A est un benchmark analytique de validation de l'instrument d'identifiabilité. Il ne constitue pas un résultat scientifique exploratoire sur l'hypothèse C.

---

## 2. Architecture retenue

La première bibliothèque commune progressive du dépôt est maintenant structurée autour de :

```text
src/cosmobox_c_model/core/
    state_space
    fermions
    ladder
    operators
    identifiability

src/cosmobox_c_model/models/model0a/
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

Les invariants `core -X-> models` et `tests/core -X-> models` sont testés automatiquement.

---

## 3. Résultats d'acceptation

La suite finale comporte :

```text
89 tests passants
```

Le runner :

```text
python3 scripts/run_0a_benchmark.py
```

reproduit les résultats gelés suivants :

```text
dimension totale             = 72
dimension physique           = 3
rang F1                      = 2
rang F2                      = 6
rang F3                      = 8
dimension noyau F2           = 2
rang F2_prime                = 8
rangs F_delta                = 2,2,2,2,2,1,1
||O_01 O_12 - O_02||_F      = 2.0
```

Le témoin Jordan-Wigner vérifie exactement :

```math
O_{01}O_{12}|\chi\rangle=0,
```

et :

```math
O_{02}|\chi\rangle=-|110;+1,0\rangle.
```

Deux exécutions successives du benchmark produisent un rapport JSON byte-identique.

---

## 4. Ce que 0A valide

0A valide techniquement la chaîne suivante :

```text
modèle fini
→ contraintes de Gauss
→ secteur physique
→ observables invariantes de jauge
→ matrice de mesure
→ SVD directe
→ rang numérique
→ noyau
→ projecteur de noyau
→ conditionnement
```

Le moteur distingue correctement :

- rang structurel connu et rang numérique au seuil ;
- spectre singulier brut et spectre complété sur le domaine ;
- noyau et projecteur de noyau ;
- conditionnement sur le support résolu ;
- régime instrumental mal conditionné via `F_delta`.

Dans le secteur physique minimal de 0A, la famille de premier ordre locale et adjacente `F2` possède un noyau réel de dimension deux correspondant à la cohérence complexe `L <-> R`. L'ajout de `X_02,Y_02` rend `F3` informationnellement complète.

Dans ce secteur particulier :

```math
P_{\mathrm{phys}}O_{01}O_{12}P_{\mathrm{phys}}
=
P_{\mathrm{phys}}O_{02}P_{\mathrm{phys}}.
```

`F2_prime` confirme uniquement la cohérence du pipeline et ne constitue pas un résultat scientifique indépendant.

---

## 5. Limites explicites

0A ne permet pas de conclure que :

- une relation non adjacente porte une information fondamentalement irréductible aux relations adjacentes ;
- une relation étendue est généralement équivalente à une composition de relations locales ;
- un degré de liberté physique autonome du champ de jauge a été identifié ;
- `C` ou `C_eff` ont été définis ou identifiés ;
- une métrique, une distance, un temps émergent ou une géométrie effective ont été reconstruits ;
- le conditionnement de 0A constitue une mesure universelle de robustesse physique.

La chaîne `0-1-2` est un arbre. Avec les contraintes de Gauss et les flux de bord fixés, 0A ne contient pas de degré de liberté de jauge physique indépendant de la matière.

---

## 6. Incidents de revue désormais fermés

Les revues distantes ont notamment permis de fermer les points suivants :

- séparation stricte entre oracles et production ;
- usage exact des tolérances préenregistrées ;
- norme de Frobenius pour B04 ;
- validation effective de `SCIENTIFIC_METADATA` ;
- rejet explicite des matrices incompatibles par `action_from_matrix()` ;
- comparaison exacte du témoin Jordan-Wigner ;
- découverte du secteur physique indépendante de l'orientation arbitraire d'une base SVD dégénérée.

Aucun de ces points ne reste ouvert à la clôture.

---

## 7. Décision de clôture

Le Toy Model 0A est déclaré :

```text
IMPLEMENTATION_0A = ACCEPTED
BENCHMARK_0A      = CLOSED
INSTRUMENT_0A     = VALIDATED
```

Au sens du projet, « instrument validé » signifie uniquement que l'implémentation reproduit le benchmark analytique gelé et que le dispositif numérique d'identifiabilité est suffisamment contrôlé pour servir de base logicielle au premier modèle exploratoire.

Cette clôture ne vaut pas autorisation implicite d'ouvrir ou d'implémenter le modèle suivant.

---

## 8. Étape suivante possible

Le prochain modèle exploratoire devra être spécifié dans un lot distinct avant toute implémentation.

Il devra notamment permettre au moins l'une des situations absentes de 0A :

```text
degré de liberté de jauge physique indépendant
```

et/ou :

```math
P O_{01}O_{12}P \neq P O_{02}P
```

sur le secteur étudié, afin que l'identifiabilité ne soit plus entièrement connue avant calcul.

Aucun choix détaillé de ce modèle suivant n'est fixé par le présent rapport.
