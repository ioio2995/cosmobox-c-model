# Toy Model 0B — consolidation pré-gel

Statut : **index de consolidation — revue de clôture**  
Projet : `ioio2995/cosmobox-c-model`  
Branche : `documentation/model0b-foundation`  
Base du lot : `08d5ca506ff05e15dd9bc084ea121c3d0a19b662`

Ce document ne crée aucune nouvelle hypothèse physique. Il consolide les décisions déjà stabilisées dans les supports 0B afin de préparer la revue de clôture, de supprimer les faux `OPEN` historiques et de limiter l'ouverture de nouvelles branches conceptuelles.

Pendant cette phase, `specification.md` et `validation-plan.md` restent les sources scientifiques principales. Lorsque leur statut historique contredit explicitement le présent index sur un point déjà arbitré, le présent index donne **le statut courant du lot**, jusqu'à intégration mécanique dans les deux sources principales avant gel final.

---

## 1. Règle de clôture

Le challenge scientifique reste autorisé en permanence, y compris par Claude Code.

Une objection ne rouvre toutefois un bloc stabilisé que si elle démontre au moins un des cas suivants :

```text
BLOCKING_CONTRADICTION
    deux exigences / théorèmes du protocole sont incompatibles

BLOCKING_ERROR
    une affirmation utilisée par le protocole est mathématiquement ou numériquement fausse

BLOCKING_UNEXECUTABLE
    une définition ou un verdict ne peut pas être implémenté / évalué comme spécifié

BLOCKING_VALIDITY_RISK
    le défaut peut modifier un verdict scientifique ou invalider un contrôle requis
```

Une amélioration, généralisation, observable supplémentaire, preuve plus élégante ou extension de domaine qui n'est pas nécessaire à la validité de 0B est classée :

```text
NON_BLOCKING_BACKLOG
```

et ne rouvre pas le périmètre courant.

Principe :

```text
CHALLENGE_PERMANENT
EXPLORATION_BOUNDED
NO_NEW_CONCEPTUAL_BRANCHING_WITHOUT_BLOCKING_DEFECT
```

---

## 2. État scientifique consolidé

```text
MODEL0B_SYSTEM_AND_GAUSS           = VALIDATED_FOR_FREEZE
MODEL0B_TRUNCATION_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_OBSERVABLES         = VALIDATED_FOR_FREEZE
MODEL0B_STATIC_IDENTIFIABILITY     = VALIDATED_FOR_FREEZE
MODEL0B_DECLARED_SYMMETRIES        = VALIDATED_FOR_FREEZE
MODEL0B_NULL_ORACLES               = VALIDATED_FOR_FREEZE
MODEL0B_KUBO_PROBE                 = VALIDATED_FOR_FREEZE
MODEL0B_PRIMARY_SIGNAL_DELTA1      = VALIDATED_FOR_FREEZE
MODEL0B_PATH_GRADING               = VALIDATED_FOR_FREEZE
MODEL0B_PATH_PURITY_STRUCTURE      = VALIDATED_FOR_FREEZE
MODEL0B_RECURRENCE_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_SHORT_TIME_STRUCTURE       = VALIDATED_FOR_FREEZE
MODEL0B_SPECTRAL_TIME_STRUCTURE    = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
MODEL0B_SOFT_LOOP_STRUCTURE        = VALIDATED_FOR_FREEZE
MODEL0B_PARAMETER_CAMPAIGN_SHAPE   = VALIDATED_FOR_FREEZE

MODEL0B_NUMERICAL_CONTROL_VALUES   = OPEN
MODEL0B_FINAL_ACCEPTANCE_RULES     = OPEN
MODEL0B_DOCUMENT_CONSOLIDATION     = IN_PROGRESS
IMPLEMENTATION_0B                  = NOT_AUTHORIZED
```

`VALIDATED_FOR_FREEZE` ne signifie pas encore `FROZEN`. Le gel final reste une décision explicite de Lionel ORCIL après revue du paquet consolidé.

---

## 3. Invariants et choix physiques stabilisés

```text
TOPOLOGY               = cycle N=6
BACKGROUND             = b=(0,1,0,1,0,1)
PARTICLE_NUMBER        = sum n_i = 3
PHYSICAL_DIMENSION     = 40 Lambda - 2
LAMBDA_REFERENCE       = 2
LAMBDA_CHECK           = 3
LAMBDA_PILOT           = 1
J                      = 1
REFERENCE_POINT        = (g,mu,delta)=(1,0,0)
```

Hamiltonien :

```math
H(g,\mu,\delta)
= -\sum_i X_i
+ g\sum_iE_i^2
+ 2\mu N_{even}
+ g\delta\sum_i(-1)^iE_i^2.
```

Notation normative du terme électrique alterné :

