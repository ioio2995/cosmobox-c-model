# Toy Model 0B — plan de validation consolidé

Statut : **revue de clôture pré-gel**
Spécification scientifique : `docs/toy-models/toy0b/specification.md`
Contrôles numériques : `docs/toy-models/toy0b/temporal-event-solver.md` (sections 15-24)

Ce document décrit le protocole de validation de 0B sous une forme compacte. Les preuves détaillées restent dans les supports analytiques du dossier `toy0b/`. Les tolérances numériques spectrales et la règle de précision sont fixées dans le document normatif `temporal-event-solver.md`.

Aucune exécution confirmatoire 0B ni implémentation n'est autorisée tant que les paramètres marqués `OPEN` ne sont pas fermés et que le lot n'est pas explicitement autorisé dans `docs/governance/current-task.md`.

---

## 1. Régimes et catégories

```text
REFERENCE_REGIME
    N=6
    Lambda=2

TRUNCATION_CHECK
    N=6
    Lambda=3

PILOT_REGRESSION
    N=6
    Lambda=1
```

Catégories de résultats :

```text
STRUCTURAL_ANALYTIC
PILOT_LAMBDA1
QUALIFICATION_NONCONFIRMATORY
PREREGISTERED_REFERENCE
TRUNCATION_CONTROL
EXTENDED_DIAGNOSTIC
```

Aucun résultat pilote ou de qualification déjà vu ne peut devenir confirmatoire par changement d'étiquette.

---

## 2. Oracles structurels obligatoires

Le code futur devra vérifier comme non-régressions analytiques :

### A01 — comptage physique

```text
spread=0 -> 1 configuration
spread=1 -> 16 configurations
spread=2 -> 3 configurations
```

```math
\dim\mathcal H_{phys}(\Lambda)=40\Lambda-2
\qquad(\Lambda\ge1).
```

```text
Lambda=1 -> 38
Lambda=2 -> 78
Lambda=3 -> 118
```

Hors de ce domaine, seul le comptage exact par `spread` fait foi (cf. A02).

### A02 — intérieur

L'identité structurelle exacte est :

```math
\dim\mathcal H_{interior}(\Lambda)
=\sum_n\max\bigl(0,2(\Lambda-1)+1-spread(n)\bigr).
```

Elle équivaut à :

```math
\dim\mathcal H_{interior}(\Lambda)
=\dim\mathcal H_{phys}(\Lambda-1)
```

à condition que `H_phys(0)` soit défini par ce même comptage exact, ce qui donne :

```text
Lambda=0 -> dim H_phys = 1
```

La forme fermée `dim H_phys(Lambda)=40*Lambda-2` n'est valide que pour `Lambda>=1` et ne doit donc **pas** être substituée à `Lambda-1` lorsque `Lambda=1`.

Valeurs de régression :

```text
Lambda=1 -> dim H_interior = 1
Lambda=2 -> dim H_interior = 38
Lambda=3 -> dim H_interior = 78
```

### A03 — shifts cycliques

Pour `j=2Lambda-k` :

```math
r_\Lambda(L^k)
=\sum_n\max(0,j+1-spread(n)).
```

Table attendue :

| `j` | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| rang | 1 | 18 | 38 | 58 | 78 | 98 |

### A04 — Gauss tangent

```math
D_{n_i}=D_{E_i}-D_{E_{i-1}}.
```

```text
S_n subset S_E
dim S_n <= 5
dim S_E <= 6
```

### A05 — flux uniforme

```math
\Phi=(1/6)\sum_iE_i,
\qquad
[\Phi,L]=L.
```

### A06 — orthogonalité cyclique sur `delta=0`

```math
D_\Phi\perp S_n
```

pour tout `(g,mu,0)` sous prescription canonique. Si `D_Phi` est actif :

```math
S_E=S_n\oplus_\perp span\{D_\Phi\}.
```

Aucun oracle `dim S_E=6` global n'est autorisé.

### A07 — symétries et covariance

Vérifier les actions déclarées de `T`, `C`, `S`, `R`, `Q`, `K` et notamment :

```math
R H(g,\mu,\delta)R^\dagger=H(g,\mu,-\delta),
```

```math
[Q,H(g,\mu,\delta)]=0,
```

```math
Qn_pQ^\dagger=1-n_{1-p}.
```

### A08 — parité temporelle et réciprocité

```math
\chi_{pq}(-t)=-\chi_{pq}(t),
```

```math
\chi_{pq}(t)=\chi_{qp}(t).
```

L'ancien besoin d'une convention ordonnée source-récepteur est donc clos.

### A09 — oracles `Delta`

```math
\Delta_1(g,\mu,0)=0,
```

```math
\Delta_1(g,\mu,-\delta)=-\Delta_1(g,\mu,+\delta),
```

```math
\Delta_2(g,\mu,\delta)=0.
```

### A10 — canal de multigrade nul

Dans le secteur physique :

```math
n_i=b_i+E_i-E_{i-1}.
```

Donc :

```math
[n_p,\Pi_0(O)]=0
```

et :

```text
ZERO_GRADE_KUBO_CHANNEL      = INACTIVE_EXACT
ZERO_GRADE_NON_TARGET_WEIGHT = ZERO_EXACT
```

Le code ne doit jamais compter deux fois le canal auto-conjugué `m=0`.

---

## 3. Régressions historiques `Lambda=1`

Résultats déjà connus :

```text
rank(F_D)        = 6
rank(F_edge)     = 18
rank(F_path)     = 36
rank(F_loop^(1)) = 38
rank(L)          = 18
```

Toute reproduction porte :

```text
RESULT_CLASS = PILOT_LAMBDA1
```

---

## 4. Qualification déjà divulguée

Les données déjà observées à `Lambda=2/3`, notamment énergie de fond, gaps, activité de `D_Phi`, poids de saturation au bord, structure SOFT-LOOP et pente vers `|mu|^-5`, sont classées :

```text
QUALIFICATION_NONCONFIRMATORY
```

Elles peuvent guider le design préenregistré, mais ne peuvent être revendiquées comme découvertes confirmatoires ultérieures.

Le diagnostic :

