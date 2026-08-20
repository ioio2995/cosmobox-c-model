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
+g\delta V_{\delta}
+2\mu N_{even},
```

avec :

```math
V_0=\sum_i E_i^2,
\qquad
V_{\delta}=\sum_i(-1)^iE_i^2,
```

et :

```math
N_{even}=n_0+n_2+n_4.
```

La notation `V_delta` est normative pour le terme électrique alterné. Elle ne doit pas être confondue avec le terme de matière `2 mu N_even`.

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

Nuance importante : le terme générateur est `g*delta*V_delta`. Ainsi `g` n'est pas un simple modulateur indépendant : il règle aussi l'amplitude du générateur de contraste. En particulier :

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

Résultats spectraux :

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

### 7.1 Qualification du degré cyclique

L'égalité des énergies aux deux cutoffs ne permet pas à elle seule de conclure que le degré cyclique est « gelé ». Elle montre surtout que les états supplémentaires accessibles à `Lambda=3` ne modifient pratiquement pas le fondamental.

Pour un fondamental pur :

```math
\|D_\Phi\|_{HS}^2
=2\,Var_{\rho}(\Phi).
```

La qualification directe donne :

```text
Lambda = 2
    <Phi>                 ~= 0
    Var(Phi)               = 0.0312410968528452
    ||D_Phi||_HS           = 0.249964384874506
    sum_i <E_i^2>          = 0.830720005054357
    weight(max |E_i| = 2)  = 1.6846381433e-6

Lambda = 3
    <Phi>                 ~= 0
    Var(Phi)               = 0.0312410968528456
    ||D_Phi||_HS           = 0.249964384874508
    sum_i <E_i^2>          = 0.830720005054361
    weight(max |E_i| = 3)  = 5.2e-18
```

La direction `D_Phi` est donc clairement active au point de référence et stable sous `Lambda=2 -> 3`.

Une projection numérique de qualification donne en outre :

```text
rank(S_n)                         = 5
||Proj_{S_n}(D_Phi)||_HS          ~= 1e-15
||D_Phi - Proj_{S_n}(D_Phi)||_HS = 0.249964384874506  (Lambda=2)
```

avec le même résultat à `Lambda=3` à la précision machine. Ce résultat est une information de qualification, pas encore un théorème structurel ajouté au protocole.

Pour la configuration de matière alternée `n=b`, qui admet la fibre uniforme la plus large :

```text
P(n=b) ~= 0.372229473184816
```

et, conditionnellement à `n=b`, le zéro-mode est fortement centré :

```text
P(Phi=0 | n=b)   ~= 0.999982470882862
P(Phi=+1 | n=b)  ~= 8.764558569e-6
P(Phi=-1 | n=b)  ~= 8.764558569e-6
```

Cela montre qu'une configuration particulière peut avoir une fibre de flux très froide sans rendre `D_Phi` globalement inactif. Il est donc interdit de déduire des seules populations conditionnelles de `n=b` que le degré cyclique global est gelé.

La référence `g=1` est ainsi **cutoff-froide** vis-à-vis des grands flux ajoutés, mais pas inactive vis-à-vis du degré cyclique représenté par `D_Phi`. Aucune décision de déplacer le domaine vers des `g<1` ne doit être fondée sur la seule coïncidence des énergies `Lambda=2/3`.

## 8. Symétrie du point de référence

Le point `delta=0` restaure `R`, mais cela vaut pour toute la variété :

```math
\{(g,\mu,0)\}.
```

Il est donc incorrect de dire que `(1,0,0)` est nécessairement « le point le plus symétrique » de toute la campagne simplement parce que `mu=0` supprime un terme. Aucun nouvel élément sector-préservant du groupe déclaré n'est actuellement démontré à `mu=0`.

La qualification de `d_GS` reste néanmoins utile parce que ce point sert de référence commune à tous les contrastes.

## 9. Gap fondamental et croisements évités

La multiplicité exacte `d_GS` ne suffit pas à qualifier la régularité du fond. Un gap faible peut rendre le projecteur fondamental très sensible aux paramètres même si `d_GS=1`.

Le rapport de campagne doit donc publier à chaque point :

```text
d_GS
gap_GS
```

avec :

```math
gap_{GS}=E_1-E_0.
```

La prescription d'état canonique reste :

```text
d_GS = 1  -> projecteur pur

d_GS > 1  -> mélange uniforme sur tout le sous-espace fondamental
```

Un drapeau :

```text
NEAR_CROSSING
```

est autorisé et doit être préenregistré avant la campagne sur la base d'un seuil de gap déclaré. Sa valeur numérique reste `OPEN` et doit être gelée avec les tolérances / règles de stabilité, jamais choisie après inspection des résultats.

`NEAR_CROSSING` est un diagnostic de conditionnement et de sensibilité, pas un échec physique automatique. Un petit gap peut représenter une vraie forte susceptibilité du fond.

En particulier, toute estimation de :

```math
\Xi_1=\partial\Delta_1/\partial\delta
```

à proximité d'un point `NEAR_CROSSING` doit être accompagnée d'un contrôle de stabilité de la dérivée. Une dégénérescence exacte ou une non-régularité du projecteur peut rendre la dérivée non applicable plutôt que simplement grande.

## 10. Règle méthodologique pour la suite

Il est autorisé de qualifier explicitement le point de référence avant le gel des bornes, à condition de traiter le résultat comme information de design divulguée.

En revanche, une cartographie large de `d_GS`, du gap ou d'autres observables sur un domaine encore non figé constituerait une exploration pilote susceptible d'influencer les bornes. Elle devrait alors être déclarée comme telle avant utilisation.

La séquence recommandée est donc :

```text
1. qualifier le point de référence ;
2. fixer les bornes structurelles et la grille de campagne ;
3. préenregistrer la publication de d_GS et gap_GS ainsi que le seuil NEAR_CROSSING ;
4. préenregistrer le traitement des dérivées près des petits gaps ;
5. seulement ensuite exécuter la cartographie confirmatoire et les observables.
```

## 11. Statut

```text
DELTA_ZERO_NULL_MANIFOLD            = VALIDATED_FOR_FREEZE
DELTA_ODD_COVARIANCE                = VALIDATED_FOR_FREEZE
DELTA_ONLY_DECLARED_SYMMETRY_BREAK  = VALIDATED_FOR_FREEZE
DELTA_GENERATOR_NAME                = V_delta
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
REFERENCE_D_PHI_ACTIVITY            = ACTIVE_NONCONFIRMATORY
REFERENCE_CUTOFF_EDGE_WEIGHT        = NEGLIGIBLE_NONCONFIRMATORY
GAP_GS_PUBLICATION                  = MANDATORY
NEAR_CROSSING_FLAG                  = VALIDATED_IN_PRINCIPLE
NEAR_CROSSING_THRESHOLD             = OPEN
PARAMETER_CAMPAIGN                  = OPEN
```