```math
V_\delta=\sum_i(-1)^iE_i^2.
```

Ne pas utiliser `V_stag` pour ce terme afin d'éviter la collision avec les anciennes notations de matière.

Le rééchelonnement global `H -> sH` est hors famille scientifique et sert uniquement d'oracle de contrôle.

---

## 4. Symétries, réciprocité et oracles nuls

Les transformations unitaires / antiunitaires déclarées et leurs compositions ont été analysées dans les supports dédiés.

Résultats consolidés :

```text
R H(g,mu,delta) R^dag = H(g,mu,-delta)
Q = S R commutes with H(g,mu,delta)
K imposes chi_pq(-t) = -chi_pq(t)
stationarity + K => chi_pq(t) = chi_qp(t)
```

Conséquence : les relations dynamiques sont traitées comme **non orientées**. L'ancien `ORDERED_RELATION_CONVENTION = OPEN` est clos.

Classes d'arêtes :

```text
O1A = {(0,1),(2,3),(4,5)}
O1B = {(0,5),(1,2),(3,4)}
```

Oracles exacts :

```math
\Delta_1(g,\mu,0)=0,
```

```math
\Delta_1(g,\mu,-\delta)=-\Delta_1(g,\mu,+\delta),
```

```math
\Delta_2(g,\mu,\delta)=0.
```

Aucun stabilisateur générique déclaré n'échange `O1A` et `O1B` lorsque `delta != 0`.

---

## 5. Degré cyclique et tangentes

Gauss donne :

```math
D_{n_i}=D_{E_i}-D_{E_{i-1}}.
```

Avec :

```math
D_\Phi=\frac16\sum_iD_{E_i},
```

on a toujours :

```math
S_E=S_n+span{D_\Phi}.
```

Sur `delta=0` :

```math
D_\Phi \perp S_n
```

pour tout `(g,mu,0)` et pour la prescription canonique pure ou dégénérée.

Donc, si `D_Phi` est actif :

```math
S_E=S_n\oplus_\perp span\{D_\Phi\}.
```

La formule globale `dim S_E = 6` est rejetée. Les rangs doivent être recalculés à chaque point de campagne.

---

## 6. Court temps et sélection

La symétrie `K` impose une réponse impaire en temps, totalement et secteur par secteur.

La règle bipartite compacte est :

```text
d pair   -> nombre impair d'insertions diagonales dans tout terme cible physique
d impair -> nombre pair d'insertions diagonales ; zéro insertion autorisée
```

Conséquences 0B :

```text
d=1 -> nu=1 si l'arête est régulière
d=2 -> premier ordre physique cible possible r=3
d=3 -> premier ordre physique possible r=3
pure hopping -> canal cible d=2 exactement inactif à tous les ordres
```

Pour une arête `{p,q}={i,i+1}` :

```math
M_1^{pq}=J\langle X_i\rangle.
```

Pour `d(p,q)>=2` :

```math
M_1^{pq}=0.
```

Les moments de court temps peuvent être calculés sans spectre excité :

```math
M_r^{pq}
=-2\langle\Omega|n_p(H-E_0)^rn_q|\Omega\rangle
```

pour un fondamental pur, avec généralisation canonique par projecteur de fond.

`ad_H(O)=[H,O]` est distinct du Liouvillien Krylov :

```math
\mathcal L_H(O)=i[H,O].
```

---

## 7. Multigraduation, chemins et canal nul

Les superopérateurs :

```math
\mathscr L_i(O)=[E_i,O]
```

définissent une multigraduation conjointe `m=(m_0,...,m_5)`.

Pour une transition de matière donnée :

```math
m_i-m_{i-1}=\Delta n_i,
```

et les solutions compatibles forment :

```math
m=m_D+w\,1.
```

Pour `d<N/2` :

```text
TARGET_DIRECT       = transition ciblée, w=0
TARGET_WINDING      = transition ciblée, w!=0
NON_TARGET_TRANSITION = autre transition de matière
```

Pour `d=3`, l'interprétation d'arrivée mono-arc est exclue.

Exception auto-conjuguée : `[0]={0}` doit être comptée une seule fois en algèbre générale. Dans le secteur physique 0B, Gauss implique que les six `E_i` déterminent `n`, donc chaque espace propre conjoint des `E_i` est unidimensionnel et :

```math
[n_p,\Pi_0(O)]=0.
```

Ainsi :

```text
ZERO_GRADE_KUBO_CHANNEL      = INACTIVE_EXACT
ZERO_GRADE_NON_TARGET_WEIGHT = ZERO_EXACT
```

Il n'y a aucune correction numérique de `P_sector` ou `Purity_direct` due à `m=0`.

---

## 8. Pureté de chemin et récurrence

Pour chaque canal physique distinct `alpha` :

