# Toy Model 0A — Contrat technique d'implémentation

**Projet :** Cosmobox C Model  
**Dépôt cible :** `ioio2995/cosmobox-c-model`  
**Référence du dépôt lors de la rédaction :** `master @ d9de78206bed6a02b8a561faf3567cdb84961130`  
**Emplacement recommandé :** `docs/toy-models/toy0/implementation-design.md`  
**Statut :** spécification d'implémentation gelée pour le benchmark 0A  
**Public cible :** implémentation via Claude Code, revue scientifique et revue logicielle  
**Documents conceptuels de référence :** `docs/model/c-hypothesis.md`, `docs/toy-models/toy0/specification.md`

---

## 1. Objet du document

Ce document constitue le contrat transversal entre la spécification scientifique du Toy Model 0 et son implémentation logicielle.

Il doit permettre à un agent de développement de construire le benchmark 0A sans avoir à reconstruire les décisions conceptuelles prises en amont, et sans introduire de nouvelle interprétation physique dans le code.

Le benchmark 0A a un statut particulier : **tous ses résultats sont connus analytiquement avant l'implémentation**. Il ne s'agit donc pas d'une expérience scientifique exploratoire, mais d'un benchmark de validation du futur dispositif d'identifiabilité.

La chaîne validée par 0A est uniquement :

```math
\text{modèle fini}
\rightarrow
\text{contraintes de Gauss}
\rightarrow
\mathcal H_{\mathrm{phys}}
\rightarrow
\text{observables invariantes}
\rightarrow
\mathcal M_F
\rightarrow
\{\sigma_k,\,r_\varepsilon,\,\ker\mathcal M_F,\,\kappa\}.
```

Toute divergence entre les résultats analytiques enregistrés ici et les résultats numériques doit être traitée comme une erreur de formalisation ou d'implémentation. **Aucune divergence de 0A ne peut être interprétée comme un résultat physique.**

---

## 2. Règles de gouvernance pour l'implémentation

Les règles suivantes sont obligatoires pendant tout le lot 0A :

1. `docs/model/c-hypothesis.md` et `docs/toy-models/toy0/specification.md` sont conceptuellement gelés.
2. Claude Code ne doit pas modifier ces deux documents pour adapter la théorie à l'implémentation.
3. Si une contradiction réelle est découverte, l'implémentation doit s'arrêter sur le point concerné et la contradiction doit être remontée explicitement avant toute modification conceptuelle.
4. Les valeurs analytiques attendues de 0A doivent vivre dans les tests/oracles, jamais dans les fonctions scientifiques de production.
5. Aucun résultat de 0A ne doit être utilisé pour introduire ou définir `C`, `C_eff`, une métrique, une distance, un Hamiltonien ou une dynamique.
6. Le code doit rester minimal. Aucune abstraction destinée à 0B ou à un modèle général ne doit être ajoutée sans besoin concret de 0A.
7. La reproductibilité prime sur l'optimisation. Pour des matrices de dimension maximale 72, une représentation dense est la référence de 0A.

Principe central :

```math
\boxed{\text{implémentation} \neq \text{oracle analytique}}
```

---

## 3. Périmètre fonctionnel

### 3.1 Inclus

0A doit implémenter :

- la base totale déterministe ;
- les primitives fermioniques avec signes de Jordan-Wigner ;
- l'opérateur de flux `E` et le transporteur tronqué `U` ;
- les contraintes de Gauss ;
- la sélection et l'ordonnancement de l'espace physique ;
- les opérateurs relationnels `O_01`, `O_12`, `O_02` ;
- leur invariance de jauge sur l'espace total ;
- leur projection sur l'espace physique ;
- les parties hermitiennes `X_ij` et `Y_ij` ;
- les familles `F1`, `F2`, `F3` ;
- le contrôle de composition projetée `F2_prime` ;
- l'espace réel traceless des variations de matrices densité ;
- la matrice de mesure `M_F` ;
- le spectre singulier complet sur le domaine ;
- le rang numérique au seuil préenregistré ;
- le noyau et son projecteur ;
- le conditionnement ;
- le stress test instrumental `F_delta` ;
- un rapport de benchmark reproductible.

### 3.2 Explicitement hors périmètre

0A ne doit pas implémenter :

- un Hamiltonien ;
- une évolution temporelle ;
- une diagonalisation spectrale physique ;
- un état fondamental ;
- une température ;
- `C^(pq)` ;
- `C_eff` ;
- un temps d'arrivée ;
- une distance ou métrique effective ;
- une boucle de jauge ;
- un Wilson loop ;
- une généralisation à des graphes arbitraires ;
- un format de campagne scientifique général ;
- une optimisation sparse prématurée.

---

## 4. Choix techniques minimaux

### 4.1 Langage et dépendances

Implémentation de référence recommandée : **Python 3.11+**.

Dépendances runtime minimales :

```text
numpy
```

Dépendance de test :

```text
pytest
```

Aucune dépendance à SciPy, SymPy ou à un framework quantique n'est nécessaire pour 0A.

Les calculs numériques utilisent `numpy.complex128` pour les opérateurs et `numpy.float64` pour les matrices de mesure après validation de leur réalité numérique.

### 4.2 Représentation matricielle

Toutes les matrices de 0A peuvent être denses.

Dimensions maximales :

```text
Hilbert total      : 72
Hilbert physique   : 3
espace traceless V : 8 dimensions réelles
```

