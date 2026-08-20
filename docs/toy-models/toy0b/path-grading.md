# Toy Model 0B — graduation par Φ et secteurs d'enroulement

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne le mécanisme intrinsèque de séparation topologique des contributions de propagation par graduation sous `ad_Φ`. Il remplace l'idée d'un étiquetage combinatoire des mots de commutateurs emboîtés. Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale.

## 1. Graduation élémentaire

On définit :

```math
\Phi=\frac16\sum_i E_i.
```

Pour le hopping orienté :

```math
h_i=c_i^\dagger U_i c_{i+1},
```

la relation tronquée reste exacte :

```math
[E_i,U_i]=U_i,
```

et donc :

```math
[\Phi,h_i]=\frac16 h_i,
\qquad
[\Phi,h_i^\dagger]=-\frac16 h_i^\dagger.
```

Les termes électriques et les termes diagonaux de matière ont graduation nulle.

Ainsi `ad_Φ=[Φ,·]` fournit une graduation intrinsèque de l'algèbre d'opérateurs, indépendante de tout découpage arbitraire de `H` en termes locaux.

## 2. Projection spectrale de ad_Φ

Comme `Φ` est hermitien dans l'espace physique fini, le superopérateur `ad_Φ` est diagonalisable. On note :

```math
\Pi_\lambda
```

le projecteur sur l'espace propre :

```math
[\Phi,O_\lambda]=\lambda O_\lambda.
```

Pour l'observable évoluée :

```math
n_q(t)=\sum_\lambda n_{q,\lambda}(t),
\qquad
n_{q,\lambda}(t)=\Pi_\lambda n_q(t).
```

Cette décomposition est exacte ; elle ne nécessite pas l'énumération des mots de `ad_H^r`.

## 3. Classe d'enroulement entière

Pour une relation orientée canonique `(p,q)`, on choisit la graduation `lambda_0` du chemin minimal déclaré. Sur le cycle à six sites, avec la convention d'orientation de `h_i`, on peut écrire :

```math
\lambda_w=\lambda_0+w,
\qquad
w\in\mathbb Z.
```

Le nombre entier `w` est la classe d'enroulement sur le revêtement universel du cycle.

Pour une paire dont l'arc minimal déclaré a longueur `d<=3` :

```math
\lambda_0=d/6,
```

et l'arc complémentaire minimal correspond à :

```math
\lambda_{-1}=d/6-1.
```

Les allers-retours ajoutés à une histoire ne changent pas la graduation nette et restent donc automatiquement dans la même classe `w`.

Les insertions de termes de graduation nulle ne changent pas non plus la classe.

La graduation remplace donc l'étiquetage combinatoire de chemins.

## 4. Relations non orientées et hermiticité

Le protocole de propagation traite `(p,q)` et `(q,p)` comme la même relation, mais la séparation topologique exige une orientation canonique interne.

Si :

```math
[\Phi,O_\lambda]=\lambda O_\lambda,
```

alors :

```math
O_\lambda^\dagger=O_{-\lambda}.
```

Les composantes de graduation opposée sont donc reliées par hermiticité. Elles sont algébriquement séparables par `Pi_lambda`, mais ne doivent pas être présentées comme deux observables réelles indépendantes.

La réponse physique réelle est reconstruite après sommation des composantes conjuguées appropriées.

## 5. Cas d=1 et d=2

Pour `d=1`, les deux arcs minimaux ont les graduations signées :

```text
arc direct        : +1/6
arc complémentaire: -5/6
```

avec leurs composantes adjointes de signe opposé.

Pour `d=2` :

```text
arc direct        : +1/3
arc complémentaire: -2/3
```

avec leurs composantes adjointes.

Les classes sont donc séparables à la fois temporellement à court temps et algébriquement par `ad_Φ`, sous réserve des annulations de coefficients d'état déjà préenregistrées.

## 6. Cas d=3

Pour une paire opposée :

```text
arc 1 : +1/2
arc 2 : -1/2
```

Les deux arcs minimaux contribuent au même ordre temporel possible `t^3`. Il n'existe donc aucun régime d'arrivée mono-arc séparé temporellement.

En revanche les composantes signées `+1/2` et `-1/2` restent séparables par projection de `ad_Φ`.

