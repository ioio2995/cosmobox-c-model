# Toy Model 0B — spécification scientifique consolidée

Statut : **revue de clôture pré-gel**  
Projet : `ioio2995/cosmobox-c-model`  
Branche documentaire : `documentation/model0b-foundation`  
Base canonique : `master @ 08d5ca506ff05e15dd9bc084ea121c3d0a19b662`

Ce document est la source scientifique principale consolidée du Toy Model 0B. Les documents spécialisés du même dossier conservent les démonstrations et qualifications détaillées ; ils ne doivent plus être chargés systématiquement dans les prompts lorsque le présent document suffit.

Aucun contenu de ce document n'autorise l'implémentation 0B tant que `docs/governance/current-task.md` ne l'autorise pas explicitement.

---

## 1. Statut du modèle

```text
MODEL0B_SYSTEM_AND_GAUSS           = VALIDÉ POUR GEL
MODEL0B_TRUNCATION_STRUCTURE       = VALIDÉ POUR GEL
MODEL0B_STATIC_OBSERVABLES         = VALIDÉ POUR GEL
MODEL0B_STATIC_IDENTIFIABILITY     = VALIDÉ POUR GEL
MODEL0B_DECLARED_SYMMETRIES        = VALIDÉ POUR GEL
MODEL0B_NULL_ORACLES               = VALIDÉ POUR GEL
MODEL0B_KUBO_PROBE                 = VALIDÉ POUR GEL
MODEL0B_PRIMARY_SIGNAL_DELTA1      = VALIDÉ POUR GEL
MODEL0B_PATH_GRADING               = VALIDÉ POUR GEL
MODEL0B_PATH_PURITY_STRUCTURE      = VALIDÉ POUR GEL
MODEL0B_RECURRENCE_STRUCTURE       = VALIDÉ POUR GEL
MODEL0B_SHORT_TIME_STRUCTURE       = VALIDÉ POUR GEL
MODEL0B_SPECTRAL_TIME_STRUCTURE    = VALIDÉ POUR GEL EN PRINCIPE
MODEL0B_SOFT_LOOP_STRUCTURE        = VALIDÉ POUR GEL
MODEL0B_PARAMETER_CAMPAIGN_SHAPE   = VALIDÉ POUR GEL

MODEL0B_NUMERICAL_CONTROL_VALUES   = OUVERT
MODEL0B_FINAL_ACCEPTANCE_RULES     = OUVERT
IMPLEMENTATION_0B                  = NON AUTORISÉE
```

`VALIDÉ POUR GEL` signifie que le contenu conceptuel peut être soumis au gel. Seule une validation explicite de Lionel ORCIL permettra de passer à `FROZEN`.

Principe de clôture : le challenge scientifique reste permanent, mais un bloc stabilisé n'est rouvert que par une contradiction, une erreur, une impossibilité d'exécution ou un défaut susceptible d'affecter un verdict scientifique. Les améliorations non nécessaires à la validité de 0B sont différées au backlog.

---

## 2. Rôle scientifique et limites

0A a validé l'instrument numérique d'identifiabilité sur un benchmark analytique. 0B introduit pour la première fois un degré cyclique non fixé par Gauss et cherche à tester sa visibilité statique et dynamique avec des observables invariantes de jauge.

0B ne prétend pas démontrer :

- que `C` est une grandeur fondamentale ;
- que `C_eff` est une vitesse locale fondamentale ;
- qu'une métrique ou un continuum relativiste a émergé ;
- que le groupe discret déclaré épuise toutes les symétries possibles ;
- qu'un système à six sites décrit un front macroscopique ;
- que `Lambda=2` est universellement convergé.

Un signal `Delta1 != 0` est seulement un signal relationnel non uniforme, relatif au protocole, au groupe déclaré, au fond et à la troncature.

---

## 3. Système physique et loi de Gauss

