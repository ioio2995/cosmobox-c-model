# Toy Model 0B — contrôle numérique de comparaison Lambda=2 -> 3

Statut : **validé pour gel — support méthodologique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Supports liés : `truncation-design-qualification.md`, `parameter-campaign-structure.md`, `validation-plan.md`, `derivative-error-budget.md`, `temporal-event-solver.md`

Ce document est la source normative détaillée du protocole complet de comparaison `Lambda=2 -> 3` sur le sous-ensemble de stress de troncature déjà fixe (`truncation-design-qualification.md` §8). Il ferme UNIQUEMENT `TRUNCATION_COMPARISON_TOLERANCES`.

## 0. Rôle épistémique

```text
TRUNCATION_COMPARISON_TOLERANCES = VALIDATED_FOR_FREEZE
```

Ceci ferme COMMENT `Lambda=2` et `Lambda=3` sont comparés sur la portée de stress/référence déjà gelée (`TRUNCATION_STRESS_POINT_SUBSET`, `TRUNCATION_REFERENCE_ANCHOR`). Ceci NE prouve PAS la convergence uniforme sur les points MAIN non échantillonnés. Ceci NE ferme PAS :

```text
ESTIMATOR_COHERENCE_CRITERION
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

## 1. Famille de tolérance

Famille normative :

```text
TRUNCATION_TOLERANCE_VALUES = {0.01,0.02,0.05}
```

équivalent :

```text
{1/100,1/50,1/20}

TRUNCATION_TOLERANCE_STRICT = 0.01
TRUNCATION_TOLERANCE_MID = 0.02
TRUNCATION_TOLERANCE_PERMISSIVE = 0.05

TRUNCATION_TOLERANCE_GRID_TYPE = THREE_POINT_OPERATIONAL_SENSITIVITY_FAMILY
TRUNCATION_TOLERANCE_DIMENSIONING = DESIGN_QUALIFICATION_INFORMED_PREREGISTRATION
```

Ces valeurs sont :

- des valeurs opérationnelles préenregistrées de sensibilité au cutoff ;
- PAS des bornes d'erreur théoriques ;
- PAS des tolérances de virgule flottante ;
- PAS des intervalles de confiance.

La `DESIGN_QUALIFICATION` d'avant gel a informé leur dimensionnement. Un futur `PASS` est donc un résultat de test préenregistré, pas une découverte indépendante de la tolérance.

## 2. Marge numérique scalaire générique

Pour une métrique scalaire de cutoff non négative `d_Q`, calculée aux précisions acceptées :

```math
d_Q^{(p)},\qquad d_Q^{(2p)}.
```

Définir :

```math
e_{Q,p2p}=\left|d_Q^{(2p)}-d_Q^{(p)}\right|.
```

Si la quantité dispose déjà d'un budget numérique propagé `e_{Q,prop}`, utiliser :

```math
e_Q=\max\left(e_{Q,p2p},e_{Q,prop}\right).
```

Alors :

```math
L_Q=\max\left(0,d_Q^{(2p)}-e_Q\right),
\qquad
U_Q=d_Q^{(2p)}+e_Q.
```

Ce sont des bornes de contrôle opérationnelles issues de `p/2p` et des incertitudes propagées déjà gelées ; ce ne sont pas des intervalles probabilistes.

La qualification de précision sous-jacente doit réussir. Sinon :

```text
TRUNCATION_SCALAR_STATUS = NUMERICALLY_INCONCLUSIVE
```

Normatif :

```text
TRUNCATION_NUMERICAL_MARGIN = MAX_P2P_AND_EXISTING_PROPAGATED_ERROR
```

## 3. Profil de tolérance scalaire générique

Pour chaque `tau` dans `TRUNCATION_TOLERANCE_VALUES` :

```text
U_Q <= tau  -> CUTOFF_TAU_PASS
L_Q > tau   -> CUTOFF_TAU_FAIL
sinon       -> CUTOFF_TAU_INCONCLUSIVE
```

Résumé de famille :

```text
si U_Q <= 0.01 :        ROBUST_STABLE
sinon si L_Q > 0.05 :    ROBUST_UNSTABLE
sinon :                  CONTROL_SENSITIVE
```

sous réserve que la résolution numérique soit disponible.

`tau=0.02` est un diagnostic de publication/sensibilité obligatoire uniquement.

Aucun choix de tolérance a posteriori n'est autorisé.

## 4. Couche catégorielle

Comparer les branches scientifiques catégorielles déjà gelées et résolues, selon leur applicabilité :

```text
- mode de construction de l'état canonique ;
- d_GS / catégorie de dégénérescence exacte ;
- applicabilité/statut terminal d'événement ;
- classe de ligne de base de chemin ;
- PATH_CONTROL_STATUS ;
- prédicat de relation de récurrence / RECURRENCE_STATUS ;
- statut de support à temps court ;
- toute autre catégorie terminale déjà gelée changeant le sens scientifique.
```

Règles :

```text
même catégorie résolue        -> CUTOFF_CATEGORICAL_COMPATIBLE
catégorie résolue différente  -> CUTOFF_CATEGORICAL_MISMATCH
catégorie non résolue, sans règle plus spécifique applicable
                               -> CUTOFF_CATEGORICAL_NUMERICALLY_INCONCLUSIVE
