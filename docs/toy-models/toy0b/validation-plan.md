# Toy Model 0B — plan de validation et pré-enregistrement

Statut : **revue en cours**  
Spécification scientifique : `docs/toy-models/toy0b/specification.md`

Ce document décrit comment les décisions scientifiques de 0B devront être testées. Il sépare les oracles analytiques déjà connus, les calculs pilotes `Λ=1`, les mesures prospectives `Λ=2`, les contrôles `Λ=3` et les paramètres de protocole encore ouverts.

Aucune exécution scientifique 0B n'est autorisée tant que les paramètres marqués `OPEN` ne sont pas fermés et que le lot d'implémentation n'est pas explicitement autorisé.

---

## 1. Régimes

```text
REFERENCE_REGIME
    N = 6
    Λ = 2

TRUNCATION_CHECK
    N = 6
    Λ = 3

PILOT_REGRESSION
    N = 6
    Λ = 1
```

Le régime `Λ=1` ne fournit aucun résultat confirmatoire pour le régime scientifique de référence.

---

## 2. Catégories de résultats

Chaque sortie doit porter une catégorie explicite :

```text
STRUCTURAL_ANALYTIC
PILOT_LAMBDA1
PREREGISTERED_REFERENCE
TRUNCATION_CONTROL
EXTENDED_DIAGNOSTIC
```

Les catégories sont définies dans la spécification et dans le brouillon de gouvernance méthodologique : `features/scientific-method-governance.md`.

---

## 3. Oracles analytiques structurels

Ces valeurs ne sont pas prospectives ; elles doivent être vérifiées par le code comme tests de non-régression.

### A01 — comptage du secteur physique

Distribution attendue :

```text
spread = 0 -> 1 configuration
spread = 1 -> 16 configurations
spread = 2 -> 3 configurations
```

Formule :

```math
\dim\mathcal H_{\rm phys}(\Lambda)=40\Lambda-2.
```

Valeurs :

```text
Λ=1 -> 38
Λ=2 -> 78
Λ=3 -> 118
```

### A02 — états strictement intérieurs

```math
\dim\mathcal H_{\rm interior}(\Lambda)
=
\dim\mathcal H_{\rm phys}(\Lambda-1).
```

Donc :

```text
Λ=2 -> 38 intérieurs
Λ=3 -> 78 intérieurs
```

### A03 — rang des shifts cycliques

Pour :

```math
j=2\Lambda-k,
```

```math
r_\Lambda(L^k)
=
\sum_m
\max(0,j+1-\operatorname{spread}(m)).
```

Table compacte :

| `j` | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| rang | 1 | 18 | 38 | 58 | 78 | 98 |

### A04 — Gauss tangent

```math
D_i^{(E)}-D_{i-1}^{(E)}=D_i^{(n)}.
```

Conséquences structurelles :

```text
S_n subset S_E
dim S_n <= 5
dim S_E <= 6
```

### A05 — zéro-mode cyclique

```math
\Phi=\frac16\sum_iE_i,
```

```math
[\Phi,L]=L.
```

### A06 — orthogonalité collective au point `δ=0`

Sous réserve que les deux générateurs passent Gate 0 :

```math
\langle D_{\rm stag},D_\Phi\rangle_{HS}=0
```

et :

```math
\dim S_{\rm resp}^{\rm collective}=2.
```

Ce résultat n'est pas applicable automatiquement pour `δ != 0`.

### A07 — réflexion unitaire

Vérifier exactement les règles d'action déclarées :

```math
R c_j^\dagger R^\dagger=c_{-j}^\dagger,
```

à phase globale près sur `N_f=3`, ainsi que :

```math
R E_iR^\dagger=-E_{-i-1},
```

```math
R U_iR^\dagger=U_{-i-1}^\dagger.
```

### A08 — covariance de `R`

```math
R H(g,\mu,\delta)R^\dagger
=H(g,\mu,-\delta).
```

### A09 — symétrie `Q`

```math
Q=SR,
```

```math
[Q,H(g,\mu,\delta)]=0.
```

### A10 — action de `Q` sur les occupations

```math
Q n_pQ^\dagger=1-n_{1-p}.
```

Le commutateur de Kubo doit éliminer les constantes :