Cycle orienté :

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 0
```

Matière :

```math
n_i\in\{0,1\},
\qquad
b=(0,1,0,1,0,1),
\qquad
q_i=n_i-b_i.
```

Liens :

```math
E_i\in\{-\Lambda,\ldots,+\Lambda\}.
```

Shift tronqué :

```math
U_i|E\rangle=
\begin{cases}
|E+1\rangle,&E<\Lambda,\\
0,&E=\Lambda.
\end{cases}
```

`U_i` est un shift partiel tronqué, pas une phase unitaire exacte.

Gauss :

```math
G_i=E_i-E_{i-1}-q_i,
\qquad
\mathcal H_{phys}=\bigcap_i\ker G_i.
```

La somme impose :

```math
\sum_i n_i=3.
```

Pour une configuration de matière `n`, toutes les solutions sont :

```math
E_j=e+s_j(n).
```

Avec :

```math
spread(n)=\max_j s_j(n)-\min_j s_j(n),
```

le nombre de valeurs admissibles de `e` est :

```math
\#\mathcal E_n
=\max(0,2\Lambda+1-spread(n)).
```

Distribution exacte sur les 20 configurations à trois fermions :

| `spread` | nombre |
|---:|---:|
| 0 | 1 |
| 1 | 16 |
| 2 | 3 |

Donc :

```math
\boxed{\dim\mathcal H_{phys}(\Lambda)=40\Lambda-2}
```

pour `Lambda>=1`.

```text
Lambda=1 -> 38
Lambda=2 -> 78
Lambda=3 -> 118
```

Le secteur scientifique principal est `Lambda=2`; `Lambda=3` est le contrôle de troncature ; `Lambda=1` est un régime pilote/régression.

Construction nominale : construire directement la base physique par Gauss, sans espace total dense.

---

## 4. Hamiltonien et état canonique

Unité d'énergie :

```math
J\equiv1.
```

On définit :

```math
h_i=c_i^\dagger U_i c_{i+1},
\qquad
X_i=h_i+h_i^\dagger,
```

```math
N_{even}=n_0+n_2+n_4,
```

```math
V_\delta=\sum_i(-1)^iE_i^2.
```

Hamiltonien :

```math
\boxed{
H(g,\mu,\delta)
=-\sum_iX_i
+g\sum_iE_i^2
+2\mu N_{even}
+g\delta V_\delta.
}
```

Point de référence :

```text
(g_ref,mu_ref,delta_ref)=(1,0,0).
```

Ne pas utiliser `V_stag` pour le terme électrique alterné : cette notation est réservée / historique et crée une collision avec les termes alternés de matière.

Le rééchelonnement global `H -> sH` est exclu de la famille scientifique et conservé uniquement comme oracle de contrôle.

État canonique :

```math
\rho=|\Omega\rangle\langle\Omega|
```

si le fondamental est unique, et :

```math
\boxed{
\rho=P_{GS}/\operatorname{Tr}P_{GS}
}
```

si le fondamental est dégénéré. Aucun vecteur particulier d'un multiplet ne peut être choisi après inspection.

Le rapport doit publier `d_GS` et `gap_GS` à chaque point de campagne. Aucun seuil `NEAR_CROSSING` n'est utilisé comme veto scientifique.

---

## 5. Degré cyclique, flux uniforme et shift de boucle

Gauss fixe les différences de flux mais laisse un zéro-mode uniforme.

```math
\Phi=\frac16\sum_iE_i.
```

Pour une matière fixée :

```math
E=E_{part}(n)+\alpha(1,1,1,1,1,1).
```

Le label d'énumération `e` est seulement une coordonnée de cette fibre :

```math
\Phi=e+c(n).
```

Au niveau tangent :

```math
D_{n_i}=-i[n_i,\rho],
\qquad
D_{E_i}=-i[E_i,\rho],
\qquad
D_\Phi=-i[\Phi,\rho].
```

Gauss donne :

```math
D_{n_i}=D_{E_i}-D_{E_{i-1}}.
```

Donc :

```math
S_n\subseteq S_E,
\qquad
S_E=S_n+span\{D_\Phi\}.
```

Sur `delta=0`, les symétries exactes imposent :

```math
\boxed{D_\Phi\perp S_n}
```

pour toute la variété `(g,mu,0)` et pour l'état canonique pur ou dégénéré.

Si `D_Phi` est actif :

```math
S_E=S_n\oplus_\perp span\{D_\Phi\}.
```

La proposition `dim S_E=6` sur toute la variété est rejetée. Les rangs doivent être recalculés à chaque point.

Shift cyclique :

```math
L=U_0U_1U_2U_3U_4U_5,
\qquad
[\Phi,L]=L.
```

Harmoniques déclarées :

```math
\mathscr H_\Lambda
=span_\mathbb R\{X_{L^k},Y_{L^k}\mid1\le k\le2\Lambda\},
```

```math
X_{L^k}=\frac{L^k+(L^\dagger)^k}{2},
\qquad
Y_{L^k}=\frac{L^k-(L^\dagger)^k}{2i}.
```

Aucune fermeture algébrique implicite n'est autorisée.

Oracle de rang : pour `j=2Lambda-k`,

```math
r_\Lambda(L^k)
=\sum_n\max(0,j+1-spread(n)).
```

| `j` | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| rang | 1 | 18 | 38 | 58 | 78 | 98 |

---

## 6. Familles de mesure et identifiabilité

### Espace tangent et carte de mesure

Les rangs instrumentaux sont des rangs de fonctionnelles sur l'espace tangent :

```math
\mathcal V=\{A=A^\dagger,\ \operatorname{Tr}A=0\}.
```

Sur `V`, la composante identité d'une observable est invisible. Pour toute observable `O`, on peut donc utiliser indifféremment `O` ou son représentant traceless :

```math
\widetilde O=O-\frac{\operatorname{Tr}O}{d_{phys}}I.
```

Pour une famille ordonnée `F={O_mu}`, `mu=1..m`, la carte de mesure est :

```math
\boxed{
\mathcal M_F(A)
=\bigl(\operatorname{Tr}(A\widetilde O_1),\ldots,
       \operatorname{Tr}(A\widetilde O_m)\bigr).
}
```

`rank(F)` désigne toujours le rang de `M_F`, c'est-à-dire la dimension du span des représentants traceless, jamais le nombre brut d'opérateurs listés.

### Transport gauge-dressed le long d'un arc

Pour un arc simple orienté :

```text
P=(i_0,i_1,...,i_d)
```

le transporteur de jauge `W_P` est le produit ordonné des `U_i` lorsque l'arc suit l'orientation du lien et des `U_i^dagger` lorsqu'il la remonte. Le transport ouvert est :

```math
T_P=c_{i_0}^\dagger W_P c_{i_d},
```

et ses deux quadratures hermitiennes sont :

```math
X_P=\frac{T_P+T_P^\dagger}{2},
\qquad
Y_P=\frac{T_P-T_P^\dagger}{2i}.
```

Une normalisation globale non nulle différente ne change ni le span ni les rangs. Pour une paire non orientée, inverser simultanément l'arc et ses extrémités envoie `T_P` sur `T_P^dagger` : cela ne crée donc pas une nouvelle paire de quadratures indépendante dans la famille.

### Familles exactes

Stratification statique :

```math
F_D\subset F_{edge}\subset F_{path}\subset F_{loop}^{(1)}\subset F_{loop}^{harm}.
```

```text
F_D
    {n_i,E_i}, i=0..5

