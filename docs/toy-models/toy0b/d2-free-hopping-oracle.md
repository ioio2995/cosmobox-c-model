# Toy Model 0B — oracle pur hopping pour d=2

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `d2-asymptotic-structure.md`, `path-purity-control.md`

Ce document consigne l'oracle exact du canal `d=2` dans la limite de pur hopping `g=mu=0` (le terme `g*delta` est alors également nul). Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale.

## 1. Symétrie bipartite du Hamiltonien de hopping

On définit la parité de sous-réseau :

```math
\mathcal P=(-1)^{N_{even}}.
```

Chaque hopping nearest-neighbor transfère exactement un fermion entre sous-réseaux, donc :

```math
\mathcal P H_{hop}\mathcal P^\dagger=-H_{hop}.
```

Les densités locales sont paires :

```math
\mathcal P n_q\mathcal P^\dagger=n_q.
```

Par récurrence :

```math
\mathcal P\,ad_{H_{hop}}^r(n_q)\,\mathcal P^\dagger
=(-1)^r ad_{H_{hop}}^r(n_q).
```

## 2. Conséquence pour une transition cible à d=2

Pour `d(p,q)=2`, `p` et `q` appartiennent au même sous-réseau.

La transition de matière cible :

```math
\Delta n=\pm(e_q-e_p)
```

préserve donc la parité de `N_even`.

Une composante `TARGET_DIRECT` ou `TARGET_WINDING` associée à cette transition ne peut être portée par un opérateur impair sous `P`.

Par conséquent, dans le pur hopping, les ordres impairs `r` de `ad_H^r(n_q)` ne possèdent aucune composante de transition cible à `d=2`.

## 3. Composition avec la sélection antiunitaire K

Dans la base occupation-flux, le Hamiltonien de pur hopping et l'état canonique réel satisfont la contrainte antiunitaire `K` déjà démontrée.

La réponse de Kubo est impaire en temps :

```math
\chi_{pq}(-t)=-\chi_{pq}(t).
```

Les coefficients physiques d'ordre pair sont donc nuls.

On obtient alors la combinaison forte :

```text
r impair  -> transition cible d=2 interdite par la bipartition
r pair    -> coefficient Kubo physique nul par K
```

Ainsi la contribution Kubo de la transition cible à `d=2` est identiquement inactive dans la limite de pur hopping.

## 4. Oracle exact

Dans la limite :

```text
g = 0
mu = 0
```

(et donc `g*delta=0` pour tout delta fini), on a :

```text
D2_TARGET_TRANSITION_RESPONSE = INACTIVE
```

pour le protocole de réponse de Kubo densité-densité.

Si la réponse totale `d=2` reste active grâce à des secteurs `NON_TARGET_TRANSITION`, alors :

```math
P_{direct}(tau)=0
```

pour tout `tau>0` et :

```math
Purity_{direct}(tau)=0
```

partout où le dénominateur sectoriel est non nul.

En particulier :

```math
P_0^{d=2}=0.
```

Si la réponse totale est elle-même inactive pour un fond particulier, la pureté est `NOT_DEFINED` et le statut du canal est `INACTIVE`, pas `P_0=0` par convention.

## 5. Portée

L'énoncé est plus fort que « l'exposant direct saute de 3 à 5 » : aucun ordre physique ne réactive la transition cible tant que le Hamiltonien reste strictement dans la limite de pur hopping bipartite et que la structure antiunitaire `K` reste applicable.

Dès qu'un terme diagonal actif est réintroduit (`g`, `g*delta`, `mu`), la composante `TARGET_DIRECT` peut réapparaître au premier ordre physique `r=3` selon la structure déjà consignée dans `d2-asymptotic-structure.md`.

## 6. Statut

```text
D2_FREE_HOPPING_TARGET_RESPONSE = INACTIVE_EXACT
D2_FREE_HOPPING_P0             = 0_IF_TOTAL_RESPONSE_ACTIVE
D2_DIRECT_ORDER5_REACTIVATION  = REJECTED
D2_NON_TARGET_RESPONSE         = ALLOWED
```
