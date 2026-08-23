# Toy Model 0B — contrôle hystérétique de récurrence

Statut : **validé pour gel — support analytique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne la garde locale de récurrence évaluée directement avant chaque événement temporel candidat. Il remplace l'idée d'une fenêtre globale de revival.

## 1. Autocorrélation locale connectée

Pour un fond stationnaire `rho_theta`, c'est-à-dire `[rho_theta,H(theta)]=0` au point `theta` évalué :

```math
\delta n_q=n_q-Tr(rho_theta n_q)I,
```

```math
C_q(t)=
\frac{Re\,Tr[rho_theta\,\delta n_q(t)\delta n_q]}
{Tr[rho_theta(\delta n_q)^2]}.
```

Si le dénominateur est non nul, stationnarité et Cauchy-Schwarz dans le produit scalaire pondéré par `rho_theta` donnent :

```math
|C_q(t)|\le1,
\qquad
C_q(0)=1.
```

Cette borne structurelle est appliquée **séparément** en chaque point évalué — référence, chaque état, `+delta`, `-delta`, chaque `h_k`, chaque cutoff — en utilisant le `rho_theta` stationnaire propre à ce point.

Normatif :

```text
RECURRENCE_AUTOCORRELATION_RANGE        = STRUCTURAL_ANALYTIC_UNDER_STATIONARITY
RECURRENCE_AUTOCORRELATION_RANGE_VALUES = [-1,1]
```

Si :

```math
Tr[rho_theta(\delta n_q)^2]=0,
```

le diagnostic local de récurrence est :

```text
RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
```

et non un échec numérique.

## 2. Détecteur hystérétique

Pour une paire de niveaux :

```math
\gamma=(\gamma_-,\gamma_+),
\qquad
\gamma_-<\gamma_+<1,
```

et un événement candidat `tau`, on cherche uniquement sur `[0,tau]`.

Une sortie existe si :

```math
\exists t_{out}\le tau:\ C_q(t_{out})\le\gamma_-.
```

Un retour existe si, après une telle sortie :

```math
\exists t_{ret}\in(t_{out},tau]:\ C_q(t_{ret})\ge\gamma_+.
```

Les trois statuts exhaustifs sont :

```text
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
```

Les deux premiers signifient qu'aucune récurrence locale hystérétique n'a été détectée avant l'événement. Le troisième invalide l'interprétation temporelle correspondante pour ce couple de contrôle.

Aucun horizon global de recherche de revival n'est utilisé.

## 3. Domaine de contrôle Gamma

Les deux niveaux ont des rôles distincts :

```text
gamma_- : profondeur minimale de l'excursion (EXIT)
gamma_+ : niveau de récupération exigé (RETURN)
```

Ils ne sont pas réduits à un unique paramètre.

Cette clause caractérise la **structure du détecteur** : il conserve toujours un seuil de sortie `gamma_-` distinct et un seuil de retour `gamma_+` distinct. Elle n'interdit pas une paramétrisation préenregistrée à une seule coordonnée d'une **famille finie de paires à deux seuils** — c'est exactement ce que fait la chaîne anti-diagonale ci-dessous : chaque point de la chaîne reste une paire `(gamma_-,gamma_+)` complète.

Normatif :

```text
HYSTERETIC_PAIR_STRUCTURE = UNCHANGED
DETECTOR_THRESHOLD_COUNT  = TWO_DISTINCT_LEVELS
```

Le domaine normatif `Gamma` est un **ensemble fini préenregistré** contenu dans :

```math
\{(\gamma_-,\gamma_+):\gamma_-<\gamma_+<1\},
```