```math
B_2=P(\max_i|E_i|=2)
```

mesure la pression au bord, pas l'erreur de troncature.

Le résidu de Ritz de l'état `Lambda=2` plongé dans `Lambda=3` est privilégié comme diagnostic de design du couplage aux états omis lorsque nécessaire.

---

## 5. État fondamental et Gate 0

À chaque point de campagne publier :

```text
d_GS
gap_GS
```

Aucun seuil `NEAR_CROSSING` ne rejette un point scientifique.

Pour chaque générateur `A` :

```math
D_A=-i[A,\rho].
```

Si :

```math
[A,P_{GS}]=0,
```

alors :

```text
GENERATOR_ACTIVITY = INACTIVE
```

et non `PASS`.

Publier au minimum :

```text
generator
commutator_norm
d_GS
activity_status
```

---

## 6. Identifiabilité statique et dynamique

`M_F` est la carte de mesure définie dans la spécification §6 : elle agit sur l'espace tangent `V={A=A^dagger, Tr A=0}` et utilise les représentants traceless des observables de `F`. Tout rang publié ici est un rang de `M_F`, jamais un comptage d'opérateurs listés.

Pour chaque sous-espace de réponse pré-déclaré `S_resp` et famille de mesure `F`, construire la restriction :

```math
M_{F|S}.
```

Publier :

```text
dim S_resp
rank(M_F|S)
dim restricted kernel
restricted singular spectrum
restricted conditioning
restricted kernel projector
```

Verdict statique :

```text
STATIC = PASS
    si S_resp intersect ker(M_F) = {0}

STATIC = FAIL
    sinon
```

`STATIC PASS => DYNAMIC PASS` exactement.

En cas de `STATIC FAIL` seulement, construire :

```math
\mathcal L_H(O)=i[H,O],
```

```math
W(F,H)=span\{F,\mathcal L_HF,\mathcal L_H^2F,\ldots\}
```

jusqu'à stabilisation.

Verdict dynamique :

```text
DYNAMIC = PASS
    si S_resp intersect W(F,H)^perp = {0}

DYNAMIC = FAIL
    sinon
```

Un `DYNAMIC PASS` autorise l'étude temporelle ; il ne valide pas les temps caractéristiques ni `C_eff`.

Les rangs doivent être recalculés à chaque point où ils interviennent ; aucun `rank S_n=5` ou `dim S_E=6` n'est transporté depuis la référence.

---

## 7. Représentation de Kubo et contrôle spectral

Pour chaque fond :

```math
\chi_{pq}(t)
=iTr[\rho[n_p,n_q(t)]].
```

```math
F_{pq}(t)=\chi_{pq}(t)^2/4.
```

Oracles :

```text
F_pq(0)=0 pour p!=q
0 <= F_pq(t) <= 1
```

Dans la base `K`-réelle :

```math
\chi_{pq}(t)=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
```

Les poids sont groupés par projecteur spectral, jamais par simple décompte des vecteurs propres individuels dans un multiplet dégénéré.

Le code futur doit comparer, sur des points-oracles, deux chemins indépendants pour les premiers moments :

```text
MOMENT_OPERATOR_PATH
MOMENT_SPECTRAL_PATH
```

avec la convention de signe normative.

Interdits comme estimateurs nominaux :

```text
finite-difference time derivatives
interpolation-based final event times
numerical quadrature of P_alpha
```

---

## 8. Court temps

Convention :

```math
ad_H(O)=[H,O],
\qquad
\mathcal L_H(O)=i[H,O].
```

Moments purs :

```math
M_r^{pq}
=-2\langle\Omega|n_p(H-E_0)^rn_q|\Omega\rangle.
```

La version canonique utilise `P_GS/d_GS` et traite explicitement le shell `omega=0`.

Détermination de `nu` :

```text
M1 != 0                  -> nu=1
M1 = 0                   -> nu>=3
M1=0 and M3 != 0         -> nu=3
M1=M3=0 and M5 != 0      -> nu=5
...
```

Les zéros exacts doivent être rattachés aux règles structurelles déjà démontrées : localité, `K_SECTOR_ODDNESS`, parité bipartite et règles pair/impair de distance. Un zéro seulement flottant reste soumis au contrôle numérique préenregistré.

Pour une arête `{p,q}={i,i+1}` :

```math
M_1^{pq}=J\langle X_i\rangle.
```

Pour `d>=2` :

```math
M_1^{pq}=0.
```

Si référence et état ont le même `nu` :

```math
C_{short}=|a_{state}/a_{ref}|^{1/\nu}.
```

Sinon :

```text
SHORT_TIME_COMPARISON = NOT_APPLICABLE
D_thr                 = NOT_DEFINED
```

Pour une arête régulière, vérifier aussi :

```math
\Delta_1^{short}
=\log|\langle X\rangle_A/\langle X\rangle_B|.
```

---

## 9. Événements temporels

Les définitions scientifiques restent celles de `F=chi^2/4`, mais les fonctions numériques résolues sont réduites analytiquement.

### `T_peak`

Chercher la première racine qualifiante :

```math
\chi'(t)=0.
```

Elle doit correspondre au premier maximum de `F`. Pour un candidat non dégénéré :

```math
\chi\chi''<0.
```

Une racine dégénérée est traitée par la définition de changement de caractère, pas rejetée arbitrairement.

### `T_thr(eta)` et `T_down(eta)`

Sur le premier lobe, avec signe `s` de `chi`, résoudre :

```math
\chi(t)-s\,2\sqrt\eta=0.
```

`T_thr` est le premier croisement montant avant `T_peak`; `T_down` le premier croisement descendant suivant dans le même lobe.

### Grille eta et admissibilité pré-pic des seuils

Grille absolue préenregistrée, paramétrée par `lambda_eta=2 sqrt(eta)` :

```text
LAMBDA_ETA_VALUES = {2^-2,2^-4,2^-6,2^-8,2^-10,2^-12,2^-14,2^-16}
ETA_VALUES         = {2^-6,2^-10,2^-14,2^-18,2^-22,2^-26,2^-30,2^-34}
ETA_GRID_TYPE       = ABSOLUTE_F_LEVELS
```

