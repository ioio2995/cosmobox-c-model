# Toy Model 0B — moments opératoriels sans spectre excité

Statut : **validé pour gel — support analytique / méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `exact-spectral-response.md`, `short-time-oracles.md`, `sector-parity-selection.md`, `path-grading.md`, `zero-grade-self-adjoint-sector.md`, `derivative-error-budget.md`

Ce document reformule les moments spectraux de la réponse de Kubo comme des espérances d'opérateurs agissant uniquement sur le sous-espace fondamental. Cette fermeture supprime toute dépendance au choix de base dans les sous-espaces excités dégénérés pour les oracles de court temps.

## 1. Conventions

On fixe :

```math
\chi_{pq}(t)
=i\,\mathrm{Tr}\!\left(\rho[n_p,n_q(t)]\right).
```

Pour éviter toute ambiguïté avec le générateur de Krylov, on définit explicitement :

```math
\operatorname{ad}_H(O):=[H,O].
```

La spécification utilise par ailleurs le Liouvillien hermitien-réel :

```math
\mathcal L_H(O)=i[H,O]=i\,\operatorname{ad}_H(O).
```

Donc :

```math
\operatorname{ad}_H^r=(-i)^r\mathcal L_H^r,
```

et :

```math
n_q(t)
=\sum_{r\ge0}\frac{(it)^r}{r!}\operatorname{ad}_H^r(n_q)
=\sum_{r\ge0}\frac{t^r}{r!}\mathcal L_H^r(n_q).
```

Aucun facteur `i^r` ne doit être transporté implicitement entre les deux conventions.

## 2. Fermeture opératorielle des moments totaux

Pour un fondamental pur `|Omega>` et les poids spectraux normatifs :

```math
C_{pq}(\omega)
=-2\langle\Omega|n_pP_{E_0+\omega}n_q|\Omega\rangle,
```

on définit pour `r>=1` :

```math
M_r^{pq}=\sum_{\omega>0}C_{pq}(\omega)\omega^r.
```

La résolution spectrale de `H-E_0` donne :

```math
\boxed{
M_r^{pq}
=-2\langle\Omega|
 n_p(H-E_0)^r n_q
|\Omega\rangle.
}
```

Le shell `omega=0` ne contribue pas pour `r>=1` parce qu'il est multiplié par `omega^r`.

Par récurrence :

```math
(H-E_0)^r n_q|\Omega\rangle
=\operatorname{ad}_H^r(n_q)|\Omega\rangle.
```

Donc :

```math
\boxed{
M_r^{pq}
=-2\langle\Omega|
 n_p\operatorname{ad}_H^r(n_q)
|\Omega\rangle.
}
```

Ces identités ne nécessitent aucun vecteur propre excité.

Le facteur `-2` n'est pas produit par l'annulation du shell `omega=0`. Il provient de la recombinaison des deux termes du commutateur, dont les amplitudes sont reliées par réalité / transposition dans la base `K`-réelle déclarée.

Avec la convention temporaire opposée :

```math
c^{(+)}=-C,
```

les moments changent de signe. Les valeurs de qualification :

```text
-0.586308472495237
-7.235888096529
```

communiquées avec `c^(+)` correspondent donc aux opposés des moments normatifs `M_1` et `M_3`.

## 3. État canonique dégénéré : trois ingrédients distincts

Si :

```math
\rho=\frac{P_G}{d_{GS}},
```

la représentation canonique exige trois étapes qui ne doivent pas être confondues.

### 3.1 Résolution en projecteurs spectraux

La réponse est d'abord décomposée sur les shells d'énergie `P_E` exactement comme dans le cas pur, avec une trace sur `P_G/d_GS`.

### 3.2 Shell de fréquence nulle

Les transitions internes au multiplet fondamental ont `omega=0`. Leur contribution au commutateur s'annule exactement car :

```math
\mathrm{Tr}(P_G n_p P_G n_q)
-
\mathrm{Tr}(P_G n_q P_G n_p)
=0
```

par cyclicité de la trace sur le sous-espace fondamental.

Pour les moments avec `r>=1`, le même shell est de toute façon tué par :

```math
(H-E_0)^rP_G=0.
```

Cette dernière identité explique l'absence du shell nul dans les moments; elle ne constitue pas à elle seule la dérivation de la formule complète.

### 3.3 Facteur -2

Dans la base réelle, la transposition relie les deux amplitudes `p,q` et `q,p` des shells `omega>0`. Leur recombinaison dans le commutateur donne le facteur `-2` de la forme en sinus et des moments normatifs.

On obtient finalement :

```math
\boxed{
M_r^{pq}
=-\frac{2}{d_{GS}}
\operatorname{Tr}\!\left[
P_G n_p(H-E_0)^r n_q
\right],
\qquad r\ge1.
}
```

La fermeture opératorielle canonique est donc indépendante de tout choix de base dans le multiplet fondamental ou les sous-espaces excités.

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

Les coefficients courts peuvent donc être obtenus sans spectre excité et sans différences finies temporelles.

