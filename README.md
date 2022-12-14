# MLOPS

Pour ce projet nous avons mis en production un modèle de ML via un webservice grâce à FastAPI

## Instructions de lancement
- Vérifier que toutes les ressources nécessaires sont bien téléchargées localement avec `pip install -r requirements.txt` ou `pip3 install -r requirements.txt`
- Créer et sauvegarder le modèle entrainé (et le jeu d'entrainement) avec `python build_model.py` ou `python3 build_model.py`
- Lancer le webservice avec `uvicorn app:app --reload`
- Rendez-vous sur le [localhost](http://localhost:8000/docs) pour tester les commandes de l'API

## Commandes
> GET /hello
> 
> Retourne un "Hello World!" pour vérifier que l'API fonctionne correctement

> POST /predict
>
>  Prend 3 paramètres en corps de requête: `glucose`, `bmi` et `age`
>  
>  Retourne la prédiction avec ces paramètres (1 pour diabétique et 0 pour non-diabétique)

> GET /predict/{n}
> 
> Prend un entier `n` en paramètre
> 
> Créer `n` requêtes POST /predict avec des données aléatoires
> 
> Retourne le temps total pour exécuter ces requêtes

> GET /new_data
> 
> Retourne le tableau de toutes les requêtes lancées depuis que l'API fonctionne (Attention: Si l'API est relancée le tableau sera effacé)

## Notes
- La commande POST est notre commande principale pour la mise en production de notre modèle de ML
- La comande GET /predict/{n} nous permet de tester la parallélisation des requêtes
- La commande GET /new_data nous permet de visualiser le nouveau jeu de données qui est en comparaison avec celui d'entrainement pour savoir s'il y a de la dérive conceptuelle