Ces niveaux sont des niveaux de réponse absolus communs. Interdit : `eta`
choisi comme fraction de `F_peak` par état, rééchelonnement par cutoff,
rééchelonnement par état, substitution post-hoc, interpolation vers un `eta`
voisin, ajout de `eta` plus petit après inspection des résultats.

`ETA_ABSOLUTE_LEVELS_FOR_CEFF_THR = MANDATORY` ; `ETA_PEAK_NORMALIZED_PER_STATE = REJECTED`
(préserve la relation asymptotique `T_thr ~ (eta/B)^(1/(2nu))` entre `C_eff^thr`
et `C_short`, cf. `short-time-oracles.md` §8).

Éligibilité de domaine pour une série de réponse élémentaire `a` :

```math
ETA\_PREPEAK\_RANGE\_ELIGIBLE(a) \iff 0<\eta<F_{peak,a}.
```

L'égalité stricte est exclue. Si `eta>=F_peak,a` est certifié :

```text
THRESHOLD_LEVEL_NOT_ADMISSIBLE_PREPEAK
```

Cette formulation, fondée sur le domaine pré-pic, remplace toute formulation
antérieure au maximum du premier lobe entier (`..._NOT_ADMISSIBLE_FIRST_LOBE`).
Aucun rebond après `T_peak` ne rend un niveau admissible.

Qualification stricte de l'événement montant : le croisement pré-pic unique
n'est `T_thr` que si `s chi'(T_thr)>0`. Une dégénérescence exacte établie par
oracle `STRUCTURAL_ANALYTIC` exclut tout `T_thr` qualifiant à ce niveau
(`NO_QUALIFYING_PREPEAK_THRESHOLD_EVENT`). Une positivité stricte non
certifiable numériquement retombe sur `SIMPLE_ROOT_CONTROL` /
`DEGENERATE_ROOT_CONTROL` déjà validés et retourne
`DEGENERATE_OR_NEAR_DEGENERATE_ROOT_UNRESOLVED`.

`T_down(eta)` reste un auxiliaire obligatoire (horizon de la garde de
récurrence, §12) ; un `T_down` non résolu rend le niveau
`THRESHOLD_LEVEL_ADMISSIBILITY_UNRESOLVED`.

Garde de précision relative profonde, réutilisant le budget `e_u` déjà validé
(`temporal-event-solver.md` §22-23) en coordonnée `u_thr=Omega_safe T_thr/pi` :

```math
r_{thr,time}=e_u/u_{thr}\le\tau_{event}=10^{-10}.
```

Aucune tolérance nouvelle. Conséquence diagnostique nécessaire seulement :
`u_thr>=tau_root/tau_event=1e-2` ; la porte normative reste le test complet
ci-dessus.

Triage complet d'admissibilité par niveau et série :
`THRESHOLD_LEVEL_NUMERICALLY_ADMISSIBLE` exige (A) `T_peak` confirmatoire,
(B) `0<eta<F(T_peak)` certifié, (C) qualification montante stricte certifiée,
(D) `T_down(eta)` certifié, (E) garde de précision relative satisfaite.
Sinon : `THRESHOLD_LEVEL_ADMISSIBILITY_UNRESOLVED`, niveau `NONCONFIRMATORY`.
Formules complètes : `temporal-event-solver.md` §27.

Fermeture de dépendance complète : pour toute quantité ou verdict dérivé `Q`
(un `C_eff^thr`, `Delta1^thr`, une valeur de dérivée centrale à un `h`, un
verdict de stabilité de dérivée, une comparaison `Lambda=2 -> 3`), le domaine
commun `E_eta^common(Q)` est l'intersection, sur la fermeture complète de
dépendance `D(Q)` de toutes les séries de réponse élémentaires
comparées/combinées/testées, des `eta` préenregistrés numériquement
admissibles pour chaque membre. Aucune comparaison de stabilité ne compare
des valeurs de seuil évaluées sur des sous-ensembles `eta` différents.

Si aucun `eta` ne survit :

```text
THRESHOLD_ESTIMATOR = NOT_APPLICABLE_NO_COMMON_ETA
```

Si un `eta` commun survit mais qu'un statut d'événement/admissibilité requis
reste non résolu, la quantité/le verdict dérivé est `NUMERICALLY_INCONCLUSIVE`
selon la propagation de statut déjà existante.

Publication par niveau et par série (diagnostic sauf `e_u/u_thr`, qui est la
porte normative) : `eta, lambda_eta, F_peak, eta/F_peak, T_peak, T_thr(eta),
T_thr(eta)/T_peak, u_thr, e_u, e_u/u_thr, T_down(eta)`, statut
d'admissibilité, motif d'exclusion/non-résolution. Publier séparément par
`Lambda=2` et `Lambda=3`.

Borne structurelle globale (`short-time-oracles.md` §9) :
`F<=Var(n_p)Var(n_q)<=1/16` (`THRESHOLD_GLOBAL_F_BOUND=STRUCTURAL_ANALYTIC`,
`THRESHOLD_GLOBAL_F_MAX=1/16`), raffinement de l'oracle générique déjà validé
`0<=F<=1`.

La densification de la grille au-delà des valeurs préenregistrées ci-dessus
est `NON_BLOCKING_BACKLOG` pour ce lot et n'est pas appliquée.

### Règle opérationnelle de convergence court-terme

Dérivation analytique complète : `short-time-oracles.md` §10.

**Applicabilité en exposant.** Requiert référence et état de même exposant
dominant certifié `nu in {1,3,5}` avec coefficients dominants certifiés non
nuls. Sinon `SHORT_TIME_CONVERGENCE_NOT_APPLICABLE`
(`SHORT_TIME_COMPARISON=NOT_APPLICABLE`, `D_THR=NOT_DEFINED`) ; exposant non
résolu -> `SHORT_TIME_CONVERGENCE_EXPONENT_UNRESOLVED` ; `nu>5` ->
`SHORT_TIME_CONVERGENCE_RANGE_NOT_PREREGISTERED`. Ces trois statuts sont
`NONCONFIRMATORY`. `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` reste `OPEN` et
conditionne les classifications de zéro numérique.

**Construction de la queue commune.** Utiliser le domaine `eta` commun
admissible déjà validé (§27 de `temporal-event-solver.md`). Sélectionner
déterministiquement les trois plus petites valeurs `lambda` communes
admissibles `lambda_0>lambda_1>lambda_2`
(`SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS=3`), sans saut de niveau, sans
triplet intérieur, sans substitution ni ajout d'`eta`. Moins de 3 niveaux
communs -> `SHORT_TIME_CONVERGENCE_INSUFFICIENT_COMMON_RANGE`.

**Résidu et budget.** Avec `S_short^(q)=(1/nu) log|a_state^(q)/a_ref^(q)|`,
`L_thr^(q)(eta)=log[T_ref^(q)(eta)/T_state^(q)(eta)]`,
`D^(q)(eta)=L_thr^(q)(eta)-S_short^(q)`, et le budget déjà validé
`r_T=e_u/u`, `L(r)=-log(1-r)` :

```math
e_D(\eta)=\max\bigl(|D^{(2p)}-D^{(p)}|,\;L(r_{T,ref})+L(r_{T,state})+|S_{short}^{(2p)}-S_{short}^{(p)}|\bigr).
```

`D(eta)=D^(2p)(eta)`, `m_D=max(0,|D|-e_D)`, `M_D=|D|+e_D`. Résolu ssi
`m_D>0`. Aucune tolérance nouvelle.

**Motif de résolution information-monotone.** Avec `R_i:=(m_D,i>0)`, seul un
préfixe résolu contigu suivi éventuellement d'un suffixe de plancher est
admis. Tout motif non contigu -> `SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE`.

**Triage exécutable :**

```text
R0=F, R1=F, R2=F
    -> SHORT_TIME_CONVERGENCE_NO_RESOLVED_RESIDUAL
       (NONCONFIRMATORY_INSUFFICIENT_RESOLUTION, non éligible au verdict fort)