F_edge
    F_D
    + {X_P,Y_P} pour les six arcs minimaux de distance 1

F_path
    F_edge
    + {X_P,Y_P} pour les six arcs minimaux uniques de distance 2
    + {X_P,Y_P} pour les deux arcs minimaux de chacune des trois paires opposées d=3

F_loop^(1)
    F_path + {X_L,Y_L}

F_loop^harm
    F_path + span_R{X_{L^k},Y_{L^k} | 1<=k<=2*Lambda}
```

Sur le secteur physique, la relation :

```math
n_i-b_iI=E_i-E_{i-1}
```

montre que la partie traceless des `n_i` est déjà portée par le span des `E_i`.

Toujours distinguer :

```math
span(F)\neq Alg(F).
```

### Rangs pilotes

Pilote `Lambda=1`, déjà vu avant pré-enregistrement :

```text
rank(F_D)        = 6
rank(F_edge)     = 18
rank(F_path)     = 36
rank(F_loop^(1)) = 38
rank(L)          = 18
```

Ce sont des **rangs mesurés de `M_F`**, une fois l'identité quotientée par la restriction `Tr A=0`, et non des comptages d'éléments de famille. `rank(F_D)=6` est ainsi cohérent avec les douze opérateurs listés dans `F_D`, et `rank(F_path)` ne se reconstruit pas par simple addition du nombre d'observables ajoutées.

Ces nombres restent `PILOT_LAMBDA1`, jamais confirmatoires pour `Lambda=2`.

Pour une famille de paramètres déclarée, l'identifiabilité porte sur le sous-espace de réponse `S_resp`, pas sur toute l'algèbre des matrices.

Gate 0 : un générateur `A` est `INACTIVE` si :

```math
[A,P_{GS}]=0.
```

Gate statique : tester :

```math
S_{resp}\cap\ker\mathcal M_F.
```

`STATIC PASS` implique `DYNAMIC PASS` car le span statique est inclus dans le Krylov.

En cas de `STATIC FAIL`, tester le sous-espace de Krylov :

```math
\mathcal L_H(O)=i[H,O],
```

```math
\mathscr W(F,H)=span\{F,\mathcal L_HF,\mathcal L_H^2F,\ldots\}.
```

`DYNAMIC PASS` autorise l'étude de la réponse temporelle ; il ne valide pas automatiquement `C_eff`.

---

## 7. Symétries déclarées et relations exactes

Le groupe déclaré inclut les transformations unitaires / antiunitaires générées par `T`, `R`, `C` et `K`; il ne prétend pas être le groupe mathématique exhaustif de toutes les symétries possibles.

Éléments utiles :

```text
T^2 : translation de deux sites, conserve le fond
C   : particule-trou bipartite
S   = T C, conserve le secteur physique à delta=0 et retourne delta dans la famille
R   : réflexion j -> -j, retourne delta
Q   = S R, symétrie exacte de H(g,mu,delta)
K   : conjugaison complexe dans la base occupation-flux réelle
```

Covariance principale :

```math
R H(g,\mu,\delta)R^\dagger=H(g,\mu,-\delta).
```

Sur les occupations :

```math
Qn_pQ^\dagger=1-n_{1-p}.
```

`K` impose :

```math
\chi_{pq}(-t)=-\chi_{pq}(t).
```

Stationnarité + `K` donnent :

```math
\boxed{\chi_{pq}(t)=\chi_{qp}(t)}.
```

Les relations source-récepteur sont donc traitées comme non orientées. L'ancien `ORDERED_RELATION_CONVENTION=OPEN` est clos.

Classes d'arêtes :

```text
O1A = {(0,1),(2,3),(4,5)}
O1B = {(0,5),(1,2),(3,4)}
```

Oracles exacts :

```math
\boxed{\Delta_1(g,\mu,0)=0}
```

```math
\boxed{\Delta_1(g,\mu,-\delta)=-\Delta_1(g,\mu,+\delta)}
```

```math
\boxed{\Delta_2(g,\mu,\delta)=0}
```

pour toute la famille.

---

## 8. Sonde de Kubo et temps court

Pour un fond `theta=(g,mu,delta)` :

```math
\chi_{pq}^{(\theta)}(t)
=iTr\left[\rho_\theta[n_p,n_q^{(\theta)}(t)]\right].
```

```math
\mathcal F_{pq}(t)=\chi_{pq}(t)^2/4,
\qquad
0\le\mathcal F\le1.
```

Pour `p!=q` :

```math
\mathcal F_{pq}(0)=0.
```

Le paramètre infinitésimal de Kubo est une sonde et ne doit jamais être confondu avec les paramètres physiques du fond.

Convention opératorielle :

```math
ad_H(O)=[H,O],
\qquad
\mathcal L_H(O)=i[H,O].
```

Développement :

```math
n_q(t)=\sum_{r\ge0}\frac{(it)^r}{r!}ad_H^r(n_q).
```

La symétrie `K` impose que `chi` ne contienne que des puissances impaires.

Règle bipartite :

```text
d pair   -> nombre impair d'insertions diagonales requis dans tout terme cible physique
d impair -> nombre pair d'insertions diagonales ; zéro autorisé
```

Pour N=6 :

```text
d=1 -> nu=1 si l'arête est régulière
d=2 -> premier ordre cible physique r=3
d=3 -> premier ordre physique possible r=3
pure hopping -> canal cible d=2 exactement inactif
```

Moments : pour un fondamental pur et `r>=1`,

```math
M_r^{pq}
=-2\langle\Omega|n_p(H-E_0)^rn_q|\Omega\rangle
=-2\langle\Omega|n_p ad_H^r(n_q)|\Omega\rangle.
```

La généralisation canonique utilise la trace sur `P_GS/d_GS` ; le shell `omega=0` est traité séparément et ne contribue pas aux moments `r>=1`.

Pour une arête `{p,q}={i,i+1}` :

```math
M_1^{pq}=J\langle X_i\rangle.
```

Pour `d(p,q)>=2` :

```math
M_1^{pq}=0.
```

Le premier moment impair non nul fixe `nu`. Une annulation flottante n'est exacte que si elle découle d'une règle structurelle démontrée ou d'un calcul exact / contrôle numérique préenregistré.

Oracle court : si référence et état ont le même exposant `nu`,

```math
C_{short}^{pq}=|a_{state}/a_{ref}|^{1/\nu}.
```

Pour une arête régulière :

```math
\Delta_1^{short}(\delta)
=\log\left|\frac{\langle X\rangle_{A,\delta}}{\langle X\rangle_{B,\delta}}\right|.
```

`Delta1_short` est un oracle algébrique, pas une mesure de propagation.

---

## 9. Représentation spectrale exacte

Dans la base `K`-réelle, pour l'état canonique stationnaire :

```math
\boxed{
\chi_{pq}(t)=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
}
```

En cas de dégénérescence excitée, les poids doivent être groupés par projecteur spectral ; le nombre brut de vecteurs propres portant un coefficient non nul n'est pas invariant.

Conséquences normatives :

```text
FINITE_DIFFERENCE_TIME_DERIVATIVE = REJECTED
INTERPOLATION_AS_FINAL_ESTIMATOR   = REJECTED
NUMERICAL_QUADRATURE_FOR_P_ALPHA   = NOT_NOMINAL
```

Les dérivées sont obtenues analytiquement terme à terme.

Pour un canal sectoriel :

```math
\chi_\alpha(t)=\sum_jC_{\alpha j}\sin(\omega_jt),
```

et :

```math
P_\alpha(\tau)=\int_0^\tau\chi_\alpha(t)^2dt
```

est évalué par les intégrales fermées de produits de sinus.

---

## 10. Temps caractéristiques et certification

Définitions scientifiques sur :

```math
F(t)=\chi(t)^2/4.
```

Premier pic :

```math
T_{peak}=\inf\{t>0:F'(t)=0\text{ avec changement }+\to-\}.
```

Numériquement, le premier pic est cherché comme première racine **qualifiante** de :

```math
\chi'(t)=0.
```

Pour une racine non dégénérée :

```math
\chi(T_{peak})\chi''(T_{peak})<0.
```

Temps primaire :

```math
T_{grow}=\inf\operatorname*{argmax}_{0<t<T_{peak}}F'(t).
```

Candidats intérieurs :

```math
H_{grow}(t)=\chi'(t)^2+\chi(t)\chi''(t)=0.
```

Temps de seuil :

```math
T_{thr}(\eta)=\inf\{0<t<T_{peak}:F(t)=\eta,\ F'(t)>0\}.
```

Sur le premier lobe, avec signe `s` de `chi`, résoudre :

```math
\chi(t)-s\,2\sqrt\eta=0.
```

`T_down(eta)` est le premier croisement descendant du même niveau après `T_peak` dans le premier lobe.

Une seule famille de raffinement :

```math
\mathcal B=\{\beta_1>\cdots>\beta_K>0\}.
```

Taille nominale d'une cellule :

```math
\Delta t_k^{event}
=\beta_k\frac{\pi}{s_{event}\Omega_{scale}},
```

avec :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

et par défaut une borne sûre :

```math
\Omega_{scale}=E_{max}-E_0.
```

Une fréquence active déterminée par un seuil numérique sur les coefficients n'est pas utilisée comme borne par défaut.

Valeurs préenregistrées :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}
```

`beta` contrôle uniquement le maillage initial de certification / bracketing ; ce n'est pas une tolérance sur le temps final, celui-ci restant obtenu par le solveur spectral continu. `beta=1` correspond à une demi-période de la bande maximale de la fonction de certification ; le raffinement est dyadique imbriqué ; `beta=1/8` donne une phase maximale `pi/8` par cellule à la bande limite. Aucune finesse supplémentaire n'est requise comme garantie de complétude, celle-ci reposant sur l'exclusion certifiée des cellules, leur subdivision adaptative et le solveur continu.

Critère de contrôle sous raffinement : identité du premier événement stable, ordre des candidats pertinents stable, aucune cellule antérieure non résolue, temps continus compatibles selon les tolérances numériques (`OPEN`). Si cette stabilité échoue : `TIME_EVENT_CONTROL_SENSITIVE`.

Les tolérances numériques (solveur, argmax, précision spectrale) restent ouvertes.

---

## 11. Multigraduation et interprétation de chemin

Les superopérateurs :

```math
\mathscr L_i(O)=[E_i,O]
```

commutent et définissent des projecteurs d'espace d'opérateurs `Pi_m` sur :

```math
m=(m_0,...,m_5).
```

Pour une transition de matière :

```math
m_i-m_{i-1}=\Delta n_i.
```

La fibre compatible est :

```math
m=m_D+w\mathbf1.
```

Pour `d<N/2` :

```text
TARGET_DIRECT          = transition ciblée, w=0
TARGET_WINDING         = transition ciblée, w!=0
NON_TARGET_TRANSITION  = autre transition de matière
```

Pour `d=3`, les deux arcs minimaux ont la même longueur ; aucune interprétation d'arrivée mono-arc n'est autorisée.

Canal physique générique : paire adjointe `{m,-m}`. Le cas `m=0` est auto-conjugué et doit être compté une seule fois en algèbre générale.

Dans le secteur physique 0B :

```math
n_i=b_i+E_i-E_{i-1}.
```

Les six flux déterminent donc entièrement la matière et les sous-espaces propres conjoints de tous les `E_i` sont unidimensionnels. Ainsi :

```math
[n_p,\Pi_0(O)]=0
```

pour tout `O`, donc :

```text
ZERO_GRADE_KUBO_CHANNEL      = INACTIVE_EXACT
ZERO_GRADE_NON_TARGET_WEIGHT = ZERO_EXACT
```

Au niveau des moments sectoriels, il faut conserver le commutateur projeté :

```math
B_{m,r}^{pq}
=Tr\left(\rho[n_p,\Pi_m ad_H^r(n_q)]\right).
```

Pour `m!=0` :

```math
B_{-m,r}=(-1)^{r+1}\overline{B_{m,r}}.
```

Dans la base réelle, les ordres pairs s'annulent canal par canal ; pour `r` impair :

```math
a_{r,[m]}^{pq}
=\frac{2(-1)^{(r+1)/2}}{r!}B_{m,r}^{pq}.
```

---

## 12. Pureté de chemin et garde de récurrence

Pour chaque canal physique distinct `alpha` :

```math
P_\alpha(\tau)=\int_0^\tau\chi_\alpha(t)^2dt.
```

Agrégats :

```math
P_{sector}=P_{direct}+P_{winding}+P_{non-target}.
```

```math
Purity_{direct}=P_{direct}/P_{sector}.
```

Cette pureté est un indice de composition sectorielle, pas une probabilité ni une décomposition additive de `chi^2`.

### Garde de pureté normalisée

La garde normative n'est pas fondée sur une impureté absolue commune à tous les fonds.

Ligne de base algébrique, à calculer avant toute évolution temporelle :

```math
P_0(\theta,\Lambda,pq)=Purity_{direct}(0^+),
\qquad
I_0(\theta)=1-P_0(\theta).
```

Enveloppe monotone d'impureté :

```math
I_{max}(\theta,\tau)
=\sup_{0<s\le\tau}\bigl[1-Purity_{direct}(\theta,s)\bigr].
```

Lorsque `P_0>0`, la garde porte sur la dégradation supplémentaire normalisée :

```math
\boxed{
R_{path}(\theta,\tau)
=\frac{I_{max}(\theta,\tau)-I_0(\theta)}{P_0(\theta)}.
}
```

La famille de contrôle commune est `epsilon in E_path subset (0,1)`, préenregistrée, avec :

```math
\tau_{path}(\epsilon)
=\inf\{\tau>0:R_{path}(\tau)>\epsilon\}.
```

Un événement passe la garde pour `epsilon` si :

```math
R_{path}(T_{event})\le\epsilon.
```

Lorsque `P_0=0` :

```text
PATH_BASELINE_STATUS = NO_DIRECT_BASELINE
```

et `R_path` n'est pas applicable.

À `d=1` régulier, `P_0=1` et `I_0=0` : `R_path` se réduit à l'impureté enveloppée absolue. À `d=2`, `P_0` n'est pas structurellement égal à `1` et doit être publié par domaine complet `(theta,Lambda,pq)`.

Les valeurs numériques de `E_path` restent ouvertes. Toute formulation appliquant une grille de contrôle commune directement à `I_max` est supersédée.

### Garde de récurrence

Sites normatifs :

```text
RECURRENCE_SITE_SET(p,q) = {p,q}
```

Les sites intermédiaires sont `DIAGNOSTIC_ONLY` et ne participent pas au veto normatif.

La récurrence est contrôlée par l'autocorrélation locale connectée normalisée :

```math
C_j(t)
=\frac{Re\,Tr[\rho_\theta\,\delta n_j(t)\delta n_j]}
{Tr[\rho_\theta(\delta n_j)^2]}.
```

Si le dénominateur est nul :

```text
RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
```

Détecteur hystérétique : pour :

```math
\gamma=(\gamma_-,\gamma_+),
\qquad\gamma_-<\gamma_+<1,
```

et un horizon `tau`, il y a sortie lorsque `C_j<=gamma_-`, puis retour si `C_j>=gamma_+` après cette sortie et avant `tau`. Les trois états sont exhaustifs :

```text
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
```

Pour la relation `(p,q)`, le statut de garde combine les deux extrémités : un retour à l'une quelconque des extrémités compte comme retour avant événement.

Horizons normatifs :

```text
T_grow       -> tau = T_peak
T_thr(eta)   -> tau = T_down(eta)
```

`T_down` est donc un auxiliaire obligatoire de la garde de récurrence des seuils, et non un estimateur scientifique indépendant.

Domaine `Gamma` : ensemble préenregistré contenu dans :

```math
\{(\gamma_-,\gamma_+):\gamma_-<\gamma_+<1\}
```

et borné dans l'ordre partiel :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm},
```

avec :

```math
\gamma_-^{strict}\le\gamma_-\le\gamma_-^{perm},
\qquad
\gamma_+^{strict}\ge\gamma_+\ge\gamma_+^{perm}.
```

Aucun domaine rectangulaire `G_- x G_+` n'est exigé. La largeur `h(gamma)=gamma_+-gamma_->0` est explicite ; le point permissif porte la largeur minimale positive du domaine préenregistré, et `h=0` est exclu du contrôle principal.

Verdict robuste par les deux bornes :

```text
gamma_perm ne détecte aucun retour
    -> RECURRENCE_STATUS = ROBUST_CLEAN

gamma_strict détecte un retour
    -> RECURRENCE_STATUS = ROBUST_CONTAMINATED

sinon
    -> RECURRENCE_STATUS = CONTROL_SENSITIVE
```

Les valeurs numériques de `Gamma` restent ouvertes.

### Condition d'interprétation

Un événement temporel est interprétable comme arrivée propre seulement si :

```text
PATH_CONTROL_ACCEPTABLE
AND RECURRENCE_CONTROL_ACCEPTABLE
```

sur les familles de contrôle préenregistrées.

---

## 13. Sonde relative et contrastes

Pour une même paire :

```math
C_{eff}^{grow}
=\frac{T_{grow}^{ref}}{T_{grow}^{state}},
```

```math
C_{eff}^{thr}(\eta)
=\frac{T_{thr}^{ref}(\eta)}{T_{thr}^{state}(\eta)}.
```

Ces deux estimateurs ne sont pas forcés à être égaux. Leur règle finale de cohérence reste à préenregistrer.

Le rééchelonnement `H_s=sH_ref` impose exactement :

```math
F_s(t)=F_{ref}(st),
```

et :

```math
C_{eff}^{grow}=C_{eff}^{thr}(\eta)=s.
```

Contraste d'orbites :

```math
\Delta_{\alpha\beta}
=\log\frac{C_{O_\alpha}}{C_{O_\beta}}.
```

Signal primaire :

```math
\boxed{
\Delta_1
=\log\frac{C_{O1A}}{C_{O1B}}.
}
```

Oracle nul :

```math
\boxed{\Delta_2=0.}
```

La susceptibilité :

```math
\Xi_1
=\left.\frac{\partial\Delta_1}{\partial\delta}\right|_{\delta=0}
```

est secondaire et locale. `Xi1=0` n'est pas un FAIL automatique.

---

## 14. Campagne principale

Campagne nominale :

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

Cette campagne mesure `Delta1` à brisure finie, souvent non linéaire. Elle ne doit pas servir à estimer `Xi1`.

Contrôles séparés :

```text
g=0, mu=0    -> pure-hopping oracle
g=0.10       -> stress faible-g hors nominal
delta=0.9    -> qualification / stress hors nominal
```

La covariance `delta<->-delta` doit être exercée sur un sous-ensemble négatif préenregistré. Le sous-ensemble exact reste ouvert.

---

## 15. Qualification de troncature

Les données de qualification déjà vues sont **non confirmatoires** et doivent être divulguées.

La saturation :

```math
B_2=P(\max_i|E_i|=2)
```

est un indicateur de pression au bord, pas une erreur de troncature.

Tendances de design déjà connues : faible `g` augmente fortement le stress ; `mu<0` est plus tendu ; `delta` est moins dominant aux points testés.

Le résidu de Ritz de l'état `Lambda=2` plongé dans `Lambda=3` est un diagnostic de design plus direct du couplage aux états omis.

Le contrôle scientifique `Lambda=2 -> 3` doit comparer les mêmes observables et les mêmes valeurs physiques des paramètres.

Pour les harmoniques : appariement principal à `k` fixe ; appariement à `j=2Lambda-k` comme diagnostic relatif au bord.

Le sous-ensemble exact des points de stress `Lambda=3` reste à préenregistrer.

---

## 16. Sous-campagne SOFT-LOOP

Sous-campagne :

```text
g  = 1
mu = {-1.25, -1.5, -2}
```

Elle vise le doublet cyclique mou et reste distincte de MAIN.

À `mu<0` fort, la matière se concentre sur le sous-réseau pair et le doublet central de flux est relié par un processus de six hoppings.

Structure analytique :

```math
\boxed{t_{loop}=O(J^6/|\mu|^5).}
```

Les données déjà vues montrant une pente vers `-5` sont de la qualification non confirmatoire.

Modèle effectif :

```math
H_{eff}=E_cI+3g\delta\sigma_z+t_{loop}\sigma_x+\cdots.
```

Dans le doublet :

```math
2\Phi\to\sigma_z.
```

Avec :

```math
x=\frac{6g\delta}{gap_0},
```

les deux prédictions statiques sont :

```math
\frac{gap(\delta)}{gap_0}\simeq\sqrt{1+x^2},
```

```math
2\langle\Phi\rangle\simeq-\frac{x}{\sqrt{1+x^2}}.
```

Le signe est fixé : pour `delta>0` (`x>0`), l'état central de flux `e=0` est énergétiquement favorisé, avec `Phi -> -1/2` dans la limite de forte polarisation.

Ces collapses constituent la porte statique de SOFT-LOOP et doivent être testés avant toute interprétation dynamique fondée sur `delta_c`.

La grille physique préenregistrée de la porte statique est :

```text
STATIC_X_PRIMARY = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_X_SATURATION_DIAGNOSTIC = {±4}
```

L'ensemble discriminant pour un futur critère de collapse agrégé est :

```text
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES = {1/4, 1/2, 1, 2}
```

`STATIC_X_SATURATION_DIAGNOSTIC` est `EXTENDED_DIAGNOSTIC`. Les points de signe négatif sont un contrôle numérique / oracle d'implémentation de la covariance exacte `R H(g,mu,delta) R^dagger = H(g,mu,-delta)`, pas une évidence indépendante de collapse (`NEGATIVE_X_HALF_ROLE = NUMERICAL_CONTROL / IMPLEMENTATION_ORACLE`). `x=0` est un contrôle de normalisation/symétrie, pas une évidence de collapse discriminante (`STATIC_X_ZERO_ROLE = NUMERICAL_CONTROL / NORMALIZATION_ORACLE`). Le détail de ces rôles et de la classification `EXTENDED_DIAGNOSTIC` est porté par `soft-loop-static-gate.md`.

Le critère numérique de conformité de la porte statique est `VALIDATED_FOR_FREEZE` :

```text
STATIC_COLLAPSE_NUMERICAL_CRITERION = VALIDATED_FOR_FREEZE
STATIC_COLLAPSE_TOLERANCE           = 0.10
```

La classification est faite en norme `POINTWISE_L_INFINITY` sur les magnitudes
informatives `{1/4,1/2,1,2}`, avec résidu de gap relatif et résidu de
polarisation absolu. À `Lambda=3`, la garde d'information exige que la
magnitude maximale échantillonnée sur ces points, `X_max^(3)`, atteigne le
croisement `|x|=1` (`STATIC_LAMBDA3_INFORMATION_GUARD = REQUIRED`,
`STATIC_LAMBDA3_MIN_DISCRIMINATING_MAGNITUDE = 1`) ; sinon un résultat
`SUPPORTED` ordinaire est requalifié `SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION`
(`NUMERICAL_CONTROL / NONCONFIRMATORY_FOR_CUTOFF_STABILITY`). Une
revendication de mécanisme à deux niveaux stable au cutoff exige
`SOFT_LOOP_STATIC_SUPPORTED` ordinaire à la fois à `Lambda=2` et à `Lambda=3` ;
`SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION` ne qualifie pas. Le statut
`SOFT_LOOP_STATIC_SUPPORTED` autorise l'exécution du protocole dynamique mais
reste provisoire pour l'interprétation confirmatoire finale de campagne tant
que `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` (`OPEN`) n'est pas fermé et
validé. Les formules complètes, les intervalles numériques et l'ordre de
classification sont définis intégralement dans `soft-loop-static-gate.md`.

Le modèle effectif motive l'échelle analytique :

```math
\delta_c^{eff}=\frac{gap_0}{6g}.
```

Pour le protocole numérique confirmatoire, l'échelle opérationnelle est définie à partir du gap calculé au cutoff de référence :

```math
\boxed{
\delta_c(g,\mu)
=
\frac{gap_{GS}^{(\Lambda=2)}(g,\mu,0)}{6g}.
}
```

La famille SOFT-LOOP préenregistrée est :

```math
\boxed{
\mathcal A_\delta
=
\left\{
\frac12,\frac14,\frac18,\frac1{16}
\right\}.
}
```

Les pas physiques sont :

```math
h_k=\alpha_k\delta_c.
```

Les mêmes valeurs physiques `h_k`, générées à partir de `Lambda=2`,
sont utilisées à `Lambda=3`.

Pour une `Delta1` lisse et impaire :

```math
\widehat\Xi_1(\alpha)
=
\Xi_1+C_2\alpha^2+O(\alpha^4).
```

L'estimateur primaire publié est :

```math
\boxed{
X_3=\widehat\Xi_1(1/16).
}
```

Le contrôle de stabilité est défini intégralement dans
`derivative-control.md`.

Ses statuts sont :

```text
DERIVATIVE_STABLE_QUADRATIC
DERIVATIVE_NUMERICAL_FLOOR
DERIVATIVE_CONTROL_SENSITIVE
DERIVATIVE_NOT_APPLICABLE
```

La voie `DERIVATIVE_STABLE_QUADRATIC` exige notamment l'intervalle certifié
`[Q_min,Q_max] subset [2,8]` défini dans `derivative-control.md`.

Le budget numérique propagé depuis les temps est défini dans
`derivative-error-budget.md` et porte le statut :

```text
DELTA1_PROPAGATED_ERROR_BUDGET = VALIDATED_FOR_FREEZE
```

Richardson est strictement secondaire :

```text
RICHARDSON = SECONDARY_EXTRAPOLATION
```

Il est autorisé uniquement sous `DERIVATIVE_STABLE_QUADRATIC`,
ne remplace pas `X_3` et ne peut pas modifier seul le verdict confirmatoire.

Les détails normatifs de `Q_min`, `Q_max`, `E_Xi_num`, `R_1`, `R_2`
et de leurs budgets restent dans les deux documents spécialisés ;
ne pas les dupliquer ici.

`Delta1` n'est pas obligé de suivre une courbe universelle à deux niveaux ; un éventuel collapse dynamique est une hypothèse secondaire.

---

## 17. Catégories de connaissance

```text
STRUCTURAL_ANALYTIC
    théorèmes et oracles connus avant exécution confirmatoire

PILOT_LAMBDA1
    résultats historiques Lambda=1

QUALIFICATION_NONCONFIRMATORY
    données de design vues avant gel

PREREGISTERED_REFERENCE
    mesures Lambda=2 exécutées seulement après gel

TRUNCATION_CONTROL
    comparaison appariée Lambda=2 -> 3

EXTENDED_DIAGNOSTIC
    contrôles hors verdict principal
```

Aucun résultat pilote ou de qualification ne doit être présenté comme confirmatoire.

---

## 18. Paramètres réellement ouverts avant gel

### Contrôle temporel et précision

`ROOT_SOLVER_TOLERANCES`, `SPECTRAL_PRECISION_CONTROL`,
`SIMPLE_ROOT_CONTROL` et `DELTA1_PROPAGATED_ERROR_BUDGET`
sont `VALIDATED_FOR_FREEZE`.

`ARGMAX_TOLERANCES` est également `VALIDATED_FOR_FREEZE`, avec
`ARGMAX_TOLERANCE = 1e-10`; sa définition normative détaillée est portée par
`temporal-event-solver.md` §25.

`DEGENERATE_ROOT_CONTROL` est `VALIDATED_FOR_FREEZE`, avec
`DEGENERATE_ROOT_NEW_TOLERANCE = NONE` ; le protocole normatif détaillé du
contrôle fail-closed des racines dégénérées ou quasi-dégénérées est porté par
`temporal-event-solver.md` §26.

### SOFT-LOOP

Aucun paramètre encore `OPEN` dans cette catégorie.

Les éléments suivants sont `VALIDATED_FOR_FREEZE` :

```text
STATIC_X_CONTROL_VALUES
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE
STATIC_COLLAPSE_NUMERICAL_CRITERION
```

### Interprétation temporelle

```text
ETA_GRID_AND_ADMISSIBLE_DOMAIN
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE
EPS_PATH_CONTROL_DOMAIN_AND_GRID
GAMMA_CONTROL_DOMAIN_AND_GRID
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS
```

### Campagne / troncature

```text
NEGATIVE_DELTA_ORACLE_SUBSET
TRUNCATION_STRESS_POINT_SUBSET
TRUNCATION_COMPARISON_TOLERANCES
```

### Verdicts

```text
ESTIMATOR_COHERENCE_CRITERION
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

Ne sont notamment plus ouverts : orientation source-récepteur, grille MAIN
`(g,mu,delta)`, choix interpolation vs solveur, différences finies temporelles,
seuil `NEAR_CROSSING`, traitement du canal `m=0`, facteur de bande global
des événements, `ROOT_SOLVER_TOLERANCES`, `SPECTRAL_PRECISION_CONTROL`,
`SIMPLE_ROOT_CONTROL`, `DELTA1_PROPAGATED_ERROR_BUDGET`, `A_DELTA_VALUES`,
`DERIVATIVE_STABILITY_CRITERION`, `RICHARDSON_USAGE_RULE`,
`ARGMAX_TOLERANCES`, `DEGENERATE_ROOT_CONTROL` et
`STATIC_COLLAPSE_NUMERICAL_CRITERION`.

---

## 19. Barrière vers l'implémentation

Avant tout code 0B :

1. faire l'audit critique read-only de clôture ;
2. classer les objections en `BLOCKING`, `NON_BLOCKING_BACKLOG` ou `REJECTED` ;
3. fermer en un lot les paramètres du §18 ;
4. mettre `validation-plan.md` en cohérence avec cette spécification ;
5. effectuer une revue finale de cohérence et de syntaxe ;
6. obtenir la décision explicite de gel de Lionel ORCIL ;
7. autoriser explicitement le lot d'audit / implémentation dans `current-task.md`.

Claude Code conserve un rôle critique pendant l'implémentation. Une objection bloquante stoppe le lot et retourne à l'arbitrage ; une amélioration non nécessaire à la validité est différée.

---

## 20. Supports analytiques détaillés

Les preuves et qualifications détaillées sont conservées notamment dans :

```text
symmetry-proof.md
cyclic-tangent-orthogonality.md
short-time-oracles.md
sector-parity-selection.md
d2-asymptotic-structure.md
d2-free-hopping-oracle.md
path-grading.md
transition-fibers.md
path-purity-control.md
zero-grade-self-adjoint-sector.md
recurrence-control.md
recurrence-order-domain.md
recurrence-site-scope.md
exact-spectral-response.md
operator-moment-oracles.md
event-bandwidth-bracketing.md
temporal-event-solver.md
parameter-campaign-structure.md
truncation-design-qualification.md
negative-mu-soft-loop.md
soft-loop-static-gate.md
derivative-control.md
derivative-error-budget.md
```

Ces supports documentent les démonstrations ; le statut courant et les choix normatifs doivent rester cohérents avec le présent document et `validation-plan.md`.
