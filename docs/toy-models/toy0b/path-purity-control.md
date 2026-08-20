# Toy Model 0B — pureté de chemin et contrôle de l'interprétation d'arrivée

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `transition-fibers.md`, `path-grading.md`, `validation-plan.md`

Ce document consigne la structure retenue pour la pureté sectorielle et transforme `epsilon_path` d'un seuil unique arbitraire en variable de contrôle. Il ne remplace pas la spécification principale et devra être consolidé lors de la revue documentaire générale.

## 1. Décomposition sectorielle

Pour chaque secteur physique `alpha`, on note :

```math
\chi_\alpha(t)=c_\alpha t^{\nu_\alpha}+O(t^{\nu_\alpha+2}),
```

avec la sélection impaire imposée par `K`.

Les secteurs sont regroupés hiérarchiquement en :

```text
TARGET_DIRECT
TARGET_WINDING
NON_TARGET_TRANSITION
```

pour `d < N/2`.

La quantité sectorielle intégrée est :

```math
P_\alpha(\tau)=\int_0^\tau \chi_\alpha(t)^2 dt.
```

On définit :

```math
P_{sector}(\tau)=\sum_\alpha P_\alpha(\tau),
```

et :

```math
Purity_{direct}(\tau)
=\frac{P_{direct}(\tau)}{P_{sector}(\tau)}.
```

Cette pureté est un indice de composition sectorielle. En général :

```math
P_{sector}(\tau)\neq\int_0^\tau \chi(t)^2dt
```

à cause des termes d'interférence entre secteurs dans la réponse totale.

## 2. Limite de court temps

Si :

```math
\nu_*=\min_\alpha \nu_\alpha,
```

alors :

```math
P_\alpha(\tau)
=\frac{c_\alpha^2}{2\nu_\alpha+1}\tau^{2\nu_\alpha+1}+\cdots.
```

Par conséquent :

```math
Purity_{direct}(0^+)
=
\frac{
\sum_{\alpha\in DIRECT,\,\nu_\alpha=\nu_*}c_\alpha^2
}{
\sum_{\beta,\,\nu_\beta=\nu_*}c_\beta^2
}.
```

La limite vaut exactement `1` si et seulement si les secteurs `TARGET_DIRECT` sont les seuls secteurs physiques actifs au plus petit exposant non nul.

### Arêtes `d=1`

Si le coefficient linéaire est régulier :

```math
\langle X_i\rangle\neq0,
```

alors `nu_*=1` et le seul secteur actif à cet ordre est `TARGET_DIRECT` :

```math
Purity_{direct}(0^+)=1.
```

Si le coefficient linéaire s'annule, cette conclusion n'est plus garantie.

### Distance `d=2`

Le premier commutateur opératoriel pertinent apparaît à ordre `2`, mais `K` annule la contribution physique paire. À ordre `3`, des secteurs `NON_TARGET_TRANSITION` peuvent déjà apparaître dans les commutateurs emboîtés. Il est donc interdit d'imposer analytiquement :

```math
Purity_{direct}(0^+)=1
```

pour `d=2` sans calcul sectoriel explicite des coefficients d'ordre `3`.

Le nombre :

```math
P_0^{pq}=Purity_{direct}(0^+)
```

est un oracle algébrique à calculer avant l'évolution temporelle.

## 3. Impureté cumulée monotone

La pureté instantanément intégrée n'a aucune raison d'être monotone en `tau`. On définit :

```math
I(\tau)=1-Purity_{direct}(\tau),
```

puis son enveloppe monotone :

```math
I_{max}(\tau)=\sup_{0<s\le\tau}I(s).
```

Cette enveloppe répond directement à la question : quelle est la plus grande impureté sectorielle déjà rencontrée avant l'événement ?

## 4. Variable de contrôle epsilon_path

Aucune valeur unique de `epsilon_path` n'est privilégiée.

Pour une valeur de contrôle `epsilon`, on définit :

```math
\tau_{pure}(\epsilon)
=\inf\{\tau>0: I_{max}(\tau)>\epsilon\}.
```

Cette définition est équivalente au premier franchissement de l'impureté et reste bien définie lorsque la pureté oscille.

Un événement temporel candidat `T_event` passe la garde pour une valeur de contrôle donnée si :

```math
T_{event}<\tau_{pure}(\epsilon),
```

ou, de manière équivalente :

```math
I_{max}(T_{event})\le\epsilon.
```

Si :

```math
\epsilon < 1-P_0^{pq},
```

alors aucun régime asymptotiquement aussi pur n'existe et `tau_pure(epsilon)=0` au sens de la garde.

## 5. Domaine de contrôle pré-enregistré

La suppression d'un seuil unique ne supprime pas l'obligation de pré-enregistrement.

La campagne devra déclarer avant inspection des courbes scientifiques :

```text
EPS_PATH_CONTROL_DOMAIN = OPEN
EPS_PATH_GRID           = OPEN
```

Le verdict d'interprétation doit être étudié sur toute cette famille de contrôle.

Une règle de robustesse naturelle est :

```text
ROBUST_CLEAN
    l'événement passe pour toute la famille de contrôle

ROBUST_NOT_ESTABLISHED
    l'événement échoue pour toute la famille de contrôle

CONTROL_SENSITIVE
    le verdict dépend de epsilon
```

`ROBUST_NOT_ESTABLISHED` n'est pas un échec de la réponse Kubo ; il signifie seulement que l'interprétation d'arrivée n'est pas établie dans le domaine de contrôle déclaré.

## 6. Contrôle de troncature

La courbe :

```math
I_{max}(\tau)
```

et/ou son inverse :

```math
\tau_{pure}(\epsilon)
```

doivent être publiées à `Lambda=2` et `Lambda=3` avec le même domaine de contrôle `epsilon`.

Il est interdit de modifier la grille ou le domaine de contrôle entre les deux cutoffs pour absorber une différence de troncature.

Le statut de robustesse de l'événement doit être comparé sur le même domaine de contrôle avant toute interprétation physique.

## 7. Relation avec la garde de récurrence

La garde de pureté sectorielle et la garde hystérétique de récurrence restent indépendantes.

Pour chaque événement :

```text
TIME_EVENT_VALID
    = PATH_CONTROL_ACCEPTABLE
      AND RECURRENCE_CONTROL_ACCEPTABLE
```

Les deux familles de contrôle (`epsilon_path` et `Gamma`) devront être pré-enregistrées et leurs sensibilités publiées.

## 8. Statut

```text
UNIVERSAL_PURITY_TO_ONE_ORACLE = REJECTED
EDGE_REGULAR_PURITY_TO_ONE     = VALIDATED_FOR_FREEZE
SHORT_PATH_PURITY_ORACLE       = VALIDATED_FOR_FREEZE
IMPURITY_MONOTONE_ENVELOPE      = VALIDATED_FOR_FREEZE
EPS_PATH_SINGLE_THRESHOLD       = NOT_REQUIRED
EPS_PATH_AS_CONTROL_VARIABLE    = VALIDATED_FOR_FREEZE
EPS_PATH_CONTROL_DOMAIN         = OPEN
EPS_PATH_GRID                   = OPEN
TRUNCATION_CONTROL              = MANDATORY
```
