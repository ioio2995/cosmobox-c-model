# Toy Model 0B — spécification scientifique consolidée

Statut : **FROZEN — spécification scientifique gelée**  
Projet : `ioio2995/cosmobox-c-model`  
Branche documentaire : `documentation/model0b-foundation`  
Base canonique : `master @ 08d5ca506ff05e15dd9bc084ea121c3d0a19b662`
Base de gel : `d796c65d2538eaba2be7882647ba91db5cf93a32`

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

MODEL0B_NUMERICAL_CONTROL_VALUES   = VALIDÉ POUR GEL
MODEL0B_FINAL_ACCEPTANCE_RULES     = VALIDÉ POUR GEL
MODEL0B_FREEZE_READINESS           = COMPLETED_BY_EXPLICIT_FREEZE_DECISION
MODEL0B_STATUS                     = FROZEN
MODEL0B_FREEZE_DECISION            = EXPLICITLY_APPROVED
MODEL0B_FREEZE_DECISION_DATE       = 2026-08-24
MODEL0B_FREEZE_BASE_COMMIT         = d796c65d2538eaba2be7882647ba91db5cf93a32
IMPLEMENTATION_0B                  = NON AUTORISÉE
```

Lionel ORCIL a donné la décision explicite de gel. Le contenu
scientifique/protocolaire figé à la base de gel ci-dessus est désormais
verrouillé (`FROZEN`). Une réouverture d'un bloc gelé n'est possible que dans
les conditions de gouvernance bloquantes déjà définies : contradiction
avérée, erreur affectant la validité, définition inexécutable ou défaut
susceptible de changer un verdict. Les améliorations, extensions,
généralisations, estimateurs alternatifs ou nouvelles questions de recherche
vont au backlog ou à un niveau de modèle ultérieur. L'implémentation reste
séparément non autorisée (`IMPLEMENTATION_0B = NON AUTORISÉE`) : le gel ne
l'autorise pas. Enregistrement normatif complet :
`docs/toy-models/toy0b/freeze-record.md`.

`MODEL0B_FINAL_ACCEPTANCE_RULES = VALIDÉ POUR GEL` ferme le mode
d'acceptation finale des revendications scientifiques de 0B (statuts de
méta-routage fail-closed, deux rangs explicites de revendication `Delta1`,
sémantique existence/absence-de-signal, coupe-feu échec/non-confirmation).
Définition normative complète : `final-acceptance-rules.md`.
`MODEL0B_FREEZE_READINESS = COMPLETED_BY_EXPLICIT_FREEZE_DECISION` : la
préparation documentaire/protocolaire est désormais close par la décision
explicite de gel de Lionel ORCIL ; cela ne signifie pas que la campagne
confirmatoire a été exécutée.

`MODEL0B_NUMERICAL_CONTROL_VALUES = VALIDÉ POUR GEL` signifie que les vingt-et-un
paramètres numériques majeurs préenregistrés de 0B, y compris le dernier,
`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE` (définition
normative complète : `numerical-zero-symmetry-control.md`), sont désormais
fermés (`OPEN_MAJOR_CONTROLS = 0`) et gelés avec le reste du modèle. Ceci ne
vaut pas autorisation d'implémentation ; `GROUPED_SPECTRAL_SUPPORT_ORACLE`
reste `OPEN_PENDING_SYMMETRY_DERIVATION` et hors de ce décompte, comme
backlog analytique non bloquant.

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

Le routage numérique fail-closed de ce test de rang/noyau (SVD `p/2p`,
classification `ROBUST_NONZERO`/`NUMERICALLY_ZERO_COMPATIBLE`/`CONTROL_SENSITIVE`,
`STATIC = NUMERICALLY_INCONCLUSIVE` tant que l'injectivité requise n'est pas
robuste-non-nulle, `STATIC = FAIL` uniquement sur certificat structurel/exact
de noyau) est fixé par `STATIC_DYNAMIC_NUMERICAL_RANK_RULE =
ROBUST_NONZERO_FOR_INJECTIVITY_EXACT_CERTIFICATE_FOR_KERNEL` (définition
normative complète : `numerical-zero-symmetry-control.md` §F16, §G). Une
valeur singulière numériquement petite ne crée jamais `STATIC FAIL` ni
`DYNAMIC FAIL`.

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

Ces oracles restent des théorèmes exacts, indépendants de toute exécution
numérique. Le contrôle numérique zéro/symétrie (`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
= VALIDATED_FOR_FREEZE` ; définition normative complète :
`numerical-zero-symmetry-control.md`) distingue strictement ce rôle
(`ZERO_SYMMETRY_EXACT_ORACLE_ROLE = IMPLEMENTATION_AND_NUMERICAL_CONSISTENCY_TEST_OF_ANALYTIC_IDENTITY`)
du cas d'une grandeur sans théorème de zéro exact, pour laquelle une
classification `NUMERICALLY_ZERO_COMPATIBLE` reste une classification de
précision finie et ne devient jamais `EXACT_ZERO`/`STRUCTURAL_ZERO`/`CERTIFIED_ZERO`
(`NUMERICALLY_ZERO_COMPATIBLE_IS_EXACT_ZERO = NO`). Un `ROBUST_ORACLE_FAIL`
sur `Delta1(delta=0)=0` ou `Delta2=0` signalerait une incohérence
numérique/de pipeline, jamais une falsification du théorème analytique.

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

Grille `eta` préenregistrée et domaine admissible (définitions normatives complètes : `temporal-event-solver.md` §27, `short-time-oracles.md` §9) :

```math
\lambda_\eta=2\sqrt\eta.
```

```text
LAMBDA_ETA_VALUES = {2^-2,2^-4,2^-6,2^-8,2^-10,2^-12,2^-14,2^-16}
ETA_VALUES         = {2^-6,2^-10,2^-14,2^-18,2^-22,2^-26,2^-30,2^-34}
ETA_GRID_TYPE       = ABSOLUTE_F_LEVELS
```

Ces niveaux sont des niveaux de réponse absolus communs. `ETA_ABSOLUTE_LEVELS_FOR_CEFF_THR = MANDATORY` ; `ETA_PEAK_NORMALIZED_PER_STATE = REJECTED` : ceci préserve la relation asymptotique déjà validée `T_thr ~ (eta/B)^(1/(2nu))` entre `C_eff^thr` et `C_short`. Aucune substitution post-hoc, interpolation vers un `eta` voisin ou ajout de niveau après inspection des résultats n'est autorisée.

Borne structurelle globale, avec `Var(n_i)<=1/4` et Cauchy-Schwarz :

```math
F_{pq}(t)\le Var(n_p)Var(n_q)\le\frac1{16}.
```

```text
THRESHOLD_GLOBAL_F_BOUND = STRUCTURAL_ANALYTIC
THRESHOLD_GLOBAL_F_MAX   = 1/16
```

Ceci raffine, sans le contredire, l'oracle générique déjà validé `0<=F<=1`.

Éligibilité de domaine, stricte et pré-pic (pas le maximum sur tout le premier lobe) :

```math
ETA\_PREPEAK\_RANGE\_ELIGIBLE \iff 0<\eta<F(T_{peak}).
```

La qualification montante de `T_thr` exige `s chi'(T_thr)>0` ; une dégénérescence exacte établie par oracle `STRUCTURAL_ANALYTIC` exclut tout `T_thr` qualifiant à ce niveau, et une positivité stricte non certifiable numériquement renvoie aux contrôles fail-closed de racine simple/dégénérée déjà validés.

