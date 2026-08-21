# Toy Model 0B — solveur spectral continu des événements temporels

Statut : **validé pour gel en principe — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `derivative-error-budget.md`, `derivative-control.md`, `recurrence-control.md`

Ce document fixe l'architecture numérique de principe pour l'extraction des temps caractéristiques. Les valeurs de tolérance et la famille de raffinement restent ouvertes.

## 1. Évaluateur spectral exact en temps

Le Toy Model 0B est fini et le Hamiltonien est diagonalizable aux cutoffs prévus.

Pour l'état canonique stationnaire et les densités réelles, la réponse possède la représentation finie :

```math
\chi_{pq}(t)
=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t),
```

avec poids groupés par projecteur spectral, selon `exact-spectral-response.md`.

Les dérivées de `chi` sont donc obtenues analytiquement terme à terme. Pour :

```math
F(t)=\frac{\chi(t)^2}{4},
```

`F'`, `F''`, `F'''` peuvent être évaluées continûment sans différence finie.

Par conséquent :

```text
TIME_GRID_AS_FINAL_ESTIMATOR = REJECTED
FINITE_DIFFERENCE_TIME_DERIVATIVE = REJECTED
```

## 2. Rôle du bracketing

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

sont obtenues par un solveur continu dans les cellules candidates.

Ainsi :

```text
TIME_SAMPLING = BRACKETING_CONTROL
```

et non estimateur final du temps.

## 3. Échelle spectrale naturelle de bracketing

Pour chaque canal, on définit la fréquence active maximale :

```math
\omega_{max}
=\max\{\omega>0:C_{pq}(\omega)\neq0\}.
```

L'échelle :

```math
\boxed{t_\omega=\pi/\omega_{max}}
```

fournit une unité naturelle de raffinement.

La famille de bracketing devra être paramétrée sous la forme :

```math
\Delta t_k
=\beta_k\frac{\pi}{\omega_{max}},
```

avec des coefficients sans dimension `beta_k` préenregistrés.

Cependant `Delta t <= pi/omega_max` n'est pas un certificat de complétude d'un test de changements de signe. Des racines multiples, tangentielles ou deux racines dans une même cellule restent possibles.

`omega_max` fournit donc une **échelle**, pas une preuve automatique que le premier événement a été trouvé.

## 4. Exclusion certifiable de cellules

La représentation spectrale fournit des bornes :

```math
|\chi^{(r)}(t)|
\le
\sum_\omega |C(\omega)|\omega^r.
```

Par composition, des bornes sur les dérivées des fonctions événement peuvent être obtenues.

Si une fonction événement `g(t)` est évaluée au centre `t_c` d'une cellule de demi-largeur `h` et qu'une borne :

```math
L\ge\sup_{cell}|g'(t)|
```

est disponible, alors :

```math
|g(t_c)|>Lh
```

certifie l'absence de racine dans cette cellule.

Les cellules non exclues sont subdivisées ou traitées par solveur continu. Une telle stratégie est préférable à une simple recherche de changements de signe si elle reste numériquement praticable.

Le choix exact entre raffinement stable et certification par bornes reste `OPEN` dans le lot numérique.

## 5. T_peak

Le premier pic est défini comme le premier `t>0` où `F'(t)` passe de positif à négatif.

Le protocole doit :

1. isoler la première cellule candidate ;
2. résoudre :

```math
F'(t)=0
```

par une méthode bracketée robuste ;
3. confirmer le changement `+ -> -` autour de la racine.

Une racine tangentielle ne constitue pas automatiquement un pic. Comme `F'` est analytique, un plateau sur un intervalle impliquerait une structure dégénérée globale qui doit recevoir un statut spécifique plutôt qu'un choix arbitraire de temps.

## 6. T_grow

`T_grow` est l'infimum de l'ensemble des maximiseurs globaux de `F'(t)` sur `(0,T_peak)`.

La stratégie nominale est :

- isoler tous les candidats pertinents dans le premier lobe ;
- utiliser une optimisation continue bornée ou résoudre :

```math
F''(t)=0
```

et vérifier le caractère maximal ;
- comparer les valeurs de `F'` de tous les candidats ;
- choisir le premier maximiseur global conformément à la définition scientifique.

Une simple sélection du plus grand échantillon de grille est interdite.

Si plusieurs maxima sont quasi-égaux au niveau de l'incertitude numérique, l'identité de `T_grow` est elle-même conditionnée et doit être signalée.

## 7. T_thr et T_down

Pour chaque `eta` admissible :

```math
F(t)-eta=0
```

est résolu par racine bracketée.

- `T_thr(eta)` : première racine ascendante avant `T_peak` ;
- `T_down(eta)` : première racine descendante après `T_peak` appartenant au même premier lobe.

