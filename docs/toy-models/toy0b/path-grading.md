# Toy Model 0B — multigraduation de flux et secteurs de chemin

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne la séparation intrinsèque des composantes de transport par graduation des champs électriques. Il corrige une formulation antérieure trop forte : la graduation scalaire par `Phi` mémorise seulement le changement total de flux uniforme et ne suffit pas, à elle seule, à identifier un chemin topologique dans la réponse de Kubo complète.

Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale.

## 1. Graduations élémentaires

On définit :

```math
Phi = (1/6) sum_i E_i.
```

Pour le hopping orienté :

```math
h_i = c_i^dagger U_i c_{i+1},
```

les relations tronquées restent exactes :

```math
[E_j,h_i] = delta_{ij} h_i,
[E_j,h_i^dagger] = -delta_{ij} h_i^dagger.
```

Donc :

```math
[Phi,h_i] = (1/6) h_i,
[Phi,h_i^dagger] = -(1/6) h_i^dagger.
```

Les termes électriques et les termes diagonaux de matière ont graduation nulle.

## 2. Multigraduation conjointe par les E_i

Les `E_i` commutent entre eux. Les superopérateurs :

```math
L_i(O) = [E_i,O]
```

commutent donc également et admettent une décomposition spectrale conjointe dans l'espace d'opérateurs fini.

On note :

```math
Pi_m,
```

avec :

```math
m = (m_0,...,m_5),
```

le projecteur conjoint défini par :

```math
[E_i,O_m] = m_i O_m
```

pour tout `i`.

Pour l'observable évoluée :

```math
n_q(t) = sum_m n_{q,m}(t),

n_{q,m}(t) = Pi_m n_q(t).
```

Cette décomposition est exacte et ne nécessite aucune énumération des mots de `ad_H^r`.

La graduation scalaire précédente n'est que la projection :

```math
lambda(m) = (1/6) sum_i m_i.
```

Ainsi `ad_Phi` est un coarse-graining de la multigraduation par les liens.

## 3. Signification de la multigraduation

Le vecteur `m` enregistre le changement net de flux lien par lien.

Un aller-retour sur un même lien ajoute `+1` puis `-1` sur ce lien et ne modifie donc pas `m`. Les insertions de termes diagonaux ne modifient pas non plus `m`.

Pour un transport ouvert déclaré entre deux extrémités fixées sur un cycle, deux chemins appartenant à des classes d'enroulement différentes diffèrent de :

```math
w * 1,
```

où :

```math
1 = (1,1,1,1,1,1),

w in Z.
```

Si `m_D` est le vecteur de graduation du chemin direct canonique, les classes d'enroulement de cette famille sont donc :

```math
m_w = m_D + w * 1.
```

L'arc complémentaire minimal correspond, avec la convention utilisée ici, à :

```math
m_W = m_D - 1.
```

La projection scalaire donne alors :

```math
lambda(m_w) = d/6 + w.
```

Cette relation explique la formule scalaire antérieure, mais la réciproque est fausse : connaître seulement `lambda` ne détermine pas le vecteur `m`.

## 4. Limite importante : la réponse de Kubo complète

La multigraduation classe exactement les secteurs de changement net de flux de `n_q(t)`.

Elle ne doit toutefois pas être interprétée sans preuve supplémentaire comme affirmant que toute composante de la réponse de Kubo appartient nécessairement à la seule famille :

```math
{m_D + w*1 | w in Z}.
```

Dans la réponse de densité complète, des composantes de multigraduation différentes peuvent apparaître à temps fini. Elles doivent être conservées et rapportées comme secteurs `OTHER` tant qu'une règle structurelle ne les a pas exclues.

Il est donc interdit de confondre :

```text
multigraduation de flux exacte
```

avec :

```text
décomposition exhaustive en deux chemins géométriques.
```

Cette distinction est particulièrement importante pour l'interprétation d'un temps d'arrivée fini.

## 5. Hermiticité et canaux physiques

Si :

```math
[E_i,O_m] = m_i O_m,
```

alors :

```math
O_m^dagger = O_{-m}.
```

On définit :

```math
A_m^(pq)(t)
=
Tr(rho [n_p, Pi_m n_q(t)]).
```

L'hermiticité donne exactement :

```math
A_{-m} = -conj(A_m).
```

La contribution réelle du couple adjoint `{m,-m}` à la réponse de Kubo est donc :

```math
chi_[m](t)
=
i(A_m + A_{-m})
=
-2 Im A_m.
```

La quantité physique élémentaire du diagnostic est donc la paire adjointe :

```text
[m] = {m,-m},
```

et non une composante signée isolée.

Une grande valeur de `|A_m|` avec `Im A_m = 0` ne contribue pas à `chi`. Une norme de contamination basée directement sur `|A_m|^2` est donc rejetée pour le diagnostic physique de `WRAP_CLEAN`.

## 6. Cas d=1 et d=2

Pour une orientation canonique, le chemin direct et l'arc complémentaire ont des vecteurs de graduation distincts :

```math
m_W = m_D - 1.
```

Ils ne sont pas adjoints l'un de l'autre pour `d < N/2`.

Les deux canaux physiques :

```text
[m_D]
[m_W]
```

sont donc algébriquement distincts et projetables séparément.

Leur projection scalaire sous `Phi` reproduit :

```text
d=1 : +1/6 versus -5/6

d=2 : +1/3 versus -2/3
```

