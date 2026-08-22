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

et, puisque `2 Phi -> sigma_z` dans le doublet, avec la convention de signe fixée par le fait que pour `delta>0` (`x>0`) l'état central de flux `e=0` est énergétiquement favorisé et `Phi -> -1/2` dans la limite de forte polarisation :

```math
2\langle\Phi\rangle\simeq-\frac{x}{\sqrt{1+x^2}}.
```

Le statut du couplage exact de signe sous-jacent à ces deux relations est :

```text
GAP_DELTA_SIGN_EVENNESS = STRUCTURAL_ANALYTIC
PHI_DELTA_SIGN_ODDNESS  = ORACLE
```

`GAP_DELTA_SIGN_EVENNESS` traduit `gap(-delta)=gap(delta)`, conséquence exacte de la covariance déjà gelée `R H(g,mu,delta) R^dagger = H(g,mu,-delta)`, donc `G(-x)=G(x)`. `PHI_DELTA_SIGN_ODDNESS` traduit `P(-x)=-P(x)` pour `P(x)=2<Phi>(x)`, valable pour un état fondamental non dégénéré.

Ces relations sont des prédictions de la réduction effective à deux niveaux. À `mu` fini, des corrections hors doublet sont autorisées ; les critères numériques de conformité restent `OPEN` jusqu'au gel du lot numérique.

## 2. Porte d'entrée de SOFT-LOOP

Pour chaque fond `(g,mu)` de la sous-campagne :

1. diagonaliser à `delta=0` et publier `d_GS` et `gap_0` ;
2. évaluer la grille de `x` préenregistrée :

```text
STATIC_X_PRIMARY = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_X_SATURATION_DIAGNOSTIC = {±4}
```

`STATIC_X_PRIMARY` est la grille physique obligatoire de la porte statique. `STATIC_X_SATURATION_DIAGNOSTIC = {±4}` est `EXTENDED_DIAGNOSTIC` : ces points sondent le régime de grand `|x|` / saturation / stress de portée, mais ne peuvent pas à eux seuls faire échouer la porte statique obligatoire ;
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

### Contenu discriminant de la grille

L'ensemble de magnitudes indépendantes et discriminantes pour un futur critère de collapse agrégé est :

```text
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES = {1/4, 1/2, 1, 2}
```

Les partenaires de signe négatif ne constituent pas une évidence indépendante pour le modèle effectif : la covariance exacte `R H(g,mu,delta) R^dagger = H(g,mu,-delta)` rend les relations de signe correspondantes exactes, pas des tests indépendants. Leur rôle est :

```text
NEGATIVE_X_HALF_ROLE = NUMERICAL_CONTROL / IMPLEMENTATION_ORACLE
```

Ils doivent néanmoins être calculés sur la grille primaire : ils exercent de bout en bout la covariance exacte et l'imparité de `Phi`, sans compter comme échantillon indépendant dans un futur score de collapse agrégé.

`x=0` est une ancre de normalisation/symétrie, pas une évidence de collapse discriminante :

```text
STATIC_X_ZERO_ROLE = NUMERICAL_CONTROL / NORMALIZATION_ORACLE
```

À `x=0`, `G(0)=1` par normalisation et `P(0)=0` par l'imparité exacte de `Phi` pour un état fondamental non dégénéré symétrique. `x=0` doit être évalué et publié, mais ne peut pas inflater un futur décompte agrégé d'évidence de collapse.

Ni la duplication de signe négatif ni `x=0` ne peuvent inflater un futur décompte d'évidence de collapse agrégée.

## 3. Absence de circularité

Le gap à `delta=0` peut être utilisé pour générer les points de test :

```math
\delta=x\frac{gap_0}{6g}.
```

Cela ne suppose pas que le collapse soit déjà vrai : cette coordonnée est l'hypothèse mise à l'épreuve. Si les deux collapses ne sont pas supportés, la coordonnée n'est pas réutilisée comme échelle normative du protocole dynamique.

Aucune valeur de `Delta_1` n'intervient dans cette porte statique.

## 4. Contrôle de troncature

Pour comparer `Lambda=2` et `Lambda=3`, les mêmes valeurs physiques de `delta` doivent être utilisées.

`gap_0^{(2)}` est calculé au moment de l'exécution en pleine précision numérique ; les valeurs arrondies de `DESIGN_QUALIFICATION` sont interdites pour générer les points physiques.

La grille physique est générée une seule fois à partir du gap de référence :

```math
\delta_j=x_j\frac{gap_0^{(2)}}{6g}.
```

Ces mêmes `delta_j` sont évalués aux deux cutoffs. La classification `STATIC_X_PRIMARY` / `STATIC_X_SATURATION_DIAGNOSTIC` (`EXTENDED_DIAGNOSTIC`) est définie sur la grille `x` de `Lambda=2` ; à `Lambda=2`, `x_j^{(2)}=x_j` par construction.

À `Lambda=3`, on publie aussi la coordonnée diagnostique dérivée :

```math
x_j^{(3)}=\frac{6g\delta_j}{gap_0^{(3)}}
```

mais on ne génère pas une seconde grille physique. `x_j^{(3)}` peut sortir de la bande nominale de `x` ; cette sortie doit être publiée telle quelle et ne redéfinit pas la classification primaire/diagnostic étendu.

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
STATIC_X_CONTROL_VALUES                = VALIDATED_FOR_FREEZE
STATIC_X_PRIMARY                       = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES = {1/4, 1/2, 1, 2}
STATIC_X_SATURATION_DIAGNOSTIC         = {±4}
SAME_PHYSICAL_DELTA_ACROSS_CUTOFFS     = MANDATORY
DELTA1_COLLAPSE_PRIMARY_ORACLE         = REJECTED
DELTA1_COLLAPSE_SECONDARY_HYPOTHESIS   = ALLOWED
```
