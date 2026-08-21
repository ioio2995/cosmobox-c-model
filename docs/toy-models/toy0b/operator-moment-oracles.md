# Toy Model 0B — moments opératoriels sans spectre excité

Statut : **validé pour gel — support analytique / méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `short-time-oracles.md`, `derivative-error-budget.md`

Ce document reformule les moments spectraux de la réponse de Kubo comme des espérances d'opérateurs agissant uniquement sur le sous-espace fondamental. Cette fermeture supprime toute dépendance au choix de base dans les sous-espaces excités dégénérés pour les oracles de court temps.

## 1. Convention spectrale

On fixe :

```math
\chi_{pq}(t)
=i\,\mathrm{Tr}\!\left(\rho[n_p,n_q(t)]\right).
```

Pour un fondamental pur `|Omega>` et des projecteurs spectraux excités `P_{E_0+omega}`, les poids invariants sont :

```math
C_{pq}(\omega)
=-2\langle\Omega|n_pP_{E_0+\omega}n_q|\Omega\rangle,
```

et :

```math
\chi_{pq}(t)=\sum_{\omega>0}C_{pq}(\omega)\sin(\omega t).
```

Si l'on utilise temporairement les coefficients opposés :

```math
c^{(+)}(\omega)=+2\langle\Omega|n_pP_{E_0+\omega}n_q|\Omega\rangle,
```

alors :

```math
\chi_{pq}(t)=-\sum_\omega c^{(+)}(\omega)\sin(\omega t).
```

Les moments numériques doivent toujours annoncer la convention utilisée. Les signes ne doivent pas être mélangés entre les deux conventions.

## 2. Fermeture opératorielle des moments

Pour `r>=1`, on définit le moment spectral normatif :

```math
M_r^{pq}=\sum_{\omega>0}C_{pq}(\omega)\omega^r.
```

Comme les projecteurs spectraux résolvent `H-E_0` sur le complément du fondamental :

```math
\boxed{
M_r^{pq}
=-2\langle\Omega|
 n_p(H-E_0)^r n_q
|\Omega\rangle.
}
```

Et puisque :

```math
(H-E_0)^r n_q|\Omega\rangle
=\operatorname{ad}_H^r(n_q)|\Omega\rangle,
```

on peut aussi écrire :

```math
\boxed{
M_r^{pq}
=-2\langle\Omega|
 n_p\operatorname{ad}_H^r(n_q)
|\Omega\rangle.
}
```

Ces identités ne nécessitent aucun vecteur propre excité.

Avec la convention temporaire `c^(+)=-C`, les moments ont naturellement le signe opposé :

```math
M_r^{(+)}=+2\langle\Omega|n_p(H-E_0)^r n_q|\Omega\rangle=-M_r.
```

La qualification numérique communiquée pour l'arête `(0,1)` avec :

```text
moment 1 = -0.586308472495237
moment 3 = -7.235888096529
```

correspond donc à la convention temporaire `c^(+)`, et non aux poids normatifs `C` de `exact-spectral-response.md`.

## 3. État canonique dégénéré

Si le fondamental a une multiplicité `d_GS` et :

```math
\rho=\frac{P_G}{d_{GS}},
```

alors pour `r>=1` :

```math
\boxed{
M_r^{pq}
=-\frac{2}{d_{GS}}
\operatorname{Tr}\!\left[
P_G n_p(H-E_0)^r n_q
\right].
}
```

On peut insérer `P_G` à droite sous la trace sans changer la valeur. La fermeture opératorielle reste donc valide pour la prescription canonique dégénérée et reste indépendante de tout choix de base dans les sous-espaces excités.

## 4. Coefficients de court temps

Pour les moments normatifs :

```math
\chi_{pq}(t)
=\sum_{k\ge0}a_{2k+1}^{pq}t^{2k+1},
```

avec :

```math
\boxed{
a_{2k+1}^{pq}
=\frac{(-1)^k}{(2k+1)!}M_{2k+1}^{pq}.
}
```

Ainsi les coefficients courts peuvent être obtenus par applications successives de `H-E_0` ou par commutateurs emboîtés, sans diagonalisation du spectre excité et sans différences finies temporelles.

Pour une arête régulière :

```math
M_1^{i,i+1}=J\langle X_i\rangle
```

avec la convention normative `C`.

## 5. Détermination de l'exposant nu

Structurellement :

```text
M1 != 0                         -> nu = 1
M1 = 0                          -> nu >= 3
M1 = 0 and M3 != 0             -> nu = 3
M1 = M3 = 0 and M5 != 0        -> nu = 5
...
```