L'usage de matrices sparse dans 0A est autorisé uniquement s'il ne complexifie pas le code ni les tests, mais il n'est ni demandé ni recommandé.

---

## 5. Architecture logicielle recommandée

La structure suivante est recommandée ; les noms peuvent être adaptés, mais la séparation des responsabilités doit être conservée :

```text
src/
  cosmobox_c_model/
    model0a/
      basis.py
      fermions.py
      links.py
      gauss.py
      observables.py
      identifiability.py
      benchmark.py

tests/
  model0a/
    test_basis_and_gauss.py
    test_link_algebra.py
    test_observables.py
    test_jordan_wigner_witness.py
    test_identifiability.py
    test_conditioning.py
    test_pipeline.py

scripts/
  run_0a_benchmark.py
```

Responsabilités :

- `basis.py` : états de base, indexation déterministe, projection/restriction ;
- `fermions.py` : `c_i`, `c_i†`, `n_i`, signes Jordan-Wigner ;
- `links.py` : `E`, `U`, `U†` et actions de lien ;
- `gauss.py` : charges, générateurs `G_i`, sélection de `H_phys` ;
- `observables.py` : `O_ij`, `X_ij`, `Y_ij`, familles physiques ;
- `identifiability.py` : `M_F`, SVD, rang, noyau, projecteur, conditionnement ;
- `benchmark.py` : assemblage du benchmark et génération du rapport ;
- `tests/` : seuls emplacements où les résultats analytiques gelés sont utilisés comme oracles.

Le découpage ne doit pas devenir un prétexte à construire un framework générique de théorie de jauge.

---

## 6. Base totale

Un état de base est représenté par :

```text
(n0, n1, n2, E01, E12)
```

avec :

```math
n_i\in\{0,1\},
\qquad
E_{01},E_{12}\in\{-1,0,+1\}.
```

Ordre lexical gelé des valeurs :

```text
occupation : 0 < 1
flux       : -1 < 0 < +1
```

La base totale doit être générée algorithmiquement et de manière déterministe à partir de ces domaines.

```math
\dim\mathcal H_{\mathrm{tot}}
=2^3\times3^2
=72.
```

Une table `state -> index` et sa réciproque doivent être disponibles afin que toute action d'opérateur puisse être auditée à partir d'états explicites.

---

## 7. Convention fermionique

L'ordre des modes est gelé :

```math
0<1<2.
```

Pour un état de matière `|n0 n1 n2>` :

```math
c_i|n_0n_1n_2\rangle
=
(-1)^{\sum_{k<i}n_k}
 n_i
|n_0\ldots(n_i-1)\ldots n_2\rangle,
```

et :

```math
c_i^\dagger|n_0n_1n_2\rangle
=
(-1)^{\sum_{k<i}n_k}
(1-n_i)
|n_0\ldots(n_i+1)\ldots n_2\rangle.
```

Les fonctions élémentaires doivent retourner explicitement :

```text
(new_state, amplitude)
```

ou un résultat nul si l'action annihile l'état.

Il est interdit d'omettre les chaînes de Jordan-Wigner au motif qu'elles valent `+1` dans les trois états physiques de 0A. Le témoin `chi` défini plus loin doit exercer un signe `-1` sur l'espace total.

---

## 8. Opérateurs de lien

Dans la base ordonnée :

```math
\{|-1\rangle,|0\rangle,|+1\rangle\},
```

l'opérateur de flux est :

```math
E=
\begin{pmatrix}
-1&0&0\\
0&0&0\\
0&0&1
\end{pmatrix}.
```

Le transporteur est une **isométrie partielle tronquée**, et non un shift cyclique :

```math
U|-1\rangle=|0\rangle,
\qquad
U|0\rangle=|+1\rangle,
\qquad
U|+1\rangle=0.
```

Donc :

```math
U=
\begin{pmatrix}
0&0&0\\
1&0&0\\
0&1&0
\end{pmatrix}.
```

Les identités de référence sont :

```math
[E,U]=U,
```

```math
[E,U^\dagger]=-U^\dagger,
```

```math
U^\dagger U=\operatorname{diag}(1,1,0),
```

```math
UU^\dagger=\operatorname{diag}(0,1,1).
```

`U` ne doit jamais être qualifié d'unitaire dans le code ou la documentation.

---

## 9. Charges et contraintes de Gauss

Le fond est gelé à :

```math
b=(0,1,0).
```

Les charges sont :

```math
q_0=n_0,
\qquad
q_1=n_1-1,
\qquad
q_2=n_2.
```

Les flux de bord sont nuls.

Les générateurs de Gauss sont :

```math
G_0=E_{01}-q_0,
```

```math
G_1=E_{12}-E_{01}-q_1,
```

```math
G_2=-E_{12}-q_2.
```

Un état total est physique si et seulement si :

```math
G_0|s\rangle=G_1|s\rangle=G_2|s\rangle=0.
```

La sélection doit être calculée à partir de ces contraintes. Il est interdit de coder en dur les trois états physiques comme mécanisme de sélection.

Le résultat analytique attendu est :

```math
E_{01}=n_0,
\qquad
E_{12}=-n_2,
\qquad
n_0+n_1+n_2=1.
```

---

## 10. Espace physique

Les trois états physiques attendus sont :

```math
|L\rangle=|100;+1,0\rangle,
```

