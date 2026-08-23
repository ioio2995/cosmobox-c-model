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

Les règles numériques de certification des franchissements (`C=gamma_-`, `C=gamma_+`), des contacts tangentiels, de l'ordonnancement sortie/retour et de l'incertitude d'horizon sont désormais fixées par `RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = VALIDATED_FOR_FREEZE` selon le protocole fail-closed de la §11. Aucune nouvelle tolérance scalaire de récurrence n'est introduite : `RECURRENCE_HYSTERESIS_NEW_SCALAR_TOLERANCE = NONE`.

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

RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = VALIDATED_FOR_FREEZE
```

Le protocole numérique complet est défini au §11 ci-dessous.

## 11. Certification numérique fail-closed

Cette section ferme `RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS`. Elle ne rouvre ni le domaine `Gamma` (§3), ni les valeurs `Gamma` (§3), ni la sémantique du détecteur de récurrence (§2), ni la garde de pureté de chemin.

### 11.1 Représentation spectrale exacte de `C_j`

Pour chaque point stationnaire évalué, `[rho_theta,H(theta)]=0`. Avec `A=delta n_j` et `V_j=Tr[rho_theta A^2]>0`, l'autocorrélation connectée normalisée est :

```math
C_j(t)=\frac{Re\,Tr[\rho_\theta A(t)A]}{V_j}.
```

Dans une base propre commune de `rho` et `H` :

```math
\boxed{
C_j(t)=\sum_kw_k\cos(\omega_kt),
\qquad
w_k\ge0,
\qquad
\sum_kw_k=1.
}
```

Important : ces fréquences de récurrence sont des différences d'énergie générales `omega_k=|E_a-E_b|`, pas seulement des fréquences d'excitation du fondamental. Néanmoins :

```math
0\le\omega_k\le\Omega_{safe},
\qquad
\Omega_{safe}=E_{max}-E_0.
```

Normatif :

```text
RECURRENCE_COSINE_REPRESENTATION = STRUCTURAL_ANALYTIC_UNDER_STATIONARITY
RECURRENCE_CERTIFICATION_OSCILLATORY_FACTOR = 1
s_rec = 1
```

### 11.2 Bornes structurelles exactes des dérivées

Les poids positifs normalisés donnent directement :

```math
|C_j'(t)|\le\sum_kw_k\omega_k\le\Omega_{safe},
\qquad
|C_j''(t)|\le\sum_kw_k\omega_k^2\le\Omega_{safe}^2,
```

et plus généralement `|C_j^{(r)}(t)|<=Omega_safe^r`.

Les moments `M_r=sum_k w_k omega_k^r` peuvent être publiés comme diagnostics / bornes non normatives plus serrées. Mais la certification CONFIRMATOIRE d'exclusion de cellule et d'unicité de récurrence NE DOIT PAS dépendre de `M_1`/`M_2` numériquement normalisés.

Bornes sûres normatives :

```text
L_rec  = Omega_safe
L2_rec = Omega_safe^2
```

Ce choix échange délibérément de l'efficacité contre de la robustesse face à un `V_j` petit.

### 11.3 Bêta et tolérances de racine communs

Réutiliser exactement :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}
```

Cellule de certification de récurrence initiale :

```math
\Delta t_k^{rec}=\beta_k\frac{\pi}{\Omega_{safe}}.
```

Coordonnée d'événement de récurrence :

```math
u_{rec}=\frac{\Omega_{safe}t}{\pi}.
```

Réutiliser exactement `tau_root=1e-12`, `tau_event=1e-10`, `SIMPLE_ROOT_CONTROL`, `DEGENERATE_ROOT_CONTROL`, `SPECTRAL_PRECISION_CONTROL` et l'échelle de précision `P0/P1/P2` existante. Aucune nouvelle famille de bracketing, aucune nouvelle tolérance de racine, aucune nouvelle tolérance scalaire de récurrence.

### 11.4 Porte de précision au petit dénominateur

Cette sous-section ferme le blocage B1 de la revue Opus ciblée.

`C_j` est un rapport normalisé `N_j/V_j`. Pour un prédicat de récurrence confirmatoire avec `V_j` non structurellement nul, la normalisation elle-même doit passer une porte `p/2p` dédiée.

Évaluer `V_j` indépendamment à `p` et `2p` depuis l'expression opérateur directe :