Garde de précision relative profonde, réutilisant le budget d'incertitude déjà validé `e_u` en coordonnée d'événement `u_thr=Omega_safe T_thr/pi` (`s_thr=1`) :

```math
r_{thr,time}=\frac{e_u}{u_{thr}}\le\tau_{event},
\qquad
\tau_{event}=10^{-10}.
```

Aucune tolérance nouvelle n'est introduite.

Fermeture de dépendance commune : pour toute quantité ou verdict dérivé comparant, combinant ou testant en stabilité des temps de seuil, le domaine `eta` commun est l'intersection, sur la fermeture complète de dépendance, des niveaux préenregistrés numériquement admissibles pour chaque série de réponse élémentaire concernée. Aucune substitution post-hoc d'un niveau `eta` n'est autorisée. Chaque niveau publie ses diagnostics associés ; seul `e_u/u_thr` est la porte normative de précision, les autres rapports sont diagnostiques.

La plage dynamique potentielle complète (`2^14` en `lambda_eta`, soit `~6.96` en temps de seuil pour `nu=5`) est potentielle seulement ; l'admissibilité commune peut la réduire.

Règle opérationnelle de convergence court-terme (définition normative complète : `short-time-oracles.md` §10) : pour `D_pq^thr(eta)=log[C_eff,pq^thr(eta)/C_short,pq]`, la cible est `D_pq^thr -> 0` en coordonnée asymptotique `z=lambda_eta^(2/nu)`, pour `nu in {1,3,5}`. Le protocole sélectionne les trois plus petites valeurs `lambda` communes admissibles (`SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS=3`) et classe le résultat selon un motif de résolution information-monotone en deux statuts forts (`SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET = {SUPPORTED_RESOLVED_TREND, SUPPORTED_FLOOR_AFTER_CONTRACTION}`) ou en statuts non confirmatoires (absence de résidu résolu, portée commune insuffisante, exposant non résolu, non applicable, contrôle sensible). L'évaluation par paire `D_A^thr`/`D_B^thr` précède toute agrégation `Delta1` (`SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY=YES`) ; une revendication de stabilité au cutoff exige l'intersection conjointe des domaines admissibles `Lambda=2` et `Lambda=3` avant la sélection de la queue à trois niveaux. Aucune tolérance numérique scalaire nouvelle n'est introduite.

```text
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE = VALIDATED_FOR_FREEZE
```

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

Critère de contrôle sous raffinement : identité du premier événement stable, ordre des candidats pertinents stable, aucune cellule antérieure non résolue, temps continus compatibles selon les tolérances numériques désormais fermées (`ROOT_SOLVER_TOLERANCES`, `ARGMAX_TOLERANCES`, `SPECTRAL_PRECISION_CONTROL`, `DEGENERATE_ROOT_CONTROL`, toutes `VALIDATED_FOR_FREEZE` ; définition normative complète : `temporal-event-solver.md` §14, §20-27). Si cette stabilité échoue : `TIME_EVENT_CONTROL_SENSITIVE`.

Les tolérances numériques (solveur, argmax, précision spectrale) sont désormais fermées : voir `ROOT_SOLVER_TOLERANCES`, `ARGMAX_TOLERANCES`, `SPECTRAL_PRECISION_CONTROL` ci-dessus.

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

### Grille `EPS_PATH_VALUES` préenregistrée et certification continue

Définition normative complète : `path-purity-control.md`.

`R_path` est structurellement bornée :

```text
R_PATH_NORMALIZED_RANGE = STRUCTURAL_ANALYTIC
R_PATH_RANGE = [0,1]
```

Grille de contrôle préenregistrée :

