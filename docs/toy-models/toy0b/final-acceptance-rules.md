# Toy Model 0B — règles finales d'acceptation pré-gel

Statut : **validé pour gel — support méthodologique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`
Supports liés : `numerical-zero-symmetry-control.md`, `estimator-coherence-control.md`, `truncation-comparison-control.md`, `path-purity-control.md`, `recurrence-control.md`

Ce document est la source normative détaillée de `MODEL0B_FINAL_ACCEPTANCE_RULES`. Il ferme UNIQUEMENT ce paramètre — la manière dont une revendication scientifique finale de 0B est acceptée, routée et publiée à partir des contrôles déjà gelés. Il n'introduit aucune formule numérique de bas niveau nouvelle ; il renvoie systématiquement aux documents normatifs qui les portent déjà.

```text
MODEL0B_FINAL_ACCEPTANCE_RULES = VALIDATED_FOR_FREEZE
```

Ce document n'autorise ni l'implémentation, ni le gel du modèle. Ces décisions restent exclusivement sous l'autorité explicite de Lionel ORCIL via `docs/governance/current-task.md`.

---

## 1. Mode d'acceptation

```text
MODEL0B_FINAL_ACCEPTANCE_MODE = CLAIM_SCOPED_FAIL_CLOSED_DEPENDENCY_CLOSURE

MODEL0B_ACCEPTANCE_AVERAGING              = FORBIDDEN
MODEL0B_ACCEPTANCE_MAJORITY_VOTE          = FORBIDDEN
MODEL0B_ACCEPTANCE_DIAGNOSTIC_AS_CONFIRMATORY = FORBIDDEN
```

Pour toute revendication scientifique `Q` :

1. déterminer si `Q` est structurellement applicable ;
2. si applicable, construire la fermeture de dépendance requise déjà gelée `D(Q)` ;
3. évaluer chaque dépendance requise applicable sous sa sémantique spécialisée déjà gelée ;
4. aucun moyennage, aucune compensation, aucun vote majoritaire, aucune substitution par un diagnostic ;
5. un objet optionnel/diagnostique ne devient jamais un veto sauf si une règle déjà gelée en fait explicitement une dépendance.

---

## 2. Couche méta-statut totale (BL1)

Normatif :

```text
MODEL0B_CLAIM_STATUS =
    PIPELINE_OR_MANDATORY_ORACLE_FAILURE
  | INVALID_BY_CONSTRUCTION
  | NUMERICALLY_INCONCLUSIVE
  | CONTROL_SENSITIVE
  | NONCONFIRMATORY_LOCAL_VETO
  | CONFIRMATORY_ELIGIBLE
  | NOT_APPLICABLE
