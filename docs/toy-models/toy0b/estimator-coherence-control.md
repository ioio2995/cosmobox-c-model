# Toy Model 0B — cohérence entre estimateurs de propagation

Statut : **validé pour gel — support méthodologique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Supports liés : `truncation-comparison-control.md`, `parameter-campaign-structure.md`, `validation-plan.md`, `derivative-error-budget.md`, `temporal-event-solver.md`, `short-time-oracles.md`

Ce document est la source normative détaillée de la cohérence générique entre estimateurs de propagation finis à `delta` fini sur MAIN. Il ferme UNIQUEMENT `ESTIMATOR_COHERENCE_CRITERION`.

## 0. Décision scientifique et portée

```text
ESTIMATOR_COHERENCE_CRITERION = VALIDATED_FOR_FREEZE
```

La cohérence générique à `delta` fini n'exige PAS l'égalité numérique de `C_eff^grow` et `C_eff^thr(eta)` : la spécification énonce déjà que ces estimateurs ne sont pas forcés d'être égaux. L'objet générique de cohérence est l'ORDRE RELATIONNEL PRIMAIRE encodé par :

```math
\Delta_1=\log\frac{C_{O1A}}{C_{O1B}}.
```

Normatif :

```text
ESTIMATOR_COHERENCE_SCOPE = MAIN_FINITE_DELTA_PRIMARY_SIGNAL
ESTIMATOR_COHERENCE_OBJECT = DELTA1_RELATIONAL_ORDERING
ESTIMATOR_MAGNITUDE_EQUALITY_GATE = REJECTED
```

## 1. Convention exacte d'orientation

Au point de référence symétrique, la réflexion exacte échange `O1A <-> O1B`, donc les temps d'événement de référence sont structurellement égaux.

Pour tout estimateur de propagation donné `e` :

```math
C_A=\frac{T_A^{ref}}{T_A^{state}},
\qquad
C_B=\frac{T_B^{ref}}{T_B^{state}}.
```

Donc, sous la symétrie de référence exacte :

```math
\Delta_1=\log\frac{C_A}{C_B}=\log\frac{T_B^{state}}{T_A^{state}}.
```

Convention d'étiquette fixée :

```text
Delta1 > 0  <=>  T_A^state < T_B^state  <=>  ESTIMATOR_ORDERING = O1A_OVER_O1B
```

Signification :

```text
O1A_OVER_O1B = EARLIER_EVENT_ON_O1A
```

De même :

```text
Delta1 < 0  <=>  ESTIMATOR_ORDERING = O1B_OVER_O1A = EARLIER_EVENT_ON_O1B
```

Normatif :

```text
ESTIMATOR_ORDERING_ORIENTATION = DELTA1_POSITIVE_MEANS_O1A_EARLIER_THAN_O1B
```

Ne PAS inférer l'égalité numérique exacte de temps de référence calculés séparément sans la porte finale de l'oracle zéro/symétrie.

## 2. Famille d'estimateurs primaires

En un point MAIN nominal positif à `delta` fini et un cutoff donné :

```text
E_prop = { GROW, THRESHOLD(eta) pour chaque eta du domaine complet admissible requis pour Delta1 en ce point }
```

Normatif :

```text
ESTIMATOR_COHERENCE_THRESHOLD_DOMAIN = EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE
ESTIMATOR_COHERENCE_POSTHOC_ETA_SELECTION = FORBIDDEN
```

Aucune suppression sélective de `eta`. Aucune interpolation vers un `eta` plus commode.

Les niveaux `eta` de seuil sont des membres de contrôle de sensibilité, pas des réplications physiques indépendantes.

Normatif :

```text
GROW_AND_THRESHOLD_AS_INDEPENDENT_EVIDENCE = NO
THRESHOLD_LEVELS_AS_INDEPENDENT_PHYSICAL_EVIDENCE = NO
```

## 3. Ce qui n'est PAS un estimateur de propagation primaire

```text
T_peak       = auxiliaire d'événement/horizon
T_down(eta)  = auxiliaire d'horizon de récurrence
Delta1_short = oracle asymptotique algébrique, pas une mesure de propagation
```

Normatif :

```text
DELTA1_SHORT_ESTIMATOR_COHERENCE_ROLE = ASYMPTOTIC_ORACLE_DIAGNOSTIC_NOT_PRIMARY_ESTIMATOR
```

