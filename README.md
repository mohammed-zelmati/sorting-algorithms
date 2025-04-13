# Analyse des Algorithmes de Tri

## Algorithmes Implémentés :

### 1- Tri par sélection :

L'algorithme parcourt la liste et sélectionne l'élément le plus petit (ou le plus grand, selon l'ordre voulu) à chaque étape, puis le place à la bonne position dans la liste.

![Diagramme explicatif](imageAlgo/selection.png)

### 2- Tri à bulles :

Il compare chaque paire d'éléments adjacents et les échange si nécessaire. Ce processus est répété jusqu'à ce que la liste soit triée.

![Diagramme explicatif](imageAlgo/bulles.png)

### 3- Tri par insertion :

L'algorithme construit progressivement une sous-liste triée en insérant chaque nouvel élément à la bonne position dans la sous-liste déjà triée.

![Diagramme explicatif](imageAlgo/insertion.png)

### 4- Tri fusion :

Il divise la liste en sous-listes plus petites, les trie récursivement, puis fusionne ces sous-listes triées pour obtenir la liste triée finale.

![Diagramme explicatif](imageAlgo/fusion.png)

### 5- Tri rapide (QuickSort) :

Il choisit un élément pivot, sépare la liste en deux parties (les éléments inférieurs et supérieurs au pivot), puis trie récursivement les deux parties.

![Diagramme explicatif](imageAlgo/rapide.png)

### 6- Tri par tas (HeapSort) :

Il construit un tas (une structure de données similaire à un arbre binaire), extrait l'élément maximum (ou minimum) à chaque étape et le place dans la liste triée.

![Diagramme explicatif](imageAlgo/tas.png)

### 7- Tri à peigne :

Cet algorithme fonctionne en réduisant progressivement l'écart (gap) entre les éléments comparés et en les échangeant si nécessaire. Cela permet de déplacer les éléments plus rapidement vers leur position correcte.

![Diagramme explicatif](imageAlgo/peigne.png)

### - Critère de comparaison des algorithmes de tri :

complexité temporelle (pire cas / en moyenne); complexité spatiale; stabilité; caractère en place.

![Diagramme explicatif](imageAlgo/tableauComparaison.png)

# Performances :

Les temps d'exécution des algorithmes sont mesurés en fonction de la taille de la liste et de la distribution des éléments.

# Observations :

#### - Le tri rapide et le tri fusion sont généralement les plus performants pour des listes de grande taille.

#### - Le tri à bulles et le tri par sélection sont très inefficaces pour les grandes listes.

# Conclusion:

#### - Le tri par sélection a une performance 𝑂(𝑛2)O(n 2) dans tous les cas, mais il est en place et nécessite peu de mémoire.

#### - Le tri fusion offre une meilleure performance théorique 𝑂(𝑛log𝑛), mais il n'est pas en place car il nécessite de la mémoire pour stocker des sous-tableaux.

#### - Le tri rapide est un algorithme très efficace en moyenne, mais son pire cas est moins bon que celui du tri fusion.

#### - Le tri par tas offre une bonne performance O(nlogn), mais il n'est pas stable.

Version finale :

# 🔢 Visualiseur Interactif des Algorithmes de Tri (Pygame)

Bienvenue dans notre outil avancé de visualisation des **algorithmes de tri** !  
Ce projet permet de **comparer visuellement et techniquement** différentes méthodes de tri sur des données variées.

---

## 🧠 Objectif du Projet

Inspiré par Héron d’Alexandrie, ce projet a pour but :

- d'automatiser l'organisation de données comme les couleurs, les lettres, les mots ou les nombres,
- de **comprendre, visualiser et comparer** les algorithmes de tri fondamentaux,
- d'offrir une **expérience utilisateur immersive et pédagogique**.

---

## ✨ Fonctionnalités Clés

| Fonction                             | Détail                                                         |
| ------------------------------------ | -------------------------------------------------------------- |
| 🎨 **Modes de visualisation**        | Couleurs 🌈, Nombres 🔢, Mots 📝, Lettres 🔤                   |
| 🖼️ **Visualisation graphique**       | Cercle de couleurs, barres de hauteurs, grille de mots         |
| ⚙️ **Algorithmes disponibles**       | Sélection, Bulles, Insertion, Fusion, Rapide, Tas, Peigne      |
| 🧾 **Historique JSON**               | Chaque tri est enregistré avec temps, mémoire, type            |
| 📊 **Comparaison automatique**       | Résumé global des performances dans `comparison_summary.json`  |
| 🕹️ **Contrôle de vitesse**           | Slider pour régler la vitesse de tri (de lent à turbo)         |
| 🧩 **Mode pas-à-pas**                | Avance manuelle des étapes avec animation                      |
| 🎛️ **Interface utilisateur moderne** | Thème sombre/clair, effets sonores, boutons dynamiques         |
| ❓ **Aide interactive**              | Fenêtre tutorielle "?" avec explications intégrées             |
| 🔁 **Redémarrage instantané**        | Touche R ou bouton pour relancer un tri avec nouvelles données |
| 💬 **Infobulles intelligentes**      | Affichées au survol de chaque élément (ex : complexité, rôle)  |

---

## 🔍 Algorithmes Implémentés

Chaque algorithme est visualisé **en temps réel** et expliqué dans le module d'aide intégré.

### 1. Tri par sélection

Parcourt la liste, sélectionne l’élément minimum à chaque étape et le place à sa position finale.  
⏱️ Complexité : `O(n²)` — **Non stable** — In-place

### 2. Tri à bulles

Compare les paires adjacentes et les échange si nécessaire jusqu’à ce que la liste soit triée.  
⏱️ Complexité : `O(n²)` — **Stable**

### 3. Tri par insertion

Construit une sous-liste triée en insérant chaque nouvel élément à sa bonne position.  
⏱️ Complexité : `O(n²)` — **Stable**

### 4. Tri fusion (Merge Sort)

Divise récursivement puis fusionne les sous-listes triées.  
⏱️ Complexité : `O(n log n)` — **Stable** — Non in-place

### 5. Tri rapide (Quick Sort)

Utilise un pivot pour diviser et trier récursivement.  
⏱️ Complexité : `O(n log n)` en moyenne — **Non stable**

### 6. Tri par tas (Heap Sort)

Construit un tas binaire, extrait les éléments dans l'ordre.  
⏱️ Complexité : `O(n log n)` — **Non stable**

### 7. Tri à peigne (Comb Sort)

Optimise le tri à bulles en diminuant l’écart entre les éléments comparés.  
⏱️ Complexité moyenne : `O(n log n)` — **Non stable**

---

## 📁 Structure du Projet

```bash
sorting-algorithms/
│
├── assets/                # Sons, polices, icônes
│   ├── fonts/
│   ├── sounds/
│
├── history/               # Logs JSON pour chaque tri
│   ├── sort_[algo]_[type]_[timestamp].json
│   └── comparison_summary.json
│
├── main.py                # Point d’entrée de l’application
├── script.py              # Logique UI, Visualisation, Algorithmes
├── requirements.txt
└── README.md              # Ce fichier
```

Fonction Ancienne version ❌ Nouvelle version ✅
Historique JSON ❌ ✅
Fichier de comparaison ❌ ✅
Reset auto sur changement ❌ ✅
Aide interactive "?" ❌ ✅
Mode Lettres ❌ ✅
Thèmes (sombre/clair) ❌ ✅
Effets sonores ❌ ✅
Contrôle de vitesse ❌ ✅
Mode manuel (étape) ❌ ✅
Redémarrer (touche R) ❌ ✅
Infobulles et survol ❌ ✅
Affichage mémoire + temps ❌ ✅
