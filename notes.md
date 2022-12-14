# Les outils possibles pour traiter des streams de données
- kafka: rapide, scalable, peut traiter des gros flux de données (beaucoup de clients, petites requêtes)
- apache flink: process les données en temps réel, supporte un large éventail de sources de données (besoin de réponse très très rapidement)
- apache spark: puissant data processing et peut supporter des grosses charges de données à traiter d'un seul coup (supporte les très grosses requêtes comme faire 12000 prédictions en une seule fois)
- google cloud pub/sub: facile à utiliser surtout si on utilise d'autres outils google à côté (facile à connecter aux outils google)

> Nous devons surtout gérer le cas de beaucoup d'utilisateurs qui soumettent une requête pour une prédiction à la fois. On a donc beaucoup de "petites" requêtes et il serait pratique de pouvoir les paralléliser.
> 
> Cela semble donc logique de se tourner vers kafka.


# Les outils possibles pour créer un webservice
- django: puissant et à un très grand set de features. (pratique pour les web services poussés avec plein d'options)
- flask: simple, flexible. (le plus simple d'utilisation)
- fastAPI: rapide, efficace. supporte l'asynchrone. (le plus efficace)

> Nous avons besoin de performances mais pas nécessairement d'un web service complet avec beaucoup d'option.
> 
> Cela semble donc logique de se tourner vers fastAPI.

---

### Après avoir essayé kafka et fastAPI, nous nous sommes rapidemment retrouvés bloqué par kafka pour divers problèmes techniques. Par mesure de simplicité on a fini par choisir fastAPI comme outil en passant donc par un webservice pour notre projet