```math
V_j^{(q)}=Tr[\rho_\theta^{(q)}(\delta n_j^{(q)})^2].
```

Pour un projecteur `n_j`, une expression équivalente stable peut être utilisée :

```math
V_j=\langle n_j\rangle(1-\langle n_j\rangle),
```

mais la quantité normative reste la variance.

Si un oracle `STRUCTURAL_ANALYTIC` exact établit `V_j=0` : utiliser la règle de variance nulle existante (§11.19).

Sinon exiger `V_j^{(2p)}>0` et définir le diagnostic de stabilité relatif, réellement relatif :

```math
\boxed{
r_V=\frac{|V_j^{(2p)}-V_j^{(p)}|}{V_j^{(2p)}}.
}
```

Exiger `r_V<=tau_event`.

IMPORTANT : ne PAS normaliser par `max(1,V_j)`. Cela deviendrait un test absolu pour `0<V_j<=1` et ne protégerait pas contre l'amplification par petit dénominateur.

Soit la masse spectrale brute NON NORMALISÉE `W_0^{(q)}=sum_k \widetilde w_k^{(q)}`, où les poids bruts positifs `\widetilde w_k` précèdent la division par `V_j`. Identité exacte : `W_0=V_j`. Exiger aux niveaux `p` et `2p` acceptés :

```math
\boxed{
r_{mass}^{(q)}=\frac{|W_0^{(q)}-V_j^{(q)}|}{V_j^{(q)}}\le\tau_{event}.
}
```

Publier/vérifier également `|C_j^{(q)}(0)-1|<=tau_event` (diagnostic de normalisation ; la fermeture indépendante `W_0` versus `V_j` reste la vérification anti-petit-dénominateur primaire).

Si le statut de positivité/non-nullité de `V_j` est non résolu, si `r_V` échoue après l'escalade de précision existante, si la fermeture de masse spectrale brute échoue, ou si la fermeture normalisée de `C_j(0)` échoue :

```text
RECURRENCE_NORMALIZATION_NUMERICALLY_INCONCLUSIVE
```

Aucun `NO RETURN`/`ROBUST_CLEAN` confirmatoire ne peut être produit dans ce cas.

Toute classification exact-zéro versus simplement-petit est désormais routée
par `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE`
(définition normative complète : `numerical-zero-symmetry-control.md` §E) :
la branche exacte structurelle `V_j=0` (`STRUCTURAL_ANALYTIC`, §11.19)
reste inchangée ; si `V_j` n'est établi ni exactement nul par théorème ni
`ROBUST_NONZERO` sous cette classification, mais seulement
`NUMERICALLY_ZERO_COMPATIBLE`, la branche est distincte et NON confirmatoire
(`RECURRENCE_NORMALIZATION_NUMERICALLY_INCONCLUSIVE`) : elle ne peut jamais
être promue silencieusement en `CERTIFIED_NO_RETURN`/`ROBUST_CLEAN` à partir
d'une seule petitesse numérique.

Normatif :

```text
RECURRENCE_NORMALIZATION_GATE = RELATIVE_V_P2P_PLUS_RAW_SPECTRAL_MASS_CLOSURE
```

### 11.5 Intervalles de contrôle `p/2p` pour `C` et `C'`

Pour un temps physique `t` évalué indépendamment à `p` et `2p`, définir :

```math
e_C(t)=|C_j^{(2p)}(t)-C_j^{(p)}(t)|,
```

et l'intervalle de contrôle numérique OPÉRATIONNEL, non une enclosure probabiliste ou d'arithmétique d'intervalles rigoureuse :

```math
I_C(t)=[\,C_j^{(2p)}(t)-e_C(t),\,C_j^{(2p)}(t)+e_C(t)\,].
```

De même `e_{C'}(t)=|C_j'^{(2p)}(t)-C_j'^{(p)}(t)|`, avec `I_{C'}` analogue lorsque requis.

Ces écarts sont utilisés à CHAQUE évaluation de cellule/témoin confirmatoire, y compris les branches sans racine. C'est essentiel : une branche sans croisement/sans sortie ne doit pas contourner la porte de précision.

### 11.6 Fonctions de racine

Pour une paire `Gamma` : `g_-(t)=C_j(t)-gamma_-` et `g_+(t)=C_j(t)-gamma_+`.

