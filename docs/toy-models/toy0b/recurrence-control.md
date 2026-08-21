# Toy Model 0B — contrôle hystérétique de récurrence

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne la garde locale de récurrence évaluée directement avant chaque événement temporel candidat. Il remplace l'idée d'une fenêtre globale de revival.

## 1. Autocorrélation locale connectée

Pour un fond stationnaire `rho_theta` :

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
gamma_- : profondeur minimale de l'excursion
gamma_+ : niveau de récupération exigé
```

Ils ne sont pas réduits à un unique paramètre.

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

Les bornes numériques `gamma^strict` et `gamma^perm` restent ouvertes jusqu'au gel numérique du protocole.

## 4. Monotonie du détecteur

À événement `tau` fixé :

- augmenter `gamma_-` rend la sortie plus facile à détecter ;
- diminuer `gamma_+` rend le retour plus facile à détecter.

Le détecteur `RETURN_BEFORE_EVENT` est donc monotone dans l'ordre partiel correspondant.

Le couple le plus permissif est la borne supérieure `gamma^perm` du domaine préenregistré : plus grand `gamma_-` et plus petit `gamma_+` admis.

Le couple le plus strict est la borne inférieure `gamma^strict` : plus petit `gamma_-` et plus grand `gamma_+` admis.

Ces deux bornes sont déclarées avec le domaine ; lorsque `Gamma` est un produit `G_- x G_+`, elles valent respectivement `(max G_-, min G_+)` et `(min G_-, max G_+)`.

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

## 7. Covariance et comparaison de fonds

Le même domaine `Gamma` est utilisé pour :

```text
reference
+delta
-delta
Lambda=2
Lambda=3
```

Un test de covariance `+delta <-> -delta` n'est recevable que si les événements comparés ont des statuts de récurrence compatibles sous le même `Gamma`.

Aucun changement du domaine `Gamma` ou de ses bornes `gamma^strict` / `gamma^perm` ne peut être utilisé pour rétablir une covariance ou une convergence de troncature après inspection des résultats.

## 8. Portée

La garde de récurrence ne mesure pas l'enroulement topologique et ne remplace pas la garde de composition sectorielle / pureté de chemin.

Le verdict temporel complet reste conditionné à deux diagnostics distincts :

```text
PATH_CONTROL
RECURRENCE_CONTROL
```

## 9. Statut

```text
GLOBAL_REVIVAL_WINDOW          = ABANDONED
EVENT_LOCAL_RECURRENCE_GUARD   = VALIDATED_FOR_FREEZE
HYSTERETIC_PAIR_STRUCTURE      = VALIDATED_FOR_FREEZE
GAMMA_RECTANGULAR_DOMAIN       = SUPERSEDED
GAMMA_ORDERED_DOMAIN           = VALIDATED_FOR_FREEZE
GAMMA_TWO_BOUND_VERDICT        = VALIDATED_FOR_FREEZE
ZERO_LOCAL_VARIANCE_STATUS     = VALIDATED_FOR_FREEZE
GAMMA_STRICT_VALUES            = OPEN
GAMMA_PERM_VALUES              = OPEN
```
