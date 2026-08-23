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

Les points `delta<0` n'ont donc pas besoin de dupliquer toute la densité scientifique de l'axe positif, mais un sous-ensemble miroir doit être préenregistré comme oracle end-to-end. Ce sous-ensemble et son protocole de comparaison sont normatifs et détaillés au §11 ci-dessous (`NEGATIVE_DELTA_ORACLE_SUBSET = VALIDATED_FOR_FREEZE`).

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

Cette sélection est désormais préenregistrée et fixe (définition normative complète : `truncation-design-qualification.md` §8) :

```text
TRUNCATION_STRESS_POINT_SUBSET = VALIDATED_FOR_FREEZE
TRUNCATION_STRESS_POINT_SUBSET_SIZE = 18
TRUNCATION_STRESS_MAIN_POINT_COUNT = 16
TRUNCATION_STRESS_OUTER_POINT_COUNT = 2
TRUNCATION_STRESS_POINT_DESIGN = THREE_AXIS_STRESS_CROSS_PLUS_CONDITIONING_INTERIOR_AND_OUTER_ANCHORS
```

L'ensemble comprend un squelette de stress à trois axes (spine `delta` complète à `g` faible ; spine `g` complète à `mu` négatif et `delta` maximal nominal ; spine `mu` complète à `g` faible et `delta` maximal nominal), une ancre intérieure de calibration `(1,0,2/5)`, deux points de stress extérieurs déjà divulgués `(1/10,0,0)` et `(1,0,9/10)`, et une ancre de stress de conditionnement `(1,-1,0)` motivée par le petit gap déjà divulgué en qualification préalable (`gap_GS ~= 0.214`), sans établir de loi de monotonie globale du gap ni de seuil de petit gap. `g_weak=g(1-|delta|)` motive ce design mais ne constitue pas un théorème de convergence.

Une ancre de référence obligatoire, distincte du sous-ensemble de stress et non comptée dans sa taille, est requise à `Lambda=3` :

```text
TRUNCATION_REFERENCE_ANCHOR = (1,0,0)
TRUNCATION_REFERENCE_ANCHOR_ROLE = MANDATORY_REFERENCE_NOT_STRESS
```

Chaque point sélectionné est comparé sur la fermeture de dépendance scientifique complète requise, avec la fermeture de dépendance `eta` commune déjà gelée aux deux cutoffs, sans rétrécissement différencié :

```text
TRUNCATION_STRESS_OBSERVABLE_SCOPE = FULL_REQUIRED_SCIENTIFIC_DEPENDENCY_CLOSURE
TRUNCATION_THRESHOLD_DOMAIN_RULE = EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE
```

Ce sous-ensemble est fixé avant toute évaluation confirmatoire `Lambda=3` ; aucune extension adaptative ni substitution a posteriori n'est autorisée à partir des résultats observés :

```text
TRUNCATION_STRESS_POSTHOC_SUBSTITUTION = FORBIDDEN
TRUNCATION_STRESS_ADAPTIVE_EXTENSION = REJECTED_FOR_PRIMARY_PREREGISTERED_SUBSET
TRUNCATION_STRESS_NEW_SCALAR_TOLERANCE = NONE
```

Tout point MAIN non sélectionné par ce sous-ensemble n'obtient aucun statut de cutoff certifié par ce protocole clairsemé, et un contrôle réussi ne supporte qu'une absence d'instabilité détectée sur ce sous-ensemble préenregistré, jamais une convergence uniforme sur tout le domaine MAIN :

```text
TRUNCATION_CUTOFF_STATUS_FOR_UNSAMPLED_MAIN_POINT = NOT_CERTIFIED_BY_STRESS_SUBSET
TRUNCATION_STRESS_CLAIM_SCOPE = PREREGISTERED_STRESS_SUPPORT_NOT_UNIFORM_THEOREM
```

