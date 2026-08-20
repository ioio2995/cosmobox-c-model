# Toy Model 0B — fibres de transition de matière et pureté de chemin

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Complément : `docs/toy-models/toy0b/path-grading.md`

Ce document précise la structure imposée par Gauss sur les multigrades des opérateurs, puis définit la garde hiérarchique `transition ciblée -> enroulement` utilisée pour l'interprétation d'un temps d'arrivée. Il ne remplace pas la spécification principale et devra être consolidé lors de la revue documentaire générale.

## 1. Fibre affine imposée par Gauss

Pour deux états physiques de matière `n` et `n'`, on pose :

```math
\Delta n_i=n'_i-n_i,
\qquad
m_i=E'_i-E_i.
```

En soustrayant les deux contraintes de Gauss :

```math
E_i-E_{i-1}=n_i-b_i,
```

on obtient :

```math
m_i-m_{i-1}=\Delta n_i.
```

Le noyau de la différence discrète sur un cycle est la direction uniforme. Ainsi, pour une transition de matière fixée, l'ensemble de tous les multigrades compatibles est une fibre affine :

```math
\mathbf m
=
\mathbf m^{(0)}(\Delta n)+w\,\mathbf 1,
\qquad
w\in\mathbb Z,
```

avec :

```math
\mathbf1=(1,1,1,1,1,1).
```

À cutoff fini, seule une sous-partie de cette fibre peut être réalisée ; la structure affine reste néanmoins exacte.

## 2. Le coordinateur `e` n'est pas un label intrinsèque

L'écriture d'un état physique sous la forme :

```math
E_i=e+s_i(n)
```

utilise un choix de solution particulière de Gauss.

Si :

```math
s_i(n)\to s_i(n)+k(n),
```

alors :

```math
e\to e-k(n).
```

Par conséquent, pour une transition `n -> n'`, la quantité brute :

```math
\Delta e=e'-e
```

change sous ce changement de convention.

Il est donc interdit d'identifier `Delta e` à une classe d'enroulement intrinsèque.

Le label d'enroulement doit être défini directement dans l'espace invariant des multigrades :

```math
\mathbf m=\mathbf m_D+w\mathbf1,
```

relativement à un représentant `m_D` déclaré.

## 3. Transition de matière ciblée

La réponse de Kubo primaire est une susceptibilité densité-densité. Elle ne doit pas être assimilée automatiquement à un transport littéral de particule.

Pour autoriser une interprétation plus restrictive de type `arrivée source-récepteur`, on déclare une classe de transition de matière ciblée :

```math
\Delta n
=\pm(\mathbf e_q-\mathbf e_p).
```

Le signe opposé appartient à la même paire adjointe et ne définit pas un canal physique indépendant.

Une composante de la réponse dont la transition de matière ne satisfait pas cette condition reste une contribution physique légitime à la réponse de Kubo, mais elle appartient à :

```text
NON_TARGET_TRANSITION
```

Elle ne doit pas être interprétée comme transfert élémentaire `p <-> q`.

## 4. Représentant direct et classe d'enroulement

Pour `d(p,q) < N/2`, l'arc minimal est unique. Il fournit un représentant canonique `m_D` du multigrade de la transition ciblée.

Toute autre composante de la même transition de matière s'écrit alors de manière unique :

```math
\mathbf m=\mathbf m_D+w\mathbf1.
```

On définit :

```text
TARGET_DIRECT
    transition de matière ciblée
    w = 0

TARGET_WINDING
    transition de matière ciblée
    w != 0

NON_TARGET_TRANSITION
    transition de matière différente de la transition ciblée
```

La discussion d'un arc direct / d'un enroulement n'est donc menée qu'après identification de la transition de matière.

## 5. Cas opposé `d=N/2`

Pour un cycle pair et une paire opposée, les deux arcs minimaux ont la même longueur.

Il n'existe donc aucun représentant direct privilégié par minimalité seule. Les deux représentants minimaux diffèrent d'une unité uniforme et doivent être traités symétriquement dans le protocole secondaire d'interférence cyclique.

Conséquence :

```text
D3_ARRIVAL_INTERPRETATION = EXCLUDED
```

et aucune `PATH_PURITY_DIRECT` n'est utilisée pour fabriquer artificiellement un arc privilégié dans ce cas.

## 6. Décomposition sectorielle fine