La racine simple nominale de SORTIE a `g_-=0`, `C_j'<0`. La racine simple nominale de RETOUR a `g_+=0`, `C_j'>0`.

Mais le prédicat binaire RETOUR peut aussi être certifié directement par un témoin ponctuel (§11.14) ; la localisation de racine n'est pas requise pour la branche positive/existentielle.

### 11.7 Exclusion de cellule à marge d'erreur

Pour une cellule centrée en `t_c` de demi-largeur `h`, un certificat de cellule vide confirmatoire pour `g_gamma=C_j-gamma` exige :

```math
\boxed{
|C_j^{(2p)}(t_c)-\gamma|>e_C(t_c)+\Omega_{safe}h.
}
```

Normatif :

```text
RECURRENCE_EMPTY_CELL_MARGIN = P2P_FUNCTION_DISCREPANCY_PLUS_STRUCTURAL_LIPSCHITZ
```

L'ancien test sans marge `|C_j(t_c)-gamma| > M_1 h` NE DOIT PAS être utilisé pour la certification confirmatoire de récurrence.

Cette correction est LOCALE à la fonction `C_j` de récurrence normalisée. Elle ne modifie pas les formules d'exclusion génériques déjà validées pour `chi`, `H_grow`, `H_path`, etc. (`temporal-event-solver.md`, `event-bandwidth-bracketing.md`).

### 11.8 Cellule à racine simple unique

Pour une cellule candidate de racine de récurrence centrée en `t_c` de demi-largeur `h` :

```math
\boxed{
|C_j'^{(2p)}(t_c)|>e_{C'}(t_c)+\Omega_{safe}^2h.
}
```

Ceci est le certificat spécifique-récurrence de stricte monotonie / racine simple unique.

Réutiliser `SIMPLE_ROOT_CONTROL`, `DEGENERATE_ROOT_CONTROL`, `tau_root`, l'exhaustion de subdivision existante. Si la condition ne peut pas être certifiée : ne pas inférer de multiplicité, subdiviser selon le protocole existant, puis après exhaustion : `RECURRENCE_THRESHOLD_CONTACT_UNRESOLVED` ou `RECURRENCE_CROSSING_NUMERICALLY_INCONCLUSIVE`, selon le cas.

Normatif :

```text
RECURRENCE_UNIQUENESS_MARGIN = P2P_DERIVATIVE_DISCREPANCY_PLUS_STRUCTURAL_SECOND_DERIVATIVE_BOUND
```

### 11.9 Qualification directionnelle de racine

Pour une estimation de racine simple certifiée `t_hat` avec incertitude de coordonnée de récurrence `e_u` :

```math
e_t=\frac{\pi e_u}{\Omega_{safe}},
\qquad
e_{C',loc}=\Omega_{safe}^2e_t,
\qquad
e_{C',dir}=e_{C'}(\hat t)+e_{C',loc}.
```

Une racine de SORTIE ne qualifie que si `C_j'^{(2p)}(\hat t)+e_{C',dir}<0`.

Une racine de RETOUR ne qualifie que si `C_j'^{(2p)}(\hat t)-e_{C',dir}>0`.

Sinon : `RECURRENCE_CROSSING_DIRECTION_UNRESOLVED`. Aucune tolérance scalaire sur le signe de la dérivée.

Normatif :

```text
RECURRENCE_DIRECTIONAL_CERTIFICATION = DERIVATIVE_CONTROL_INTERVAL_SIGN
```

### 11.10 Précision de localisation de racine

Pour une racine de récurrence simple certifiée :

```math
\epsilon_{g,spec}(t)=|C_j^{(2p)}(t)-C_j^{(p)}(t)|.
```

Réutiliser :

```math
\epsilon_{u,spec}=\frac{\Omega_{safe}}{\pi}\frac{\epsilon_{g,spec}(t_*)}{|C_j'(t_*)|},
```

et `tau_event=1e-10`, la porte existante de déplacement spectral de racine, la porte `p/2p` de coordonnée de racine, la largeur solveur `tau_root`, la construction existante de `e_u`. Si non résolu : `RECURRENCE_CROSSING_NUMERICALLY_INCONCLUSIVE`.

### 11.11 Contacts tangentiels / multiples

