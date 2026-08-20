# Proposition de gouvernance de méthode scientifique

Statut : **revue en cours**  
Destination prévue après validation : `docs/governance/scientific-method-governance.md`

Ce document est placé temporairement dans `features/` conformément à la gouvernance documentaire : il propose des règles transverses non encore gelées. Après validation explicite, son contenu devra être migré vers `docs/governance/` et les gouvernances gelées qui référencent l'arborescence / l'ordre de lecture devront être mises à jour dans un paquet normatif distinct.

---

## 1. Objet

Cette gouvernance proposée fixe les règles de méthode scientifique et expérimentale communes aux modèles du dépôt `cosmobox-c-model`.

Elle ne définit aucune physique particulière. Elle encadre :

- le pré-enregistrement ;
- la séparation entre oracles, pilotes et résultats prospectifs ;
- la formulation des questions d'identifiabilité ;
- les conditions de modification d'une famille de sondes ;
- l'analyse des symétries et résultats nuls ;
- les verdicts `PASS / FAIL / INCONCLUSIVE / INACTIVE` ;
- les contrôles de troncature ;
- la portée des interprétations.

---

## 2. Principe de pré-enregistrement

Une grandeur destinée à porter un verdict scientifique doit être définie avant son calcul sur le régime de référence.

Le pré-enregistrement porte au minimum sur :

- la question testée ;
- le sous-espace / les directions physiques ciblées ;
- les observables ou sondes utilisées ;
- les paramètres de fond ;
- les contrôles ;
- les critères de verdict ;
- les tolérances nécessaires ;
- les règles de comparaison entre régimes.

Une valeur ou un protocole déjà calculé avant le gel n'est pas caché : il est déclaré comme pilote et ne peut pas être présenté ensuite comme résultat confirmatoire dans le même régime.

---

## 3. Catégories de provenance scientifique

Tout résultat significatif doit être classé selon sa provenance.

```text
STRUCTURAL_ANALYTIC
    conséquence démontrée avant calcul scientifique
    oracle exact ou borne structurelle

PILOT
    résultat déjà observé avant pré-enregistrement
    utilisable pour faisabilité / régression
    non confirmatoire dans le même régime

PREREGISTERED_REFERENCE
    résultat calculé seulement après gel du protocole
    dans le régime scientifique de référence

TRUNCATION_CONTROL
    répétition appariée dans un espace / cutoff élargi

EXTENDED_DIAGNOSTIC
    nouvelle sonde ou nouveau degré accessible uniquement
    dans le régime élargi ; hors verdict principal de convergence
```

Une conséquence analytique connue ne doit jamais être présentée comme découverte numérique.

---

## 4. Domaine obligatoire d'un verdict

Un verdict ne doit jamais circuler sans son domaine de validité.

Selon le modèle, le rapport doit publier au minimum les composantes pertinentes du tuple :

```text
modèle
troncature / taille
Hamiltonien / paramètres de fond
état ou règle de préparation
famille d'observables
sous-espace de réponse / directions ciblées
dimension du sous-espace ciblé
groupe de transformations déclaré
protocole numérique / tolérances
```

Un `PASS` sur un sous-espace faible dimension n'est jamais transférable à une perturbation ou une famille non testée.

Les formulations du type :

```text
MODEL = PASS
```

sont interdites lorsqu'elles masquent un domaine plus restreint.

---

## 5. Interdiction de sauvetage post-hoc

Après observation d'un `FAIL`, d'un noyau ou d'un défaut d'identifiabilité, il est interdit d'enrichir implicitement la famille de sondes jusqu'à obtenir le résultat attendu.

Toute nouvelle observable proposée après inspection des résultats constitue :

1. une nouvelle famille ;
2. une nouvelle hypothèse instrumentale ;
3. un nouveau pré-enregistrement ;
4. un nouveau verdict indépendant.

Le résultat négatif initial est conservé.

---

## 6. `span` linéaire et algèbre engendrée

Une famille de sondes `F` désigne son `span` linéaire explicitement déclaré, pas l'algèbre complète engendrée par ses éléments.

```math
\operatorname{span}(F)\neq\operatorname{Alg}(F).
```

Les produits, puissances, projecteurs spectraux et conditionnements ne sont disponibles que s'ils figurent explicitement dans la famille pré-enregistrée.

Une famille dite mono-mode peut contenir les sondes canoniques et harmoniques explicitement déclarées pour un même degré de liberté. Cette qualification n'autorise aucune fermeture algébrique implicite.

Un produit qui croise ou conditionne plusieurs modes déclarés distincts constitue une **observable composite inter-modes** et doit appartenir à une famille distincte.

---

## 7. Identifiabilité ciblée plutôt que tomographie par défaut

L'injectivité globale sur l'espace complet des matrices de densité n'est pas un objectif par défaut.

Pour une application de mesure :

```math
\mathcal M_F:\mathcal V\to\mathbb R^m,
```

la question scientifique doit d'abord nommer les directions physiques que l'étape suivante cherche réellement à exciter ou distinguer.

On définit un sous-espace ciblé :

