# Toy Model 0B — domaine ordonné du contrôle de récurrence

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Support lié : `recurrence-control.md`

Ce document raffine le domaine de contrôle hystérétique afin de rendre explicite la largeur d'hystérésis sans imposer artificiellement un rectangle cartésien séparé du domaine physique `gamma_- < gamma_+`.

## 1. Détecteur

Un couple valide vérifie :

```math
\gamma=(\gamma_-,\gamma_+),
\qquad
\gamma_-<\gamma_+<1.
```

À événement `tau` fixé, `RETURN_BEFORE_EVENT` devient plus facile lorsque :

```text
gamma_- augmente

gamma_+ diminue
```

On définit l'ordre partiel :

```math
\gamma^{(1)}\preceq\gamma^{(2)}
```

si `gamma^(1)` est plus strict que `gamma^(2)`, c'est-à-dire :

```math
\gamma_-^{(1)}\le\gamma_-^{(2)},
\qquad
\gamma_+^{(1)}\ge\gamma_+^{(2)}.
```

Le prédicat `RETURN_BEFORE_EVENT` est monotone pour cet ordre.

## 2. Domaine de contrôle comme intervalle d'ordre

Il n'est pas nécessaire d'imposer :

```math
Gamma=G_-\times G_+
```

avec `max(G_-)<min(G_+)`.

Cette construction rectangle impose en effet une largeur minimale d'hystérésis :

```math
h_{min}=min(G_+)-max(G_-)>0,
```

qui devient elle-même un paramètre de contrôle.

La structure générale retenue est plutôt un domaine préenregistré `Gamma` contenu dans :

```math
\{(\gamma_-,\gamma_+):\gamma_-<\gamma_+<1\}
```

et borné dans l'ordre partiel par deux couples valides :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm}
\qquad
\forall\gamma\in\Gamma.
```

Le couple strict doit lui-même vérifier `gamma_-^strict < gamma_+^strict`, et le couple permissif :

```math
\gamma_-^{perm}<\gamma_+^{perm}<1.
```

Aucune hypothèse rectangulaire n'est requise sur l'intérieur de `Gamma`.

## 3. Verdict par deux bornes

La monotonie donne exactement :

```text
si gamma_perm ne détecte aucun retour
    -> ROBUST_CLEAN sur tout Gamma

si gamma_strict détecte un retour
    -> ROBUST_CONTAMINATED sur tout Gamma

sinon
    -> CONTROL_SENSITIVE
```

Les points intermédiaires servent uniquement à cartographier la frontière de sensibilité.

Le verdict robuste est donc indépendant de la densité de l'échantillonnage intérieur.

## 4. Largeur d'hystérésis explicite

On définit :

```math
h(\gamma)=\gamma_+-\gamma_->0.
```

La largeur d'hystérésis est une variable de contrôle explicite, pas un paramètre caché.

Le couple permissif peut être choisi avec une largeur faible afin d'approcher la limite d'un seuil simple, mais :

```math
h=0
```

n'appartient pas au protocole hystérétique principal. À largeur nulle, une recroisée infinitésimale du même niveau peut créer un retour immédiatement après la sortie, ce qui réintroduit exactement la sensibilité aux oscillations locales que l'hystérésis devait supprimer.

La limite :

```math
h\to0^+
```

peut être publiée comme diagnostic de sensibilité, mais ne doit pas être confondue avec un point physiquement privilégié.

## 5. Paramétrisation recommandée pour publication

En plus de `(gamma_-,gamma_+)`, il est utile de publier :

```math
h=\gamma_+-\gamma_-
```

ainsi que par exemple la profondeur de sortie :

```math
d_{out}=1-\gamma_-.
```

Cette reparamétrisation rend immédiatement visible si un changement de statut provient :

- d'une excursion minimale plus profonde ;
- d'une exigence de retour plus forte ;
- ou spécifiquement de la largeur d'hystérésis.

Elle ne remplace pas les niveaux `gamma_-` et `gamma_+` dans la définition normative.

## 6. Contrainte de l'autocorrélation

Pour le diagnostic connecté stationnaire déjà défini :

```math
|C_q(t)|\le1,
\qquad
C_q(0)=1.
```

La condition `gamma_+<1` évite d'imposer comme contrôle principal un retour exactement parfait à l'autocorrélation initiale.

Elle ne signifie pas à elle seule que le retour est « quasi complet » : ce qualificatif dépend de la valeur effectivement choisie pour `gamma_+`.

## 7. Statut

```text
RECURRENCE_PARTIAL_ORDER          = VALIDATED_FOR_FREEZE
TWO_BOUND_VERDICT                 = VALIDATED_FOR_FREEZE
RECTANGULAR_GAMMA_DOMAIN          = NOT_REQUIRED
HYSTERESIS_WIDTH_EXPLICIT         = VALIDATED_FOR_FREEZE
ZERO_WIDTH_PRIMARY_CONTROL        = REJECTED
ZERO_WIDTH_LIMIT_DIAGNOSTIC       = ALLOWED
GAMMA_BOUND_VALUES                = OPEN
GAMMA_INTERIOR_PUBLICATION_GRID   = OPEN
```
