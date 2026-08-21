# Toy Model 0B — fibres de transition de matière et pureté de chemin

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Compléments : `docs/toy-models/toy0b/path-grading.md`, `docs/toy-models/toy0b/zero-grade-self-adjoint-sector.md`

Ce document précise la structure imposée par Gauss sur les multigrades des opérateurs, puis définit la garde hiérarchique `transition ciblée -> enroulement` utilisée pour l'interprétation d'un temps d'arrivée.

## 1. Fibre affine imposée par Gauss

Pour deux états physiques de matière `n` et `n'`, on pose :

```math
\Delta n_i=n'_i-n_i,
\qquad
m_i=E'_i-E_i.
```

En soustrayant Gauss :

```math
E_i-E_{i-1}=n_i-b_i,
```

on obtient :

```math
m_i-m_{i-1}=\Delta n_i.
```

Le noyau de la différence discrète sur un cycle est la direction uniforme. Ainsi, pour une transition de matière fixée :

```math
\mathbf m
=\mathbf m^{(0)}(\Delta n)+w\mathbf1,
\qquad
w\in\mathbb Z,
```

avec :

```math
\mathbf1=(1,1,1,1,1,1).
```

À cutoff fini, seule une sous-partie de cette fibre peut être réalisée ; la structure affine reste exacte.

## 2. Le coordinateur e n'est pas un label intrinsèque

L'écriture :

```math
E_i=e+s_i(n)
```

utilise un choix de solution particulière de Gauss. Sous :

```math
s_i(n)\to s_i(n)+k(n),
```

on a :

```math
e\to e-k(n).
```

Donc `Delta e` n'est pas un label d'enroulement intrinsèque. Le label doit être défini directement par :

```math
\mathbf m=\mathbf m_D+w\mathbf1.
```

## 3. Transition de matière ciblée

La réponse de Kubo densité-densité ne doit pas être assimilée automatiquement à un transport littéral de particule.

Pour une interprétation plus restrictive d'arrivée source-récepteur, on déclare :

```math
\Delta n=\pm(\mathbf e_q-\mathbf e_p).
```

Le signe opposé appartient au même canal adjoint et ne définit pas un canal physique indépendant.

Une composante portant une autre transition appartient à :

```text
NON_TARGET_TRANSITION.
```

## 4. Représentant direct et enroulement

Pour `d(p,q)<N/2`, l'arc minimal est unique et fournit `m_D`.

Toute autre composante de la même transition de matière s'écrit :

```math
\mathbf m=\mathbf m_D+w\mathbf1.
```

On définit :

```text
TARGET_DIRECT
    transition ciblée, w=0

TARGET_WINDING
    transition ciblée, w!=0

NON_TARGET_TRANSITION
    transition de matière différente
```

## 5. Cas opposé d=N/2

Pour une paire opposée sur un cycle pair, les deux arcs minimaux ont la même longueur. Aucun représentant direct n'est privilégié par minimalité seule.

Donc :

```text
D3_ARRIVAL_INTERPRETATION = EXCLUDED
```

et aucune `PATH_PURITY_DIRECT` n'est utilisée pour fabriquer artificiellement un arc privilégié.

## 6. Décomposition sectorielle fine et canal auto-conjugué

Le découpage le plus fin utilise :

