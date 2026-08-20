# Toy Model 0B — structure de campagne des paramètres

Statut : **validé pour gel — support analytique / qualification préalable**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne la structure imposée au futur domaine de campagne `(g,mu,delta)` avant le choix des valeurs numériques. Il ne fixe encore aucune borne ni grille confirmatoire.

## 1. Rôle des trois paramètres

Le Hamiltonien s'écrit :

```math
H
=H_{hop}
+g V_0
+g\delta V_{stag}
+2\mu N_{even},
```

avec :

```math
V_0=\sum_i E_i^2,
\qquad
V_{stag}=\sum_i(-1)^iE_i^2.
```

La réflexion exacte vérifie :

```math
R H(g,\mu,\delta)R^\dagger
=H(g,\mu,-\delta).
```

À `delta=0`, `R` échange les deux orbites d'arêtes utilisées dans `Delta_1`. Par conséquent :

```math
\boxed{\Delta_1(g,\mu,0)=0}
```

pour tout `g,mu` dans le domaine où le protocole est défini.

`delta` est donc la seule coordonnée déclarée qui brise cette symétrie et autorise `Delta_1 != 0`.

Nuance importante : le terme générateur est en réalité `g*delta*V_stag`. Ainsi `g` n'est pas un simple modulateur indépendant : il règle aussi l'amplitude du générateur de contraste. En particulier :

```math
g=0 \Longrightarrow H \text{ indépendant de } \delta,
```

et donc :

```math
\boxed{\Delta_1(0,\mu,\delta)=0}
```

pour tout `mu,delta`.

Le paramètre `mu` est un modulateur du fond. Aucun élément sector-préservant du groupe déclaré n'impose une covariance `mu <-> -mu`. Les deux signes doivent donc être traités comme des régimes scientifiques distincts.

## 2. Géométrie qualitative de la campagne

La campagne ne doit pas être conçue comme un cube isotrope.

La structure naturelle est :

```text
- une grille de fonds (g,mu),
- croisée avec un axe delta symétrique,
- avec delta=0 comme variété nulle exacte,
- et un sous-ensemble négatif de delta réservé au test end-to-end de covariance.
```

L'oddness exacte impose :

```math
\Delta_1(g,\mu,-\delta)
=-\Delta_1(g,\mu,+\delta).
```

Les points `delta<0` n'ont donc pas besoin de dupliquer toute la densité scientifique de l'axe positif, mais un sous-ensemble miroir doit être préenregistré comme oracle end-to-end. Sa densité reste `OPEN`.

## 3. Domaine structurel de delta

Pour `g>0`, les coefficients électriques des deux sous-réseaux de liens valent :

```math
g(1+\delta),
\qquad
g(1-\delta).
```

Le régime positif nominal exige :

```math
|\delta|<1.
```

À `|delta|=1`, un sous-réseau de liens perd tout coût électrique et le régime change qualitativement. Ces bords sont exclus de la campagne scientifique nominale.

La borne numérique `delta_max<1` reste `OPEN`.

## 4. Structure de l'axe g

`g` est un rapport d'échelle entre énergie électrique et hopping (`J=1`). Un échantillonnage logarithmique des valeurs strictement positives est recommandé parce que les régimes faible et fort couplage sont multiplicatifs, mais ce choix reste un élément de protocole et non un théorème analytique.

Le point :

```math
g=0
```

ne peut pas appartenir à une grille logarithmique et doit être traité séparément comme oracle / régime limite.

Deux limites sont particulièrement informatives :

```text
g -> 0 : faible pénalité électrique, risque accru de sensibilité à la troncature ;
g >> 1 : dynamique de matière fortement ralentie, possibilité de NO_EXIT_BEFORE_EVENT dans la garde de récurrence.
```

Le second énoncé est une attente de régime, pas un oracle exact.

## 5. Contrôle de troncature

Le risque de troncature n'est pas contrôlé uniquement par `g`.

La plus faible raideur électrique vaut :

```math
g_{weak}=g(1-|\delta|).
```

Les contrôles `Lambda=2 -> 3` doivent donc être concentrés en priorité dans les régions où `g_weak` est petit, et non uniquement aux petits `g` à `delta=0`.

Le paramètre `mu` peut en outre modifier les configurations de matière dominantes et donc leur `spread`; les deux signes de `mu` doivent être représentés dans les points de stress de troncature.

La sélection exacte de ces points reste `OPEN`.

## 6. Limite de pur hopping et scaling d=2

Pour :

```math
g=0,
\qquad
\mu=0,
```

le Hamiltonien est de pur hopping et le secteur cible `d=2` est exactement inactif dans la réponse Kubo, selon l'oracle déjà démontré.

