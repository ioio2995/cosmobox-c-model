# Toy Model 0B — errata normatifs issus de l’audit de clôture

Statut : **correctifs normatifs pré-gel — aucun nouvel arbitrage physique**  
Branche : `documentation/model0b-foundation`

Ce document consigne uniquement les cinq défauts de consolidation établis par l’audit critique de clôture. Il ne crée aucune nouvelle branche scientifique. Jusqu’à leur intégration mécanique dans `specification.md` et `validation-plan.md`, les règles ci-dessous **supersèdent explicitement** toute formulation contradictoire de ces deux documents ou des supports antérieurs.

---

## E1 — familles de mesure et application de mesure

### Espace tangent et quotient par l’identité

Les rangs instrumentaux sont des rangs de fonctionnelles sur :

```math
\mathcal V=\{A=A^\dagger,\ \operatorname{Tr}A=0\}.
```

Pour toute observable `O`, sa composante identité est invisible sur `V`. On peut donc utiliser indifféremment :

```math
O
```

ou son représentant traceless :

```math
\widetilde O
=O-\frac{\operatorname{Tr}O}{d_{phys}}I.
```

Pour une famille ordonnée `F={O_mu}`, l’application de mesure est :

```math
\boxed{
\mathcal M_F(A)
=\bigl(\operatorname{Tr}(A\widetilde O_1),\ldots,
       \operatorname{Tr}(A\widetilde O_m)\bigr).
}
```

Le `rank(F)` pilote désigne le rang de cette application / du span des représentants traceless, jamais le nombre brut d’opérateurs listés.

En particulier, sur le secteur physique :

```math
n_i-b_iI=E_i-E_{i-1},
```

et le rang pilote :

```text
rank(F_D)=6
```

est cohérent avec :

```math
F_D=\{n_i,E_i\}_{i=0}^{5}
```

une fois l’identité quotientée par la restriction `Tr A=0`.

### Transport gauge-dressed le long d’un arc

Pour un arc simple orienté :

```text
P=(i_0,i_1,...,i_d)
```

on définit le transporteur de jauge `W_P` comme le produit ordonné des `U_i` lorsque l’arc suit l’orientation du lien et des `U_i^dagger` lorsqu’il la remonte.

Le transport ouvert est :

```math
T_P=c_{i_0}^\dagger W_P c_{i_d}.
```

Les deux quadratures hermitiennes sont :

```math
X_P=\frac{T_P+T_P^\dagger}{2},
\qquad
Y_P=\frac{T_P-T_P^\dagger}{2i}.
```

Une normalisation globale non nulle différente ne change pas le span ni les rangs.

### Familles exactes

```text
F_D
    {n_i,E_i}, i=0..5

F_edge
    F_D
    + {X_P,Y_P} pour les six arcs minimaux de distance 1

F_path
    F_edge
    + {X_P,Y_P} pour les six arcs minimaux uniques de distance 2
    + {X_P,Y_P} pour les deux arcs minimaux de chacune des trois paires opposées d=3

F_loop^(1)
    F_path + {X_L,Y_L}

F_loop^harm
    F_path + span_R{X_{L^k},Y_{L^k} | 1<=k<=2Lambda}
```

Pour une paire non orientée, inverser simultanément l’arc et ses extrémités envoie `T_P` sur `T_P^dagger`; cela ne crée donc pas une nouvelle paire de quadratures indépendante dans la famille.

Les valeurs pilotes `Lambda=1` :

```text
rank(F_D)        = 6
rank(F_edge)     = 18
rank(F_path)     = 36
rank(F_loop^(1)) = 38
```

sont des **rangs mesurés**, pas des comptages d’éléments de famille. Il est donc incorrect de reconstruire `rank(F_path)` par simple addition du nombre d’observables ajoutées.

---

## E2 — garde de pureté : normalisation relative

La garde normative n’est pas fondée sur une impureté absolue commune à tous les fonds.

On définit :

```math
P_0(\theta,\Lambda,pq)=Purity_{direct}(0^+),
```

```math
I_0(\theta)=1-P_0(\theta),
```

```math
I_{max}(\theta,\tau)
=\sup_{0<s\le\tau}\left[1-Purity_{direct}(\theta,s)\right].
```

Si :

```text
P_0 > 0
```

la dégradation supplémentaire normalisée est :

```math
\boxed{
R_{path}(\theta,\tau)
=\frac{I_{max}(\theta,\tau)-I_0(\theta)}{P_0(\theta)}.
}
```

La famille de contrôle commune est :

```text
epsilon in E_path subset (0,1)
```

et :

```math
\tau_{path}(\epsilon)
=\inf\{\tau>0:R_{path}(\tau)>\epsilon\}.
```

Un événement passe la garde pour `epsilon` si :

```math
R_{path}(T_{event})\le\epsilon.
```

Si :

```text
P_0 = 0
```

alors :

```text
PATH_BASELINE_STATUS = NO_DIRECT_BASELINE
```

et `R_path` n’est pas applicable.

À `d=1` régulier :

```text
P_0=1
I_0=0
```

et `R_path` se réduit à l’impureté enveloppée absolue.

À `d=2`, `P_0` n’est pas structurellement égal à 1 et doit être publié par domaine complet `(theta,Lambda,pq)`.

Contrôle obligatoire `Lambda=2 -> 3` avec la même grille `E_path` :

```text
P_0(theta)
W(0+)
O(0+)
R_path(theta,tau)
tau_path(theta,epsilon)
```

