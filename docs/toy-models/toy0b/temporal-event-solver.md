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
4. confirmer que `F'` passe de `+` à `-`, ou de manière équivalente que la racine de `chi'` correspond bien à un maximum de `|chi|` sur le premier lobe.

Les racines tangentielles de `chi'` sans changement de caractère ne sont pas automatiquement des pics.

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

Cette réduction évite de certifier directement `F-eta`, qui possède une bande jusqu'à `2 Omega_chi` alors que le croisement de niveau équivalent vit à la bande de `chi`.

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

Le conditionnement numérique de localisation est attaché à la fonction réellement résolue.

Pour une racine simple `g(t*)=0` :

```math
|\delta t_*|
\sim
\frac{|\delta g(t_*)|}{|g'(t_*)|}.
```

Les diagnostics nominaux sont donc :

```text
T_thr  -> |chi'(T_thr)|
T_down -> |chi'(T_down)|
T_peak -> |chi''(T_peak)|
T_grow -> |H_grow'(T_grow)|
```

avec :

```math
H_{grow}'=3\chi'\chi''+\chi\chi'''=2F'''.
```

Les quantités basées sur `F` peuvent être publiées en complément. Par exemple, à `T_peak` :

```math
F''(T_{peak})
=\frac12\chi(T_{peak})\chi''(T_{peak}).
```

Mais elles ne remplacent pas le conditionnement de la fonction de racine effectivement utilisée.

## 11. Budget spectral dynamique

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
GLOBAL_FACTOR_TWO_FOR_ALL_EVENTS       = REJECTED
ESTIMATOR_SPECIFIC_BAND_FACTOR         = VALIDATED_FOR_FREEZE
SPECTRAL_CELL_EXCLUSION                = VALIDATED_IN_PRINCIPLE
CONTINUOUS_ROOT_SOLVER                 = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
CONTINUOUS_ARGMAX                      = VALIDATED_FOR_FREEZE_IN_PRINCIPLE
INTERPOLATION_ROOT_FINDING_FINAL       = REJECTED
EVENT_ROOT_CONDITIONING_PUBLICATION    = VALIDATED_FOR_FREEZE
BRACKETING_REFINEMENT_VALUES           = OPEN
ROOT_SOLVER_TOLERANCES                 = OPEN
ARGMAX_TOLERANCES                      = OPEN
SPECTRAL_PRECISION_CONTROL             = OPEN
DELTA1_PROPAGATED_ERROR_BUDGET         = OPEN
SAME_NUMERICAL_RULES_ACROSS_CUTOFFS    = MANDATORY
```
