# Toy Model 0B — budget d'erreur de la dérivée en delta

Statut : **validé pour gel — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `derivative-control.md`, `soft-loop-static-gate.md`

Ce document précise pourquoi la famille sans dimension `A_delta` ne peut pas être figée indépendamment de la précision numérique atteignable sur `Delta_1` et du solveur des événements temporels.

## 1. Expansion locale de Delta_1

L'oddness exacte impose, lorsque `Delta_1` est suffisamment régulière autour de `delta=0` :

```math
Delta_1(delta)=a_1\,delta+a_3\,delta^3+a_5\,delta^5+\cdots
```

avec :

```math
Xi_1=a_1.
```

Dans le protocole numérique SOFT-LOOP, l'échelle opérationnelle est :

```math
h=\alpha\,\delta_c,
```

avec :

```math
\delta_c(g,\mu)=\frac{gap_{GS}^{(\Lambda=2)}(g,\mu,0)}{6g}.
```

Le `gap_0` du modèle effectif motive analytiquement cette coordonnée, mais le pas confirmatoire est construit à partir du gap calculé à `Lambda=2`. Les mêmes valeurs physiques de `h` sont ensuite utilisées à `Lambda=2` et `Lambda=3`.

L'estimateur central est donc :

```math
\widehat\Xi_1(alpha)
=\frac{Delta_1(h)-Delta_1(-h)}{2h}
=a_1+a_3\,delta_c^2\alpha^2+O(\alpha^4).
```

La convergence dominante est ainsi quadratique en `alpha`.

## 2. Le coefficient 1/2 n'est pas universel pour Delta_1

La fonction à deux niveaux :

```math
f(x)=\frac{x}{\sqrt{1+x^2}}
```

vérifie :

```math
\frac{f(alpha)}{alpha}=1-\frac{alpha^2}{2}+O(alpha^4).
```

Mais `Delta_1` n'est pas contrainte à suivre cette fonction : elle provient d'une réponse de Kubo et de temps caractéristiques.

Il est donc interdit d'écrire pour `Xi_1` :

```math
relative\ bias = \frac{alpha^2}{2}
```

comme loi universelle.

La seule structure générale gelable est :

```math
relative\ bias = C_2\alpha^2+O(alpha^4),
```

avec `C_2` dépendant du fond et de l'estimateur dynamique.

## 3. Amplification de l'erreur sur Delta_1

Soit `sigma_Delta` une erreur absolue caractéristique sur `Delta_1(h)`.

L'erreur absolue correspondante sur la dérivée est de l'ordre :

```math
sigma_Xi\sim\frac{sigma_Delta}{h}
=\frac{sigma_Delta}{alpha\,delta_c}.
```

Pour une erreur relative sur `Xi_1`, il faut donc introduire la quantité sans dimension :

```math
\varepsilon_Delta
=\frac{sigma_Delta}{|Xi_1|\,delta_c}.
```

Alors seulement :

```math
relative\ numerical\ error
\sim\frac{\varepsilon_Delta}{alpha}.
```

Par conséquent, une phrase du type :

```text
Delta_1 est précis à 1e-4 -> alpha_opt ~ (1e-4)^(1/3)
```

n'est pas dimensionnellement suffisante : le niveau absolu `1e-4` doit être comparé à l'échelle locale de signal `|Xi_1| delta_c`.

Comme `delta_c` s'effondre dans le régime cyclique mou, la demande de précision sur `Delta_1` devient automatiquement plus sévère lorsque `mu` devient très négatif.

## 3.1 Budget propagé depuis les événements temporels

Pour un estimateur temporel :

```math
C_O = \frac{T_O^{state}}{T_O^{ref}}.
```

Dans :

```math
N(h) = \Delta_1(+h) - \Delta_1(-h),
```

les mêmes temps de référence calculés sont réutilisés aux deux signes. Ils s'annulent donc algébriquement exactement.

Le budget central dépend uniquement des quatre temps d'état :

```text
T_{A,+h}
T_{B,+h}
T_{A,-h}
T_{B,-h}
```

Pour chacun de ces événements, dans la coordonnée `u_e` définie par `temporal-event-solver.md` :

```math
e_u = \epsilon_{u,solver} + \max(\epsilon_{u,spec}, |u_e^{(2p)} - u_e^{(p)}|).
```

Définir :

```math
r_T = \frac{u_e}{e_u},
```

avec la garde obligatoire :

```math
r_T < 1.
```

Alors :

```math
|\delta\log T| \le L(r_T),
```

avec :

```math
L(r) = -\log(1-r).
```

Le budget absolu sur le numérateur central est :

```math
E_N(h) = \sum_{\sigma=\pm} [L(r_{A,\sigma}) + L(r_{B,\sigma})].
```

Le budget numérique propagé sur la dérivée est donc :

```math
E_\Xi^{num}(h) = \frac{E_N(h)}{2h} = \frac{E_N(h)}{2\alpha\delta_c}.
```

Ce budget est un budget numérique propagé ; il ne constitue pas une borne sur l'erreur de troncature asymptotique de la différence finie.

```text
DELTA1_PROPAGATED_ERROR_BUDGET = VALIDATED_FOR_FREEZE
```

## 4. Position qualitative de l'optimum

Si l'on modélise l'erreur relative totale par :

