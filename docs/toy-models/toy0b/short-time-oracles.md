# Toy Model 0B — support analytique des oracles de court temps

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne les conséquences analytiques de la symétrie antiunitaire `K` et du développement de Kubo à court temps. Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale précédant le gel final de 0B.

## 1. Parité temporelle imposée par K

Dans la base occupation-flux, `H`, `rho` et les occupations `n_i` sont réels pour la famille de fonds déclarée. La conjugaison complexe `K` vérifie donc :

```math
K H K^{-1}=H,
\qquad
K \rho K^{-1}=\rho,
\qquad
K n_i K^{-1}=n_i.
```

Comme `K` est antiunitaire :

```math
K i K^{-1}=-i,
\qquad
K n_q(t)K^{-1}=n_q(-t).
```

Pour :

```math
\chi_{pq}(t)=i\,\mathrm{Tr}\!\left(\rho[n_p,n_q(t)]\right),
```

on obtient :

```math
\chi_{pq}(-t)=-\chi_{pq}(t).
```

Par conséquent :

```math
\mathcal F_{pq}(t)=\chi_{pq}(t)^2/4
```

est paire en temps.

Le développement de `chi` ne contient que des puissances impaires :

```math
\chi_{pq}(t)=a_1t+a_3t^3+a_5t^5+\cdots.
```

## 2. Règle de sélection sur l'exposant d'état

La localité impose au niveau opératoriel :

```math
[n_p,\mathrm{ad}_H^r(n_q)]=0
\quad\text{pour}\quad r<d(p,q).
```

La parité temporelle ajoute, pour les fonds `K`-invariants, que les coefficients d'ordre pair sont nuls dans l'espérance de Kubo.

Le premier exposant d'état possible satisfait donc :

```math
\nu_{\rm state}
\ge
\min\{r\ge d(p,q)\mid r\text{ impair}\}.
```

Table structurelle :

```text
d = 1 -> nu_state >= 1
d = 2 -> nu_state >= 3
d = 3 -> nu_state >= 3
```

Pour les paires opposées `d=3`, si le coefficient d'ordre 3 s'annule par interférence des deux arcs minimaux, alors la règle de parité impose :

```text
nu_state >= 5
```

et non seulement `nu_state > 3`.

## 3. Relations non orientées

La stationnarité donne :

```math
\chi_{qp}(t)=-\chi_{pq}(-t).
```

Avec l'imparité temporelle imposée par `K` :

```math
\chi_{qp}(t)=\chi_{pq}(t).
```

Donc :

```math
\mathcal F_{qp}(t)=\mathcal F_{pq}(t),
```

et les temps `T_grow` et `T_thr(eta)` sont identiques sous échange de la source et du récepteur. Pour le protocole 0B, les relations `(p,q)` sont donc traitées comme non orientées.

## 4. Oracle linéaire sur une arête

Pour une arête `i -> i+1`, on définit :

```math
h_i=c_i^\dagger U_i c_{i+1},
\qquad
X_i=h_i+h_i^\dagger.
```

Le Hamiltonien contient le hopping `-J sum_i X_i`. On a :

```math
[n_i,[H,n_{i+1}]]=-JX_i.
```

Le développement de la réponse de Kubo donne alors :

```math
\chi_{i,i+1}(t)
=J\langle X_i\rangle_\rho\,t+O(t^3).
```

Avec la convention `J=1` :

```math
a_1^{(i,i+1)}=\langle X_i\rangle_\rho.
```

Cet oracle est calculable par diagonalisation et valeurs moyennes, sans évolution temporelle.

## 5. Oracle court-terme du contraste primaire

Lorsque les coefficients linéaires des deux orbites d'arête restent non nuls, `nu=1` pour ces canaux et :

```math
C_{\rm short}^{(1,A)}
=\left|\frac{\langle X\rangle_{A,\mathrm{state}}}
              {\langle X\rangle_{A,\mathrm{ref}}}\right|,
```

```math
C_{\rm short}^{(1,B)}
=\left|\frac{\langle X\rangle_{B,\mathrm{state}}}
              {\langle X\rangle_{B,\mathrm{ref}}}\right|.
```

