# Toy Model 0B — bande fréquentielle des événements et coût de bracketing

Statut : **validé pour gel en principe — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `temporal-event-solver.md`

Ce document précise la bande fréquentielle pertinente pour chaque estimateur temporel. Il corrige une formulation antérieure trop conservative qui appliquait uniformément la bande de `F=chi^2/4` à tous les événements.

## 1. Bande de chi

Pour un canal :

```math
\chi(t)=\sum_j C_j\sin(\omega_j t),
```

on définit une borne spectrale :

```math
\Omega_\chi=\max_j\omega_j.
```

Pour éviter toute dépendance à un seuil déclarant certains poids `C_j` numériquement nuls, la borne conservative par défaut est :

```math
\Omega_{safe}=E_{max}-E_0.
```

Une borne plus serrée n'est admise que si elle résulte d'une règle de sélection analytique préenregistrée.

## 2. Identités exactes des événements

On utilise :

```math
F(t)=\frac{\chi(t)^2}{4},
```

avec :

```math
F'(t)=\frac12\chi(t)\chi'(t),
```

et :

```math
F''(t)=\frac12\left(\chi'(t)^2+\chi(t)\chi''(t)\right).
```

### T_peak

`T_peak` est le premier maximum strict du premier lobe de `F`.

Avant ce maximum, `chi` conserve le signe de son premier coefficient court non nul. Un zéro de `chi` est un minimum de `F`, pas un pic. Pour un pic strict avec `chi != 0` :

```math
F'(T_{peak})=0
\quad\Longleftrightarrow\quad
\chi'(T_{peak})=0.
```

Le candidat doit en outre satisfaire le changement de signe correspondant à un maximum de `F`.

Ainsi la fonction de certification nominale de `T_peak` est `chi'`, dont la bande reste `Omega_chi`.

### T_thr et T_down

Pour `eta>0` :

```math
F(t)=\eta
\quad\Longleftrightarrow\quad
|\chi(t)|=2\sqrt\eta.
```

Sur le premier lobe, le signe de `chi` est fixé. Si :

```math
s=sign(\chi(t))
```

sur ce lobe, les croisements sont donc les racines de :

```math
\chi(t)-s\,2\sqrt\eta=0.
```

`T_thr` est la première racine ascendante avant `T_peak`; `T_down` la première racine descendante après `T_peak` appartenant au même premier lobe.

Ces fonctions ont la même bande `Omega_chi` que `chi`.

### T_grow

`T_grow` maximise :

```math
F'(t)=\frac12\chi\chi'
```

sur `(0,T_peak)`. Les candidats intérieurs satisfont :

```math
H_{grow}(t)
:=\chi'(t)^2+\chi(t)\chi''(t)
=0.
```

Les produits de composantes spectrales génèrent des fréquences jusqu'à :

```math
2\Omega_\chi.
```

`T_grow` est donc le seul estimateur primaire de ce bloc qui paie structurellement le facteur de bande deux.

## 3. Bande par estimateur

On définit :

```text
s_peak = 1
s_thr  = 1
s_down = 1
s_grow = 2
```

et une **seule famille sans dimension commune** :

```math
\mathcal B=\{\beta_1>\beta_2>\cdots>\beta_K>0\}.
```

La taille de cellule nominale est :

```math
\boxed{
\Delta t_k^{(event)}
=\beta_k\frac{\pi}{s_{event}\,\Omega_{scale}}
}
```

avec :

```text
Omega_scale = Omega_safe
```

par défaut.

Il est interdit de choisir des familles `beta` différentes par estimateur après inspection. Seul le facteur `s_event`, fixé analytiquement ci-dessus, diffère.

Les valeurs numériques `beta_k` restent `OPEN`.

## 4. Pourquoi certifier sur chi / chi' plutôt que sur F' pour T_peak

La fonction :

```math
F'=\chi\chi'/2
```

s'annule à chaque zéro de `chi` en plus des extrema de `chi`.

Ces zéros de `chi` correspondent à des minima de `F` et ne sont pas des candidats `T_peak`. Une certification brute de toutes les racines de `F'` introduirait donc des cellules non pertinentes et des subdivisions inutiles.

La stratégie normative est :

```text
T_peak -> certifier les racines qualifiantes de chi'
T_thr  -> certifier les racines de chi - s 2 sqrt(eta)
T_down -> certifier les racines de chi - s 2 sqrt(eta)
T_grow -> certifier les racines de H_grow = chi'^2 + chi chi''
```