Le détecteur mathématique utilise `C<=gamma_-` et `C>=gamma_+`. Un contact exactement tangent à un seuil compte donc mathématiquement comme un contact.

La précision finie NE DOIT PAS inférer une tangence/multiplicité exacte. Si un contact de seuil ne peut être certifié par la voie directionnelle simple : réutiliser `DEGENERATE_ROOT_CONTROL`. Après exhaustion finie : `RECURRENCE_THRESHOLD_CONTACT_UNRESOLVED`.

Un tel contact non résolu DOIT empêcher `CERTIFIED_NO_RETURN`, et donc empêcher `ROBUST_CLEAN` lorsqu'il est décisif.

Un contact tangent exact ne peut être promu que par un oracle `STRUCTURAL_ANALYTIC` établissant : l'égalité de niveau exacte ; la condition de dérivée stationnaire exacte ; l'inégalité de côté local correcte. Aucun secours numérique par dérivées d'ordre supérieur.

Normatif :

```text
RECURRENCE_TANGENTIAL_CONTACT_RULE = STRUCTURAL_ORACLE_OR_NUMERICALLY_UNRESOLVED
```

### 11.12 Séparation structurelle sortie/retour

Aucune tolérance de temps minimal arbitraire. Pour toute SORTIE réelle en `t_out` et RETOUR ultérieur en `t_ret`, avec `h_gamma=gamma_+-gamma_-` et `|C_j'|<=Omega_safe`, le théorème des accroissements finis donne :

```math
\boxed{
t_{ret}-t_{out}\ge\frac{h_\gamma}{\Omega_{safe}}.
}
```

En coordonnée de récurrence : `u_ret - u_out >= h_gamma/pi`. Pour la paire permissive, `h_gamma=1/4`, donc `u_ret-u_out>=1/(4pi)~=0.079577...`.

Normatif :

```text
RECURRENCE_MIN_TIME_SEPARATION = STRUCTURAL_DERIVED_FROM_HYSTERESIS_AND_OMEGA_SAFE
RECURRENCE_MIN_SEPARATION_NEW_TOLERANCE = NONE
```

Aucun `M_1` numériquement normalisé n'est requis pour cette borne confirmatoire.

### 11.13 Ordonnancement sortie/retour pour la voie par racine

Si une première SORTIE est localisée dans `I_out=[t_out^-,t_out^+]`, une recherche de RETOUR par racine ne peut démarrer strictement après `t_out^+` que si la séparation structurelle garantit qu'aucun retour ne peut se trouver dans l'intervalle de sortie. Condition suffisante :

```math
t_{out}^+<t_{out}^-+\frac{h_\gamma}{\Omega_{safe}}.
```

Si cette condition échoue : `RECURRENCE_EXIT_RETURN_ORDERING_UNRESOLVED`. Si elle passe, tout retour véritable se trouve strictement après `t_out^+` ; rechercher les contacts `g_+` qualifiants sur `(t_out^+,tau]`.

Aucun langage discrétionnaire du type « exclure la structure de descroisement pré-sortie connue » n'est utilisé.

### 11.14 `CERTIFIED_RETURN` fondé sur témoin

RETOUR est un prédicat existentiel. Un verdict positif de récurrence n'exige donc PAS une énumération exhaustive de racines.

Pour un horizon fixe/incertain avec horizon garanti au plus tôt `tau_-`, `CERTIFIED_RETURN` est établi s'il existe deux temps d'évaluation physique `t_1<t_2<=tau_-` tels que les intervalles de contrôle `p/2p` certifient :

```math
\sup I_C(t_1)\le\gamma_-
\qquad\text{et}\qquad
\inf I_C(t_2)\ge\gamma_+.
```

La porte de normalisation (§11.4) doit déjà avoir été franchie. C'est un témoin direct valide de SORTIE suivie de RETOUR. Ce n'est PAS un estimateur de croisement sur grille échantillonnée ni un temps d'événement fondé sur interpolation. Aucun temps de croisement n'a besoin d'être publié depuis ce témoin, sauf certification de racine séparée. Un témoin directionnel fondé sur racine reste autorisé, mais n'est pas requis pour `CERTIFIED_RETURN`.

Normatif :

```text
RECURRENCE_CERTIFIED_RETURN_MODE = WITNESS_BASED_EXISTENTIAL
```