```math
P_\alpha(\tau)=\int_0^\tau\chi_\alpha(t)^2dt.
```

```math
P_{sector}=\sum_\alpha P_\alpha,
```

```math
Purity_{direct}=P_{direct}/P_{sector}.
```

Ces poids décrivent une composition sectorielle et ne constituent pas une décomposition additive de `chi(t)^2`.

L'impureté cumulée utilise :

```math
I(\tau)=1-Purity_{direct}(\tau),
```

```math
I_{max}(\tau)=\sup_{0<s\le\tau}I(s).
```

`epsilon_path` est une **famille de contrôle préenregistrée**, pas un seuil ajusté après inspection.

La garde de récurrence est event-local, basée sur l'autocorrélation connectée normalisée des sites source et récepteur. Elle utilise une famille hystérétique `Gamma`; ses valeurs numériques restent ouvertes.

Un événement temporel n'est interprétable comme arrivée propre que si :

```text
PATH_CONTROL_ACCEPTABLE
AND RECURRENCE_CONTROL_ACCEPTABLE
```

sur les familles de contrôle déclarées.

---

## 9. Représentation spectrale exacte de la dynamique

Pour l'état canonique stationnaire dans la base `K`-réelle :

```math
\chi_{pq}(t)=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
```

Les poids doivent être groupés par projecteur spectral en cas de dégénérescence excitées ; le nombre brut de vecteurs propres ayant un coefficient non nul n'est pas un oracle invariant.

Conséquences :

```text
FINITE_DIFFERENCE_TIME_DERIVATIVE = REJECTED
INTERPOLATION_AS_FINAL_ESTIMATOR   = REJECTED
NUMERICAL_QUADRATURE_FOR_P_ALPHA   = NOT_NOMINAL
```

Les dérivées temporelles sont obtenues analytiquement terme à terme et les intégrales `P_alpha` par intégrales fermées de produits de sinus.

---

## 10. Événements temporels

Définitions scientifiques conservées sur :

```math
F(t)=\chi(t)^2/4.
```

Équations numériques équivalentes :

```text
T_peak
    première racine qualifiante de chi'(t)=0
    avec maximum de F ; si non dégénéré : chi*chi'' < 0

T_thr(eta), T_down(eta)
    racines de chi(t)-s*2*sqrt(eta)=0 sur le premier lobe

T_grow
    premier maximiseur global de F' sur (0,T_peak)
    candidats : H_grow=chi'^2+chi*chi''=0
```

Une seule famille de raffinement sans dimension est utilisée :

```math
\mathcal B=\{\beta_1>\cdots>\beta_K>0\}.
```

Avec une borne spectrale sûre `Omega_scale` :

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

`T_grow` est plus coûteux à certifier non seulement par sa bande `2 Omega`, mais aussi parce que les bornes de dérivée de `H_grow` sont des produits de sommes spectrales.

Les valeurs numériques `beta_k` restent ouvertes.

---

## 11. Campagne de paramètres consolidée

### Campagne principale

```text
g     = {0.25, 0.5, 1, 2}
mu    = {-1, -0.75, -0.5, 0, +0.5, +1}
delta = {0, 0.1, 0.2, 0.4, 0.6, 0.8}
```

Cette grille mesure `Delta1` à brisure finie et ne doit pas être utilisée comme approximation de `Xi1`.

### Contrôles séparés

```text
g=0, mu=0          -> oracle pure hopping
g=0.10             -> stress faible-g hors domaine nominal
delta=0.9          -> qualification / stress hors domaine nominal
```

La réflexion impose des points `delta<0` comme oracles de covariance, mais le sous-ensemble négatif exact à exécuter reste à figer parmi les contrôles numériques.

### Sous-campagne SOFT-LOOP

```text
g  = 1
mu = {-1.25, -1.5, -2}
```

Elle étudie le doublet cyclique mou autour de `delta=0`, séparément de la grille MAIN.

---

## 12. Doublet cyclique mou et porte statique

Dans le régime `mu<0` fort, la configuration dominante est le sous-réseau pair occupé. Le doublet central de flux est relié par un processus de six hoppings.

Structure analytique :

```math
t_{loop}=O(J^6/|\mu|^5).
```

La qualification déjà divulguée montre une pente locale du gap tendant vers `-5`; cette observation est **design / qualification non confirmatoire**.

Le Hamiltonien effectif est :

```math
H_{eff}=E_cI+3g\delta\sigma_z+t_{loop}\sigma_x+\cdots.
```

Avec :

```math
x=6g\delta/gap_0,
```

les prédictions statiques du doublet sont :

```math
gap(\delta)/gap_0\simeq\sqrt{1+x^2},
```

```math
2\langle\Phi\rangle\simeq-\frac{x}{\sqrt{1+x^2}}
```