R0=T, R1=T, R2=F
    -> exiger même signe certifié (I_D,0, I_D,1), M_D,1<m_D,0, M_D,2<m_D,1
    -> si passe : SHORT_TIME_CONVERGENCE_SUPPORTED_FLOOR_AFTER_CONTRACTION
       (SUPPORT_MODE=FLOOR_AFTER_CONTRACTION)
    -> sinon : SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE

R0=T, R1=F, R2=F
    -> exiger M_D,1<m_D,0, M_D,2<M_D,1
    -> si passe : SHORT_TIME_CONVERGENCE_SUPPORTED_FLOOR_AFTER_CONTRACTION
    -> sinon : SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE

R0=T, R1=T, R2=T
    -> exiger même signe certifié sur les trois, M_D,1<m_D,0, M_D,2<m_D,1
    -> former z_i=lambda_i^(2/nu), q_01=z_1/z_0, q_12=z_2/z_1,
       R_01=(D_1-q_01 D_0)/(1-q_01), R_12=(D_2-q_12 D_1)/(1-q_12),
       e_R01, e_R12 (mêmes pondérations), m_R12=max(0,|R_12|-e_R12),
       M_shift=|R_12-R_01|+e_R12+e_R01
    -> exiger m_R12<=M_shift
    -> si tout passe : SHORT_TIME_CONVERGENCE_SUPPORTED_RESOLVED_TREND
       (SUPPORT_MODE=RESOLVED_RICHARDSON_TREND)
    -> sinon : SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE

motif non contigu (ex. F,T,F ou F,T,T)
    -> SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE
```

`SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE` n'est jamais présenté comme une
falsification physique de l'oracle analytique de court terme. Aucune valeur
`c1`/`c2`/taux résolu n'est inférée de `FLOOR_AFTER_CONTRACTION`. `M_shift`
n'est jamais présenté comme une borne de troncature rigoureuse
(`RICHARDSON_ZERO_COMPATIBILITY = OPERATIONAL_COMPATIBILITY_NOT_RIGOROUS_TRUNCATION_BOUND`).

```text
SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET =
{ SUPPORTED_RESOLVED_TREND, SUPPORTED_FLOOR_AFTER_CONTRACTION }
```

**Traitement par paire avant `Delta1`.** Évaluer séparément `D_A^thr` et
`D_B^thr` (`SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY=YES`). Une annulation
`D_A-D_B~=0` ne peut jamais racheter un canal non confirmatoire
(`DELTA1_CANCELLATION_AS_PRIMARY_EVIDENCE=REJECTED`). `Delta1_dyn^thr=D_A-D_B`
reste secondaire.

**Agrégation complète `Delta1` :**

```text
1. si A et B sont tous deux dans STRONG_STATUS_SET
       -> DELTA1_SHORT_LIMIT = SUPPORTED
2. sinon si A ou B est NOT_APPLICABLE ou RANGE_NOT_PREREGISTERED
       -> DELTA1_SHORT_LIMIT = NOT_APPLICABLE
3. sinon si A ou B est INSUFFICIENT_COMMON_RANGE
       -> DELTA1_SHORT_LIMIT = INSUFFICIENT_COMMON_RANGE
4. sinon si A ou B est CONTROL_SENSITIVE
       -> DELTA1_SHORT_LIMIT = CONTROL_SENSITIVE
5. sinon
       -> DELTA1_SHORT_LIMIT = NONCONFIRMATORY