```text
EPS_PATH_VALUES     = {1/32, 1/16, 1/8, 1/4}
EPS_PATH_STRICT      = 1/32
EPS_PATH_PERMISSIVE  = 1/4
```

Trichotomie de ligne de base, distincte du statut de dégradation : `DIRECT_DOMINANT_BASELINE` (`P_0=1`), `MIXED_BASELINE` (`0<P_0<1`), `NO_DIRECT_BASELINE` (`P_0=0`), `NO_ACTIVE_PATH_RESPONSE`. `PATH_CONTROL_STATUS` (`ROBUST_CLEAN`/`CONTROL_SENSITIVE`/`ROBUST_CONTAMINATED`) mesure uniquement la dégradation relative à cette ligne de base ; `ROBUST_CLEAN` seul ne signifie jamais une arrivée directe propre.

Le routage numérique de cette trichotomie exige désormais explicitement les
amplitudes `A_D`, `A_N` et `A_S` (normes, pas carrés d'amplitude ;
`PATH_BASELINE_ZERO_TEST_OBJECT = AMPLITUDE_NORMS_A_D_A_N_AND_A_S_NOT_SQUARED_AMPLITUDES`).
`DIRECT_DOMINANT_BASELINE`/`NO_DIRECT_BASELINE` exigent que le côté dominant
soit `ROBUST_NONZERO` ET que le côté opposé soit nul par certificat
`STRUCTURAL_ANALYTIC`/exact ; un côté seulement `NUMERICALLY_ZERO_COMPATIBLE`
est insuffisant et ne peut jamais produire `DIRECT_DOMINANT`/`NO_DIRECT` par
seule petitesse numérique
(`PATH_DIRECT_DOMINANCE_NUMERICAL_SMALLNESS_AS_EXACT_ZERO = REJECTED`).
Sinon : `PATH_CONTROL_NUMERICALLY_INCONCLUSIVE`. Définition normative
complète : `numerical-zero-symmetry-control.md` §F12, §H.

Une interprétation confirmatoire d'arrivée propre côté chemin exige :

```text
PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE =
DIRECT_DOMINANT_BASELINE AND ROBUST_CLEAN
```

La certification de l'extremum continu de `Purity_direct` est obligatoire (aucun minimum sur grille échantillonnée n'est admis). Elle repose sur la fonction exacte `H_path=Q_D P_S-P_D Q_S`, avec facteur de bracketing oscillatoire `s_path=4` (bracketing initial seulement, `BETA_VALUES` réutilisées). L'origine `t=0` est exclue de la certification générique par cellule (zéro structurel d'ordre élevé de `H_path`) et couverte par une fenêtre analytique de Taylor certifiée `(0,t_0]` avec `t_0=pi/(32 Omega_safe)` ; la certification par cellule ne s'applique que sur `[t_0,T]`. Un oracle `STRUCTURAL_ANALYTIC` établissant `H_path==0` identiquement dispense de toute certification de racine.

```text
PATH_EXTREMUM_CONTINUOUS_CERTIFICATION = REQUIRED
PATH_SAMPLED_SUPREMUM_AS_CERTIFICATE   = REJECTED
```

`d=3` reste exclu de toute interprétation d'arrivée, même en `DIRECT_DOMINANT_BASELINE` + `ROBUST_CLEAN` ; le profil complet reste publiable en `DIAGNOSTIC_ONLY`.

La même grille `EPS_PATH_VALUES` est utilisée à `Lambda=2` et `Lambda=3` ; `ROBUST_CLEAN` aux deux cutoffs ne prouve pas que `P_0` lui-même est stable au cutoff, ce qui est évalué par le contrôle dédié `TRUNCATION_COMPARISON_TOLERANCES` (`VALIDATED_FOR_FREEZE` ; définition normative complète : `truncation-comparison-control.md` §21).

```text
EPS_PATH_CONTROL_DOMAIN_AND_GRID = VALIDATED_FOR_FREEZE
```

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

Sous stationnarité `[rho_theta,H(theta)]=0` au point évalué (référence, état, `+delta`, `-delta`, chaque `h_k`, chaque cutoff), avec la propre `rho_theta` de ce point :

```text
RECURRENCE_AUTOCORRELATION_RANGE        = STRUCTURAL_ANALYTIC_UNDER_STATIONARITY
RECURRENCE_AUTOCORRELATION_RANGE_VALUES = [-1,1]
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
T_grow       -> tau >= T_peak (au minimum jusqu'à T_peak)
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

Les deux niveaux gardent des rôles distincts (`gamma_-` = sortie, `gamma_+` = retour) : `HYSTERETIC_PAIR_STRUCTURE = UNCHANGED`, `DETECTOR_THRESHOLD_COUNT = TWO_DISTINCT_LEVELS`. La chaîne préenregistrée à une seule coordonnée ci-dessous ne réduit pas le détecteur à un seuil unique ; elle paramétrise une famille finie de paires à deux seuils (définition complète : `recurrence-control.md` §3).

Chaîne anti-diagonale préenregistrée, `gamma(a)=(a,1-a)` avec `0<a<1/2` :

```text
GAMMA_A_VALUES = {1/8, 1/4, 3/8}
GAMMA_VALUES   = {(1/8,7/8), (1/4,3/4), (3/8,5/8)}
GAMMA_STRICT     = (1/8,7/8)
GAMMA_MID        = (1/4,3/4)
GAMMA_PERMISSIVE = (3/8,5/8)
GAMMA_HYSTERESIS_WIDTHS = {3/4, 1/2, 1/4}
```

Le centre fixe `gamma_-+gamma_+=1` (`GAMMA_CENTER=1/2`) est une restriction de design de contrôle, pas une symétrie physique, une probabilité ou un seuil physique de récurrence.

Verdict robuste par les deux bornes :

```text
gamma_perm ne détecte aucun retour
    -> RECURRENCE_STATUS = ROBUST_CLEAN