Ce sous-ensemble porte exclusivement sur `delta` non négatif ; `delta` négatif reste un oracle d'implémentation de signe déjà couvert par `NEGATIVE_DELTA_ORACLE_SUBSET` (§11) et n'apporte aucune évidence de troncature physique indépendante (`TRUNCATION_NEGATIVE_DELTA_ROLE = IMPLEMENTATION_ORACLE_ONLY`). Il n'absorbe pas SOFT-LOOP : la porte statique `Lambda=2`/`3` déjà gelée de SOFT-LOOP reste inchangée et hors de cette sélection (`SOFT_LOOP_EXISTING_CUTOFF_OBLIGATIONS = UNCHANGED_AND_OUTSIDE_TRUNCATION_STRESS_SUBSET_SELECTION`) ; ce lot n'impose aucune nouvelle campagne dynamique `Xi1` au cutoff (`SOFT_LOOP_DYNAMIC_XI1_CUTOFF_REQUIREMENT_BY_THIS_LOT = NOT_IMPOSED`).

COMMENT ces deux cutoffs sont comparés sur ce sous-ensemble est désormais également fixé (définition normative complète : `truncation-comparison-control.md`) :

```text
TRUNCATION_COMPARISON_TOLERANCES = VALIDATED_FOR_FREEZE
TRUNCATION_TOLERANCE_VALUES = {0.01,0.02,0.05}
TRUNCATION_TOLERANCE_DIMENSIONING = DESIGN_QUALIFICATION_INFORMED_PREREGISTRATION
```

Résumé de la sémantique d'agrégation : chaque point sélectionné reçoit un `TRUNCATION_POINT_STATUS` fail-closed (`ROBUST_UNSTABLE > NUMERICALLY_INCONCLUSIVE > CONTROL_SENSITIVE > ROBUST_STABLE`, sans moyennage) combinant couche catégorielle, métrique d'état, métriques log positives, métrique double de `Delta_1` (absolue + relative symétrique) et admissibilité `eta` évaluée AVANT intersection commune. L'ancre de référence `(1,0,0)` doit être `ROBUST_STABLE` pour toute revendication MAIN robuste-stable ; les 16 points MAIN et les 2 points extérieurs sont agrégés séparément (`TRUNCATION_MAIN_AGGREGATION = POINTWISE_FAIL_CLOSED_NO_AVERAGING`, `TRUNCATION_OUTER_STRESS_ROLE = SEPARATE_DIAGNOSTIC_OUTSIDE_MAIN`). `B2`, l'écart `E_GS` et `F_peak` restent `DIAGNOSTIC_ONLY`. Ce contrôle ne ferme pas `ESTIMATOR_COHERENCE_CRITERION` (fermé séparément par `estimator-coherence-control.md`) ni `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` (fermé séparément par `numerical-zero-symmetry-control.md`), et ne prouve toujours pas la convergence uniforme sur MAIN non échantillonné :

```text
TRUNCATION_STRESS_CLAIM_SCOPE = PREREGISTERED_STRESS_SUPPORT_NOT_UNIFORM_THEOREM
TRUNCATION_CUTOFF_STATUS_FOR_UNSAMPLED_MAIN_POINT = NOT_CERTIFIED_BY_STRESS_SUBSET
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE
```

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

## 11. Oracle end-to-end de covariance en delta négatif (MAIN)

Cette section ferme `NEGATIVE_DELTA_ORACLE_SUBSET`.

### 11.1 Rôle et portée exacts

La réflexion exacte donne `R H(g,mu,delta) R^dagger = H(g,mu,-delta)` pour tout `g,mu`, avec `R` échangeant `O1A<->O1B`. Donc `Delta_1(g,mu,-delta) = -Delta_1(g,mu,+delta)`.

Les points MAIN à `delta<0` ne fournissent donc AUCUNE évidence physique indépendante : ce sont des points de contrôle numérique/implémentation.

Normatif :

```text
NEGATIVE_DELTA_ORACLE_POINT_ROLE = NUMERICAL_CONTROL / IMPLEMENTATION_ORACLE
NEGATIVE_DELTA_ORACLE_PHYSICAL_EVIDENCE_WEIGHT = ZERO
```

Ce contrôle s'applique EXCLUSIVEMENT à MAIN à `delta` fini :

```text
NEGATIVE_DELTA_ORACLE_SUBSET_SCOPE = MAIN_FINITE_DELTA_ONLY
```

Il ne redéfinit pas SOFT-LOOP, qui a déjà ses deux signes dans `STATIC_X_PRIMARY` et ses évaluations `+/-h_k` explicites (§14-16 de `specification.md`). En conséquence, l'énoncé « l'imparité seule de `Delta_1` ne suffit pas comme oracle end-to-end » est borné à MAIN :