et borné dans l'ordre partiel du détecteur :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm},
```

c'est-à-dire :

```math
\gamma_-^{strict}\le\gamma_-\le\gamma_-^{perm},
\qquad
\gamma_+^{strict}\ge\gamma_+\ge\gamma_+^{perm}.
```

Aucune structure de produit rectangulaire `G_- x G_+` n'est exigée : l'ancienne exigence rectangulaire est supersédée. Un produit reste un cas particulier admissible lorsqu'il satisfait la contrainte ci-dessus.

La largeur :

```math
h(\gamma)=\gamma_+-\gamma_->0
```

est explicite pour tout point du domaine. Le point permissif porte la largeur minimale positive du domaine préenregistré ; `h=0` est exclu du contrôle principal.

### Chaîne anti-diagonale préenregistrée

Définir la coordonnée de domaine :

```math
\gamma(a)=(a,1-a),
\qquad
0<a<\frac12.
```

Préenregistrer exactement :

```text
GAMMA_A_VALUES = {1/8, 1/4, 3/8}.
```

Donc :

```text
GAMMA_VALUES =
{
(1/8,7/8),
(1/4,3/4),
(3/8,5/8)
}.
```

```text
GAMMA_STRICT     = (1/8,7/8)
GAMMA_MID        = (1/4,3/4)
GAMMA_PERMISSIVE = (3/8,5/8)
```

Largeurs :

```text
GAMMA_HYSTERESIS_WIDTHS = {3/4, 1/2, 1/4}.
```

Normatif :

```text
GAMMA_PARAMETERIZATION = ANTI_DIAGONAL_FIXED_CENTER
GAMMA_CENTER            = 1/2
GAMMA_GRID_TYPE          = THREE_POINT_ORDERED_CHAIN
```

Toutes les valeurs sont des rationnels binaires exacts.

### Le centre fixe n'a aucun statut physique

L'identité `gamma_-+gamma_+=1` est une restriction de **design de contrôle**. Elle n'est :

- ni une symétrie de la dynamique physique ;
- ni un énoncé de probabilité ;
- ni un théorème sélectionnant `1/2` ;
- ni une revendication que `1/2` est un seuil physique de récurrence.

Son but est d'éviter un réglage indépendant a posteriori de la profondeur de sortie et de la hauteur de retour.

Conséquence déclarée : `gamma_-^perm=3/8<1/2` et `gamma_+^perm=5/8>1/2`. Ceci crée une fenêtre de détection finie intentionnelle, décrite au §8.

Les bornes numériques de tolérance de croisement (voisinage de `C=gamma_-`, de `C=gamma_+`, contact tangentiel, séparation temporelle minimale sortie/retour) restent exclusivement sous `RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = OPEN`.

## 4. Monotonie du détecteur

À événement `tau` fixé :

- augmenter `gamma_-` rend la sortie plus facile à détecter ;
- diminuer `gamma_+` rend le retour plus facile à détecter.

Le détecteur `RETURN_BEFORE_EVENT` est donc monotone dans l'ordre partiel correspondant.

Le couple le plus permissif est la borne supérieure `gamma^perm` du domaine préenregistré : plus grand `gamma_-` et plus petit `gamma_+` admis.

Le couple le plus strict est la borne inférieure `gamma^strict` : plus petit `gamma_-` et plus grand `gamma_+` admis.

Ces deux bornes sont déclarées avec le domaine ; lorsque `Gamma` est un produit `G_- x G_+`, elles valent respectivement `(max G_-, min G_+)` et `(min G_-, max G_+)`. Pour la chaîne anti-diagonale ci-dessus, elles valent exactement `GAMMA_STRICT=(1/8,7/8)` et `GAMMA_PERMISSIVE=(3/8,5/8)`.

### Preuve par témoin commun

La monotonie rigoureuse s'établit par un témoin commun, pas par continuité.

Pour `a_1<a_2<1/2` :

```math
\gamma_-(a_1)<\gamma_-(a_2),
\qquad
\gamma_+(a_1)>\gamma_+(a_2).
```

Donc `gamma(a_1)` est plus strict que `gamma(a_2)`.

Si `RETURN_BEFORE_EVENT` se produit sous une paire stricte, il existe :

```math
t_{out}\le\tau:\ C(t_{out})\le\gamma_-^{strict},
```

et :

```math
t_{ret}\in(t_{out},\tau]:\ C(t_{ret})\ge\gamma_+^{strict}.
```

Comme `gamma_-^strict<=gamma_-^perm` et `gamma_+^strict>=gamma_+^perm`, le MÊME couple `(t_out,t_ret)` témoigne d'un retour pour toute paire plus permissive.

Donc :

```text
RETURN(strict) => RETURN(mid) => RETURN(permissive).
```

Et par contraposée :

```text
NO_RETURN(permissive) => NO_RETURN(mid) => NO_RETURN(strict).
```

## 5. Verdict robuste par les deux bornes

Le verdict sur tout `Gamma` est déterminé par deux évaluations seulement.

Si la borne permissive `gamma^perm` donne :

```text
NO_EXIT_BEFORE_EVENT
```

ou :

```text
EXIT_NO_RETURN_BEFORE_EVENT
```

alors aucun couple de `Gamma` ne peut donner de retour :

```text
RECURRENCE_STATUS = ROBUST_CLEAN
```

Si la borne stricte `gamma^strict` donne :

```text
RETURN_BEFORE_EVENT
```

alors tous les couples de `Gamma` donnent un retour :

```text
RECURRENCE_STATUS = ROBUST_CONTAMINATED
```

Dans tous les autres cas :

```text
RECURRENCE_STATUS = CONTROL_SENSITIVE
```

Une grille intermédiaire peut être publiée pour cartographier la frontière de sensibilité, mais elle ne participe pas au verdict.

Densifier `Gamma` après coup ne peut donc pas modifier le verdict robuste.

### Équivalence de verdict de la chaîne

`GAMMA_TWO_BOUND_VERDICT` (ci-dessus) ne dépend que de `gamma^strict` et `gamma^perm`. La chaîne anti-diagonale préenregistrée est donc **verdict-équivalente** à tout domaine `Gamma` fini ordonné plus grand ayant les mêmes extrema — en particulier au rectangle/intervalle d'ordre complet admissible borné par `gamma^strict=(1/8,7/8)` et `gamma^perm=(3/8,5/8)`.

Normatif :

```text
GAMMA_CHAIN_ROBUST_VERDICT_DEPENDS_ONLY_ON_ENDPOINTS = YES
GAMMA_INTERIOR_POINTS_ROLE                            = SENSITIVITY_DIAGNOSTIC_ONLY
```

La paire médiane `GAMMA_MID=(1/4,3/4)` est obligatoire pour la publication dans cette préenregistrement (cartographie de sensibilité), mais elle ne crée pas d'évidence confirmatoire indépendante.

Publier le profil complet des trois paires :

```text
RECURRENCE_GAMMA_PROFILE.
```

## 6. Événements concernés

Pour `T_grow`, la garde de récurrence est évaluée au minimum jusqu'à :

```math
\tau=T_{peak},
```

afin de couvrir toute la première montée utilisée pour définir l'argmax de croissance.

Pour un seuil `eta`, elle est évaluée jusqu'au franchissement descendant du même premier lobe :

```math
\tau=T_{down}(eta).
```

Ainsi tout le lobe associé au seuil est contrôlé.

Ce lot ne modifie que les valeurs du domaine `Gamma` (§3) ; ces horizons restent inchangés. `T_grow` n'est en particulier PAS redéfini par une égalité exacte à `T_peak` : la garde reste évaluée au minimum jusqu'à `T_peak`.

## 7. Covariance et comparaison de fonds

Le même domaine `Gamma` est utilisé pour :

```text
reference
+delta
-delta
chaque h_k
Lambda=2
Lambda=3
```

Un test de covariance `+delta <-> -delta` n'est recevable que si les événements comparés ont des statuts de récurrence compatibles sous le même `Gamma`.

Interdit :

- `Gamma` spécifique à un état ;
- `Gamma` spécifique à un signe ;
- `Gamma` spécifique à un cutoff ;
- recentrage spécifique à un événement ;
- combiner `gamma_-` d'une paire préenregistrée avec `gamma_+` d'une autre ;
- ajouter une nouvelle paire après inspection des courbes de récurrence ;
- rééchelonner les seuils à partir des minima/maxima observés.

Aucun changement du domaine `Gamma` ou de ses bornes `gamma^strict` / `gamma^perm` ne peut être utilisé pour rétablir une covariance ou une convergence de troncature après inspection des résultats.

Normatif :

```text
GAMMA_POSTHOC_SUBSTITUTION = FORBIDDEN.
```

## 8. Fenêtre de détection déclarée

Pour la paire permissive `gamma_perm=(3/8,5/8)`, un retour est détectable ssi il existe :

```math
t_1\le\tau:\ C_j(t_1)\le3/8
```

et ensuite :

```math
t_2\in(t_1,\tau]:\ C_j(t_2)\ge5/8.
```

Publier :

```text
GAMMA_EXIT_FLOOR       = 3/8
GAMMA_RETURN_FLOOR     = 5/8
GAMMA_MIN_DETECTED_SWING = 1/4
```

Restriction sémantique normative :

```text
ROBUST_CLEAN_SEMANTICS = NO_RECURRENCE_DETECTABLE_BY_PREREGISTERED_FAMILY.
```

`ROBUST_CLEAN` doit toujours être lu comme « aucune récurrence détectable par la famille préenregistrée », jamais comme une preuve d'absence de toute récurrence possible. Ne jamais écrire `ROBUST_CLEAN = NO_RECURRENCE` sans cette qualification.

### Insensibilité déclarée

Documenter explicitement que la famille préenregistrée ne détecte PAS comme récurrence :

A. toute trajectoire avec :

```math
\min_{0\le t\le\tau}C_j(t)>3/8,
```

même si elle oscille/revisite des valeurs ensuite ;

B. après une sortie armée, toute récupération qui n'atteint jamais `5/8` avant l'horizon local de l'événement.

Normatif :

```text
GAMMA_DECLARED_INSENSITIVITY =
{
RECURRENCE_WITHOUT_EXIT_BELOW_OR_EQUAL_3/8,
RECOVERY_BELOW_5/8_AFTER_EXIT
}.
```

Ceci n'est ni un blocage ni un défaut après préenregistrement : cela définit le sens opérationnel du détecteur fini de récurrence.

La garde séparée de pureté de chemin reste requise et n'est PAS affaiblie par ce choix de `Gamma`.

### Niveaux de sortie positifs

Tous les `gamma_-` sont positifs.

Conséquences déclarées :

- toute trajectoire continue atteignant `C_j<=0` traverse nécessairement tous les seuils `gamma_-` positifs auparavant ;
- les excursions profondes/négatives ne sont donc jamais manquées, `gamma_-` étant positif ;
- les excursions modérées restant au-dessus de `3/8` sont intentionnellement hors de la fenêtre de détection permissive et relèvent de l'insensibilité déclarée ci-dessus, jamais interprétées silencieusement comme preuve d'absence de récurrence.

## 9. Portée

La garde de récurrence ne mesure pas l'enroulement topologique et ne remplace pas la garde de composition sectorielle / pureté de chemin.

Le verdict temporel complet reste conditionné à deux diagnostics distincts :

```text
PATH_CONTROL
RECURRENCE_CONTROL
```

## 10. Statut

```text
GLOBAL_REVIVAL_WINDOW          = ABANDONED
EVENT_LOCAL_RECURRENCE_GUARD   = VALIDATED_FOR_FREEZE
HYSTERETIC_PAIR_STRUCTURE      = UNCHANGED
DETECTOR_THRESHOLD_COUNT       = TWO_DISTINCT_LEVELS
GAMMA_RECTANGULAR_DOMAIN       = SUPERSEDED
GAMMA_ORDERED_DOMAIN           = VALIDATED_FOR_FREEZE
GAMMA_TWO_BOUND_VERDICT        = VALIDATED_FOR_FREEZE
GAMMA_CHAIN_ROBUST_VERDICT_DEPENDS_ONLY_ON_ENDPOINTS = YES
GAMMA_INTERIOR_POINTS_ROLE     = SENSITIVITY_DIAGNOSTIC_ONLY
ZERO_LOCAL_VARIANCE_STATUS     = VALIDATED_FOR_FREEZE