```math
S_{\rm resp}\subseteq\mathcal V.
```

Le test pertinent est alors :

```math
S_{\rm resp}\cap\ker\mathcal M_F.
```

Le rang global de `M_F` peut rester un diagnostic d'indépendance instrumentale, mais il n'est pas un indicateur universel de réussite scientifique.

---

## 8. Gate d'activité avant identifiabilité

Pour un générateur `A` appliqué à une référence `rho_ref`, le protocole doit vérifier que la perturbation annoncée agit réellement sur la référence.

Pour une référence construite depuis un projecteur spectral `P` :

```math
[A,P]=0
```

implique que le kick unitaire associé laisse exactement la référence inchangée.

Le statut est alors :

```text
INACTIVE
```

et non `PASS`.

Un sous-espace de réponse de dimension nulle ne peut jamais produire un verdict positif d'identifiabilité.

---

## 9. Visibilité individuelle et injectivité collective

Une direction `D` est individuellement visible si :

```math
\|\mathcal M_F(D)\|>0.
```

Mais toutes les directions nominales peuvent être individuellement visibles tout en étant collectivement confondues par la mesure.

Le protocole doit donc distinguer :

```text
VISIBILITY
    direction par direction

INJECTIVITY
    sur le span complet des directions ciblées
```

Aucune visibilité individuelle ne remplace le calcul du noyau restreint lorsque le protocole exige de distinguer des combinaisons de directions.

---

## 10. Statique et dynamique

Lorsque l'observabilité dynamique est définie par le span de Krylov :

```math
\mathscr W(F,H)
=
\operatorname{span}
\{F,\mathcal L_HF,\mathcal L_H^2F,\ldots\},
```

on a :

```math
\operatorname{span}(F)\subseteq\mathscr W(F,H).
```

Donc un `PASS` statique sur le sous-espace ciblé est suffisant pour le `PASS` dynamique.

```text
STATIC PASS
    -> DYNAMIC PASS

STATIC FAIL
    -> dynamique encore indéterminée
       calcul du Krylov requis
```

Cette implication ne vaut pas pour des observables non linéaires extraites ensuite de la trajectoire, notamment les temps de franchissement ou les argmax.

---

## 11. Barrières distinctes pour les quantités dérivées

L'identifiabilité d'une trajectoire `G(t)` ne garantit pas l'identifiabilité ni la robustesse d'une fonctionnelle non linéaire extraite de cette trajectoire.

Un protocole dynamique doit donc séparer au minimum :

```text
STATE / RESPONSE IDENTIFIABILITY
DYNAMIC OBSERVABILITY
DERIVED-QUANTITY IDENTIFIABILITY
INTERPRETATION
```

Un `PASS` à une étape n'autorise que l'étape suivante explicitement prévue.

---

## 12. Recherche des résultats nuls avant conception du signal

Avant de pré-enregistrer un contraste comme signal, le protocole doit rechercher les résultats nuls exacts imposés par les transformations connues du secteur physique.

La procédure recommandée est :

1. déclarer un ensemble discret de transformations pertinentes ;
2. calculer leur action sur le secteur physique ;
3. calculer leur action sur les paramètres du Hamiltonien ;
4. construire le stabilisateur du point / de la famille ;
5. inclure les transformations composées ;
6. calculer l'action du stabilisateur sur les observables et relations comparées ;
7. reclasser tout contraste échangé par le stabilisateur comme oracle nul.

Le fait qu'un terme ajouté brise plusieurs générateurs pris séparément ne suffit pas : un composé peut subsister et interdire exactement le signal recherché.

---

## 13. Groupe déclaré et révocabilité d'une interprétation

La documentation ne doit parler de « groupe complet » que si l'exhaustivité a été démontrée.

Sinon elle utilise :

```text
stabilisateur dans le groupe discret pré-déclaré
et exhaustivement énuméré pour le protocole
```

Un signal non nul reste donc interprétable relativement à ce groupe déclaré.

La découverte ultérieure d'une symétrie exacte omise peut réviser l'interprétation d'un résultat antérieur sans rendre le calcul numérique faux.

Le groupe déclaré fait partie du domaine obligatoire du verdict.

---

## 14. Contrôle du mode trivial de rééchelonnement

Lorsqu'une observable dérivée est construite à partir de temps caractéristiques, un rééchelonnement global :

```math
H\mapsto sH
```

peut rééchelonner tous les temps sans produire de structure relationnelle non uniforme.

La famille scientifique doit soit exclure cette direction, soit la quotienter explicitement.

Le rééchelonnement global doit être utilisé comme contrôle nul lorsqu'il fournit un oracle analytique simple.

Un signal relationnel ne doit pas être défini par la seule condition :

```text
quantité relative != 1
```

si un mode uniforme peut produire cette variation.

---

## 15. Comparaisons inter-orbites

Deux relations peuvent :

- appartenir à la même orbite d'un stabilisateur et devoir donner le même résultat ;
- appartenir à des orbites distinctes et être comparées pour mesurer une différence physique ;
- avoir la même distance de graphe sans être symmetry-equivalentes.