À la référence `delta=0`, la réflexion échange les deux orbites et impose :

```math
\langle X\rangle_{A,\mathrm{ref}}
=
\langle X\rangle_{B,\mathrm{ref}}.
```

Donc :

```math
\Delta_1^{\rm short}(\delta)
=
\log\left|
\frac{\langle X\rangle_{A,\delta}}
     {\langle X\rangle_{B,\delta}}
\right|.
```

La covariance de réflexion implique également :

```math
\Delta_1^{\rm short}(-\delta)
=-\Delta_1^{\rm short}(\delta).
```

Cette identité constitue un oracle statique préalable au test dynamique end-to-end.

## 6. Gate de régularité court-terme

La formule précédente n'est applicable que si les coefficients linéaires concernés sont non nuls dans la référence et dans le fond comparé.

Si, pour une orbite d'arête :

```math
\langle X\rangle=0,
```

alors le terme linéaire s'annule et la règle de parité impose :

```text
nu_state >= 3
```

pour ce canal.

Le verdict est alors :

```text
EDGE_SHORT_ORACLE = NOT_APPLICABLE
```

et non `FAIL`. Le protocole dynamique peut rester actif ; il doit déterminer le nouvel exposant et appliquer les règles générales de comparaison des exposants.

La notion de zéro numérique et les tolérances restent `OPEN` jusqu'au gel des tolérances numériques.

## 7. Hiérarchie scientifique des quantités Delta1

La limite de petit seuil ne doit pas être présentée comme résultat de propagation. Elle reproduit un contraste de valeur moyenne du hopping dans le fond considéré.

La hiérarchie validée pour gel est :

```text
Delta1_short
    oracle algébrique / statique au sens calculable sans évolution
    aucune interprétation de temps d'arrivée

Delta1_thr(eta)
    famille complète de seuils finis
    doit tendre vers Delta1_short dans le régime asymptotique lorsque les exposants concordent

Delta1_dyn_thr(eta)
    = Delta1_thr(eta) - Delta1_short
    contraste de la partie quittant le régime court

Delta1_grow
    observable scientifique temporelle primaire
    extraite de la montée finie
```

En termes des corrections par paire :

```math
D_{pq}^{\rm thr}(\eta)
=
\log\frac{C_{\rm eff,pq}^{\rm thr}(\eta)}{C_{{\rm short},pq}},
```

on a, pour les deux orbites d'arête :

```math
\Delta_{1,\rm dyn}^{\rm thr}(\eta)
=
D_A^{\rm thr}(\eta)-D_B^{\rm thr}(\eta)
=
\Delta_1^{\rm thr}(\eta)-\Delta_1^{\rm short}.
```

Cette quantité n'est définie que lorsque les comparaisons `C_short` correspondantes sont elles-mêmes applicables.

## 8. Conséquence pour les seuils et fenêtres

Comme :

```math
\mathcal F(t)\sim t^{2\nu},
```

les départs minimaux sont :

```text
d=1 -> F(t) ~ t^2 si a1 != 0
d=2 -> F(t) ~ t^6 ou ordre supérieur
d=3 -> F(t) ~ t^6 ou ordre supérieur
```

Pour un régime asymptotique `F ~ B t^(2 nu)` :

```math
T_{\rm thr}(\eta)\sim(\eta/B)^{1/(2\nu)}.
```

Donc la sensibilité logarithmique au seuil est :

```math
\frac{d\log T_{\rm thr}}{d\log\eta}=\frac1{2\nu}.
```

Les canaux `nu=3` sont ainsi moins sensibles fractionnellement à `eta` que les canaux `nu=1`. Leur temps absolu de franchissement n'est toutefois pas ordonné par cette seule loi, car le coefficient `B` dépend du canal et du fond.

Le protocole devra donc définir des domaines admissibles de `eta` et des validations de fenêtre séparés par classe de relation / exposant, tout en utilisant un domaine commun par intersection lorsque plusieurs courbes sont comparées dans un même contraste.

### Grille eta préenregistrée (référence)

