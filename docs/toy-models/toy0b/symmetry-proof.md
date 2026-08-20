# Toy Model 0B — support analytique des symétries

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne les démonstrations et l'énumération du groupe discret déclaré utilisées par le bloc de symétrie du Toy Model 0B. Il ne remplace pas la spécification scientifique principale. Son contenu devra être consolidé dans la spécification lors de la revue documentaire générale précédant le gel final de 0B.

## 1. Générateurs déclarés

On considère les transformations :

- `T` : translation d'un site ;
- `R` : réflexion `r(j) = -j mod 6` ;
- `C` : particule-trou avec phase bipartite ;
- `K` : conjugaison complexe dans la base occupation-flux.

La notation correcte est une forme normale

```text
T^a R^r C^c K^k,

a in {0,...,5},
r,c,k in {0,1},
```

et non un produit direct : les générateurs satisfont notamment la relation diédrique `R T R = T^-1`.

Le groupe candidat déclaré contient 48 transformations unitaires ou antiunitaires distinctes dans cette représentation.

## 2. Réflexion fermionique

La réflexion fermionique est définie par seconde quantification :

```math
R_f c_j^\dagger R_f^\dagger = c_{-j}^\dagger,
\qquad
R_f |0\rangle = |0\rangle.
```

Dans la convention de base

```math
|n_0\ldots n_5\rangle =
(c_0^\dagger)^{n_0}\cdots(c_5^\dagger)^{n_5}|0\rangle,
```

les modes occupés autres que `0` apparaissent après réflexion en ordre décroissant. Avec

```math
M=3-n_0\in\{2,3\},
```

le réordonnement canonique nécessite

```math
\frac{M(M-1)}2\in\{1,3\}
```

transpositions, donc produit toujours le facteur `-1` dans le secteur physique à trois fermions. Ce facteur est global sur tout le secteur et peut être absorbé dans la phase de `R_f`.

Sur les liens :

```math
R E_i R^\dagger=-E_{-i-1},
\qquad
R U_i R^\dagger=U_{-i-1}^\dagger.
```

Pour

```math
h_i=c_i^\dagger U_i c_{i+1},
```

on obtient

```math
R h_i R^\dagger=h_{-i-1}^\dagger.
```

Le lien de bord ne constitue pas une exception :

```math
h_5=c_5^\dagger U_5c_0
\longmapsto
c_1^\dagger U_0^\dagger c_0=h_0^\dagger.
```

Le hopping hermitien total est donc invariant sous `R`.

Pour la modulation électrique alternée

```math
V_\delta=\sum_i(-1)^i E_i^2,
```

la réflexion donne

```math
R V_\delta R^\dagger=-V_\delta.
```

Ainsi :

```math
R H(g,\mu,\delta)R^\dagger=H(g,\mu,-\delta).
```

Cette covariance est unitaire et exacte.

## 3. Particule-trou composée avec translation

La particule-trou est choisie avec phase bipartite :

```math
C c_i C^\dagger=(-1)^i c_i^\dagger,
\qquad
C E_i C^\dagger=-E_i,
\qquad
C U_i C^\dagger=U_i^\dagger.
```

Le signe fermionique du hopping est alors absorbé exactement et

```math
C h_i C^\dagger=h_i^\dagger.
```

`C` envoie le fond alterné `b` sur `1-b`. Une translation impaire le ramène sur `b`.

On définit notamment

```math
S=T C.
```

La réflexion `R` et `S` retournent chacune `delta`. Leur composé

```math
Q=S R=T C R
```

préserve donc `H(g,mu,delta)` pour toute la campagne.

Sur les occupations :

```math
Q n_p Q^\dagger=1-n_{1-p}.
```

Les constantes disparaissent dans le commutateur de Kubo :

```math
[1-n_a,1-n_b(t)]=[n_a,n_b(t)].
```

`Q` échange les deux orbites à distance 2 et impose donc l'oracle exact

```math
Delta_2(g,mu,delta)=0
```

sur toute la famille de fonds.

## 4. Conjugaison complexe K

Dans la base occupation-flux, les matrices de `H(g,mu,delta)` sont réelles :

- les termes électriques sont diagonaux réels ;
- les opérateurs de lien tronqués sont des shifts réels ;
- les signes fermioniques du hopping sont `+/-1`.

La conjugaison complexe `K` est donc une symétrie antiunitaire exacte :

```math
K H K^{-1}=H.
```

La prescription canonique de l'état fondamental est également réelle : pour un fondamental non dégénéré le projecteur est réel, et pour une dégénérescence le projecteur spectral `P_GS` est réel. Ainsi

```math
K rho K^{-1}=rho.
```

Pour les densités locales :

```math
K n_i K^{-1}=n_i.
```

Comme `K i K^{-1}=-i`, on a

```math
K n_q(t)K^{-1}=n_q(-t).
```

En posant

```math
chi_pq(t)=i Tr(rho [n_p,n_q(t)]),
```

le commutateur a une espérance purement imaginaire et la conjugaison donne l'oracle exact

```math
chi_pq(-t)=-chi_pq(t).
```

La fonctionnelle retenue

```math
F_pq(t)=chi_pq(t)^2/4
```

est donc exactement paire :

```math
F_pq(-t)=F_pq(t).
```

Une transformation antiunitaire `K g` a la même action spatiale sur les orbites que son partenaire unitaire `g`. Elle relie naturellement `t` à `-t`; combinée à l'imparité exacte de `chi`, elle n'introduit aucun nouvel échange d'orbites à temps positif. Le carré `F` supprime en outre toute ambiguïté de signe.

## 5. Comptage du groupe déclaré et du stabilisateur