```math
|M\rangle=|010;0,0\rangle,
```

```math
|R\rangle=|001;0,-1\rangle.
```

Après leur découverte par Gauss, la base physique est explicitement réordonnée selon :

```math
\boxed{(|L\rangle,|M\rangle,|R\rangle)}.
```

Toutes les matrices analytiques du benchmark utilisent cet ordre.

```math
\dim\mathcal H_{\mathrm{phys}}=3.
```

Le projecteur physique dans l'espace total est :

```math
P_{\mathrm{phys}}
=
|L\rangle\langle L|
+|M\rangle\langle M|
+|R\rangle\langle R|.
```

Pour produire une matrice `3 x 3`, l'implémentation peut utiliser directement une matrice d'inclusion `Q` dont les colonnes sont les trois vecteurs physiques, puis :

```math
O_{\mathrm{phys}}=Q^\dagger O_{\mathrm{tot}}Q.
```

Cette représentation est recommandée pour éviter les ambiguïtés entre « projection dans 72 dimensions » et « restriction dans 3 dimensions ».

---

## 11. Occupations projetées

Dans la base physique `(L,M,R)` :

```math
n_0=
\begin{pmatrix}
1&0&0\\
0&0&0\\
0&0&0
\end{pmatrix},
```

```math
n_1=
\begin{pmatrix}
0&0&0\\
0&1&0\\
0&0&0
\end{pmatrix},
```

```math
n_2=
\begin{pmatrix}
0&0&0\\
0&0&0\\
0&0&1
\end{pmatrix}.
```

Donc :

```math
n_0+n_1+n_2=\mathbb I_3.
```

---

## 12. Observables relationnelles

Les trois opérateurs sont construits **sur l'espace total** :

```math
O_{01}=c_0^\dagger U_{01}c_1,
```

```math
O_{12}=c_1^\dagger U_{12}c_2,
```

```math
O_{02}=c_0^\dagger U_{01}U_{12}c_2.
```

L'ordre d'action sur un ket est explicitement de droite à gauche. Pour `O_02` :

```text
c2 -> U12 -> U01 -> c0†
```

Même si `U01` et `U12` commutent ici car ils agissent sur deux liens différents, cet ordre doit rester explicite dans le constructeur.

Avant toute restriction physique, l'implémentation doit vérifier :

```math
[G_k,O_{ij}]=0
```

pour tous les `k` et pour les trois `O_ij` sur les 72 dimensions de `H_tot`.

Après restriction à `H_phys`, les matrices attendues sont :

```math
O_{01}=|L\rangle\langle M|
=
\begin{pmatrix}
0&1&0\\
0&0&0\\
0&0&0
\end{pmatrix},
```

```math
O_{12}=|M\rangle\langle R|
=
\begin{pmatrix}
0&0&0\\
0&0&1\\
0&0&0
\end{pmatrix},
```

```math
O_{02}=|L\rangle\langle R|
=
\begin{pmatrix}
0&0&1\\
0&0&0\\
0&0&0
\end{pmatrix}.
```

---

## 13. Parties hermitiennes

Pour tout `O_ij` :

```math
X_{ij}=\frac{O_{ij}+O_{ij}^\dagger}{2},
```

```math
Y_{ij}=\frac{O_{ij}-O_{ij}^\dagger}{2i}.
```

En particulier :

```math
X_{02}=
\begin{pmatrix}
0&0&1/2\\
0&0&0\\
1/2&0&0
\end{pmatrix},
```

```math
Y_{02}=
\begin{pmatrix}
0&0&-i/2\\
0&0&0\\
i/2&0&0
\end{pmatrix}.
```

---

## 14. Composition : identité projetée, non identité générale

Sur l'espace total :

```math
O_{01}O_{12}
=
c_0^\dagger U_{01}(1-n_1)U_{12}c_2.
```

Il ne s'agit donc pas d'une identité générale avec `O_02`.

Sur le seul secteur physique de 0A :

```math
P_{\mathrm{phys}}O_{01}O_{12}P_{\mathrm{phys}}
=
P_{\mathrm{phys}}O_{02}P_{\mathrm{phys}}.
```

Dans la représentation restreinte `(L,M,R)` :

```math
O_{01}O_{12}=O_{02}=|L\rangle\langle R|.
```

Cette égalité doit être vérifiée exactement dans le pipeline physique.

### 14.1 Témoin hors secteur physique

Le témoin est :

```math
|\chi\rangle=|011;0,-1\rangle.
```

Les résultats attendus sont exactement :

```math
O_{01}O_{12}|\chi\rangle=0,
```

et :

```math
\boxed{
O_{02}|\chi\rangle
=-|110;+1,0\rangle.
}
```

Le signe `-` est produit par l'action de `c_2` avec `n_1=1`. Il constitue le test explicite d'un signe Jordan-Wigner non trivial dans 0A.

La différence globale satisfait :

```math
\boxed{
\left\|O_{01}O_{12}-O_{02}\right\|_F=2.
}
```

Ce test remplace toute simple assertion de type « les opérateurs sont différents ».

---

## 15. Espace réel d'identifiabilité

Une matrice densité physique `3 x 3`, hermitienne et de trace fixée, possède :

```math
3^2-1=8
```

degrés de liberté réels.

L'espace utilisé par l'analyse est :

```math
\mathcal V
=
\{A\in M_3(\mathbb C)\mid A=A^\dagger,\ \operatorname{Tr}A=0\}.
```