gamma_strict détecte un retour
    -> RECURRENCE_STATUS = ROBUST_CONTAMINATED

sinon
    -> RECURRENCE_STATUS = CONTROL_SENSITIVE
```

Ce verdict robuste ne dépend que de `gamma^strict` et `gamma^perm` (`GAMMA_CHAIN_ROBUST_VERDICT_DEPENDS_ONLY_ON_ENDPOINTS=YES`) ; la chaîne est verdict-équivalente à tout domaine ordonné plus grand ayant les mêmes extrema. La paire médiane est un diagnostic de sensibilité obligatoire à publier (`GAMMA_INTERIOR_POINTS_ROLE=SENSITIVITY_DIAGNOSTIC_ONLY`), pas une évidence confirmatoire indépendante.

Fenêtre de détection déclarée pour la paire permissive `(3/8,5/8)` : `GAMMA_EXIT_FLOOR=3/8`, `GAMMA_RETURN_FLOOR=5/8`, `GAMMA_MIN_DETECTED_SWING=1/4`. Restriction sémantique normative :

```text
ROBUST_CLEAN_SEMANTICS = NO_RECURRENCE_DETECTABLE_BY_PREREGISTERED_FAMILY
```

`ROBUST_CLEAN` ne signifie jamais l'absence de toute récurrence possible, seulement l'absence de récurrence détectable par la famille préenregistrée (insensibilité déclarée aux excursions restant au-dessus de `3/8` et aux récupérations n'atteignant jamais `5/8` : `recurrence-control.md` §8).

Le même domaine `Gamma` est utilisé pour `reference`, `+delta`, `-delta`, chaque `h_k`, `Lambda=2` et `Lambda=3` ; aucune substitution post-hoc (`GAMMA_POSTHOC_SUBSTITUTION=FORBIDDEN`).

Les bornes numériques de tolérance de croisement/contact/séparation temporelle sont désormais `VALIDATED_FOR_FREEZE` (`RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS`, définition normative complète : `recurrence-control.md` §11).

```text
GAMMA_CONTROL_DOMAIN_AND_GRID = VALIDATED_FOR_FREEZE
```

### Certification numérique fail-closed de la garde de récurrence

`RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS` est `VALIDATED_FOR_FREEZE`. Le protocole numérique complet (`recurrence-control.md` §11) repose sur :

- une porte de précision au petit dénominateur sur la normalisation `C_j=N_j/V_j` (`RECURRENCE_NORMALIZATION_GATE = RELATIVE_V_P2P_PLUS_RAW_SPECTRAL_MASS_CLOSURE`), fondée sur un rapport `p/2p` réellement relatif à `V_j` et sur la fermeture indépendante de la masse spectrale brute, sans normalisation `max(1,V_j)` ;
- des marges d'exclusion de cellule et d'unicité de racine spécifiques à `C_j`, fondées sur les écarts fonctionnels/dérivés `p/2p` et les bornes structurelles exactes `Omega_safe`/`Omega_safe^2` (`RECURRENCE_EMPTY_CELL_MARGIN`, `RECURRENCE_UNIQUENESS_MARGIN`), en remplacement de l'ancien test sans marge ;
- aucune nouvelle tolérance scalaire (`RECURRENCE_HYSTERESIS_NEW_SCALAR_TOLERANCE = NONE`) : réutilisation exacte de `BETA_VALUES`, `tau_root=1e-12`, `tau_event=1e-10`, `SIMPLE_ROOT_CONTROL`, `DEGENERATE_ROOT_CONTROL`, `SPECTRAL_PRECISION_CONTROL` ;
- `CERTIFIED_RETURN` fondé sur témoin existentiel (`RECURRENCE_CERTIFIED_RETURN_MODE = WITNESS_BASED_EXISTENTIAL`), sans énumération exhaustive de racines ;
- `CERTIFIED_NO_RETURN` fondé sur complétude continue (`RECURRENCE_CERTIFIED_NO_RETURN_MODE = CONTINUOUS_COMPLETENESS_BASED`), via `NO_EXIT_BEFORE_EVENT` certifié ou `EXIT_NO_RETURN_BEFORE_EVENT` certifié ; toute ambiguïté reste `RECURRENCE_HORIZON_UNRESOLVED` ou `RECURRENCE_FIXED_HORIZON_NUMERICALLY_INCONCLUSIVE`, jamais promue silencieusement ;
- une règle d'incertitude d'horizon fixe/incertain (`RECURRENCE_HORIZON_UNCERTAINTY_RULE = EARLIEST_HORIZON_FOR_RETURN_LATEST_HORIZON_FOR_NO_RETURN`) ; `RECURRENCE_TGROW_PRIMARY_HORIZON = T_peak` instancie opérationnellement, pour la campagne primaire préenregistrée, l'énoncé scientifique déjà validé « au moins jusqu'à `T_peak` » (§6), sans le redéfinir ; `RECURRENCE_TTHR_PRIMARY_HORIZON = T_down(eta)` est inchangé ;
- une agrégation par site fail-closed et un verdict robuste `Gamma` évalué aux deux bornes, avec contrôle croisé de la monotonie exacte déjà démontrée (§4) : toute contradiction donne `RECURRENCE_GAMMA_MONOTONICITY_VIOLATION` et `RECURRENCE_STATUS = NUMERICALLY_INCONCLUSIVE`, sans arbitrage par sélection d'un seul calcul ;
- la variance locale nulle reste non confirmatoire (`RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE`), sans identification silencieuse à `CERTIFIED_NO_RETURN` ; ceci reste conditionné à la politique désormais fermée `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE` (définition normative complète : `numerical-zero-symmetry-control.md`) ;
- `RECURRENCE_CONTROL_ACCEPTABLE` n'est établi que pour `RECURRENCE_STATUS = ROBUST_CLEAN` avec dépendances confirmatoires.

```text
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = VALIDATED_FOR_FREEZE
```

### Condition d'interprétation

Un événement temporel est interprétable comme arrivée propre seulement si :

```text
PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE
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