Le protocole 0B utilise la grille absolue préenregistrée, paramétrée par
`lambda_eta=2 sqrt(eta)` :

```text
LAMBDA_ETA_VALUES = {2^-2,2^-4,2^-6,2^-8,2^-10,2^-12,2^-14,2^-16}
ETA_VALUES         = {2^-6,2^-10,2^-14,2^-18,2^-22,2^-26,2^-30,2^-34}
ETA_GRID_TYPE       = ABSOLUTE_F_LEVELS
ETA_AMPLITUDE_GRID   = DYADIC_IN_2SQRTETA
ETA_AMPLITUDE_RATIO  = 4
```

Ces niveaux sont des niveaux de réponse absolus communs (§18 de
`specification.md`, §27 de `temporal-event-solver.md` pour l'admissibilité
détaillée).

Pour `nu=5`, la plage lambda complète donne une plage de temps de seuil
potentielle :

```math
2^{14/5}\approx6.96.
```

Cette plage (`ETA_POTENTIAL_LAMBDA_DYNAMIC_RANGE = 2^14`) est **potentielle
seulement** : elle n'est pas garantie de survivre à l'admissibilité commune
(intersection sur la fermeture de dépendance complète de §27 de
`temporal-event-solver.md`). Le protocole opérationnel de convergence qui
exploite cette grille est défini en §10 ci-dessous
(`SHORT_TIME_THRESHOLD_CONVERGENCE_RULE = VALIDATED_FOR_FREEZE`). Une plage
insuffisante doit être signalée après exécution confirmatoire, jamais
réparée post hoc par ajout ou substitution de niveaux.

## 9. Borne structurelle globale sur l'amplitude de réponse

Pour `n_i` à valeurs de projecteur :

```math
Var(n_i)\le\frac14.
```

Avec :

```math
\chi_{pq}(t)=-2\,Im\langle\delta n_p\,\delta n_q(t)\rangle,
```

Cauchy-Schwarz donne :

```math
|\chi_{pq}(t)|\le2\sqrt{Var(n_p)Var(n_q)}\le\frac12.
```

Donc :

```math
F_{pq}(t)=\frac{\chi_{pq}(t)^2}{4}
```

satisfait :

```math
\boxed{
F_{pq}(t)\le Var(n_p)Var(n_q)\le\frac1{16}.
}
```

```text
THRESHOLD_GLOBAL_F_BOUND = STRUCTURAL_ANALYTIC
THRESHOLD_GLOBAL_F_MAX   = 1/16
```

Ceci **raffine**, sans le contredire ni le remplacer, l'oracle générique déjà
validé `0<=F<=1` (`specification.md` §8-9, `validation-plan.md` §7). Il ne
rouvre aucun bloc gelé.

## 10. Règle opérationnelle de convergence court-terme

Cette section définit `SHORT_TIME_THRESHOLD_CONVERGENCE_RULE`. Elle distingue
strictement :

- le théorème/oracle analytique (§10.1) : conséquence exacte de la structure
  `K`-réelle/temps impair déjà validée ;
- le protocole opérationnel numérique de convergence (§10.2-§10.6, §10.9-§10.14)
  ;
- le mode plancher numérique (§10.6, branche A) ;
- le mode plancher-après-contraction (§10.7, branche B) ;
- le mode Richardson résolu (§10.8, branche C).

Aucun de ces modes numériques n'est lui-même un oracle analytique.

### 10.1 Cible analytique

Pour la famille `K`-réelle déjà supposée en 0B (§1) :

```math
\chi(t)=a_\nu t^\nu+a_{\nu+2}t^{\nu+2}+\cdots
```

ne contient que des puissances impaires.

Pour une référence/état de MÊME exposant impair dominant certifié `nu` :

```math
C_{short}=|a_{state}/a_{ref}|^{1/\nu}.
```

Définir :

```math
D_{pq}^{thr}(\eta)=\log\!\left[\frac{C_{eff,pq}^{thr}(\eta)}{C_{short,pq}}\right].
```

Avec `lambda_eta=2 sqrt(eta)`, l'inversion analytique donne :