Il est muni du produit scalaire réel de Hilbert-Schmidt :

```math
\langle A,B\rangle_{\mathrm{HS}}
=
\operatorname{Tr}(AB).
```

Une base orthonormale gelée est :

```math
B_1=
\frac{|L\rangle\langle L|-|M\rangle\langle M|}{\sqrt2},
```

```math
B_2=
\frac{|L\rangle\langle L|+|M\rangle\langle M|-2|R\rangle\langle R|}{\sqrt6},
```

```math
B_3=\sqrt2X_{01},
\qquad
B_4=\sqrt2Y_{01},
```

```math
B_5=\sqrt2X_{12},
\qquad
B_6=\sqrt2Y_{12},
```

```math
B_7=\sqrt2X_{02},
\qquad
B_8=\sqrt2Y_{02}.
```

Le code doit vérifier :

```math
\operatorname{Tr}(B_aB_b)=\delta_{ab}.
```

---

## 16. Matrice de mesure

Pour une famille ordonnée d'observables hermitiennes :

```math
F=(O_1,\ldots,O_m),
```

l'application est :

```math
\mathcal M_F(A)
=
\left(
\operatorname{Tr}(AO_1),\ldots,\operatorname{Tr}(AO_m)
\right).
```

Dans la base `B_1,...,B_8` :

```math
(M_F)_{ka}=\operatorname{Tr}(B_aO_k).
```

### 16.1 Réalité numérique

`B_a` et `O_k` étant hermitiens, chaque coefficient est réel mathématiquement.

L'implémentation doit néanmoins :

1. calculer la trace en complexe ;
2. vérifier explicitement que sa partie imaginaire est inférieure à la tolérance ;
3. seulement ensuite convertir en `float64`.

Il est interdit d'appeler silencieusement `real(...)` ou d'abandonner la partie imaginaire sans contrôle.

---

## 17. Familles physiques du benchmark

Ordre gelé :

```math
F_1=(n_0,n_1,n_2).
```

```math
F_2=(n_0,n_1,n_2,X_{01},Y_{01},X_{12},Y_{12}).
```

```math
F_3=(n_0,n_1,n_2,X_{01},Y_{01},X_{12},Y_{12},X_{02},Y_{02}).
```

Les ordres ci-dessus doivent être conservés dans les rapports afin de rendre les matrices de mesure auditables.

---

## 18. Oracles analytiques de `M_F`

### 18.1 `F1`

```math
M_{F_1}
=
\begin{pmatrix}
1/\sqrt2&1/\sqrt6&0&0&0&0&0&0\\
-1/\sqrt2&1/\sqrt6&0&0&0&0&0&0\\
0&-2/\sqrt6&0&0&0&0&0&0
\end{pmatrix}.
```

Rang attendu :

```math
r(F_1)=2.
```

### 18.2 `F2`

```math
M_{F_2}
=
\begin{pmatrix}
1/\sqrt2&1/\sqrt6&0&0&0&0&0&0\\
-1/\sqrt2&1/\sqrt6&0&0&0&0&0&0\\
0&-2/\sqrt6&0&0&0&0&0&0\\
0&0&1/\sqrt2&0&0&0&0&0\\
0&0&0&1/\sqrt2&0&0&0&0\\
0&0&0&0&1/\sqrt2&0&0&0\\
0&0&0&0&0&1/\sqrt2&0&0
\end{pmatrix}.
```

Rang attendu :

```math
r(F_2)=6.
```

Noyau exact :

```math
\ker M_{F_2}
=
\operatorname{span}_{\mathbb R}\{B_7,B_8\}
=
\operatorname{span}_{\mathbb R}\{X_{02},Y_{02}\}.
```

### 18.3 `F3`

`M_F3` ajoute les deux lignes :

```math
\begin{pmatrix}
0&0&0&0&0&0&1/\sqrt2&0\\
0&0&0&0&0&0&0&1/\sqrt2
\end{pmatrix}.
```

Rang attendu :

```math
r(F_3)=8.
```

Noyau :

```math
\ker M_{F_3}=\{0\}.
```

---

## 19. Calcul numérique du spectre singulier

### 19.1 Définition mathématique

Le « spectre singulier complet sur le domaine » contient toujours huit valeurs pour 0A et correspond mathématiquement aux racines carrées des valeurs propres de :

```math
M_F^\mathsf TM_F.
```

### 19.2 Implémentation obligatoire

**Le code ne doit pas former `M.T @ M` pour calculer les valeurs singulières.**

Former la matrice de Gram carré le nombre de conditionnement et détruit précisément la résolution des petites valeurs singulières que le contrôle `F_delta` doit exercer.

Le calcul doit utiliser directement une SVD de `M` :

```text
s = svd(M, compute_uv=False)
```

Les valeurs retournées sont ensuite complétées par des zéros jusqu'à la dimension du domaine :

```text
n_domain = 8
sigma_domain = [singular values returned by SVD] + trailing zeros
```

avec tri décroissant garanti.

Pour extraire le noyau, une SVD avec `full_matrices=True` doit fournir les vecteurs singuliers droits complets.

---

## 20. Valeurs singulières analytiques

Les spectres attendus sont :

```math
\sigma(F_1)
=\{1,1,0,0,0,0,0,0\},
```

