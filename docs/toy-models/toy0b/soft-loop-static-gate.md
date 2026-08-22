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

Ces relations sont des prédictions de la réduction effective à deux niveaux. À `mu` fini, des corrections hors doublet sont autorisées ; le critère numérique de conformité (`STATIC_COLLAPSE_NUMERICAL_CRITERION`) est défini au §6.

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
SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
SOFT_LOOP_STATIC_DEVIATES
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

`SOFT_LOOP_STATIC_DEVIATES` n'interdit pas de publier les observables du modèle complet ; il interdit seulement d'utiliser la réduction à deux niveaux comme interprétation normative de la sous-campagne pour ce point. `SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION` est un statut spécialisé défini au §6.8 : il ne s'applique qu'à `Lambda=3` sous la garde d'information et ne se substitue pas à `SOFT_LOOP_STATIC_SUPPORTED` dans une revendication de mécanisme stable au cutoff (§6.10).

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

## 6. Critère numérique de conformité au modèle (`tau_static`)

Ce critère fixe la conformité numérique du modèle effectif à `mu` fini pour la
porte statique de SOFT-LOOP.

### 6.1 Tolérance de conformité

```text
STATIC_COLLAPSE_TOLERANCE = 0.10
```

`tau_static=0.10` est une tolérance opérationnelle de **conformité au modèle
effectif** à `mu` fini. Ce n'est pas une tolérance de virgule flottante, pas
une borne d'erreur de théorème, et pas une affirmation que la réduction à
deux niveaux est exacte à 10%. Elle reste épistémiquement distincte des
contrôles de précision numérique à `~1e-10` (`SPECTRAL_PRECISION_CONTROL`,
`ROOT_SOLVER_TOLERANCES`, `ARGMAX_TOLERANCES`, etc.).

### 6.2 Coordonnée locale au cutoff

Pour chaque précision acceptée `q` et chaque cutoff `Lambda`, pour la même
valeur physique `delta_j` :

```math
x_j^{(q,\Lambda)}=\frac{6g\delta_j}{gap_0^{(q,\Lambda)}}
```

```math
G_j^{(q,\Lambda)}=\frac{gap^{(q,\Lambda)}(\delta_j)}{gap_0^{(q,\Lambda)}}
```

```math
P_j^{(q,\Lambda)}=2\langle\Phi\rangle^{(q,\Lambda)}(\delta_j)
```

avec `G_eff(x)=sqrt(1+x^2)` et `P_eff(x)=-x/sqrt(1+x^2)`.

### 6.3 Déviations signées et budget numérique p/2p

Les déviations signées sont d'abord définies :

```math
d_G^{(q)}=\frac{G^{(q)}-G_{eff}(x^{(q)})}{G_{eff}(x^{(q)})}
```

```math
d_P^{(q)}=P^{(q)}-P_{eff}(x^{(q)})
```

Les résidus à haute précision sont :

```math
r_G^{(2p)}=|d_G^{(2p)}|,\qquad r_P^{(2p)}=|d_P^{(2p)}|.
```

Les proxys d'incertitude numérique résiduelle sont :

```math
e_G=|d_G^{(2p)}-d_G^{(p)}|,\qquad e_P=|d_P^{(2p)}-d_P^{(p)}|.
```

Ce budget (`STATIC_COLLAPSE_NUMERICAL_BUDGET = P_OVER_2P_SIGNED_DEVIATION_DIFFERENCE`)
remplace la proposition plus faible `| |d^{(2p)}| - |d^{(p)}| |`, qui peut
s'annuler artificiellement si le signe de la déviation numérique change entre
`p` et `2p`. La paire de précision `p/2p` utilisée est celle déjà validée par
l'échelle spectrale (`SPECTRAL_PRECISION_CONTROL`). Si l'appariement de
précision sous-jacent n'est pas résolu, aucun verdict de conformité au modèle
n'est publié :