```math
D_{pq}^{thr}(\lambda)=O(\lambda^{2/\nu}).
```

Définir :

```math
z=\lambda^{2/\nu}.
```

Alors :

```math
D(z)=c_1z+c_2z^2+O(z^3).
```

```text
SHORT_TIME_CONVERGENCE_TARGET                = D_PQ_THR_TO_ZERO
SHORT_TIME_CONVERGENCE_ASYMPTOTIC_COORDINATE = lambda_eta^(2/nu)
```

Ce développement, et l'absence de termes en puissance demi-entière, reposent
sur la structure `K`-réelle/temps impair déjà validée (§1). Il n'est pas
revendiqué hors de cette famille.

### 10.2 Domaine en exposant dominant

L'usage confirmatoire exige :

- référence et état ont le MÊME exposant dominant certifié ;
- les coefficients dominants requis sont certifiés non nuls ;
- `nu in {1,3,5}`.

Si les exposants diffèrent :

```text
SHORT_TIME_COMPARISON = NOT_APPLICABLE
D_THR                 = NOT_DEFINED
SHORT_TIME_CONVERGENCE_NOT_APPLICABLE
```

Si la classification d'exposant est non résolue :

```text
SHORT_TIME_CONVERGENCE_EXPONENT_UNRESOLVED
```

Si `nu > 5` :

```text
SHORT_TIME_CONVERGENCE_RANGE_NOT_PREREGISTERED
```

Ces trois cas sont `NONCONFIRMATORY`.

Les classifications de zéro/non-zéro numérique restent conditionnées à
`NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES`, qui reste `OPEN`.

### 10.3 Budget de résidu numérique

À la précision acceptée `q in {p,2p}` :

```math
S_{short}^{(q)}=\frac1\nu\log\left|\frac{a_{state}^{(q)}}{a_{ref}^{(q)}}\right|,
```

```math
L_{thr}^{(q)}(\eta)=\log\!\left[\frac{T_{ref}^{(q)}(\eta)}{T_{state}^{(q)}(\eta)}\right],
```

```math
D^{(q)}(\eta)=L_{thr}^{(q)}(\eta)-S_{short}^{(q)}.
```

Pour chaque événement de seuil, réutiliser (déjà validés,
`temporal-event-solver.md`) :

```math
r_T=e_u/u,\qquad r_T<1,\qquad L(r)=-\log(1-r).
```

Pour une paire ref/état :

```math
e_L(\eta)=L(r_{T,ref})+L(r_{T,state}).
```

Proxy de précision de l'oracle court :

```math
e_S=|S_{short}^{(2p)}-S_{short}^{(p)}|.
```

Écart complet de doublement de précision :

```math
d_D=|D^{(2p)}-D^{(p)}|.
```

Budget de résidu conservatif normatif :

```math
\boxed{
e_D(\eta)=\max\bigl(d_D,\;e_L(\eta)+e_S\bigr).
}
```

Utiliser `D(eta)=D^(2p)(eta)`. Définir :

```math
I_D=[D-e_D,D+e_D],
\qquad
m_D=\max(0,|D|-e_D),
\qquad
M_D=|D|+e_D.
```

Un résidu est `RESOLVED` ssi `m_D>0`. Son signe est certifié par l'intervalle
correspondant excluant zéro.

Aucune nouvelle tolérance numérique scalaire n'est introduite.

### 10.4 Queue commune

Utiliser uniquement le domaine `eta` commun admissible déjà validé
(fermeture complète de dépendance, `temporal-event-solver.md` §27) pour la
quantité publiée considérée.

```text
SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS = 3
```

Sélectionner déterministiquement les TROIS plus petites valeurs `lambda`
communes admissibles :

```math
\lambda_0>\lambda_1>\lambda_2
```

où `lambda_2` est le seuil le plus profond/le plus petit.

Aucune sélection sélective : pas de saut d'un niveau admissible plus profond,
pas de triplet intérieur plus « propre », pas de substitution d'`eta`, pas de
nouvel `eta`.

Pour `nu<=5`, trois niveaux préenregistrés adjacents couvrent au moins :