```math
[1-n_a,1-n_b(t)]=[n_a,n_b(t)].
```

---

## 4. Calculs pilotes `Λ=1`

Ces résultats sont déjà connus et servent uniquement de régression :

```text
rank(F_D)          = 6
rank(F_edge)       = 18
rank(F_path)       = 36
rank(F_loop^(1))   = 38
rank(L)            = 18
```

Toute reproduction de ces valeurs doit être marquée :

```text
RESULT_CLASS = PILOT_LAMBDA1
```

et non `PREREGISTERED_REFERENCE`.

---

## 5. Mesures prospectives `Λ=2`

Les quantités suivantes n'ont pas encore été calculées dans le régime de référence et pourront devenir confirmatoires après gel du protocole :

```text
rank(F_D)
rank(F_edge)
rank(F_path)
rank(F_loop^(1))
rank(F_loop^harm)
```

Ces rangs globaux sont des diagnostics instrumentaux et ne constituent pas le critère scientifique primaire.

Le rapport doit également publier les spectres singuliers pertinents, noyaux et conditionnements lorsqu'ils sont utilisés par un verdict pré-enregistré.

---

## 6. Gate 0 — activité de la référence

Pour chaque générateur déclaré `A` :

1. calculer `d_GS` ;
2. construire `P_GS` ;
3. calculer :

```math
[A,P_{GS}].
```

Si le commutateur est nul selon le critère numérique gelé :

```text
GENERATOR_ACTIVITY = INACTIVE
```

et aucune analyse d'identifiabilité n'est interprétée pour ce générateur.

Le rapport publie :

```text
generator
commutator_norm
d_GS
activity_status
```

---

## 7. Test statique ciblé

Pour les générateurs actifs, construire la base HS orthonormale de :

```math
S_{\rm resp}.
```

Pour chaque famille `F`, construire la matrice restreinte :

```math
M_{F|S}.
```

Publier :

```text
dim S_resp
rank(M_F|S)
dim restricted kernel
restricted singular spectrum
restricted conditioning
restricted kernel projector
```

Verdict :

```text
STATIC = PASS
    si S_resp intersect ker(M_F) = {0}

STATIC = FAIL
    sinon
```

Le `PASS` statique autorise le `PASS` dynamique par implication mathématique ; le `FAIL` statique n'implique pas un échec dynamique.

---

## 8. Test dynamique de Krylov

Ce test n'est exécuté que si :

```text
STATIC = FAIL
```

pour le domaine considéré.

Construire :

```math
W(F,H)=span{F,L_HF,L_H^2F,...}
```

jusqu'à stabilisation du rang du span.

Tester :

```math
S_{\rm resp}\cap W(F,H)^\perp.
```

Publier :

```text
krylov_span_dimension
stabilization_order
restricted_dynamic_kernel_dimension
dynamic_status
```

Verdict :

```text
DYNAMIC = PASS
    si l'intersection est nulle

DYNAMIC = FAIL
    sinon
```

`DYNAMIC = PASS` n'autorise que le protocole de réponse temporelle ; il ne vaut pas validation des temps caractéristiques ni de `C_eff`.

---

## 9. Réponse de Kubo

Pour chaque fond `theta=(g,mu,delta,...)` :

```math
\chi_{pq}^{(\theta)}(t)
=
i Tr[\rho_\theta [n_p,n_q^{(\theta)}(t)]].
```

La fonctionnelle utilisée est :

```math
F_{pq}^{(\theta)}(t)
=\chi_{pq}^{(\theta)}(t)^2/4.
```

Oracles immédiats :

```text
F_pq(0) = 0 pour p != q
0 <= F_pq(t) <= 1
```

Le protocole de validation doit vérifier que la source de Kubo `epsilon` n'est jamais confondue avec les paramètres du fond `theta`.

---

## 10. Développement de court temps

Pour chaque relation testée :

1. calculer le premier nested commutator opératoriel non nul ;
2. vérifier la borne structurelle issue de la localité ;
3. calculer les coefficients d'état `a_r` ;
4. déterminer `nu_state` comme premier coefficient d'état non nul.

Une valeur :

```text
nu_state > distance_graph
```

est autorisée et ne constitue pas automatiquement une erreur.