```text
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

### 6.4 Métriques de résidu

Résidu de gap, relatif :

```math
r_G=\frac{|G-G_{eff}(x)|}{G_{eff}(x)},\qquad G_{eff}\geq1.
```

Résidu de polarisation, absolu :

```math
r_P=|P-P_{eff}(x)|.
```

`P=2\langle\Phi\rangle` est adimensionnel et borné ; un écart absolu a donc
un sens physique uniforme sur l'échelle bornée de la polarisation. Ce choix
n'est pas justifié par une prétendue singularité relative sur l'ensemble
informatif. Il est documenté explicitement que le seuil absolu est moins
exigeant en termes relatifs à `|x|=1/4` qu'à `|x|=2` ; la puissance
discriminante principale provient donc des magnitudes `|x|` proches de `1` et
`2`. Cette observation ne se convertit en aucun nouveau schéma de pondération.

### 6.5 Intervalles numériques `L`/`U`

Pour `O` dans `{G,P}` :

```math
L_O=\max(0,\ r_O^{(2p)}-e_O),\qquad U_O=r_O^{(2p)}+e_O.
```

Aucune interprétation gaussienne ou probabiliste : ce sont des intervalles de
contrôle numérique issus du doublement de précision.

### 6.6 Classification ponctuelle en norme `L_infinity`

Pour un fond `(g,mu)` et un cutoff `Lambda` donnés, la précision numérique
acceptée sous-jacente est d'abord requise. Chaque point physique informatif
correspondant aux magnitudes nominales `Lambda=2` :

```text
{1/4, 1/2, 1, 2}
```

est ensuite évalué. La condition `DEVIATES` est prioritaire :

```text
si L_G > 0.10  OU  L_P > 0.10  pour au moins un point/observable
-> SOFT_LOOP_STATIC_DEVIATES
```

Sinon, si au moins un intervalle chevauche la frontière (c'est-à-dire pas
tous les `U <= 0.10`) :

```text
-> SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

Sinon, si tous les bornes supérieures des points/observables informatifs
satisfont `U_G <= 0.10 ET U_P <= 0.10`, le résultat brut de forme du modèle
est supporté, sous réserve à `Lambda=3` de la garde d'information définie en
§6.8.

Aucune moyenne n'est autorisée sur `x`, les observables, les signes, `mu` ou
le cutoff. Aucune compensation entre `gap` et `Phi` n'est autorisée.

```text
STATIC_COLLAPSE_NORM = POINTWISE_L_INFINITY
```

### 6.7 Porte locale au fond à `Lambda=2`

À `Lambda=2`, les magnitudes informatives préenregistrées sont exactement
`{1/4,1/2,1,2}`, donc la bande d'information est garantie par construction.
Pour chaque `mu` dans `{-1.25,-1.5,-2}`, la porte statique est décidée
séparément. Si le résultat `Lambda=2` est `SOFT_LOOP_STATIC_SUPPORTED`, le
protocole dynamique fondé sur `delta_c` PEUT être exécuté pour ce fond.
Aucune moyenne ni compensation entre valeurs de `mu`. Les observables brutes
du modèle complet restent publiables sous tous les statuts.

### 6.8 Garde d'information à `Lambda=3`

À `Lambda=3`, on utilise les mêmes `delta_j` physiques générés à `Lambda=2`.
On publie :

```math
\rho=\frac{gap_0^{(2)}}{gap_0^{(3)}}
```

et tous les `x_j^{(3)}` dérivés. Sur les points physiques informatifs, on
définit :

```math
X_{max}^{(3)}=\max_j |x_j^{(3)}|.
```

Le croisement analytiquement naturel est `|x|=1`. Donc :

```text
STATIC_LAMBDA3_INFORMATION_GUARD = REQUIRED
STATIC_LAMBDA3_MIN_DISCRIMINATING_MAGNITUDE = 1
```

Si la classification ordinaire des résidus serait `SUPPORTED` mais
`X_max^(3) < 1`, on ne publie pas le statut ordinaire
`SOFT_LOOP_STATIC_SUPPORTED`. On publie à la place :

```text
SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
```

avec le statut épistémique :

```text
NUMERICAL_CONTROL / NONCONFIRMATORY_FOR_CUTOFF_STABILITY
```

Ce statut signifie que les points `Lambda=3` échantillonnés sont compatibles
avec la courbe à deux niveaux, mais que la bande échantillonnée n'atteint pas
le croisement et est insuffisamment discriminante pour supporter une
revendication de mécanisme à deux niveaux stable au cutoff. Il ne bloque pas
la publication des observables brutes `Lambda=3`. Il ne régénère pas la
grille. Il ne modifie pas `tau_static`.

Ordre de classification :

```text
a) si un L > tau_static             -> SOFT_LOOP_STATIC_DEVIATES
b) sinon si chevauchement précision/frontière
                                     -> SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
c) sinon si tous U <= tau_static ET X_max^(3) < 1
                                     -> SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
d) sinon                            -> SOFT_LOOP_STATIC_SUPPORTED
```

### 6.9 Diagnostic d'excursion de bande à `Lambda=3`

La classification primaire/étendue reste définie à partir de la grille
préenregistrée `Lambda=2`. Si un point physique informatif se projette sur
`|x_j^{(3)}| > 2`, on publie :

```text
STATIC_LAMBDA3_BAND_EXCURSION = YES
```