### Portée de l'oracle d'arête

L'identité :

```math
M_1=J\langle X\rangle
```

n'est pas une identité générale pour toute paire `(p,q)`.

Pour une arête non orientée :

```text
{p,q}={i,i+1}
```

on a :

```math
\boxed{M_1^{pq}=J\langle X_i\rangle.}
```

Pour :

```math
d(p,q)\ge2,
```

la localité impose :

```math
\boxed{M_1^{pq}=0.}
```

Il est donc interdit d'écrire sans quantificateur `M_1^{pq}=<X_p>`.

La qualification énergétique au point de référence fournit un contrôle indépendant du signe :

```math
E_0
=\left\langle\sum_iE_i^2\right\rangle
-\sum_i\langle X_i\rangle
```

pour `g=1, mu=delta=0`. Avec les six arêtes équivalentes par la symétrie du fond, le signe positif de `<X_i>` restitue une énergie électrique positive, contrairement au signe opposé.

L'observation de corrélations croisées positives entre liens à ce point est compatible avec Gauss, mais leur signe positif n'est pas élevé ici au rang de théorème général de Gauss.

## 5. Détermination de l'exposant nu et provenance des zéros

Structurellement :

```text
M1 != 0                         -> nu = 1
M1 = 0                          -> nu >= 3
M1 = 0 and M3 != 0             -> nu = 3
M1 = M3 = 0 and M5 != 0        -> nu = 5
...
```

La formulation opératorielle supprime le regroupement de fréquences et les rotations dans les multiplets excités.

Elle ne transforme pas un calcul flottant en preuve exacte de nullité.

Les zéros exacts doivent être rattachés aux règles structurelles déjà déclarées, notamment :

```text
- localité des commutateurs emboîtés ;
- K_SECTOR_ODDNESS ;
- BIPARTITE_WORD_PARITY ;
- EVEN_DISTANCE_ODD_DIAG_RULE ;
- ODD_DISTANCE_EVEN_DIAG_RULE.
```

Aucun second vocabulaire parallèle de « zéros de moments » n'est créé.

Pour un moment dont l'annulation n'est pas démontrée par ces règles, une règle numérique de zéro préenregistrée et un contrôle de précision restent nécessaires.

## 6. Moments sectoriels et imparité canal par canal

Le projecteur :

```math
\Pi_{\mathbf m}
```

est un projecteur **dans l'espace d'opérateurs** sur le multigrade conjoint des `E_i`; ce n'est pas un projecteur spectral de Hilbert.

Pour :

```math
O_{\mathbf m,r}
=\Pi_{\mathbf m}\operatorname{ad}_H^r(n_q),
```

on définit :

```math
B_{\mathbf m,r}^{pq}
=\mathrm{Tr}\left(\rho[n_p,O_{\mathbf m,r}]\right).
```

L'hermiticité donne pour tout `r` :

```math
\boxed{
B_{-\mathbf m,r}^{pq}
=(-1)^{r+1}\overline{B_{\mathbf m,r}^{pq}}.
}
```

Dans la base `K`-réelle déclarée, `B_{m,r}` est réel pour tout `r`. Donc pour `m != 0` :

```text
r pair   -> B_-m,r = -B_m,r
r impair -> B_-m,r = +B_m,r
```

et la recombinaison du canal physique `{m,-m}` donne :

```math
\boxed{a_{r,[\mathbf m]}^{pq}=0,\qquad r\;pair.}
```

Pour `r` impair :

```math
\boxed{
a_{r,[\mathbf m]}^{pq}
=
\frac{2i^{r+1}}{r!}
B_{\mathbf m,r}^{pq}
=
\frac{2(-1)^{(r+1)/2}}{r!}
B_{\mathbf m,r}^{pq},
\qquad \mathbf m\neq0.
}
```

L'annulation des ordres pairs est donc exactement la version en moments de `K_SECTOR_ODDNESS`; elle a lieu canal par canal, sans compensation intersectorielle.

Il est interdit de réutiliser sectoriellement la formule totale :

```math
-2\langle n_p(H-E_0)^r n_q\rangle
```

avec un `Pi_m` inséré naïvement.

### 6.1 Cas auto-conjugué m=0

La paire `{m,-m}` possède un seul élément pour :

```math
\mathbf m=\mathbf0.
```

Dans une graduation générique, ce cas demanderait un facteur un et non deux.

Dans le secteur physique de 0B, on a cependant le théorème plus fort démontré dans `zero-grade-self-adjoint-sector.md` : les valeurs des six `E_i` déterminent entièrement `n` par Gauss, donc chaque sous-espace propre conjoint des `E_i` est unidimensionnel. Ainsi :

```math
\Pi_{\mathbf0}(O)
```

est diagonal dans la base physique et :

```math
[n_p,\Pi_{\mathbf0}(O)]=0.
```

Par conséquent :

```math
\boxed{B_{\mathbf0,r}^{pq}=0}
```