Ces deux estimateurs ne sont pas forcés à être égaux en magnitude (`ESTIMATOR_MAGNITUDE_EQUALITY_GATE = REJECTED`). L'objet générique de cohérence n'est pas leur égalité numérique mais la robustesse de l'ordre relationnel primaire encodé par `Delta1` (`ESTIMATOR_COHERENCE_OBJECT = DELTA1_RELATIONAL_ORDERING`) sur la famille complète des estimateurs de seuil `eta` requis, avec éligibilité scientifique locale évaluée en premier ; une asymétrie d'éligibilité entre familles d'estimateurs est une limitation de couverture non confirmatoire, pas un contre-exemple d'ordre résolu, tandis qu'un ordre opposé résolu entre estimateurs éligibles reste sensible au contrôle. Toute revendication finale d'ordre non nul reste conditionnée au routage zéro/non-zéro de `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE`, qui fournit désormais cette dépendance finale (`ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL = SATISFIED_BY_THIS_CONTROL`). Définition normative complète : `ESTIMATOR_COHERENCE_CRITERION = VALIDATED_FOR_FREEZE`, `estimator-coherence-control.md` ; `numerical-zero-symmetry-control.md`.

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

### Deux rangs explicites de revendication `Delta1`

Définition normative complète : `final-acceptance-rules.md` §4.

```text
DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY = CLAIM_RANK_PRIMARY
DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY = CLAIM_RANK_STRONGER_OPTIONAL
```

Le rang PRIMAIRE (`DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY`) est un contraste
relationnel confirmatoire non nul entre observables de temps de réponse de
Kubo résolus ; il n'est PAS, en soi, une revendication d'arrivée propre, de
propagation, de vitesse ou de front causal. Le rang plus fort optionnel
(`DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY`) exige en plus `TIME_EVENT_VALID
= PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE AND RECURRENCE_CONTROL_ACCEPTABLE` pour
chaque dépendance d'événement requise de l'estimateur. Les deux rangs ne
sont jamais fusionnés ; le vocabulaire d'arrivée/propagation est interdit
pour le rang relationnel seul
(`DELTA1_RELATIONAL_CONTRAST_ARRIVAL_LANGUAGE = FORBIDDEN`).

---

## 14. Campagne principale

Campagne nominale :

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

Cette campagne mesure `Delta1` à brisure finie, souvent non linéaire. Elle ne doit pas servir à estimer `Xi1`.

```text
XI1_CONFIRMATORY_SCOPE = SOFT_LOOP_ONLY
```

Définition normative complète : `final-acceptance-rules.md` §10,
`derivative-control.md` §3-4. Aucune campagne `Xi1` MAIN n'est créée par ce
document.

Contrôles séparés :

```text
g=0, mu=0    -> pure-hopping oracle
g=0.10       -> stress faible-g hors nominal
delta=0.9    -> qualification / stress hors nominal
```

La covariance `delta<->-delta` doit être exercée sur un sous-ensemble négatif préenregistré. Ce sous-ensemble est `VALIDATED_FOR_FREEZE` (`NEGATIVE_DELTA_ORACLE_SUBSET`, définition normative complète : `parameter-campaign-structure.md` §11) : il combine une base géométrique fixe de 17 points (`NEGATIVE_DELTA_ORACLE_BASE_SIZE=17`) avec une extension déterministe de couverture de branches sélectionnée UNIQUEMENT depuis les statuts catégoriels d'exécution `+delta` déjà requis, avant toute exécution `-delta` (`NEGATIVE_DELTA_ORACLE_BRANCH_EXTENSION_SOURCE=POSITIVE_MAIN_STATUSES_ONLY`, `NEGATIVE_DELTA_RESULTS_AFFECT_SUBSET_SELECTION=FORBIDDEN`), pour une taille totale dérivée bornée entre 17 et 120 points (`NEGATIVE_DELTA_ORACLE_TOTAL_SIZE=DERIVED_BOUNDED_17_TO_120`). Chaque point `-delta` requis DOIT être recalculé indépendamment par le pipeline générique (`NEGATIVE_DELTA_ORACLE_INDEPENDENT_RECOMPUTATION=REQUIRED`) : toute construction sign-dérivée depuis le côté `+delta` (par exemple `H_minus:=R H_plus R^dagger` ou `Delta_1(-d):=-Delta_1(+d)`) rend le point `DELTA_COVARIANCE_ORACLE_POINT=INVALID_BY_CONSTRUCTION` et fait échouer l'oracle (`NEGATIVE_DELTA_ORACLE_CONTROL=FAIL`), jamais `NOT_APPLICABLE`. La comparaison utilise une fermeture de dépendance mappée complète (`NEGATIVE_DELTA_ORACLE_COMPARISON_LEVEL=FULL_MAPPED_DEPENDENCY_CLOSURE`), séparée en une couche discrète catégorielle sans nouvelle tolérance et une couche continue dont les seuils sont désormais fournis par `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE` (`NEGATIVE_DELTA_ORACLE_CONTINUOUS_TOLERANCE_SOURCE = NUMERICAL_ZERO_AND_SYMMETRY_CONTROL` ; définition normative complète : `numerical-zero-symmetry-control.md`). Les points négatifs ne fournissent aucune évidence physique indépendante (`NEGATIVE_DELTA_ORACLE_POINT_ROLE=NUMERICAL_CONTROL/IMPLEMENTATION_ORACLE`) et ne servent à régler aucun autre paramètre. Le cutoff primaire est `Lambda=2` ; `Lambda=3` utilise l'intersection avec les points de stress de troncature ou, si elle est vide, l'ancre de repli fixe `(1,0,+/-2/5)` (`NEGATIVE_DELTA_ORACLE_LAMBDA3_RULE=TRUNCATION_INTERSECTION_OR_FIXED_ANCHOR_FALLBACK`). Cet oracle porte exclusivement sur MAIN à `delta` fini (`NEGATIVE_DELTA_ORACLE_SUBSET_SCOPE=MAIN_FINITE_DELTA_ONLY`) et ne s'applique ni à SOFT-LOOP (déjà couvert par ses deux signes explicites) ni aux points de stress `g=0.10`/`|delta|=0.9` (`NEGATIVE_DELTA_ORACLE_EXCLUDED_STRESS_POINTS`).

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

