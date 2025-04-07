# Dans l'effervescence de la ville égyptienne au Ier siècle apr. J.-C. se dressait la Grande Bibliothèque d’Alexandrie, tel un phare
# du savoir antique. Parmi les érudits arpentant les couloirs sacrés se trouvait Héron, un esprit brillant réputé pour ses prouesses 
# et son habileté en mathématiques, en mécanique et en ingénierie.
# Un jour, alors que Héron parcourait la vaste collection de papyrus et de parchemins, il ne put s'empêcher de remarquer le
# désordre qui sévissait dans la Bibliothèque (probablement à cause d’autres savants pas très disciplinés). Les étagères,
# autrefois bien organisées, reflétaient désormais la

# complexité des problèmes qu'il avait l’habitude de résoudre.

# Déterminé à rétablir l'ordre, Heron s'est attelé à la tâche en explorant différentes méthodes pour résoudre ce nouveau défi qui se présentait à lui.

# Les algorithmes de tri et vous

# Voyant les efforts considérables de Héron d’Alexandrie et voulant l’aider dans sa labeur, vous effectuez des recherches afin de trouver une façon d’automatiser
# l’organisation des papyrus contenant le savoir de l'humanité. Lors de vos recherches vous tombez sur les algorithmes de tri. Quelle aubaine ! Vous allez pouvoir

# aider ce pauvre érudit dans sa quête (presque) impossible. Un algorithme de tri, notion fondamentale en informatique ou en
# mathématiques, est un algorithme qui permet d'organiser une collection d'objets selon une relation d'ordre déterminée. Suivant la relation d'ordre
# considérée, une même collection d'objets peut donner lieu à divers arrangements.
# On pourrait, par exemple, trier un tableau tab d'entiers naturels de 1 à N dans un ordre croissant ou décroissant.

# L'implémentation des algorithmes de tri est un excellent exercice pour comprendre des concepts fondamentaux de la programmation,
# comprendre d'autres algorithmes et se préparer à des entretiens techniques. ➔ Dans un élan héroïque, vous portez secours à Héron, en créant un outil
# d'automatisation de tri d’objets (ici, des listes de nombres réels). Implémentez les algorithmes de tri suivants :
# 1. Tri par sélection
# 2. Tri à bulles
# 3. Tri par insertion
# 4. Tri fusion
# 5. Tri rapide
# 6. Tri par tas
# 7. Tri à peigne
# ➔ Pour une liste de nombres réels et un algorithme de tri définis par l’utilisateur, affichez l’input, triez le et affichez le résultat trié dans le
# terminal.

# ➔ (Question recommandée spécialisation IA) Vous avez réussi à implémenter 7 différents algorithmes de tri, vous pouvez être fiers de vous !
# Cependant vous ne voulez pas vous arrêter en si bonne lancée. En bon développeur, vous décidez d’analyser et calculer le temps
# d’exécution de vos implémentations lors du tri d’une liste de nombre réels afin de proposer le plus rapide à Héron.
# Notez vos observations dans le fichier README.md de votre repository. 
# ➔ Afin d’apporter un aspect visuel à l’efficacité de vos algorithmes de tri et de valoriser votre travail (et aussi parce que vous vous sentez l'âme d’un artiste), vous décidez de créer une interface graphique.
# Vous pourriez, comme sur l’exemple ci-dessous, trier un cercle de couleurs aléatoires. Attribuez une couleur quelconque à chaque valeur
# de la liste et montrer à l’utilisateur le tri au fur et à mesure.

# ➔ (Question recommandée spécialisation logiciel / image) Parallélisez l'exécution des différents algorithmes de tri (multithreading).

# Dans un repository github public nommé sorting-algorithms, vous devrez fournir les éléments suivants :
# ● Un script sorting.py contenant les différentes implémentations des algorithmes de tri (fonctions, classes),
# ● Un script main.py permettant de coordonner et d’exécuter le code principal de votre outil,
# ● Un fichier README.md expliquant le contexte du projet, les algorithmes utilisés et une conclusion sur votre travail.

# ------------------------Résoudre-------------------------------------

