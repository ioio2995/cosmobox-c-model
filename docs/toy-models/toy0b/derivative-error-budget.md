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

Dans SOFT-LOOP :

```math
h=alpha\,delta_c,
\qquad
\delta_c=\frac{gap_0}{6g}.
```

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

Ce rapport est un diagnostic utile d'entrée dans le régime asymptotique de l'estimateur central.

Il n'est **pas** un test spécifique de la réduction à deux niveaux : toute fonction `Delta_1` lisse et impaire possédant un terme cubique générique produit la même convergence quadratique.

Les collapses statiques de `gap` et `<Phi>` restent les tests propres de la réduction à deux niveaux.

Si les différences au dénominateur deviennent comparables au plancher numérique, `R_2` devient lui-même non résolu et ne doit pas recevoir un verdict physique.

## 6. Extrapolation de Richardson

Dans le régime quadratique :

```math
Xi_R(alpha)
=\frac{4\widehat\Xi(alpha/2)-\widehat\Xi(alpha)}{3}
=Xi+O(alpha^4).
```

Une extrapolation de Richardson peut donc être publiée comme estimateur amélioré lorsque :

- le rapport de convergence est compatible avec le régime quadratique selon la règle numérique préenregistrée ;
- les deux points utilisés sont au-dessus du plancher numérique ;
- la même procédure est appliquée à tous les fonds concernés.

Richardson ne remplace pas la publication des valeurs brutes `Xi_hat(alpha_k)`.

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
RICHARDSON_EXTRAPOLATION               = VALIDATED_IN_PRINCIPLE
A_DELTA_VALUES                         = OPEN
NUMERICAL_EVENT_LOT                    = OPEN
```
