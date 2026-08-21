# Toy Model 0B — multigraduation de flux et secteurs de chemin

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne la séparation intrinsèque des composantes de transport par graduation des champs électriques. La graduation scalaire par `Phi` mémorise seulement le changement total de flux uniforme et ne suffit pas, à elle seule, à identifier un chemin topologique dans la réponse de Kubo complète.

Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale.

## 1. Graduations élémentaires

On définit :

```math
Phi = (1/6) sum_i E_i.
```

Pour le hopping orienté :

```math
h_i = c_i^\dagger U_i c_{i+1},
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

Les termes électriques et diagonaux de matière ont graduation nulle.

## 2. Multigraduation conjointe par les E_i

Les `E_i` commutent entre eux. Les superopérateurs :

```math
L_i(O)=[E_i,O]
```

commutent donc également et admettent une décomposition spectrale conjointe dans l'espace d'opérateurs fini.

On note :

```math
Pi_m,
```

avec :

```math
m=(m_0,...,m_5),
```

le projecteur conjoint défini par :

```math
[E_i,O_m]=m_i O_m.
```

Pour l'observable évoluée :

```math
n_q(t)=sum_m n_{q,m}(t),

n_{q,m}(t)=Pi_m n_q(t).
```

Cette décomposition est exacte et ne nécessite aucune énumération des mots de `ad_H^r`.

La graduation scalaire précédente n'est que :

```math
lambda(m)=(1/6)sum_i m_i.
```

Ainsi `ad_Phi` est un coarse-graining de la multigraduation par liens.

## 3. Signification de la multigraduation

Le vecteur `m` enregistre le changement net de flux lien par lien.

Un aller-retour sur un même lien ajoute `+1` puis `-1` et ne modifie donc pas `m`. Les insertions de termes diagonaux ne modifient pas non plus `m`.

Pour un transport ouvert déclaré entre deux extrémités fixées sur un cycle, deux chemins appartenant à des classes d'enroulement différentes diffèrent de :

```math
w*1,
```

avec :

```math
1=(1,1,1,1,1,1),
\qquad w\in Z.
```

Si `m_D` est le vecteur du chemin direct canonique :

```math
m_w=m_D+w*1.
```

L'arc complémentaire minimal correspond, avec la convention utilisée ici, à :

```math
m_W=m_D-1.
```

La projection scalaire donne :

```math
lambda(m_w)=d/6+w.
```

La réciproque est fausse : connaître seulement `lambda` ne détermine pas `m`.

## 4. Limite importante : réponse de Kubo complète

La multigraduation classe exactement les secteurs de changement net de flux de `n_q(t)`.

Elle ne doit pas être interprétée sans preuve supplémentaire comme affirmant que toute composante appartient nécessairement à la seule famille :

```math
{m_D+w*1 | w in Z}.
```

Des composantes différentes peuvent apparaître à temps fini et doivent être conservées comme secteurs non ciblés tant qu'une règle structurelle ne les exclut pas.

## 5. Hermiticité, canaux physiques et cas auto-conjugué

Si :

```math
[E_i,O_m]=m_i O_m,
```

alors :

```math
O_m^dagger=O_{-m}.
```

On définit :

```math
A_m^(pq)(t)
=Tr(rho [n_p, Pi_m n_q(t)]).
```

L'hermiticité donne :

```math
A_{-m}=-conj(A_m).
```

### 5.1 Canaux m != 0

Pour :

```math
m\neq0,
```

le canal physique est l'orbite à deux éléments :

```text
[m]={m,-m}.
```

Sa contribution réelle à la réponse est :

```math
chi_[m](t)
=i(A_m+A_{-m})
=-2 Im A_m.
```

Une grande valeur de `|A_m|` avec `Im A_m=0` ne contribue pas à `chi`; une contamination basée directement sur `|A_m|^2` est donc rejetée.

### 5.2 Canal auto-conjugué m=0

Le seul multigrade entier vérifiant :

```math
m=-m
```

est :

```math
m=0.
```

Dans une graduation générique, ce canal devrait être compté une seule fois, et non avec le facteur deux de la paire précédente.

Dans le secteur physique 0B, Gauss donne :

```math
n_i=b_i+E_i-E_{i-1}.
```

Le sextuplet `E` détermine donc entièrement `n`; les sous-espaces propres conjoints des six `E_i` sont unidimensionnels. Par conséquent :

```math
Pi_0(O)
```

est diagonal dans la base physique, et :

```math
[n_p,Pi_0(O)]=0.
```

Ainsi :

```math
\boxed{A_0^{pq}(t)=0}
```

et :

```math
\boxed{chi_[0]^{pq}(t)=0}
```

exactement.

Le canal auto-conjugué ne contribue donc pas à la réponse Kubo densité-densité de 0B et ne doit jamais être double-compté dans les poids sectoriels.

## 6. Cas d=1 et d=2

Pour une orientation canonique, le chemin direct et l'arc complémentaire ont des vecteurs distincts :

```math
m_W=m_D-1.
```

Ils ne sont pas adjoints l'un de l'autre pour `d<N/2`.

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

mais la séparation exacte repose sur les vecteurs `m`.

## 7. Cas opposé d=N/2

Pour `N=6,d=3`, avec un chemin direct supporté sur trois liens et l'arc complémentaire sur les trois autres :

```math
m_W=m_D-1,
```

et en général :

```math
m_W!= -m_D.
```

Les adjoints sont séparément :

```text
[m_D]={m_D,-m_D}
[m_W]={m_W,-m_W}.
```

La projection par `Phi` replie ces informations : le secteur scalaire `+1/2` peut contenir à la fois le chemin direct et l'adjoint du chemin complémentaire. La phase d'une amplitude scalaire `A_(+1/2)` ne peut donc pas être interprétée, à elle seule, comme une phase relative entre les deux arcs.

Le diagnostic `d=3` doit utiliser la multigraduation par liens pour tester séparément `[m_D]` et `[m_W]`.

Si leurs contributions d'ordre trois sont individuellement non nulles mais que leur somme s'annule, alors :

```text
D3_INTERFERENCE_MECHANISM = ESTABLISHED_AT_ORDER_3
```

sous réserve qu'aucun secteur non ciblé ne contribue au même ordre.

L'interprétation d'arrivée reste exclue pour `d=3`.

## 8. Diagnostic intégré de composition

Pour chaque canal physique distinct `alpha`, on utilise sa contribution réellement présente dans `chi` :

```math
P_alpha(tau)=integral_0^tau chi_alpha(t)^2 dt.
```

Les canaux `m != 0` sont indexés une seule fois par orbite `{m,-m}`. Le canal `m=0` est auto-conjugué mais possède exactement :

```math
P_[0](tau)=0.
```

On distingue :

```text
DIRECT
    canal [m_D]