Le signe de `F'` autour de la racine doit confirmer montée ou descente.

## 8. Pas d'interpolation comme estimateur scientifique

Une interpolation de grille peut servir à la visualisation ou à proposer une cellule initiale.

Elle ne fournit jamais le temps final publié lorsque l'évaluateur spectral est disponible.

```text
INTERPOLATION_AS_FINAL_TIME_ESTIMATOR = REJECTED
CONTINUOUS_ROOT_SOLVER                = REQUIRED
```

## 9. Contrôle de résolution du premier événement

Même avec un évaluateur spectral continu, le risque principal est de manquer le **premier** événement ou un candidat tangent.

Le protocole doit préenregistrer une famille de raffinement et vérifier que :

```text
- l'identité du premier événement est stable ;
- les cellules candidates se stabilisent ;
- le solveur continu retourne le même événement ;
- les éventuelles cellules non exclues plus précoces sont résolues.
```

Si l'identité du premier événement change sous raffinement :

```text
TIME_EVENT_CONTROL_SENSITIVE
```

jusqu'à résolution suffisante.

Les valeurs `beta_k` restent `OPEN`.

## 10. Conditionnement des événements

La représentation spectrale élimine la discrétisation temporelle comme estimateur final, mais elle n'élimine pas le conditionnement des racines et extrema.

Pour une racine simple :

```math
g(t_*)=0,
```

une perturbation `delta g` donne au premier ordre :

```math
|\delta t_*|
\sim
\frac{|\delta g(t_*)|}{|g'(t_*)|}.
```

Les diagnostics naturels à publier sont donc notamment :

```text
T_thr  -> |F'(T_thr)|
T_peak -> |F''(T_peak)|
T_grow -> |F'''(T_grow)| lorsque F''=0 sert à localiser le candidat
```

Des valeurs faibles indiquent un événement mal conditionné même si la diagonalisation est précise.

Le cas de plusieurs candidats quasi-égaux pour `T_grow` doit également être traité comme problème de conditionnement de l'argmax.

## 11. Budget spectral

L'erreur globale ne doit pas être identifiée à l'epsilon machine.

Le protocole numérique devra contrôler au minimum :

```text
- résidus des paires propres / projecteurs ;
- défaut d'orthogonalité ;
- stabilité des fréquences et poids spectraux sous précision / solveur ;
- accumulation de phase delta_omega * t ;
- annulations dans les sommes trigonométriques ;
- conditionnement des événements ci-dessus.
```

La stabilité sous augmentation de précision peut être utilisée comme contrôle numérique indépendant, avec une règle uniforme préenregistrée.

## 12. Propagation vers Delta1

Les contrastes utilisent des logarithmes de rapports de temps. Pour une petite erreur :

```math
\delta\log T\simeq\frac{\delta T}{T}.
```

Le budget d'erreur de `Delta_1` doit être dérivé des erreurs des temps qui entrent dans chaque estimateur (`grow`, `thr`) et de leurs corrélations éventuelles.

Cette propagation est nécessaire avant le choix de `alpha_min` dans `A_delta`.

## 13. Troncature

Les mêmes règles de bracketing, solveurs, diagnostics de conditionnement et tolérances sont utilisées à :

```text
Lambda=2
Lambda=3
```

sur les points soumis au contrôle de troncature.

Il est interdit d'améliorer sélectivement un cutoff après inspection pour restaurer la convergence.

## 14. Statut

```text
FINITE_SINE_TIME_EVALUATOR          = VALIDATED_FOR_FREEZE
TIME_GRID_AS_FINAL_ESTIMATOR        = REJECTED
TIME_GRID_AS_BRACKETING_CONTROL     = VALIDATED_FOR_FREEZE
OMEGA_MAX_BRACKETING_SCALE          = VALIDATED_FOR_FREEZE
OMEGA_MAX_GRID_COMPLETENESS         = REJECTED
SPECTRAL_CELL_EXCLUSION             = VALIDATED_IN_PRINCIPLE
CONTINUOUS_ROOT_SOLVER              = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
CONTINUOUS_ARGMAX                   = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
INTERPOLATION_ROOT_FINDING_FINAL    = REJECTED
EVENT_CONDITIONING_PUBLICATION      = VALIDATED_FOR_FREEZE
BRACKETING_REFINEMENT_FAMILY        = OPEN
ROOT_SOLVER_TOLERANCES              = OPEN
ARGMAX_TOLERANCES                   = OPEN
SPECTRAL_PRECISION_CONTROL          = OPEN
DELTA1_PROPAGATED_ERROR_BUDGET      = OPEN
SAME_NUMERICAL_RULES_ACROSS_CUTOFFS = MANDATORY
```