```

Aucune paire mixte n'est promue silencieusement à `SUPPORTED`.

**Statut local par cutoff et queue conjointe.** Un statut local par `Lambda`
peut être publié à titre `LOCAL_DIAGNOSTIC_ONLY`, en utilisant le domaine
commun admissible propre à ce cutoff ; il ne supporte pas seul une
revendication de stabilité de cutoff. Pour une revendication comparant
`Lambda=2` et `Lambda=3`, appliquer D'ABORD l'intersection conjointe :

```math
E_\eta^{joint\_cutoff}(Q)=\bigcap(\text{eta admissibles à }\Lambda=2\text{ ET }\Lambda=3\text{, pour chaque membre comparé}).
```

Sélectionner ENSUITE les trois plus petites valeurs `lambda` de
`E_eta^joint_cutoff(Q)`, et utiliser cette même queue à `Lambda=2` et à
`Lambda=3`. Si `D_A` et `D_B` sont forts aux deux cutoffs sur cette même
queue : `CUTOFF_STABLE_SHORT_TIME_CONVERGENCE=SUPPORTED`. Si l'intersection
conjointe contient moins de 3 niveaux :
`CUTOFF_STABLE_SHORT_TIME_CONVERGENCE=INSUFFICIENT_COMMON_RANGE`. Sinon,
propager les statuts non confirmatoires fail-closed. Ceci ne ferme pas
`TRUNCATION_COMPARISON_TOLERANCES`, qui reste `OPEN`.

**Publication diagnostique** par queue par paire : `nu`, triplets `lambda`/`z`,
`q_01`,`q_12`, `D_i`, `e_D,i`, `m_D,i`/`M_D,i`, motif résolu/non résolu,
mode/statut de support ; pour `RESOLVED_RICHARDSON_TREND` en plus `R_01`,
`R_12`, `e_R01`, `e_R12`, `m_R12`, `M_shift`. Contraction dominante attendue
par pas de grille `lambda` : facteur `16` (`nu=1`), `4^(2/3)~=2.52` (`nu=3`),
`4^(2/5)~=1.74` (`nu=5`). Un verdict `nu=1` typique peut n'avoir exactement
que les trois niveaux minimaux ; la perte d'un niveau donne
`INSUFFICIENT_COMMON_RANGE`, pas une réparation post hoc de la grille.

```text
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE       = VALIDATED_FOR_FREEZE
SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS    = 3
SHORT_TIME_CONVERGENCE_MAX_PREREGISTERED_NU = 5
SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY     = YES
SHORT_TIME_CONVERGENCE_NEW_SCALAR_TOLERANCE = NONE
```

### `T_grow`

```math
T_{grow}
=\inf\operatorname*{argmax}_{0<t<T_{peak}}F'(t).
```

Candidats intérieurs :

```math
H_{grow}=\chi'^2+\chi\chi''=0.
```

Tous les candidats pertinents dans `(0,T_peak)` sont comparés ; le premier maximiseur global est retenu.

### Famille de bracketing

Une seule famille :

```math
B=\{\beta_1>\cdots>\beta_K>0\}.
```

```math
\Delta t_k^{event}
=\beta_k\frac{\pi}{s_{event}\Omega_{scale}},
```

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

Par défaut :

```math
\Omega_{scale}=E_{max}-E_0.
```

Le coût de `T_grow` est plus élevé : `H_grow` a la bande `2 Omega` et ses bornes de dérivées sont des produits de sommes spectrales.

La certification de cellules peut utiliser des bornes de Lipschitz / dérivées. Une densité moyenne de zéros ne constitue jamais un certificat de complétude.

Valeurs `beta_k` préenregistrées :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}
```

`beta` contrôle uniquement le maillage initial de certification / bracketing, pas une tolérance sur le temps final (obtenu par le solveur spectral continu). `beta=1` correspond à une demi-période de la bande maximale de la fonction de certification ; raffinement dyadique imbriqué ; `beta=1/8` donne une phase maximale `pi/8` par cellule à la bande limite. Aucune finesse supplémentaire n'est requise comme garantie de complétude, celle-ci reposant sur l'exclusion certifiée des cellules, leur subdivision adaptative et le solveur continu.

Critère de contrôle sous raffinement : identité du premier événement stable, ordre des candidats pertinents stable, aucune cellule antérieure non résolue, temps continus compatibles selon les tolérances numériques (`OPEN`). Sinon : `TIME_EVENT_CONTROL_SENSITIVE`.

---

## 10. Conditionnement et budget numérique dynamique

Le conditionnement d'une racine simple est invariant sous multiplication régulière de la fonction de racine. Le choix de `chi` plutôt que `F` sert principalement à obtenir des bornes de dérivées plus directes, un modèle d'erreur spectral plus simple et moins de racines parasites.

Diagnostics attachés aux fonctions résolues :

```text
T_thr / T_down -> |chi'|
T_peak         -> |chi''|
T_grow         -> |H_grow'|
```

avec :

```math
H_{grow}'=3\chi'\chi''+\chi\chi'''=2F'''.
```

Le budget dynamique doit contrôler au minimum :

```text
residuals of eigensystem / projectors
orthogonality defects
stability of Bohr frequencies and spectral weights
phase accumulation delta_omega * t
cancellations in spectral sums
root / argmax conditioning
```

Les tolérances numériques et la règle uniforme de stabilité sous précision sont fixées dans `temporal-event-solver.md` (sections 15-24) et `VALIDATED_FOR_FREEZE`.

Le budget propagé vers `Delta1` est désormais défini dans
`derivative-error-budget.md` et porte le statut :

```text
DELTA1_PROPAGATED_ERROR_BUDGET = VALIDATED_FOR_FREEZE
```

La famille `A_DELTA_VALUES`, le critère de stabilité de la dérivée et la
règle d'usage de Richardson sont également `VALIDATED_FOR_FREEZE`.

Le plan de validation renvoie à `derivative-control.md` et
`derivative-error-budget.md` pour leurs définitions normatives détaillées ;
il ne les duplique pas ici.

---

## 11. Décomposition sectorielle et pureté de chemin

Pour la multigraduation conjointe des `E_i`, utiliser les projecteurs d'espace d'opérateurs `Pi_m`.

Une transition physique satisfait :

```math
m_i-m_{i-1}=\Delta n_i.
```

Pour `d<N/2` :

```text
TARGET_DIRECT
TARGET_WINDING
NON_TARGET_TRANSITION
```

sont définis comme dans la spécification.

Pour les moments sectoriels :

```math
B_{m,r}^{pq}
=Tr(\rho[n_p,\Pi_m ad_H^r(n_q)]).
```

Pour `m!=0` :

```math
B_{-m,r}=(-1)^{r+1}\overline{B_{m,r}}.
```

Les ordres pairs s'annulent canal par canal ; les ordres impairs sont appariés avec le facteur correct.