La règle déjà fermée `SHORT_TIME_THRESHOLD_CONVERGENCE_RULE` reste le lien normatif entre le comportement de seuil profond et `Delta1_short`.

Ne PAS compter `Delta1_short` comme une troisième famille d'estimateur de propagation.

## 4. L'éligibilité scientifique locale précède la cohérence

Pour chaque membre d'estimateur requis, évaluer d'abord sa fermeture de dépendance locale déjà gelée.

`GROW` inclut selon applicabilité :

```text
- résolution d'événement ;
- interprétation côté chemin ;
- garde de récurrence avec sa sémantique d'horizon GROW déjà gelée ;
- toute autre dépendance locale.
```

`THRESHOLD(eta)` inclut :

```text
- admissibilité eta/événement ;
- T_thr ;
- T_down requis ;
- interprétation côté chemin ;
- garde de récurrence ;
- toute autre dépendance locale.
```

Catégories locales normatives :

```text
ESTIMATOR_LOCAL_ELIGIBILITY =
ELIGIBLE_CONFIRMATORY | RESOLVED_LOCAL_VETO | NUMERICALLY_UNRESOLVED | NOT_APPLICABLE
```

Seuls les estimateurs `ELIGIBLE_CONFIRMATORY` participent à une comparaison d'ordre positive résolue.

Un veto scientifique local n'est JAMAIS racheté par la cohérence.

## 5. Intervalle numérique de Delta1 — aucune nouvelle tolérance

Réutiliser le budget propagé `Delta1` déjà gelé pour un seul point (`truncation-comparison-control.md` §11).

Pour l'estimateur `e` au cutoff `Lambda` :

```math
\Delta_e=\Delta_{1,e}^{(2p)}.
```

En un point `Delta1` :

```math
E_{\Delta_1,prop}(e,\Lambda)
=L(r_{A,ref})+L(r_{A,state})+L(r_{B,ref})+L(r_{B,state}).
```

Utiliser :

```math
e_\Delta(e)=\max\left(E_{\Delta_1,prop}(e,\Lambda),\left|\Delta_{1,e}^{(2p)}-\Delta_{1,e}^{(p)}\right|\right).
```

Définir :

```math
I_e=\left[\Delta_e-e_\Delta(e),\;\Delta_e+e_\Delta(e)\right].
```

Ceci est un intervalle numérique opérationnel, pas un intervalle de confiance probabiliste.

Normatif :

```text
ESTIMATOR_ORDERING_SIGN_RESOLUTION = EXISTING_PROPAGATED_INTERVAL_NO_NEW_ZERO_THRESHOLD
```

## 6. Classification de l'ordre

Pour un estimateur `e` `ELIGIBLE_CONFIRMATORY` :

```text
si lower(I_e) > 0 : ESTIMATOR_ORDERING = O1A_OVER_O1B
si upper(I_e) < 0 : ESTIMATOR_ORDERING = O1B_OVER_O1A
si 0 dans I_e     : ESTIMATOR_ORDERING = ORDERING_NUMERICALLY_UNRESOLVED
```

Ceci ne déclare PAS `Delta1` exactement nul. Cela indique seulement que l'ordre n'est pas résolu au-delà du budget numérique propagé déjà gelé.

## 7. Conditionnalité finale zéro/symétrie

Le contrôle final zéro/symétrie peut imposer une distinction préenregistrée plus stricte entre valeur non nulle numériquement résolue et valeur effectivement compatible avec zéro/symétrie.

Toutes les revendications d'ordre du signal fini de ce lot restent donc conditionnées à ce contrôle final.

Normatif :

```text
ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL = YES
```

Jusqu'à la fermeture de `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES` :

- `ROBUST_COHERENT_ORDERING` est un statut de cohérence d'estimateur provisoire ;
- `ESTIMATOR_ORDERING_CONFLICT` est un conflit d'ordre résolu provisoire sous l'intervalle propagé existant ;
- ni l'un ni l'autre n'est promu en revendication finale que `Delta1 != 0`.

Ne PAS affaiblir le routage interne actuel. Ne PAS définir ici la future tolérance de zéro.

## 8. Cohérence interne de la famille de seuils

Inspecter TOUS les membres `eta` requis du domaine de seuil gelé.

Parmi les estimateurs de seuil `ELIGIBLE_CONFIRMATORY` :

