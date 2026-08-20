# Toy Model 0B — support analytique des oracles de court temps

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Plan de validation : `docs/toy-models/toy0b/validation-plan.md`

Ce document consigne les conséquences analytiques de la symétrie antiunitaire `K` et du développement de Kubo à court temps. Il devra être consolidé dans la spécification et le plan de validation lors de la revue documentaire générale précédant le gel final de 0B.

## 1. Parité temporelle imposée par K

Dans la base occupation-flux, `H`, `rho` et les occupations `n_i` sont réels pour la famille de fonds déclarée. La conjugaison complexe `K` vérifie donc :

```math
K H K^{-1}=H,
\qquad
K \rho K^{-1}=\rho,
\qquad
K n_i K^{-1}=n_i.
```

Comme `K` est antiunitaire :

```math
K i K^{-1}=-i,
\qquad
K n_q(t)K^{-1}=n_q(-t).
```

Pour :

```math
\chi_{pq}(t)=i\,\mathrm{Tr}\!\left(\rho[n_p,n_q(t)]\right),
```

on obtient :

```math
\chi_{pq}(-t)=-\chi_{pq}(t).
```

Par conséquent :

```math
\mathcal F_{pq}(t)=\chi_{pq}(t)^2/4
```

est paire en temps.

Le développement de `chi` ne contient que des puissances impaires :

```math
\chi_{pq}(t)=a_1t+a_3t^3+a_5t^5+\cdots.
```

## 2. Règle de sélection sur l'exposant d'état

La localité impose au niveau opératoriel :

```math
[n_p,\mathrm{ad}_H^r(n_q)]=0
\quad\text{pour}\quad r<d(p,q).
```

La parité temporelle ajoute, pour les fonds `K`-invariants, que les coefficients d'ordre pair sont nuls dans l'espérance de Kubo.

Le premier exposant d'état possible satisfait donc :

```math
\nu_{\rm state}
\ge
\min\{r\ge d(p,q)\mid r\text{ impair}\}.
```

Table structurelle :

```text
d = 1 -> nu_state >= 1
d = 2 -> nu_state >= 3
d = 3 -> nu_state >= 3
```

Pour les paires opposées `d=3`, si le coefficient d'ordre 3 s'annule par interférence des deux arcs minimaux, alors la règle de parité impose :

```text
nu_state >= 5
```

et non seulement `nu_state > 3`.

## 3. Relations non orientées

La stationnarité donne :

```math
\chi_{qp}(t)=-\chi_{pq}(-t).
```

Avec l'imparité temporelle imposée par `K` :

```math
\chi_{qp}(t)=\chi_{pq}(t).
```

Donc :

```math
\mathcal F_{qp}(t)=\mathcal F_{pq}(t),
```

et les temps `T_grow` et `T_thr(eta)` sont identiques sous échange de la source et du récepteur. Pour le protocole 0B, les relations `(p,q)` sont donc traitées comme non orientées.

## 4. Oracle linéaire sur une arête

Pour une arête `i -> i+1`, on définit :

```math
h_i=c_i^\dagger U_i c_{i+1},
\qquad
X_i=h_i+h_i^\dagger.
```

Le Hamiltonien contient le hopping `-J sum_i X_i`. On a :

```math
[n_i,[H,n_{i+1}]]=-JX_i.
```

Le développement de la réponse de Kubo donne alors :

```math
\chi_{i,i+1}(t)
=J\langle X_i\rangle_\rho\,t+O(t^3).
```

Avec la convention `J=1` :

```math
a_1^{(i,i+1)}=\langle X_i\rangle_\rho.
```

Cet oracle est calculable par diagonalisation et valeurs moyennes, sans évolution temporelle.

## 5. Oracle court-terme du contraste primaire

Lorsque les coefficients linéaires des deux orbites d'arête restent non nuls, `nu=1` pour ces canaux et :

```math
C_{\rm short}^{(1,A)}
=\left|\frac{\langle X\rangle_{A,\mathrm{state}}}
              {\langle X\rangle_{A,\mathrm{ref}}}\right|,
```