### 11.15 `CERTIFIED_NO_RETURN` fondé sur complétude

NO RETURN est une revendication universelle/négative et exige donc une complétude continue. Deux branches résolues sont autorisées.

**A. SANS SORTIE CERTIFIÉE.** Si toutes les cellules `g_-` sur `[0,tau_+]` sont certifiées vides sous la marge `p/2p` spécifique à la récurrence, avec `C_j(0)=1>gamma_-` et aucune cellule de contact non résolue, alors :

```text
RECURRENCE_THREE_STATE_DETAIL = NO_EXIT_BEFORE_EVENT
RECURRENCE_RETURN_PREDICATE   = CERTIFIED_NO_RETURN
```

**B. SORTIE CERTIFIÉE, PUIS PAS DE RETOUR CERTIFIÉ.** Exiger un intervalle de première SORTIE certifiée `I_out=[t_out^-,t_out^+]`, avec `t_out^+<=tau_-` (SORTIE garantie pour tout horizon vrai admissible), et la garde d'ordonnancement structurelle du §11.13. Certifier ensuite que chaque cellule `g_+` sur `(t_out^+,tau_+]` est soit certifiée vide, soit résolue en une racine simple/contact non-RETOUR, et qu'aucun contact tangentiel/dégénéré de RETOUR non résolu ne subsiste. Alors :

```text
RECURRENCE_THREE_STATE_DETAIL = EXIT_NO_RETURN_BEFORE_EVENT
RECURRENCE_RETURN_PREDICATE   = CERTIFIED_NO_RETURN
```

Toute ambiguïté sur le fait que la SORTIE se soit produite avant l'horizon, ne relevant ni de la branche A ni de la branche B, donne `RECURRENCE_HORIZON_UNRESOLVED` ou `RECURRENCE_FIXED_HORIZON_NUMERICALLY_INCONCLUSIVE`. Une situation ambiguë NO_EXIT-versus-EXIT_NO_RETURN N'EST PAS promue en `CERTIFIED_NO_RETURN` dans ce protocole primaire. Ceci est intentionnellement conservateur.

Normatif :

```text
RECURRENCE_CERTIFIED_NO_RETURN_MODE = CONTINUOUS_COMPLETENESS_BASED
```

### 11.16 Règle d'horizon fixe / incertain

Soit `I_tau=[tau_-,tau_+]`. Pour RETOUR : un témoin doit se compléter avant `tau_-`. Pour NO RETURN : le certificat négatif/de complétude doit couvrir jusqu'à `tau_+`. Ainsi :

```text
RETOUR avant tau_-  -> robuste à l'incertitude d'horizon
NO RETURN jusqu'à tau_+ -> robuste à l'incertitude d'horizon
```

Tout contact potentiellement décisif confiné à `(tau_-,tau_+]` donne `RECURRENCE_HORIZON_UNRESOLVED`.

Normatif :

```text
RECURRENCE_HORIZON_UNCERTAINTY_RULE = EARLIEST_HORIZON_FOR_RETURN_LATEST_HORIZON_FOR_NO_RETURN
```

Aucune nouvelle tolérance d'horizon.

### 11.17 Horizon opérationnel primaire de `T_grow`

L'énoncé scientifique déjà validé demeure : la garde de récurrence pour `T_grow` est évaluée AU MOINS jusqu'à `T_peak` (§6). Pour la campagne numérique primaire préenregistrée de Toy 0B, ce minimum est instancié déterministiquement comme :

```text
RECURRENCE_TGROW_PRIMARY_HORIZON = T_peak
```

C'est un choix de préenregistrement OPÉRATIONNEL, pas une redéfinition de l'énoncé analytique. Ainsi : utiliser l'intervalle `T_peak` certifié comme `I_tau` pour la garde `T_grow` primaire ; aucune extension ou réduction post-hoc de l'horizon primaire ; tout diagnostic de récurrence à horizon plus long doit être séparément préenregistré et rester `DIAGNOSTIC_ONLY` sauf promotion explicite par la gouvernance.

Pour les événements de seuil, préserver :

```text
RECURRENCE_TTHR_PRIMARY_HORIZON = T_down(eta)
```

Aucune définition scientifique d'événement n'est changée.

### 11.18 Évaluation normalisée complète `p/2p`