Comme elles sont adjointes, leur mécanisme d'interférence doit être analysé par leurs amplitudes complexes / phases relatives, et non comme la somme de deux réponses réelles indépendantes.

Le diagnostic secondaire `d=3` doit distinguer au minimum :

```text
- disparition individuelle des deux composantes ;
- composantes non nulles dont la recombinaison annule le coefficient total d'ordre 3.
```

Si le second mécanisme est observé, la hausse de l'exposant d'état vers `nu>=5` est attribuable à une interférence entre les deux secteurs topologiques plutôt qu'à l'inactivité du canal.

Toute interprétation ultérieure de type Aharonov-Bohm reste conditionnée aux critères déjà préenregistrés : dépendance au degré cyclique, variation contrôlée sous le paramètre pertinent et robustesse `Lambda=2 -> 3`.

## 7. Décomposition de la réponse

Pour chaque graduation, on peut définir une amplitude projetée :

```math
A_\lambda^{(pq)}(t)
=
Tr\left(\rho\,[n_p,\Pi_\lambda n_q(t)]\right).
```

La réponse totale est reconstruite exactement par :

```math
\chi_{pq}(t)
=
i\sum_\lambda A_\lambda^{(pq)}(t).
```

Les amplitudes `A_lambda` peuvent être complexes ; seule la réponse totale est requise réelle.

Pour `d=1,2`, la classe directe correspond à la classe de zéro enroulement déclarée et toutes les classes d'enroulement non nulles constituent la contamination topologique pour l'interprétation d'arrivée.

## 8. Garde quantitative d'enroulement

Le concept suivant est validé : la contamination doit être évaluée à partir des composantes projetées exactes, et non à partir du seul ordre de Taylor.

Une forme intégrée sur `[0,tau]` est privilégiée afin d'éviter les singularités dues aux zéros instantanés des amplitudes directes.

Une quantité de type :

```math
W_{pq}(\tau)
=
\frac{
\sum_{\lambda\in\Lambda_{wrap}}
\int_0^\tau |A_\lambda(t)|^2dt
}{
\sum_{\lambda\in\Lambda_{all}}
\int_0^\tau |A_\lambda(t)|^2dt
}
```

est le candidat naturel.

Cette formule fixe la structure du diagnostic, mais les éléments suivants restent ouverts :

```text
WRAP_NORM_DEFINITION = OPEN
WRAP_TOLERANCE       = OPEN
```

Si le dénominateur est nul, le canal est `INACTIVE` pour ce diagnostic et non en échec numérique.

Pour `d=3`, cette garde n'est pas utilisée pour autoriser un temps d'arrivée ; les deux arcs minimaux appartiennent constitutivement au protocole d'interférence cyclique.

## 9. Troncature

La relation :

```math
[E_i,U_i]=U_i
```

et donc la graduation par `ad_Φ` restent exactes à cutoff fini pour les opérateurs ladder tronqués déclarés.

En revanche la dynamique des composantes n'est pas neutre vis-à-vis de la troncature. Les secteurs de grand enroulement peuvent être bloqués au bord, mais la troncature modifie aussi l'état de fond, les composantes directes et leurs interférences.

Il est donc interdit d'affirmer que la troncature rend `WRAP_CLEAN` automatiquement conservateur.

Le verdict de robustesse exige le contrôle apparié :

```text
Lambda=2 -> Lambda=3
```

selon les règles de troncature déjà préenregistrées.

## 10. Statut

```text
PHI_GRADING                 = VALIDATED_FOR_FREEZE
INTEGER_WINDING_CLASSES     = VALIDATED_FOR_FREEZE
WORD_ENUMERATION            = NOT_REQUIRED
D1_D2_TOPOLOGICAL_SEPARATION = VALIDATED_FOR_FREEZE
D3_SIGNED_GRADE_SEPARATION  = VALIDATED_FOR_FREEZE
D3_ARRIVAL_INTERPRETATION   = EXCLUDED
WRAP_INTEGRATED_DIAGNOSTIC  = VALIDATED_IN_PRINCIPLE
WRAP_NORM_DEFINITION        = OPEN
WRAP_TOLERANCE              = OPEN
TRUNCATION_CONTROL          = MANDATORY
```