Les définitions scientifiques en termes de `F` restent inchangées ; seules leurs équations numériques équivalentes sont utilisées.

## 5. Densité de zéros : portée limitée

Une somme trigonométrique finie est une fonction entière de type exponentiel après prolongement complexe. Des résultats asymptotiques relient son type fréquentiel à une densité moyenne de zéros sous des hypothèses appropriées.

Cependant, une règle du type :

```math
N_{zero}([0,\tau])\sim O(\Omega\tau/\pi)
```

ne constitue pas une borne universelle sur intervalle fini suffisante pour certifier le protocole 0B.

La quantité `Omega*tau/pi` peut être utilisée au plus comme estimation de coût / ordre de grandeur pour dimensionner un raffinement initial. Elle ne doit jamais être utilisée pour conclure que toutes les racines ont été trouvées.

## 6. Certification par bornes de dérivées

Pour toute fonction de certification `g(t)`, on peut construire une borne :

```math
L\ge\sup_{cell}|g'(t)|.
```

Si la cellule est centrée en `t_c` et de demi-largeur `h` :

```math
|g(t_c)|>Lh
```

certifie l'absence de racine dans cette cellule.

Les cellules non exclues doivent être subdivisées ou résolues explicitement. Les racines tangentielles exigent une logique adaptée aux dérivées supérieures et ne sont pas capturées par un simple changement de signe.

## 7. Conditionnement aligné sur la fonction résolue

Le diagnostic numérique doit être attaché à la fonction effectivement résolue :

```text
T_thr  : |chi'(T_thr)|
T_down : |chi'(T_down)|
T_peak : |chi''(T_peak)|
T_grow : |H_grow'(T_grow)|
```

avec :

```math
H_{grow}'
=3\chi'\chi''+\chi\chi'''
=2F'''.
```

À `T_peak`, puisque `chi'=0` :

```math
F''(T_{peak})
=\frac12\chi(T_{peak})\chi''(T_{peak}).
```

L'ancien diagnostic `|F''(T_peak)|` reste dérivable, mais `|chi''|` est le conditionnement direct de la racine réellement résolue.

De même, utiliser `|F'(T_thr)|` introduirait artificiellement le facteur `sqrt(eta)` dans le conditionnement d'un croisement de niveau de `chi`; le conditionnement nominal de localisation est donc `|chi'|`.

## 8. Statut

```text
CHI_BANDWIDTH_SCALE                    = VALIDATED_FOR_FREEZE
GLOBAL_EVENT_BANDWIDTH_FACTOR_TWO       = REJECTED
PEAK_BANDWIDTH_FACTOR_ONE               = VALIDATED_FOR_FREEZE
THRESHOLD_BANDWIDTH_FACTOR_ONE          = VALIDATED_FOR_FREEZE
DOWN_BANDWIDTH_FACTOR_ONE               = VALIDATED_FOR_FREEZE
GROW_BANDWIDTH_FACTOR_TWO               = VALIDATED_FOR_FREEZE
COMMON_BETA_FAMILY                      = VALIDATED_FOR_FREEZE
ESTIMATOR_SPECIFIC_ANALYTIC_BAND_FACTOR = VALIDATED_FOR_FREEZE
FPRIME_AS_PEAK_CERTIFICATION_FUNCTION   = REJECTED
CHI_PRIME_PEAK_CERTIFICATION            = VALIDATED_FOR_FREEZE
CHI_LEVEL_THRESHOLD_CERTIFICATION       = VALIDATED_FOR_FREEZE
HGROW_CERTIFICATION                     = VALIDATED_FOR_FREEZE
ACTIVE_OMEGA_FROM_NUMERICAL_ZERO_CUT    = REJECTED_AS_DEFAULT
SAFE_SPECTRAL_BANDWIDTH                 = VALIDATED_FOR_FREEZE
ZERO_DENSITY_AS_COMPLETENESS_BOUND      = REJECTED
ZERO_DENSITY_AS_COST_HEURISTIC          = ALLOWED_WITH_SCOPE
DERIVATIVE_CELL_EXCLUSION               = VALIDATED_IN_PRINCIPLE
EVENT_ROOT_CONDITIONING_BY_SOLVED_FUNC  = VALIDATED_FOR_FREEZE
BETA_GRID_VALUES                        = OPEN
```
