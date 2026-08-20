# Toy Model 0B — portée spatiale de la garde de récurrence

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `recurrence-control.md`, `recurrence-order-domain.md`

Ce document fixe la portée spatiale normative de la garde locale de récurrence et précise le statut de la largeur minimale d'hystérésis du point permissif.

## 1. Nature du diagnostic local

Pour un site `j` et un fond stationnaire `rho_theta` :

```math
C_j(t)=
\frac{Re\,Tr[rho_\theta\,\delta n_j(t)\delta n_j]}
{Tr[rho_\theta(\delta n_j)^2]}.
```

Cette quantité est une autocorrélation locale d'équilibre. Elle n'est pas conditionnée par la source `p` de la réponse de Kubo.

Par conséquent, un retour de `C_j(t)` sur un site intermédiaire ne prouve pas qu'une excitation émise depuis `p` a traversé puis revisité ce site. Utiliser ce retour comme veto causal de chemin surinterpréterait une observable locale non conditionnée.

## 2. Ensemble normatif de sites

Pour la relation source-récepteur `(p,q)`, la garde de récurrence normative est évaluée uniquement sur :

```text
RECURRENCE_SITE_SET(p,q) = {p,q}
```

Les deux extrémités ont un statut opérationnel privilégié :

```text
p = site de source de la sonde Kubo
q = site récepteur de la sonde Kubo
```

Le site source contrôle la mémoire locale pouvant affecter une réexcitation/reconstruction au point d'injection ; le site récepteur contrôle la mémoire locale du point où le temps caractéristique est lu.

## 3. Sites intermédiaires

Pour `d>1`, les autocorrélations des sites intermédiaires de l'arc minimal peuvent être calculées et publiées comme diagnostics auxiliaires :

```text
INTERMEDIATE_RECURRENCE = DIAGNOSTIC_ONLY
```

Elles ne participent pas au verdict normatif :

```text
RECURRENCE_STATUS
```

et ne peuvent pas à elles seules invalider `T_grow` ou `T_thr`.

Un éventuel rebond interne au chemin direct est traité comme une caractéristique de la dynamique finie du canal direct, sauf s'il se manifeste par une contamination déjà couverte par une autre garde normative :

```text
- perte de pureté sectorielle / NON_TARGET_TRANSITION ;
- TARGET_WINDING ;
- récurrence détectée à p ou q ;
- sortie du premier lobe de la réponse elle-même.
```

## 4. Justification par portée du protocole

Le protocole primaire ne cherche pas à reconstruire une trajectoire microscopique ni un premier passage classique. Il définit un temps opérationnel à partir de la réponse source-récepteur `chi_pq(t)`.

Inclure tous les sites intermédiaires dans le veto de récurrence introduirait une condition de chemin plus forte que celle portée par la sonde elle-même et ferait dépendre le verdict d'autocorrélations locales qui ne sont pas causalement conditionnées par `p`.

Le choix `endpoints-only` est donc normatif et non implicite.

## 5. Cas d=1, d=2, d=3

### d=1

Il n'existe aucun site intermédiaire. La règle se réduit automatiquement à `{p,q}`.

### d=2

Le site intermédiaire de l'arc minimal peut être publié en diagnostic auxiliaire, mais ne participe pas à la garde normative d'arrivée.

### d=3

Le protocole d'arrivée mono-arc est déjà exclu structurellement. Les sites intermédiaires peuvent être étudiés dans le protocole secondaire d'interférence cyclique, mais la garde d'arrivée n'est pas réintroduite par leur autocorrélation.

## 6. Largeur minimale d'hystérésis du domaine Gamma

Le domaine de contrôle de récurrence est borné par :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm}.
```

Comme `gamma^perm` est le point le plus permissif valide, sa largeur :

```math
h_{min}=h(\gamma^{perm})
=\gamma_+^{perm}-\gamma_-^{perm}>0
```

est la plus petite largeur d'hystérésis autorisée dans le domaine ordonné.

Cette largeur minimale n'est donc pas supprimée par le passage d'un rectangle cartésien à un domaine ordonné. Elle est **relocalisée et rendue explicite** comme propriété déclarée du point permissif.

Une valeur plus petite de `h_min` rend le détecteur plus sensible aux recroisements faibles et tend à détecter plus facilement un retour ; une valeur plus grande tend à favoriser `ROBUST_CLEAN`. Le paramètre `h_min` doit donc être publié avec les bornes de `Gamma`.

## 7. Pas de diagnostic séparé h -> 0+

La frontière complète de la région :

```text
RETURN_BEFORE_EVENT
```

dans le plan `(gamma_-,gamma_+)` contient déjà l'information de sensibilité aux petites largeurs d'hystérésis.

Le diagnostic séparé :

```text
h -> 0+
```

n'est donc pas retenu comme item normatif distinct. Les petites valeurs de `h` peuvent apparaître dans la cartographie publiée si elles appartiennent au domaine préenregistré, mais elles ne constituent pas une observable ou un oracle séparé.

## 8. Statut

```text
RECURRENCE_SITE_SCOPE             = ENDPOINTS_ONLY
INTERMEDIATE_SITE_AUTOCORR        = DIAGNOSTIC_ONLY
INTERMEDIATE_SITE_VETO            = REJECTED
SOURCE_CONDITIONED_PATH_REPLAY     = NOT_INFERRED_FROM_LOCAL_AUTOCORR
HYSTERESIS_MIN_WIDTH              = EXPLICIT_AT_GAMMA_PERM
ZERO_WIDTH_LIMIT_SEPARATE_ITEM     = NOT_REQUIRED
RECURRENCE_BOUND_VALUES            = OPEN
```
