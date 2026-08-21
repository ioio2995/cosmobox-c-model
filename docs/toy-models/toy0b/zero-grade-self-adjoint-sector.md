# Toy Model 0B — canal auto-conjugué de multigrade nul

Statut : **validé pour gel — support analytique correctif**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `path-grading.md`, `transition-fibers.md`, `path-purity-control.md`, `operator-moment-oracles.md`, `sector-parity-selection.md`

Ce document corrige explicitement la convention générale d'appariement des multigrades dans le cas auto-conjugué `m=0`. Dans le Toy Model 0B physique, ce canal est en outre exactement inactif pour la réponse Kubo densité-densité.

## 1. Appariement général et exception auto-conjuguée

Pour un multigrade entier :

```math
\mathbf m=(m_0,\ldots,m_5),
```

l'adjoint envoie :

```math
\mathbf m\mapsto-\mathbf m.
```

Pour :

```math
\mathbf m\neq\mathbf0,
```

le canal physique est la paire à deux éléments :

```text
[m] = {m,-m}.
```

En revanche :

```math
[\mathbf0]=\{\mathbf0\}
```

est un canal auto-conjugué à un seul élément. Une formule qui additionne mécaniquement `m` et `-m` avec un facteur deux ne doit donc jamais être appliquée à `m=0` sans traitement séparé.

## 2. Théorème spécifique au secteur physique 0B

Dans le secteur de Gauss :

```math
E_i-E_{i-1}=n_i-b_i.
```

Donc le sextuplet des flux détermine la matière :

```math
\boxed{
n_i=b_i+E_i-E_{i-1}.
}
```

Ainsi deux états de base physiques ayant exactement les mêmes six valeurs de `E_i` ont nécessairement la même configuration d'occupation `n`.

Comme la base d'occupation à `n` fixé est unidimensionnelle, chaque sous-espace propre conjoint des six opérateurs `E_i` dans `H_phys` est de dimension un.

Par conséquent, pour tout opérateur `O`, la composante de multigrade nul :

```math
\Pi_{\mathbf0}(O)
```

est diagonale dans la base physique occupation-flux.

Les densités `n_p` étant diagonales dans cette même base :

```math
\boxed{
[n_p,\Pi_{\mathbf0}(O)]=0
}
```

pour tout `p` et tout `O`.

## 3. Conséquence pour la réponse de Kubo

Avec :

```math
A_{\mathbf0}^{pq}(t)
=\operatorname{Tr}\!\left(
\rho[n_p,\Pi_{\mathbf0}n_q(t)]
\right),
```

on obtient exactement :

```math
\boxed{A_{\mathbf0}^{pq}(t)=0}
```

et donc :

```math
\boxed{\chi_{[\mathbf0]}^{pq}(t)=0}
```

pour toute paire `p,q`, tout fond de la famille 0B et tout temps.

Le contre-exemple algébrique générique où un secteur `m=0` auto-conjugué contribue est donc pertinent pour une graduation dont les espaces propres conjoints ont une multiplicité interne, mais il ne s'applique pas au secteur physique de Gauss de 0B.

## 4. Conséquence pour les moments sectoriels

Pour :

```math
O_{\mathbf m,r}
=\Pi_{\mathbf m}\operatorname{ad}_H^r(n_q),
```

et :

```math
B_{\mathbf m,r}^{pq}
=\operatorname{Tr}\left(\rho[n_p,O_{\mathbf m,r}]\right),
```

on a en particulier :

```math
\boxed{B_{\mathbf0,r}^{pq}=0}
```

pour tout `r`.

Pour `m != 0`, l'hermiticité donne :

```math
B_{-\mathbf m,r}^{pq}
=(-1)^{r+1}\overline{B_{\mathbf m,r}^{pq}}.
```

Dans la base réelle déclarée, `B_{m,r}` est réel pour tout `r`. Donc :

```text
r pair   -> B_-m,r = -B_m,r -> annulation dans le canal apparié
r impair -> B_-m,r = +B_m,r -> addition dans le canal apparié
```

Le coefficient physique pour `m != 0` et `r` impair vaut :

```math
\boxed{
a_{r,[\mathbf m]}^{pq}
=
\frac{2(-1)^{(r+1)/2}}{r!}
B_{\mathbf m,r}^{pq}.
}
```

Pour `r` pair :

```math
\boxed{a_{r,[\mathbf m]}^{pq}=0.}
```

Cette annulation canal par canal est la forme en moments de `K_SECTOR_ODDNESS`; elle ne repose sur aucune compensation entre secteurs.

## 5. Conséquence pour les fibres de transition

Si `m=0`, la différence de Gauss entre deux états physiques donne :

```math
\Delta n_i=m_i-m_{i-1}=0.
```

Donc le multigrade nul ne peut appartenir à une transition de matière ciblée :

```math
\Delta n=\pm(e_q-e_p)
```

pour `p != q`.

Il relèverait formellement de la classe `NON_TARGET_TRANSITION`, mais sa contribution Kubo est exactement nulle par le théorème précédent.

Ainsi :

```text
ZERO_GRADE_TARGET_DIRECT   = IMPOSSIBLE
ZERO_GRADE_TARGET_WINDING  = IMPOSSIBLE
ZERO_GRADE_NON_TARGET      = INACTIVE_EXACT
```

## 6. Conséquence pour P_sector et Purity_direct

Les poids sectoriels sont sommés sur les **canaux physiques distincts**, c'est-à-dire :

```text
- une seule fois par orbite {m,-m} avec m != 0 ;
- le canal m=0 une seule fois en principe.
```

Dans 0B densité-densité :

```math
P_{[\mathbf0]}(\tau)=0
```

exactement.

Par conséquent les définitions déjà retenues :

```math
P_{sector}=P_{direct}+P_{winding}+P_{non-target}
```

et :

```math
Purity_{direct}=P_{direct}/P_{sector}
```

ne reçoivent **aucune correction numérique** provenant de `m=0`, à condition que l'implémentation future n'additionne jamais deux fois le représentant auto-conjugué.

Un test structurel futur doit vérifier explicitement :

```text
ZERO_GRADE_KUBO_NORM = 0
```

à la tolérance numérique préenregistrée, tout en conservant le théorème analytique comme référence.

## 7. Statut

```text
SELF_ADJOINT_GRADE_SET                  = {m=0}
GENERIC_SELF_ADJOINT_DOUBLE_COUNTING    = REJECTED
PHYSICAL_JOINT_E_EIGENSPACE_DIMENSION   = 1
ZERO_GRADE_OPERATOR_DIAGONAL            = VALIDATED_FOR_FREEZE
ZERO_GRADE_DENSITY_COMMUTATOR            = ZERO_EXACT
ZERO_GRADE_KUBO_CHANNEL                  = INACTIVE_EXACT
ZERO_GRADE_TARGET_TRANSITION             = IMPOSSIBLE
ZERO_GRADE_NON_TARGET_WEIGHT             = ZERO_EXACT
PATH_PURITY_ZERO_GRADE_CORRECTION        = NOT_REQUIRED_NUMERICALLY
K_SECTOR_EVEN_ORDER_CANCELLATION         = VALIDATED_FOR_FREEZE
SELF_ADJOINT_CHANNEL_FUTURE_TEST         = MANDATORY
```
