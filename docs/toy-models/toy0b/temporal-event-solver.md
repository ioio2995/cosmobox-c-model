# Toy Model 0B — solveur spectral continu des événements temporels

Statut : **validé pour gel en principe — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `event-bandwidth-bracketing.md`, `derivative-error-budget.md`, `derivative-control.md`, `recurrence-control.md`

Ce document fixe l'architecture numérique de principe pour l'extraction des temps caractéristiques. Les valeurs de tolérance et la famille de raffinement restent ouvertes.

## 1. Évaluateur spectral exact en temps

Pour l'état canonique stationnaire et les densités réelles :

```math
\chi_{pq}(t)
=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
```

Les dérivées de `chi` sont obtenues analytiquement terme à terme. Pour :

```math
F(t)=\frac{\chi(t)^2}{4},
```

on dispose également exactement en temps de :

```math
F'=\frac12\chi\chi',
```

```math
F''=\frac12(\chi'^2+\chi\chi''),
```

et des dérivées supérieures.

Donc :

```text
TIME_GRID_AS_FINAL_ESTIMATOR       = REJECTED
FINITE_DIFFERENCE_TIME_DERIVATIVE  = REJECTED
```

## 2. Rôle du bracketing

Une grille / stratégie d'échantillonnage sert uniquement à :

- isoler les cellules pouvant contenir les premiers événements ;
- exclure les cellules antérieures sans événement ;
- construire les brackets des solveurs continus ;
- fournir des diagnostics et figures.

Les temps finaux sont toujours obtenus par évaluation continue de la somme spectrale.

```text
TIME_SAMPLING = BRACKETING_CONTROL
```

## 3. Famille de raffinement commune et facteur analytique par estimateur

Une seule famille sans dimension :

```math
\mathcal B=\{\beta_1>\beta_2>\cdots>\beta_K>0\}
```

est préenregistrée.

Avec une borne spectrale conservative `Omega_scale`, la taille nominale d'une cellule vaut :

```math
\Delta t_k^{(event)}
=\beta_k\frac{\pi}{s_{event}\Omega_{scale}},
```

avec :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

conformément aux réductions exactes décrites dans `event-bandwidth-bracketing.md`.

Les `beta_k` sont communs à tous les estimateurs. Le facteur `s_event` n'est pas ajustable : il est fixé analytiquement par la fonction effectivement résolue.

Valeurs préenregistrées :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}
```

`beta` contrôle uniquement le maillage initial de certification / bracketing ; ce n'est pas une tolérance sur le temps final, obtenu par le solveur spectral continu. `beta=1` correspond à une demi-période de la bande maximale de la fonction de certification ; raffinement dyadique imbriqué ; `beta=1/8` donne une phase maximale `pi/8` par cellule à la bande limite. Aucune finesse supplémentaire n'est requise comme garantie de complétude, celle-ci reposant sur l'exclusion certifiée des cellules, leur subdivision adaptative et le solveur continu.

Critère de contrôle sous raffinement : identité du premier événement stable, ordre des candidats pertinents stable, aucune cellule antérieure non résolue, temps continus compatibles selon les tolérances numériques (`OPEN`). Sinon : `TIME_EVENT_CONTROL_SENSITIVE`.

## 4. Certification de T_peak par chi'

Scientifiquement, `T_peak` reste le premier `t>0` où `F'` passe de positif à négatif.

Comme :

```math
F'=\frac12\chi\chi',
```

et qu'un zéro de `chi` est un minimum de `F`, le premier pic strict avec `chi != 0` est localisé par une racine qualifiante de :

```math
\boxed{\chi'(t)=0.}
```

Le protocole doit :

1. certifier qu'aucune racine qualifiante antérieure de `chi'` n'a été manquée ;
2. résoudre `chi'(t)=0` dans la première cellule candidate ;
3. vérifier `chi(T_peak) != 0` au niveau de résolution déclaré ;
4. pour un maximum non dégénéré, vérifier :

```math
\boxed{\chi(T_{peak})\chi''(T_{peak})<0;}
```