Toute formulation antérieure utilisant directement une grille commune sur `I_max` est **supersédée**.

---

## E3 — garde de récurrence : domaine ordonné et horizon événementiel

Pour chaque extrémité normative :

```text
RECURRENCE_SITE_SET(p,q) = {p,q}
```

on utilise l’autocorrélation locale connectée :

```math
C_j(t)=
\frac{\operatorname{Re}\operatorname{Tr}
[\rho_\theta\,\delta n_j(t)\delta n_j]}
{\operatorname{Tr}[\rho_\theta(\delta n_j)^2]}.
```

Si le dénominateur est nul :

```text
RECURRENCE_DIAGNOSTIC = NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
```

### Détecteur

Pour :

```math
\gamma=(\gamma_-,\gamma_+),
\qquad\gamma_-<\gamma_+<1,
```

et un horizon `tau`, les trois états exhaustifs sont :

```text
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
```

avec sortie lorsque `C_j<=gamma_-`, puis retour si `C_j>=gamma_+` après cette sortie et avant `tau`.

Pour la relation `(p,q)`, le statut de garde combine les deux extrémités ; un retour à l’une quelconque des extrémités compte comme retour avant événement.

### Horizon normatif

```text
T_grow       -> tau = T_peak
T_thr(eta)   -> tau = T_down(eta)
```

`T_down` est donc un auxiliaire obligatoire de la garde de récurrence des seuils et non un estimateur scientifique indépendant.

### Domaine Gamma retenu

L’ancien domaine rectangulaire :

```text
Gamma = G_- x G_+
```

est **supersédé**.

Le domaine normatif est un ensemble préenregistré contenu dans :

```math
\{(\gamma_-,\gamma_+):\gamma_-<\gamma_+<1\}
```

et borné dans l’ordre partiel :

```math
\gamma^{strict}\preceq\gamma\preceq\gamma^{perm},
```

avec :

```math
\gamma_-^{strict}\le\gamma_-\le\gamma_-^{perm},
\qquad
\gamma_+^{strict}\ge\gamma_+\ge\gamma_+^{perm}.
```

Le verdict robuste est :

```text
gamma_perm ne détecte aucun retour
    -> RECURRENCE_STATUS = ROBUST_CLEAN

gamma_strict détecte un retour
    -> RECURRENCE_STATUS = ROBUST_CONTAMINATED

sinon
    -> RECURRENCE_STATUS = CONTROL_SENSITIVE
```

La largeur :

```math
h(\gamma)=\gamma_+-\gamma_->0
```

est explicite. Le point permissif porte la largeur minimale positive du domaine préenregistré. `h=0` est exclu du contrôle principal.

Les sites intermédiaires sont `DIAGNOSTIC_ONLY` et ne participent pas au veto normatif.

---

## E4 — domaine exact de l’identité d’intérieur

L’identité structurelle correcte est :

```math
\dim\mathcal H_{interior}(\Lambda)
=\sum_n\max\bigl(0,2(\Lambda-1)+1-spread(n)\bigr).
```

Elle équivaut à :

```math
\dim\mathcal H_{interior}(\Lambda)
=\dim\mathcal H_{phys}(\Lambda-1)
```

si `H_phys(0)` est défini par le même comptage exact, donnant :

```text
Lambda=0 -> dim H_phys = 1
```

La forme fermée :

```math
\dim\mathcal H_{phys}(\Lambda)=40\Lambda-2
```

n’est valide que pour :

```text
Lambda >= 1
```

et ne doit donc pas être substituée à `Lambda-1` lorsque `Lambda=1`.

Valeurs de régression :

```text
Lambda=1 -> dim H_interior = 1
Lambda=2 -> dim H_interior = 38
Lambda=3 -> dim H_interior = 78
```

---

## E5 — vocabulaire des statuts

La liste `PASS / FAIL / INCONCLUSIVE / INACTIVE / NOT_APPLICABLE` décrit uniquement les **verdicts scientifiques généraux** et n’est pas exhaustive des statuts spécialisés.

Les statuts spécialisés explicitement autorisés incluent notamment :

```text
NOT_DEFINED
EXCLUDED
INACTIVE_EXACT
ZERO_EXACT
NOT_APPLICABLE_ZERO_LOCAL_VARIANCE
NO_DIRECT_BASELINE
NO_EXIT_BEFORE_EVENT
EXIT_NO_RETURN_BEFORE_EVENT
RETURN_BEFORE_EVENT
ROBUST_CLEAN
ROBUST_CONTAMINATED
CONTROL_SENSITIVE
TIME_EVENT_CONTROL_SENSITIVE
DERIVATIVE_CONTROL_SENSITIVE
SOFT_LOOP_STATIC_SUPPORTED
SOFT_LOOP_STATIC_DEVIATES
SOFT_LOOP_STATIC_NUMERICALLY_INCONCLUSIVE
```

Un statut spécialisé ne doit pas être remappé silencieusement vers `PASS` ou `FAIL`.

---

## Statut de l’audit après errata

Les cinq défauts établis par l’audit ont une correction normative définie ci-dessus. Cela **ne transforme pas** le verdict d’audit en `PASS` sans nouvelle vérification indépendante.

```text
CLOSURE_AUDIT_ORIGINAL = BLOCKED
BLOCKING_DEFECTS        = 5
ERRATA_DEFINED          = 5/5
IMPLEMENTATION_0B       = NOT_AUTHORIZED
```

Les éléments classés `NON_BLOCKING_BACKLOG` pendant l’audit ne sont pas développés dans le présent lot.