# 1.1 Tri par sélection
def tri_selection(tab):
    n = len(tab)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if tab[j] < tab[min_index]:
                min_index = j
        tab[i], tab[min_index] = tab[min_index], tab[i]
    return tab

# 1.2 Tri à bulles
# Le tri à bulles compare chaque paire d'éléments adjacents et les échange s'ils sont dans le mauvais ordre.
def tri_bulles(tab):
    n = len(tab)
    for i in range(n):
        for j in range(0, n-i-1):
            if tab[j] > tab[j+1]:
                tab[j], tab[j+1] = tab[j+1], tab[j]
    return tab

# 1.3 Tri par insertion
# Le tri par insertion insère chaque élément dans une sous-liste triée à gauche de l'élément.
def tri_insertion(tab):
    for i in range(1, len(tab)):
        key = tab[i]
        j = i - 1
        while j >= 0 and key < tab[j]:
            tab[j + 1] = tab[j]
            j -= 1
        tab[j + 1] = key
    return tab

# 1.4 Tri fusion
# Le tri fusion est un algorithme de tri diviser-pour-régner qui divise le tableau en sous-tableaux et les fusionne de manière triée.
def tri_fusion(tab):
    if len(tab) <= 1:
        return tab
    mid = len(tab) // 2
    left = tri_fusion(tab[:mid])
    right = tri_fusion(tab[mid:])
    return fusion(left, right)

def fusion(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 1.5 Tri rapide
# Le tri rapide utilise un pivot pour diviser la liste en deux sous-listes, puis trie récursivement les sous-listes.
def tri_rapide(tab):
    if len(tab) <= 1:
        return tab
    pivot = tab[len(tab) // 2]
    left = [x for x in tab if x < pivot]
    middle = [x for x in tab if x == pivot]
    right = [x for x in tab if x > pivot]
    return tri_rapide(left) + middle + tri_rapide(right)
# 1.6 Tri par tas
# Le tri par tas utilise un tas binaire pour organiser les éléments et les trier.

import heapq

def tri_tas(tab):
    heapq.heapify(tab)
    return [heapq.heappop(tab) for _ in range(len(tab))]
# 1.7 Tri à peigne
# Le tri à peigne est une amélioration du tri à bulles, avec une meilleure performance sur les grandes listes.

def tri_peigne(tab):
    gap = len(tab)
    swapped = True
    while gap != 1 or swapped:
        gap = max(1, int(gap / 1.3))
        swapped = False
        for i in range(len(tab) - gap):
            if tab[i] > tab[i + gap]:
                tab[i], tab[i + gap] = tab[i + gap], tab[i]
                swapped = True
    return tab

# 2. Mesure du temps d'exécution
# Vous pouvez mesurer le temps d'exécution de chaque algorithme en utilisant le module time de Python.

import time

def mesurer_temps(algorithme, tab):
    start_time = time.time()
    algorithme(tab)
    end_time = time.time()
    return end_time - start_time
# 3. Interface graphique pour visualisation
# Pour la visualisation, nous utiliserons Tkinter (ou toute autre bibliothèque graphique de votre choix). L'interface affichera les valeurs sous forme de barres de différentes couleurs.

import tkinter as tk
import random

def afficher_graphe(tab):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    # Afficher les valeurs sous forme de barres colorées
    for i, val in enumerate(tab):
        canvas.create_rectangle(i * 10, 500, (i + 1) * 10, 500 - int(val * 100), fill="blue")

    root.mainloop()

# Exemple d'affichage
tab = [random.uniform(0, 1) for _ in range(50)]
afficher_graphe(tab)

# 4. Parallélisation (multithreading)
# Pour paralléliser les algorithmes de tri, vous pouvez utiliser la bibliothèque threading. Cela permettra d'exécuter plusieurs algorithmes en même temps et de comparer leurs temps d'exécution.

import threading

def exécuter_en_parallel(algorithmes, tab):
    threads = []
    results = []

    def wrapper(algorithme):
        results.append((algorithme.__name__, mesurer_temps(algorithme, tab)))

    for algorithme in algorithmes:
        thread = threading.Thread(target=wrapper, args=(algorithme,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results