Pour les paires opposées `d=3`, le protocole doit conserver la possibilité préenregistrée d'une annulation par interférence des deux arcs minimaux.

---

## 11. Oracle `C_short`

Si :

```text
nu_ref = nu_state = nu
```

calculer algébriquement :

```math
C_short
=|a_state/a_ref|^(1/nu).
```

Puis vérifier que :

```math
C_eff^thr(eta) -> C_short
```

lorsque `eta` entre dans le régime asymptotique défini par le protocole final.

Le critère numérique de convergence reste :

```text
OPEN
```

jusqu'au gel des tolérances et de la grille `eta`.

Si les exposants diffèrent :

```text
SHORT_TIME_COMPARISON = NOT_APPLICABLE
D_thr                 = NOT_DEFINED
```

---

## 12. Temps de croissance

Sur la première montée :

```math
T_peak
```

est le premier maximum de `F`.

Puis :

```math
T_grow
=
inf argmax_{0<t<T_peak} dF/dt.
```

Le protocole numérique de localisation d'un argmax et le traitement des égalités / plateaux restent :

```text
OPEN
```

jusqu'au gel de l'échantillonnage temporel.

`T_grow` est l'estimateur temporel primaire.

---

## 13. Temps de seuil

Pour chaque `eta` de la grille pré-enregistrée :

```math
T_thr(eta)
```

est le premier franchissement montant avant `T_peak`.

La courbe complète :

```math
C_eff^thr(eta)
```

doit être conservée ; aucune valeur de `eta` ne peut être choisie a posteriori comme résultat privilégié.

La grille `eta` et son domaine admissible restent :

```text
OPEN
```

---

## 14. Diagnostic de récurrence et fenêtre temporelle

La référence étant stationnaire, la fidélité de l'état de référence n'est pas un diagnostic de récurrence utile.

On utilise une autocorrélation locale connectée :

```math
\delta n_q
=n_q-Tr(\rho_ref n_q)I,
```

```math
C_q(t)
=
Re Tr[\rho_ref \delta n_q(t)\delta n_q]
/
Tr[\rho_ref(\delta n_q)^2].
```

Une famille de niveaux :

```text
Gamma = OPEN
```

sera pré-enregistrée.

Pour chaque niveau `gamma`, le diagnostic identifiera un franchissement descendant puis le premier franchissement montant suivant.

La règle finale construisant `T_window^(pq)` à partir de ces niveaux reste :

```text
OPEN
```

mais elle devra être fixée avant inspection des courbes scientifiques.

Le premier lobe de réponse doit être contenu avant la fenêtre de récurrence. Si le protocole final ne peut pas établir cette séparation :

```text
TIME_WINDOW_STATUS = INCONCLUSIVE
```

---

## 15. Cohérence des deux estimateurs

`C_eff^grow` et `C_eff^thr(eta)` ne sont pas requis égaux numériquement.

Le protocole final doit définir avant calcul un critère de cohérence portant au minimum sur :

- le signe du contraste inter-orbites ;
- le classement des fonds lors d'un balayage paramétrique ;
- l'absence de contradiction systématique entre la montée finie et la famille de seuils admissibles.

Le critère formel final reste :

```text
OPEN
```

---

## 16. Contrôle nul de rééchelonnement

Pour :

```math
H_s=sH_ref,
```

on attend exactement :

```math
F_s(t)=F_ref(st),
```

et donc :

```math
C_eff^grow=s,
```

ainsi que :

```math
C_eff^thr(eta)=s
```

pour tout `eta` admissible.

Tous les contrastes logarithmiques inter-orbites doivent être nuls.

Ce contrôle est hors famille scientifique de fonds.

---

## 17. Oracle `Delta2`

Pour toute la campagne :

```math
Delta_2(g,mu,delta)=0.
```

Ce résultat est protégé par `Q = S R`.

Le test doit être appliqué séparément à :

```text
Delta2_grow
Delta2_thr(eta) pour tout eta de la grille admissible
```

Une violation au-delà de la tolérance gelée est :

```text
PIPELINE_OR_SYMMETRY_FAILURE
```

et non un résultat scientifique.

---

## 18. Signal primaire `Delta1`

Le signal scientifique primaire est :