```text
si au moins deux ordres de seuil résolus ont des signes opposés :
    THRESHOLD_FAMILY_COHERENCE = ORDERING_CONFLICT

sinon si aucun ordre résolu opposé n'existe mais qu'un ordre de seuil
ELIGIBLE_CONFIRMATORY requis est numériquement non résolu :
    THRESHOLD_FAMILY_COHERENCE = NUMERICALLY_INCONCLUSIVE

sinon si chaque ordre de seuil éligible est résolu et que tous les ordres
résolus concordent :
    THRESHOLD_FAMILY_COHERENCE = COHERENT_O1A_OVER_O1B
    ou
    THRESHOLD_FAMILY_COHERENCE = COHERENT_O1B_OVER_O1A
```

Les membres `eta` à veto local résolu / non applicables ne sont PAS silencieusement écartés : leur profil d'éligibilité est publié et affecte la sémantique de couverture ci-dessous (§12).

Aucun moyennage. Aucun vote majoritaire.

Un seul ordre de seuil éligible résolu opposé suffit à établir un conflit d'ordre d'estimateur résolu à l'intérieur de la famille de seuils.

## 9. Correction de blocage — l'éligibilité n'est pas l'ordre

REJETER le routage initial `ESTIMATOR_ELIGIBILITY_CONFLICT` en tant que contre-exemple d'ordre résolu.

Remplacer par :

```text
ESTIMATOR_ELIGIBILITY_ASYMMETRY
```

Définition :

`ESTIMATOR_ELIGIBILITY_ASYMMETRY` = le profil résolu d'éligibilité/veto local diffère entre familles/membres d'estimateurs requis, alors qu'aucun ordre opposé résolu n'a été établi entre estimateurs éligibles.

Exemples :

```text
- THRESHOLD(eta) est ELIGIBLE_CONFIRMATORY alors que GROW a un veto résolu
  de chemin ou de récurrence ;
- GROW est éligible alors qu'un ou plusieurs niveaux de seuil requis ont
  des vetos locaux résolus ;
- tous les membres d'estimateur requis sont localement vetotés mais les
  profils de veto résolus diffèrent.
```

Rôle :

```text
ESTIMATOR_ELIGIBILITY_ASYMMETRY_ROLE = NONCONFIRMATORY_COVERAGE_LIMITATION_NOT_ORDERING_CONFLICT
```

Ceci est une LIMITATION CONNUE DE COUVERTURE/INTERPRÉTABILITÉ. Cela ne signifie PAS « l'ordre/le signe dépend du choix d'estimateur ».

Normatif :

```text
ESTIMATOR_ELIGIBILITY_CONFLICT_AS_ORDERING_COUNTEREXAMPLE = REJECTED
```

## 10. Comparaison GROW vs seuil

Lorsque :

- `GROW` est `ELIGIBLE_CONFIRMATORY` avec ordre résolu ;
- la famille de seuils éligible a un ordre résolu cohérent ;

alors, même ordre :

```text
ESTIMATOR_COHERENCE_POINT = ROBUST_COHERENT_ORDERING
```

ordre opposé :

```text
ESTIMATOR_COHERENCE_POINT = ESTIMATOR_ORDERING_CONFLICT
```

`ESTIMATOR_ORDERING_CONFLICT` est `CONTROL_SENSITIVE` / `NONCONFIRMATORY_FOR_ESTIMATOR_INDEPENDENT_ORDERING`.

Ce n'est PAS :

- une falsification de Toy 0B ;
- une erreur d'implémentation lorsque les deux estimateurs sont valides ;
- un motif pour écarter un estimateur.

Un croisement dynamique légitime entre le régime de seuil court/profond et l'échelle GROW peut produire un tel conflit. C'est une dépendance protocolaire réelle de l'ordre sur la famille d'estimateurs déclarée.

## 11. Routage limité par la couverture

Si aucun conflit d'ordre résolu n'existe :

```text
A. toute ESTIMATOR_ELIGIBILITY_ASYMMETRY :
   ESTIMATOR_COHERENCE_POINT = ESTIMATOR_ELIGIBILITY_ASYMMETRY

B. toute dépendance/ordre numérique requis non résolu :
   ESTIMATOR_COHERENCE_POINT = NUMERICALLY_INCONCLUSIVE

C. si toutes les familles d'estimateurs requises sont résolues mais
   localement vetotées pour le même profil/raison scientifique :
   ESTIMATOR_COHERENCE_POINT = NONCONFIRMATORY_COMMON_LOCAL_VETO

D. si aucun estimateur de seuil n'est scientifiquement applicable :
   ESTIMATOR_COHERENCE_POINT = NOT_APPLICABLE_NO_THRESHOLD_ESTIMATOR

E. delta=0 :
   ESTIMATOR_COHERENCE_POINT = NOT_APPLICABLE_STRUCTURAL_ZERO
```

