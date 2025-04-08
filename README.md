
Il est important de documenter vos résultats dans un fichier README.md. Vous y inclurez vos observations sur les performances des algorithmes et des analyses concernant leur complexité.

markdown
Copier
# Analyse des Algorithmes de Tri

## Algorithmes Implémentés :

#### - Tri par sélection :
![Diagramme explicatif](imageAlgo/selection.png)

#### - Tri à bulles :
![Diagramme explicatif](imageAlgo/bulles.png)

#### - Tri par insertion :
![Diagramme explicatif](imageAlgo/insertion.png)

#### - Tri fusion :
![Diagramme explicatif](imageAlgo/fusion.png)

#### - Tri rapide :
![Diagramme explicatif](imageAlgo/rapide.png)

#### - Tri par tas :
![Diagramme explicatif](imageAlgo/tas.png)

#### - Tri à peigne : 
Cet algorithme fonctionne en réduisant progressivement l'écart (gap) entre les éléments comparés et en les échangeant si nécessaire. Cela permet de déplacer les éléments plus rapidement vers leur position correcte. On considère généralement que, dans le meilleur des cas: linéaire (en O(n)), et que, dans le pire des cas : Θ(n2). En moyenne : O(n log n).Tri non stable

#### - Critère de comparaison des algorithmes de tri : 
 complexité temporelle (pire cas / en
 moyenne); complexité spatiale; stabilité; caractère en place.
![Diagramme explicatif](imageAlgo/tableauComparaison.png)

## Performances
Les temps d'exécution des algorithmes sont mesurés en fonction de la taille de la liste et de la distribution des éléments.

### Observations :
- Le tri rapide et le tri fusion sont généralement les plus performants pour des listes de grande taille.
- Le tri à bulles et le tri par sélection sont très inefficaces pour les grandes listes.

## Conclusion
Le tri rapide est l'algorithme de tri le plus rapide pour des listes de taille moyenne à grande. Cependant, pour de très petites listes, des algorithmes comme le tri par insertion peuvent être plus efficaces.


