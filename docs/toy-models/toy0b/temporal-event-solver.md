# Toy Model 0B — solveur continu des événements temporels

Statut : **validé pour gel en principe — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `derivative-error-budget.md`, `derivative-control.md`, `recurrence-control.md`

Ce document fixe l'architecture numérique de principe pour l'extraction des temps caractéristiques. Les valeurs de tolérance restent ouvertes.

## 1. Principe

Le Toy Model 0B est de dimension finie et le Hamiltonien est diagonalizable numériquement aux cutoffs prévus.

Une fois le spectre et les éléments de matrice connus, la réponse :

```math
\chi_{pq}(t)
=i\,Tr\left[\rho\,[n_p,n_q(t)]\right]
```

peut être évaluée à un temps arbitraire par somme spectrale des phases `exp(i(E_a-E_b)t)`.

Les dérivées temporelles de `chi` et de :

```math
F(t)=\frac{\chi(t)^2}{4}
```

peuvent être évaluées par la même représentation spectrale, sans différence finie temporelle.

Par conséquent, une grille temporelle ne doit pas définir directement les temps scientifiques.

## 2. Rôle de la grille temporelle

Une grille / stratégie d'échantillonnage sert uniquement à :

- découvrir l'ordre des événements ;
- construire des brackets pour les premières racines / extrema ;
- vérifier qu'aucun événement antérieur n'a été manqué ;
- fournir des diagnostics et figures.

Les valeurs finales de :

```text
T_peak
T_grow
T_thr(eta)
T_down(eta)
```

sont obtenues par un solveur continu dans les brackets déterminés.

Ainsi :

```text
TIME_SAMPLING = BRACKETING_CONTROL
```

et non estimateur final du temps.

## 3. T_peak

Le premier pic est défini comme le premier `t>0` où `F'(t)` passe de positif à négatif.

Le protocole doit :

1. détecter le premier bracket de changement de signe compatible ;
2. résoudre :

```math
F'(t)=0
```

par une méthode bracketée robuste ;
3. confirmer le changement `+ -> -` autour de la racine.

Une racine tangentielle ou un plateau nécessite un statut spécifique / traitement numérique préenregistré ; elle ne doit pas être arbitrairement sélectionnée comme pic.

## 4. T_grow

`T_grow` est le premier maximiseur global de `F'(t)` sur `(0,T_peak)`.

La stratégie nominale est :

- construire un bracket de lobe pour les maxima candidats de `F'` ;
- utiliser un solveur continu d'optimisation bornée ou, lorsque la régularité le permet, résoudre `F''(t)=0` puis vérifier le caractère maximal ;
- comparer tous les candidats dans `(0,T_peak)` ;
- choisir l'infimum de l'ensemble des maximiseurs conformément à la définition scientifique.

Une simple sélection du plus grand échantillon de grille est interdite comme estimateur final.

## 5. T_thr et T_down

Pour chaque `eta` admissible :

```math
F(t)-eta=0
```

est résolu par racine bracketée.

- `T_thr(eta)` : première racine ascendante avant `T_peak` ;
- `T_down(eta)` : première racine descendante après `T_peak` appartenant au même premier lobe.

La monotonie locale / le signe de `F'` doit être vérifié autour de la racine pour distinguer montée et descente.

## 6. Pas d'interpolation comme estimateur scientifique

Une interpolation linéaire, spline ou polynomiale d'une grille échantillonnée peut être utilisée pour visualisation ou pour générer un bracket initial.

Elle ne doit pas fournir directement le temps final publié lorsque l'évaluateur spectral continu est disponible.

Donc :

```text
INTERPOLATION_AS_FINAL_TIME_ESTIMATOR = REJECTED
CONTINUOUS_ROOT_SOLVER                = REQUIRED
```

Cette décision retire une source majeure de biais de discrétisation du budget d'erreur sur `Delta_1`.

## 7. Contrôle de résolution du bracketing

Le fait d'utiliser un solveur continu n'élimine pas le risque de manquer le **premier** événement.

Le protocole doit donc préenregistrer une famille de résolution / stratégie de bracketing et vérifier que :

```text
- l'identité du premier événement est stable sous raffinement ;
- le bracket converge vers le même événement ;
- le solveur continu retourne une racine / un extremum compatible.
```

Si le premier événement change sous raffinement :

```text
TIME_EVENT_CONTROL_SENSITIVE
```

jusqu'à résolution suffisante.

Les valeurs de cette famille restent `OPEN`.

## 8. Tolérances et propagation vers Delta_1

Le solveur final doit utiliser des tolérances absolues et/ou relatives préenregistrées sur les temps.

Comme les contrastes sont construits à partir de logarithmes de rapports de temps, une erreur relative sur un temps `T` se propage naturellement comme :

```math
\delta\log T\simeq\frac{\delta T}{T}.
```

Le budget d'erreur de `Delta_1` doit donc être dérivé explicitement du nombre de temps entrant dans chaque estimateur (`grow`, `thr`, etc.) et des tolérances de résolution correspondantes.

Cette propagation doit être fixée avant le choix de `alpha_min` dans `A_delta`.

## 9. Troncature

Les mêmes règles de bracketing, solveurs et tolérances doivent être utilisées à :

```text
Lambda=2
Lambda=3
```

sur les points soumis au contrôle de troncature.

Il est interdit d'améliorer sélectivement le solveur d'un cutoff après inspection pour restaurer la convergence.

## 10. Statut

```text
SPECTRAL_CONTINUOUS_TIME_EVALUATOR   = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
TIME_GRID_AS_FINAL_ESTIMATOR         = REJECTED
TIME_GRID_AS_BRACKETING_CONTROL      = VALIDATED_FOR_FREEZE
CONTINUOUS_ROOT_SOLVER               = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
CONTINUOUS_ARGMAX                     = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
INTERPOLATION_ROOT_FINDING_FINAL     = REJECTED
BRACKETING_REFINEMENT_FAMILY         = OPEN
ROOT_SOLVER_TOLERANCES               = OPEN
ARGMAX_TOLERANCES                    = OPEN
DELTA1_PROPAGATED_ERROR_BUDGET       = OPEN
SAME_NUMERICAL_RULES_ACROSS_CUTOFFS  = MANDATORY
```