```math
16^{2/5}\approx3.03
```

en `z=lambda^(2/nu)`.

Publier le triplet `lambda`, le triplet `z`, `q_01=z_1/z_0`, `q_12=z_2/z_1` et
la plage `z` totale.

### 10.5 Branchement information-monotone

Soit :

```math
R_i:=(m_{D,i}>0).
```

La classification de convergence DOIT être monotone en contenu
d'information. Une queue attendue de contraction vers zéro doit avoir un
préfixe résolu contigu suivi, éventuellement, d'un suffixe de plancher
numérique.

Tout motif non contigu tel que :

- non résolu -> résolu ;
- résolu -> non résolu -> résolu ;

est :

```text
SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE.
```

Aucun point résolu ne peut réapparaître après que la queue est entrée dans le
plancher.

### 10.6 Branche A — aucun résidu résolu

Si :

```text
R_0 = FALSE
R_1 = FALSE
R_2 = FALSE
```

publier :

```text
SHORT_TIME_CONVERGENCE_NO_RESOLVED_RESIDUAL
```

Statut épistémique :

```text
NONCONFIRMATORY_INSUFFICIENT_RESOLUTION
```

Interprétation : les trois résidus sont compatibles avec zéro, mais aucune
tendance de contraction n'a jamais été numériquement résolue. C'est une
évidence plus faible qu'une contraction suivie d'une entrée dans le plancher.
Non éligible au verdict agrégé fort de `Delta1`.

### 10.7 Branche B — plancher supporté après contraction

```text
SHORT_TIME_CONVERGENCE_SUPPORTED_FLOOR_AFTER_CONTRACTION
```

C'est un statut fort de compatibilité avec la limite court-terme. Il
supporte la revendication de limite vers zéro, mais NE supporte PAS une
revendication résolue sur le taux de convergence asymptotique une fois le
plancher atteint.

Sous-cas B1 : `R_0=TRUE, R_1=TRUE, R_2=FALSE`. Exiger :

- `I_D,0` et `I_D,1` ont le même signe certifié ;
- `M_D,1 < m_D,0` ;
- `M_D,2 < m_D,1`.

Sous-cas B2 : `R_0=TRUE, R_1=FALSE, R_2=FALSE`. Exiger :

- `M_D,1 < m_D,0` ;
- `M_D,2 < M_D,1`.

Si les conditions pertinentes passent :

```text
SHORT_TIME_CONVERGENCE_SUPPORTED_FLOOR_AFTER_CONTRACTION
```

Sinon :

```text
SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE
```

Publier :

```text
SHORT_TIME_CONVERGENCE_SUPPORT_MODE = FLOOR_AFTER_CONTRACTION
```

Ne pas inférer `c1`, `c2`, ni un taux résolu depuis cette branche.

### 10.8 Branche C — tendance de Richardson pleinement résolue

Si `R_0=R_1=R_2=TRUE`, exiger :

1. les trois intervalles signés ont le MÊME signe certifié ;
2. contraction certifiée : `M_D,1 < m_D,0` ET `M_D,2 < m_D,1`.

Avec `z_i=lambda_i^(2/nu)`, `q_01=z_1/z_0`, `q_12=z_2/z_1` :

```math
R_{01}=\frac{D_1-q_{01}D_0}{1-q_{01}},
\qquad
R_{12}=\frac{D_2-q_{12}D_1}{1-q_{12}}.
```

Budgets :

```math
e_{R01}=\frac{e_{D,1}+q_{01}e_{D,0}}{1-q_{01}},
\qquad
e_{R12}=\frac{e_{D,2}+q_{12}e_{D,1}}{1-q_{12}}.
```

Définir :

```math
m_{R12}=\max(0,|R_{12}|-e_{R12}),
\qquad
M_{shift}=|R_{12}-R_{01}|+e_{R12}+e_{R01}.
```

Exiger :

```math
m_{R12}\le M_{shift}.
```

Si toutes les conditions passent :

```text
SHORT_TIME_CONVERGENCE_SUPPORTED_RESOLVED_TREND
```

Publier :