Le canal `m=0` est testé comme oracle nul exact.

Poids :

```math
P_\alpha(\tau)=\int_0^\tau\chi_\alpha(t)^2dt
```

évalués analytiquement à partir de la représentation en sinus.

```math
P_{sector}=P_{direct}+P_{winding}+P_{non-target},
```

```math
Purity_{direct}=P_{direct}/P_{sector}.
```

Si `P_sector=0` :

```text
PATH_DIAGNOSTIC = INACTIVE
```

Ligne de base algébrique, calculée avant l'évolution temporelle :

```math
P_0(\theta,\Lambda,pq)=Purity_{direct}(0^+),
\qquad
I_0(\theta)=1-P_0(\theta).
```

Impureté monotone :

```math
I_{max}(\theta,\tau)=\sup_{0<s\le\tau}(1-Purity_{direct}(\theta,s)).
```

La garde normative porte sur la dégradation supplémentaire normalisée, définie lorsque `P_0>0` :

```math
R_{path}(\theta,\tau)
=\frac{I_{max}(\theta,\tau)-I_0(\theta)}{P_0(\theta)},
```

```math
\tau_{path}(\epsilon)
=\inf\{\tau>0:R_{path}(\tau)>\epsilon\}.
```

Un événement passe la garde pour `epsilon` si `R_path(T_event)<=epsilon`.

Si `P_0=0` :

```text
PATH_BASELINE_STATUS = NO_DIRECT_BASELINE
```

et `R_path` n'est pas applicable.

La famille de contrôle `epsilon in E_path subset (0,1)` est `OPEN` numériquement et doit être commune aux cutoffs comparés. Appliquer une grille de contrôle commune directement à `I_max` est supersédé.

À publier par domaine complet `(theta,Lambda,pq)` :

```text
P_0(theta)
W(0+)
O(0+)
R_path(theta,tau)
tau_path(theta,epsilon)
```

Le contrôle `Lambda=2 -> 3` est obligatoire avec la même grille `E_path`.

Pour `d=3` :

```text
ARRIVAL_INTERPRETATION = EXCLUDED
```

même si les deux arcs sont séparables algébriquement.

---

## 12. Récurrence event-local

Autocorrélation connectée :

```math
C_j(t)
=\frac{Re\,Tr[\rho_\theta\,\delta n_j(t)\delta n_j]}
{Tr[\rho_\theta(\delta n_j)^2]}.
```

Si le dénominateur est nul :

```text
RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
```

Sites normatifs :

```text
RECURRENCE_SITE_SET(p,q) = {p,q}
```

Les sites intermédiaires sont `DIAGNOSTIC_ONLY` et ne participent pas au veto normatif.

Détecteur hystérétique : pour `gamma=(gamma_-,gamma_+)` avec `gamma_-<gamma_+<1` et un horizon `tau`, il y a sortie lorsque `C_j<=gamma_-`, puis retour si `C_j>=gamma_+` après cette sortie et avant `tau`. Les trois états sont exhaustifs :

```text
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
```

Pour la relation `(p,q)`, un retour à l'une quelconque des deux extrémités compte comme retour avant événement.

Horizons normatifs, obligatoires :

```text
T_grow       -> tau = T_peak
T_thr(eta)   -> tau = T_down(eta)
```

`T_down(eta)` est donc un auxiliaire obligatoire de la garde de récurrence des seuils et non un estimateur scientifique indépendant.

La famille `Gamma` est un ensemble préenregistré contenu dans `{(gamma_-,gamma_+):gamma_-<gamma_+<1}`, borné dans l'ordre partiel :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm},
```

```math
\gamma_-^{strict}\le\gamma_-\le\gamma_-^{perm},
\qquad
\gamma_+^{strict}\ge\gamma_+\ge\gamma_+^{perm}.
```

Aucun domaine rectangulaire `G_- x G_+` n'est exigé. La largeur `h(gamma)=gamma_+-gamma_->0` est explicite ; `h=0` est exclu du contrôle principal. Les bornes numériques restent `OPEN`.

Verdict robuste évalué aux deux bornes seulement :

```text
gamma_perm ne détecte aucun retour
    -> RECURRENCE_STATUS = ROBUST_CLEAN

gamma_strict détecte un retour
    -> RECURRENCE_STATUS = ROBUST_CONTAMINATED

sinon
    -> RECURRENCE_STATUS = CONTROL_SENSITIVE