Le sous-ensemble exact des points de stress `Lambda=3` est désormais préenregistré et fixe (`TRUNCATION_STRESS_POINT_SUBSET = VALIDATED_FOR_FREEZE`, définition normative complète : `truncation-design-qualification.md` §8, résumé opérationnel : `parameter-campaign-structure.md` §5). Il comprend 18 points fixes (`TRUNCATION_STRESS_POINT_SUBSET_SIZE=18` ; `TRUNCATION_STRESS_MAIN_POINT_COUNT=16` ; `TRUNCATION_STRESS_OUTER_POINT_COUNT=2` ; `TRUNCATION_STRESS_POINT_DESIGN=THREE_AXIS_STRESS_CROSS_PLUS_CONDITIONING_INTERIOR_AND_OUTER_ANCHORS`), plus une ancre de référence obligatoire `Lambda=3` distincte et non comptée dans ce total (`TRUNCATION_REFERENCE_ANCHOR=(1,0,0)`, `TRUNCATION_REFERENCE_ANCHOR_ROLE=MANDATORY_REFERENCE_NOT_STRESS`). Chaque point sélectionné est comparé sur la fermeture de dépendance scientifique complète requise (`TRUNCATION_STRESS_OBSERVABLE_SCOPE=FULL_REQUIRED_SCIENTIFIC_DEPENDENCY_CLOSURE`), avec la fermeture `eta` commune déjà gelée aux deux cutoffs, sans rétrécissement différencié (`TRUNCATION_THRESHOLD_DOMAIN_RULE=EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE`). Le sous-ensemble porte exclusivement sur `delta` non négatif ; `delta` négatif n'apporte aucune évidence de troncature physique indépendante et reste un oracle d'implémentation de signe déjà couvert par `NEGATIVE_DELTA_ORACLE_SUBSET` (`TRUNCATION_NEGATIVE_DELTA_ROLE=IMPLEMENTATION_ORACLE_ONLY`). Aucune extension adaptative n'est autorisée après inspection des résultats `Lambda=3` (`TRUNCATION_STRESS_ADAPTIVE_EXTENSION=REJECTED_FOR_PRIMARY_PREREGISTERED_SUBSET`, `TRUNCATION_STRESS_POSTHOC_SUBSTITUTION=FORBIDDEN`). Un contrôle réussi sur ce sous-ensemble clairsemé ne supporte qu'une absence d'instabilité de cutoff détectée sur ce sous-ensemble préenregistré, jamais une convergence uniforme sur tout le domaine MAIN (`TRUNCATION_STRESS_CLAIM_SCOPE=PREREGISTERED_STRESS_SUPPORT_NOT_UNIFORM_THEOREM`) ; tout point MAIN non sélectionné reste non certifié par ce protocole (`TRUNCATION_CUTOFF_STATUS_FOR_UNSAMPLED_MAIN_POINT=NOT_CERTIFIED_BY_STRESS_SUBSET`). COMMENT ces deux cutoffs sont comparés sur ce sous-ensemble est également fixé (`TRUNCATION_COMPARISON_TOLERANCES = VALIDATED_FOR_FREEZE`, définition normative complète : `truncation-comparison-control.md`) : famille opérationnelle de sensibilité `TRUNCATION_TOLERANCE_VALUES={0.01,0.02,0.05}` dimensionnée par la qualification de design préalable (`TRUNCATION_TOLERANCE_DIMENSIONING=DESIGN_QUALIFICATION_INFORMED_PREREGISTRATION`) ; distance de trace pour la métrique d'état (`TRUNCATION_STATE_METRIC=TRACE_DISTANCE_UNDER_NATURAL_EMBEDDING`) ; métriques log-ratio pour les quantités positives ; garde double absolue + relative-symétrique obligatoire pour `Delta1` fini (`TRUNCATION_DELTA1_DUAL_METRIC=REQUIRED_FOR_FINITE_DELTA_PRIMARY_SIGNAL`), `Delta1` structurel à `delta=0` restant `NOT_APPLICABLE_STRUCTURAL_ZERO` et conditionné à `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE` (définition normative complète : `numerical-zero-symmetry-control.md`) ; comparaison d'admissibilité `eta` AVANT intersection commune (`TRUNCATION_ETA_ADMISSIBILITY_COMPARISON_STAGE=BEFORE_COMMON_INTERSECTION`) ; porte de référence robuste-stable obligatoire (`TRUNCATION_REFERENCE_GATE=ROBUST_STABLE_REQUIRED`) ; agrégation ponctuelle fail-closed sans moyennage, MAIN séparé de l'extérieur (`TRUNCATION_MAIN_AGGREGATION=POINTWISE_FAIL_CLOSED_NO_AVERAGING`). `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` est fermé séparément (`VALIDATED_FOR_FREEZE`, définition normative complète : `numerical-zero-symmetry-control.md`), pas par ce contrôle lui-même.

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
reste provisoire pour l'interprétation confirmatoire finale de campagne, sous
la politique désormais fermée `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES =
VALIDATED_FOR_FREEZE` (définition normative complète :
`numerical-zero-symmetry-control.md`), jusqu'à son application effective en
exécution confirmatoire. Les formules complètes, les intervalles numériques
et l'ordre de classification sont définis intégralement dans
`soft-loop-static-gate.md`.

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

