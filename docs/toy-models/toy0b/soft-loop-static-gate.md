# Toy Model 0B — porte statique de la sous-campagne SOFT-LOOP

Statut : **validé pour gel — support méthodologique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `negative-mu-soft-loop.md`, `derivative-control.md`

Ce document fixe l'ordre logique de la sous-campagne SOFT-LOOP : la réduction effective à deux niveaux doit être testée statiquement avant toute interprétation dynamique fondée sur cette réduction.

## 1. Modèle effectif testé

Dans le doublet cyclique central :

```math
H_{eff}=E_c I+3g\delta\,\sigma_z+t_{loop}\,\sigma_x+\cdots
```

avec, à `delta=0` :

```math
gap_0=2|t_{loop}|.
```

On définit :

```math
x=\frac{6g\delta}{gap_0}.
```

Les deux prédictions statiques du modèle effectif sont :

```math
\frac{gap(\delta)}{gap_0}\simeq\sqrt{1+x^2}
```

et, puisque `2 Phi -> sigma_z` dans le doublet :

```math
2\langle\Phi\rangle\simeq-\frac{x}{\sqrt{1+x^2}}
```

à convention de signe près.

Ces relations sont des prédictions de la réduction effective à deux niveaux. À `mu` fini, des corrections hors doublet sont autorisées ; les critères numériques de conformité restent `OPEN` jusqu'au gel du lot numérique.

## 2. Porte d'entrée de SOFT-LOOP

Pour chaque fond `(g,mu)` de la sous-campagne :

1. diagonaliser à `delta=0` et publier `d_GS` et `gap_0` ;
2. construire un petit ensemble préenregistré de valeurs de `x` / `delta` autour de zéro ;
3. calculer uniquement par diagonalisation :
   - `gap(delta)/gap_0` ;
   - `2<Phi>(delta)` ;
4. comparer ces deux quantités aux courbes effectives ;
5. seulement si la réduction est suffisamment supportée selon le critère préenregistré, autoriser l'interprétation de `delta_c=gap_0/(6g)` comme échelle locale de linéarité et lancer le protocole dynamique `Xi_1` fondé sur `A_delta`.

Les statuts conceptuels sont :

```text
SOFT_LOOP_STATIC_SUPPORTED
SOFT_LOOP_STATIC_DEVIATES
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

`SOFT_LOOP_STATIC_DEVIATES` n'interdit pas de publier les observables du modèle complet ; il interdit seulement d'utiliser la réduction à deux niveaux comme interprétation normative de la sous-campagne pour ce point.

## 3. Absence de circularité

Le gap à `delta=0` peut être utilisé pour générer les points de test :

```math
\delta=x\frac{gap_0}{6g}.
```

Cela ne suppose pas que le collapse soit déjà vrai : cette coordonnée est l'hypothèse mise à l'épreuve. Si les deux collapses ne sont pas supportés, la coordonnée n'est pas réutilisée comme échelle normative du protocole dynamique.

Aucune valeur de `Delta_1` n'intervient dans cette porte statique.

## 4. Contrôle de troncature

Pour comparer `Lambda=2` et `Lambda=3`, les mêmes valeurs physiques de `delta` doivent être utilisées.

La grille physique est générée une seule fois à partir du gap de référence :

```math
\delta_j=x_j\frac{gap_0^{(2)}}{6g}.
```

Ces mêmes `delta_j` sont évalués aux deux cutoffs.

À `Lambda=3`, on publie aussi :

```math
x_j^{(3)}=\frac{6g\delta_j}{gap_0^{(3)}}
```

comme diagnostic, mais on ne génère pas une seconde grille physique.

## 5. Portée sur Delta_1

Les deux collapses statiques contraignent directement le doublet et ses observables statiques.

Ils ne démontrent pas :

```math
Delta_1(mu,delta)=F(x)
```

car `Delta_1` est construit à partir de la réponse de Kubo et de temps caractéristiques pouvant dépendre d'états hors doublet.

Donc :

```text
SOFT_LOOP_GAP_COLLAPSE      = EFFECTIVE_MODEL_PREDICTION
SOFT_LOOP_PHI_COLLAPSE      = EFFECTIVE_MODEL_PREDICTION
DELTA1_UNIVERSAL_COLLAPSE   = SECONDARY_HYPOTHESIS
```

Une absence de collapse de `Delta_1` ne réfute pas la réduction effective si les deux tests statiques sont satisfaits.

## 6. Statut

```text
SOFT_LOOP_STATIC_GATE                  = VALIDATED_FOR_FREEZE
STATIC_BEFORE_DYNAMIC                  = MANDATORY
DELTA_C_DYNAMIC_USE_REQUIRES_STATIC    = VALIDATED_FOR_FREEZE
STATIC_COLLAPSE_NUMERICAL_CRITERION    = OPEN
STATIC_X_CONTROL_VALUES                = OPEN
SAME_PHYSICAL_DELTA_ACROSS_CUTOFFS     = MANDATORY
DELTA1_COLLAPSE_PRIMARY_ORACLE         = REJECTED
DELTA1_COLLAPSE_SECONDARY_HYPOTHESIS   = ALLOWED
```