```

### 2.1 Ordre de routage

**ÉTAPE 0 — applicabilité structurelle.** Si une règle structurelle déjà gelée établit que la revendication n'est pas applicable :

```text
MODEL0B_CLAIM_STATUS = NOT_APPLICABLE
```

et le routage de la revendication s'arrête là.

Sinon, appliquer la précédence suivante :

```text
1. PIPELINE_OR_MANDATORY_ORACLE_FAILURE
2. INVALID_BY_CONSTRUCTION
3. NUMERICALLY_INCONCLUSIVE
4. CONTROL_SENSITIVE
5. NONCONFIRMATORY_LOCAL_VETO
6. CONFIRMATORY_ELIGIBLE
```

### 2.2 Définitions

**`PIPELINE_OR_MANDATORY_ORACLE_FAILURE`** : si une dépendance requise applicable présente une incohérence structurelle/de modèle, OU l'échec d'une famille d'oracle exact obligatoire (`ROBUST_ORACLE_FAIL`, définition : `numerical-zero-symmetry-control.md` §D, §AB). C'est un échec RÉSOLU de cohérence pipeline/théorème. Il ne doit JAMAIS être requalifié en `NUMERICALLY_INCONCLUSIVE`.

Normatif :

```text
MODEL0B_PIPELINE_FAILURE_AS_NUMERICAL_LIMITATION = FORBIDDEN
```

**`INVALID_BY_CONSTRUCTION`** : si une dépendance requise porte son statut existant d'invalidité par construction (par exemple `DELTA_COVARIANCE_ORACLE_POINT = INVALID_BY_CONSTRUCTION`, `numerical-zero-symmetry-control.md` §K).

**`NUMERICALLY_INCONCLUSIVE`** : si aucun échec de précédence supérieure n'existe et qu'au moins une dépendance requise est numériquement non résolue / insuffisamment résolue.

**`CONTROL_SENSITIVE`** : si toutes les dépendances numériques requises sont résolues mais qu'au moins une couche de robustesse/contrôle requise porte sa sémantique `CONTROL_SENSITIVE` déjà gelée.

**`NONCONFIRMATORY_LOCAL_VETO`** : si l'objet scientifique numérique est résolu mais qu'un veto interprétatif/de couverture local déjà gelé empêche la revendication demandée (par exemple asymétrie d'éligibilité d'estimateur, contamination de chemin, `d=3` exclu d'interprétation d'arrivée).

**`CONFIRMATORY_ELIGIBLE`** : uniquement si chaque dépendance requise applicable présente le statut confirmatoire positif exigé par son propre protocole gelé.

---

## 3. Exigence globale du contrôle zéro/symétrie/rang

Pour toute revendication physique finale dont la fermeture de dépendance utilise la politique finale zéro/symétrie/rang :

```text
NUMERICAL_ZERO_AND_SYMMETRY_CONTROL_STATUS = PASS
```

est requis.

Il ne suffit PAS d'énoncer seulement « aucune famille d'oracle obligatoire n'échoue ». Un état de famille inconclusif / sans passage indépendant (`NUMERICALLY_INCONCLUSIVE_NO_INDEPENDENT_PASS`, `numerical-zero-symmetry-control.md` §AB-AC) empêche le contrôle global `PASS` et donc toute revendication confirmatoire qui en dépend.

Ce `PASS` global reste :

```text
NUMERICAL / IMPLEMENTATION CONTROL
PAS UNE ÉVIDENCE PHYSIQUE
```

---

## 4. Deux rangs explicites de revendication `Delta1` (BL2)

Le corpus existant distingue déjà une réponse numérique de Kubo/événement d'une interprétation de cet événement comme arrivée propre. Le chemin et la récurrence ne deviennent PAS une dépendance circulaire de tout énoncé `Delta1`.

### 4.1 `DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY`

```text
DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY = CLAIM_RANK_PRIMARY
```

C'est le rang de revendication PRIMAIRE de 0B à `delta` fini.

Signification : un contraste RELATIONNEL confirmatoire non nul entre observables de temps de réponse de Kubo résolus, entre `O1A` et `O1B`.

Ce n'est PAS, en soi :

- une revendication d'arrivée propre ;
- une revendication de propagation ;
- une revendication de vitesse ;
- une revendication de front causal ;
- une revendication de `C` fondamental.

Fermeture de dépendance minimale requise pour un point donné et un estimateur donné :

```text
1. branche d'état canonique / spectrale résolue ;
2. la porte d'identifiabilité statique/dynamique requise permet l'étude temporelle ;
3. les objets d'événement requis par l'estimateur sont résolus numériquement/
   scientifiquement sous le protocole d'événement ;
4. NUMERICAL_ZERO_AND_SYMMETRY_CONTROL_STATUS = PASS ;
5. classe numérique de Delta1 = ROBUST_NONZERO ;
6. aucun échec applicable d'oracle exact obligatoire / de pipeline ;
7. aucun INVALID_BY_CONSTRUCTION ;
8. pour une revendication d'ordre indépendant de l'estimateur :
   statut confirmatoire positif de cohérence d'estimateur requis ;
9. pour une revendication de stabilité au cutoff :
   statut positif approprié déjà gelé de troncature/référence requis.