pour tout `r`, et :

```math
\boxed{\chi_{[\mathbf0]}^{pq}(t)=0}
```

exactement.

Le canal auto-conjugué n'apporte donc aucune correction numérique à la pureté de chemin 0B, sous réserve que l'implémentation future ne le double-compte pas artificiellement.

## 7. Séparation des budgets numériques

La fermeture opératorielle permet de distinguer trois blocs.

### A. Bloc court / opératoriel

Peuvent être calculés à partir du fond canonique et d'opérations sur `H` :

```text
C_short
moments M_{2k+1}
regularite d'arete
exposants nu, sous les règles structurelles / numériques ci-dessus
coefficients sectoriels courts via commutateur projeté
<Phi>
```

Ce bloc n'hérite pas des rotations de base dans les sous-espaces excités, du regroupement des fréquences quasi-dégénérées ni des erreurs de phase `delta_omega*t`.

Il hérite encore de l'erreur sur le fond canonique, `E_0`, les produits d'opérateurs et les annulations numériques.

### B. Bloc statique spectral bas

Le collapse SOFT-LOOP du gap et :

```math
\delta_c=gap_0/(6g)
```

requièrent le premier niveau excité. Ce bloc est léger en **coût spectral**, mais il n'est pas exempt de budget de précision : son conditionnement dépend précisément de `gap_0`.

Pour les points SOFT-LOOP déjà divulgués à `g=1` :

```text
mu=-1.25 -> gap ~= 0.104
mu=-1.50 -> gap ~= 0.052
mu=-2.00 -> gap ~= 0.015
```

ces gaps restent numériquement confortables en double précision dans la qualification actuelle, sans que cela constitue encore une borne préenregistrée d'erreur. L'extrapolation vers des `mu` beaucoup plus négatifs n'appartient pas à la sous-campagne nominale et demanderait un contrôle de précision renforcé.

### C. Bloc dynamique spectral complet

Les événements temporels, `Delta1_grow`, `Delta1_thr` et les intégrales sectorielles finies utilisent la représentation spectrale complète / sectorielle et supportent le budget de conditionnement dynamique : fréquences de Bohr, projecteurs, annulations, phases accumulées et conditionnement des racines / extrema.

Le budget `DELTA1_ERROR_BUDGET` doit être construit sur ce bloc dynamique et ne doit pas être appliqué indistinctement aux oracles courts.

## 8. Validation future

L'implémentation devra fournir deux chemins indépendants pour les premiers moments sur des points-oracles :

```text
MOMENT_OPERATOR_PATH
MOMENT_SPECTRAL_PATH
```

et vérifier leur accord avec la convention de signe déclarée.

Elle devra aussi vérifier numériquement, comme oracle structurel :

```text
ZERO_GRADE_KUBO_CHANNEL = 0
EVEN_SECTOR_MOMENTS = 0
```

avec les tolérances numériques préenregistrées, sans remplacer les preuves analytiques correspondantes.

Aucun code 0B n'est autorisé par ce document.

## 9. Statut

```text
AD_H_CONVENTION                         = COMMUTATOR_WITHOUT_I
KRYLOV_LIOUVILLIAN_RELATION             = L_H = i AD_H
OPERATOR_MOMENT_CLOSURE_PURE            = VALIDATED_FOR_FREEZE
OPERATOR_MOMENT_CLOSURE_CANONICAL       = VALIDATED_FOR_FREEZE
CANONICAL_ZERO_FREQUENCY_TRACE_LEMMA    = VALIDATED_FOR_FREEZE
CANONICAL_FACTOR_MINUS2_ORIGIN           = REAL_TRANSPOSE_RECOMBINATION
MOMENT_EXCITED_BASIS_INVARIANCE         = VALIDATED_FOR_FREEZE
SHORT_TIME_NO_EXCITED_SPECTRUM_REQUIRED = VALIDATED_FOR_FREEZE
EDGE_M1_SCOPE                            = VALIDATED_FOR_FREEZE
NONEDGE_M1_ZERO                          = VALIDATED_FOR_FREEZE
MOMENT_SIGN_CONVENTION                   = VALIDATED_FOR_FREEZE
FLOATING_POINT_MOMENT_ZERO_IS_EXACT      = REJECTED
EXISTING_SELECTION_RULES_GOVERN_ZEROS    = VALIDATED_FOR_FREEZE
SECTOR_TOTAL_MINUS2_REUSE                = REJECTED
SECTOR_PROJECTED_COMMUTATOR_MOMENTS      = VALIDATED_FOR_FREEZE
SECTOR_EVEN_ORDER_CANCELLATION           = VALIDATED_FOR_FREEZE
ZERO_GRADE_KUBO_CHANNEL                  = INACTIVE_EXACT
NUMERICAL_BUDGET_BLOCK_SPLIT             = VALIDATED_FOR_FREEZE
MOMENT_OPERATOR_SPECTRAL_CROSSCHECK      = MANDATORY_FUTURE_VALIDATION
```
