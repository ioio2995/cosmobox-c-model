# Toy Model 0B — représentation spectrale exacte de la réponse de Kubo

Statut : **validé pour gel — support analytique / méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `short-time-oracles.md`, `path-purity-control.md`, `temporal-event-solver.md`, `sector-parity-selection.md`

Ce document exploite le caractère fini et réel du Toy Model 0B pour écrire la réponse de Kubo comme une somme trigonométrique finie. Il en déduit des formules exactes pour les moments de court temps et pour les intégrales sectorielles, et précise ce que cette structure autorise ou non pour le bracketing temporel et les oracles de symétrie.

## 1. Forme spectrale pour un fondamental pur

On fixe la convention scientifique :

```math
\chi_{pq}(t)
=i\langle\Omega|[n_p,n_q(t)]|\Omega\rangle,
\qquad
n_q(t)=e^{iHt}n_qe^{-iHt}.
```

Dans la base occupation-flux, `H` et les densités sont réels. Une base propre réelle peut donc être choisie. Pour un fondamental non dégénéré `|Omega>` d'énergie `E_0`, on définit :

```math
\omega_a=E_a-E_0>0.
```

Comme les éléments de matrice des densités sont réels :

```math
A_a^{pq}
=\langle\Omega|n_p|a\rangle
 \langle a|n_q|\Omega\rangle
\in\mathbb R.
```

La réponse vaut exactement :

```math
\boxed{
\chi_{pq}(t)
=-2\sum_{a:E_a>E_0}
A_a^{pq}\sin(\omega_a t)
}
```

avec la convention `chi = i<[n_p,n_q(t)]>` ci-dessus.

Le signe opposé apparaît si l'on définit temporairement des coefficients :

```math
c_a^{(+)}=+2A_a^{pq}.
```

Dans ce cas :

```math
\chi=-\sum_a c_a^{(+)}\sin(\omega_a t).
```

Le signe doit donc être fixé normativement avant implémentation ; il ne doit pas être absorbé silencieusement dans les coefficients.

L'absence exacte de cosinus est l'écriture spectrale de l'imparité :

```math
\chi_{pq}(-t)=-\chi_{pq}(t).
```

## 2. Forme invariante sous les dégénérescences excitées

Le coefficient associé à un vecteur propre individuel n'est pas invariant sous rotation de base dans un sous-espace excité dégénéré.

Pour chaque valeur propre `E=E_0+omega`, on note `P_E` son projecteur spectral et on définit :

```math
\boxed{
C_{pq}(\omega)
=-2\langle\Omega|n_p P_{E_0+\omega} n_q|\Omega\rangle.
}
```

Alors :

```math
\boxed{
\chi_{pq}(t)
=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
}
```

La somme porte sur les fréquences de Bohr distinctes actives. Cette représentation est indépendante du choix de base à l'intérieur des sous-espaces dégénérés.

## 3. Extension à l'état canonique dégénéré

Si le fondamental a une multiplicité `d_GS` et que la prescription canonique est :

```math
\rho=\frac{P_G}{d_{GS}},
```

avec `P_G` le projecteur sur l'espace fondamental d'énergie `E_0`, la même structure subsiste :

```math
\boxed{
C_{pq}(\omega)
=-\frac{2}{d_{GS}}
\operatorname{Tr}
\left(P_G n_p P_{E_0+\omega}n_q\right)
}
```

et :

```math
\chi_{pq}(t)
=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
```

Les transitions internes au sous-espace fondamental ont `omega=0` et ne contribuent pas à la réponse impaire.

Ainsi la forme trigonométrique finie ne dépend pas de la non-dégénérescence du fondamental ; elle dépend de la stationnarité de l'état canonique et de la réalité imposée par `K`.

## 4. Moments spectraux et court temps

Le développement :

```math
\sin(\omega t)
=\sum_{k\ge0}
\frac{(-1)^k(\omega t)^{2k+1}}{(2k+1)!}
```

entraîne :

```math
\chi_{pq}(t)
=\sum_{k\ge0}a_{2k+1}^{pq}t^{2k+1},
```

avec :

```math
\boxed{
a_{2k+1}^{pq}
=\frac{(-1)^k}{(2k+1)!}
\sum_{\omega>0}C_{pq}(\omega)\omega^{2k+1}.
}
```

Les coefficients de court temps sont donc des moments spectraux exacts. Aucune différence finie temporelle n'est requise.

On définit :

```math
M_{2k+1}^{pq}
=\sum_{\omega>0}C_{pq}(\omega)\omega^{2k+1}.
```

Alors l'exposant d'état `nu` est le plus petit ordre impair `2k+1` tel que :

```math
M_{2k+1}^{pq}\neq0.
```