```

Le même domaine `Gamma` est utilisé pour `reference`, `+delta`, `-delta`, `Lambda=2` et `Lambda=3`.

Un événement candidat est temporellement interprétable seulement si :

```text
PATH_CONTROL_ACCEPTABLE
AND RECURRENCE_CONTROL_ACCEPTABLE
```

sur toute la famille de contrôle déclarée.

Si la séparation ne peut être établie :

```text
TIME_WINDOW_STATUS = INCONCLUSIVE
```

---

## 13. Signaux et oracles dynamiques

```math
C_{eff}^{grow}
=T_{grow}^{ref}/T_{grow}^{state},
```

```math
C_{eff}^{thr}(\eta)
=T_{thr}^{ref}(\eta)/T_{thr}^{state}(\eta).
```

`T_grow` est primaire ; la famille `T_thr(eta)` est secondaire et doit être publiée sur tout son domaine admissible.

Oracle de rééchelonnement hors famille scientifique :

```math
H_s=sH_{ref}
\Rightarrow
F_s(t)=F_{ref}(st)
```

et :

```math
C_{eff}^{grow}=C_{eff}^{thr}(\eta)=s.
```

Signal principal :

```math
\Delta_1=\log(C_{O1A}/C_{O1B}).
```

Tester :

```math
\Delta_1(g,\mu,0)=0,
```

et sur le sous-ensemble miroir préenregistré :

```math
\Delta_1(-\delta)=-\Delta_1(+\delta).
```

Oracle nul :

```math
\Delta_2=0
```

séparément pour `grow` et pour chaque `eta` admissible.

Une violation de `Delta2` au-delà de la tolérance est un défaut pipeline/symétrie, jamais un signal.

La règle finale de cohérence entre `grow` et `thr` reste `OPEN`.

---

## 14. Campagne MAIN

Grille nominale :

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

La grille MAIN sonde `Delta1` à brisure finie. Elle n'est pas une grille de dérivée `Xi1`.

Contrôles séparés :

```text
g=0, mu=0 -> pure-hopping oracle
g=0.10    -> weak-g stress outside nominal domain
delta=0.9 -> disclosed qualification/stress outside nominal domain
```

À figer avant campagne :

```text
NEGATIVE_DELTA_ORACLE_SUBSET = OPEN
```

---

## 15. Sous-campagne SOFT-LOOP

```text
g  = 1
mu = {-1.25, -1.5, -2}
```

À chaque fond :

1. diagonaliser à `delta=0` et publier `d_GS`, `gap_0` ;
2. évaluer la grille de coordonnées `x` préenregistrée :

```text
STATIC_X_PRIMARY = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_X_SATURATION_DIAGNOSTIC = {±4}
```

`STATIC_X_SATURATION_DIAGNOSTIC` est `EXTENDED_DIAGNOSTIC` (sonde du régime de grand `|x|` / saturation) et ne peut pas à lui seul faire échouer la porte statique obligatoire ;
3. tester statiquement :

```math
gap(\delta)/gap_0\simeq\sqrt{1+x^2},
```

```math
2\langle\Phi\rangle\simeq-x/\sqrt{1+x^2},
```

avec :

```math
x=6g\delta/gap_0;
```

L'ensemble discriminant pour un futur critère de collapse agrégé est :

```text
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES = {1/4, 1/2, 1, 2}
```

Les points de signe négatif sont un contrôle numérique / oracle d'implémentation de la covariance exacte (`NEGATIVE_X_HALF_ROLE = NUMERICAL_CONTROL / IMPLEMENTATION_ORACLE`), non une évidence indépendante de collapse. `x=0` est un contrôle de normalisation/symétrie (`STATIC_X_ZERO_ROLE = NUMERICAL_CONTROL / NORMALIZATION_ORACLE`), non une évidence de collapse discriminante. Ni l'un ni l'autre ne peuvent inflater un futur décompte d'évidence de collapse agrégée ;

Le critère numérique de conformité est `VALIDATED_FOR_FREEZE`
(`STATIC_COLLAPSE_NUMERICAL_CRITERION = VALIDATED_FOR_FREEZE`,
`STATIC_COLLAPSE_TOLERANCE = 0.10`). Les formules complètes sont dans
`soft-loop-static-gate.md` §6 ; l'ordre exécutable de classification, repris
tel quel, est :

```text
a) si un L > tau_static             -> SOFT_LOOP_STATIC_DEVIATES
b) sinon si chevauchement précision/frontière
                                     -> SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
c) sinon si tous U <= tau_static ET X_max^(3) < 1
                                     -> SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
d) sinon                            -> SOFT_LOOP_STATIC_SUPPORTED
```

où `L`/`U` sont les intervalles numériques de contrôle issus du doublement de
précision `p/2p` sur les résidus signés (gap relatif, `Phi` absolu), évalués
en norme ponctuelle `L_infinity` sur `{1/4,1/2,1,2}`, et où `X_max^(3)` est la
magnitude maximale échantillonnée à `Lambda=3` sur les mêmes points physiques
que `Lambda=2` (garde d'information `STATIC_LAMBDA3_INFORMATION_GUARD =
REQUIRED`, `STATIC_LAMBDA3_MIN_DISCRIMINATING_MAGNITUDE = 1`).
`SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION` est `NUMERICAL_CONTROL /
NONCONFIRMATORY_FOR_CUTOFF_STABILITY` : elle ne bloque pas la publication des
observables brutes `Lambda=3`, ne régénère pas la grille et ne modifie pas
`tau_static`. Une revendication de mécanisme à deux niveaux stable au cutoff
exige `SOFT_LOOP_STATIC_SUPPORTED` ordinaire à `Lambda=2` et à `Lambda=3` ;
ce statut y compris `SOFT_LOOP_STATIC_SUPPORTED` reste provisoire pour
l'interprétation confirmatoire finale de campagne tant que
`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` (`OPEN`) n'est pas fermé et validé.
Le diagnostic `±4` reste `EXTENDED_DIAGNOSTIC` et ne peut pas à lui seul
modifier le statut de la porte statique ;

4. seulement si la réduction est suffisamment supportée selon le critère préenregistré, utiliser :

```math
\delta_c=gap_0/(6g)
```

pour la famille dynamique :

```math
h_k=\alpha_k\delta_c.
```

Pour le contrôle `Lambda=2 -> 3`, les `h_k` sont générés une fois depuis `gap_0^(Lambda=2)` puis repris identiquement à `Lambda=3`.

Pour une `Delta1` lisse et impaire :

```math
\widehat\Xi_1(\alpha)
=\Xi_1+C_2\alpha^2+O(\alpha^4).
```

Diagnostic quadratique pour `alpha,alpha/2,alpha/4` :

```math
R_2
=\frac{\widehat\Xi(\alpha)-\widehat\Xi(\alpha/2)}
{\widehat\Xi(\alpha/2)-\widehat\Xi(\alpha/4)}
\to4
```

si le terme quadratique domine et si les différences restent au-dessus du plancher numérique.

Richardson n'est autorisé que selon une règle préenregistrée et ne remplace jamais les valeurs brutes.

`Delta1` n'a pas d'oracle de collapse universel en `x` ; un collapse dynamique éventuel est secondaire.

Valeurs encore `OPEN` :

```text
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE
```

`STATIC_X_CONTROL_VALUES` et `STATIC_COLLAPSE_NUMERICAL_CRITERION` sont
`VALIDATED_FOR_FREEZE` (cf. §17).

---

## 16. Contrôle de troncature

Contrôle principal : mêmes paramètres physiques et mêmes observables à `Lambda=2` puis `Lambda=3`.

Pour les harmoniques :

```text
same k = primary convergence pairing
same j=2Lambda-k = edge-relative diagnostic
```

Les harmonique `k=5,6` propres à `Lambda=3` sont `EXTENDED_DIAGNOSTIC`.

Le sous-ensemble `Lambda=3` doit concentrer les points de stress préenregistrés, notamment dans la région faible `g`, `mu<0`, grand `|delta|`, sans modifier le sous-ensemble après inspection.

À figer :

```text
TRUNCATION_STRESS_POINT_SUBSET = OPEN
TRUNCATION_COMPARISON_TOLERANCES = OPEN
```

---

## 17. Paramètres numériques réellement OPEN

Cette liste est normative pour la phase de clôture et remplace les anciennes listes dispersées.

```text
# threshold / interpretation
EPS_PATH_CONTROL_DOMAIN_AND_GRID
GAMMA_CONTROL_DOMAIN_AND_GRID
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS

# campaign / cutoff
NEGATIVE_DELTA_ORACLE_SUBSET
TRUNCATION_STRESS_POINT_SUBSET
TRUNCATION_COMPARISON_TOLERANCES

# verdicts
ESTIMATOR_COHERENCE_CRITERION
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

Ne sont plus `OPEN` (clôturés ou `VALIDATED_FOR_FREEZE`) :

```text
ORDERED_RELATION_CONVENTION
PARAMETER_CAMPAIGN_MAIN_GRID
TIME_INTERPOLATION_AS_FINAL_ESTIMATOR
TIME_FINITE_DIFFERENCE_DERIVATIVES
GLOBAL_FACTOR_TWO_FOR_ALL_EVENTS
NEAR_CROSSING_GAP_THRESHOLD
ZERO_GRADE_PATH_PURITY_CORRECTION
RAW_EIGENVECTOR_NONZERO_COUNT_ORACLE
ROOT_SOLVER_TOLERANCES
SPECTRAL_PRECISION_CONTROL
SIMPLE_ROOT_CONTROL
ARGMAX_TOLERANCES
DELTA1_PROPAGATED_ERROR_BUDGET
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE
DEGENERATE_ROOT_CONTROL
STATIC_X_CONTROL_VALUES
STATIC_COLLAPSE_NUMERICAL_CRITERION
ETA_GRID_AND_ADMISSIBLE_DOMAIN
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE
```

`DEGENERATE_ROOT_CONTROL` est `VALIDATED_FOR_FREEZE`, avec
`DEGENERATE_ROOT_NEW_TOLERANCE = NONE` (protocole détaillé :
`temporal-event-solver.md` §26).

`ETA_GRID_AND_ADMISSIBLE_DOMAIN` est `VALIDATED_FOR_FREEZE` (grille absolue,
borne structurelle `1/16`, éligibilité pré-pic, qualification montante
stricte, garde de précision relative et fermeture de dépendance commune ;
protocole détaillé : `temporal-event-solver.md` §27, `short-time-oracles.md`
§9).

`SHORT_TIME_THRESHOLD_CONVERGENCE_RULE` est `VALIDATED_FOR_FREEZE` (cible
`D_pq^thr -> 0`, coordonnée `z=lambda_eta^(2/nu)`, portée `nu in {1,3,5}`,
queue commune à trois niveaux minimum, branchement information-monotone,
statuts forts `SUPPORTED_RESOLVED_TREND`/`SUPPORTED_FLOOR_AFTER_CONTRACTION`,
traitement par paire avant `Delta1`, queue conjointe de stabilité au cutoff ;
protocole détaillé ci-dessus et `short-time-oracles.md` §10). Ne ferme ni
`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` ni `TRUNCATION_COMPARISON_TOLERANCES`,
qui restent `OPEN`.

---

## 18. Verdicts autorisés

La liste des verdicts scientifiques généraux ci-dessous n'est **pas exhaustive** des statuts publiables : elle ne décrit que la couche de verdict général.

Verdicts scientifiques généraux :

```text
PASS
FAIL
INCONCLUSIVE
INACTIVE
NOT_APPLICABLE
```

Statuts spécialisés explicitement autorisés, notamment :

```text
NOT_DEFINED
EXCLUDED
INACTIVE_EXACT
ZERO_EXACT
NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
NO_DIRECT_BASELINE
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
ROBUST_CLEAN
ROBUST_CONTAMINATED
CONTROL_SENSITIVE
TIME_EVENT_CONTROL_SENSITIVE
DERIVATIVE_CONTROL_SENSITIVE
SOFT_LOOP_STATIC_SUPPORTED
SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
SOFT_LOOP_STATIC_DEVIATES
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

Un statut spécialisé ne doit pas être remappé silencieusement vers `PASS` ou `FAIL`.

Tout verdict doit publier son domaine complet et les contrôles ayant conduit à ce statut.

---

## 19. Audit critique de clôture

Avant gel, Claude Code reçoit un mandat **read-only**.

Il peut challenger librement, mais chaque remarque doit être classée :

```text
BLOCKING
    contradiction démontrée
    erreur affectant la validité
    définition inexécutable
    défaut pouvant modifier un verdict

NON_BLOCKING_BACKLOG
    amélioration, généralisation ou extension non nécessaire à la validité de 0B

REJECTED
    objection fausse, non démontrée ou hors périmètre
```

Principe :

```text
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_NEW_CONCEPTUAL_BRANCHING_WITHOUT_BLOCKING_DEFECT
```

Aucune modification scientifique ne peut être faite silencieusement pendant l'audit ou l'implémentation.

---

## 20. Critère d'ouverture de l'implémentation

`IMPLEMENTATION_0B = NOT_AUTHORIZED` tant que :

1. l'audit critique de clôture n'est pas arbitré ;
2. tous les paramètres du §17 affectant les résultats ne sont pas préenregistrés ;
3. `specification.md` et le présent plan ne sont pas cohérents et validés pour gel global ;
4. la revue finale de cohérence / syntaxe n'est pas faite ;
5. Lionel ORCIL n'a pas explicitement gelé le paquet ;
6. `docs/governance/current-task.md` n'autorise pas explicitement le lot d'implémentation.

Après autorisation, Claude Code conserve son rôle critique : un défaut `BLOCKING` stoppe le lot et retourne à l'arbitrage ; un `NON_BLOCKING_BACKLOG` ne modifie pas le périmètre en cours.