```math
C_{\rm short}^{(1,B)}
=\left|\frac{\langle X\rangle_{B,\mathrm{state}}}
              {\langle X\rangle_{B,\mathrm{ref}}}\right|.
```

À la référence `delta=0`, la réflexion échange les deux orbites et impose :

```math
\langle X\rangle_{A,\mathrm{ref}}
=
\langle X\rangle_{B,\mathrm{ref}}.
```

Donc :

```math
\Delta_1^{\rm short}(\delta)
=
\log\left|
\frac{\langle X\rangle_{A,\delta}}
     {\langle X\rangle_{B,\delta}}
\right|.
```

La covariance de réflexion implique également :

```math
\Delta_1^{\rm short}(-\delta)
=-\Delta_1^{\rm short}(\delta).
```

Cette identité constitue un oracle statique préalable au test dynamique end-to-end.

## 6. Gate de régularité court-terme

La formule précédente n'est applicable que si les coefficients linéaires concernés sont non nuls dans la référence et dans le fond comparé.

Si, pour une orbite d'arête :

```math
\langle X\rangle=0,
```

alors le terme linéaire s'annule et la règle de parité impose :

```text
nu_state >= 3
```

pour ce canal.

Le verdict est alors :

```text
EDGE_SHORT_ORACLE = NOT_APPLICABLE
```

et non `FAIL`. Le protocole dynamique peut rester actif ; il doit déterminer le nouvel exposant et appliquer les règles générales de comparaison des exposants.

La notion de zéro numérique et les tolérances restent `OPEN` jusqu'au gel des tolérances numériques.

## 7. Hiérarchie scientifique des quantités Delta1

La limite de petit seuil ne doit pas être présentée comme résultat de propagation. Elle reproduit un contraste de valeur moyenne du hopping dans le fond considéré.

La hiérarchie validée pour gel est :

```text
Delta1_short
    oracle algébrique / statique au sens calculable sans évolution
    aucune interprétation de temps d'arrivée

Delta1_thr(eta)
    famille complète de seuils finis
    doit tendre vers Delta1_short dans le régime asymptotique lorsque les exposants concordent

Delta1_dyn_thr(eta)
    = Delta1_thr(eta) - Delta1_short
    contraste de la partie quittant le régime court

Delta1_grow
    observable scientifique temporelle primaire
    extraite de la montée finie
```

En termes des corrections par paire :

```math
D_{pq}^{\rm thr}(\eta)
=
\log\frac{C_{\rm eff,pq}^{\rm thr}(\eta)}{C_{{\rm short},pq}},
```

on a, pour les deux orbites d'arête :

```math
\Delta_{1,\rm dyn}^{\rm thr}(\eta)
=
D_A^{\rm thr}(\eta)-D_B^{\rm thr}(\eta)
=
\Delta_1^{\rm thr}(\eta)-\Delta_1^{\rm short}.
```

Cette quantité n'est définie que lorsque les comparaisons `C_short` correspondantes sont elles-mêmes applicables.

## 8. Conséquence pour les seuils et fenêtres

Comme :

```math
\mathcal F(t)\sim t^{2\nu},
```

les départs minimaux sont :

```text
d=1 -> F(t) ~ t^2 si a1 != 0
d=2 -> F(t) ~ t^6 ou ordre supérieur
d=3 -> F(t) ~ t^6 ou ordre supérieur
```

Pour un régime asymptotique `F ~ B t^(2 nu)` :

```math
T_{\rm thr}(\eta)\sim(\eta/B)^{1/(2\nu)}.
```

Donc la sensibilité logarithmique au seuil est :

```math
\frac{d\log T_{\rm thr}}{d\log\eta}=\frac1{2\nu}.
```

Les canaux `nu=3` sont ainsi moins sensibles fractionnellement à `eta` que les canaux `nu=1`. Leur temps absolu de franchissement n'est toutefois pas ordonné par cette seule loi, car le coefficient `B` dépend du canal et du fond.

Le protocole devra donc définir des domaines admissibles de `eta` et des validations de fenêtre séparés par classe de relation / exposant, tout en utilisant un domaine commun par intersection lorsque plusieurs courbes sont comparées dans un même contraste.