En particulier :

```text
M1 != 0              -> nu = 1
M1 = 0               -> nu >= 3
M1 = 0 and M3 != 0   -> nu = 3
```

Il est incorrect d'écrire :

```text
M1 = 0 <=> nu = 3
```

sans vérifier le moment suivant.

## 5. Somme spectrale de l'oracle d'arête

Pour une arête `i,i+1`, l'oracle de commutateur déjà démontré donne :

```math
a_1^{(i,i+1)}=J\langle X_i\rangle.
```

La représentation spectrale impose donc le sum rule exact :

```math
\boxed{
\sum_{\omega>0}
C_{i,i+1}(\omega)\omega
=J\langle X_i\rangle.
}
```

Ce sum rule relie directement :

```text
- l'assemblage du Hamiltonien ;
- la diagonalisation ;
- les éléments de matrice des densités ;
- la convention de signe de Kubo ;
- l'oracle statique de court temps.
```

Il constitue un oracle end-to-end très fort avant toute extraction d'événement temporel.

La qualification indépendante au point de référence a reproduit cette identité à environ `1e-15` sur l'arête `(0,1)` à une convention de signe temporaire des coefficients près.

## 6. Réponse sectorielle

Toute projection linéaire préenregistrée de la réponse sur un secteur opératoriel fini reste une somme finie de phases spectrales.

Après appariement physique par adjonction et usage de `K`, chaque canal sectoriel physique `[alpha]` possède une représentation de la forme :

```math
\chi_\alpha(t)
=\sum_j C_{\alpha j}\sin(\omega_{\alpha j}t),
```

avec coefficients réels après regroupement approprié.

L'imparité sectorielle déjà démontrée est donc visible directement dans la représentation spectrale : aucun cosinus physique n'est requis.

Les moments spectraux sectoriels fournissent les coefficients `c_alpha` utilisés dans la limite de pureté de chemin sans dérivation numérique en temps.

## 7. Intégrales sectorielles exactes

Pour :

```math
P_\alpha(\tau)
=\int_0^\tau\chi_\alpha(t)^2dt,
```

et :

```math
\chi_\alpha(t)
=\sum_jC_j\sin(\omega_j t),
```

on obtient exactement :

```math
P_\alpha(\tau)
=\sum_{j,k}C_jC_k\,I(\omega_j,\omega_k;\tau),
```

avec :

```math
I(u,v;\tau)
=\frac12\left[
\frac{\sin((u-v)\tau)}{u-v}
-
\frac{\sin((u+v)\tau)}{u+v}
\right],
```

et la convention continue :

```math
\frac{\sin((u-v)\tau)}{u-v}\to\tau
\quad\text{lorsque}\quad u=v.
```

Ainsi :

```math
I(u,u;\tau)
=\frac{\tau}{2}
-
\frac{\sin(2u\tau)}{4u}.
```

Les quantités :

```text
P_direct
P_winding
P_non_target
P_sector
Purity_direct
```

peuvent donc être calculées sans quadrature temporelle.

La quadrature peut rester un test de régression indépendant, mais elle n'est pas l'estimateur scientifique nominal.

## 8. Fréquence maximale active et échelle de bracketing

On définit :

```math
\omega_{max}^{pq}
=\max\{\omega>0:C_{pq}(\omega)\neq0\}.
```

Une échelle temporelle naturelle est :

```math
\boxed{
t_\omega=\frac{\pi}{\omega_{max}}.
}
```

Elle fixe la demi-période de la composante active la plus rapide et fournit une unité sans dimension naturelle pour une famille de bracketing :

```math
\Delta t_k=\beta_k\frac{\pi}{\omega_{max}},
```

avec une famille préenregistrée `beta_k` décroissante.

Cependant :

```text
Delta t <= pi/omega_max
```

n'est **pas** à lui seul une preuve que toutes les racines ou tous les extrema sont bracketés.

Une somme band-limitée peut présenter :

- deux racines dans une même cellule avec le même signe aux extrémités ;
- une racine tangentielle sans changement de signe ;
- des extrema proches produits par interférence.

`omega_max` fournit donc une **échelle de raffinement**, pas un certificat de complétude du simple test de signes.

## 9. Vers un bracketing certifiable

La représentation spectrale donne également des bornes exactes simples sur les dérivées :

```math
|\chi^{(r)}(t)|
\le
\sum_\omega |C(\omega)|\omega^r.
```

Ces bornes peuvent être utilisées avec subdivision adaptative pour exclure des cellules ne pouvant contenir de racine d'une fonction événement donnée.

