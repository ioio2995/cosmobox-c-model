# Toy Model 0B — bande fréquentielle des événements et coût de bracketing

Statut : **validé pour gel en principe — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `temporal-event-solver.md`

Ce document précise la bande fréquentielle pertinente pour les événements construits à partir de `F=chi^2/4` et borne la portée des arguments fondés sur une densité moyenne de zéros.

## 1. Bande de chi

Pour un canal :

```math
\chi(t)=\sum_j C_j\sin(\omega_j t),
```

on définit une borne spectrale sûre :

```math
\Omega_\chi=\max_j\omega_j.
```

Lorsqu'on veut éviter toute dépendance à une tolérance déclarant certains poids `C_j` nuls, on peut utiliser la borne conservative :

```math
\Omega_{safe}=E_{max}-E_0,
```

ou une borne plus serrée uniquement si elle est obtenue par une règle de sélection analytique préenregistrée.

## 2. Bande des fonctions événement

La quantité scientifique est :

```math
F(t)=\chi(t)^2/4.
```

Les produits de sinus génèrent des fréquences :

```math
|\omega_j-\omega_k|
\qquad\text{et}\qquad
\omega_j+\omega_k.
```

Donc :

```math
\boxed{\Omega_F\le2\Omega_\chi.}
```

Les dérivées :

```text
F'
F''
F'''
```

ont le même support fréquentiel que `F` et sont donc également bornées par `2 Omega_chi`.

Par conséquent, pour les événements :

```text
T_peak  -> racine de F'
T_grow  -> extremum de F' / racine de F''
T_thr   -> racine de F-eta
T_down  -> racine de F-eta
```

l'échelle de demi-période la plus rapide est :

```math
\boxed{
t_{event}=\frac{\pi}{2\Omega_\chi}
}
```

ou, de façon conservative :

```math
\boxed{
t_{event,safe}=\frac{\pi}{2\Omega_{safe}}.}
```

La précédente échelle `pi/Omega_chi` reste naturelle pour `chi` elle-même, mais elle est trop grossière comme unité de départ pour les événements construits sur `F`.

## 3. Famille de bracketing

La famille sans dimension doit donc être exprimée sous la forme :

```math
\Delta t_k
=\beta_k\frac{\pi}{2\Omega_{scale}},
```

avec :

```text
Omega_scale = Omega_safe
```

par défaut, ou une borne active plus serrée si celle-ci est justifiée analytiquement sans seuil numérique sur les coefficients spectraux.

Les valeurs `beta_k` restent `OPEN`.

## 4. Densité de zéros : portée limitée

Une somme trigonométrique finie est une fonction entière de type exponentiel après prolongement complexe. Des résultats asymptotiques relient son type fréquentiel à une densité moyenne de zéros sous des hypothèses appropriées.

Cependant, une règle du type :

```math
N_{zero}([0,\tau])\lesssim\Omega\tau/\pi
```

ne constitue pas une borne finite-interval universelle suffisante pour certifier le protocole 0B.

Sur un intervalle fini, l'interférence peut produire :

```text
- plusieurs racines proches ;
- racines tangentielles ;
- cellules avec deux racines et même signe aux bords ;
- densité locale fortement non uniforme.
```

La quantité `Omega*tau/pi` peut être utilisée au plus comme **estimation de coût / ordre de grandeur** pour dimensionner un raffinement initial. Elle ne doit jamais être utilisée pour conclure que toutes les racines ont été trouvées.

## 5. Certification par bornes de dérivées

La complétude du bracketing doit reposer sur des bornes locales ou globales de dérivées des fonctions événement.

Pour :

```math
g(t)=F'(t),
```

ou :

```math
g(t)=F(t)-\eta,
```

on peut construire une borne :

```math
L\ge\sup_{cell}|g'(t)|.
```

Si la cellule est centrée en `t_c` et de demi-largeur `h` :

```math
|g(t_c)|>Lh
```

certifie l'absence de racine dans la cellule.

Les cellules non exclues doivent être subdivisées ou résolues explicitement. Les racines tangentielles exigent une logique adaptée aux dérivées supérieures et ne sont pas capturées par un simple changement de signe.

## 6. Conditionnement des événements

Une fois un événement localisé, le diagnostic de conditionnement est disponible sans nouvelle machinerie :

```text
T_thr  : |F'(T_thr)|
T_peak : |F''(T_peak)|
T_grow : |F'''(T_grow)| si obtenu via F''=0
```

Ces quantités sont évaluées par les mêmes sommes trigonométriques exactes en temps.

Le coût d'évaluation est donc faible relativement à la diagonalisation ; la difficulté résiduelle est la certification du premier événement et le conditionnement numérique, pas le calcul des dérivées temporelles.

## 7. Statut

```text
CHI_BANDWIDTH_SCALE                  = VALIDATED_FOR_FREEZE
F_EVENT_BANDWIDTH_FACTOR_TWO         = VALIDATED_FOR_FREEZE
EVENT_NATURAL_SCALE_PI_OVER_2OMEGA   = VALIDATED_FOR_FREEZE
ACTIVE_OMEGA_FROM_NUMERICAL_ZERO_CUT = REJECTED_AS_DEFAULT
SAFE_SPECTRAL_BANDWIDTH              = VALIDATED_FOR_FREEZE
ZERO_DENSITY_AS_COMPLETENESS_BOUND   = REJECTED
ZERO_DENSITY_AS_COST_HEURISTIC       = ALLOWED_WITH_SCOPE
DERIVATIVE_CELL_EXCLUSION            = VALIDATED_IN_PRINCIPLE
EVENT_CONDITIONING_NO_EXTRA_ENGINE   = VALIDATED_FOR_FREEZE
BETA_GRID_VALUES                     = OPEN
```