```

Un accord catégoriel de cutoff ne rend PAS acceptable un statut scientifique localement inacceptable.

Exemple : `ROBUST_CONTAMINATED` aux deux cutoffs peut être cohérent au cutoff mais reste scientifiquement vetoté pour une interprétation d'arrivée propre.

Aucun verdict de troncature ne rachète un veto scientifique local.

L'admissibilité `eta` de seuil utilise la règle spéciale PRE-INTERSECTION ci-dessous (§16-20), pas une comparaison de `E_eta^common(Q)` à lui-même.

### 4.1 Dépendance : cohérence entre estimateurs de propagation

Aux points de stress `Lambda=3` sélectionnés, lorsqu'une quantité scientifique requise s'appuie sur l'interprétation par estimateur de propagation à `delta` fini, évaluer le statut catégoriel :

```text
ESTIMATOR_COHERENCE_POINT
```

en utilisant `estimator-coherence-control.md`. Ce statut fait partie de la fermeture de dépendance scientifique complète requise (§4, catégorie « toute autre catégorie terminale déjà gelée changeant le sens scientifique »).

Routage au sein du présent protocole de cutoff :

```text
- ROBUST_COHERENT_ORDERING reste comparable au cutoff, sous la même
  provisionalité finale zéro/symétrie que le reste de ce protocole ;
- ESTIMATOR_ORDERING_CONFLICT reste une condition scientifique locale
  CONTROL_SENSITIVE/non confirmatoire ; la stabilité de cutoff ne la rachète
  jamais ;
- ESTIMATOR_ELIGIBILITY_ASYMMETRY, NONCONFIRMATORY_COMMON_LOCAL_VETO et les
  limitations de couverture sans estimateur de seuil restent des
  dépendances locales non confirmatoires ;