```math
\sigma(F_2)
=\left\{
1,1,
\frac1{\sqrt2},\frac1{\sqrt2},\frac1{\sqrt2},\frac1{\sqrt2},
0,0
\right\},
```

```math
\sigma(F_3)
=\left\{
1,1,
\frac1{\sqrt2},\frac1{\sqrt2},\frac1{\sqrt2},\frac1{\sqrt2},
\frac1{\sqrt2},\frac1{\sqrt2}
\right\}.
```

---

## 21. Rang numérique

La tolérance absolue gelée pour 0A est :

```math
\boxed{\varepsilon_{\mathrm{rank}}=10^{-12}}.
```

Le rang numérique est défini explicitement par :

```math
r_\varepsilon
=
\#\{\sigma_k>\varepsilon_{\mathrm{rank}}\}.
```

Le moteur ne doit pas utiliser la tolérance implicite de `numpy.linalg.matrix_rank`.

La valeur de `epsilon_rank` doit être passée explicitement ou provenir d'une constante de configuration identifiée dans le rapport.

---

## 22. Noyau et projecteur

Le noyau doit être obtenu à partir des vecteurs singuliers droits de la SVD.

Les vecteurs individuels ne constituent pas un oracle stable lorsqu'un sous-espace nul est dégénéré. La comparaison de référence porte donc sur le projecteur orthogonal du noyau :

```math
P_{\ker}=K^\dagger K,
```

où les lignes de `K` forment une base orthonormale du noyau dans les coordonnées `B_a`.

Pour `F2`, le projecteur analytique est :

```math
P_{\ker(F_2)}
=
\operatorname{diag}(0,0,0,0,0,0,1,1).
```

Le test doit porter sur la norme de Frobenius de la différence des projecteurs et non sur les vecteurs singuliers eux-mêmes.

---

## 23. Conditionnement

Deux diagnostics doivent être distingués.

### 23.1 Conditionnement sur le support résolu

Avec le rang numérique `r_epsilon` :

```math
\kappa^+_\varepsilon
=
\frac{\sigma_{\max}}
{\sigma_{r_\varepsilon}}.
```

Il mesure le conditionnement du sous-espace que la tolérance déclare résolu.

Résultats physiques de référence :

```math
\kappa^+(F_1)=1,
```

```math
\kappa^+(F_2)=\sqrt2,
```

```math
\kappa(F_3)=\sqrt2.
```

### 23.2 Spectre brut

Le moteur doit toujours conserver les valeurs singulières brutes retournées par LAPACK avant application de `epsilon_rank`.

Ceci est indispensable pour `F_delta` : une valeur singulière peut être non nulle mathématiquement et numériquement calculable tout en étant déclarée non résolue par le seuil scientifique.

Le rapport doit donc distinguer au minimum :

```text
singular_values_raw
singular_values_domain
rank_epsilon
condition_number_resolved
```

Pour le contrôle `F_delta`, un `condition_number_compact` peut également être rapporté comme le rapport des deux valeurs singulières du bloc instrumental 2 x 2 lorsque la plus petite est strictement positive.

---

## 24. États témoins physiques

Les quatre états sont :

```math
|\psi_+\rangle
=\frac{|L\rangle+|R\rangle}{\sqrt2},
```

```math
|\psi_-\rangle
=\frac{|L\rangle-|R\rangle}{\sqrt2},
```

```math
|\psi_{+i}\rangle
=\frac{|L\rangle+i|R\rangle}{\sqrt2},
```

```math
|\psi_{-i}\rangle
=\frac{|L\rangle-i|R\rangle}{\sqrt2}.
```

Pour les quatre :

```math
\langle n_0\rangle=\frac12,
\qquad
\langle n_1\rangle=0,
\qquad
\langle n_2\rangle=\frac12,
```

et :

```math
\langle X_{01}\rangle
=\langle Y_{01}\rangle
=\langle X_{12}\rangle
=\langle Y_{12}\rangle
=0.
```

Ils sont donc exactement indiscernables par `F2`.

Sous `F3`, les valeurs attendues sont :

| état | `<X_02>` | `<Y_02>` |
|---|---:|---:|
| `psi_plus` | `+1/2` | `0` |
| `psi_minus` | `-1/2` | `0` |
| `psi_plus_i` | `0` | `+1/2` |
| `psi_minus_i` | `0` | `-1/2` |

---

## 25. Famille `F2_prime` : contrôle de pipeline uniquement

On définit :

```math
O_{\mathrm{comp}}
=
Q^\dagger(O_{01}O_{12})Q.
```

Puis ses parties hermitiennes `X_comp`, `Y_comp` et :

```math
F'_2=F_2\cup\{X_{\mathrm{comp}},Y_{\mathrm{comp}}\}.
```

Dans 0A :

```math
X_{\mathrm{comp}}=X_{02},
\qquad
Y_{\mathrm{comp}}=Y_{02}.
```

`F2_prime` doit donc produire exactement la même matrice de mesure et la même analyse que `F3`.

Ce contrôle est un **test de plomberie** du pipeline :

```text
operator -> hermitian parts -> family -> measurement matrix -> analysis
```

Il ne constitue pas un résultat physique indépendant et ne doit pas être comptabilisé comme tel dans les conclusions.

---

## 26. Famille instrumentale `F_delta`

`F1`, `F2` et `F3` valident les rangs et noyaux, mais leurs lignes sont orthogonales dans la base `B`. Elles n'exercent donc pas réellement un régime mal conditionné.