```

Les statuts de chemin/récurrence DOIVENT toujours être publiés pour les dépendances d'événement, mais ils ne mettent PAS leur veto sur ce rang RELATIONNEL au seul motif que l'interprétation d'arrivée n'est pas disponible.

Cependant, si le chemin/la récurrence n'établissent pas la sémantique d'arrivée propre, la formulation de la revendication NE DOIT PAS utiliser :

```text
arrivée / arrival
arrivée propre / clean arrival
propagation
vitesse de propagation
vitesse de propagation effective
front
trajet causal
```

ni formulation équivalente.

Formulation autorisée, explicitement relationnelle, par exemple : « contraste relationnel non nul résolu de sondes de temps de réponse préenregistrées ».

Normatif :

```text
DELTA1_RELATIONAL_CONTRAST_PATH_RECURRENCE_ROLE = MANDATORY_PUBLICATION_NOT_ARRIVAL_VETO
DELTA1_RELATIONAL_CONTRAST_ARRIVAL_LANGUAGE      = FORBIDDEN
```

### 4.2 `DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY`

```text
DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY = CLAIM_RANK_STRONGER_OPTIONAL
```

Exige TOUTES les exigences du rang relationnel PLUS :

Pour chaque dépendance d'événement requise entrant dans l'estimateur `Delta1` :

```text
TIME_EVENT_VALID = TRUE
```

où, déjà gelé :

```text
TIME_EVENT_VALID = PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE AND RECURRENCE_CONTROL_ACCEPTABLE
```

(définitions : `path-purity-control.md`, `recurrence-control.md`).

Pour un `Delta1` de croissance construit à partir de : référence `O1A`, état `O1A`, référence `O1B`, état `O1B` — les quatre dépendances d'événement requises doivent satisfaire `TIME_EVENT_VALID`.

Pour un `Delta1` de seuil à `eta` : la même exigence s'applique aux quatre dépendances d'événement à ce `eta`.

Toute dépendance d'arrivée `d=3` requise avec `ARRIVAL_INTERPRETATION = EXCLUDED` reste dominante et empêche ce rang plus fort.

Ce rang plus fort permet uniquement l'interprétation d'arrivée propre déjà supportée. Il n'établit TOUJOURS PAS :

- une vitesse locale fondamentale ;
- une vitesse causale relativiste ;
- une métrique ;
- une émergence de continuum ;
- un `C` fondamental.

Normatif :

```text
DELTA1_ARRIVAL_INTERPRETED_REQUIREMENT = ALL_REQUIRED_EVENT_DEPENDENCIES_TIME_EVENT_VALID
```

---

## 5. Revendication d'existence de la campagne primaire

La revendication d'existence primaire de Toy 0B utilise le rang RELATIONNEL, pas le rang d'arrivée plus fort.

```text
PRIMARY_RELATIONAL_NONUNIFORMITY_DETECTED_ON_PREREGISTERED_MAIN
```

ssi au moins un point MAIN positif nominal à `delta` fini a :

```text
DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY avec Delta1 = ROBUST_NONZERO.
```

Cela supporte uniquement :

```text
EXISTS_AT_LEAST_ONE_PREREGISTERED_MAIN_POINT_WITH_CONFIRMATORY_NONZERO_RELATIONAL_DELTA1
```

Cela n'implique PAS :

- `Delta1` non nul partout ;
- monotonie ;
- signe uniforme ;
- anisotropie universelle ;
- comportement de continuum ;
- arrivée propre, sauf si le rang de revendication plus fort passe séparément.

Si au moins un point passe également le rang plus fort, un énoncé séparé peut être fait :

```text
EXISTS_AT_LEAST_ONE_PREREGISTERED_MAIN_POINT_WITH_ARRIVAL_INTERPRETED_NONZERO_DELTA1
```

Les deux énoncés ne sont JAMAIS fusionnés.

---

## 6. Formulation en l'absence de signal

Si aucun point MAIN n'a de `Delta1` relationnel confirmatoire `ROBUST_NONZERO` :

publier :

```text
NO_CONFIRMATORY_NONZERO_RELATIONAL_DELTA1_DETECTED_ON_PREREGISTERED_MAIN
```

JAMAIS :

```text
DELTA1_IS_ZERO_ON_MAIN
MODEL_PROVES_NO_NONUNIFORMITY
```

Publication obligatoire :

```text
MODEL0B_MAIN_POINT_CLAIM_STATUS_VECTOR = MANDATORY_PUBLICATION
```

Publier chaque point MAIN préenregistré, y compris : robuste non nul ; compatible zéro ; sensible au contrôle ; numériquement inconclusif ; veto local ; invalide/échec le cas échéant.

Ceci maintient distincts :
- une absence résolue compatible-zéro de signal détecté ;
- une limitation de couverture/dépendance ;
- un échec de pipeline/oracle.

---

## 7. Revendication de cohérence d'estimateur

Préserver exactement la sémantique déjà gelée de `estimator-coherence-control.md`.

Une formulation d'ordre indépendant de l'estimateur exige le statut existant `ROBUST_COHERENT_ORDERING`/`ROBUST_COHERENT` sur la famille effective d'estimateurs préenregistrés admissible.

Si la cohérence d'estimateur est `CONTROL_SENSITIVE` ou limitée en couverture/inconclusive :

le `Delta1` spécifique à l'estimateur peut toujours être publié s'il est par ailleurs éligible,

mais :

```text
ESTIMATOR_INDEPENDENT_ORDERING_CLAIM = FORBIDDEN
```

Ne PAS inférer une égalité de magnitude.

---

## 8. Revendication de troncature

Préserver exactement la sémantique de troncature déjà gelée (`truncation-comparison-control.md`).

Aucun nouveau critère de troncature.

Un statut robuste-stable de référence + stress MAIN est requis pour la formulation de stabilité de cutoff correspondante. Le stress extérieur reste rapporté séparément.

Ne jamais écrire :

```text
UNIFORM_CUTOFF_CONVERGENCE_PROVEN_ON_FULL_MAIN_DOMAIN
```

Le domaine MAIN non échantillonné reste :

```text
NOT_CERTIFIED_BY_STRESS_SUBSET
```

---

## 9. Court temps / SOFT-LOOP

Aucune refonte.

Court temps :
- un exposant certifié exige toujours que tous les ordres autorisés inférieurs soient nuls par certificat structurel/exact et que le coefficient courant soit `ROBUST_NONZERO` ;
- un zéro numérique ne certifie jamais un saut d'ordre ;
- `Delta1_short` reste un oracle/diagnostic, pas un troisième estimateur de propagation.

SOFT-LOOP :
- indépendant de MAIN ;
- la porte statique à `Lambda=2` et `Lambda=3` doit avoir `SOFT_LOOP_STATIC_SUPPORTED` ordinaire pour la revendication de mécanisme à deux niveaux ;
- la stabilité de dérivée et l'imparité explicite `+/-h` restent requises ;
- Richardson reste secondaire.

---

## 10. Portée confirmatoire `Xi1` (BL3)

```text
XI1_CONFIRMATORY_SCOPE = SOFT_LOOP_ONLY
```

La campagne MAIN à `delta` fini ne doit JAMAIS servir à estimer `Xi1` (déjà énoncé dans `specification.md` §14).

```text
H_DELTA_VALUES                = NOT_INSTANTIATED_IN_PREREGISTERED_CAMPAIGN
ABSOLUTE_STEP_FAMILY_H_DELTA  = GENERIC_FUTURE_EXTENSION_NOT_USED_FOR_MODEL0B_CONFIRMATORY
```

La famille absolue générique `H_delta` (`derivative-control.md` §3) peut rester documentée comme extension méthodologique future. Elle NE DOIT PAS supporter de revendication confirmatoire `Xi1` de Toy 0B. Aucune nouvelle valeur `h` n'est sélectionnée. Aucune campagne `Xi1` MAIN n'est créée.

---

## 11. Support spectral groupé — disposition finale (backlog non bloquant)

Préserver exactement :

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
```