Aucun statut limité par la couverture ne peut être reformulé comme preuve positive de dépendance à l'estimateur.

## 12. Cardinalité effective de la famille — publication obligatoire

Pour chaque point évalué, publier :

```text
ESTIMATOR_COHERENCE_REQUIRED_THRESHOLD_COUNT
    = nombre de membres eta requis par le domaine de cohérence gelé,
      avant filtrage d'éligibilité locale.

ESTIMATOR_COHERENCE_ELIGIBLE_THRESHOLD_COUNT
    = nombre de membres de seuil ELIGIBLE_CONFIRMATORY.

ESTIMATOR_COHERENCE_RESOLVED_THRESHOLD_ORDER_COUNT
    = nombre de membres de seuil éligibles avec ordre résolu.

ESTIMATOR_COHERENCE_EFFECTIVE_PROPAGATION_ESTIMATOR_COUNT
    = nombre de membres d'estimateur de propagation éligibles/résolus
      soutenant effectivement l'énoncé de cohérence d'ordre, GROW inclus
      lorsqu'éligible/résolu.
```

Normatif :

```text
ESTIMATOR_COHERENCE_CARDINALITY_DIAGNOSTICS = MANDATORY_PUBLICATION
```

Aucun comptage minimal n'est introduit. Un point avec un seul niveau de seuil admissible/résolu peut néanmoins obtenir un statut de cohérence, mais la revendication DOIT être explicitement restreinte à la famille d'estimateurs admissible EFFECTIVE réellement réalisée en ce point.

Ne PAS emprunter la règle « minimum 3 niveaux » de la convergence à temps court ; elle appartient à un contrôle scientifique distinct.

## 13. Sémantique de la revendication

Remplacer tout énoncé trop large par :

```text
PRIMARY_RELATIONAL_ORDERING_ROBUST_OVER_EFFECTIVE_ADMISSIBLE_PREREGISTERED_ESTIMATOR_FAMILY
```

Cela signifie uniquement : parmi les membres d'estimateur préenregistrés, scientifiquement éligibles et numériquement résolus en ce point, aucun désaccord d'ordre résolu n'a été trouvé.

Cela ne signifie PAS :

- que les magnitudes de croissance et de seuil sont égales ;
- que tout `eta` préenregistré était scientifiquement éligible ;
- que tous les estimateurs de propagation concevables concordent ;
- qu'une vitesse de propagation universelle existe.

Le profil d'éligibilité/cardinalité DOIT accompagner la revendication.

## 14. Diagnostics obligatoires de magnitude

Publier :

```text
Delta1_grow
Delta1_thr(eta) pour chaque eta requis
```

Publier également, lorsque les deux quantités sont définies :

```math
D_{est}(\eta)=\Delta_{1,thr}(\eta)-\Delta_{1,grow}.
```

Publier l'étendue/plage de seuil lorsqu'elle est définie.

Mais :

```text
ESTIMATOR_MAGNITUDE_EQUALITY_GATE = REJECTED
```

Ne PAS appliquer à la cohérence générique d'estimateur :

- `TRUNCATION_TOLERANCE_VALUES` ;
- `STATIC_COLLAPSE_TOLERANCE` ;
- toute nouvelle tolérance scalaire.

Les différences de magnitude sont `DIAGNOSTIC_ONLY` sauf si un autre contrôle déjà gelé leur donne un rôle.

## 15. Ensemble des statuts de point

Statuts de point finaux exhaustifs :

```text
ESTIMATOR_COHERENCE_POINT =
ROBUST_COHERENT_ORDERING |
ESTIMATOR_ORDERING_CONFLICT |
ESTIMATOR_ELIGIBILITY_ASYMMETRY |
NUMERICALLY_INCONCLUSIVE |
NONCONFIRMATORY_COMMON_LOCAL_VETO |
NOT_APPLICABLE_STRUCTURAL_ZERO |
NOT_APPLICABLE_NO_THRESHOLD_ESTIMATOR
```

Ne PAS utiliser `ESTIMATOR_ELIGIBILITY_CONFLICT` comme contre-exemple d'ordre.

## 16. Agrégation MAIN — corrigée