Le long du rayon :

```math
\mu=0,
\qquad
\delta=0,
\qquad
g\to0^+,
```

la règle de parité impose au secteur cible `d=2` au moins une insertion diagonale, donc l'amplitude directe est au moins linéaire en `g` et son poids sectoriel intégré est au moins quadratique en `g`, sous régularité du fond.

Il est interdit de transformer cet énoncé en oracle universel :

```math
P_{direct}\propto g^2
```

sans vérifier que :

- le projecteur fondamental varie régulièrement ;
- le coefficient linéaire ne s'annule pas ;
- le temps d'intégration utilisé ne varie pas singulièrement avec `g`.

Le scaling quadratique est donc une **attente structurelle conditionnelle**, pas encore un exposant confirmatoire gelé.

## 7. Qualification préalable de la référence

Le point de référence est :

```math
(g,\mu,\delta)=(1,0,0).
```

La prescription scientifique était déjà définie : fondamental unique -> projecteur pur ; fondamental dégénéré -> mélange uniforme sur tout le sous-espace fondamental.

Une diagonalisation indépendante de qualification préalable a été effectuée avant le gel de la campagne. Elle n'est pas un résultat confirmatoire et doit être divulguée comme information de design.

Résultats :

```text
Lambda = 2
    dim H_phys = 78
    E_GS        = -2.6871308299170664
    d_GS        = 1
    gap_1       = 1.5618418174199504

Lambda = 3
    dim H_phys = 118
    E_GS        = -2.6871308299170558
    d_GS        = 1
    gap_1       = 1.5618418174199824
```

Le fondamental de référence est donc non dégénéré aux deux cutoffs principaux et :

```math
\rho_{ref}=|\Omega\rangle\langle\Omega|.
```

La très forte stabilité numérique de l'énergie et du gap entre `Lambda=2` et `Lambda=3` est informative mais ne remplace pas les contrôles de troncature préenregistrés sur les observables de campagne.

## 8. Symétrie du point de référence

Le point `delta=0` restaure `R`, mais cela vaut pour toute la variété :

```math
\{(g,\mu,0)\}.
```

Il est donc incorrect de dire que `(1,0,0)` est nécessairement « le point le plus symétrique » de toute la campagne simplement parce que `mu=0` supprime un terme. Aucun nouvel élément sector-préservant du groupe déclaré n'est actuellement démontré à `mu=0`.

La qualification de `d_GS` reste néanmoins utile parce que ce point sert de référence commune à tous les contrastes.

## 9. Règle méthodologique pour la suite

Il est autorisé de qualifier explicitement le point de référence avant le gel des bornes, à condition de traiter le résultat comme information de design divulguée.

En revanche, une cartographie large de `d_GS` ou d'autres observables sur un domaine encore non figé constituerait une exploration pilote susceptible d'influencer les bornes. Elle devrait alors être déclarée comme telle avant utilisation.

La séquence recommandée est donc :

```text
1. qualifier le point de référence ;
2. fixer les bornes structurelles et la grille de campagne ;
3. préenregistrer les règles de traitement des points dégénérés ;
4. seulement ensuite exécuter la cartographie confirmatoire d_GS et des observables.
```

## 10. Statut

```text
DELTA_ZERO_NULL_MANIFOLD            = VALIDATED_FOR_FREEZE
DELTA_ODD_COVARIANCE                = VALIDATED_FOR_FREEZE
DELTA_ONLY_DECLARED_SYMMETRY_BREAK  = VALIDATED_FOR_FREEZE
G_TIMES_DELTA_GENERATOR             = VALIDATED_FOR_FREEZE
G_ZERO_DELTA_COLLAPSE               = VALIDATED_FOR_FREEZE
MU_SIGN_COVARIANCE                  = NOT_ESTABLISHED
MU_BOTH_SIGNS_REQUIRED              = VALIDATED_FOR_FREEZE
DELTA_POSITIVITY_BOUND              = VALIDATED_FOR_FREEZE
DELTA_NUMERICAL_BOUND               = OPEN
G_GRID_VALUES                       = OPEN
MU_GRID_VALUES                      = OPEN
NEGATIVE_DELTA_ORACLE_SUBSET        = OPEN
TRUNCATION_STRESS_POINTS            = OPEN
D2_G2_SCALING                       = CONDITIONAL_EXPECTATION
REFERENCE_GS_QUALIFICATION          = COMPLETED_NONCONFIRMATORY
REFERENCE_D_GS_LAMBDA2              = 1
REFERENCE_D_GS_LAMBDA3              = 1
PARAMETER_CAMPAIGN                  = OPEN
```