```text
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_CURRENT_CONFIRMATORY_DEPENDENCY = NONE
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
```

Justification explicite et bornée :

- les poids groupés du projecteur spectral sont déjà la représentation numérique invariante (`exact-spectral-response.md` §2) ;
- la correspondance mappée de cluster (nombre/multiplicité/identité) est déjà requise par `numerical-zero-symmetry-control.md` §F13 avant toute comparaison de poids signés ;
- `EDGE_SPECTRAL_SUM_RULE_NUMERICAL_ORACLE` (famille K) donne un contrôle absolu indépendant de bout en bout sur un ensemble fixe à six points ;
- `MOMENT_OPERATOR_SPECTRAL_CROSSCHECK` (famille L) donne une voie indépendante opérateur/spectrale sur son sous-ensemble fixe de relations/ordres ;
- ces contrôles NE dérivent PAS et NE prouvent PAS un patron analytique complet de support des fréquences groupées actives ;
- le futur théorème de support groupé reste donc utile mais n'est la dépendance d'AUCUNE revendication confirmatoire actuelle.

Ne PAS fermer cet oracle. Ne PAS dériver de nouvelle règle de sélection. Ne PAS le déclarer définitivement inutile.

---

## 12. Coupe-feu échec / non-confirmation / absence de signal

Trois sémantiques distinctes de premier niveau :

**A. `PIPELINE_OR_MANDATORY_ORACLE_FAILURE`**
- incohérence structurelle ;
- échec d'oracle exact obligatoire ;
- contradiction résolue de théorème/pipeline.

**B. `SCIENTIFIC_NONCONFIRMATION`**
- résultat sensible au contrôle ;
- inconclusion numérique ;
- veto d'interprétation locale ;
- limitation de couverture ;
- signal compatible-zéro.

**C. `NO_CONFIRMATORY_NONZERO_SIGNAL_DETECTED`**
- aucun point MAIN échantillonné n'atteint la revendication relationnelle confirmatoire robuste-non-nulle requise.

B/C NE DOIVENT JAMAIS être qualifiés de :
```text
échec d'implémentation
falsification de théorème
```