La formulation opératorielle supprime le problème de regroupement des fréquences et la dépendance aux rotations dans les sous-espaces excités dégénérés.

Elle ne transforme cependant pas un calcul flottant en preuve exacte de nullité. Une valeur numérique très petite de `M_r` exige encore :

- soit une annulation analytique démontrée par symétrie / sélection ;
- soit une règle numérique de zéro préenregistrée et un contrôle de précision ;
- soit, lorsque disponible, un calcul exact ou à précision arbitraire.

Donc :

```text
EXCITED_DEGENERACY_TOLERANCE_FOR_MOMENTS = NOT_REQUIRED
NUMERICAL_ZERO_TOLERANCE_FOR_UNPROVEN_MOMENT = STILL_REQUIRED
```

La détermination de `nu` est exacte lorsqu'une suite suffisante d'annulations est établie analytiquement et que le premier moment non nul est résolu. Elle n'est pas automatiquement exacte par la seule utilisation d'arithmétique flottante.

## 6. Séparation des budgets numériques

La fermeture opératorielle permet de distinguer trois blocs.

### A. Bloc court / opératoriel

Peuvent être calculés à partir du fond canonique et d'opérations sur `H` :

```text
C_short
moments M_{2k+1}
regularite d'arete
exposants nu, sous les regles de zero ci-dessus
coefficients asymptotiques sectoriels accessibles par projection opératorielle
<Phi>
```

Ce bloc n'hérite pas :

```text
- des rotations de base dans les sous-espaces excités ;
- du regroupement des fréquences quasi-dégénérées ;
- des erreurs de phase delta_omega * t.
```

Il hérite encore de l'erreur sur le fond canonique, `E_0`, les produits d'opérateurs et les annulations numériques.

### B. Bloc statique spectral bas

Le collapse SOFT-LOOP du gap et l'échelle :

```math
\delta_c=gap_0/(6g)
```

requièrent le premier niveau excité. Ils ne nécessitent pas le spectre complet ni une évolution temporelle, mais ils restent soumis à la précision du calcul du gap.

Ainsi il est incorrect de classer `gap(delta)/gap_0` comme observable dépendant du seul état fondamental.

### C. Bloc dynamique spectral complet

Les événements :

```text
T_peak
T_grow
T_thr
T_down
Delta1_grow
Delta1_thr
```

et les intégrales sectorielles exactes en temps utilisent la représentation spectrale complète / sectorielle et supportent le budget de conditionnement dynamique :

```text
- erreurs de fréquences de Bohr ;
- conditionnement des projecteurs spectraux ;
- annulations dans les sommes trigonométriques ;
- erreurs de phase accumulées ;
- conditionnement des racines et extrema.
```

Le budget `DELTA1_ERROR_BUDGET` doit donc être construit sur ce bloc dynamique et ne doit pas être appliqué indistinctement aux oracles courts.

## 7. Conséquence pour l'implémentation future

L'implémentation devra fournir deux chemins indépendants pour les premiers moments sur des points-oracles :

```text
MOMENT_OPERATOR_PATH
MOMENT_SPECTRAL_PATH
```

et vérifier leur accord avec la convention de signe déclarée.

Cette redondance teste simultanément :

```text
- l'assemblage de H ;
- l'état fondamental ;
- la représentation spectrale ;
- les matrices de densité ;
- la convention Kubo.
```

Aucun code 0B n'est autorisé par ce document ; il s'agit d'une exigence future de validation.

## 8. Statut

```text
OPERATOR_MOMENT_CLOSURE_PURE            = VALIDATED_FOR_FREEZE
OPERATOR_MOMENT_CLOSURE_CANONICAL       = VALIDATED_FOR_FREEZE
MOMENT_EXCITED_BASIS_INVARIANCE         = VALIDATED_FOR_FREEZE
SHORT_TIME_NO_EXCITED_SPECTRUM_REQUIRED = VALIDATED_FOR_FREEZE
MOMENT_SIGN_CONVENTION                   = VALIDATED_FOR_FREEZE
FLOATING_POINT_MOMENT_ZERO_IS_EXACT      = REJECTED
NU_NO_DEGENERACY_GROUPING_REQUIRED       = VALIDATED_FOR_FREEZE
NU_NUMERICAL_ZERO_TOLERANCE_ELIMINATED   = REJECTED
STATIC_GAP_GROUND_ONLY                   = REJECTED
NUMERICAL_BUDGET_BLOCK_SPLIT             = VALIDATED_FOR_FREEZE
MOMENT_OPERATOR_SPECTRAL_CROSSCHECK      = MANDATORY_FUTURE_VALIDATION
```