5. dans les cas dégénérés où `chi''=0`, revenir à la définition scientifique par changement de signe de `F'` et/ou examiner les dérivées supérieures.

La condition `chi != 0` et `chi'' != 0` n'est pas suffisante à elle seule : `chi chi'' > 0` correspond à un minimum local non nul de `F`.

## 5. Certification de T_thr et T_down par croisement de niveau de chi

Pour `eta>0` :

```math
F=\eta
\quad\Longleftrightarrow\quad
|\chi|=2\sqrt\eta.
```

Sur le premier lobe, `chi` conserve un signe `s` fixé par le premier coefficient court non nul. On résout donc :

```math
\boxed{\chi(t)-s\,2\sqrt\eta=0.}
```

- `T_thr(eta)` : première racine ascendante avant `T_peak` ;
- `T_down(eta)` : première racine descendante après `T_peak` appartenant au même premier lobe.

Le signe de `chi'` au voisinage de la racine distingue montée et descente.

Cette réduction est retenue pour la certification parce qu'elle évite la convolution spectrale de `F`, fournit des bornes directes sur `chi` et simplifie le modèle d'erreur spectral. Elle n'est pas revendiquée comme intrinsèquement mieux conditionnée que l'équation équivalente `F-eta=0`.

## 6. T_grow

`T_grow` est l'infimum de l'ensemble des maximiseurs globaux de :

```math
F'(t)=\frac12\chi\chi'
```

sur `(0,T_peak)`.

Les candidats intérieurs satisfont :

```math
\boxed{
H_{grow}(t)
:=\chi'(t)^2+\chi(t)\chi''(t)
=0.
}
```

La stratégie nominale est :

- isoler toutes les cellules pouvant contenir une racine de `H_grow` dans `(0,T_peak)` ;
- résoudre les candidats continûment ;
- vérifier leur caractère maximal pour `F'` ;
- comparer les valeurs de `F'` de tous les candidats ;
- choisir le premier maximiseur global conformément à la définition scientifique.

`H_grow` contient des fréquences jusqu'à `2 Omega_chi`; c'est pourquoi `s_grow=2`.

De plus :

```math
H_{grow}'=3\chi'\chi''+\chi\chi'''=2F'''.
```

Avec :

```math
S_r=\sum_\omega |C_\omega|\omega^r,
```

une borne sûre est :

```math
\boxed{
\sup|H_{grow}'|
\le3S_1S_2+S_0S_3.
}
```

La certification de `T_grow` est donc potentiellement plus coûteuse non seulement par le facteur de bande deux, mais aussi par cette borne composite plus lâche.

Si plusieurs maxima sont quasi-égaux au niveau de l'incertitude numérique, l'identité de `T_grow` est conditionnée et doit être signalée.

## 7. Exclusion certifiable de cellules

Pour une fonction de certification `g(t)`, si sur une cellule centrée en `t_c` de demi-largeur `h` :

```math
L\ge\sup_{cell}|g'(t)|
```

et :

```math
|g(t_c)|>Lh,
```

alors aucune racine de `g` ne se trouve dans la cellule.

Les fonctions nominales sont :

```text
peak      -> g = chi'
threshold -> g = chi - s 2 sqrt(eta)
down      -> g = chi - s 2 sqrt(eta)
grow      -> g = H_grow
```

Les cellules non exclues sont subdivisées ou résolues explicitement. Une simple recherche de changements de signe ne suffit pas pour les racines tangentielles.

## 8. Pas d'interpolation comme estimateur scientifique

Une interpolation de grille peut servir à la visualisation ou à proposer une cellule initiale.

Elle ne fournit jamais le temps final publié lorsque l'évaluateur spectral est disponible.

```text
INTERPOLATION_AS_FINAL_TIME_ESTIMATOR = REJECTED
CONTINUOUS_ROOT_SOLVER                = REQUIRED
```

## 9. Contrôle de résolution du premier événement

Le protocole doit vérifier sous raffinement de la famille `B` que :