Le groupe candidat déclaré est

```math
G_decl=\langle T,R,C,K\rangle,
```

avec 48 formes normales `T^a R^r C^c K^k`.

### 5.1 Préservation du secteur physique b

`C` échange `b` et `1-b`. Une translation impaire fait de même. La réflexion et `K` préservent le fond.

La condition de préservation de `H_phys(b)` est donc

```math
a\equiv c\pmod 2.
```

Le sous-groupe déclaré agissant dans le secteur physique contient alors 24 éléments.

### 5.2 Stabilisateur pour delta != 0

`T^a` retourne l'alternance de lien lorsque `a` est impair ; `R` la retourne ; `C` et `K` la préservent.

Pour fixer une valeur non nulle de `delta`, il faut donc en plus

```math
a\equiv r\pmod 2.
```

Avec la contrainte de secteur :

```math
a\equiv r\equiv c\pmod 2.
```

Le stabilisateur d'un fond générique `delta != 0` contient exactement 12 éléments : six unitaires et leurs six partenaires antiunitaires obtenus par multiplication par `K`.

La partie unitaire est

```text
{1, T^2, T^4,
 T R C, T^3 R C, T^5 R C}.
```

Elle agit comme le groupe diédral engendré par `T^2` et `Q = T C R`, avec

```math
Q T^2 Q^{-1}=T^{-2}.
```

### 5.3 Stabilisateur pour delta = 0

Lorsque `delta=0`, la contrainte `a == r mod 2` disparaît. Le stabilisateur dans le secteur physique contient alors les 24 éléments satisfaisant seulement

```math
a\equiv c\pmod 2.
```

La réflexion pure appartient de nouveau au stabilisateur et échange les deux orbites d'arête, ce qui impose

```math
Delta_1(0)=0.
```

## 6. Action sur les orbites d'arête

Sous le sous-groupe spatial résiduel `C3=<T^2>`, les arêtes se séparent en

```text
O_1,A = {(0,1),(2,3),(4,5)}
O_1,B = {(0,5),(1,2),(3,4)}.
```

Pour un élément unitaire du stabilisateur générique, l'action de site est de la forme

```math
j\mapsto a+j
```

ou

```math
j\mapsto a-j.
```

Une arête d'indice `i` est envoyée respectivement vers une arête d'indice

```math
i+a
```

ou

```math
a-i-1.
```

Sous la condition `a == r mod 2`, la parité de l'indice d'arête est préservée dans les deux cas. Aucun des six éléments unitaires du stabilisateur générique n'échange `O_1,A` et `O_1,B`.

`K` ne déplace aucun site ; les six éléments antiunitaires `K g` ont donc exactement la même action sur les orbites que `g`.

Conclusion : pour `delta != 0`, aucun des 12 éléments du stabilisateur déclaré n'échange les deux orbites d'arête.

Ainsi `Delta_1` est un signal autorisé relativement au groupe déclaré, sans être garanti non nul.

## 7. Covariance de Delta_1

La réflexion échange `O_1,A` et `O_1,B` tout en envoyant `delta` sur `-delta`. La covariance unitaire exacte implique

```math
C_{1,A}(delta)=C_{1,B}(-delta).
```

Pour

```math
Delta_1(delta)=log(C_{1,A}(delta)/C_{1,B}(delta)),
```

on obtient l'oracle

```math
Delta_1(-delta)=-Delta_1(delta),
```

et en particulier

```math
Delta_1(0)=0.
```

Cette identité doit être testée séparément pour `C_eff^grow` et pour toute la courbe admissible `C_eff^thr(eta)`.

## 8. Portée du résultat

L'énoncé scientifique doit nommer explicitement le groupe utilisé :

> Dans le stabilisateur de `H(g,mu,delta)` au sein du sous-groupe de `G_decl=<T,R,C,K>` qui préserve `H_phys(b)`, aucun élément déclaré n'échange `O_1,A` et `O_1,B` pour `delta != 0`.

La conclusion reste relative au groupe discret pré-déclaré. Une symétrie exacte non incluse dans `G_decl` et découverte ultérieurement peut réviser l'interprétation d'un contraste non nul.

## 9. Oracles de non-régression issus de ce bloc

```text
R_COVARIANCE
    R H(g,mu,delta) R^-1 = H(g,mu,-delta)

K_TIME_REVERSAL
    chi_pq(-t) = -chi_pq(t)
    F_pq(-t) = F_pq(t)

Q_NULL_ORACLE
    Delta_2(g,mu,delta) = 0 partout

DELTA1_ODD_COVARIANCE
    Delta_1(-delta) = -Delta_1(delta)
    Delta_1(0) = 0

EDGE_ORBIT_STABILIZER
    aucun des 12 éléments du stabilisateur déclaré a delta != 0
    n'échange O_1,A et O_1,B
```

## 10. Statut

```text
MODEL0B_REFLECTION_OPERATOR        = PROUVE EXACTEMENT
MODEL0B_K_ANTIUNITARY              = PROUVE EXACTEMENT
MODEL0B_DECLARED_GROUP_48          = ENUMERE
MODEL0B_SECTOR_SUBGROUP_24         = ENUMERE
MODEL0B_GENERIC_STABILIZER_12      = ENUMERE
MODEL0B_DELTA1_ORBIT_FREEDOM       = PROUVE RELATIVEMENT AU GROUPE DECLARE
MODEL0B_DELTA1_ODD_COVARIANCE      = PROUVEE
MODEL0B_DELTA2_GLOBAL_NULL_ORACLE  = PROUVE
MODEL0B_SYMMETRY_BLOCK             = VALIDE POUR GEL
```