- NUMERICALLY_INCONCLUSIVE reste fail-closed.
```

Ceci ne crée aucune nouvelle tolérance de troncature et n'agrège jamais le statut de cohérence dans une métrique scalaire.

## 5. Métrique d'état

Plongement naturel :

```math
\iota:\mathcal H_{phys}^{(2)}\to\mathcal H_{phys}^{(3)}.
```

Plongement de l'état canonique :

```math
\rho_{2,emb}=\iota\rho_2\iota^\dagger.
```

Distance de trace :

```math
D_\rho=\frac12\left\|\rho_3-\rho_{2,emb}\right\|_1.
```

Étendue :

```text
0 <= D_rho <= 1
```

Normatif :

```text
TRUNCATION_STATE_METRIC = TRACE_DISTANCE_UNDER_NATURAL_EMBEDDING
```

Budget numérique d'état :

```math
e_{\rho,state}=D\!\left(\rho_2^{(2p)},\rho_2^{(p)}\right)+D\!\left(\rho_3^{(2p)},\rho_3^{(p)}\right)
```

avec plongement `Lambda=2` cohérent. Utiliser :

```math
e_\rho=\max\left(\left|D_\rho^{(2p)}-D_\rho^{(p)}\right|,e_{\rho,state}\right).
```

Appliquer la famille générique de cutoff (§2-3).

Cette métrique reste valide aussi pour des mélanges canoniques uniformes sur un sous-espace fondamental dégénéré.

## 6. Énergie de l'état fondamental

L'écart d'énergie fondamentale entre cutoffs est `DIAGNOSTIC_ONLY`.

Normatif :

```text
TRUNCATION_EGS_CUTOFF_ROLE = DIAGNOSTIC_ONLY
GS_ENERGY_CUTOFF_DIFFERENCE_AS_SUFFICIENT_CERTIFICATE = REJECTED
```

Publier brut :

```math
\Delta E_{GS}=E_{GS}^{(3)}-E_{GS}^{(2)}.
```

Diagnostic normalisé optionnel invariant par décalage :

```math
\bar E_\Lambda=\frac{Tr(H_\Lambda)}{d_\Lambda},
\qquad
H_{s,\Lambda}=\max\left(J,\left\|H_\Lambda-\bar E_\Lambda I\right\|_2\right)
```

où `||.||_2` est explicitement la norme spectrale d'opérateur.

```math
d_E=\frac{\left|E_{GS}^{(3)}-E_{GS}^{(2)}\right|}{\max(H_{s,2},H_{s,3})}.
```

`d_E` n'est PAS une porte scalaire obligatoire.

## 7. Gap

Lorsque les deux gaps sont positifs et résolus :

```math
d_{gap}=\left|\log\left(\frac{gap_3}{gap_2}\right)\right|.
```

Utiliser `p/2p` et le budget de précision propagé (§2). Appliquer la famille de tolérance générique (§3).

Si un zéro/dégénérescence structurel rend la métrique log positive non applicable, utiliser la branche catégorielle (§4).

Si une décision zéro/non-zéro requise n'est pas encore résolue sous la future politique zéro/symétrie :

```text
NUMERICALLY_INCONCLUSIVE
```

Ne pas fermer `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES`.

## 8. Temps d'événements

Pour la MÊME définition physique d'événement aux deux cutoffs :

```math
d_T=\left|\log\left(\frac{T_3}{T_2}\right)\right|.
```

Chaque événement dispose déjà, dans la coordonnée `u_e` de `temporal-event-solver.md`, de :

```math
r_T=\frac{e_u}{u}<1,
\qquad
L(r)=-\log(1-r)
```

(définition déjà existante, `derivative-error-budget.md` §3.1). Budget propagé croisé aux cutoffs :

```math
e_{T,prop}=L(r_{T,2})+L(r_{T,3}).
```

Utiliser :

```math
e_T=\max\left(\left|d_T^{(2p)}-d_T^{(p)}\right|,e_{T,prop}\right).
```

Appliquer la famille de tolérance générique.

Types d'événements requis selon applicabilité :

```text
T_peak
T_grow
T_thr(eta)
T_down(eta)
```

Les événements de seuil utilisent le protocole `eta` défini en §16-20.

## 9. C_eff

`C_eff` est positif. Utiliser :

```math
d_{Ceff}=\left|\log\left(\frac{C_{eff}^{(3)}}{C_{eff}^{(2)}}\right)\right|.
```

Propager les budgets d'erreur log-temporels déjà existants depuis l'événement de référence et l'événement d'état, aux deux cutoffs. Utiliser le maximum avec l'écart `p/2p` de la métrique. Appliquer la famille de tolérance générique.

L'ancre de référence `Lambda=3` (`TRUNCATION_REFERENCE_ANCHOR = (1,0,0)`) est obligatoire.

Pour l'interprétation : une dérive log-ratio `d=0.05` correspond à :

```math
e^{0.05}-1\approx5.13\%
```

de changement multiplicatif du ratio positif sous-jacent. Ne pas écrire « le logarithme a changé de 5% ».

## 10. Delta1 — métrique à double échelle

`Delta1` est le contraste logarithmique signé primaire. Une seule métrique absolue est insuffisante. Une seule métrique relative est également insuffisante. Pour les comparaisons du signal primaire à `delta` fini, utiliser les DEUX.

A. Métrique absolue native-log :

```math
d_{abs}=\left|\Delta_1^{(3)}-\Delta_1^{(2)}\right|.
```

Normatif :

```text
TRUNCATION_DELTA1_ABSOLUTE_METRIC = ABSOLUTE_NATIVE_LOG_COORDINATE_DIFFERENCE
```

B. Métrique relative symétrique :

```math
d_{rel}=\frac{2\left|\Delta_1^{(3)}-\Delta_1^{(2)}\right|}{\left|\Delta_1^{(3)}\right|+\left|\Delta_1^{(2)}\right|}.
```

Étendue :

```text
0 <= d_rel <= 2
```

Normatif :

```text
TRUNCATION_DELTA1_RELATIVE_METRIC = SYMMETRIC_RELATIVE_DIFFERENCE
TRUNCATION_DELTA1_DUAL_METRIC = REQUIRED_FOR_FINITE_DELTA_PRIMARY_SIGNAL
```

## 11. Budget numérique explicite par cutoff pour Delta1

Ne PAS se référer à un « `E_Delta1_existing_prop` » générique inexistant.

Pour un estimateur `Delta1` à un cutoff `Lambda` :

```math
\Delta_1=\log C_A-\log C_B,
\qquad
C_A=\frac{T_A^{ref}}{T_A^{state}},
\qquad
C_B=\frac{T_B^{ref}}{T_B^{state}}.
```

En un seul point `Delta1`, les références NE s'annulent PAS. Définir explicitement :

```math
E_{\Delta_1,prop}^{(\Lambda)}
=L\!\left(r_{A,ref}^{\Lambda}\right)+L\!\left(r_{A,state}^{\Lambda}\right)
+L\!\left(r_{B,ref}^{\Lambda}\right)+L\!\left(r_{B,state}^{\Lambda}\right).
```

Pour les estimateurs de seuil, les quatre termes se réfèrent au MÊME `eta` comparé. Alors :

```math
e_\Lambda=\max\left(E_{\Delta_1,prop}^{(\Lambda)},\left|\Delta_{1,\Lambda}^{(2p)}-\Delta_{1,\Lambda}^{(p)}\right|\right).
```

Ceci est distinct de `derivative-error-budget.md` §3.1, où les termes de référence s'annulent uniquement dans le numérateur central `Delta1(+h)-Delta1(-h)`.

## 12. Bornes d'intervalle pour Delta1

Soit `Delta_L = Delta1_L^(2p)`. Bornes d'amplitude :

```math
m_L=\max\left(0,\left|\Delta_L\right|-e_L\right),
\qquad
M_L=\left|\Delta_L\right|+e_L.
```

Bornes de différence :

```math
m_{diff}=\max\left(0,\left|\Delta_3-\Delta_2\right|-(e_3+e_2)\right),
\qquad
M_{diff}=\left|\Delta_3-\Delta_2\right|+(e_3+e_2).
```

Bornes de la métrique absolue :

```text
L_abs = m_diff
U_abs = M_diff
```

Pour la métrique relative symétrique :

```text
S_min = m_2 + m_3
S_max = M_2 + M_3
```

Si `S_min > 0` :

```math
L_{rel}=\frac{2\,m_{diff}}{S_{max}},
\qquad
U_{rel}=\min\left(2,\frac{2\,M_{diff}}{S_{min}}\right).
```

Ces bornes sont conservatrices.

Si `S_min = 0` :

```text
TRUNCATION_DELTA1_RELATIVE_STATUS = NUMERICALLY_INCONCLUSIVE
```

Ceci ne déclare PAS `Delta1` numériquement nul. Aucun nouveau seuil de zéro n'est introduit.

## 13. Routage composite Delta1 — correction finale

Classer les métriques absolue et relative séparément avec la MÊME famille `{0.01,0.02,0.05}`.

Routage composite à `delta` fini :

```text
1. si l'une des deux métriques est NUMERICALLY_INCONCLUSIVE :
   TRUNCATION_DELTA1_STATUS = NUMERICALLY_INCONCLUSIVE