Agréger uniquement les points MAIN positifs nominaux à `delta` fini. Les points de zéro structurel à `delta=0` sont exclus de cet agrégat de signal fini.

Aucun moyennage. Aucun vote majoritaire.

Priorité :

```text
1. si UN point quelconque est ESTIMATOR_ORDERING_CONFLICT :
   ESTIMATOR_COHERENCE_MAIN_STATUS = CONTROL_SENSITIVE
   (un contre-exemple d'ordre résolu domine)

2. sinon si UN point quelconque est NUMERICALLY_INCONCLUSIVE :
   ESTIMATOR_COHERENCE_MAIN_STATUS = NUMERICALLY_INCONCLUSIVE

3. sinon si UN point quelconque est :
   - ESTIMATOR_ELIGIBILITY_ASYMMETRY ;
   - NONCONFIRMATORY_COMMON_LOCAL_VETO ;
   - NOT_APPLICABLE_NO_THRESHOLD_ESTIMATOR ;
   ESTIMATOR_COHERENCE_MAIN_STATUS = NONCONFIRMATORY_COVERAGE_LIMITED

4. sinon, chaque point MAIN à delta fini est ROBUST_COHERENT_ORDERING :
   ESTIMATOR_COHERENCE_MAIN_STATUS = ROBUST_COHERENT
```

Normatif :

```text
ESTIMATOR_COHERENCE_MAIN_AGGREGATION = POINTWISE_NO_AVERAGING_ORDERING_CONFLICT_ONLY_DOMINATES_AS_PROTOCOL_DEPENDENCE
```

Important : une asymétrie d'éligibilité ne devient JAMAIS `CONTROL_SENSITIVE` au seul motif que différentes familles d'estimateurs ont des horizons de chemin/récurrence différents.

## 17. Delta négatif

La covariance exacte inverse l'étiquette d'ordre `Delta1` :

```text
positif  O1A_OVER_O1B  <->  négatif  O1B_OVER_O1A
```

et réciproquement. La CLASSE de cohérence doit être préservée.

Normatif :

```text
ESTIMATOR_COHERENCE_COVARIANCE_ROLE = IMPLEMENTATION_ORACLE_ONLY
```

Points négatifs : AUCUNE évidence physique indépendante.

## 18. Rôle du cutoff

Cohérence primaire : `Lambda=2`.

Normatif :

```text
ESTIMATOR_COHERENCE_PRIMARY_CUTOFF = Lambda=2
```

Aux points de stress sélectionnés `Lambda=3` : appliquer le MÊME protocole catégoriel de cohérence d'estimateur sur les estimateurs/membres `eta` physiques appariés.

Le statut de cohérence résultant fait partie de la fermeture de dépendance complète de troncature déjà gelée.

Normatif :

```text
ESTIMATOR_COHERENCE_LAMBDA3_ROLE = DERIVED_STATUS_UNDER_EXISTING_TRUNCATION_CONTROL
```

Aucune nouvelle tolérance de troncature.

## 19. Oracle exact de rééchelonnement temporel

Pour le contrôle synthétique exact :

```math
H_s=sH_{ref},
```

structurellement :

```math
F_s(t)=F_{ref}(st),
```

et donc :

```math
C_{eff}^{grow}=C_{eff}^{thr}(\eta)=s
```

pour tout `eta` applicable, et `Delta1=0`.

C'est le SEUL cas générique ici où l'égalité exacte de `C_eff` de croissance et de seuil est un théorème.

L'oracle est scientifiquement précieux comme test d'implémentation de bout en bout de :

- rééchelonnement temporel ;
- résolution d'événement ;
- niveaux `eta` absolus ;
- assemblage `C_eff`.

Cependant ce lot ne choisit PAS :

- la grille numérique `s` ;
- le seuil d'égalité/zéro flottant.

Normatif :

```text
ESTIMATOR_RESCALING_ORACLE_ROLE = MANDATORY_IMPLEMENTATION_CONTROL
ESTIMATOR_RESCALING_ORACLE_PARAMETERIZATION = DEFERRED_TO_NUMERICAL_ZERO_AND_SYMMETRY_CONTROL
ESTIMATOR_RESCALING_ORACLE_CONFIRMATORY_EXECUTION = PENDING_FINAL_ZERO_SYMMETRY_CONTROL
```

Ne PAS créer ici de nouvelle grille `s`. Ne PAS revendiquer que l'oracle a été validé numériquement.