```text
SHORT_TIME_CONVERGENCE_SUPPORT_MODE = RESOLVED_RICHARDSON_TREND
```

Si le signe, la contraction ou la compatibilité-zéro de Richardson échoue :

```text
SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE
```

Aucune revendication que `M_shift` est une borne de troncature rigoureuse.

### 10.9 Ensemble de statuts forts

```text
SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET =
{
SHORT_TIME_CONVERGENCE_SUPPORTED_RESOLVED_TREND,
SHORT_TIME_CONVERGENCE_SUPPORTED_FLOOR_AFTER_CONTRACTION
}
```

Les deux statuts supportent la compatibilité avec `D_pq^thr -> 0`. Seul
`SUPPORTED_RESOLVED_TREND` supporte une revendication numériquement résolue
sur la tendance asymptotique.

### 10.10 Autres issues non confirmatoires

Moins de 3 niveaux `eta` communs admissibles :

```text
SHORT_TIME_CONVERGENCE_INSUFFICIENT_COMMON_RANGE
```

Dépendance d'événement/précision/exposant non résolue :

```text
SHORT_TIME_CONVERGENCE_NUMERICALLY_INCONCLUSIVE
```

ou

```text
SHORT_TIME_CONVERGENCE_EXPONENT_UNRESOLVED
```

selon le cas.

Motif de résolution non contigu, ou échec de contraction/signe/Richardson :

```text
SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE
```

Comparaison structurellement non applicable :

```text
SHORT_TIME_CONVERGENCE_NOT_APPLICABLE
```

`nu>5` :

```text
SHORT_TIME_CONVERGENCE_RANGE_NOT_PREREGISTERED
```

Ces statuts sont `NONCONFIRMATORY`. `CONTROL_SENSITIVE` n'est jamais présenté
comme une falsification physique de l'oracle analytique de court terme.

### 10.11 Traitement par paire avant `Delta1`

Pour le contraste d'orbites primaire, évaluer séparément :

```text
D_A^thr
D_B^thr
```

Une revendication forte :

```math
\Delta_1^{thr}\to\Delta_1^{short}
```

exige que LES DEUX canaux par paire appartiennent à
`SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET`. Alors :

```text
DELTA1_SHORT_LIMIT = SUPPORTED
```

Une annulation `D_A-D_B~=0` ne peut jamais sauver un résultat par paire non
confirmatoire.

```text
SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY = YES
DELTA1_CANCELLATION_AS_PRIMARY_EVIDENCE = REJECTED
```

`Delta1_dyn^thr=D_A-D_B` reste SECONDAIRE.

### 10.12 Agrégation complète de `Delta1`

Pour les canaux par paire requis A et B :

```text
1. si LES DEUX sont dans SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET :
       DELTA1_SHORT_LIMIT = SUPPORTED

2. sinon si l'un est SHORT_TIME_CONVERGENCE_NOT_APPLICABLE
   ou SHORT_TIME_CONVERGENCE_RANGE_NOT_PREREGISTERED :
       DELTA1_SHORT_LIMIT = NOT_APPLICABLE

3. sinon si l'un est SHORT_TIME_CONVERGENCE_INSUFFICIENT_COMMON_RANGE :
       DELTA1_SHORT_LIMIT = INSUFFICIENT_COMMON_RANGE

4. sinon si l'un est SHORT_TIME_CONVERGENCE_CONTROL_SENSITIVE :
       DELTA1_SHORT_LIMIT = CONTROL_SENSITIVE

5. sinon :
       DELTA1_SHORT_LIMIT = NONCONFIRMATORY
```

Aucune paire mixte ne peut être promue silencieusement à `SUPPORTED`.

### 10.13 Statut local par cutoff

À chaque `Lambda` séparément, un statut local de convergence peut être
calculé en utilisant le domaine commun admissible complet propre à ce
cutoff. Le publier.

Pour une revendication de stabilité inter-cutoff, ces queues locales
indépendamment sélectionnées sont `LOCAL_DIAGNOSTIC_ONLY`, sauf si elles
coïncident avec la queue commune conjointe entre cutoffs définie ci-dessous.
Elles ne peuvent pas, à elles seules, supporter une revendication de
stabilité de cutoff.