Un contrôle purement instrumental est ajouté :

```math
F_\delta
=
\{X_{01},\ X_{01}+\delta Y_{01}\}.
```

Il n'a **aucune interprétation physique propre** et ne doit jamais être intégré aux conclusions du Toy Model.

Dans le sous-espace `(B3,B4)` :

```math
M_\delta
=
\frac1{\sqrt2}
\begin{pmatrix}
1&0\\
1&\delta
\end{pmatrix}.
```

Les six autres colonnes du domaine sont nulles.

La Gram des deux lignes est :

```math
M_\delta M_\delta^\mathsf T
=
\frac12
\begin{pmatrix}
1&1\\
1&1+\delta^2
\end{pmatrix}.
```

Les valeurs propres sont :

```math
\lambda_\pm
=
\frac{2+\delta^2\pm\sqrt{4+\delta^4}}{4}.
```

Donc :

```math
\sigma_+
=
\frac12
\sqrt{2+\delta^2+\sqrt{4+\delta^4}},
```

et :

```math
\sigma_-
=
\frac12
\sqrt{2+\delta^2-\sqrt{4+\delta^4}}.
```

Pour calculer l'oracle analytique lorsque `delta` est petit, la forme précédente de `sigma_minus` ne doit pas être évaluée directement, car elle subit une annulation catastrophique.

Utiliser :

```math
\boxed{
\sigma_-=
\frac{|\delta|}{2\sigma_+}
}
```

puisque :

```math
\sigma_+\sigma_-=\frac{|\delta|}{2}.
```

Pour `|delta| << 1` :

```math
\sigma_+\rightarrow1,
\qquad
\sigma_-\sim\frac{|\delta|}{2},
```

et :

```math
\boxed{
\kappa_\delta\sim\frac{2}{|\delta|}.
}
```

---

## 27. Sweep préenregistré de `F_delta`

Les valeurs sont gelées avant implémentation :

```text
1e-2
1e-4
1e-6
1e-8
1e-10
1e-13
0
```

Avec :

```text
epsilon_rank = 1e-12
```

les comportements attendus sont :

| `delta` | rang mathématique du bloc actif | rang numérique attendu |
|---:|---:|---:|
| `1e-2` | 2 | 2 |
| `1e-4` | 2 | 2 |
| `1e-6` | 2 | 2 |
| `1e-8` | 2 | 2 |
| `1e-10` | 2 | 2 |
| `1e-13` | 2 | 1 |
| `0` | 1 | 1 |

Pour `delta = 1e-13` :

```math
\sigma_-\approx5\times10^{-14}<\varepsilon_{\mathrm{rank}}.
```

La bascule théorique se situe près de :

```math
|\delta|\approx2\times10^{-12}.
```

Aucun point n'est placé volontairement à proximité immédiate de cette frontière afin que le benchmark teste le moteur et non les détails de résolution d'un backend LAPACK exactement au seuil.

Le test doit vérifier séparément :

```text
- agreement of raw singular values with analytic oracle
- evolution of compact condition number
- numerical rank at epsilon_rank
```

Il doit notamment être possible de rapporter simultanément pour `delta=1e-13` :

```text
mathematical_active_rank = 2
rank_epsilon             = 1
```

L'information `mathematical_active_rank` appartient à l'oracle du benchmark, pas au moteur générique.

---

## 28. Tolérances numériques

Tolérances gelées :

```text
exact_matrix_atol              = 1e-12
commutator_atol                = 1e-12
hermiticity_atol               = 1e-12
measurement_imag_atol          = 1e-12
singular_value_atol            = 1e-12
expectation_atol               = 1e-12
rank_epsilon                   = 1e-12
kernel_projector_frobenius_tol = 1e-10
```

Pour les identités constituées uniquement de coefficients `0`, `+1` et `-1`, le test peut utiliser une égalité exacte de tableau lorsque cela améliore la détection d'erreurs. Les tolérances ci-dessus restent l'interface numérique de référence pour les opérations impliquant SVD, racines ou normalisations irrationnelles.

Aucune tolérance ne doit être ajustée après observation des résultats de 0A.

---

## 29. Catalogue d'acceptation

### A — Conformité du modèle

**A01 — dimension totale**  
La base totale contient exactement 72 états distincts.

**A02 — algèbre du lien**  
Les quatre identités de `E`, `U`, `U†` sont conformes, y compris les projecteurs `U†U` et `UU†`.

**A03 — sélection physique**  
Les contraintes de Gauss sélectionnent exactement trois états.

**A04 — contenu physique**  
Après réordonnancement, les états sont exactement `L`, `M`, `R` avec les flux spécifiés.

**A05 — occupations physiques**  
Les matrices `n0`, `n1`, `n2` et leur somme sont conformes.

### B — Observables et jauge

**B01 — construction totale de `O_01`**  
L'opérateur est construit par action des primitives, pas par injection de sa matrice physique attendue.

**B02 — construction totale de `O_12`**  
Même exigence.

**B03 — construction totale de `O_02`**  
Même exigence, avec ordre d'action explicite.

**B04 — invariance de jauge**  
Tous les défauts `||[G_k,O_ij]||_F` sont inférieurs à `commutator_atol` sur les 72 dimensions.

**B05 — matrices projetées**  
Les trois matrices restreintes sont exactement les oracles `|L><M|`, `|M><R|`, `|L><R|`.