## 20. Rôles extérieur / SOFT-LOOP

Points de stress extérieurs : le même diagnostic de cohérence peut être publié séparément ; ils n'entrent PAS dans l'agrégation MAIN de cohérence.

`Xi1` SOFT-LOOP : exclu de ce critère de cohérence d'estimateur à `delta` fini. Ses propres règles restent autoritatives :

- famille de pas `alpha` ;
- stabilité de dérivée ;
- règles de Richardson.

Normatif :

```text
SOFT_LOOP_XI1_ESTIMATOR_COHERENCE_ROLE = SEPARATE_DERIVATIVE_CONTROL_NOT_PART_OF_PRIMARY_FINITE_DELTA_COHERENCE
```

## 21. Aucune nouvelle tolérance scalaire

Normatif :

```text
ESTIMATOR_COHERENCE_NEW_SCALAR_TOLERANCE = NONE
```

Utiliser uniquement les contrôles déjà gelés :

- précision `p/2p` ;
- budgets propagés d'événement ;
- contrôles `eta`/chemin/récurrence.

Résolution finale exacte de zéro/symétrie reste :

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```

## 22. Bloc de statut final

```text
ESTIMATOR_COHERENCE_CRITERION = VALIDATED_FOR_FREEZE
ESTIMATOR_COHERENCE_SCOPE = MAIN_FINITE_DELTA_PRIMARY_SIGNAL
ESTIMATOR_COHERENCE_OBJECT = DELTA1_RELATIONAL_ORDERING
ESTIMATOR_COHERENCE_THRESHOLD_DOMAIN = EXISTING_COMPLETE_COMMON_ETA_DEPENDENCY_CLOSURE
ESTIMATOR_COHERENCE_POSTHOC_ETA_SELECTION = FORBIDDEN
ESTIMATOR_MAGNITUDE_EQUALITY_GATE = REJECTED
DELTA1_SHORT_ESTIMATOR_COHERENCE_ROLE = ASYMPTOTIC_ORACLE_DIAGNOSTIC_NOT_PRIMARY_ESTIMATOR
ESTIMATOR_ORDERING_SIGN_RESOLUTION = EXISTING_PROPAGATED_INTERVAL_NO_NEW_ZERO_THRESHOLD
ESTIMATOR_ORDERING_ORIENTATION = DELTA1_POSITIVE_MEANS_O1A_EARLIER_THAN_O1B
ESTIMATOR_ORDERING_FINAL_CLAIM_REQUIRES_ZERO_SYMMETRY_CONTROL = YES
ESTIMATOR_ELIGIBILITY_ASYMMETRY_ROLE = NONCONFIRMATORY_COVERAGE_LIMITATION_NOT_ORDERING_CONFLICT
ESTIMATOR_ELIGIBILITY_CONFLICT_AS_ORDERING_COUNTEREXAMPLE = REJECTED
ESTIMATOR_COHERENCE_CARDINALITY_DIAGNOSTICS = MANDATORY_PUBLICATION
ESTIMATOR_COHERENCE_MAIN_AGGREGATION = POINTWISE_NO_AVERAGING_ORDERING_CONFLICT_ONLY_DOMINATES_AS_PROTOCOL_DEPENDENCE
ESTIMATOR_COHERENCE_COVARIANCE_ROLE = IMPLEMENTATION_ORACLE_ONLY
ESTIMATOR_COHERENCE_PRIMARY_CUTOFF = Lambda=2
ESTIMATOR_COHERENCE_LAMBDA3_ROLE = DERIVED_STATUS_UNDER_EXISTING_TRUNCATION_CONTROL
ESTIMATOR_RESCALING_ORACLE_ROLE = MANDATORY_IMPLEMENTATION_CONTROL
ESTIMATOR_RESCALING_ORACLE_PARAMETERIZATION = DEFERRED_TO_NUMERICAL_ZERO_AND_SYMMETRY_CONTROL
ESTIMATOR_RESCALING_ORACLE_CONFIRMATORY_EXECUTION = PENDING_FINAL_ZERO_SYMMETRY_CONTROL
SOFT_LOOP_XI1_ESTIMATOR_COHERENCE_ROLE = SEPARATE_DERIVATIVE_CONTROL_NOT_PART_OF_PRIMARY_FINITE_DELTA_COHERENCE
ESTIMATOR_COHERENCE_NEW_SCALAR_TOLERANCE = NONE
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```