à convention de signe près.

Ces deux collapses statiques doivent précéder toute interprétation dynamique SOFT-LOOP. `Delta1` n'est pas contraint à suivre une courbe universelle exacte en `x`; un collapse de `Delta1` est seulement une hypothèse secondaire.

Échelle locale :

```math
\delta_c=gap_0/(6g).
```

La famille de dérivée utilise :

```math
h_k=\alpha_k\,\delta_c,
```

où les `alpha_k` sont préenregistrés après fermeture du budget numérique dynamique. Pour le contrôle `Lambda=2 -> 3`, les mêmes valeurs physiques `h_k`, générées à partir du gap `Lambda=2`, sont utilisées aux deux cutoffs.

---

## 13. Qualification de troncature déjà divulguée

Les mesures de saturation de bord `B_2=P(max|E|=2)` sont des indicateurs de **stress de troncature**, pas des estimations directes de l'erreur.

La qualification déjà vue indique notamment :

```text
g=1, mu=0, delta=0   -> cutoff très froid
g décroissant         -> pression de bord croissante
mu<0                  -> région plus tendue et gap plus faible
```

Le résidu de Ritz de l'état `Lambda=2` plongé dans `Lambda=3` est le diagnostic de design privilégié pour quantifier le couplage aux états omis lorsque ce contrôle est requis.

Le sous-ensemble exact de points `Lambda=3` de stress à exécuter reste à figer avant campagne confirmatoire.

---

## 14. Paramètres réellement OPEN avant gel

La liste suivante remplace les anciennes listes dispersées d'`OPEN` pour la phase de clôture.

### A. Contrôles temporels et précision

```text
BETA_REFINEMENT_VALUES
ROOT_SOLVER_TOLERANCES
ARGMAX_TOLERANCES
SPECTRAL_PRECISION_CONTROL
DELTA1_PROPAGATED_ERROR_BUDGET
```

### B. Dérivée SOFT-LOOP

```text
STATIC_X_CONTROL_VALUES
STATIC_COLLAPSE_NUMERICAL_CRITERION
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE
```

### C. Contrôles de fenêtre / interprétation

```text
ETA_GRID_AND_ADMISSIBLE_DOMAIN
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE
EPS_PATH_CONTROL_DOMAIN_AND_GRID
GAMMA_CONTROL_DOMAIN_AND_GRID
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS
```

### D. Campagne et troncature

```text
NEGATIVE_DELTA_ORACLE_SUBSET
TRUNCATION_STRESS_POINT_SUBSET
TRUNCATION_COMPARISON_TOLERANCES
```

### E. Verdict scientifique global

```text
ESTIMATOR_COHERENCE_CRITERION
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

Tous les autres anciens `OPEN` doivent être soit supprimés, soit reclassés explicitement comme `VALIDATED_FOR_FREEZE`, `QUALIFICATION_NONCONFIRMATORY`, `REJECTED` ou `BACKLOG` lors de la consolidation mécanique des deux sources principales.

---

## 15. Éléments explicitement clos qui ne doivent plus réapparaître comme OPEN

```text
ORDERED_RELATION_CONVENTION
    CLOSED_BY_K_RECIPROCITY

PARAMETER_CAMPAIGN_MAIN_GRID
    VALIDATED_FOR_FREEZE

TIME_INTERPOLATION_AS_FINAL_ESTIMATOR
    REJECTED

TIME_FINITE_DIFFERENCE_DERIVATIVES
    REJECTED

GLOBAL_FACTOR_TWO_FOR_ALL_EVENTS
    REJECTED

NEAR_CROSSING_GAP_THRESHOLD
    REMOVED; publish gap continuously instead

ZERO_GRADE_PATH_PURITY_CORRECTION
    NOT_REQUIRED; channel exactly inactive in 0B

RAW_EIGENVECTOR_NONZERO_COUNT_ORACLE
    REJECTED
```

---

## 16. Prochaine phase

Avant tout code 0B :

1. intégrer mécaniquement le présent état dans `specification.md` et `validation-plan.md` ;
2. faire un audit critique de clôture en lecture seule ;
3. classer chaque objection `BLOCKING`, `NON_BLOCKING_BACKLOG` ou `REJECTED` ;
4. fermer en un seul lot les paramètres numériques du §14 ;
5. effectuer une revue finale de cohérence et de syntaxe ;
6. soumettre le paquet à Lionel ORCIL pour décision explicite de gel ;
7. seulement après gel, autoriser le lot d'audit / implémentation 0B.

Claude Code conserve son rôle de challenge pendant l'implémentation. Une objection bloquante stoppe le lot et retourne à l'arbitrage conceptuel ; une amélioration non nécessaire à la validité est différée au backlog.