A NE DOIT JAMAIS être adouci en :
```text
limitation numérique
```

---

## 13. Disposition finale de préparation au gel

Après intégration réussie et vérification indépendante du diff distant :

```text
MODEL0B_CLOSURE_REVIEW         = PASS
MODEL0B_FINAL_ACCEPTANCE_RULES = VALIDATED_FOR_FREEZE
MODEL0B_FINAL_ACCEPTANCE_MODE  = CLAIM_SCOPED_FAIL_CLOSED_DEPENDENCY_CLOSURE
MODEL0B_FREEZE_READINESS       = READY_FOR_LIONEL_DECISION
MODEL0B_STATUS                 = NOT_FROZEN_PENDING_LIONEL_DECISION
IMPLEMENTATION_0B               = NOT_AUTHORIZED

CLOSED_MAJOR_CONTROLS = 21
OPEN_MAJOR_CONTROLS   = 0

GROUPED_SPECTRAL_SUPPORT_ORACLE = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE = NO
```

Important : `READY_FOR_LIONEL_DECISION` est une préparation documentaire/protocolaire uniquement. Cela ne signifie PAS que la campagne confirmatoire a été exécutée ou qu'elle a réussi. `MODEL0B_STATUS = NOT_FROZEN_PENDING_LIONEL_DECISION` reste le statut courant du modèle tant que Lionel ORCIL n'a pas explicitement prononcé le gel dans `docs/governance/current-task.md`.

---

## 14. Statut

```text
MODEL0B_FINAL_ACCEPTANCE_RULES                 = VALIDATED_FOR_FREEZE
MODEL0B_FINAL_ACCEPTANCE_MODE                  = CLAIM_SCOPED_FAIL_CLOSED_DEPENDENCY_CLOSURE
MODEL0B_ACCEPTANCE_AVERAGING                   = FORBIDDEN
MODEL0B_ACCEPTANCE_MAJORITY_VOTE               = FORBIDDEN
MODEL0B_ACCEPTANCE_DIAGNOSTIC_AS_CONFIRMATORY  = FORBIDDEN
MODEL0B_PIPELINE_FAILURE_AS_NUMERICAL_LIMITATION = FORBIDDEN
DELTA1_RELATIONAL_CONTRAST_CONFIRMATORY        = CLAIM_RANK_PRIMARY
DELTA1_ARRIVAL_INTERPRETED_CONFIRMATORY        = CLAIM_RANK_STRONGER_OPTIONAL
DELTA1_RELATIONAL_CONTRAST_PATH_RECURRENCE_ROLE = MANDATORY_PUBLICATION_NOT_ARRIVAL_VETO
DELTA1_RELATIONAL_CONTRAST_ARRIVAL_LANGUAGE     = FORBIDDEN
DELTA1_ARRIVAL_INTERPRETED_REQUIREMENT          = ALL_REQUIRED_EVENT_DEPENDENCIES_TIME_EVENT_VALID
MODEL0B_MAIN_POINT_CLAIM_STATUS_VECTOR          = MANDATORY_PUBLICATION
ESTIMATOR_INDEPENDENT_ORDERING_CLAIM_UNSUPPORTED = FORBIDDEN
XI1_CONFIRMATORY_SCOPE                          = SOFT_LOOP_ONLY
H_DELTA_VALUES                                  = NOT_INSTANTIATED_IN_PREREGISTERED_CAMPAIGN
ABSOLUTE_STEP_FAMILY_H_DELTA                    = GENERIC_FUTURE_EXTENSION_NOT_USED_FOR_MODEL0B_CONFIRMATORY
GROUPED_SPECTRAL_SUPPORT_ORACLE                 = OPEN_PENDING_SYMMETRY_DERIVATION
GROUPED_SPECTRAL_SUPPORT_ORACLE_FREEZE_ROLE     = NON_BLOCKING_BACKLOG
GROUPED_SPECTRAL_SUPPORT_ORACLE_CURRENT_CONFIRMATORY_DEPENDENCY = NONE
GROUPED_SPECTRAL_SUPPORT_ORACLE_REQUIRED_FOR_MODEL0B_FREEZE     = NO
MODEL0B_CLOSURE_REVIEW                          = PASS
MODEL0B_FREEZE_READINESS                        = READY_FOR_LIONEL_DECISION
MODEL0B_STATUS                                  = NOT_FROZEN_PENDING_LIONEL_DECISION
IMPLEMENTATION_0B                               = NOT_AUTHORIZED
```