```text
DELTA1_ODDNESS_ONLY_AS_END_TO_END_ORACLE = REJECTED_AS_INSUFFICIENT_FOR_MAIN
```

### 11.2 Grille MAIN de référence

Grille déjà fixée (§14 de `specification.md`) :

```text
G_MAIN = {1/4,1/2,1,2}
MU_MAIN = {-1,-3/4,-1/2,0,+1/2,+1}
DELTA_MAIN_POSITIVE = {1/10,1/5,2/5,3/5,4/5}
```

120 points MAIN positifs à `delta` fini. L'oracle négatif n'introduit aucun nouveau point positif.

### 11.3 Base géométrique fixe à 17 points

Partenaires positifs :

```text
S_delta = {(1,0,1/10),(1,0,1/5),(1,0,2/5),(1,0,3/5),(1,0,4/5)}

S_g_extra = {(1/4,0,2/5),(1/2,0,2/5),(2,0,2/5)}

S_mu_extra = {(1,-1,2/5),(1,-3/4,2/5),(1,-1/2,2/5),(1,+1/2,2/5),(1,+1,2/5)}

S_corner = {(1/4,-1,4/5),(1/4,+1,4/5),(2,-1,4/5),(2,+1,4/5)}

S_oracle_base_plus = S_delta union S_g_extra union S_mu_extra union S_corner
```

```text
NEGATIVE_DELTA_ORACLE_BASE_SIZE = 17
NEGATIVE_DELTA_ORACLE_BASE_DESIGN = AXIAL_CROSS_PLUS_INTERACTION_CORNERS
```

Les partenaires négatifs réels sont `mirror_delta(S) = {(g,mu,-d):(g,mu,+d) in S}`.

Important : cette base à 17 points est un SQUELETTE DE RÉGRESSION géométrique déterministe. Sa seule géométrie ne prouve pas la couverture des branches d'exécution dont la localisation dans MAIN n'est pas connue avant l'exécution positive.

### 11.4 Extension déterministe de couverture de branches

L'ensemble final de partenaires positifs est :

```text
S_oracle_plus = S_oracle_base_plus union S_branch_extension_plus
```

L'extension est sélectionnée déterministiquement à partir de l'exécution positive MAIN déjà requise. Aucun pilote exploratoire n'est ajouté. Aucun résultat négatif n'est utilisé pour la sélection.

**Signature de branche.** Pour chaque point MAIN positif à `delta` fini, à `Lambda=2`, définir une signature catégorielle d'exécution à partir des statuts normatifs déjà publiés effectivement pris par ce point, incluant au minimum :

```text
A. CANONICAL_STATE_MODE =
   PURE_GROUND_STATE | UNIFORM_GROUND_SUBSPACE_MIXTURE | STATE_CONSTRUCTION_UNRESOLVED

B. classes terminales d'événement temporel requises pour T_peak, T_grow,
   chaque T_thr(eta) requis, chaque T_down(eta) requis (catégories
   résolu/non-admissible/non-résolu déjà publiées par le solveur d'événements)

C. profil catégoriel terminal côté chemin requis par les observables MAIN
   dérivées : classe de ligne de base, PATH_CONTROL_STATUS, catégories
   numériquement-inconclusive/non-applicable de chemin où présentes

D. profil catégoriel terminal côté récurrence : prédicat relationnel
   RETURN/NO_RETURN/inconclusif le cas échéant, RECURRENCE_STATUS,
   catégorie variance-nulle/non-confirmatoire où présente

E. toute branche catégorielle de contrôle de racine/événement déjà gelée
   changeant la sémantique d'exécution des observables MAIN requises
```

`NEAR_CROSSING` n'est PAS utilisé comme déclencheur de branche dans ce lot ; aucun nouveau seuil numérique n'est créé pour définir une branche.

```text
NEGATIVE_DELTA_ORACLE_BRANCH_SIGNATURE = PUBLISHED_CATEGORICAL_EXECUTION_STATUS_TUPLE
```

**Algorithme de sélection.** Une fois que les 120 points MAIN positifs ont complété leur calcul côté positif suffisamment pour émettre la signature catégorielle :