mais la séparation topologique exacte repose sur les vecteurs `m`, pas sur ces seuls nombres scalaires.

## 7. Cas opposé d=N/2

La coïncidence scalaire :

```math
lambda_D = +1/2,

lambda_W = -1/2
```

est générale pour une paire opposée sur un cycle pair.

Cependant elle ne signifie pas que les deux arcs sont adjoints au niveau de la multigraduation de liens.

Pour `N=6, d=3`, avec un chemin direct supporté sur trois liens et l'arc complémentaire sur les trois autres :

```math
m_W = m_D - 1,
```

et en général :

```math
m_W != -m_D.
```

Les adjoints sont séparément :

```text
[m_D] = {m_D,-m_D}
[m_W] = {m_W,-m_W}.
```

La projection par `Phi` replie ces informations : le secteur scalaire `+1/2` peut contenir à la fois le chemin direct et l'adjoint du chemin complémentaire. La phase d'une amplitude scalaire `A_{+1/2}` ne peut donc pas être interprétée, à elle seule, comme une phase relative entre les deux arcs.

Le diagnostic `d=3` doit utiliser la multigraduation par liens pour tester séparément les deux canaux physiques `[m_D]` et `[m_W]`.

Si leurs contributions d'ordre trois sont individuellement non nulles mais que leur somme s'annule, alors :

```text
D3_INTERFERENCE_MECHANISM = ESTABLISHED_AT_ORDER_3
```

sous réserve qu'aucun secteur `OTHER` ne contribue au même ordre.

Si l'annulation du coefficient total est observée uniquement après projection scalaire par `Phi`, le mécanisme reste :

```text
D3_INTERFERENCE_MECHANISM = NOT_ESTABLISHED
```

Toute interprétation ultérieure de type Aharonov-Bohm reste conditionnée à une dépendance démontrée au degré cyclique et à la robustesse `Lambda=2 -> Lambda=3`.

## 8. Diagnostic intégré de composition

Pour chaque canal physique `[m]`, on utilise la contribution réellement présente dans `chi` :

```math
chi_[m](t) = -2 Im A_m(t).
```

Une mesure intégrée évite les singularités dues aux zéros instantanés :

```math
P_[m](tau) = integral_0^tau chi_[m](t)^2 dt.
```

On distingue conceptuellement :

```text
DIRECT
    canal [m_D]

WINDING
    canaux [m_D + w*1], w != 0

OTHER
    toutes les autres paires de multigraduation présentes
```

La contamination d'enroulement peut être rapportée par :

```math
W_pq(tau)
=
P_WINDING(tau) / P_ALL(tau),
```

avec :

```math
P_ALL = P_DIRECT + P_WINDING + P_OTHER.
```

La pureté du canal direct peut également être rapportée :

```math
PURITY_DIRECT(tau)
=
P_DIRECT(tau) / P_ALL(tau).
```

Ces ratios sont des diagnostics de composition sectorielle. Ils ne sont pas égaux à une décomposition additive de `chi(t)^2`, car les contributions de canaux différents peuvent interférer dans la réponse totale.

Les seuils d'acceptation restent ouverts :

```text
WRAP_TOLERANCE          = OPEN
OTHER_SECTOR_TOLERANCE  = OPEN
```

Si `P_ALL = 0`, le canal est `INACTIVE` pour ce diagnostic.

## 9. Garde pour l'interprétation d'arrivée

Pour `d=1,2`, un temps candidat `tau` ne peut recevoir une interprétation d'arrivée mono-chemin que si la composition sectorielle reste suffisamment dominée par le canal direct jusqu'à `tau`.

Le principe est :

```text
PATH_COMPOSITION_GUARD = REQUIRED
```

avec au minimum :

```text
WINDING contamination sous tolérance
OTHER contamination sous tolérance
```

Les normes intégrées sont fixées dans leur principe ; les tolérances restent à pré-enregistrer.

Pour `d=3`, aucun temps d'arrivée mono-arc n'est autorisé, indépendamment de la séparabilité algébrique des deux arcs, car les deux chemins minimaux apparaissent au même ordre temporel.

## 10. Troncature

Les relations :

```math
[E_j,U_i] = delta_{ij} U_i
```

et la multigraduation restent exactes à cutoff fini pour les ladders tronqués déclarés.

En revanche la dynamique des secteurs, l'état de fond et leurs interférences dépendent du cutoff.

Aucune monotonie de `W_pq`, de `PURITY_DIRECT` ou des composantes `d=3` n'est supposée.

Le verdict de robustesse exige le contrôle apparié :

```text
Lambda=2 -> Lambda=3.
```

## 11. Statut

```text
JOINT_E_GRADING                = VALIDATED_FOR_FREEZE
PHI_SCALAR_GRADING             = VALIDATED_AS_COARSE_GRAINING
WORD_ENUMERATION               = NOT_REQUIRED
D1_D2_LINK_SECTOR_SEPARATION   = VALIDATED_FOR_FREEZE
D3_LINK_SECTOR_SEPARATION      = VALIDATED_FOR_FREEZE
D3_PHI_PHASE_INTERPRETATION    = REJECTED
D3_ARRIVAL_INTERPRETATION      = EXCLUDED
PATH_COMPOSITION_GUARD         = VALIDATED_IN_PRINCIPLE
WRAP_TOLERANCE                 = OPEN
OTHER_SECTOR_TOLERANCE         = OPEN
TRUNCATION_CONTROL             = MANDATORY
```