`ETA_GRID_AND_ADMISSIBLE_DOMAIN` est `VALIDATED_FOR_FREEZE` ; la grille absolue, la borne structurelle `1/16`, l'éligibilité pré-pic et la garde de précision relative sont définies dans `temporal-event-solver.md` §27 et `short-time-oracles.md` §9.

`SHORT_TIME_THRESHOLD_CONVERGENCE_RULE` est également `VALIDATED_FOR_FREEZE` ; le protocole opérationnel complet (cible `D_pq^thr -> 0`, coordonnée `z=lambda_eta^(2/nu)`, portée `nu in {1,3,5}`, queue commune à trois niveaux minimum, branchement information-monotone, statuts forts `SUPPORTED_RESOLVED_TREND`/`SUPPORTED_FLOOR_AFTER_CONTRACTION`, traitement par paire avant `Delta1`, queue conjointe de stabilité au cutoff) est défini dans `short-time-oracles.md` §10.

`EPS_PATH_CONTROL_DOMAIN_AND_GRID` est également `VALIDATED_FOR_FREEZE` ; la grille `EPS_PATH_VALUES={1/32,1/16,1/8,1/4}`, la trichotomie de ligne de base, la certification continue de l'extremum `H_path` (fenêtre analytique d'origine, raccourci structurel exact) et la classification epsilon sont définies dans `path-purity-control.md` et `event-bandwidth-bracketing.md` §8.

`GAMMA_CONTROL_DOMAIN_AND_GRID` est également `VALIDATED_FOR_FREEZE` ; la borne structurelle d'autocorrélation sous stationnarité, la chaîne anti-diagonale préenregistrée `GAMMA_VALUES={(1/8,7/8),(1/4,3/4),(3/8,5/8)}`, le verdict robuste à deux bornes et la fenêtre de détection déclarée sont définis dans `recurrence-control.md`.

`RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS` est également `VALIDATED_FOR_FREEZE` ; la porte de précision au petit dénominateur sur la normalisation `C_j`, les marges d'exclusion de cellule et d'unicité `p/2p` spécifiques à la récurrence, le mode témoin de `CERTIFIED_RETURN`, le mode complétude de `CERTIFIED_NO_RETURN`, la règle d'incertitude d'horizon, l'instanciation opérationnelle `RECURRENCE_TGROW_PRIMARY_HORIZON=T_peak` et le contrôle croisé de monotonie `Gamma` sont définis dans `recurrence-control.md` §11. Aucune nouvelle tolérance scalaire n'est introduite (`RECURRENCE_HYSTERESIS_NEW_SCALAR_TOLERANCE=NONE`).

### Campagne / troncature

`NEGATIVE_DELTA_ORACLE_SUBSET` est également `VALIDATED_FOR_FREEZE` ; la base géométrique fixe à 17 points, l'extension déterministe de couverture de branches fondée uniquement sur les statuts catégoriels `+delta`, la taille totale dérivée bornée `17..120`, le recalcul indépendant obligatoire du côté `-delta`, la fermeture de dépendance mappée complète à deux couches (discrète/continue) et la règle de cutoff `Lambda=2`/`Lambda=3` sont définis dans `parameter-campaign-structure.md` §11. Aucune nouvelle tolérance scalaire n'est introduite (`NEGATIVE_DELTA_ORACLE_NEW_SCALAR_TOLERANCE=NONE`). `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` est fermé séparément (`VALIDATED_FOR_FREEZE`, définition normative complète : `numerical-zero-symmetry-control.md`), pas par ce contrôle lui-même.

`TRUNCATION_STRESS_POINT_SUBSET` est `VALIDATED_FOR_FREEZE` ; le sous-ensemble fixe de 18 points de stress préenregistrés (16 points MAIN + 2 points de stress extérieurs déjà divulgués), l'ancre de référence obligatoire non comptée `(1,0,0)`, l'ancre de conditionnement `(1,-1,0)`, la fermeture de dépendance scientifique complète requise, la règle `eta` commune déjà existante, l'absence d'extension adaptative et la portée de revendication restreinte au soutien préenregistré sont définis dans `truncation-design-qualification.md` §8 et résumés dans `parameter-campaign-structure.md` §5. Aucune nouvelle tolérance scalaire n'est introduite (`TRUNCATION_STRESS_NEW_SCALAR_TOLERANCE=NONE`).