```text
1. calculer l'ensemble des signatures représentées par S_oracle_base_plus ;
2. pour chaque signature MAIN positive réalisée NON représentée par la base,
   choisir exactement UN représentant : le point MAIN positif
   lexicographiquement premier ayant cette signature
   (ordre canonique : g croissant, mu croissant, delta croissant) ;
3. réunir tous ces représentants dans S_branch_extension_plus ;
4. figer l'ensemble final complet `S_oracle_plus` (base + extension) ainsi
   que son ensemble miroir négatif dérivé, AVANT TOUTE exécution
   négative-delta MAIN, y compris les 17 miroirs de la base géométrique
   fixe ;
5. ne jamais itérer ni agrandir cet ensemble sur la base de résultats
   observés à -delta.
```

```text
NEGATIVE_DELTA_ORACLE_BRANCH_COVERAGE_RULE = REQUIRED
NEGATIVE_DELTA_ORACLE_BRANCH_EXTENSION = ONE_LEXICOGRAPHIC_REPRESENTATIVE_PER_UNCOVERED_REALIZED_SIGNATURE
NEGATIVE_DELTA_ORACLE_BRANCH_EXTENSION_SOURCE = POSITIVE_MAIN_STATUSES_ONLY
NEGATIVE_DELTA_RESULTS_AFFECT_SUBSET_SELECTION = FORBIDDEN
NEGATIVE_DELTA_ORACLE_SET_FREEZE_TIMING = BEFORE_ANY_NEGATIVE_MAIN_EXECUTION
```

**Diagnostics obligatoires de couverture de branches.** Une fois la sélection ci-dessus effectuée, publier :

```text
NEGATIVE_DELTA_ORACLE_REALIZED_SIGNATURE_COUNT
```

= nombre de signatures catégorielles de branche distinctes réalisées sur l'ensemble des 120 points MAIN positifs à `delta` fini, à `Lambda=2`.

```text
NEGATIVE_DELTA_ORACLE_BASE_SIGNATURE_COUNT
```

= nombre de ces signatures réalisées déjà représentées par la base à 17 points.

```text
NEGATIVE_DELTA_ORACLE_BRANCH_EXTENSION_SIZE
```

= `|S_branch_extension_plus|`.

```text
NEGATIVE_DELTA_ORACLE_FINAL_SIZE
```

= `|S_oracle_plus|`.

```text
NEGATIVE_DELTA_ORACLE_BRANCH_COVERAGE_DIAGNOSTICS = MANDATORY_PUBLICATION
```

Ces comptages sont `DIAGNOSTIC_ONLY`. Ils :

- ne créent pas de diversité minimale requise ;
- ne changent pas `PASS`/`FAIL` par eux-mêmes ;
- ne modifient pas l'appartenance au sous-ensemble après gel ;
- ne prétendent pas qu'un grand nombre de signatures implique la correction.

Avertissement : une partition de signatures réalisées dégénérée (par exemple une seule signature partagée par la plupart/la totalité des points MAIN positifs) doit être visible dans la publication et ne doit jamais être décrite comme une forte couverture de branches au seul motif que l'algorithme déterministe s'est achevé.

Cette règle est information-monotone : elle ne peut qu'ajouter du travail de test, jamais racheter un `FAIL` ni améliorer un résultat scientifique. Taille finale :

```text
17 <= NEGATIVE_DELTA_ORACLE_TOTAL_SIZE <= 120
NEGATIVE_DELTA_ORACLE_TOTAL_SIZE = DERIVED_BOUNDED_17_TO_120
```

`NEGATIVE_DELTA_ORACLE_SUBSET_SIZE = 17` n'est jamais écrit ; seule la base est de taille fixe.

### 11.5 Point requis non exécuté

Tout point de `S_oracle_plus` est REQUIS. Si son miroir négatif n'est pas exécuté :

```text
DELTA_COVARIANCE_ORACLE_POINT = NUMERICALLY_INCONCLUSIVE
```

Un point requis manquant n'est jamais silencieusement omis de l'agrégation.

### 11.6 Recalcul indépendant côté négatif

Ceci ferme le blocage Opus B2.

```text
NEGATIVE_DELTA_ORACLE_INDEPENDENT_RECOMPUTATION = REQUIRED
```