2. sinon si les DEUX métriques sont ROBUST_UNSTABLE :
   TRUNCATION_DELTA1_STATUS = ROBUST_UNSTABLE

3. sinon si les DEUX métriques sont ROBUST_STABLE :
   TRUNCATION_DELTA1_STATUS = ROBUST_STABLE

4. sinon :
   TRUNCATION_DELTA1_STATUS = CONTROL_SENSITIVE
```

Normatif :

```text
TRUNCATION_DELTA1_COMPOSITE_RULE = DUAL_SCALE_CONJUNCTIVE_STABILITY_AND_INSTABILITY
```

Conséquences :

```text
+0.004 -> -0.004 : absolu stable, relatif instable
    => CONTROL_SENSITIVE, jamais ROBUST_STABLE.

1e-6 -> 1.2e-6 : absolu stable, relatif instable
    => CONTROL_SENSITIVE, jamais faux ROBUST_UNSTABLE.
```

Une dérive réellement matérielle doit être grande sur les DEUX échelles (native-log absolue et relative-au-signal) pour devenir `ROBUST_UNSTABLE`. `ROBUST_STABLE` exige que les deux métriques soient stables.

## 14. Delta1 au zéro structurel

À `delta=0` :

```math
\Delta_1(g,\mu,0)=0
```

est un oracle structurel exact à chaque cutoff. Les deux métriques du signal fini sont :

```text
TRUNCATION_DELTA1_ABSOLUTE_METRIC_AT_STRUCTURAL_ZERO = NOT_APPLICABLE_STRUCTURAL_ZERO
TRUNCATION_DELTA1_RELATIVE_METRIC_AT_STRUCTURAL_ZERO = NOT_APPLICABLE_STRUCTURAL_ZERO
```

Ne pas laisser une comparaison de résidu absolu à `delta=0` produire `ROBUST_STABLE` par construction.

La vérification numérique de l'oracle de zéro structurel à chaque cutoff reste conditionnée à :

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```

