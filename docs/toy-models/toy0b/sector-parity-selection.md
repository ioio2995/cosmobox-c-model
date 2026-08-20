# Toy Model 0B — sélection sectorielle par K et parité bipartite

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `d2-free-hopping-oracle.md`, `d2-asymptotic-structure.md`, `path-grading.md`

Ce document explicite la sélection de parité au niveau de chaque canal sectoriel de la réponse de Kubo et sa combinaison avec la bipartition du cycle.

## 1. Impairité temporelle sectorielle

On considère la multigraduation par les opérateurs électriques et le projecteur réel `Pi_m` sur un multigrade `m` dans la base occupation-flux.

Pour :

```math
A_m(t)=Tr\left(\rho\,[n_p,\Pi_m n_q(t)]\right),
```

la conjugaison complexe `K` commute avec `Pi_m`, préserve `rho` et les densités, et inverse le temps. On obtient :

```math
A_m(-t)=\overline{A_m(t)}.
```

L'hermiticité donne par ailleurs :

```math
A_{-m}(t)=-\overline{A_m(t)}.
```

La contribution physique de la paire adjointe `[m]={m,-m}` est donc :

```math
\chi_{[m]}(t)
=i\bigl(A_m(t)+A_{-m}(t)\bigr)
=-2\,Im\,A_m(t).
```

Ainsi :

```math
\chi_{[m]}(-t)=-\chi_{[m]}(t).
```

La sélection impaire de `K` vaut donc **secteur par secteur**, et non seulement après sommation de la réponse totale. Aucun coefficient pair non nul dans un secteur ne peut être masqué par compensation avec un autre secteur.

## 2. Parité bipartite des mots de commutateurs

On définit :

```math
\mathcal P=(-1)^{N_{even}}.
```

Les termes diagonaux du Hamiltonien sont `P`-pairs :

```math
\mathcal P H_{diag}\mathcal P^\dagger=H_{diag},
```

avec :

```text
H_diag = termes électriques g, terme dimerisé g*delta, terme de matière mu.
```

Le hopping nearest-neighbor est `P`-impair :

```math
\mathcal P H_{hop}\mathcal P^\dagger=-H_{hop}.
```

Un mot de `ad_H^r(n_q)` contenant `k` insertions de hopping et `l=r-k` insertions diagonales possède donc la parité :

```math
(-1)^k.
```

Une transition de matière cible `q -> p` exige :

```math
k \equiv \Delta N_{even} \pmod 2.
```

Sur un graphe biparti :

```math
\Delta N_{even}\equiv d(p,q) \pmod 2.
```

Pour une contribution Kubo physique, l'impairité sectorielle impose `r` impair. Par conséquent :

```math
l=r-k\equiv 1-d(p,q)\pmod 2.
```

## 3. Règle générale

La règle structurante est donc :

```text
d pair   -> nombre impair d'insertions diagonales requis dans tout terme cible physique

d impair -> nombre pair d'insertions diagonales requis ; zéro insertion est autorisée
```

Cette règle vaut pour toute paire sur un graphe biparti tant que les hypothèses `K`, `P` et la sonde densité-densité restent valides.

## 4. Conséquences pour N=6

### d=1

`d` impair. Le terme cible peut être porté par un seul hopping, sans insertion diagonale. Cela est cohérent avec :

```math
\nu=1
```

pour une arête régulière.

### d=2

`d` pair. Toute contribution cible physique requiert un nombre impair d'insertions diagonales.

Au premier ordre physique autorisé `r=3` :

```text
k=2 hoppings + l=1 insertion diagonale -> TARGET_DIRECT
```

alors que les mots `k=3` appartiennent à des transitions de matière de parité opposée et relèvent du secteur `NON_TARGET_TRANSITION`.

Dans la limite de pur hopping, `l=0` à tous les ordres. Le canal cible `d=2` est donc identiquement absent de la réponse physique à tous les ordres.

### d=3

`d` impair. Trois hoppings sans insertion diagonale sont autorisés, cohérents avec le premier ordre physique `r=3` des paires opposées.

## 5. Portée quantitative près du pur hopping

Pour `d=2`, le coefficient direct dominant est au moins linéaire dans les couplages diagonaux actifs, tandis que son poids sectoriel intégré est donc au moins quadratique dans ces couplages.

Cependant aucune loi universelle du type :

```math
P_0 \propto \lambda_{diag}^2
```

n'est gelée sans qualifications supplémentaires, car :

- les coefficients dépendent de `rho_theta` ;
- plusieurs couplages diagonaux peuvent interférer ;
- le secteur non ciblé peut lui-même subir des annulations ;
- la troncature intervient dans les coefficients.

L'oracle exact reste la limite stricte de pur hopping où le poids direct est nul.

## 6. Statut

```text
K_SECTOR_ODDNESS                 = VALIDATED_FOR_FREEZE
BIPARTITE_WORD_PARITY            = VALIDATED_FOR_FREEZE
EVEN_DISTANCE_ODD_DIAG_RULE      = VALIDATED_FOR_FREEZE
ODD_DISTANCE_EVEN_DIAG_RULE      = VALIDATED_FOR_FREEZE
D2_PURE_HOPPING_TARGET_INACTIVE  = VALIDATED_FOR_FREEZE
D2_SMALL_DIAG_QUADRATIC_WEIGHT   = STRUCTURAL_SCALING_EXPECTATION
P0_NONZERO_FLOOR                 = NOT_STRUCTURALLY_DEFINED
```