La documentation doit distinguer :

```text
ORBIT CONSISTENCY
    égalité exigée par symétrie

INTER-ORBIT CONTRAST
    différence physique autorisée
```

La distance de graphe seule ne définit jamais une équivalence physique.

---

## 16. Troncature : deux appariements distincts

Lorsqu'une famille dépend d'un cutoff `Λ`, la comparaison entre `Λ_ref` et `Λ_check` doit séparer :

### Appariement opératoriel

Même observable / même indice, espace élargi.

C'est le contrôle principal de convergence.

### Appariement structurel relatif au bord

Même position relative au bord du spectre tronqué, quitte à changer l'indice de l'observable.

C'est un diagnostic d'effet de bord et non un verdict de convergence.

Changer simultanément le cutoff et la famille de sondes invalide une conclusion de convergence si les contributions ne sont pas séparées.

---

## 17. Contrôles de troncature par observable

Une famille agrégée peut masquer qu'un résultat est porté par une seule sonde particulièrement mince ou située au bord de la troncature.

Lorsque le protocole possède des harmoniques ou secteurs hiérarchisés, la convergence doit être publiée sonde par sonde lorsque cette granularité peut changer l'interprétation.

Une stabilité globale n'efface pas une instabilité localisée dans l'observable qui porte réellement le signal.

---

## 18. Normalisation non circulaire

Une sonde comparant plusieurs fonds ne doit pas être normalisée séparément par une amplitude extraite de chaque fond mesuré si cette amplitude fait partie de la réponse étudiée.

Sont préférables :

- une borne structurelle indépendante du fond ;
- une norme d'opérateur ;
- une normalisation fixée exclusivement depuis une référence avant inspection des états comparés.

La réponse d'un état ne doit pas fixer son propre dénominateur si cela peut masquer la variation que le protocole cherche précisément à mesurer.

---

## 19. Oracle asymptotique et contenu scientifique

Une limite asymptotique calculable algébriquement sans évolution temporelle complète peut constituer un excellent oracle de non-régression tout en n'étant pas la quantité scientifique primaire.

Le protocole doit distinguer :

```text
ORACLE
    valeur connue qui contrôle l'implémentation / le régime asymptotique

SCIENTIFIC SIGNAL
    comportement dans le domaine où la question physique est effectivement posée
```

La convergence vers un oracle ne suffit jamais à démontrer que l'oracle porte l'interprétation recherchée.

---

## 20. Verdicts

Les statuts génériques sont :

```text
PASS
    le critère pré-enregistré est satisfait dans son domaine déclaré

FAIL
    le critère pré-enregistré échoue

INCONCLUSIVE
    les calculs sont valides mais le protocole ne permet pas
    l'interprétation prévue dans le domaine déclaré

INACTIVE
    la perturbation / le canal déclaré n'agit pas sur la référence

NOT_APPLICABLE
    la quantité dérivée n'est pas mathématiquement définie
    sous les conditions rencontrées
```

Un `INCONCLUSIVE` ne devient jamais `PASS` par choix post-hoc d'un seuil ou d'une tolérance.

---

## 21. Paramètres et tolérances

Un seuil nécessaire au verdict doit être :

- justifié par une précision numérique démontrée ;
- ou pré-enregistré avec une analyse de sensibilité ;
- ou remplacé par un test structurel lorsque celui-ci existe.

Le protocole privilégie les critères sans seuil arbitraire lorsque cela est possible, mais ne masque jamais un seuil nécessaire derrière une notion qualitative comme « assez stable », « vrai maximum » ou « petite erreur ».

---

## 22. Rapport négatif obligatoire

Les résultats négatifs et limitations ne sont pas des incidents à effacer.

Le rapport conserve notamment :

- les directions dans le noyau ;
- les générateurs inactifs ;
- les familles insuffisantes ;
- les signaux interdits par symétrie ;
- les dépendances au cutoff ;
- les définitions de temps qui échouent ;
- les transformations nouvelles qui requalifient un ancien résultat.

Le lot suivant ne doit pas réécrire l'histoire pour faire disparaître ces résultats.

---

## 23. Séparation outil / résultat scientifique

Un benchmark analytique connu valide un instrument, pas une hypothèse scientifique.

Réciproquement, un résultat exploratoire ne doit pas être déclaré valide uniquement parce que :

- les tests passent ;
- le code est déterministe ;
- la SVD est numériquement stable ;
- un oracle de régression est reproduit.

Les validations instrumentales et scientifiques restent séparées.

---

## 24. Application future

Après gel, cette gouvernance devra être lue avant toute spécification, manifeste ou validation scientifique applicable.

La migration future devra :

1. créer `docs/governance/scientific-method-governance.md` ;
2. mettre à jour `docs/governance/documentation-governance.md` ;
3. mettre à jour l'ordre de lecture de `docs/governance/collaboration-governance.md` si Lionel le valide ;
4. journaliser la décision normative ;
5. vérifier le diff documentaire global ;
6. ne modifier aucune convention scientifique de modèle en dehors du paquet explicitement autorisé.