WINDING
    canaux [m_D+w*1], w != 0

OTHER / NON_TARGET
    toutes les autres contributions physiques actives
```

On pose :

```math
P_ALL=P_DIRECT+P_WINDING+P_OTHER.
```

Puis :

```math
PURITY_DIRECT=P_DIRECT/P_ALL,
```

et :

```math
W=P_WINDING/P_ALL.
```

Ces ratios sont des diagnostics de composition sectorielle. En général :

```math
P_ALL != integral chi(t)^2 dt
```

car les canaux distincts peuvent interférer dans la réponse totale.

## 9. Garde pour l'interprétation d'arrivée

Pour `d=1,2`, un temps candidat `tau` ne peut recevoir une interprétation d'arrivée mono-chemin que si la composition sectorielle reste suffisamment dominée par le canal direct jusqu'à `tau`.

Le principe est :

```text
PATH_COMPOSITION_GUARD = REQUIRED
```

avec la famille de contrôle `epsilon_path` définie dans les supports dédiés.

Pour `d=3`, aucun temps d'arrivée mono-arc n'est autorisé, indépendamment de la séparabilité algébrique des deux arcs.

## 10. Troncature

Les relations de multigraduation restent exactes à cutoff fini pour les ladders tronqués déclarés.

En revanche la dynamique des secteurs, l'état de fond et leurs interférences dépendent du cutoff.

Aucune monotonie des poids sectoriels n'est supposée. Le verdict de robustesse exige le contrôle apparié :

```text
Lambda=2 -> Lambda=3.
```

## 11. Statut

```text
JOINT_E_GRADING                 = VALIDATED_FOR_FREEZE
PHI_SCALAR_GRADING              = VALIDATED_AS_COARSE_GRAINING
WORD_ENUMERATION                = NOT_REQUIRED
ADJOINT_PAIR_CHANNEL_M_NE_0     = VALIDATED_FOR_FREEZE
SELF_ADJOINT_CHANNEL_M_0        = IDENTIFIED
ZERO_GRADE_KUBO_CHANNEL         = INACTIVE_EXACT
ZERO_GRADE_DOUBLE_COUNTING      = REJECTED
D1_D2_LINK_SECTOR_SEPARATION    = VALIDATED_FOR_FREEZE
D3_LINK_SECTOR_SEPARATION       = VALIDATED_FOR_FREEZE
D3_PHI_PHASE_INTERPRETATION     = REJECTED
D3_ARRIVAL_INTERPRETATION       = EXCLUDED
PATH_COMPOSITION_GUARD          = VALIDATED_IN_PRINCIPLE
TRUNCATION_CONTROL              = MANDATORY
```