Pour chaque miroir requis `theta_minus=(g,mu,-d)`, le côté `-delta` DOIT être produit par le pipeline générique avec `delta=-d` en entrée indépendante. Objets sign-dérivés requis indépendamment : `H(g,mu,-d)` assemblé génériquement ; système propre / projecteurs spectraux ; `rho_minus` canonique ; poids spectraux sign-dépendants ; `chi_pq(t)` ; événements temporels ; quantités et statuts de pureté de chemin ; quantités et statuts de récurrence ; valeurs `C_eff` d'orbite ; `Delta_1` final.

INTERDIT : `H_minus:=R H_plus R^dagger` ; `rho_minus:=R rho_plus R^dagger` ; réutilisation des vecteurs propres/projecteurs/poids spectraux `+delta` pour fabriquer le côté `-delta` ; `C_O1A(-d):=C_O1B(+d)` par substitution analytique ; `Delta_1(-d):=-Delta_1(+d)` ; toute substitution sign-dérivée équivalente rendant l'oracle vrai par construction.

Partage autorisé : base physique immuable, définitions d'opérateurs, géométrie/tables de permutation déclarées, objets de référence communs analytiquement indépendants du signe de `delta`.

Si la règle d'indépendance est violée :

```text
DELTA_COVARIANCE_ORACLE_POINT = INVALID_BY_CONSTRUCTION
NEGATIVE_DELTA_ORACLE_CONTROL = FAIL
```

Ceci n'est jamais réinterprété comme `NOT_APPLICABLE`.

### 11.7 Fermeture de dépendance complète mappée et oracle à deux couches

```text
NEGATIVE_DELTA_ORACLE_COMPARISON_LEVEL = FULL_MAPPED_DEPENDENCY_CLOSURE
```

Pour chaque paire `+/-` recalculée indépendamment, comparer au minimum : la couche spectrale/d'état (branche d'état canonique, `d_GS`/statut spectral catégoriel, `E_GS` et `gap_GS` où la comparaison continue s'applique) ; la couche relationnelle (`O1A(-d)` correspond à `O1B(+d)`, `O1B(-d)` correspond à `O1A(+d)`) ; les événements temporels requis (`T_peak`, `T_grow`, `T_thr(eta)`, `T_down(eta)`) ; les profils/statuts mappés de garde de chemin ; les profils/statuts mappés de récurrence ; les estimateurs d'orbite `C_O1A^e(-d)=C_O1B^e(+d)`, `C_O1B^e(-d)=C_O1A^e(+d)` lorsqu'applicable/résolu ; enfin `Delta_1^e(-d)=-Delta_1^e(+d)`. Les comparaisons de famille de seuils utilisent uniquement la fermeture de dépendance `eta` commune déjà validée, sans rétrécissement différencié entre les deux signes.

Séparer :

```text
DELTA_COVARIANCE_ORACLE_DISCRETE_LAYER
DELTA_COVARIANCE_ORACLE_CONTINUOUS_LAYER
```

La couche discrète compare les correspondances catégorielles/de statut, sans nouvelle tolérance d'égalité flottante ; `PASS` uniquement si les deux côtés sont individuellement résolus et leurs branches catégorielles symétriquement cohérentes ; un côté non résolu donne `NUMERICALLY_INCONCLUSIVE`.

La couche continue compare `E_GS`, gap, temps d'événement, diagnostics continus de chemin/récurrence, `C_eff`, `Delta_1`, etc. ; ses seuils `PASS`/`FAIL` sont désormais fournis par `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE` (`NEGATIVE_DELTA_ORACLE_CONTINUOUS_TOLERANCE_SOURCE = NUMERICAL_ZERO_AND_SYMMETRY_CONTROL` ; définition normative complète : `numerical-zero-symmetry-control.md`). Ce lot ne redéfinit ni le sous-ensemble, ni la grille, ni la logique de branche de l'oracle de covariance négative ci-dessus.

**Diagnostic d'asymétrie de résolution.** Pour chaque paire `+/-` requise, enregistrer si un signe est résolu alors que le partenaire mappé est numériquement non résolu. Publier :

```text
NEGATIVE_DELTA_ORACLE_RESOLUTION_ASYMMETRY_COUNT
```

ainsi que les points de paramètres / objets mappés affectés.