```text
- l'identité du premier événement est stable ;
- les cellules candidates se stabilisent ;
- les cellules antérieures sont exclues ou résolues ;
- le solveur continu retourne le même événement.
```

Si l'identité change sous raffinement :

```text
TIME_EVENT_CONTROL_SENSITIVE
```

jusqu'à résolution suffisante.

## 10. Conditionnement des événements

Pour une racine simple `g(t*)=0`, le déplacement au premier ordre est :

```math
|\delta t_*|
\sim
\frac{|\delta g(t_*)|}{|g'(t_*)|}.
```

Le protocole doit donc associer à chaque pente locale une borne ou estimation de l'erreur sur la fonction résolue. Une pente brute n'est pas un nombre de conditionnement invariant.

Les pentes disponibles sont :

```text
T_thr/down -> |chi'|
T_peak     -> |chi''|
T_grow     -> |H_grow'|
```

mais le diagnostic de précision sur le temps est de la forme :

```text
error_on_root_function / root_slope
```

avec un modèle d'erreur cohérent issu des perturbations spectrales.

Les formulations équivalentes en `F` ont le même conditionnement local si leurs erreurs sont propagées depuis les mêmes perturbations sous-jacentes. En particulier, le facteur `sqrt(eta)` des seuils multiplie simultanément pente et erreur et ne constitue pas une pénalité intrinsèque.

## 11. Budget spectral dynamique

L'erreur globale ne doit pas être identifiée à l'epsilon machine.

Le protocole numérique devra contrôler au minimum :

```text
- résidus des paires propres / projecteurs ;
- défaut d'orthogonalité ;
- stabilité des fréquences et poids spectraux sous précision / solveur ;
- accumulation de phase delta_omega * t ;
- annulations dans les sommes trigonométriques ;
- erreur propagée sur la fonction de racine ;
- pente locale de la fonction de racine ;
- conditionnement de l'argmax de T_grow.
```

La stabilité sous augmentation de précision peut être utilisée comme contrôle numérique indépendant, avec une règle uniforme préenregistrée.

## 12. Propagation vers Delta1

Les contrastes utilisent des logarithmes de rapports de temps. Pour une petite erreur :

```math
\delta\log T\simeq\frac{\delta T}{T}.
```

Le budget d'erreur de `Delta_1` doit être dérivé des erreurs des temps entrant dans chaque estimateur (`grow`, `thr`) et de leurs corrélations éventuelles.

Cette propagation est nécessaire avant le choix de `alpha_min` dans `A_delta`.

## 13. Troncature

Les mêmes `beta_k`, règles de certification, solveurs, diagnostics de conditionnement et tolérances sont utilisés à :

```text
Lambda=2
Lambda=3
```

sur les points soumis au contrôle de troncature.

Il est interdit d'améliorer sélectivement un cutoff après inspection pour restaurer la convergence.

## 14. Statut