Par exemple, si `g(t)` est une fonction événement et qu'une borne `L >= sup |g'(t)|` est disponible sur une cellule centrée en `t_c` de demi-largeur `h`, alors :

```math
|g(t_c)|>Lh
```

certifie qu'aucune racine de `g` n'appartient à cette cellule.

Les cellules non exclues sont subdivisées ou traitées par solveur continu. Cette approche permet de transformer le raffinement en contrôle quantifiable plutôt qu'en simple heuristique.

La stratégie exacte de certification et les valeurs `beta_k` restent `OPEN` pour le lot numérique.

## 10. Nombre de termes non nuls et symétrie

Le nombre brut de coefficients propres individuels non nuls :

```text
# {a : c_a != 0}
```

n'est pas un invariant lorsqu'un niveau excité est dégénéré : une rotation de base dans le sous-espace propre peut redistribuer les coefficients individuels.

L'objet invariant est le poids groupé :

```math
C_{pq}(\omega)
=-2\langle\Omega|n_pP_{E_0+\omega}n_q|\Omega\rangle
```

ou sa généralisation canonique.

Même le nombre de fréquences actives groupées ne constitue un **oracle de symétrie** qu'après démonstration analytique des secteurs / représentations autorisés et interdits. Des annulations accidentelles peuvent autrement modifier ce nombre.

La valeur observée de `42` coefficients propres non nuls sur `77` états excités à la référence est donc une **empreinte numérique de qualification**, pas encore un oracle structurel gelé.

Un futur oracle de support spectral devra être formulé en termes de projecteurs spectraux et de règles de sélection démontrées, jamais en termes d'un choix arbitraire de vecteurs propres dans un sous-espace dégénéré.

## 11. Conditionnement numérique : le goulot ne disparaît pas

L'évaluation analytique en temps supprime :

```text
- les différences finies temporelles ;
- l'interpolation comme estimateur final ;
- la quadrature des P_alpha.
```

Elle ne réduit pas automatiquement l'erreur globale à l'epsilon machine.

Les sources restantes incluent :

```text
- résidus de diagonalisation et défaut d'orthogonalité des vecteurs / projecteurs ;
- conditionnement des sous-espaces proches ou dégénérés ;
- erreurs sur les fréquences de Bohr accumulées en phase comme delta_omega * t ;
- annulations dans les sommes spectrales ;
- conditionnement des racines / extrema temporels.
```

Pour une racine simple :

```math
g(t_*)=0,
```

une perturbation `delta g` produit au premier ordre :

```math
|\delta t_*|
\sim
\frac{|\delta g(t_*)|}{|g'(t_*)|}.
```

Ainsi les diagnostics naturels sont :

```text
T_thr  : |F'(T_thr)|
T_peak : |F''(T_peak)|, puisque la racine porte sur F'
T_grow : |F'''(T_grow)| lorsque le candidat est obtenu par F''=0
```

Des pentes / courbures faibles rendent l'événement intrinsèquement mal conditionné même avec une représentation spectrale exacte en forme.

Le budget numérique doit donc être établi à partir de résidus spectraux, de la stabilité en précision et du conditionnement des événements, et non supposé égal à quelques `1e-15`.

## 12. Statut

```text
KUBO_FINITE_SINE_REPRESENTATION       = VALIDATED_FOR_FREEZE
KUBO_SPECTRAL_SIGN_CONVENTION         = VALIDATED_FOR_FREEZE
DEGENERATE_GS_PROJECTOR_FORM           = VALIDATED_FOR_FREEZE
BASIS_INVARIANT_FREQUENCY_WEIGHTS      = VALIDATED_FOR_FREEZE
SHORT_TIME_SPECTRAL_MOMENTS            = VALIDATED_FOR_FREEZE
M1_ZERO_IMPLIES_NU_GE_3                = VALIDATED_FOR_FREEZE
M1_ZERO_IFF_NU_EQ_3                    = REJECTED
EDGE_SPECTRAL_SUM_RULE                 = VALIDATED_FOR_FREEZE
SECTOR_SINE_REPRESENTATION             = VALIDATED_FOR_FREEZE
SECTOR_PURITY_ANALYTIC_INTEGRAL        = VALIDATED_FOR_FREEZE
OMEGA_MAX_BRACKETING_SCALE             = VALIDATED_FOR_FREEZE
OMEGA_MAX_SIGN_GRID_COMPLETENESS        = REJECTED
SPECTRAL_DERIVATIVE_BOUNDS             = VALIDATED_IN_PRINCIPLE
RAW_NONZERO_EIGENVECTOR_COUNT_ORACLE   = REJECTED
GROUPED_SPECTRAL_SUPPORT_ORACLE         = OPEN_PENDING_SYMMETRY_DERIVATION
MACHINE_EPSILON_GLOBAL_ERROR_ASSUMPTION= REJECTED
```