```math
E(alpha)\approx |C_2|\alpha^2+\frac{\varepsilon_Delta}{alpha},
```

alors :

```math
alpha_*\sim\left(\frac{\varepsilon_Delta}{2|C_2|}\right)^{1/3}.
```

Cette relation explique la compétition entre non-linéarité et amplification numérique, mais ne fournit pas une valeur de `alpha_*` avant que :

- la précision sur `Delta_1` soit bornée ;
- le coefficient asymptotique effectif soit suffisamment contrôlé ;
- la stabilité sous raffinements soit vérifiée.

`A_delta` doit donc être gelée avec le protocole numérique de calcul des temps et non indépendamment.

## 5. Rapport quadratique pour une famille géométrique

Si :

```math
\widehat\Xi(alpha)=Xi+C_2\alpha^2+C_4\alpha^4+\cdots
```

et que la famille contient :

```math
alpha,\ alpha/2,\ alpha/4,
```

alors, tant que le terme quadratique domine :

```math
R_2
=\frac{\widehat\Xi(alpha)-\widehat\Xi(alpha/2)}
{\widehat\Xi(alpha/2)-\widehat\Xi(alpha/4)}
\to4.
```

La limite 4 reste un diagnostic asymptotique, mais le protocole confirmatoire n'utilise pas le seul ratio ponctuel observé.

En présence des budgets numériques sur les différences, le critère opérationnel est l'intervalle certifié `[Q_min, Q_max]` défini dans `derivative-control.md §6`.

La voie :

```text
DERIVATIVE_STABLE_QUADRATIC
```

n'est autorisée que si cet intervalle complet est contenu dans `[2,8]` et si les deux différences résolues ont le même signe certifié.

Une différence noyée dans son budget numérique ne peut donc pas produire artificiellement un verdict de convergence.

Ce contrôle n'est pas spécifique au modèle à deux niveaux : toute `Delta_1` lisse et impaire avec terme cubique générique possède la même structure asymptotique quadratique.

Les collapses statiques du gap et de `<Phi>` restent les tests propres de la réduction effective à deux niveaux.

## 6. Extrapolation de Richardson

Richardson est strictement une extrapolation secondaire.

L'estimateur primaire publié reste :

```math
X_3 = \Xi_1(1/16).
```

Richardson est autorisé si et seulement si :

```text
DERIVATIVE_STABLE_QUADRATIC
```

On définit alors :

```math
R_2 = \frac{4X_3 - X_2}{3}.
```

Son budget numérique, et uniquement numérique, est :

```math
e_{R_2}^{num} = \frac{4e_3 + e_2}{3}.
```

On peut également former :

```math
R_1 = \frac{4X_2 - X_1}{3}.
```

La quantité :

```math
|R_1 - R_2|
```

est publiée comme :

```text
TRUNCATION_DIAGNOSTIC_ONLY
```

Elle n'est pas une borne rigoureuse sur :

```math
|R_2 - \Xi_1|.
```

Statut :

```text
RICHARDSON = SECONDARY_EXTRAPOLATION
```

Richardson :

- ne remplace pas `X_3` comme estimateur primaire ;
- ne peut pas modifier seul le verdict confirmatoire ;
- est interdit sous `DERIVATIVE_NUMERICAL_FLOOR` ;
- est interdit sous `DERIVATIVE_CONTROL_SENSITIVE`.

Les valeurs brutes :

```text
X_0
X_1
X_2
X_3
```

restent obligatoirement publiées.

## 7. Lot numérique couplé

Les éléments suivants doivent être gelés comme un seul lot cohérent :

```text
TIME_BRACKETING / TIME_SAMPLING
EVENT_ROOT_SOLVER
ARGMAX_LOCALIZATION
EVENT_SOLVER_TOLERANCES
DELTA1_ERROR_BUDGET
A_DELTA_VALUES
DERIVATIVE_STABILITY_CRITERION
RICHARDSON_USAGE_RULE
```

Il est interdit de choisir `alpha_min` avant d'avoir défini comment l'erreur sur les temps se propage vers `Delta_1`.

## 8. Statut

```text
DERIVATIVE_ALPHA2_CONVERGENCE          = VALIDATED_FOR_FREEZE_IF_SMOOTH
DERIVATIVE_ALPHA2_COEFFICIENT_HALF     = REJECTED_FOR_DELTA1
DELTA1_ERROR_AMPLIFICATION             = VALIDATED_FOR_FREEZE
RAW_SIGMA_DELTA_CUBEROOT_RULE          = REJECTED
DIMENSIONLESS_ERROR_BALANCE            = VALIDATED_IN_PRINCIPLE
QUADRATIC_CONVERGENCE_RATIO_4          = VALIDATED_FOR_FREEZE_AS_ASYMPTOTIC_DIAGNOSTIC
RATIO_4_TWO_LEVEL_SPECIFIC             = REJECTED
RICHARDSON_USAGE_RULE                  = VALIDATED_FOR_FREEZE
RICHARDSON_ROLE                        = SECONDARY_EXTRAPOLATION
A_DELTA_VALUES                         = VALIDATED_FOR_FREEZE
DELTA1_PROPAGATED_ERROR_BUDGET         = VALIDATED_FOR_FREEZE
DERIVATIVE_STABILITY_CRITERION         = VALIDATED_FOR_FREEZE
NUMERICAL_EVENT_LOT                    = OPEN
```