```text
FINITE_SINE_TIME_EVALUATOR             = VALIDATED_FOR_FREEZE
TIME_GRID_AS_FINAL_ESTIMATOR           = REJECTED
TIME_GRID_AS_BRACKETING_CONTROL        = VALIDATED_FOR_FREEZE
COMMON_BETA_REFINEMENT_FAMILY          = VALIDATED_FOR_FREEZE
PEAK_SOLVED_VIA_CHI_PRIME              = VALIDATED_FOR_FREEZE
THRESHOLDS_SOLVED_VIA_CHI_LEVEL        = VALIDATED_FOR_FREEZE
GROW_SOLVED_VIA_HGROW                  = VALIDATED_FOR_FREEZE
PEAK_NONDEGENERATE_CRITERION           = chi*chi'' < 0
GLOBAL_FACTOR_TWO_FOR_ALL_EVENTS       = REJECTED
ESTIMATOR_SPECIFIC_BAND_FACTOR         = VALIDATED_FOR_FREEZE
SPECTRAL_CELL_EXCLUSION                = VALIDATED_IN_PRINCIPLE
CONTINUOUS_ROOT_SOLVER                 = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
CONTINUOUS_ARGMAX                      = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
INTERPOLATION_ROOT_FINDING_FINAL       = REJECTED
ROOT_SLOPE_ALONE_IS_CONDITION_NUMBER   = REJECTED
ERROR_NORMALIZED_ROOT_CONDITIONING     = VALIDATED_FOR_FREEZE
SQRT_ETA_CONDITIONING_PENALTY          = REJECTED
HGROW_DERIVATIVE_BOUND                 = 3 S1 S2 + S0 S3
GROW_COMPOSITE_CERTIFICATION_COST      = VALIDATED_FOR_FREEZE
BRACKETING_REFINEMENT_VALUES           = VALIDATED_FOR_FREEZE
ROOT_SOLVER_TOLERANCES                 = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCES                      = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCE                       = 1e-10
SPECTRAL_PRECISION_CONTROL             = VALIDATED_FOR_FREEZE
DELTA1_PROPAGATED_ERROR_BUDGET         = VALIDATED_FOR_FREEZE
SAME_NUMERICAL_RULES_ACROSS_CUTOFFS    = MANDATORY
SIMPLE_ROOT_CONTROL                   = VALIDATED_FOR_FREEZE
```

## 15. Backward gate

```math
E_{bar} = Tr(H)/d
```

```math
H_s = \max(J, \|H-E_{bar} I\|_2), \quad J = 1
```

```math
R = HV - V \Lambda
```

```math
r_H = \|R\|_2 / H_s, \quad r_{orth} = \|V^\dagger V - I\|_2
```

Critères :

```text
r_H <= 1e-12
r_orth <= 1e-12
BACKWARD_ERROR_PASS != FORWARD_SPECTRAL_PASS
```

## 16. Clustering numérique

```math
\epsilon_H = H_s (r_H + r_{orth})
```

```math
I_i = [E_i - \epsilon_H, E_i + \epsilon_H]
```

Frontière résolue si :

```math
E_{i+1} - E_i > 2 \epsilon_H
```

Les composantes de recouvrement définissent les clusters numériques.

```text
Cluster numérique != dégénérescence physique
Aucune fréquence représentative
```

## 17. Stabilité des projecteurs

```math
P_C = \sum_{i \in C} |v_i\rangle\langle v_i|
```

```math
d_P = \max_C \|P_C^{(2p)} - P_C^{(p)}\|_2
```

Critère :

```text
d_P <= 1e-10
```

Si un cluster basse précision se scinde, comparer avec la somme des projecteurs haute précision couvrant le même sous-espace.

Échec d'appariement :

```text
SPECTRAL_CLUSTER_UNRESOLVED
```

## 18. Poids

```math
C_C^{(pq)} = -(2/d_{GS}) Tr(P_{GS} n_p P_C n_q)
```

```math
d_C = \frac{\sum_C |C_C^{(2p)} - C_C^{(p)}|}{\max(1, \sum_C |C_C^{(2p)}|)}
```

Critère :

```text
d_C <= 1e-10
```

```text
C_C est un diagnostic signé, pas une borne d'amplitude
```

## 19. Dynamique de cluster

```math
\chi_C^{(pq)}(t) = -(2/d_{GS}) Tr\left[ P_{GS} n_p P_C \sin((H-E_0 I)t) P_C n_q \right]
```

Verdict :

```text
CLUSTER_COLLAPSE_FOR_DYNAMICS = REJECTED
```

## 20. Précision

Niveaux de précision :

```text
P0 = 53 bits
P1 >= 106 bits
P2 >= 212 bits
```

À chaque précision `p` :

```math
H^{(p)}
```

doit être réassemblé directement à cette précision.

Règles de stabilité :

```text
P0/P1 stable -> PRECISION_STABLE
sinon P2

P1/P2 stable -> PRECISION_ESCALATED
sinon -> PRECISION_UNRESOLVED
```

```text
PRECISION_UNRESOLVED interdit un verdict confirmatoire dépendant
```

## 21. Coordonnée d'événement