Évaluer la récurrence indépendamment à `p` et `2p`, y compris `rho_theta`/`H(theta)`, `V_j`, la masse spectrale brute `W_0`, les poids normalisés, `C_j(t)`, `C_j'(t)`, les identités de racine/cellule, les comparaisons d'horizon, l'agrégation par site. L'écart `p/2p` doit entrer dans tous les tests confirmatoires de cellule et de témoin. La normalisation n'est jamais évaluée une seule fois puis réutilisée entre précisions. Si l'identité de racine/cellule est incohérente entre les précisions acceptées : `RECURRENCE_CROSSING_NUMERICALLY_INCONCLUSIVE`.

### 11.19 Variance locale nulle

Préserver `RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE`. Ne PAS identifier silencieusement `V_j=0` exact avec `CERTIFIED_NO_RETURN`.

Pour l'agrégation au niveau relation : si l'autre extrémité certifie RETOUR, la relation RETOUR est certifiée ; sinon toute extrémité requise avec variance locale exactement nulle empêche une relation `NO RETURN` confirmatoire au niveau relation :

```text
RECURRENCE_RELATION_NONCONFIRMATORY_ZERO_LOCAL_VARIANCE
```

Ceci est fail-closed. Aucune convention optionnelle `C_j==1` à `V_j=0` n'est introduite dans ce lot. La classification exact-zéro versus simplement-petit est
routée par `NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE`
(définition normative complète : `numerical-zero-symmetry-control.md` §E) :
`V_j=0` exact par théorème structurel garde exactement la branche existante
ci-dessus ; `V_j` seulement `NUMERICALLY_ZERO_COMPATIBLE` reçoit une branche
NUMÉRIQUE distincte et également non confirmatoire
(`RECURRENCE_NORMALIZATION_NUMERICALLY_INCONCLUSIVE`, §11.4 ci-dessus) ; ni
l'une ni l'autre branche ne peut jamais produire `CERTIFIED_NO_RETURN` à
partir d'une seule petitesse numérique.

### 11.20 Agrégation par site

Pour une paire `Gamma` et une relation `(p,q)` : si l'un ou l'autre site normatif d'extrémité a `CERTIFIED_RETURN`, alors au niveau relation `RECURRENCE_RETURN_PREDICATE = CERTIFIED_RETURN`. Si LES DEUX sites normatifs d'extrémité ont `CERTIFIED_NO_RETURN`, alors au niveau relation `RECURRENCE_RETURN_PREDICATE = CERTIFIED_NO_RETURN`. Sinon `RECURRENCE_RETURN_PREDICATE = NUMERICALLY_INCONCLUSIVE`.

Ceci est le complément fail-closed exact de la règle existentielle par site déjà gelée.

### 11.21 Verdict robuste Gamma

Évaluer le prédicat au niveau relation à `GAMMA_STRICT`, `GAMMA_MID`, `GAMMA_PERMISSIVE`, selon la règle des deux bornes déjà validée (§5) : `permissive=CERTIFIED_NO_RETURN => ROBUST_CLEAN` ; `strict=CERTIFIED_RETURN => ROBUST_CONTAMINATED` ; `CONTROL_SENSITIVE` exige `strict=CERTIFIED_NO_RETURN` ET `permissive=CERTIFIED_RETURN` ; sinon `NUMERICALLY_INCONCLUSIVE`. La paire médiane reste `SENSITIVITY_DIAGNOSTIC_ONLY`.

Contrôle croisé du profil publié complet contre la monotonie `Gamma` exacte déjà démontrée (§4) :

```text
RETURN(strict) => RETURN(mid) => RETURN(permissive)
NO_RETURN(permissive) => NO_RETURN(mid) => NO_RETURN(strict)
```

Toute contradiction observée entre statuts certifiés indépendamment évalués force `RECURRENCE_GAMMA_MONOTONICITY_VIOLATION` et `RECURRENCE_STATUS = NUMERICALLY_INCONCLUSIVE`. Une telle contradiction n'est jamais résolue en choisissant un seul calcul.

### 11.22 Acceptabilité du contrôle de récurrence

`RECURRENCE_CONTROL_ACCEPTABLE` ssi `RECURRENCE_STATUS = ROBUST_CLEAN` et que toutes les dépendances de récurrence requises pour ce verdict sont confirmatoires sous les règles ci-dessus.

