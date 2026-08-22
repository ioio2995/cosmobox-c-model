# Toy Model 0B — pureté de chemin et contrôle de l'interprétation d'arrivée

Statut : **validé pour gel — support analytique**
Source scientifique principale : `docs/toy-models/toy0b/specification.md`
Supports liés : `transition-fibers.md`, `path-grading.md`, `validation-plan.md`, `event-bandwidth-bracketing.md`

Ce document consigne la structure retenue pour la pureté sectorielle, la variable de contrôle normalisée `R_path`, sa grille préenregistrée `EPS_PATH_VALUES` et le protocole de certification continue de son extremum. Il ne remplace pas la spécification principale et devra être consolidé lors de la revue documentaire générale.

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

Cette pureté est un indice de composition sectorielle CUMULÉ et INCOHÉRENT. Ce n'est :

- ni une probabilité ;
- ni l'amplitude instantanée du chemin ;
- ni une décomposition additive de `chi^2` total.

En général :

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

De manière équivalente, en notant :

```math
Purity_{min}(\tau)=\inf_{0<s\le\tau}Purity_{direct}(s),
```

on a `I_max(tau)=1-Purity_min(tau)`.

## 4. Variable de contrôle normalisée `R_path`

Aucune valeur unique de `epsilon_path` n'est privilégiée.

La garde n'est **pas** fondée sur une impureté absolue commune à tous les fonds : elle porte sur la dégradation supplémentaire relative à la ligne de base `P_0^{pq}`. Avec :

```math
I_0=1-P_0^{pq},
```

et lorsque `P_0^{pq}>0` :

```math
R_{path}(\tau)
=\frac{I_{max}(\tau)-I_0}{P_0^{pq}}
=1-\frac{Purity_{min}(\tau)}{P_0^{pq}}.
```

Pour une valeur de contrôle `epsilon in (0,1)`, on définit :

```math
\tau_{path}(\epsilon)
=\inf\{\tau>0: R_{path}(\tau)>\epsilon\}.
```

Cette définition est équivalente au premier franchissement de la dégradation normalisée et reste bien définie lorsque la pureté oscille.

Un événement temporel candidat `T_event` passe la garde pour une valeur de contrôle donnée si :

```math
T_{event}<\tau_{path}(\epsilon),
```

ou, de manière équivalente :

```math
R_{path}(T_{event})\le\epsilon.
```

Si :

```math
P_0^{pq}=0,
```

alors :

```text
PATH_BASELINE_STATUS = NO_DIRECT_BASELINE
```

et `R_path` n'est pas applicable ; la garde de pureté ne rend aucun verdict pour ce couple.

À `d=1` régulier, `P_0^{pq}=1` et `I_0=0` : `R_path` se réduit à l'impureté enveloppée absolue `I_max`. À `d=2`, `P_0^{pq}` n'est pas structurellement égal à `1` et doit être publié par domaine complet `(theta,Lambda,pq)`.

### Domaine structurel de `R_path`

Comme `0<=Purity_direct(tau)<=1` (oracle générique déjà validé) et `0<=Purity_min(tau)<=P_0` par construction de l'infimum, la borne suit immédiatement :

```text
R_PATH_NORMALIZED_RANGE = STRUCTURAL_ANALYTIC
R_PATH_RANGE            = [0,1]
```

`epsilon` est une fraction de pureté sectorielle directe cumulée relative à la ligne de base initiale, **pas** un niveau de contamination d'amplitude.

## 5. Grille `EPS_PATH_VALUES` préenregistrée

La suppression d'un seuil unique (§4) ne supprime pas l'obligation de pré-enregistrement. La famille de contrôle normative est désormais fixée :

```text
EPS_PATH_VALUES     = {1/32, 1/16, 1/8, 1/4}
EPS_PATH_STRICT      = 1/32
EPS_PATH_PERMISSIVE  = 1/4
EPS_PATH_GRID_TYPE    = DYADIC_NORMALIZED_LOSS_FRACTION
```

Interprétation :

```math
R_{path}\le1/32 \iff Purity_{min}\ge\frac{31}{32}P_0,
```

```math
R_{path}\le1/4 \iff Purity_{min}\ge\frac34 P_0.
```