```math
u_e = \frac{s_{event} \Omega_{safe} t}{\pi}
```

avec :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
Omega_safe = E_{max} - E_0
```

Pour comparer `p/2p`, utiliser le même `Omega_safe` haute précision.

## 22. Solveur

```text
tau_root = 1e-12
```

```math
w_u \le 2 \tau_{root} \max(1, |\hat{u}|)
```

```math
\epsilon_{u,solver} = w_u / 2
```

## 23. Racine simple — erreur forward

```math
\epsilon_{g,spec}(t) = |g^{(2p)}(t) - g^{(p)}(t)|
```

```math
\epsilon_{u,spec} = \frac{s_{event} \Omega_{safe}}{\pi} \frac{\epsilon_{g,spec}(t_*)}{|g'(t_*)|}
```

```text
tau_event = 1e-10
```

Critères :

```text
epsilon_u_spec / max(1, |u_*|) <= 1e-10
```

et :

```text
|u_e^{(2p)} - u_e^{(p)}| / max(1, |u_e^{(2p)}|) <= 1e-10
```

Budget final :

```math
\epsilon_{u,solver} + \epsilon_{u,spec} \le 1e-10 \max(1, |u_*|)
```

Défaut de pente insuffisante :

```text
EVENT_CONDITIONING_UNRESOLVED
```

## 24. Limites

```text
DEGENERATE_ROOT_CONTROL = OPEN
ARGMAX_TOLERANCES = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCE = 1e-10
```

## 25. Certification numérique de l'argmax de `T_grow`

Cette certification s'applique uniquement au chemin nominal où toutes les
cellules candidates pertinentes de `(0,T_peak)` sont soit certifiées vides,
soit résolues en candidats appariés associés à des racines simples qualifiantes
de `H_grow`.

Une cellule candidate non exclue dont la racine de `H_grow` est dégénérée,
non résolue ou non certifiée comme racine simple appariée n'est jamais écartée
silencieusement de la comparaison.

Sa présence interdit tout verdict argmax nominal et renvoie au statut
non résolu approprié, notamment `TIME_EVENT_CONTROL_SENSITIVE`, ou au traitement
encore ouvert de :

```text
DEGENERATE_ROOT_CONTROL = OPEN
```

### 25.1 Coordonnée et hauteur sans dimension

Pour `T_grow` :

```math
u
=
\frac{2\Omega_{safe}t}{\pi}.
```

Définir :

```math
\kappa
=
\frac{\pi}{2\Omega_{safe}},
```

et :

```math
\boxed{
a(u)
=
\frac{dF}{du}
=
\kappa F'(t(u)).
}
```

Comme `\kappa>0` est constant pour un fond et un cutoff donnés, maximiser
`a(u)` est exactement équivalent à maximiser `F'(t)`.

À un candidat stationnaire :

```math
a'(u)=0.
```

Avec :

```math
H_{grow}'(t)
=
3\chi'(t)\chi''(t)+\chi(t)\chi'''(t)
=
2F'''(t),
```

on obtient :

```math
a''(u)
=
\frac{\kappa^3}{2}H_{grow}'(t).
```

La borne déjà validée :

```math
L_H
=
3S_1S_2+S_0S_3
```

donne donc la borne sûre :

```math
\boxed{
B_{a''}
=
\frac{\kappa^3}{2}L_H.
}
```

Les hauteurs `a` sont comparées uniquement entre candidats du même fond et du
même cutoff. Elles ne sont jamais comparées directement entre `Lambda=2` et
`Lambda=3`.

### 25.2 Exhaustivité des candidats sur un premier lobe actif

Sur le premier lobe :

```math
\chi(0)=0,
```

et, par définition de `T_peak` :

```math
\chi'(T_{peak})=0.
```

Donc :

```math
F'(0)=0,
\qquad
F'(T_{peak})=0.
```

La voie nominale exige un premier lobe actif certifié :

```text
T_peak > 0
chi non identiquement nul
F' > 0 en au moins un point de (0,T_peak), avec signe certifié
```

Comme `F'` est continue sur `[0,T_peak]`, son maximum global positif est alors
atteint strictement dans `(0,T_peak)`.

Tout maximiseur intérieur satisfait :

```math
F''(t)=0,
```

soit :

```math
H_{grow}(t)=0.
```

Comme `chi` est une somme trigonométrique finie, `H_grow` est analytique réel.
Sur un premier lobe actif, `H_grow` n'est pas identiquement nul ; ses zéros sur
l'intervalle compact sont donc isolés et en nombre fini.

L'exclusion ou la résolution certifiée de toutes les cellules candidates
pertinentes suffit ainsi à énumérer tous les maximiseurs globaux possibles de
`F'`.

Pour une racine simple, un candidat de maximum local de `F'` vérifie :

```math
H_{grow}'(t_i)<0.
```

### 25.3 Incertitude de localisation d'un candidat

Pour chaque candidat simple apparié `i`, réutiliser le budget déjà validé en
coordonnée `u` :

```math
e_{u,i}
=
\epsilon_{u,solver,i}
+
\max\left(
\epsilon_{u,spec,i},
|u_i^{(2p)}-u_i^{(p)}|
\right).
```

Aucune nouvelle tolérance de racine n'est introduite.

Comme `a'(u_i^*)=0`, l'incertitude de localisation contribue à la hauteur au
second ordre :

```math
\epsilon_{a,loc,i}
=
\frac12 B_{a''}e_{u,i}^2.
```

Donc :

```math
\boxed{
\epsilon_{a,loc,i}
=
\frac{\kappa^3L_H}{4}e_{u,i}^2.
}
```

### 25.4 Contrôle spectral de la hauteur

Au même point physique haute précision `u_i^{(2p)}`, définir :

```math
\epsilon_{a,spec,i}
=
\left|
a^{(2p)}(u_i^{(2p)})
-
a^{(p)}(u_i^{(2p)})
\right|.
```

Pour le candidat apparié évalué à sa propre racine à chaque précision :

```math
d_{a,i}
=
\left|
a_i^{(2p)}
-
a_i^{(p)}
\right|.
```

Le budget numérique final de hauteur est :

```math
\boxed{
e_{a,i}
=
\max\left(
d_{a,i},
\epsilon_{a,spec,i}+\epsilon_{a,loc,i}
\right).
}
```

La porte de précision est :

```text
tau_argmax = 1e-10
```

avec :

```math
\boxed{
\frac{e_{a,i}}
{\max(1,|a_i^{(2p)}|)}
\le
10^{-10}.
}
```

Cette condition doit être satisfaite par chaque candidat participant à la
comparaison globale.

Sinon :

```text
ARGMAX_PRECISION_UNRESOLVED
```

et aucun `T_grow` confirmatoire n'est publié.

### 25.5 Maximiseur global unique

Pour chaque candidat qualifiant `i`, former :

```math
I_i
=
[
a_i^{(2p)}-e_{a,i},
a_i^{(2p)}+e_{a,i}
].
```

Le candidat `k` est un maximiseur global unique numériquement résolu si :

```math
\boxed{
a_k^{(2p)}-e_{a,k}
>
\max_{j\ne k}
\left(
a_j^{(2p)}+e_{a,j}
\right).
}
```

Alors :

```text
ARGMAX_UNIQUE_RESOLVED
```

et :

```text
T_grow = t_k
```

Aucune tolérance indépendante de « quasi-égalité » des maxima n'est utilisée.

Si les intervalles des meilleurs candidats se recouvrent sans oracle exact
applicable :

```text
ARGMAX_AMPLITUDE_UNRESOLVED
```

et aucun `T_grow` confirmatoire n'est publié.

### 25.6 Égalité exacte de plusieurs maxima

Une branche d'égalité exacte n'est autorisée que si l'égalité des hauteurs
exactes d'un ensemble fini `T` de candidats qualifiants est établie par un
oracle `STRUCTURAL_ANALYTIC` du modèle exact, par exemple une symétrie exacte ou
une identité démontrée.

Un cluster spectral numérique, une coïncidence numérique ou un recouvrement
d'intervalles ne constitue jamais un tel oracle.

`T` doit être la classe d'égalité complète identifiée par cet oracle parmi les
candidats auxquels il s'applique.

Pour chaque `i in T`, utiliser :

```math
I_i
=
[
a_i^{(2p)}-e_{a,i},
a_i^{(2p)}+e_{a,i}
].
```

Comme l'oracle impose une hauteur exacte commune, définir l'intervalle certifié
de cette hauteur commune par intersection :

```math
L_T
=
\max_{i\in T}
\left(
a_i^{(2p)}-e_{a,i}
\right),
```

```math
U_T
=
\min_{i\in T}
\left(
a_i^{(2p)}+e_{a,i}
\right).
```

La porte d'oracle est :

```math
\boxed{
L_T\le U_T.
}
```

Dès qu'un oracle exact applicable est invoqué, cette porte est évaluée avant
tout autre verdict argmax.

Si elle échoue :

```text
ARGMAX_EXACT_ORACLE_NUMERICAL_INCONSISTENCY
```

et aucun verdict confirmatoire, y compris `ARGMAX_UNIQUE_RESOLVED`, n'est
autorisé.

Si elle passe, la classe liée `T` n'est certifiée globalement maximale que si :

```math
\boxed{
L_T
>
\max_{j\notin T}
\left(
a_j^{(2p)}+e_{a,j}
\right).
}
```

Si cette dominance résiduelle échoue :

```text
ARGMAX_AMPLITUDE_UNRESOLVED
```

et aucun `T_grow` confirmatoire n'est publié.

### 25.7 Plus ancien membre d'une égalité globale exacte

Une fois `T` certifié comme ensemble des maximiseurs globaux, le candidat
`k in T` est certifié comme le plus ancien si :

```math
\boxed{
u_k+e_{u,k}
<
\min_{\substack{j\in T\\j\ne k}}
\left(
u_j-e_{u,j}
\right).
}
```

Alors :

```text
ARGMAX_EXACT_TIE_EARLIEST_RESOLVED
```

et :

```text
T_grow = t_k
```

conformément à la définition scientifique de `T_grow` comme infimum des
maximiseurs globaux.

Si l'ordre temporel des membres de `T` n'est pas résolu :

```text
ARGMAX_TIME_ORDER_UNRESOLVED
```

et aucun `T_grow` confirmatoire n'est publié.

### 25.8 Porte de complétude et statut épistémique

La certification argmax n'est valide que si :

```text
- toutes les cellules candidates pertinentes avant T_peak sont certifiées
  vides ou résolues en racines simples appariées qualifiantes ;
- aucun candidat dégénéré ou non résolu ne subsiste ;
- tous les candidats comparés satisfont la porte de précision de hauteur ;
- l'identité et l'ordre des candidats sont stables sous la famille beta
  préenregistrée ;
- l'appariement p / 2p est résolu ;
- aucune cellule candidate antérieure non résolue ne subsiste.
```

La certification argmax ne peut jamais écraser un statut
`TIME_EVENT_CONTROL_SENSITIVE`, spectralement non résolu ou conditionnellement
non résolu.

Les statuts :

```text
ARGMAX_UNIQUE_RESOLVED
ARGMAX_EXACT_TIE_EARLIEST_RESOLVED
```

sont des statuts :

```text
NUMERICAL_CONTROL / PREREGISTERED_CONFIRMATORY
```

et non des énoncés `STRUCTURAL_ANALYTIC`.

La même règle numérique est appliquée à `Lambda=2` et `Lambda=3`, mais les
hauteurs adimensionnées `a` ne sont comparées qu'à l'intérieur d'un même cutoff.
Les temps physiques d'événement restent les quantités comparées entre cutoffs.

### 25.9 Statut

```text
ARGMAX_TOLERANCES = VALIDATED_FOR_FREEZE
ARGMAX_TOLERANCE = 1e-10
DEGENERATE_ROOT_CONTROL = OPEN
```
