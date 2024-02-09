from datetime import datetime
from flask import Blueprint, jsonify, render_template, request
from .database import db
from .models import Chambre, Reservation


main = Blueprint('main', __name__)



@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
	data = request.get_json()

	# Vérifier si tous les champs nécessaires sont fournis
	if 'numero' not in data or 'type' not in data or 'prix' not in data:
		return jsonify({"error": "Tous les champs (numero, type, prix) sont obligatoires."}), 400

	# Vérifier si le numéro de chambre existe déjà
	if Chambre.query.filter_by(numero=data['numero']).first():
		return jsonify({"error": "Le numéro de chambre existe déjà."}), 400

	nouvelle_chambre = Chambre(
		numero=data['numero'],
		type=data['type'],
		prix=data['prix']
	)

	db.session.add(nouvelle_chambre)
	db.session.commit()

	return jsonify({"success": True, "message": "Chambre ajoutée avec succès."})



@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
	data = request.get_json()
	
	chambre = Chambre.query.get(id)
	if not chambre:
		return jsonify({"error": "La chambre spécifiée n'existe pas."}), 404

	chambre.numero = data['numero']
	chambre.type = data['type']
	chambre.prix = data['prix']

	db.session.commit()

	return jsonify({"success": True, "message": "Chambre mise à jour avec succès."})



@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
	# Vérifier si la chambre avec l'ID spécifié existe
	chambre = Chambre.query.get(id)
	if not chambre:
		return jsonify({"error": "La chambre spécifiée n'existe pas."}), 404

	db.session.delete(chambre)
	db.session.commit()

	return jsonify({"success": True, "message": "Chambre supprimée avec succès."})



@main.route('/api/chambres/disponibles', methods=['POST'])
def chambres_disponibles():
	data = request.get_json()

	if not data or 'date_arrivee' not in data or 'date_depart' not in data:
		return jsonify({"error": "Les dates de recherche (date_arrivee, date_depart) sont obligatoires dans le JSON."}), 400

	date_arrivee = datetime.strptime(data['date_arrivee'], "%Y-%m-%d")
	date_depart = datetime.strptime(data['date_depart'], "%Y-%m-%d")

	chambres_disponibles = []

	toutes_chambres = Chambre.query.all()

	for chambre in toutes_chambres:
		if not chambre_est_reserve(chambre.id, date_arrivee, date_depart):
			chambre_disponible = {
				"id": chambre.id,
				"numero": chambre.numero,
				"type": chambre.type,
				"prix": chambre.prix
			}
			chambres_disponibles.append(chambre_disponible)

	return jsonify(chambres_disponibles)



@main.route('/api/reservations', methods=['POST'])
def creer_reservation():
	data = request.get_json()

	# Vérifier si tous les champs nécessaires sont fournis
	if 'id_client' not in data or 'id_chambre' not in data or 'date_arrivee' not in data or 'date_depart' not in data:
		return jsonify({"error": "Tous les champs (id_client, id_chambre, date_arrivee, date_depart) sont obligatoires."}), 400

	# Convertir les dates du format string en objets datetime
	date_arrivee = datetime.strptime(data['date_arrivee'], "%Y-%m-%d")
	date_depart = datetime.strptime(data['date_depart'], "%Y-%m-%d")

	# Vérifier la disponibilité de la chambre pour les dates demandées
	if chambre_est_reserve(data['id_chambre'], date_arrivee, date_depart):
		return jsonify({"error": "La chambre n'est pas disponible pour les dates demandées."}), 400

	nouvelle_reservation = Reservation(
		id_client=data['id_client'],
		id_chambre=data['id_chambre'],
		date_arrivee=date_arrivee,
		date_depart=date_depart,
		statut="Confirmée"
	)

	db.session.add(nouvelle_reservation)
	db.session.commit()

	return jsonify({"success": True, "message": "Réservation créée avec succès."})



@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annuler_reservation(id):
	# Vérifier si la réservation avec l'ID spécifié existe
	reservation = Reservation.query.get(id)
	if not reservation:
		return jsonify({"error": "La réservation spécifiée n'existe pas."}), 404

	db.session.delete(reservation)
	db.session.commit()

	return jsonify({"success": True, "message": "Réservation annulée avec succès."})



def chambre_est_reserve(id_chambre, date_arrivee, date_depart):
	reservations = Reservation.query.filter_by(id_chambre=id_chambre).all()

	for reservation in reservations:
		if reservation_chevauche_dates(reservation.date_arrivee, reservation.date_depart, date_arrivee, date_depart):
			return True

	return False


def reservation_chevauche_dates(debut_reservation, fin_reservation, debut_recherche, fin_recherche):
  return (debut_reservation < fin_recherche) and (fin_reservation > debut_recherche)