`TRUNCATION_COMPARISON_TOLERANCES` est `VALIDATED_FOR_FREEZE` ; la famille opérationnelle préenregistrée `TRUNCATION_TOLERANCE_VALUES={0.01,0.02,0.05}` (dimensionnée par la qualification de design préalable), la marge numérique générique `p/2p` + budget propagé, la couche catégorielle, la métrique d'état par distance de trace, les métriques log-ratio positives, la garde double absolue + relative-symétrique obligatoire pour `Delta1` fini, l'exclusion `NOT_APPLICABLE_STRUCTURAL_ZERO` de `Delta1` à `delta=0`, la comparaison d'admissibilité `eta` avant intersection commune, la porte de référence robuste-stable obligatoire et l'agrégation ponctuelle fail-closed sans moyennage (MAIN séparé de l'extérieur) sont définies dans `truncation-comparison-control.md`. Aucune nouvelle tolérance de virgule flottante n'est introduite (`TRUNCATION_NEW_FLOATING_POINT_TOLERANCE=NONE`). `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` est fermé séparément (`VALIDATED_FOR_FREEZE`, définition normative complète : `numerical-zero-symmetry-control.md`), pas par ce contrôle lui-même.

`ESTIMATOR_COHERENCE_CRITERION` est `VALIDATED_FOR_FREEZE` ; la portée `MAIN_FINITE_DELTA_PRIMARY_SIGNAL`, l'objet de cohérence par ordre relationnel `Delta1` (`ESTIMATOR_COHERENCE_OBJECT=DELTA1_RELATIONAL_ORDERING`), le rejet de la porte d'égalité de magnitude (`ESTIMATOR_MAGNITUDE_EQUALITY_GATE=REJECTED`), la famille complète de seuils `eta` sans sélection a posteriori (`ESTIMATOR_COHERENCE_THRESHOLD_DOMAIN=EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE`, `ESTIMATOR_COHERENCE_POSTHOC_ETA_SELECTION=FORBIDDEN`), l'éligibilité scientifique locale évaluée en premier, la correction de blocage distinguant l'asymétrie d'éligibilité (limitation de couverture non confirmatoire) d'un contre-exemple d'ordre résolu (`ESTIMATOR_ELIGIBILITY_CONFLICT_AS_ORDERING_COUNTEREXAMPLE=REJECTED`), les diagnostics obligatoires de cardinalité effective (`ESTIMATOR_COHERENCE_CARDINALITY_DIAGNOSTICS=MANDATORY_PUBLICATION`), l'agrégation MAIN ponctuelle sans moyennage où seul un ordre en conflit résolu domine (`ESTIMATOR_COHERENCE_MAIN_AGGREGATION=POINTWISE_NO_AVERAGING_ORDERING_CONFLICT_ONLY_DOMINATES_AS_PROTOCOL_DEPENDENCE`), et la conditionnalité de toute revendication finale d'ordre non nul au contrôle zéro/symétrie (`ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL=YES`) sont définies dans `estimator-coherence-control.md`. L'oracle exact de rééchelonnement temporel reste un contrôle d'implémentation obligatoire dont la paramétrisation numérique est différée au contrôle zéro/symétrie (`ESTIMATOR_RESCALING_ORACLE_ROLE=MANDATORY_IMPLEMENTATION_CONTROL`, `ESTIMATOR_RESCALING_ORACLE_PARAMETERIZATION=DEFERRED_TO_NUMERICAL_ZERO_AND_SYMMETRY_CONTROL`). Aucune nouvelle tolérance scalaire n'est introduite (`ESTIMATOR_COHERENCE_NEW_SCALAR_TOLERANCE=NONE`). `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` est fermé séparément (`VALIDATED_FOR_FREEZE`, définition normative complète : `numerical-zero-symmetry-control.md`), pas par ce contrôle lui-même.

### Verdicts

```text
(aucun paramètre numérique majeur préenregistré encore OPEN)
```

`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` est désormais `VALIDATED_FOR_FREEZE`
(définition normative complète : `numerical-zero-symmetry-control.md`),
dernier des vingt-et-un paramètres numériques majeurs préenregistrés de
0B (`OPEN_MAJOR_CONTROLS=0`).

Le seul `OPEN` spécialisé actuel intentionnel restant est le backlog de
support spectral groupé :

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
```

hors de ce décompte des contrôles numériques majeurs et ne bloquant pas la
préparation au gel (définition normative complète :
`final-acceptance-rules.md` §11).

Ne sont notamment plus ouverts : orientation source-récepteur, grille MAIN
`(g,mu,delta)`, choix interpolation vs solveur, différences finies temporelles,
seuil `NEAR_CROSSING`, traitement du canal `m=0`, facteur de bande global
des événements, `ROOT_SOLVER_TOLERANCES`, `SPECTRAL_PRECISION_CONTROL`,
`SIMPLE_ROOT_CONTROL`, `DELTA1_PROPAGATED_ERROR_BUDGET`, `A_DELTA_VALUES`,
`DERIVATIVE_STABILITY_CRITERION`, `RICHARDSON_USAGE_RULE`,
`ARGMAX_TOLERANCES`, `DEGENERATE_ROOT_CONTROL`,
`STATIC_COLLAPSE_NUMERICAL_CRITERION`, `ETA_GRID_AND_ADMISSIBLE_DOMAIN`,
`SHORT_TIME_THRESHOLD_CONVERGENCE_RULE`, `EPS_PATH_CONTROL_DOMAIN_AND_GRID`,
`GAMMA_CONTROL_DOMAIN_AND_GRID`, `RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS`,
`NEGATIVE_DELTA_ORACLE_SUBSET`, `TRUNCATION_STRESS_POINT_SUBSET`,
`TRUNCATION_COMPARISON_TOLERANCES`, `ESTIMATOR_COHERENCE_CRITERION` et
`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES`.

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