- le couple de configurations de matière `(n,n')` ;
- le multigrade invariant `m` ;
- l'orbite adjointe `(n,n',m) <-> (n',n,-m)`.

Pour `m!=0`, cette orbite contient deux composantes adjointes qui sont recombinées en une seule contribution physique `chi_alpha(t)`.

Le cas :

```math
m=0
```

est auto-conjugué et doit être traité une seule fois en général.

Dans le secteur physique 0B, il est toutefois exactement inactif. En effet :

```math
m=0
\quad\Longrightarrow\quad
\Delta n_i=m_i-m_{i-1}=0.
```

Plus fortement, les six flux `E_i` déterminent entièrement `n` par Gauss, donc `Pi_0(O)` est diagonal dans la base physique et commute avec toute densité `n_p`.

Ainsi :

```math
\boxed{\chi_{m=0}(t)=0}
```

et :

```math
\boxed{P_{m=0}(\tau)=0.}
```

Le canal `m=0` ne peut pas être `TARGET_DIRECT` ni `TARGET_WINDING` pour `p!=q`. Il relèverait formellement de `NON_TARGET_TRANSITION`, mais avec poids exactement nul.

Pour chaque canal physique actif distinct `alpha`, on définit :

```math
P_\alpha(\tau)
=\int_0^\tau \chi_\alpha(t)^2dt.
```

Chaque orbite adjointe non nulle est sommée une seule fois.

## 7. Agrégats diagnostiques

Pour une relation primaire `d<N/2` :

```math
P_{direct}
=\sum_{\alpha\in TARGET\_DIRECT}P_\alpha,
```

```math
P_{winding}
=\sum_{\alpha\in TARGET\_WINDING}P_\alpha,
```

```math
P_{non-target}
=\sum_{\alpha\in NON\_TARGET\_TRANSITION}P_\alpha.
```

Le canal nul peut être inclus formellement dans la dernière somme puisqu'il apporte exactement zéro ; l'implémentation future doit néanmoins l'identifier explicitement pour empêcher tout double comptage.

Puis :

```math
P_{sector}
=P_{direct}+P_{winding}+P_{non-target}.
```

Si `P_sector=0`, le diagnostic est `INACTIVE`.

## 8. Pureté directe diagnostique

On définit :

```math
Purity_{direct}(\tau)
=\frac{P_{direct}(\tau)}{P_{sector}(\tau)}.
```

et :

```math
1-Purity_{direct}
=\frac{P_{winding}+P_{non-target}}{P_{sector}}.
```

Le théorème d'inactivité du multigrade nul implique qu'aucune correction numérique de cette définition n'est nécessaire : le défaut potentiel était un risque de comptage, pas une contribution physique manquante.

Cette pureté reste un indice de composition sectorielle, pas une probabilité quantique ni une fraction exacte de `chi(t)^2`.

En général :

```math
P_{sector}\neq\int_0^\tau\chi(t)^2dt
```

à cause des interférences entre canaux distincts.

## 9. Garde de chemin

La garde utilise la famille de contrôle `epsilon_path` définie dans les supports dédiés. Les diagnostics séparés restent publiés :

```math
W(\tau)=P_{winding}/P_{sector},
```

```math
O(\tau)=P_{non-target}/P_{sector}.
```

Aucun seuil indépendant n'est introduit pour chacun.

## 10. Portée du verdict

Si la garde échoue :

```text
PATH_INTERPRETATION = INCONCLUSIVE
```

La réponse de Kubo elle-même n'est pas invalidée.

Le protocole publie la pureté, `W`, `O`, le spectre sectoriel complet et le contrôle apparié `Lambda=2 -> Lambda=3`.

## 11. Statut

```text
GAUSS_AFFINE_TRANSITION_FIBER = VALIDATED_FOR_FREEZE
RAW_DELTA_E_WINDING_LABEL     = REJECTED
TARGET_MATTER_TRANSITION      = VALIDATED_FOR_FREEZE
TARGET_DIRECT_CLASS           = VALIDATED_FOR_FREEZE for d < N/2
TARGET_WINDING_CLASS          = VALIDATED_FOR_FREEZE for d < N/2
NON_TARGET_TRANSITION_CLASS   = VALIDATED_FOR_FREEZE
D_N_OVER_2_DIRECT_LABEL       = NOT_DEFINED
SELF_ADJOINT_ZERO_GRADE       = IDENTIFIED
ZERO_GRADE_KUBO_CHANNEL       = INACTIVE_EXACT
ZERO_GRADE_DOUBLE_COUNTING    = REJECTED
PATH_PURITY_STRUCTURE         = VALIDATED_FOR_FREEZE
PATH_PURITY_ZERO_GRADE_FIX    = NO_NUMERICAL_CHANGE
FULL_SECTOR_SPECTRUM          = MANDATORY
TRUNCATION_CONTROL            = MANDATORY
```
