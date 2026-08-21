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

Avant ce maximum, `chi` conserve le signe de son premier coefficient court non nul. Un zéro de `chi` est un minimum de `F`, pas un pic. Pour un candidat avec `chi != 0` :

```math
F'(T_{peak})=0
\quad\Longleftrightarrow\quad
\chi'(T_{peak})=0.
```

Pour un maximum strict non dégénéré il faut en plus :

```math
\boxed{\chi(T_{peak})\chi''(T_{peak})<0.}
```

La condition `chi != 0` et `chi'' != 0` seule n'est pas suffisante : si `chi chi'' > 0`, le point est un minimum local non nul de `F`. Si `chi''=0`, le protocole revient à la définition scientifique par changement de signe de `F'` et/ou aux dérivées supérieures.

La fonction de certification nominale de `T_peak` est donc `chi'`, dont la bande reste `Omega_chi`.

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

sur ce lobe, les croisements sont les racines de :

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

Valeurs numériques préenregistrées :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}
```

`beta` contrôle uniquement le maillage initial de certification / bracketing ; ce n'est pas une tolérance sur le temps final, obtenu par le solveur spectral continu. `beta=1` correspond à une demi-période de la bande maximale de la fonction de certification ; raffinement dyadique imbriqué ; `beta=1/8` donne une phase maximale `pi/8` par cellule à la bande limite. Aucune finesse supplémentaire n'est requise comme garantie de complétude, celle-ci reposant sur l'exclusion certifiée des cellules, leur subdivision adaptative et le solveur continu.

Critère de contrôle sous raffinement : identité du premier événement stable, ordre des candidats pertinents stable, aucune cellule antérieure non résolue, temps continus compatibles selon les tolérances numériques (`OPEN`). Sinon : `TIME_EVENT_CONTROL_SENSITIVE`.

## 4. Pourquoi certifier sur chi / chi' plutôt que sur F'

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

Le gain de la formulation en `chi` n'est **pas** un meilleur conditionnement intrinsèque de la même racine. Si deux formulations vérifient localement `g_2=k g_1` avec `k(t*) != 0`, la pente et l'erreur de fonction sont multipliées par le même facteur au premier ordre lorsque le modèle d'erreur est propagé correctement, et le déplacement de racine est inchangé.

Les avantages réels sont :

- des bornes de dérivées directes et plus serrées ;
- un modèle d'erreur spectral directement exprimable sur `chi` et ses dérivées ;
- l'absence des zéros parasites de `F'` dus à `chi=0` ;
- une bande `Omega_chi` pour `T_peak`, `T_thr` et `T_down`.

## 5. Densité de zéros : portée limitée

Une somme trigonométrique finie est une fonction entière de type exponentiel après prolongement complexe. Des résultats asymptotiques relient son type fréquentiel à une densité moyenne de zéros sous des hypothèses appropriées.

Cependant, une règle du type :

```math
N_{zero}([0,\tau])\sim O(\Omega\tau/\pi)
```

ne constitue pas une borne universelle sur intervalle fini suffisante pour certifier le protocole 0B.

La quantité `Omega*tau/pi` peut être utilisée au plus comme estimation de coût / ordre de grandeur pour dimensionner un raffinement initial. Elle ne doit jamais être utilisée pour conclure que toutes les racines ont été trouvées.

## 6. Certification par bornes de dérivées

On pose :

```math
S_r=\sum_\omega |C_\omega|\omega^r,
```

ce qui donne :

```math
|\chi^{(r)}(t)|\le S_r.
```

Pour toute fonction de certification `g(t)`, si une cellule est centrée en `t_c` avec demi-largeur `h` et si :

```math
L\ge\sup_{cell}|g'(t)|,
```

alors :

```math
|g(t_c)|>Lh
```

certifie l'absence de racine dans la cellule.

Pour les événements simples :

```text
T_thr/down -> g'=chi'  : L <= S_1
T_peak     -> g'=chi'' : L <= S_2
```

Pour :

```math
H_{grow}=\chi'^2+\chi\chi'',
```

on a :

```math
H_{grow}'=3\chi'\chi''+\chi\chi'''=2F'''.
```

Une borne sûre est donc :

```math
\boxed{
\sup|H_{grow}'|
\le3S_1S_2+S_0S_3.
}
```

Cette borne produit-de-sommes est généralement plus lâche que les bornes linéaires `S_1` ou `S_2`. `T_grow` paie donc deux fois : par sa bande jusqu'à `2 Omega_chi` et par une certification composite potentiellement beaucoup plus coûteuse en subdivisions.

La famille commune `B` reste valide ; elle n'implique pas un coût uniforme entre estimateurs.

## 7. Conditionnement des racines

Pour une racine simple de `g(t*)=0`, le déplacement au premier ordre est contrôlé par :

```math
|\delta t_*|
\sim
\frac{|\delta g(t_*)|}{|g'(t_*)|}.
```

Le protocole doit donc associer à la pente locale une borne ou estimation de l'erreur sur la fonction réellement évaluée. Une pente brute n'est pas, à elle seule, un nombre de conditionnement invariant.

Les fonctions résolues sont :

```text
T_thr/down -> g = chi - s 2 sqrt(eta)
T_peak     -> g = chi'
T_grow     -> g = H_grow
```

Les pentes locales correspondantes peuvent être publiées :

```text
T_thr/down -> |chi'|
T_peak     -> |chi''|
T_grow     -> |H_grow'|
```

mais le diagnostic de précision sur le temps doit utiliser le rapport `error_on_g / |g'|`.

Pour les seuils, l'ancienne affirmation selon laquelle la formulation en `F` introduirait artificiellement un facteur `sqrt(eta)` dans le conditionnement est rejetée : ce facteur multiplie simultanément la pente et l'erreur propagée et s'annule au premier ordre.

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
PEAK_NONDEGENERATE_CRITERION            = chi*chi'' < 0
SQRT_ETA_CONDITIONING_PENALTY           = REJECTED
ROOT_ERROR_NORMALIZATION_REQUIRED       = VALIDATED_FOR_FREEZE
HGROW_DERIVATIVE_BOUND                  = 3 S1 S2 + S0 S3
GROW_COMPOSITE_CERTIFICATION_COST       = VALIDATED_FOR_FREEZE
ACTIVE_OMEGA_FROM_NUMERICAL_ZERO_CUT    = REJECTED_AS_DEFAULT
SAFE_SPECTRAL_BANDWIDTH                 = VALIDATED_FOR_FREEZE
ZERO_DENSITY_AS_COMPLETENESS_BOUND      = REJECTED
ZERO_DENSITY_AS_COST_HEURISTIC          = ALLOWED_WITH_SCOPE
DERIVATIVE_CELL_EXCLUSION               = VALIDATED_IN_PRINCIPLE
BETA_GRID_VALUES                        = VALIDATED_FOR_FREEZE
```