Le découpage le plus fin utilisé pour le diagnostic est défini par :

- le couple de configurations de matière `(n,n')` ;
- le multigrade invariant `m` ;
- la paire adjointe obtenue par `(n,n',m) <-> (n',n,-m)`.

Pour chaque paire adjointe `alpha`, on définit sa contribution physique à la réponse :

```math
\chi_\alpha(t),
```

obtenue après recombinaison des deux composantes adjointes.

On définit ensuite son poids diagnostique intégré :

```math
P_\alpha(\tau)
=
\int_0^\tau \chi_\alpha(t)^2\,dt.
```

Ces poids servent uniquement à caractériser la composition sectorielle de la réponse.

## 7. Agrégats diagnostiques

Pour une relation primaire `d<N/2`, on pose :

```math
P_{direct}
=
\sum_{\alpha\in TARGET\_DIRECT}P_\alpha,
```

```math
P_{winding}
=
\sum_{\alpha\in TARGET\_WINDING}P_\alpha,
```

```math
P_{non-target}
=
\sum_{\alpha\in NON\_TARGET\_TRANSITION}P_\alpha.
```

Puis :

```math
P_{sector}
=
P_{direct}+P_{winding}+P_{non-target}.
```

Si `P_sector = 0`, le canal est `INACTIVE` pour ce diagnostic.

## 8. Pureté directe diagnostique

On définit :

```math
Purity_{direct}(\tau)
=
\frac{P_{direct}(\tau)}{P_{sector}(\tau)}.
```

et donc :

```math
1-Purity_{direct}
=
\frac{P_{winding}+P_{non-target}}{P_{sector}}.
```

Cette quantité est un **indice de composition sectorielle**, pas une probabilité quantique ni une fraction exacte de `chi(t)^2`.

En particulier :

```math
P_{sector}
\neq
\int_0^\tau \chi(t)^2dt
```

en général, car les contributions sectorielles interfèrent dans la réponse totale.

## 9. Une seule tolérance de garde

La garde d'interprétation utilise une tolérance unique :

```math
1-Purity_{direct}(\tau)
\le
\varepsilon_{path}.
```

Les diagnostics séparés restent publiés :

```math
W(\tau)
=
\frac{P_{winding}}{P_{sector}},
```

```math
O(\tau)
=
\frac{P_{non-target}}{P_{sector}}.
```

mais ils ne possèdent pas de seuils d'acceptation indépendants.

La raison est logique : deux seuils séparés permettraient à deux contaminations distinctes de passer chacune juste sous sa borne tout en produisant une impureté totale plus importante.

La valeur numérique de `epsilon_path` reste :

```text
PATH_PURITY_TOLERANCE = OPEN
```

jusqu'au pré-enregistrement final.

## 10. Portée du verdict

Si la garde échoue :

```text
PATH_INTERPRETATION = INCONCLUSIVE
```

La réponse de Kubo elle-même n'est pas invalidée.

Le protocole doit publier :

- `Purity_direct(tau)` ;
- `W(tau)` ;
- `O(tau)` ;
- le spectre sectoriel complet `P_alpha(tau)` ;
- le contrôle apparié `Lambda=2 -> Lambda=3`.

Aucune interprétation ne doit reposer uniquement sur le franchissement discret de `epsilon_path` sans publication de ces quantités continues.

## 11. Statut

```text
GAUSS_AFFINE_TRANSITION_FIBER = VALIDATED_FOR_FREEZE
RAW_DELTA_E_WINDING_LABEL     = REJECTED
TARGET_MATTER_TRANSITION      = VALIDATED_FOR_FREEZE
TARGET_DIRECT_CLASS           = VALIDATED_FOR_FREEZE for d < N/2
TARGET_WINDING_CLASS          = VALIDATED_FOR_FREEZE for d < N/2
NON_TARGET_TRANSITION_CLASS   = VALIDATED_FOR_FREEZE
D_N_OVER_2_DIRECT_LABEL       = NOT_DEFINED
PATH_PURITY_STRUCTURE         = VALIDATED_FOR_FREEZE
SINGLE_PATH_TOLERANCE         = VALIDATED_FOR_FREEZE
PATH_PURITY_TOLERANCE         = OPEN
FULL_SECTOR_SPECTRUM          = MANDATORY
TRUNCATION_CONTROL            = MANDATORY
```