Ces valeurs sont des choix de robustesse de contrôle, pas des constantes fondamentales. Les points intérieurs `1/16` et `1/8` sont des diagnostics de sensibilité obligatoires. Le point permissif `1/4` sert uniquement à distinguer `ROBUST_CONTAMINATED` de `CONTROL_SENSITIVE` (§21) ; il n'est jamais moyenné avec le point strict.

## 6. Trichotomie de ligne de base — distincte de la dégradation

Pour chaque canal physique de chemin actif `alpha` :

```math
\chi_\alpha(t)=c_\alpha t^{\nu_\alpha}+O(t^{\nu_\alpha+2}).
```

Soit `nu_*` l'exposant dominant certifié minimum sur tous les canaux de chemin actifs. Définir :

```math
A_D^2=\sum_{\alpha\in DIRECT,\,\nu_\alpha=\nu_*}c_\alpha^2,
\qquad
A_S^2=\sum_{\alpha,\,\nu_\alpha=\nu_*}c_\alpha^2.
```

Lorsque `A_S^2>0` :

```math
P_0=A_D^2/A_S^2
```

(le facteur commun `1/(2 nu_*+1)` s'annule exactement).

Statut normatif de ligne de base :

```text
DIRECT_DOMINANT_BASELINE
    iff A_D^2 = A_S^2 > 0
    iff P_0 = 1

MIXED_BASELINE
    iff 0 < A_D^2 < A_S^2
    iff 0 < P_0 < 1

NO_DIRECT_BASELINE
    iff A_D^2 = 0 < A_S^2
    iff P_0 = 0
```

Si aucune réponse de chemin active n'existe à aucun ordre certifié :

```text
NO_ACTIVE_PATH_RESPONSE
```

Aucun seuil scalaire sur `P_0` n'est introduit.

Toute classification de zéro/non-zéro numérique non établie structurellement reste conditionnelle à :

```text
NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN.
```

## 7. Le statut de pureté n'est pas le statut d'arrivée propre

`PATH_CONTROL_STATUS` (§21) mesure uniquement la dégradation relative à la propre ligne de base `P_0` de chaque réponse.

Une interprétation confirmatoire d'arrivée propre côté chemin exige :

```text
PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE
    iff
    PATH_BASELINE_STATUS = DIRECT_DOMINANT_BASELINE
    AND
    PATH_CONTROL_STATUS = ROBUST_CLEAN
```

Ainsi :

```text
MIXED_BASELINE + ROBUST_CLEAN
```

signifie une composition mixte stable, **pas** une arrivée directe propre.

`NO_DIRECT_BASELINE` et `NO_ACTIVE_PATH_RESPONSE` ne sont jamais des passages d'arrivée propre.

L'interprétation complète d'un événement temporel exige en outre séparément la garde de récurrence (§24). Ce lot ne ferme pas `Gamma` (`GAMMA_CONTROL_DOMAIN_AND_GRID` reste `OPEN`).

## 8. Fonction exacte de certification de l'extremum : `H_path`

Définir :

```math
P_D(t)=P_{direct}(t),
\qquad
P_S(t)=P_{sector}(t),
```

```math
Q_D(t)=P_D'(t)=\sum_{\alpha\in DIRECT}\chi_\alpha(t)^2,
\qquad
Q_S(t)=P_S'(t)=\sum_{\alpha}\chi_\alpha(t)^2.
```

Pour une réponse active et `t>0` : `P_S(t)>0`. Donc :

```math
\frac{d}{dt}Purity_{direct}(t)=\frac{H_{path}(t)}{P_S(t)^2}
```

avec :

```math
\boxed{
H_{path}(t)=Q_D(t)P_S(t)-P_D(t)Q_S(t).
}
```

Normatif :

```text
PATH_EXTREMUM_CERTIFICATION_FUNCTION = H_path
```

Les points stationnaires intérieurs de `Purity_direct` sont exactement les racines de `H_path`.

## 9. Facteur oscillatoire et famille `beta` existante

Chaque `chi_alpha` a des fréquences spectrales `<=Omega_safe`. Donc :

- `Q_D`, `Q_S` contiennent des fréquences oscillatoires `<=2 Omega_safe` ;
- `P_D`, `P_S` contiennent des pièces séculaires linéaires plus des fréquences oscillatoires `<=2 Omega_safe` ;
- `H_path` contient des termes polynôme-fois-trigonométrique de degré `<=1` avec des fréquences oscillatoires `<=4 Omega_safe`.

Utiliser :

```text
PATH_CERTIFICATION_OSCILLATORY_FACTOR = 4
s_path = 4.
```

Réutiliser exactement :

```text
BETA_VALUES = {1, 1/2, 1/4, 1/8}.
```

Taille de cellule de certification de chemin initiale :

```math
\Delta t_k^{path}=\beta_k\frac{\pi}{4\Omega_{safe}}.
```

`s_path=4` est **uniquement** un facteur de fréquence oscillatoire pour le bracketing initial. `H_path` n'est **pas** traité comme un polynôme trigonométrique pur à bande limitée. La complétude provient de :

- l'exclusion de cellule par dérivée ;
- la subdivision adaptative ;
- l'exhaustion finie.

`ZERO_DENSITY` n'est jamais une preuve de complétude.

## 10. Bornes de dérivées pour `H_path`

Pour chaque canal `alpha` :

```math
S_{\alpha,r}=\sum_\omega |C_{\alpha,\omega}|\omega^r,
```

donc `|chi_alpha^(r)(t)| <= S_(alpha,r)`.

Pour un groupe `G` (direct `D` ou secteur complet `S`), définir :

```math
B_{G,0}=\sum_{\alpha\in G}S_{\alpha,0}^2,
```

```math
B_{G,1}=2\sum_{\alpha\in G}S_{\alpha,0}S_{\alpha,1},
```

```math
B_{G,2}=2\sum_{\alpha\in G}\left[S_{\alpha,1}^2+S_{\alpha,0}S_{\alpha,2}\right].
```

Alors :

```math
|Q_G|\le B_{G,0},
\qquad
|Q_G'|\le B_{G,1},
\qquad
|Q_G''|\le B_{G,2}.
```

Sur `[0,T]` :

```math
0\le P_G(t)\le T B_{G,0}.
```

Dérivées exactes :

```math
H_{path}'=Q_D'P_S-P_DQ_S',
```

```math
H_{path}''=Q_D''P_S+Q_D'Q_S-Q_DQ_S'-P_DQ_S''.
```

Bornes sûres :

```math
\boxed{
L_{path}(T)=T\left[B_{D,1}B_{S,0}+B_{D,0}B_{S,1}\right].
}
```

```math
\boxed{
L2_{path}(T)=T\left[B_{D,2}B_{S,0}+B_{D,0}B_{S,2}\right]+B_{D,1}B_{S,0}+B_{D,0}B_{S,1}.
}
```

Ces bornes ont été vérifiées indépendamment par revue Opus.

## 11. Problème structurel à l'origine

Le protocole générique de cellule de racine de `H_path` (§16) n'est **pas** appliqué à la cellule touchant `t=0`.

`H_path` possède un zéro structurel d'ordre élevé à l'origine. Sous la famille `K`-impaire :

```math
ord_0(H_{path})\ge4\nu_*+3\ge7
```

pour une correction de pureté non constante.

Un certificat générique de cellule vide/racine simple à Lipschitz global dégénère donc au voisinage de zéro et ne peut y établir la complétude. L'origine est traitée par la fenêtre analytique de court temps ci-dessous (§12-14).

## 12. Fenêtre analytique de court temps

Soit `beta_min=1/8`. Pour `Omega_safe>0`, définir, sans aucun nouveau scalaire :

```math
\boxed{
t_0=\beta_{min}\frac{\pi}{4\Omega_{safe}}=\frac{\pi}{32\Omega_{safe}}.
}
```

Si `Omega_safe=0` : il n'existe aucune réponse à fréquence de Bohr non nulle, et la réponse de chemin est traitée comme `NO_ACTIVE_PATH_RESPONSE` / cas structurel exact selon le cas.

L'intervalle `(0,t_0]` est certifié analytiquement (§13-14). Le protocole de cellule `H_path` (§16) n'est utilisé que sur `[t_0,T]`. Aucune cellule de certification de racine ne traverse zéro.

## 13. Certificat de Taylor explicite sur `(0,t_0]`

Soit `nu=nu_*`. Pour chaque canal `alpha`, définir :

```math
b_\alpha=\frac{S_{\alpha,\nu+2}}{(\nu+2)!}.
```

Pour un canal d'exposant dominant certifié `nu_alpha=nu`, la structure de Taylor à temps impair donne, pour `0<=t<=t_0` :

```math
\chi_\alpha(t)=c_\alpha t^\nu+r_\alpha(t),
\qquad
|r_\alpha(t)|\le b_\alpha t^{\nu+2}.
```

Pour un canal d'exposant dominant certifié `>nu`, l'imparité impose au moins `nu+2`, donc :

```math
|\chi_\alpha(t)|\le b_\alpha t^{\nu+2}.
```

Pour un groupe `G` (`D` ou `S`), définir :

```math
A_G^2=\sum_{\alpha\in G,\,\nu_\alpha=\nu}c_\alpha^2,
```

```math
C_{Q,G}
=\sum_{\alpha\in G,\,\nu_\alpha=\nu}\left[2|c_\alpha|b_\alpha+b_\alpha^2t_0^2\right]
+\sum_{\alpha\in G,\,\nu_\alpha>\nu}b_\alpha^2t_0^2.
```

Alors pour tout `0<=t<=t_0` :

```math
\left|Q_G(t)-A_G^2t^{2\nu}\right|\le C_{Q,G}t^{2\nu+2}.
```

En intégrant exactement, avec `m=2nu+1` :

```math
K_G=A_G^2/m,
\qquad
C_{P,G}=C_{Q,G}/(m+2),
```

et :

```math
\left|P_G(t)-K_Gt^m\right|\le C_{P,G}t^{m+2}.
```

Donc pour tout `0<t<=t_0` :

```math
\frac{P_G(t)}{t^m}\in\left[\max(0,K_G-C_{P,G}t_0^2),\;K_G+C_{P,G}t_0^2\right].
```

C'est un intervalle certifié UNIFORME sur toute la fenêtre d'origine.

## 14. Borne inférieure certifiée de pureté sur la fenêtre d'origine

Comme `A_S^2>0` pour une réponse active, définir :

```math
D_{low}=\max(0,K_D-C_{P,D}t_0^2),
\qquad
S_{high}=K_S+C_{P,S}t_0^2.
```

Alors :

```math
\boxed{
L_{Purity,origin}=D_{low}/S_{high}
}
```

est une borne inférieure rigoureuse de `Purity_direct(t)` pour tout `0<t<=t_0`. Aucune borne de dérivée sur `Purity` elle-même n'est nécessaire.

Pour une borne SUPÉRIEURE sur l'infimum sur la fenêtre d'origine, utiliser les valeurs candidates certifiées effectives :

```math
U_{Purity,origin}
=\min\left(P_{0,upper},\;Purity_{direct}(t_0)_{upper}\right).
```

Raison : l'infimum est `<=` à n'importe quelle valeur candidate effective.

Toutes les quantités numériques `_lower`/`_upper` doivent utiliser des enclosures certifiées à arrondi extérieur à la précision acceptée.

Si la classification requise d'exposant/coefficient/moment est non résolue :

```text
PATH_ORIGIN_WINDOW_CERTIFICATION_UNRESOLVED
```

et le verdict de chemin est `NONCONFIRMATORY`. Aucun rétrécissement post-hoc de `t_0` n'est autorisé.

## 15. Raccourci structurel exact `H_path` identiquement nul

Avant certification de racine, appliquer : si un oracle `STRUCTURAL_ANALYTIC` exact établit :

```math
H_{path}(t)\equiv0
```

sur le domaine actif, alors :

```math
Purity_{direct}(t)\equiv P_0,
\qquad
R_{path}(t)\equiv0,
```

pour tout `t` de l'horizon, et aucune certification de racine de `H_path` n'est requise.

Normatif :

```text
PATH_CONSTANT_COMPOSITION_ORACLE = STRUCTURAL_ANALYTIC
PATH_CONSTANT_COMPOSITION_R      = 0
```

Cas particulier suffisant obligatoire : si toutes les réponses de secteur non direct sont structurellement identiquement nulles, alors `P_D=P_S -> P_0=1 -> Purity_direct=1 -> R_path=0`.

Des identités proportionnelles de secteur plus générales ne peuvent utiliser ce raccourci que si elles sont prouvées structurellement, jamais inférées d'une coïncidence en virgule flottante.

## 16. Certification de cellule `H_path` sur `[t_0,T]`

Sur `[t_0,T]`, réutiliser le mécanisme de racine déjà validé avec `g=H_path`. Pour une cellule centrée `t_c`, demi-largeur `h` :

```text
CERTIFIED_EMPTY_CELL
    si |H_path(t_c)| > L_path(T) h.
```

Certificat de racine simple unique :

```text
|H_path'(t_c)| > L2_path(T) h.
```

Réutiliser exactement :

- `BETA_VALUES` ;
- `tau_root = 1e-12` ;
- `SIMPLE_ROOT_CONTROL` ;
- `DEGENERATE_ROOT_CONTROL` ;
- l'exhaustion de subdivision finie dérivée de `beta` et `tau_root`.

Aucune nouvelle tolérance de racine.

Toute cellule de `[t_0,T]` restant ni certifiée vide ni certifiée/résolue sous le protocole fail-closed existant donne :

```text
PATH_EXTREMUM_CERTIFICATION_UNRESOLVED
```

et donc :

```text
PATH_CONTROL_NUMERICALLY_INCONCLUSIVE.
```

## 17. Minimum de pureté certifié sur `[t_0,T]`

Pour chaque cellule de racine `H_path` certifiée `C=[a,b]` avec `t_0<=a<b`, et des intervalles `P` certifiés à arrondi extérieur, la monotonie de `P_D` et `P_S` donne :

```math
\frac{P_D(a)}{P_S(b)}\le Purity_{direct}(t)\le\frac{P_D(b)}{P_S(a)}
```

pour tout `t` de `C`.

Utiliser l'enclosure inférieure conservative :

```math
L_{Purity,cell}=\frac{P_D(a)_{lower}}{P_S(b)_{upper}}.
```

Valeur candidate supérieure : évaluer la pureté à l'estimation de racine certifiée avec enclosure `p/2p`.

Inclure l'extrémité `T` avec évaluation directe certifiée.

La borne inférieure du minimum sur `[t_0,T]` est :

```math
L_{Purity,late}
=\min\left(Purity(t_0)_{lower},\;Purity(T)_{lower},\;\text{toutes les }L_{Purity,cell}\right).
```

Une borne supérieure conservative de ce minimum est le minimum des évaluations candidates supérieures certifiées effectives : `t_0`, `T`, toutes les estimations de racine stationnaire certifiées.

Si un intervalle certifié bilatéral ne peut être formé :

```text
PATH_CONTROL_NUMERICALLY_INCONCLUSIVE.
```

## 18. Minimum de pureté continu global

Combiner la fenêtre d'origine `(0,t_0]` et la fenêtre tardive `[t_0,T]`. Définir :

```math
L_{Purity,min}=\min(L_{Purity,origin},L_{Purity,late}),
```

```math
U_{Purity,min}=\min(U_{Purity,origin},U_{Purity,late}).
```

Donc :

```math
Purity_{min}(T)\in\left[L_{Purity,min},\,U_{Purity,min}\right].
```

Aucun minimum sur grille échantillonnée n'est admis comme certificat.

```text
PATH_EXTREMUM_CONTINUOUS_CERTIFICATION = REQUIRED
PATH_SAMPLED_SUPREMUM_AS_CERTIFICATE   = REJECTED
```

## 19. Intervalle certifié de `R_path`

Pour `P_0>0` :

```math
R_{path}(T)=1-\frac{Purity_{min}(T)}{P_0}.
```

Construire un intervalle conservateur en utilisant les bornes `P_0` et `Purity_min` à arrondi extérieur. À `P_0` exact algébrique, ceci se réduit à :

```math
L_R=\max\left(0,\,1-\frac{U_{Purity,min}}{P_0}\right),
```

```math
U_R=\min\left(1,\,1-\frac{L_{Purity,min}}{P_0}\right).
```

Si `P_0` lui-même est numérique, l'arithmétique d'intervalle doit préserver les directions monotones correctes du quotient.

Évaluer la certification COMPLÈTE indépendamment à `p` et `2p`. Utiliser l'écart `p/2p` comme proxy numérique additionnel, jamais comme substitut au certificat continu.

Si les extrema/cellules ne peuvent être appariés de manière cohérente ou si l'échelle de précision acceptée est non résolue :

```text
PATH_CONTROL_NUMERICALLY_INCONCLUSIVE.
```

## 20. Incertitude de temps d'événement

Pour un événement certifié `T_e^(2p)` avec l'incertitude de coordonnée d'événement déjà existante `e_u` :

```math
e_t=\frac{\pi e_u}{s_{event}\Omega_{safe}}.
```

```math
t_-=\max(0,T_e^{(2p)}-e_t),
\qquad
t_+=T_e^{(2p)}+e_t.
```

Définir par continuité `R_path(0)=0`. Comme `R_path` est non décroissante :

```math
R_{path}(t_-)\le R_{path}(T_{true})\le R_{path}(t_+).
```

Les deux valeurs `R_path` aux extrémités DOIVENT utiliser la certification continue complète ci-dessus. Aucune borne de dérivée sur `R_path` elle-même n'est requise.

## 21. Classification epsilon et statut de robustesse

Pour chaque `epsilon in EPS_PATH_VALUES` :

```text
si U_R <= epsilon  -> PATH_EPSILON_PASS
si L_R > epsilon   -> PATH_EPSILON_FAIL
sinon              -> PATH_EPSILON_INCONCLUSIVE
```

Verdict de famille :

```text
U_R <= 1/32  -> PATH_CONTROL_STATUS = ROBUST_CLEAN
L_R > 1/4    -> PATH_CONTROL_STATUS = ROBUST_CONTAMINATED
sinon        -> PATH_CONTROL_STATUS = CONTROL_SENSITIVE
```

`ROBUST_CONTAMINATED` n'est pas un échec de la réponse Kubo ; il signifie que la dégradation normalisée dépasse le point permissif préenregistré.

Seul le point strict `1/32` peut soutenir une revendication confirmatoire d'arrivée propre côté chemin (§7). Les points intérieurs et le point permissif restent des diagnostics de sensibilité/robustesse, jamais une évidence indépendante.

## 22. Agrégation de dépendance

Le contrôle de chemin est LOCAL À L'ÉVÉNEMENT.

Pour une quantité dérivée `Q` :

- toute dépendance d'événement requise à `d=3` : `ARRIVAL_INTERPRETATION_FOR_Q = EXCLUDED` ;
- sinon, chaque dépendance d'événement requise doit avoir `DIRECT_DOMINANT_BASELINE` ET `ROBUST_CLEAN` pour une interprétation d'arrivée confirmatoire côté chemin.

Si un événement requis est `ROBUST_CONTAMINATED` : `PATH_CONTROL_FOR_Q = CONTAMINATED`.

Sinon, si aucun n'est contaminé mais qu'au moins un est `CONTROL_SENSITIVE`, `PATH_CONTROL_NUMERICALLY_INCONCLUSIVE`, `MIXED_BASELINE`, `NO_DIRECT_BASELINE` ou `NO_ACTIVE_PATH_RESPONSE` : `PATH_CONTROL_FOR_Q = NONCONFIRMATORY`.

Aucune moyenne entre dépendances.

## 23. Règle de cutoff / contrôle de troncature

Utiliser exactement la même `EPS_PATH_VALUES` à `Lambda=2` et `Lambda=3`. Les statuts de chemin locaux sont publiés séparément.

`ROBUST_CLEAN` aux deux cutoffs signifie uniquement une non-dégradation relative par rapport à la propre ligne de base de chaque cutoff. Cela ne prouve **pas** que `P_0` lui-même est stable au cutoff.

Une revendication d'arrivée propre stable au cutoff reste conditionnelle à :

```text
TRUNCATION_COMPARISON_TOLERANCES = OPEN.
```

Aucun rééchelonnement d'`epsilon` par cutoff.

## 24. Relation avec la garde de récurrence

La garde de pureté sectorielle et la garde hystérétique de récurrence restent indépendantes.

Pour chaque événement :

```text
TIME_EVENT_VALID
    = PATH_CONTROL_ACCEPTABLE
      AND RECURRENCE_CONTROL_ACCEPTABLE
```

Les deux familles de contrôle (`EPS_PATH_VALUES` et `Gamma`) doivent être pré-enregistrées et leurs sensibilités publiées. `GAMMA_CONTROL_DOMAIN_AND_GRID` et `RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS` restent `OPEN`.

## 25. Cas `d=3`

À `d=3` :

```text
ARRIVAL_INTERPRETATION = EXCLUDED
```

reste dominant. Le profil complet `P_0`/`R_path`/`epsilon` peut néanmoins être publié comme `DIAGNOSTIC_ONLY`. Même `DIRECT_DOMINANT_BASELINE` + `ROBUST_CLEAN` ne peut pas restaurer une interprétation d'arrivée à `d=3`.

## 26. Publication diagnostique

Publier par domaine complet `(theta,Lambda,pq,event)` :

```text
P_0
PATH_BASELINE_STATUS

nu_*
A_D^2
A_S^2

t_0
s_path

L_Purity_origin
U_Purity_origin

nombre de cellules/racines candidates H_path sur [t_0,T]
PATH_EXTREMUM_CERTIFICATION_STATUS

L_Purity_min
U_Purity_min

L_R
U_R

PATH_EPSILON_PROFILE pour {1/32, 1/16, 1/8, 1/4}

PATH_CONTROL_STATUS

PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE
```

Publier à `p/2p` les diagnostics complets d'écart de certification de chemin.

Pour les intégrales analytiques à fréquences quasi-égales, utiliser la forme stable :

```text
t * sinc((omega-omega')t)
```

plutôt que la division directe par `omega-omega'`. Ceci est une consigne de stabilité numérique d'implémentation, pas une nouvelle tolérance.

## 27. Statut

```text
UNIVERSAL_PURITY_TO_ONE_ORACLE          = REJECTED
EDGE_REGULAR_PURITY_TO_ONE              = VALIDATED_FOR_FREEZE
SHORT_PATH_PURITY_ORACLE                = VALIDATED_FOR_FREEZE
IMPURITY_MONOTONE_ENVELOPE              = VALIDATED_FOR_FREEZE
EPS_PATH_SINGLE_THRESHOLD               = NOT_REQUIRED
EPS_PATH_AS_CONTROL_VARIABLE            = VALIDATED_FOR_FREEZE
EPS_PATH_CONTROL_DOMAIN_AND_GRID        = VALIDATED_FOR_FREEZE

R_PATH_NORMALIZED_RANGE = STRUCTURAL_ANALYTIC
R_PATH_RANGE             = [0,1]

EPS_PATH_VALUES     = {1/32,1/16,1/8,1/4}
EPS_PATH_STRICT      = 1/32
EPS_PATH_PERMISSIVE  = 1/4
EPS_PATH_GRID_TYPE    = DYADIC_NORMALIZED_LOSS_FRACTION

PATH_BASELINE_STATUS =
DIRECT_DOMINANT_BASELINE | MIXED_BASELINE | NO_DIRECT_BASELINE | NO_ACTIVE_PATH_RESPONSE

PATH_CONTROL_STATUS =
ROBUST_CLEAN | CONTROL_SENSITIVE | ROBUST_CONTAMINATED

PATH_SIDE_CLEAN_ARRIVAL_ACCEPTABLE =
DIRECT_DOMINANT_BASELINE AND ROBUST_CLEAN

PATH_EXTREMUM_CERTIFICATION_FUNCTION  = H_path
PATH_CERTIFICATION_OSCILLATORY_FACTOR = 4
PATH_CERTIFICATION_BETA_VALUES        = EXISTING_BETA_VALUES

PATH_ORIGIN_WINDOW    = ANALYTIC_TAYLOR_CERTIFICATE
PATH_ORIGIN_WINDOW_T0 = pi/(32 Omega_safe)

PATH_EXTREMUM_CONTINUOUS_CERTIFICATION = REQUIRED
PATH_SAMPLED_SUPREMUM_AS_CERTIFICATE   = REJECTED

PATH_CONSTANT_COMPOSITION_ORACLE = STRUCTURAL_ANALYTIC

PATH_CONTROL_NEW_SCALAR_NUMERICAL_TOLERANCE = NONE

TRUNCATION_CONTROL = MANDATORY

NUMERICAL_ZERO_AND_SYMMETRY_TOLERANCES = OPEN
TRUNCATION_COMPARISON_TOLERANCES       = OPEN
GAMMA_CONTROL_DOMAIN_AND_GRID          = OPEN
RECURRENCE_HYSTERESIS_NUMERICAL_BOUNDS = OPEN
```