```math
Delta_1(delta)
=
log(C_O1A(delta)/C_O1B(delta)).
```

Oracles exacts :

```math
Delta_1(0)=0,
```

```math
Delta_1(-delta)=-Delta_1(delta).
```

Ces identités doivent être testées pour :

```text
Delta1_grow
Delta1_thr(eta) pour chaque eta admissible
```

La campagne primaire doit être symétrique en `delta`.

La grille de valeurs :

```text
delta_grid = OPEN
```

reste à pré-enregistrer.

La susceptibilité :

```math
Xi_1=d Delta_1/d delta |_{delta=0}
```

est un diagnostic local seulement ; `Xi1=0` ne vaut pas `FAIL`.

---

## 19. Convention ordonnée source-récepteur

Les classes d'arêtes actuellement stabilisées sont des classes **non orientées** issues de l'analyse spatiale :

```text
{(0,1),(2,3),(4,5)}
{(0,5),(1,2),(3,4)}
```

La réponse de Kubo distingue une source `p` et un récepteur `q`.

Avant gel complet, il faut donc fixer explicitement :

```text
ORDERED_RELATION_CONVENTION = OPEN
```

Le protocole devra préciser :

- si une relation non orientée est représentée par un ordre canonique ;
- ou si les deux orientations sont calculées et combinées ;
- ou si une réciprocité exacte est démontrée et utilisée.

Aucune moyenne implicite ne sera autorisée.

---

## 20. Contrôle de troncature `Λ=2 -> 3`

Le contrôle principal utilise l'appariement opératoriel par `k`.

Pour les harmoniques présentes à `Λ=2` :

```text
k = 1,2,3,4
```

répéter à `Λ=3` les mêmes sondes et les mêmes fonds.

Publier harmonie par harmonie :

```text
support / rang
contribution au sous-espace ciblé
contribution au signal dynamique lorsqu'applicable
statut de convergence
```

L'appariement par :

```math
j=2Lambda-k
```

est calculé séparément comme diagnostic relatif au bord.

Les nouvelles harmoniques :

```text
k = 5,6 à Λ=3
```

sont classées :

```text
EXTENDED_DIAGNOSTIC
```

et ne contribuent pas au verdict principal de convergence du protocole `Λ=2`.

---

## 21. Groupe discret déclaré

Le plan de validation doit énumérer explicitement les transformations implémentées / vérifiées :

```text
T^2
C
S = T C
R
Q = S R
```

et les transformations composées nécessaires à l'action de stabilisateur.

Le rapport ne doit pas affirmer que ce groupe est mathématiquement exhaustif au-delà de ce qui a été démontré.

Tout verdict de contraste doit citer le groupe déclaré applicable.

---

## 22. Paramètres encore ouverts

Avant gel global du protocole dynamique, les éléments suivants doivent recevoir une valeur / règle exacte :

```text
ORDERED_RELATION_CONVENTION
Gamma
eta_grid
short_time_oracle_convergence_rule
time_window_rule
time_sampling_strategy
interpolation_or_root_finding_strategy
argmax_localization_rule
matrix_equalities_tolerance
rank_tolerance
singular_value_tolerance
symmetry_oracle_tolerance
Kubo_response_tolerance
truncation_comparison_tolerance
g_grid
mu_grid
delta_grid
estimator_consistency_rule
```

Aucun de ces paramètres ne doit être fixé après inspection des résultats scientifiques du régime `Λ=2`.

---

## 23. Verdicts autorisés

```text
PASS
FAIL
INCONCLUSIVE
INACTIVE
NOT_APPLICABLE
```

Chaque verdict est accompagné de son domaine complet.

Aucun `PASS` global du modèle n'est autorisé lorsque seule une sous-question a été validée.

---

## 24. Critère d'ouverture de l'implémentation

L'implémentation 0B reste :

```text
NOT_AUTHORIZED
```

jusqu'à ce que :

1. la spécification scientifique soit gelée ;
2. tous les paramètres du §22 affectant les résultats soient pré-enregistrés ;
3. ce plan de validation soit validé pour gel ;
4. Lionel ORCIL autorise explicitement le lot d'audit / implémentation ;
5. Claude Code reçoive un mandat conforme à la gouvernance de collaboration.