### 10.14 Queue conjointe de stabilité de cutoff

Pour une revendication publiée `Q` comparant `Lambda=2` et `Lambda=3`,
appliquer D'ABORD l'invariant de fermeture de dépendance déjà validé :

```math
E_\eta^{joint\_cutoff}(Q)
=
\bigcap\text{(eta préenregistrés numériquement admissibles à \(\Lambda=2\) ET \(\Lambda=3\), pour chaque membre comparé)}.
```

Seulement ensuite, sélectionner les TROIS plus petites valeurs `lambda` de
`E_eta^joint_cutoff(Q)`.

Utiliser exactement cette MÊME queue à trois niveaux pour évaluer la règle de
convergence par paire à `Lambda=2` et à `Lambda=3`.

Une revendication de limite court-terme stable au cutoff exige, sur cette
même queue :

- `D_A` fort à `Lambda=2` ;
- `D_B` fort à `Lambda=2` ;
- `D_A` fort à `Lambda=3` ;
- `D_B` fort à `Lambda=3`.

Si les quatre sont forts :

```text
CUTOFF_STABLE_SHORT_TIME_CONVERGENCE = SUPPORTED
```

Si l'intersection conjointe contient moins de 3 niveaux :

```text
CUTOFF_STABLE_SHORT_TIME_CONVERGENCE = INSUFFICIENT_COMMON_RANGE
```

Sinon, propager les statuts non confirmatoires fail-closed.

Ceci ne ferme PAS `TRUNCATION_COMPARISON_TOLERANCES`, qui reste `OPEN`.

### 10.15 Publication diagnostique

Pour chaque queue de convergence par paire, publier :

```text
nu
lambda_0, lambda_1, lambda_2
z_0, z_1, z_2
q_01, q_12
D_0, D_1, D_2
e_D,0, e_D,1, e_D,2
m_D,i / M_D,i
motif résolu/non résolu
mode/statut de support
```

Pour `RESOLVED_RICHARDSON_TREND`, publier en plus :

```text
R_01
R_12
e_R01
e_R12
m_R12
M_shift
```

et énoncer :

```text
RICHARDSON_ZERO_COMPATIBILITY =
OPERATIONAL_COMPATIBILITY_NOT_RIGOROUS_TRUNCATION_BOUND
```

Pour tous les résultats supportés, publier la plage `z` effective et les
facteurs de contraction observés.

Contraction dominante attendue par pas de grille `lambda` :

- facteur `16` pour `nu=1` ;
- facteur `4^(2/3)~=2.52` pour `nu=3` ;
- facteur `4^(2/5)~=1.74` pour `nu=5`.

Un verdict de convergence `nu=1` typique peut n'avoir exactement que les
trois niveaux minimaux ; la perte d'un niveau donne
`INSUFFICIENT_COMMON_RANGE`, pas une réparation post hoc de la grille.

### 10.16 Statut

```text
SHORT_TIME_THRESHOLD_CONVERGENCE_RULE        = VALIDATED_FOR_FREEZE
SHORT_TIME_CONVERGENCE_TARGET                = D_PQ_THR_TO_ZERO
SHORT_TIME_CONVERGENCE_ASYMPTOTIC_COORDINATE = lambda_eta^(2/nu)
SHORT_TIME_CONVERGENCE_MIN_COMMON_LEVELS     = 3
SHORT_TIME_CONVERGENCE_MAX_PREREGISTERED_NU  = 5
SHORT_TIME_CONVERGENCE_PAIRWISE_PRIMARY      = YES
DELTA1_CANCELLATION_AS_PRIMARY_EVIDENCE      = REJECTED

SHORT_TIME_CONVERGENCE_STRONG_STATUS_SET =
{
SUPPORTED_RESOLVED_TREND,
SUPPORTED_FLOOR_AFTER_CONTRACTION
}

SHORT_TIME_CONVERGENCE_NEW_SCALAR_TOLERANCE = NONE

NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
TRUNCATION_COMPARISON_TOLERANCES       = OPEN
```