Un verdict confirmatoire final de cutoff pour une dépendance `delta=0` ne peut donc pas utiliser l'oracle de zéro `Delta1` comme résolu tant que ce contrôle ultérieur n'est pas fermé.

## 15. Delta1_short

La règle catégorielle de cutoff à temps court déjà gelée reste obligatoire :

```text
CUTOFF_STABLE_SHORT_TIME_CONVERGENCE
```

Pour `C_short` positif :

```math
d_{Cshort}=\left|\log\left(\frac{C_{short}^{(3)}}{C_{short}^{(2)}}\right)\right|.
```

Si une quantité continue signée `Delta1_short` est elle-même une quantité publiée requise comparée au cutoff, appliquer le MÊME traitement dual absolu + relatif-symétrique et le même routage que `Delta1` (§10-13).

Normatif :

```text
TRUNCATION_DELTA1_SHORT_METRIC = SAME_DUAL_METRIC_AS_DELTA1_WHEN_REQUIRED
```

La règle catégorielle par paire à temps court reste primaire et ne peut pas être rachetée par une annulation dans `Delta1_short`.

## 16. Admissibilité eta — pré-intersection

Rejeter comme test de cutoff : « appartenance à `E_eta^common(Q)` ». C'est vrai par construction après intersection.

Pour toute quantité de seuil publiée requise `Q` : AVANT toute intersection commune, comparer les signatures d'admissibilité de fermeture de dépendance complète spécifiques à chaque cutoff.

Soit `D(Q)` la fermeture de dépendance déjà gelée. Les membres appariés utilisent la correspondance canonique :

```text
(référence/état) x (orbite O1A/O1B) x (relation pq requise / membre d'événement)
```

selon ce que `Q` requiert. Les objets harmoniques propres à `Lambda=3`, `k=5,6`, restent `EXTENDED_DIAGNOSTIC` et ne sont PAS insérés dans les signatures `eta` appariées.

Définir :

```text
A_Lambda(eta,Q) = tuple des statuts d'admissibilité terminale eta/événement
                  déjà existants pour chaque membre requis apparié de D(Q)
                  au cutoff Lambda
```

Normatif :

```text
TRUNCATION_ETA_ADMISSIBILITY_COMPARISON_STAGE = BEFORE_COMMON_INTERSECTION
TRUNCATION_ETA_ADMISSIBILITY_OBJECT = COMPLETE_DEPENDENCY_CLOSURE_STATUS_SIGNATURE
TRUNCATION_ETA_MATCHED_MEMBER_RULE = CANONICAL_REFERENCE_STATE_ORBIT_RELATION_CORRESPONDENCE
```

## 17. Portée de pré-comparaison eta

La famille évaluée pour `Q` est : tous les niveaux `eta` préenregistrés dont l'admissibilité doit être évaluée pour au moins un `Q` publié requis à l'un ou l'autre cutoff.

Équivalent : utiliser l'union des niveaux `eta` candidats de pré-intersection requis à travers les deux cutoffs, AVANT filtrage commun.

Les niveaux exclus de tout `Q` publié requis aux deux cutoffs sont `DIAGNOSTIC_ONLY` et n'affectent pas le verdict de cutoff.

Normatif :

```text
TRUNCATION_ETA_PREINTERSECTION_SCOPE = UNION_OF_REQUIRED_PREREGISTERED_CANDIDATE_LEVELS_ACROSS_CUTOFFS
```

## 18. Routage par paire eta — correction finale

Pour chaque `eta` dans la portée de pré-intersection, comparer `A_2(eta,Q)` vs `A_3(eta,Q)` :