Non acceptable : `ROBUST_CONTAMINATED`, `CONTROL_SENSITIVE`, `NUMERICALLY_INCONCLUSIVE`, cas non confirmatoires de variance nulle, cas de normalisation non résolue.

La validité finale d'événement reste : `PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE AND RECURRENCE_CONTROL_ACCEPTABLE`.

### 11.23 Raccourci DC optionnel

À partir des poids cosinus positifs, la masse à fréquence nulle `w_0>=0`. Comme `sum_{omega>0} w_omega = 1-w_0` et `cos>=-1` :

```math
C_j(t)\ge w_0-(1-w_0)=2w_0-1.
```

Donc si un certificat spectral exact/accepté établit `2w_0-1 > gamma_-` pour une paire `Gamma`, alors la SORTIE est structurellement impossible pour cette paire : `NO_EXIT_BEFORE_EVENT`.

Ceci est un raccourci certifié OPTIONNEL. Il doit utiliser la même porte de normalisation. Il n'affaiblit jamais le certificat de cellule continue général.

Normatif :

```text
RECURRENCE_DC_NO_EXIT_SHORTCUT = ALLOWED_DIAGNOSTIC_CERTIFICATE
```

### 11.24 Statut de clôture

```text
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = VALIDATED_FOR_FREEZE

RECURRENCE_COSINE_REPRESENTATION = STRUCTURAL_ANALYTIC_UNDER_STATIONARITY
RECURRENCE_CERTIFICATION_OSCILLATORY_FACTOR = 1

RECURRENCE_CERTIFICATION_BETA_VALUES = EXISTING_BETA_VALUES
RECURRENCE_ROOT_TOLERANCE            = EXISTING_TAU_ROOT
RECURRENCE_EVENT_TOLERANCE           = EXISTING_TAU_EVENT

RECURRENCE_NORMALIZATION_GATE = RELATIVE_V_P2P_PLUS_RAW_SPECTRAL_MASS_CLOSURE

RECURRENCE_EMPTY_CELL_MARGIN = P2P_FUNCTION_DISCREPANCY_PLUS_STRUCTURAL_LIPSCHITZ
RECURRENCE_UNIQUENESS_MARGIN = P2P_DERIVATIVE_DISCREPANCY_PLUS_STRUCTURAL_SECOND_DERIVATIVE_BOUND

RECURRENCE_DIRECTIONAL_CERTIFICATION = DERIVATIVE_CONTROL_INTERVAL_SIGN
RECURRENCE_TANGENTIAL_CONTACT_RULE   = STRUCTURAL_ORACLE_OR_NUMERICALLY_UNRESOLVED

RECURRENCE_MIN_TIME_SEPARATION          = STRUCTURAL_DERIVED_FROM_HYSTERESIS_AND_OMEGA_SAFE
RECURRENCE_MIN_SEPARATION_NEW_TOLERANCE = NONE

RECURRENCE_CERTIFIED_RETURN_MODE    = WITNESS_BASED_EXISTENTIAL
RECURRENCE_CERTIFIED_NO_RETURN_MODE = CONTINUOUS_COMPLETENESS_BASED

RECURRENCE_HORIZON_UNCERTAINTY_RULE = EARLIEST_HORIZON_FOR_RETURN_LATEST_HORIZON_FOR_NO_RETURN

RECURRENCE_TGROW_PRIMARY_HORIZON = T_peak
RECURRENCE_TTHR_PRIMARY_HORIZON  = T_down(eta)

RECURRENCE_RETURN_PREDICATE = CERTIFIED_RETURN | CERTIFIED_NO_RETURN | NUMERICALLY_INCONCLUSIVE

RECURRENCE_CONTROL_ACCEPTABLE = ROBUST_CLEAN_ONLY

RECURRENCE_HYSTERESIS_NEW_SCALAR_TOLERANCE = NONE

RECURRENCE_DC_NO_EXIT_SHORTCUT = ALLOWED_DIAGNOSTIC_CERTIFICATE

NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = VALIDATED_FOR_FREEZE
```

Définition normative complète de la politique numérique : `numerical-zero-symmetry-control.md`. Ce lot ne modifie ni le domaine `Gamma` (§3), ni les bornes numériques d'hystérésis déjà fermées ci-dessus.