**B06 — identité projetée de composition**  
`Q†(O_01 O_12)Q = Q†O_02Q`.

**B07 — témoin Jordan-Wigner**  
`O_01 O_12 |chi> = 0` et `O_02 |chi> = -|110;+1,0>` exactement.

**B08 — non-identité globale quantitative**  
`||O_01 O_12 - O_02||_F = 2` à la tolérance gelée.

### C — Moteur d'identifiabilité

**C01 — base traceless**  
Les huit `B_a` sont hermitiens, traceless et Hilbert-Schmidt orthonormaux.

**C02 — réalité de `M_F`**  
Les parties imaginaires sont contrôlées avant conversion en réel.

**C03 — `F1`**  
Matrice de mesure, rang, spectre et noyau conformes.

**C04 — `F2`**  
Matrice de mesure, rang 6, spectre et noyau conformes.

**C05 — projecteur du noyau de `F2`**  
La norme de Frobenius du défaut au projecteur analytique est inférieure à `1e-10`.

**C06 — `F3`**  
Rang 8, noyau nul et spectre conforme.

**C07 — conditionnement des familles physiques**  
Les valeurs `1`, `sqrt(2)`, `sqrt(2)` sont reproduites selon les définitions du présent contrat.

**C08 — états témoins sous `F2`**  
Les quatre signatures sont identiques.

**C09 — états témoins sous `F3`**  
Les quatre couples `<X_02>,<Y_02>` sont exactement ceux enregistrés.

### D — Stress numérique instrumental

**D01 — oracle `F_delta`**  
Les deux valeurs singulières actives suivent la formule analytique sur tout le sweep.

**D02 — conditionnement `F_delta`**  
Le ratio compact suit la valeur analytique et son asymptotique `2/|delta|` dans le régime petit `delta`.

**D03 — rang numérique `F_delta`**  
Le rang au seuil est 2 jusqu'à `1e-10`, puis 1 pour `1e-13` et `0`.

**D04 — conservation du spectre brut**  
Pour `delta=1e-13`, la petite valeur singulière reste rapportée même si `rank_epsilon` l'exclut.

### E — Pipeline

**E01 — `F2_prime`**  
Le pipeline construit à partir de `O_comp` produit la même matrice de mesure et la même analyse que `F3`.

`E01` est un test de plomberie et n'est pas une validation scientifique indépendante de `B06`.

---

## 30. Politique d'échec

Tout test de catégories `A`, `B`, `C` ou `D` est bloquant.

Un échec doit être classé avant correction parmi :

```text
model construction
fermionic sign/order
link convention
Gauss projection
observable construction
gauge invariance
physical restriction
measurement construction
SVD/nullspace
rank thresholding
conditioning/reporting
```

Il est interdit de modifier un oracle analytique, une convention ou une tolérance pour faire passer un test sans démonstration préalable que la spécification contient effectivement une erreur.

---

## 31. Rapport de benchmark

Le runner 0A doit pouvoir produire un rapport machine-readable, idéalement JSON, non nécessairement versionné dans Git.

Schéma minimal recommandé :

```json
{
  "schema_version": "0a-benchmark-v1",
  "model": "toy-model-0a",
  "dimensions": {
    "total": 72,
    "physical": 3,
    "identifiability_domain": 8
  },
  "tolerances": {},
  "defects": {
    "gauss_commutators": {},
    "composition_projected": 0.0,
    "composition_full_frobenius": 2.0
  },
  "families": {
    "F1": {},
    "F2": {},
    "F3": {}
  },
  "conditioning_sweep": [],
  "tests": {},
  "passed": true
}
```

Les objets `families` doivent au minimum contenir :

```text
observable_order
measurement_matrix
singular_values_raw
singular_values_domain
rank_epsilon
kernel_dimension_epsilon
kernel_projector
condition_number_resolved
```

Pour 0A, le volume est suffisamment faible pour privilégier l'auditabilité à la compacité.

---

## 32. Interface minimale recommandée

Le contrat ne fixe pas une API publique définitive, mais les responsabilités suivantes doivent être isolables et testables :

```python
build_total_basis() -> Basis

apply_annihilation(state, site) -> Transition | None
apply_creation(state, site) -> Transition | None
apply_link_raise(state, link) -> Transition | None

build_operator_from_action(basis, action) -> np.ndarray

build_gauss_operators(basis) -> tuple[np.ndarray, ...]
select_physical_states(basis, gauss_operators, atol) -> PhysicalBasis
restrict_operator(operator, physical_basis) -> np.ndarray

build_relational_operators(...) -> RelationalOperators
hermitian_parts(operator) -> tuple[np.ndarray, np.ndarray]

build_traceless_hs_basis(...) -> tuple[np.ndarray, ...]
build_measurement_matrix(observables, hs_basis, imag_atol) -> np.ndarray
analyze_identifiability(matrix, rank_epsilon) -> IdentifiabilityResult

run_benchmark_0a() -> BenchmarkReport
```

Les noms peuvent varier. Les responsabilités ne doivent pas être fusionnées au point d'empêcher les tests unitaires indépendants.

---

## 33. Exigences sur les types de résultats

Un résultat d'identifiabilité devrait exposer explicitement :

```text
measurement_matrix
singular_values_raw
singular_values_domain
numerical_rank
kernel_dimension
kernel_basis_coordinates
kernel_projector
condition_number_resolved
rank_epsilon
```

