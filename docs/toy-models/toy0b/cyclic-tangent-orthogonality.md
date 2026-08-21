# Toy Model 0B — orthogonalité cyclique exacte sur delta=0

Statut : **validé pour gel — support analytique**  
Source scientifique principale : `docs/toy-models/toy0b/specification.md`  
Supports liés : `symmetry-proof.md`, `parameter-campaign-structure.md`

Ce document élève au statut analytique l'orthogonalité entre la direction cyclique `D_Phi` et l'espace tangent de matière `S_n` sur toute la variété `delta=0`.

## 1. Tangentes

Pour tout opérateur hermitien `A`, on définit :

```math
D_A=-i[A,\rho_\theta].
```

En particulier :

```math
D_\Phi=-i[\Phi,\rho_\theta],
\qquad
D_{n_p}=-i[n_p,\rho_\theta].
```

et :

```math
S_n=\operatorname{span}\{D_{n_0},\ldots,D_{n_5}\}.
```

La preuve ci-dessous n'exige pas que `rho_theta` soit pure. Elle vaut également pour la prescription canonique dégénérée `rho=P_GS/Tr(P_GS)`, dès lors que le sous-espace fondamental est invariant sous les symétries exactes du Hamiltonien.

## 2. Action des symétries sur delta=0

Sur la variété :

```math
\delta=0,
```

la réflexion `R` est une symétrie exacte et :

```math
R\Phi R^\dagger=-\Phi,
\qquad
Rn_pR^\dagger=n_{-p}.
```

La symétrie `Q` reste exacte et :

```math
Q\Phi Q^\dagger=+\Phi,
\qquad
Qn_pQ^\dagger=1-n_{1-p}.
```

Comme `rho_theta` est invariant sous les symétries exactes du fond :

```math
RD_\Phi R^\dagger=-D_\Phi,
\qquad
RD_{n_p}R^\dagger=D_{n_{-p}},
```

et :

```math
QD_\Phi Q^\dagger=D_\Phi,
\qquad
QD_{n_p}Q^\dagger=-D_{n_{1-p}}.
```

## 3. Orthogonalité exacte

Posons :

```math
x_p=\langle D_\Phi,D_{n_p}\rangle_{HS}.
```

L'invariance du produit de Hilbert-Schmidt donne par `R` :

```math
x_p=-x_{-p},
```

et par `Q` :

```math
x_p=-x_{1-p}.
```

En appliquant la seconde relation à `-p` puis la première :

```math
x_p=x_{p+1}.
```

Les six `x_p` sont donc égaux.

Dans le secteur physique `N_f=3` :

```math
\sum_p n_p=3I,
```

et par conséquent :

```math
\sum_pD_{n_p}
=-i[3I,\rho_\theta]
=0.
```

Donc :

```math
\sum_px_p
=\left\langle D_\Phi,\sum_pD_{n_p}\right\rangle_{HS}
=0.
```

Comme tous les `x_p` sont égaux :

```math
\boxed{\langle D_\Phi,D_{n_p}\rangle_{HS}=0\quad\forall p.}
```

Ainsi :

```math
\boxed{D_\Phi\perp S_n\qquad(\delta=0).}
```

Cet énoncé est exact et ne dépend ni de la pureté du fondamental, ni d'un calcul numérique de covariance.

## 4. Forme covariance pour un fondamental pur

Si `rho=|Omega><Omega|` est pure, alors pour deux opérateurs hermitiens `A,B` :

```math
\langle D_A,D_B\rangle_{HS}
=\langle AB+BA\rangle
-2\langle A\rangle\langle B\rangle.
```

Si `A` et `B` commutent, cela devient :

```math
\langle D_A,D_B\rangle_{HS}
=2\,Cov_\rho(A,B).
```

Comme `Phi` et `n_p` sont diagonaux et commutent :

```math
\boxed{Cov_\rho(\Phi,n_p)=0\quad\forall p,\ \delta=0}
```

pour un fondamental pur.

Cette écriture est un corollaire de la preuve tangentielle plus générale, pas son hypothèse.

## 5. Décomposition exacte de S_E

Les contraintes de Gauss tangentielles donnent :

```math
D_{n_i}=D_{E_i}-D_{E_{i-1}}.
```

Et :

```math
D_\Phi=\frac16\sum_iD_{E_i}.
```

Les différences `D_{E_i}-D_{E_{i-1}}` engendrent la partie de coefficients de somme nulle, tandis que `D_Phi` porte la direction uniforme. Il en résulte structurellement :

```math
\boxed{S_E=S_n+\operatorname{span}\{D_\Phi\}.}
```

Sur `delta=0`, l'orthogonalité précédente donne :

```math
\boxed{S_E=S_n\oplus_\perp\operatorname{span}\{D_\Phi\}}
```

**si `D_Phi != 0`**.

Par conséquent :

```math
\dim S_E=
\begin{cases}
\dim S_n+1,&D_\Phi\neq0,\\
\dim S_n,&D_\Phi=0.
\end{cases}
```

Il est donc interdit de transporter automatiquement :

```text
dim S_E = 6
```

sur toute la variété `delta=0` sans vérifier :

```text
rank(S_n)=5
D_Phi != 0
```

au point considéré.

Au point de référence `(g,mu,delta)=(1,0,0)`, ces deux conditions sont qualifiées numériquement :

```text
rank(S_n)=5
||D_Phi||_HS ~= 0.249964384874506
```

et donc :

```math
\boxed{\dim S_E=6}
```

à la référence.

## 6. Hors de delta=0

Pour `delta != 0`, `R` n'est plus une symétrie du même fond. `Q` seul impose encore :

```math
x_p=-x_{1-p}.
```

Cette relation n'entraîne pas l'annulation individuelle des `x_p`.

Donc :

```text
D_Phi orthogonal S_n
```

n'est pas transportable hors de `delta=0`.

Les rangs et sous-espaces tangents doivent être recalculés à chaque point de campagne.

## 7. Statut

```text
D_PHI_SN_ORTHOGONAL_DELTA0       = VALIDATED_FOR_FREEZE
D_PHI_SN_ORTHOGONAL_MIXED_RHO    = VALIDATED_FOR_FREEZE
PURE_STATE_COVARIANCE_COROLLARY  = VALIDATED_FOR_FREEZE
S_E_DECOMPOSITION                = VALIDATED_FOR_FREEZE
S_E_ORTHOGONAL_SUM_DELTA0        = VALIDATED_FOR_FREEZE_IF_DPHI_ACTIVE
DIM_S_E_EQUALS_6_GLOBAL_DELTA0    = REJECTED
DIM_S_E_EQUALS_6_REFERENCE        = ESTABLISHED_NONCONFIRMATORY
OFF_DELTA0_ORTHOGONALITY          = NOT_ESTABLISHED
RANK_RECOMPUTE_EACH_CAMPAIGN_PT   = MANDATORY
```
