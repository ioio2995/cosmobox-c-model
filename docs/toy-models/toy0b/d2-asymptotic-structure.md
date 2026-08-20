# Toy Model 0B — structure asymptotique à distance 2

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `path-purity-control.md`, `transition-fibers.md`, `path-grading.md`

Ce document consigne la structure du premier ordre physique non nul du canal `d=2` et la normalisation retenue pour la variable de contrôle de pureté. Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale.

## 1. Parité des hoppings à d=2

Sur le cycle biparti, deux sites à distance 2 appartiennent au même sous-réseau.

Un mot contenant un nombre impair de hoppings change la parité de sous-réseau. Par conséquent, à l'ordre `r=3`, trois hoppings purs ne peuvent pas produire un bilinéaire `q <-> p` lorsque `d(p,q)=2`.

La famille précédemment envisagée « trois hoppings avec aller-retour mais transition cible » est rejetée.

Au premier ordre physique autorisé par `K`, `r=3`, les supports se répartissent structurellement en deux classes :

```text
J^2 x DIAGONAL
    -> TARGET_DIRECT

J^3
    -> NON_TARGET_TRANSITION
```

Le bloc diagonal comprend les contributions électriques `g`, dimerisées `g*delta` et de matière `mu` lorsqu'elles sont actives dans le commutateur considéré.

Les valeurs des coefficients de réponse dépendent toutefois de l'état canonique `rho_theta` et peuvent s'annuler sur des sous-ensembles particuliers de paramètres. La présence opératorielle d'un secteur ne prouve donc pas à elle seule un coefficient d'état non nul.

## 2. Statut exact de la pureté asymptotique

On note :

```math
P_0(theta,Lambda,pq)
=
Purity_direct(0^+).
```

Le domaine complet est en général :

```text
theta = (g, mu, delta)
Lambda
pair/orbit pq
```

Il est incorrect de réduire structurellement `P_0` à une fonction de `(g,mu)` seulement.

La présence de secteurs `NON_TARGET_TRANSITION` au même ordre physique implique :

```text
P_0 = 1
```

n'est pas un oracle structurel à `d=2`.

Le statut :

```text
ASYMPTOTIC_PATH_MIXED
```

est attendu génériquement si les coefficients `TARGET_DIRECT` et `NON_TARGET_TRANSITION` d'ordre 3 sont tous deux non nuls, mais il ne devient un verdict exact pour un fond donné qu'après calcul des coefficients sectoriels d'état.

## 3. Absence d'enroulement à l'ordre 3

Pour `N=6`, `d=2`, l'arc complémentaire minimal contient 4 hoppings.

La sélection impaire de `K` reporte la première contribution physique possible de cette classe à un ordre impair `>=5`.

Par conséquent, au régime asymptotique `r=3` :

```math
W(0^+)=0,
```

et :

```math
O(0^+)=1-P_0,
```

si `O` désigne la part sectorielle `NON_TARGET_TRANSITION`.

L'impureté asymptotique de `d=2`, lorsqu'elle est présente, est donc de type transition non ciblée et non de type enroulement.

## 4. Séparation entre impureté de base et dégradation finie

On définit :

```math
I(theta,tau)=1-Purity_direct(theta,tau),
```

et l'enveloppe monotone :

```math
I_max(theta,tau)
=
sup_{0<s<=tau} I(theta,s).
```

L'impureté asymptotique est :

```math
I_0(theta)=1-P_0(theta).
```

Lorsque `P_0(theta)>0`, on définit la dégradation relative supplémentaire :

```math
R_path(theta,tau)
=
\frac{I_max(theta,tau)-I_0(theta)}{P_0(theta)}.
```

Comme l'enveloppe contient le voisinage de zéro :

```math
I_max(theta,tau)>=I_0(theta),
```

et :

```math
0<=R_path(theta,tau)<=1.
```

Ainsi `R_path` mesure uniquement la perte de pureté au-delà du mélange asymptotique irréductible propre au fond.

Si :

```text
P_0 = 0
```

le canal ne possède aucun poids direct au premier ordre physique et :

```text
PATH_BASELINE_STATUS = NO_DIRECT_BASELINE
```

La normalisation `R_path` n'est alors pas applicable.

## 5. Variable de contrôle epsilon_path

`epsilon_path` n'est pas un seuil physique privilégié.

Pour `P_0>0`, on définit :

```math
tau_path(epsilon)
=
inf\{tau>0 : R_path(tau)>epsilon\}.
```

La garde d'un événement `T_event` est étudiée sur une grille préenregistrée commune :

```text
epsilon in E_path subset (0,1)
```

et non sur une grille absolue dépendant de `1-P_0(theta)`.

Cette normalisation permet d'utiliser la même variable de contrôle pour les différents fonds, y compris les couples `+delta/-delta`, tout en publiant séparément `P_0(theta)` comme information physique de base.

La grille `E_path` reste ouverte jusqu'au gel numérique du protocole.

## 6. Portée pour d=1 et d=2

Pour une arête régulière `d=1` avec coefficient linéaire direct non nul :

```math
P_0=1,
I_0=0,
```

et `R_path` se réduit à l'impureté absolue enveloppée déjà envisagée.

Pour `d=2`, `P_0` doit être publié et ne doit pas être absorbé dans le seuil de contrôle.

En particulier, une forte impureté asymptotique `1-P_0` ne peut pas être rendue invisible par la normalisation : elle reste un résultat sectoriel explicite et limite la portée de toute interprétation comme arrivée élémentaire source-récepteur.

## 7. Contrôle de troncature

Les quantités suivantes doivent être comparées à `Lambda=2` et `Lambda=3` :

```text
P_0(theta)
W(0^+)
O(0^+)
R_path(theta,tau)
tau_path(theta,epsilon)
```

La même grille `E_path` est utilisée aux deux cutoffs.

Aucune modification de `E_path` ne peut être utilisée pour absorber une différence de troncature.

## 8. Statut

```text
D2_R3_THREE_HOP_TARGET_CLASS      = REJECTED
D2_R3_J2_DIAGONAL_TARGET          = VALIDATED_FOR_FREEZE
D2_R3_J3_NON_TARGET               = VALIDATED_FOR_FREEZE
D2_R3_WINDING                     = ABSENT_STRUCTURALLY
D2_P0_EQUALS_ONE                  = NOT_AN_ORACLE
D2_ASYMPTOTIC_MIXING              = GENERIC_EXPECTATION
D2_P0_PER_DOMAIN                  = MANDATORY
PATH_BASELINE_IMPURITY_I0         = VALIDATED_FOR_FREEZE
PATH_RELATIVE_DEGRADATION_R_PATH  = VALIDATED_FOR_FREEZE
EPS_PATH_SINGLE_VALUE             = NOT_REQUIRED
EPS_PATH_CONTROL_GRID             = OPEN
TRUNCATION_CONTROL                = MANDATORY
```