```text
A. signatures IDENTIQUES, y compris le même statut terminal non résolu
   pour la même raison aux deux cutoffs :
   CUTOFF_ETA_ADMISSIBILITY_COMPATIBLE

   Une raison non résolue identique symétrique est cutoff-compatible.
   Elle reste localement non confirmatoire exactement comme défini par le
   protocole eta.

B. un cutoff résolu pendant que l'autre est non résolu :
   CUTOFF_ETA_ADMISSIBILITY_NUMERICALLY_INCONCLUSIVE

C. les deux résolus mais signatures différentes :
   CUTOFF_ETA_ADMISSIBILITY_MISMATCH -> CONTROL_SENSITIVE

D. les deux non résolus mais avec des raisons/motifs terminaux DIFFÉRENTS :
   CUTOFF_ETA_ADMISSIBILITY_UNRESOLVED_PATTERN_MISMATCH -> CONTROL_SENSITIVE
```

Aucun moyennage.

## 19. Routage de famille eta

Sur toute la portée de pré-intersection pour `Q` requis :

```text
si une paire quelconque est CUTOFF_ETA_ADMISSIBILITY_NUMERICALLY_INCONCLUSIVE :
    TRUNCATION_ETA_DOMAIN_STATUS = NUMERICALLY_INCONCLUSIVE

sinon si une paire quelconque est :
    - CUTOFF_ETA_ADMISSIBILITY_MISMATCH ; ou
    - CUTOFF_ETA_ADMISSIBILITY_UNRESOLVED_PATTERN_MISMATCH :
    TRUNCATION_ETA_DOMAIN_STATUS = CONTROL_SENSITIVE

sinon :
    TRUNCATION_ETA_DOMAIN_STATUS = ROBUST_STABLE
```

Une fois ce profil publié, construire le déjà gelé `E_eta^common(Q)` ou domaine `eta` joint aux deux cutoffs. Les comparaisons continues de cutoff utilisent uniquement le domaine commun.

Le `TRUNCATION_ETA_DOMAIN_STATUS` de pré-intersection se propage néanmoins au verdict de cutoff au niveau du point et ne peut pas être effacé par l'intersection.

## 20. Eta commun vide/insuffisant

Si une quantité de seuil requise produit `NOT_APPLICABLE_NO_COMMON_ETA` pour la comparaison croisée de cutoff :

```text
TRUNCATION_THRESHOLD_CUTOFF_STATUS = NUMERICALLY_INCONCLUSIVE
```

Ceci est fail-closed mais n'est pas un `FAIL` physique.

Pour l'oracle à temps court, préserver sa règle existante plus stricte :

```text
moins de 3 niveaux communs joints
-> CUTOFF_STABLE_SHORT_TIME_CONVERGENCE = INSUFFICIENT_COMMON_RANGE
```

Aucun nouveau `eta`. Aucun rétrécissement spécifique au cutoff.

## 21. Couche de chemin

Comparaisons catégorielles, selon applicabilité :

```text
PATH_BASELINE_STATUS
PATH_CONTROL_STATUS
PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE
```

Pour `P_0` dans `[0,1]` : différence absolue à échelle naturelle + marge numérique générique (§2-3).

Pour `R_path`, chaque cutoff fournit déjà :

```text
I_R,2 = [L_R,2, U_R,2]
I_R,3 = [L_R,3, U_R,3]
```

Bornes de différence :

```math
L_{dR}=\max\left(0,\,L_{R,2}-U_{R,3},\,L_{R,3}-U_{R,2}\right),
\qquad
U_{dR}=\max\left(\left|L_{R,2}-U_{R,3}\right|,\left|U_{R,2}-L_{R,3}\right|\right).
```

Appliquer directement la famille `{0.01,0.02,0.05}` à `[L_dR,U_dR]`.

## 22. Couche de récurrence

La comparaison de cutoff est catégorielle, sous la même famille `Gamma` gelée et la même sémantique d'horizon. Comparer :

```text
- prédicat de relation d'extrémité RETURN/NO_RETURN/inconclusif ;
- profil Gamma strict/moyen/permissif ;
- RECURRENCE_STATUS ;
- catégorie variance-nulle/non-confirmatoire.
```

Aucune nouvelle norme de trajectoire continue sur `C_j(t)`.

Normatif :

```text
TRUNCATION_RECURRENCE_CUTOFF_METRIC = CATEGORICAL_CERTIFIED_DETECTOR_PROFILE_ONLY
```

Les diagnostics continus de récurrence peuvent être publiés `DIAGNOSTIC_ONLY`.

## 23. Harmoniques

Préserver :

```text
même k              = PRIMARY_CONVERGENCE_PAIRING
même j=2Lambda-k     = EDGE_RELATIVE_DIAGNOSTIC
k=5,6 propres à Lambda=3 = EXTENDED_DIAGNOSTIC
```