Le code ne doit pas représenter implicitement un noyau nul par une valeur ambiguë. Une matrice de base de forme `(0, n_domain)` et un projecteur nul `n_domain x n_domain` constituent des représentations explicites adaptées.

---

## 34. Discipline numérique

1. Aucun arrondi ne doit être appliqué avant les assertions ou l'analyse.
2. Les arrondis sont réservés à l'affichage humain du rapport.
3. La SVD est calculée directement sur `M`, jamais via `M.T @ M`.
4. Le rang utilise `epsilon_rank` explicitement.
5. Les petits résidus négatifs produits éventuellement par des opérations numériques sur des quantités théoriquement positives doivent être traités uniquement lorsque la nécessité est démontrée ; ils ne doivent pas être masqués globalement.
6. Toute conversion `complex -> real` doit être précédée du contrôle de la partie imaginaire.
7. Les comparaisons de sous-espaces utilisent des projecteurs, pas des vecteurs de base arbitraires.
8. Les matrices d'oracle sont construites dans les tests indépendamment du chemin de calcul de production autant que raisonnablement possible.

---

## 35. Ce que 0A valide réellement

Si tous les tests passent, la seule conclusion technique autorisée est :

> L'implémentation reproduit correctement un benchmark analytique fini de jauge U(1) tronquée, sa projection physique et l'analyse d'identifiabilité associée ; elle distingue correctement rang structurel connu, rang numérique au seuil, noyau, projecteur de noyau et conditionnement, y compris dans un contrôle artificiellement mal conditionné.

Concernant la structure physique du benchmark :

> Dans le secteur physique minimal de 0A, le span linéaire des observables locales et relationnelles adjacentes de premier ordre possède un noyau réel de dimension deux correspondant à la cohérence complexe `L <-> R`. L'ajout de `X_02,Y_02` rend la famille informationnellement complète. Dans ce secteur particulier, `O_02` coïncide après projection avec `O_01 O_12` ; 0A ne distingue donc pas une relation étendue d'une composition de relations adjacentes.

---

## 36. Conclusions interdites

Même après succès complet de 0A, il est interdit d'affirmer que :

- une relation non adjacente porte une information fondamentalement irréductible aux relations adjacentes ;
- une relation étendue est généralement équivalente à une composition de relations locales ;
- un degré de liberté physique propre du champ de jauge a été identifié ;
- l'état collectif matière + jauge a été caractérisé dans un secteur comportant une dynamique de jauge autonome ;
- une grandeur `C^(pq)` a été identifiée ;
- `C_eff` est défini ou justifié ;
- une géométrie ou une distance a été reconstruite ;
- le conditionnement de 0A constitue une mesure de robustesse physique universelle.

La chaîne à trois nœuds est un arbre. Avec les conditions de Gauss et les flux de bord fixés, elle ne contient aucun degré de liberté de jauge indépendant de la matière. Cette limitation doit rester visible dans tout rapport 0A.

---

## 37. Critère de clôture du lot 0A

Le lot est clôturable lorsque :

```text
- tous les tests A/B/C/D sont verts ;
- le test de pipeline E01 est vert ;
- le runner produit un rapport complet ;
- aucun oracle scientifique n'est codé dans les fonctions de production ;
- les deux documents conceptuels gelés n'ont pas été modifiés ;
- le diff ne contient aucune fonctionnalité hors périmètre ;
- une revue séparée confirme que le code reproduit la spécification plutôt qu'il ne la recode en dur.
```

À ce moment seulement, 0A est considéré comme un **instrument validé** et peut servir de base logicielle au premier modèle exploratoire.

---

## 38. Consigne de handoff pour Claude Code

Claude Code doit traiter ce document comme un **contrat d'implémentation**, non comme une invitation à redéfinir le modèle.

Ordre de travail recommandé :

```text
1. lire intégralement docs/model/c-hypothesis.md, docs/toy-models/toy0/specification.md et ce document ;
2. confirmer le périmètre et l'état initial du dépôt ;
3. mettre en place le package et les tests sans logique scientifique codée en dur ;
4. implémenter d'abord la base, les primitives et Gauss ;
5. faire passer A01-A05 ;
6. implémenter les observables et faire passer B01-B08 ;
7. implémenter le moteur d'identifiabilité et faire passer C01-C09 ;
8. ajouter F_delta et faire passer D01-D04 ;
9. ajouter le contrôle de pipeline E01 ;
10. produire le rapport final 0A ;
11. effectuer une revue du diff complet et vérifier l'absence de dérive de périmètre.
```

Si un résultat analytique n'est pas reproduit, Claude Code doit rechercher l'erreur dans l'implémentation ou signaler une contradiction démontrée. Il ne doit jamais modifier silencieusement l'oracle, la tolérance ou la convention concernée.

---

## 39. Point de passage vers le modèle suivant

0A n'est pas un jalon scientifique. Il valide uniquement l'instrument.

Le modèle exploratoire suivant devra être spécifié séparément. Il devra notamment permettre au moins l'une des situations absentes de 0A :

```math
\text{degré de liberté de jauge indépendant}
```

et/ou :

```math
O_{01}O_{12}\neq O_{02}
\quad\text{après restriction au secteur étudié},
```

afin que l'identifiabilité cesse d'être entièrement connue avant calcul.

Aucune hypothèse détaillée sur ce modèle suivant n'est introduite dans le contrat 0A.
