# Toy Model 0B — spécification scientifique

Statut : **revue en cours**  
Projet : `ioio2995/cosmobox-c-model`  
Branche documentaire : `documentation/model0b-foundation`  
Base canonique : `master @ 08d5ca506ff05e15dd9bc084ea121c3d0a19b662`

Ce document fixe la source scientifique principale du Toy Model 0B. Il distingue explicitement les éléments déjà **validés pour gel**, les résultats pilotes connus avant pré-enregistrement et les paramètres qui restent ouverts. Aucun contenu de ce document ne vaut autorisation d'implémentation tant que `docs/governance/current-task.md` ne l'autorise pas explicitement.

---

## 1. Statut des blocs

```text
MODEL0B_SYSTEM_AND_GAUSS       = VALIDÉ POUR GEL
MODEL0B_TRUNCATION             = VALIDÉ POUR GEL
MODEL0B_STATIC_OBSERVABLES     = VALIDÉ POUR GEL
MODEL0B_STATIC_IDENTIFIABILITY = VALIDÉ POUR GEL
MODEL0B_SYMMETRIES             = VALIDÉ POUR GEL
MODEL0B_NULL_ORACLES           = VALIDÉ POUR GEL
MODEL0B_KUBO_PROBE             = VALIDÉ POUR GEL
MODEL0B_PRIMARY_SIGNAL_DELTA1  = VALIDÉ POUR GEL

MODEL0B_TIME_WINDOW_PROTOCOL   = OUVERT
MODEL0B_GAMMA_SET              = OUVERT
MODEL0B_TIME_SAMPLING          = OUVERT
MODEL0B_NUMERICAL_TOLERANCES   = OUVERT
MODEL0B_PARAMETER_CAMPAIGN     = OUVERT

IMPLEMENTATION_0B              = NON AUTORISÉE
```

Le statut `VALIDÉ POUR GEL` signifie que le contenu conceptuel correspondant a été suffisamment stabilisé pour être proposé au gel. Le statut `gelé` ne sera attribué qu'après validation explicite de Lionel ORCIL et publication du paquet documentaire correspondant.

---

## 2. Rôle scientifique de 0B

0A a validé l'instrument numérique d'identifiabilité sur un benchmark analytique, sans fournir de degré de liberté physique autonome du champ de jauge.

0B est le premier modèle exploratoire destiné à contenir simultanément :

- un degré de liberté cyclique non fixé par Gauss ;
- des observables locales et relationnelles invariantes de jauge ;
- des symétries exactes suffisamment riches pour fournir des oracles nuls ;
- une sonde dynamique de réponse retardée source-récepteur ;
- une comparaison relative de temps caractéristiques qui ne doit jamais être confondue avec une vitesse fondamentale.

0B ne cherche pas à effectuer une tomographie complète de l'état quantique. La question d'identifiabilité est restreinte aux directions physiques effectivement utilisées par le protocole suivant.

---

## 3. Système principal