en listant les points affectés. Cela ne reclasse ni ne retire ces points du
critère ponctuel. Si `Lambda=3` est `DEVIATES` et que chaque point informatif
en défaut (`L>0.10`) se situe hors de `|x^(3)| <= 2`, on publie le diagnostic
de cause :

```text
STATIC_DEVIATION_DRIVER = BAND_EXCURSION
```

Cela reste un résultat `DEVIATES` fail-closed pour la stabilité au cutoff,
mais empêche d'interpréter silencieusement un échec de stress hors bande
comme identique à un échec en bande du mécanisme.

### 6.10 Revendication de mécanisme stable au cutoff

Une revendication de mécanisme à deux niveaux stable au cutoff pour un fond
requiert :

```text
STATIC_STATUS_LAMBDA2 = SOFT_LOOP_STATIC_SUPPORTED
ET
STATIC_STATUS_LAMBDA3 = SOFT_LOOP_STATIC_SUPPORTED
```

Ne qualifient pas :

```text
SOFT_LOOP_STATIC_SUPPORTED_LOW_INFORMATION
SOFT_LOOP_STATIC_DEVIATES
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

Si `Lambda=2` est `SUPPORTED` mais que `Lambda=3` n'est pas `SUPPORTED`
ordinaire : le protocole dynamique de `Lambda=2` peut toujours être calculé ;
la comparaison de troncature SOFT-LOOP interprétée est
`NONCONFIRMATORY`/sensible à la troncature ; aucune revendication de
mécanisme à deux niveaux stable au cutoff n'est autorisée. Cela ne ferme pas :

```text
TRUNCATION_COMPARISON_TOLERANCES = OPEN
```

### 6.11 Oracles signe négatif / `x=0` et provisionalité

Le signe négatif de `x` et `x=0` restent hors de la norme de forme du modèle.
Leurs tolérances quantitatives restent sous :

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```

Par conséquent, `SOFT_LOOP_STATIC_SUPPORTED` autorise l'exécution du
protocole dynamique mais reste PROVISOIRE pour l'interprétation confirmatoire
finale de campagne tant que le contrôle d'oracle numérique zéro/symétrie
n'est pas fermé et validé. Le statut de base n'est pas renommé pour cette
seule provisionalité.

```text
STATIC_SUPPORTED_FINAL_CAMPAIGN_USE =
    REQUIRES_NUMERICAL_ZERO_AND_SYMMETRY_CONTROL_PASS
```

### 6.12 Diagnostic étendu `±4`

Les résidus `±4` sont évalués et publiés avec les mêmes formules lorsqu'ils
sont programmés. Ils restent `EXTENDED_DIAGNOSTIC` et ne peuvent pas à eux
seuls modifier le statut obligatoire de la porte statique.

## 7. Statut

```text
SOFT_LOOP_STATIC_GATE                  = VALIDATED_FOR_FREEZE
STATIC_BEFORE_DYNAMIC                  = MANDATORY
DELTA_C_DYNAMIC_USE_REQUIRES_STATIC    = VALIDATED_FOR_FREEZE
STATIC_COLLAPSE_NUMERICAL_CRITERION    = VALIDATED_FOR_FREEZE
STATIC_COLLAPSE_TOLERANCE              = 0.10
STATIC_COLLAPSE_NORM                   = POINTWISE_L_INFINITY
STATIC_COLLAPSE_GAP_RESIDUAL           = RELATIVE
STATIC_COLLAPSE_PHI_RESIDUAL           = ABSOLUTE
STATIC_COLLAPSE_NUMERICAL_BUDGET       = P_OVER_2P_SIGNED_DEVIATION_DIFFERENCE
STATIC_LAMBDA3_INFORMATION_GUARD       = REQUIRED
STATIC_LAMBDA3_MIN_DISCRIMINATING_MAGNITUDE = 1
STATIC_X_CONTROL_VALUES                = VALIDATED_FOR_FREEZE
STATIC_X_PRIMARY                       = {0, ±1/4, ±1/2, ±1, ±2}
STATIC_COLLAPSE_INFORMATIVE_MAGNITUDES = {1/4, 1/2, 1, 2}
STATIC_X_SATURATION_DIAGNOSTIC         = {±4}
SAME_PHYSICAL_DELTA_ACROSS_CUTOFFS     = MANDATORY
DELTA1_COLLAPSE_PRIMARY_ORACLE         = REJECTED
DELTA1_COLLAPSE_SECONDARY_HYPOTHESIS   = ALLOWED
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
TRUNCATION_COMPARISON_TOLERANCES       = OPEN
```