```text
NEGATIVE_DELTA_ORACLE_RESOLUTION_ASYMMETRY_DIAGNOSTIC = MANDATORY_PUBLICATION
```

Rôle : `DIAGNOSTIC_ONLY`. Ceci ne crée aucune nouvelle règle de `FAIL` autonome. La sémantique existante reste inchangée :

- un décalage résolu au-delà de la tolérance applicable future -> `FAIL` ;
- un côté requis non résolu, sans `FAIL` résolu -> `NUMERICALLY_INCONCLUSIVE`.

```text
NEGATIVE_DELTA_ORACLE_NEW_SCALAR_TOLERANCE = NONE
```

### 11.8 Statuts de point et agrégation

```text
DELTA_COVARIANCE_ORACLE_POINT = PASS | FAIL | NUMERICALLY_INCONCLUSIVE | NOT_APPLICABLE | INVALID_BY_CONSTRUCTION
```

`PASS` : toutes les comparaisons mappées discrètes et continues applicables requises passent sous leurs critères déjà/ultérieurement préenregistrés. `FAIL` : au moins une comparaison mappée résolue requise viole la covariance. `NUMERICALLY_INCONCLUSIVE` : au moins une comparaison ou exécution requise est non résolue/manquante, sans `FAIL` résolu. `NOT_APPLICABLE` : uniquement quand l'objet scientifique mappé est structurellement non défini sur LES DEUX signes pour la même raison symétrique. `INVALID_BY_CONSTRUCTION` : le recalcul indépendant a été violé. Un veto scientifique symétriquement cohérent (contamination de chemin, contamination de récurrence, non-applicabilité d'événement) n'est PAS automatiquement un échec de l'oracle : la comparaison teste si les deux signes se transforment de façon cohérente.

Agrégation au niveau sous-ensemble, fail-closed :

```text
NEGATIVE_DELTA_ORACLE_CONTROL = FAIL
    si un point quelconque est FAIL, ou INVALID_BY_CONSTRUCTION

sinon NEGATIVE_DELTA_ORACLE_CONTROL = NUMERICALLY_INCONCLUSIVE
    si au moins un point requis est NUMERICALLY_INCONCLUSIVE

sinon NEGATIVE_DELTA_ORACLE_CONTROL = PASS
    ssi chaque point requis est PASS ou NOT_APPLICABLE symétriquement cohérent,
    et qu'il existe au moins un point applicable PASS (pas de PASS vide)
```

### 11.9 Règle de cutoff

```text
NEGATIVE_DELTA_ORACLE_PRIMARY_CUTOFF = Lambda=2
```

Tous les points oracle MAIN dérivés finaux sont mirorrés à `Lambda=2`. Pour `Lambda=3` :

```text
S_oracle_plus^(Lambda3) = S_oracle_plus intersect S_truncation_plus^(Lambda3)
```

Cette dépendance est `DERIVED_PENDING_TRUNCATION_STRESS_POINT_SUBSET`. Si l'intersection future est non vide : mirorrer exactement cette intersection à `Lambda=3`. Si elle est vide : utiliser l'ancre de repli déterministe `(g,mu,delta)=(1,0,2/5)` et son miroir négatif à `Lambda=3`.

```text
NEGATIVE_DELTA_ORACLE_LAMBDA3_RULE = TRUNCATION_INTERSECTION_OR_FIXED_ANCHOR_FALLBACK
NEGATIVE_DELTA_ORACLE_LAMBDA3_FALLBACK = (1,0,+/-2/5)
```

Ce repli est un oracle d'implémentation de signe uniquement ; il ne devient pas un point de stress de troncature.

Le sous-ensemble de stress de troncature étant désormais fixe (§5 ; définition normative complète : `truncation-design-qualification.md` §8), l'intersection `S_oracle_plus intersect S_truncation_plus^(Lambda3)` contient structurellement au moins `(1,0,2/5)`. La règle générique de repli ci-dessus n'est pas supprimée et reste une garde de sécurité valide pour le protocole général, mais elle n'est PAS déclenchée pour cette campagne :

```text
NEGATIVE_DELTA_ORACLE_LAMBDA3_FALLBACK_STATUS_FOR_CURRENT_TRUNCATION_SUBSET = NOT_TRIGGERED_STRUCTURALLY
```

### 11.10 Exclusions / couverture résiduelle