`PRIMARY_CONVERGENCE_PAIRING` est une règle de correspondance, pas une tolérance scalaire zéro-sûre indépendante.

Si une harmonique entre dans un `Q` scientifique dérivé REQUIS, la stabilité de cutoff est testée via la métrique de ce `Q`.

Sinon : les différences à `k` fixe sont des diagnostics obligatoires ; `j` fixe et `k=5,6` conservent leurs rôles diagnostiques existants.

Aucune nouvelle tolérance de passage à zéro spécifique aux harmoniques dans ce lot.

## 24. F_peak

Lorsque positif/résolu, publier :

```math
d_{Fpeak}=\left|\log\left(\frac{F_{peak}^{(3)}}{F_{peak}^{(2)}}\right)\right|.
```

Normatif :

```text
TRUNCATION_FPEAK_CUTOFF_ROLE = DIAGNOSTIC_ONLY
```

`F_peak` ne devient pas une porte scalaire requise indépendante. L'admissibilité différentielle de seuil est gérée par le profil `eta` de pré-intersection (§16-20).

## 25. Porte de référence

Le point de référence obligatoire `(1,0,0)` est une dépendance, pas l'un des 18 points de stress.

Évaluer ses dépendances requises d'état/spectrales/d'événement sous les mêmes règles de cutoff.

Normatif :

```text
TRUNCATION_REFERENCE_GATE = ROBUST_STABLE_REQUIRED
TRUNCATION_REFERENCE_STATUS = ROBUST_STABLE | CONTROL_SENSITIVE | ROBUST_UNSTABLE | NUMERICALLY_INCONCLUSIVE
```

L'instabilité/non-conclusion de référence ne peut pas être annulée par un `C_eff` ou un ratio `Delta1` stable en aval.

À `delta=0`, la vérification du zéro structurel `Delta1` reste en attente du contrôle zéro/symétrie, comme décrit en §14.

## 26. Agrégation au niveau point

Garder l'acceptabilité scientifique locale séparée de la stabilité de cutoff.

Pour un point de stress sélectionné :

```text
1. si une comparaison catégorielle GÉNÉRALE résolue requise ne correspond pas
   OU si un scalaire requis quelconque est ROBUST_UNSTABLE :
   TRUNCATION_POINT_STATUS = ROBUST_UNSTABLE

   Exception : le désaccord de domaine eta a son routage spécifique
   CONTROL_SENSITIVE défini en §19.

2. sinon si une dépendance/scalaire requis quelconque est
   NUMERICALLY_INCONCLUSIVE :
   TRUNCATION_POINT_STATUS = NUMERICALLY_INCONCLUSIVE

3. sinon si un scalaire ou une comparaison de domaine eta requis quelconque
   est CONTROL_SENSITIVE :
   TRUNCATION_POINT_STATUS = CONTROL_SENSITIVE

4. sinon, toutes les comparaisons requises sont cutoff-compatibles /
   ROBUST_STABLE :
   TRUNCATION_POINT_STATUS = ROBUST_STABLE
```

Aucun moyennage.

Un point peut être cutoff-stable tout en restant localement scientifiquement vetoté. La stabilité de cutoff ne rachète jamais le veto local.

## 27. Agrégation MAIN vs extérieur

Primaire :

```text
TRUNCATION_MAIN_STRESS_STATUS
```

sur les 16 points de stress MAIN.

Séparé :

```text
TRUNCATION_OUTER_STRESS_STATUS
```

sur `(1/10,0,0)` et `(1,0,9/10)`.

Ordre fail-closed :

```text
ROBUST_UNSTABLE > NUMERICALLY_INCONCLUSIVE > CONTROL_SENSITIVE > ROBUST_STABLE
```

Une revendication MAIN robuste-stable requiert :

```text
TRUNCATION_REFERENCE_STATUS = ROBUST_STABLE
ET
les 16 points de stress MAIN = ROBUST_STABLE
```

Les points extérieurs :

- ne peuvent pas racheter un problème MAIN ;
- ne mettent pas indépendamment leur veto sur une revendication stable de domaine MAIN, étant hors MAIN ;
- sont publiés séparément.

Si MAIN est robuste-stable et le stress extérieur robuste-instable, publier :

```text
MAIN_CUTOFF_STABLE_WITH_OUTER_STRESS_INSTABILITY
```

Utiliser la formule plus large :

```text
NO_CUTOFF_INSTABILITY_DETECTED_ON_PREREGISTERED_STRESS_SUBSET
```