On considère un cycle orienté à six nœuds :

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 0
```

Les occupations de matière sont :

```math
n_i\in\{0,1\}.
```

Le fond alterné est :

```math
b=(0,1,0,1,0,1),
```

et :

```math
q_i=n_i-b_i.
```

Les liens portent un champ électrique tronqué :

```math
E_i\in\{-\Lambda,\ldots,+\Lambda\},
```

avec un opérateur de montée tronqué :

```math
U_i|E\rangle=
\begin{cases}
|E+1\rangle,&E<\Lambda,\\
0,&E=\Lambda.
\end{cases}
```

`U_i` est une isométrie partielle tronquée, jamais une unité de phase exacte.

Le régime scientifique de référence est :

```text
Λ_ref = 2
```

et le contrôle principal de troncature :

```text
Λ_check = 3
```

Le régime `Λ = 1` est rétrogradé en fixture / régime pilote fortement tronqué.

---

## 4. Loi de Gauss et secteur physique

Avec l'orientation ci-dessus :

```math
G_i=E_i-E_{i-1}-q_i,
```

avec indices modulo 6.

Le secteur physique est :

```math
\mathcal H_{\rm phys}=\bigcap_i\ker G_i.
```

La somme des contraintes impose :

```math
\sum_i q_i=0
\quad\Longrightarrow\quad
\sum_i n_i=3.
```

Il existe donc exactement :

```math
\binom{6}{3}=20
```

configurations de matière candidates.

Pour une configuration de matière `m`, choisir un flux initial `e` détermine tous les autres flux par Gauss :

```math
E_j=e+s_j(m).
```

On définit :

```math
\operatorname{spread}(m)
=\max_j s_j(m)-\min_j s_j(m).
```

L'admissibilité sous la troncature donne exactement :

```math
\#\mathcal E_m
=
\max\!\left(
0,
2\Lambda+1-\operatorname{spread}(m)
\right).
```

Pour les 20 configurations de matière du 6-cycle :

| `spread(m)` | nombre de configurations |
|---:|---:|
| 0 | 1 |
| 1 | 16 |
| 2 | 3 |

L'unique configuration de spread nul est :

```math
n=b=(0,1,0,1,0,1).
```

Elle possède la plus grande largeur admissible du zéro-mode de flux :

```math
\#\mathcal E_b=2\Lambda+1.
```

Corollaire :

```math
\boxed{\dim\mathcal H_{\rm phys}(\Lambda)=40\Lambda-2}
```

pour `Λ >= 1`.

Donc :

```text
Λ = 1 -> dim H_phys = 38
Λ = 2 -> dim H_phys = 78
Λ = 3 -> dim H_phys = 118
```

L'identité :

```math
\dim \mathcal H_{\rm interior}(\Lambda)
=
\dim \mathcal H_{\rm phys}(\Lambda-1)
```

est une conséquence de définition : être strictement intérieur à `±Λ` équivaut à satisfaire la borne `Λ-1`.

---

## 5. Construction du secteur physique

La construction nominale ne doit pas bâtir une matrice dense sur tout :

```math
\dim\mathcal H_{\rm tot}=2^6(2\Lambda+1)^6.
```

Elle doit exploiter directement Gauss :

1. énumérer les 20 configurations de matière avec trois fermions ;
2. énumérer les `2Λ+1` valeurs possibles du flux initial ;
3. reconstruire les six `E_i` par Gauss ;
4. rejeter les configurations qui sortent de `[-Λ,+Λ]` ;
5. construire les opérateurs directement dans la base physique obtenue.

Cette récursion est spécifique à l'assemblage cyclique de 0B ; sa localisation logicielle future relève donc du modèle et non d'une brique générique de `core` sauf décision architecturale ultérieure explicitement justifiée.

Le contrôle de l'invariance de jauge des règles d'action ne doit pas être abandonné : pour une transition non nulle :

```math
O|s\rangle=a|s'\rangle,
```

on peut vérifier sans matrice full-space que :

```math
g_i(s')=g_i(s)
```

pour toutes les contraintes de Gauss.

---

## 6. Hamiltonien de référence et famille de fonds

On fixe l'unité d'énergie par :

```math
J\equiv1.
```

Le Hamiltonien familial est :

```math
H(g,\mu,\delta)
=
g\sum_iE_i^2
-
\sum_i
\left(
c_i^\dagger U_i c_{i+1}
+
 c_{i+1}^\dagger U_i^\dagger c_i
\right)
+
2\mu N_{\rm even}
+
g\delta\sum_i(-1)^iE_i^2,
```

avec :

```math
N_{\rm even}=n_0+n_2+n_4.
```

Le point de référence est :

```math
(g_{\rm ref},\mu_{\rm ref},\delta_{\rm ref})=(1,0,0).
```

Le paramètre `g` compare l'énergie électrique au hopping. `μ` module le potentiel relatif des deux sous-réseaux. `δ` module de façon alternée l'énergie électrique des liens.

La direction de rééchelonnement global :

```math
H\mapsto sH
```

est exclue de la famille scientifique. Elle est conservée uniquement comme contrôle nul / oracle de rééchelonnement.

Le terme alterné de matière n'appartient pas au Hamiltonien nominal :

```math
\lambda_m=0
```

au point de référence afin de ne pas favoriser artificiellement `n=b`, qui est précisément la configuration possédant la plus grande largeur admissible du zéro-mode de flux.

---

## 7. État de référence

Si le fondamental est non dégénéré :

```math
\rho_{\rm ref}=|\Omega\rangle\langle\Omega|.
```

S'il est dégénéré :

```math
\boxed{
\rho_{\rm ref}
=
\frac{P_{\rm GS}}{\operatorname{Tr}P_{\rm GS}}
}
```

sur tout le sous-espace fondamental.

Aucun vecteur particulier dans un sous-espace dégénéré ne doit être sélectionné après inspection des résultats.

Le rapport doit publier :

```text
d_GS
```

et vérifier l'activité des générateurs avant toute analyse de réponse.

---

## 8. Degré cyclique et flux uniforme

Sur le secteur physique, Gauss fixe les différences de flux :

```math
E_i-E_{i-1}=q_i.
```

On définit le flux uniforme :

```math
\Phi=\frac16\sum_iE_i.
```

Pour une configuration de matière fixée, les solutions de Gauss forment une fibre affine :

```math
E=E_{\rm part}(m)+\alpha(1,1,1,1,1,1).
```

Avec une solution particulière de moyenne nulle, `α = Φ`.

Le label d'énumération `e` est une autre coordonnée de la même fibre :

```math
\Phi=e+c(m),
```

avec un offset dépendant de la matière `c(m)`. Il est donc interdit d'identifier naïvement `e` à une coordonnée plus fondamentale que `Φ`.

Au niveau tangent :

```math
D_i^{(E)}=-i[E_i,\rho_{\rm ref}],
```

```math
D_i^{(n)}=-i[n_i,\rho_{\rm ref}].
```

Gauss impose :

```math
D_i^{(E)}-D_{i-1}^{(E)}=D_i^{(n)}.
```

Donc :

```math
S_n\subseteq S_E,
\qquad
\dim S_n\le5,
\qquad
\dim S_E\le6.
```

Le degré cyclique intrinsèque est représenté par le quotient :

```math
\boxed{S_E/S_n}
```

plutôt que par une prétendue « direction de boucle pure » unique.

`D_Φ = -i[Φ,ρ_ref]` est un représentant adapté aux symétries du zéro-mode de flux ; il peut contenir des composantes changeant la configuration de matière et ne doit pas être décrit comme vivant exclusivement dans les blocs à matière fixée.

---

## 9. Shift cyclique et harmoniques

On définit :

```math
L=U_0U_1U_2U_3U_4U_5.
```

`L` n'est pas une Wilson loop unitaire. C'est un shift cyclique tronqué du zéro-mode de flux.

Il vérifie :

```math
[\Phi,L]=L.
```

La famille harmonique déclarée est le **span linéaire** :

```math
\boxed{
\mathscr H_\Lambda
=
\operatorname{span}_{\mathbb R}
\left\{
X_{L^k},Y_{L^k}
\mid
1\le k\le2\Lambda
\right\}
}
```

avec :

```math
X_{L^k}=\frac{L^k+(L^\dagger)^k}{2},
\qquad
Y_{L^k}=\frac{L^k-(L^\dagger)^k}{2i}.
```

Aucune fermeture algébrique implicite n'est autorisée.

Sont explicitement hors famille :

```math
f(\Phi)L^k,
\qquad
n_iL^k,
\qquad
P_mL^k.
```

Ces objets conditionnent ou croisent des secteurs distincts et constitueraient une nouvelle famille composite à pré-enregistrer séparément.

La motivation des `L^k` est uniquement qu'ils forment les harmoniques naturelles de translation du zéro-mode tronqué ; ils ne sont pas introduits après observation d'un défaut de rang.

---

## 10. Oracle analytique des rangs de `L^k`

Pour :

```math
j=2\Lambda-k,
```

on a :

```math
\boxed{
r_\Lambda(L^k)
=
\sum_m
\max\left(
0,
j+1-\operatorname{spread}(m)
\right)
}
```

Le rang dépend donc de `j` seulement.

| `j = 2Λ-k` | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| `rank(L^k)` | 1 | 18 | 38 | 58 | 78 | 98 |

Corollaire :

```math
r_\Lambda(L^k)=r_{\Lambda-1}(L^{k-2})
```

lorsque les indices ont un sens.

L'harmonique extrême vérifie :

```math
r_\Lambda(L^{2\Lambda})=1.
```

Elle ne sonde qu'une cohérence de la configuration `n=b`; toute conclusion portée exclusivement par cette harmonique doit donc être qualifiée de sectorielle et particulièrement sensible à la troncature.

---

## 11. Familles de mesure statiques

La stratification déclarée est :

```math
F_D
\subset
F_{\rm edge}
\subset
F_{\rm path}
\subset
F_{\rm loop}^{(1)}
\subset
F_{\rm loop}^{\rm harm}.
```

### `F_D`

```math
F_D=\{n_i,E_i\}_{i=0}^{5}.
```

Ces observables diagonales locales de premier ordre ne constituent pas une tomographie des populations.

En particulier :

```math
\dim(\text{diagonal traceless})=d^2_{\rm diagonal}-1=d_{\rm phys}-1,
```

alors que `F_D` ne contient qu'un nombre linéaire de fonctionnelles.

### `F_edge`

`F_D` plus les parties hermitiennes des transports gauge-dressed sur les arêtes.

### `F_path`

`F_edge` plus les transports ouverts associés aux arcs déclarés du cycle, notamment les deux arcs distincts pour les paires opposées.

### `F_loop^(1)`

`F_path` plus :

```math
X_L,Y_L.
```

Cette famille est conservée comme sous-famille diagnostique historique car elle a été utilisée dans les calculs pilotes `Λ=1`.

### `F_loop^harm`

`F_path` plus tout le span harmonique `H_Λ` défini en §9.

La distinction :

```math
\operatorname{span}(F)\neq\operatorname{Alg}(F)
```

reste normative. On n'ajoute jamais implicitement des produits d'observables pour augmenter le rang.

---

## 12. Résultats pilotes connus avant pré-enregistrement

Les résultats suivants ont été calculés pendant l'étude de faisabilité **à `Λ=1` uniquement**. Ils ne constituent pas des résultats confirmatoires du régime de référence `Λ=2`.

```text
PILOT_LAMBDA = 1
N            = 6
dim H_phys   = 38
dim V        = 1443

rank(F_D)          = 6
rank(F_edge)       = 18
rank(F_path)       = 36
rank(F_loop^(1))   = 38
rank(L)            = 18
```

Le régime `Λ=2` est vierge de rangs globaux calculés pour :

```text
F_D
F_edge
F_path
F_loop^(1)
F_loop^harm
```

Les faits analytiques des §§4 et 10 ne sont pas des résultats prospectifs : ils doivent être traités comme oracles structurels.

L'inclusion :

```math
F_{\rm loop}^{(1)}\subset F_{\rm loop}^{\rm harm}
```

implique trivialement :

```math
r(F_{\rm loop}^{\rm harm})\ge r(F_{\rm loop}^{(1)}).
```

Cette inégalité ne doit jamais être présentée comme résultat scientifique.

---

## 13. Identifiabilité ciblée

Pour :

```math
\mathcal V=\{A=A^\dagger,\operatorname{Tr}A=0\},
```

une famille d'observables `F={O_μ}` définit :

```math
\mathcal M_F(A)
=
\left(
\operatorname{Tr}(A\cdot O_1),\ldots,
\operatorname{Tr}(A\cdot O_m)
\right).
```

0B ne demande pas l'injectivité de `M_F` sur tout `V`.

Pour une famille de paramètres physiques pré-déclarée `θ`, on définit les directions de réponse :

```math
D_a
=
\left.
\frac{\partial\rho_\theta}{\partial\theta_a}
\right|_{\theta=\theta_0}
```

lorsque cette dérivée est pertinente, puis :

```math
S_{\rm resp}=\operatorname{span}_{\mathbb R}\{D_a\}.
```

La question d'identifiabilité porte sur :

```math
S_{\rm resp}\cap\ker\mathcal M_F.
```

Le rapport d'un verdict doit toujours publier :

```text
Λ
H / paramètres de fond
rho_ref
générateurs / paramètres θ
dim S_resp
famille F
groupe de transformations déclaré applicable
```

Un PASS sur un petit sous-espace de réponse n'est jamais transférable à d'autres perturbations.

---

## 14. Gate 0 — activité des générateurs

Pour un kick unitaire généré par `A` autour d'une référence fondamentalement dégénérée :

```math
D_A
=-i[A,\rho_{\rm ref}]
=-\frac{i}{d_{\rm GS}}[A,P_{\rm GS}].
```

Si :

```math
[A,P_{\rm GS}]=0,
```

alors :

```math
e^{-i\epsilon A}\rho_{\rm ref}e^{+i\epsilon A}=\rho_{\rm ref}
```

pour tout `ε`.

Le générateur est alors :

```text
GENERATOR_ACTIVITY = INACTIVE
```

et non `PASS`.

Un sous-espace de réponse de dimension nulle ne produit jamais un verdict d'observabilité positif.

---

## 15. Observabilité statique et dynamique

On définit la super-opération :

```math
\mathcal L_H(O)=i[H,O]
```

et le sous-espace de Krylov d'observables :

```math
\mathscr W(F,H)
=
\operatorname{span}_{\mathbb R}
\{O_\mu,\mathcal L_H(O_\mu),\mathcal L_H^2(O_\mu),\ldots\}
```

jusqu'à stabilisation du span.

Comme :

```math
\operatorname{span}(F)\subseteq\mathscr W(F,H),
```

on a :

```math
\mathscr W(F,H)^\perp\subseteq\ker\mathcal M_F.
```

Donc :

```math
\boxed{
S_{\rm resp}\cap\ker\mathcal M_F=\{0\}
\Longrightarrow
S_{\rm resp}\cap\mathscr W(F,H)^\perp=\{0\}
}
```

Le test statique est donc **suffisant mais non nécessaire** pour l'observabilité dynamique.

Pipeline :

```text
STATIC = PASS
    -> DYNAMIC = PASS
       aucun Krylov nécessaire

STATIC = FAIL
    -> statut dynamique inconnu
       construire W(F,H)

DYNAMIC = PASS
    -> autorise l'étude de G_pq(t)
       n'autorise pas C_eff
```

La condition d'invisibilité dynamique s'écrit sans ambiguïté :

```math
\operatorname{Tr}\!\left(D\cdot O_\mu(t)\right)=0.
```

---

## 16. Secteur collectif au point de référence

Sous le stabilisateur complet du point `δ=0`, les occupations se réduisent collectivement à :

```math
N_{\rm even}=n_0+n_2+n_4,
```

car :

```math
N_{\rm even}+N_{\rm odd}=3.
```

Côté flux, le seul zéro-mode collectif non fixé par Gauss est `Φ`.

Au point `δ=0`, la réflexion `R` est une symétrie de `H` et de `ρ_ref` :

- `N_even` est pair ;
- `Φ` est impair.

Donc :

```math
\langle D_{\rm stag},D_\Phi\rangle_{\rm HS}=0.
```

Si les deux générateurs passent Gate 0 :

```math
\boxed{\dim S_{\rm resp}^{\rm collective}=2}
```

au point `δ=0`.

Cette orthogonalité **n'est pas garantie pour `δ != 0`** et ne doit jamais être transportée le long de la campagne sans recalcul.

---

## 17. Transformations discrètes déclarées

La spécification distingue le groupe discret **pré-déclaré et explicitement énuméré** des transformations pertinentes du secteur physique ; elle ne prétend pas avoir démontré l'exhaustivité de toutes les symétries mathématiquement possibles.

### 17.1 Translation de deux sites

```math
\mathcal T^2:i\mapsto i+2.
```

Elle préserve le fond alterné et le Hamiltonien familial.

### 17.2 Particule-trou bipartite

On choisit :

```math
\mathcal C c_i\mathcal C^\dagger=(-1)^ic_i^\dagger,
```

```math
\mathcal C E_i\mathcal C^\dagger=-E_i,
\qquad
\mathcal C U_i\mathcal C^\dagger=U_i^\dagger.
```

Pour :

```math
h_i=c_i^\dagger U_ic_{i+1},
```

la phase bipartite donne :

```math
\mathcal C h_i\mathcal C^\dagger=h_i^\dagger.
```

Le hopping hermitien total est donc invariant.

`C` envoie le fond `b` sur `1-b`.

### 17.3 Transformation composée `S`

On définit :

```math
\mathcal S=\mathcal T\mathcal C.
```

La translation d'un site ramène `1-b` sur `b`, donc `S` préserve le secteur physique.

Le terme `2 μ N_even` est également invariant sous `S`.

### 17.4 Réflexion unitaire exacte

On choisit :

```math
r(j)=-j\pmod6.
```

La seconde quantification fermionique satisfait :

```math
\mathcal R_f c_j^\dagger\mathcal R_f^\dagger=c_{r(j)}^\dagger.
```

Dans le secteur `N_f=3`, le signe de réordonnancement Jordan-Wigner est le même pour tous les états et se réduit à une phase globale. Il ne produit aucune anomalie de bord.

Sur les liens :

```math
\mathcal R E_i\mathcal R^\dagger=-E_{-i-1},
```

```math
\mathcal R U_i\mathcal R^\dagger=U_{-i-1}^\dagger.
```

Le hopping total est invariant et :

```math
\boxed{
\mathcal R H(g,\mu,\delta)\mathcal R^\dagger
=
H(g,\mu,-\delta)
}
```

est une covariance unitaire exacte.

### 17.5 Transformation `Q`

On définit :

```math
\mathcal Q=\mathcal S\mathcal R.
```

`S` et `R` retournent tous deux `δ`, donc :

```math
\boxed{[\mathcal Q,H(g,\mu,\delta)]=0}
```

pour toute la famille.

Sur les occupations :

```math
\mathcal Q n_p\mathcal Q^\dagger
=1-n_{\sigma(p)},
\qquad
\sigma(p)=1-p.
```

Le sous-groupe spatial pur résiduel à `δ != 0` est `C3=<T^2>`, mais le stabilisateur physique déclaré contient aussi `Q`; l'action générée par `T^2` et `Q` est de type diédral `D3` sur les relations.

---

## 18. Règle de stabilisateur

Pour une famille `H(θ)`, chaque transformation déclarée `g` agit sur les paramètres par :

```math
U_gH(\theta)U_g^\dagger=H(g\cdot\theta).
```

Au point `θ`, on définit dans le groupe déclaré :

```math
\operatorname{Stab}_{\rm declared}(\theta)
=
\{g\mid g\cdot\theta=\theta\}.
```

Avant de déclarer un contraste comme signal, il faut calculer l'action de ce stabilisateur sur les relations comparées.

Si une transformation du stabilisateur échange deux classes, leur contraste est un oracle nul et ne peut pas être utilisé comme signal.

Un contraste non nul reste interprétable **relativement au groupe déclaré**. La découverte ultérieure d'une symétrie exacte omise peut réviser son interprétation.

---

## 19. Sonde de propagation de Kubo

Le protocole de propagation est distinct du protocole collectif de boucle.

La source et le récepteur primaires sont strictement site-locaux :

```math
A_p=n_p,
\qquad
B_q=n_q.
```

Pour un fond physique `θ` :

```math
\chi_{pq}^{(\theta)}(t)
=
i\,\operatorname{Tr}
\left[
\rho_\theta
[n_p,n_q^{(\theta)}(t)]
\right],
```

avec :

```math
n_q^{(\theta)}(t)
=e^{iH_\theta t}n_qe^{-iH_\theta t}.
```

La fonctionnelle positive et lisse utilisée par les temps est :

```math
\boxed{
\mathcal F_{pq}^{(\theta)}(t)
=
\frac{\chi_{pq}^{(\theta)}(t)^2}{4}
}
```

et :

```math
0\le\mathcal F\le1.
```

Comme :

```math
[n_p,n_q]=0
```

pour `p != q` :

```math
\boxed{\mathcal F_{pq}(0)=0.}
```

Le paramètre infinitésimal de Kubo `ε` utilisé conceptuellement pour définir la réponse locale est une **sonde**, et ne doit jamais être confondu avec les paramètres de fond `θ=(g,μ,δ,...)` comparés par `C_eff`.

---

## 20. Développement à temps court

On développe :

```math
n_q(t)
=
\sum_{r\ge0}
\frac{(it)^r}{r!}
\operatorname{ad}_H^r(n_q).
```

La localité de `H` impose :

```math
[n_p,\operatorname{ad}_H^r(n_q)]=0
```

pour tout ordre strictement inférieur à la portée minimale imposée par le graphe.

La distance de graphe fournit donc un **ordre minimal possible au niveau opérateur**, mais l'espérance dans un état peut annuler ce premier terme.

On définit l'exposant d'état :

```math
\nu_{pq}(\rho)
=
\min\{r\mid a_r(\rho)\neq0\},
```

avec :

```math
a_r(\rho)
\propto
\operatorname{Tr}
\left[
\rho
[n_p,\operatorname{ad}_H^r(n_q)]
\right].
```

Une pente observée supérieure à la distance de graphe n'est pas automatiquement un bug ; elle peut provenir d'une annulation physique ou d'une symétrie.

Pour les paires opposées (`d=3`), deux arcs minimaux de même longueur contribuent au même ordre. Une annulation du coefficient de premier ordre autorisé est préenregistrée comme possibilité d'**interférence sensible au secteur cyclique**. Aucun terme « Aharonov-Bohm » ne doit être utilisé sans preuve supplémentaire de dépendance au degré cyclique et de robustesse sous troncature.

---

## 21. Temps caractéristiques

### 21.1 Premier maximum de la réponse

On définit le premier maximum de la première montée par :

```math
T_{\rm peak}
=
\inf\{t>0\mid
\dot{\mathcal F}(t)=0
\text{ avec changement }+\to-\}.
```

### 21.2 Temps de croissance

```math
\boxed{
T_{\rm grow}
=
\inf\operatorname*{arg\,max}_{0<t<T_{\rm peak}}
\dot{\mathcal F}(t)
}
```

`T_grow` est l'estimateur temporel primaire : il est sans seuil et porte sur une montée finie de la réponse.

### 21.3 Temps de seuil

Pour un seuil `η` :

```math
T_{\rm thr}(\eta)
=
\inf\{0<t<T_{\rm peak}\mid
\mathcal F(t)=\eta,
\dot{\mathcal F}(t)>0\}.
```

`η` n'est pas un paramètre physique privilégié. La courbe complète `C_eff^thr(η)` doit être publiée dans le domaine admissible.

Les détails numériques de l'échantillonnage des courbes, de la grille de `η`, de la fenêtre temporelle et des tolérances restent ouverts dans `validation-plan.md`.

---

## 22. Oracle de temps court

Si :

```math
\chi_x(t)=a_xt^\nu+O(t^{\nu+1}),
```

alors :

```math
\mathcal F_x(t)
=
\frac{a_x^2}{4}t^{2\nu}+\cdots.
```

Si :

```math
\nu_{\rm ref}=\nu_{\rm state}=\nu,
```

alors :

```math
\boxed{
C_{\rm short}^{(pq)}
=
\left|
\frac{a_{\rm state}}{a_{\rm ref}}
\right|^{1/\nu}
}
```

est calculable algébriquement sans effectuer l'évolution temporelle complète, et :

```math
\lim_{\eta\to0}
C_{\rm eff}^{\rm thr}(\eta)
=
C_{\rm short}^{(pq)}.
```

`C_short` est un **oracle de court temps**, pas un temps d'arrivée ni une vitesse.

Le contenu scientifique dynamique de la sonde seuil vit à `η` fini, après sortie du régime asymptotique de court temps et avant les récurrences.

La quantité :

```math
D_{pq}^{\rm thr}(\eta)
=
\log
\frac{C_{\rm eff}^{\rm thr}(\eta)}{C_{\rm short}^{(pq)}}
```

n'est définie que si les exposants de référence et d'état sont égaux et finis.

Sinon :

```text
SHORT_TIME_COMPARISON = NOT_APPLICABLE
D_thr                 = NOT_DEFINED
```

---

## 23. Sonde relative `C_eff`

Pour une même paire `pq` :

```math
C_{\rm eff}^{(pq|\rm ref)}
=
\frac{T_{pq}^{\rm ref}}{T_{pq}^{\rm state}}.
```

Deux estimateurs complémentaires sont conservés :

```math
C_{\rm eff}^{\rm grow}
=
\frac{T_{\rm grow}^{\rm ref}}
{T_{\rm grow}^{\rm state}},
```

et :

```math
C_{\rm eff}^{\rm thr}(\eta)
=
\frac{T_{\rm thr}^{\rm ref}(\eta)}
{T_{\rm thr}^{\rm state}(\eta)}.
```

Ils ne doivent pas être égaux numériquement par construction. Leur cohérence porte sur l'interprétation et le classement des fonds, pas sur l'identité de leurs valeurs.

Le mode uniforme :

```math
H\mapsto sH
```

implique exactement :

```math
C_{\rm eff}=s
```

pour toutes les paires. Il est conventionnel / trivial pour le contraste relationnel et sert d'oracle de contrôle.

---

## 24. Contrastes inter-orbites

Un changement uniforme de `C_eff` ne constitue pas le signal relationnel primaire.

Pour deux orbites `O_α`, `O_β` :

```math
\Delta_{\alpha\beta}
=
\log\frac{C_{\mathcal O_\alpha}}
{C_{\mathcal O_\beta}}.
```

Cette quantité élimine exactement le mode de rééchelonnement global.

### 24.1 Signal primaire `Δ1`

À `δ != 0`, les arêtes se séparent sous les translations de deux sites en deux classes non fusionnées par `Q` :

```text
O_1A = classe d'arêtes de type A
O_1B = classe d'arêtes de type B
```

Les représentants canoniques et l'orientation source-récepteur exacte restent à fixer dans le protocole dynamique avant gel complet ; les classes non orientées correspondantes sont :

```text
{(0,1),(2,3),(4,5)}
{(0,5),(1,2),(3,4)}
```

La réflexion échange les deux classes tout en envoyant `δ -> -δ`.

On définit :

```math
\boxed{
\Delta_1(\delta)
=
\log
\frac{C_{\mathcal O_{1A}}(\delta)}
{C_{\mathcal O_{1B}}(\delta)}
}
```

avec les oracles :

```math
\boxed{\Delta_1(0)=0}
```

et :

```math
\boxed{\Delta_1(-\delta)=-\Delta_1(\delta)}.
```

`Δ1(δ)` est l'observable primaire de la campagne. La susceptibilité :

```math
\Xi_1=
\left.\frac{\partial\Delta_1}{\partial\delta}\right|_{\delta=0}
```

n'est qu'un diagnostic local lorsqu'elle existe. `Xi1 = 0` n'implique pas un FAIL car la première réponse autorisée peut être cubique ou d'ordre impair supérieur.

### 24.2 Oracle nul `Δ2`

`Q = S R` échange les deux classes de relations à distance 2 tout en préservant tout `H(g,μ,δ)`.

Comme :

```math
\mathcal Qn_p\mathcal Q^\dagger
=1-n_{\sigma(p)}
```

et :

```math
[1-n_a,1-n_b(t)]
=[n_a,n_b(t)],
```

la réponse de Kubo est exactement préservée.

Donc :

```math
\boxed{
\Delta_2(g,\mu,\delta)=0
}
```

pour toute la campagne.

Toute valeur non nulle de `Δ2` au-delà des tolérances gelées est un défaut du pipeline, pas un signal.

### 24.3 Paires opposées

Les relations à distance 3 constituent un protocole secondaire d'interférence cyclique. Elles ne sont pas utilisées comme signal primaire et sont traitées séparément car les deux arcs minimaux de même longueur peuvent annuler le coefficient de court temps dans certains fonds.

---

## 25. Contrôle de troncature

Deux appariements distincts sont gelés conceptuellement.

### Appariement par `k`

Même harmonique, espace élargi :

```math
L^k_{\Lambda=2}
\leftrightarrow
L^k_{\Lambda=3}.
```

C'est le contrôle de convergence principal.

Le contrôle de `Λ=2` vers `Λ=3` utilise donc d'abord les mêmes indices :

```text
k = 1,2,3,4
```

à la référence et au contrôle.

### Appariement par `j`

Même position relative au bord :

```math
j=2\Lambda-k=\text{constante}.
```

C'est un diagnostic de localisation au bord, pas un verdict de convergence.

Les harmoniques nouvelles `k=5,6` présentes uniquement à `Λ=3` appartiennent à un diagnostic étendu et ne doivent pas être utilisées pour déclarer la convergence du protocole `Λ=2`.

La convergence doit être examinée harmonique par harmonique ; un effet qui suit `j` plutôt que `k` lors du changement de troncature est un indice de verrouillage relatif au bord.

---

## 26. Catégories de connaissance

Les résultats doivent être étiquetés selon leur provenance.

```text
STRUCTURAL_ANALYTIC
    relations de Gauss
    distribution de spread
    dim H_phys(Λ)
    oracle rank(L^k)
    transformations et covariances prouvées
    oracles nuls de symétrie
    implication STATIC PASS => DYNAMIC PASS

PILOT_LAMBDA1
    calculs vus avant pré-enregistrement
    uniquement dans le régime Λ=1

PREREGISTERED_REFERENCE
    quantités non encore calculées à Λ=2
    après gel du protocole

TRUNCATION_CONTROL
    comparaison appariée Λ=2 -> 3

EXTENDED_DIAGNOSTIC
    sondes nouvelles propres au régime de contrôle
    hors verdict principal de convergence
```

Un résultat pilote ne doit jamais être présenté comme confirmatoire. Un fait analytique connu ne doit jamais être présenté comme découverte numérique.

---

## 27. Questions encore ouvertes avant gel complet

Les décisions suivantes restent explicitement ouvertes :

1. convention exacte des relations **ordonnées** source-récepteur pour les orbites dynamiques `O_1A/O_1B` ;
2. ensemble de niveaux `Γ` servant au diagnostic de récurrence de l'autocorrélation locale ;
3. définition numérique finale de la fenêtre temporelle associée à `Γ` ;
4. grille de `η` utilisée pour publier `C_eff^thr(η)` ;
5. algorithme et tolérance de convergence vers l'oracle `C_short` ;
6. résolution temporelle et stratégie d'interpolation / localisation des extrema ;
7. tolérances numériques de toutes les identités et verdicts ;
8. grille de campagne en `(g,μ,δ)` ;
9. critère formel de cohérence de classement entre `C_eff^grow` et `C_eff^thr(η)` ;
10. formulation finale de la fenêtre pré-récurrence et du statut `INCONCLUSIVE` associé.

Aucune de ces valeurs ne doit être choisie après inspection des courbes scientifiques.

---

## 28. Non-objectifs et limites

0B ne démontre pas :

- que `C` est une grandeur fondamentale ;
- que `C_eff` est une vitesse locale ;
- qu'une métrique a émergé ;
- que les contrastes inter-orbites sont géométriques ;
- que le continuum relativiste est obtenu ;
- que le groupe discret déclaré épuise toutes les symétries possibles ;
- qu'une sonde à six sites décrit un front macroscopique ;
- que la troncature finie `Λ=2` est universellement convergée.

Un signal `Δ1 != 0` est uniquement un signal relationnel non uniforme, relatif au protocole, au groupe déclaré, à la troncature et à la famille de fonds correspondants.

---

## 29. Barrière vers l'implémentation

Le présent document n'autorise aucun code.

Avant toute implémentation 0B, il faudra au minimum :

1. fermer les questions du §27 qui affectent les résultats ;
2. mettre le document en `validé pour gel` global ;
3. obtenir la validation explicite de Lionel ORCIL pour le gel ;
4. disposer d'un `validation-plan.md` cohérent ;
5. mettre à jour `docs/governance/current-task.md` pour autoriser explicitement l'audit Claude Code ;
6. exécuter le cycle de collaboration normal : audit read-only, revue conceptuelle, autorisation d'implémentation, implémentation, revue distante, acceptation.