Ne PAS ajouter `g=0`, `g=0.10`, `|delta|=0.9` à l'oracle négatif MAIN. À `g=0`, `delta` est structurellement inactif et l'oracle de signe dégénère vers l'oracle nul déjà existant. `g=0.10` et `|delta|=0.9` sont des points de stress/qualification divulgués séparés, hors MAIN.

```text
NEGATIVE_DELTA_ORACLE_EXCLUDED_STRESS_POINTS = {g=0.10 stress, |delta|=0.9 stress}
```

Leur covariance de signe n'est PAS certifiée par l'oracle négatif MAIN. `NEGATIVE_DELTA_ORACLE_CONTROL = PASS` ne se généralise jamais silencieusement en « toute covariance de signe de tout protocole secondaire/de stress passe ».

### 11.11 Absence d'évidence physique / absence de réglage

Les points de l'oracle négatif NE DOIVENT PAS : compter comme évidence physique indépendante ; augmenter le numérateur/dénominateur d'évidence ; régler `Gamma` ; régler `EPS_PATH` ; régler `eta` ; régler les pas de dérivée ; sélectionner les points de stress de troncature ; sélectionner les tolérances de comparaison de troncature ; sélectionner la cohérence d'estimateur ; sélectionner la tolérance numérique de zéro/symétrie ; modifier la base à 17 points ; modifier l'algorithme d'extension de branche. Les points MAIN à `+delta` restent les observations scientifiques.

## 12. Statut

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
NEGATIVE_DELTA_ORACLE_SUBSET        = VALIDATED_FOR_FREEZE
NEGATIVE_DELTA_ORACLE_SUBSET_SCOPE  = MAIN_FINITE_DELTA_ONLY
NEGATIVE_DELTA_ORACLE_BASE_SIZE     = 17
NEGATIVE_DELTA_ORACLE_BASE_DESIGN   = AXIAL_CROSS_PLUS_INTERACTION_CORNERS
NEGATIVE_DELTA_ORACLE_BRANCH_COVERAGE_RULE = REQUIRED
NEGATIVE_DELTA_ORACLE_SET_FREEZE_TIMING = BEFORE_ANY_NEGATIVE_MAIN_EXECUTION
NEGATIVE_DELTA_ORACLE_BRANCH_COVERAGE_DIAGNOSTICS = MANDATORY_PUBLICATION
NEGATIVE_DELTA_ORACLE_RESOLUTION_ASYMMETRY_DIAGNOSTIC = MANDATORY_PUBLICATION
NEGATIVE_DELTA_ORACLE_TOTAL_SIZE    = DERIVED_BOUNDED_17_TO_120
NEGATIVE_DELTA_ORACLE_INDEPENDENT_RECOMPUTATION = REQUIRED
NEGATIVE_DELTA_ORACLE_COMPARISON_LEVEL = FULL_MAPPED_DEPENDENCY_CLOSURE
NEGATIVE_DELTA_ORACLE_PRIMARY_CUTOFF = Lambda=2
NEGATIVE_DELTA_ORACLE_LAMBDA3_RULE  = TRUNCATION_INTERSECTION_OR_FIXED_ANCHOR_FALLBACK
NEGATIVE_DELTA_ORACLE_LAMBDA3_FALLBACK = (1,0,+/-2/5)
NEGATIVE_DELTA_ORACLE_POINT_ROLE    = NUMERICAL_CONTROL / IMPLEMENTATION_ORACLE
NEGATIVE_DELTA_ORACLE_NEW_SCALAR_TOLERANCE = NONE
NEGATIVE_DELTA_ORACLE_CONTINUOUS_TOLERANCE_SOURCE = NUMERICAL_ZERO_AND_SYMMETRY_CONTROL
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE
DELTA1_ODDNESS_ONLY_AS_END_TO_END_ORACLE = REJECTED_AS_INSUFFICIENT_FOR_MAIN
TRUNCATION_STRESS_POINT_SUBSET      = VALIDATED_FOR_FREEZE
TRUNCATION_STRESS_POINT_SUBSET_SIZE = 18
TRUNCATION_COMPARISON_TOLERANCES    = VALIDATED_FOR_FREEZE
TRUNCATION_TOLERANCE_VALUES         = {0.01,0.02,0.05}
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