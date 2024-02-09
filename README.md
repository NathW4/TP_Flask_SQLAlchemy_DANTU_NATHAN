# TP_Flask_SQL_Alchemy_DANTU_NATHAN

## Liste des routes :
### 1. Ajouter une chambre

- Méthode : POST
- Endpoint : http://127.0.0.1:5000/api/chambres

**Corps de la Requête (JSON) :**

	{
		"numero": "100",
		"type": "Simple",
		"prix": 30.00
	}

### 2. Modifier une chambre

- Méthode : PUT
- Endpoint : http://127.0.0.1:5000/api/chambres/{id}

**Corps de la Requête (JSON) :**

	{
		"numero": "100",
		"type": "Simple",
		"prix": 50.00
	}

### 3. Supprimer une chambre

- Méthode : DELETE
- Endpoint : http://127.0.0.1:5000/api/chambres/{id}

### 4. Chambres disponibles

- Méthode : POST
- Endpoint : http://127.0.0.1:5000/api/chambres/disponibles

**Corps de la Requête (JSON) :**

	{
		"date_arrivee": "2024-02-14",
		"date_depart": "2024-02-20"
	}

### 5. Créer une réservation

- Méthode : POST
- Endpoint : http://127.0.0.1:5000/api/reservations


**Corps de la Requête (JSON) :**

	{
		"id_client": 1,
		"id_chambre": 4,
		"date_arrivee": "2024-04-10",
		"date_depart": "2024-05-15"
	}

*Assurez-vous de créer un client pour pouvoir en utiliser l'id,
par exemple, en entrant dans le base MYSQL : *

	INSERT INTO client (nom, email) VALUES ('Bob', 'le.bob@gmail.com');

### 6. Annuler une réservation

- Méthode : DELETE
- Endpoint : http://127.0.0.1:5000/api/reservations/{id}