UNIQUEMENT si les statuts MAIN et extérieur sont tous deux `ROBUST_STABLE`.

## 28. Portée de la revendication

Préserver :

```text
TRUNCATION_STRESS_CLAIM_SCOPE = PREREGISTERED_STRESS_SUPPORT_NOT_UNIFORM_THEOREM
TRUNCATION_CUTOFF_STATUS_FOR_UNSAMPLED_MAIN_POINT = NOT_CERTIFIED_BY_STRESS_SUBSET
```

Même référence + les 18 points robustes-stables ne prouve pas la convergence uniforme sur MAIN non échantillonné.

## 29. Dépendance zéro/symétrie

Ce lot NE définit PAS de tolérance flottante de zéro exact ou de symétrie exacte.

Tout oracle numérique requis dont la résolution finale dépend de cette politique reste en attente/non conclusif jusqu'à ce que :

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES
```

soit fermé.

Normatif :

```text
TRUNCATION_NEW_FLOATING_POINT_TOLERANCE = NONE
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```

## 30. Bloc de statut final

```text
TRUNCATION_COMPARISON_TOLERANCES = VALIDATED_FOR_FREEZE

TRUNCATION_TOLERANCE_VALUES = {0.01,0.02,0.05}
TRUNCATION_TOLERANCE_STRICT = 0.01
TRUNCATION_TOLERANCE_MID = 0.02
TRUNCATION_TOLERANCE_PERMISSIVE = 0.05
TRUNCATION_TOLERANCE_GRID_TYPE = THREE_POINT_OPERATIONAL_SENSITIVITY_FAMILY
TRUNCATION_TOLERANCE_DIMENSIONING = DESIGN_QUALIFICATION_INFORMED_PREREGISTRATION

TRUNCATION_POSITIVE_SCALAR_METRIC = ABS_LOG_RATIO
TRUNCATION_BOUNDED_SCALAR_METRIC = ABSOLUTE_NATURAL_SCALE_DIFFERENCE
TRUNCATION_STATE_METRIC = TRACE_DISTANCE_UNDER_NATURAL_EMBEDDING
TRUNCATION_NUMERICAL_MARGIN = MAX_P2P_AND_EXISTING_PROPAGATED_ERROR
TRUNCATION_CATEGORICAL_RULE = EXACT_RESOLVED_CATEGORY_COMPATIBILITY

TRUNCATION_DELTA1_DUAL_METRIC = REQUIRED_FOR_FINITE_DELTA_PRIMARY_SIGNAL
TRUNCATION_DELTA1_ABSOLUTE_METRIC = ABSOLUTE_NATIVE_LOG_COORDINATE_DIFFERENCE
TRUNCATION_DELTA1_RELATIVE_METRIC = SYMMETRIC_RELATIVE_DIFFERENCE
TRUNCATION_DELTA1_COMPOSITE_RULE = DUAL_SCALE_CONJUNCTIVE_STABILITY_AND_INSTABILITY
TRUNCATION_DELTA1_SHORT_METRIC = SAME_DUAL_METRIC_AS_DELTA1_WHEN_REQUIRED

TRUNCATION_ETA_ADMISSIBILITY_COMPARISON_STAGE = BEFORE_COMMON_INTERSECTION
TRUNCATION_ETA_ADMISSIBILITY_OBJECT = COMPLETE_DEPENDENCY_CLOSURE_STATUS_SIGNATURE
TRUNCATION_ETA_MATCHED_MEMBER_RULE = CANONICAL_REFERENCE_STATE_ORBIT_RELATION_CORRESPONDENCE
TRUNCATION_ETA_PREINTERSECTION_SCOPE = UNION_OF_REQUIRED_PREREGISTERED_CANDIDATE_LEVELS_ACROSS_CUTOFFS

TRUNCATION_REFERENCE_GATE = ROBUST_STABLE_REQUIRED
TRUNCATION_MAIN_AGGREGATION = POINTWISE_FAIL_CLOSED_NO_AVERAGING
TRUNCATION_OUTER_STRESS_ROLE = SEPARATE_DIAGNOSTIC_OUTSIDE_MAIN

TRUNCATION_EGS_CUTOFF_ROLE = DIAGNOSTIC_ONLY
TRUNCATION_FPEAK_CUTOFF_ROLE = DIAGNOSTIC_ONLY

TRUNCATION_NEW_FLOATING_POINT_TOLERANCE = NONE
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
```