RECURRENCE_AUTOCORRELATION_RANGE        = STRUCTURAL_ANALYTIC_UNDER_STATIONARITY
RECURRENCE_AUTOCORRELATION_RANGE_VALUES = [-1,1]

GAMMA_CONTROL_DOMAIN_AND_GRID   = VALIDATED_FOR_FREEZE
GAMMA_STRICT_VALUES             = VALIDATED_FOR_FREEZE
GAMMA_PERM_VALUES               = VALIDATED_FOR_FREEZE

GAMMA_PARAMETERIZATION = ANTI_DIAGONAL_FIXED_CENTER
GAMMA_CENTER            = 1/2
GAMMA_A_VALUES          = {1/8,1/4,3/8}
GAMMA_VALUES            = {(1/8,7/8),(1/4,3/4),(3/8,5/8)}
GAMMA_STRICT             = (1/8,7/8)
GAMMA_MID                = (1/4,3/4)
GAMMA_PERMISSIVE         = (3/8,5/8)
GAMMA_HYSTERESIS_WIDTHS  = {3/4,1/2,1/4}
GAMMA_GRID_TYPE          = THREE_POINT_ORDERED_CHAIN

GAMMA_EXIT_FLOOR         = 3/8
GAMMA_RETURN_FLOOR       = 5/8
GAMMA_MIN_DETECTED_SWING = 1/4

ROBUST_CLEAN_SEMANTICS = NO_RECURRENCE_DETECTABLE_BY_PREREGISTERED_FAMILY

GAMMA_POSTHOC_SUBSTITUTION = FORBIDDEN

RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = OPEN
```
