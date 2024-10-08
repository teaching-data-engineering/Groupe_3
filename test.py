import requests
import time

def get_json_from_url(mon_url,params=None):
    # Définir l'agent utilisateur
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:  # Gestion des exceptions avec un bloc try/except
        response = requests.get(mon_url, headers=headers, params=params)
        response.raise_for_status()  # Génère une exception pour les codes d'erreur HTTP
        return response.json()  # Renvoie directement la réponse au format JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    return None


def param(date= "2024-10-07T14:01:04,2024-10-31T23:00:00",longitude= -0.12574,latitude= 51.50853,salle=None, page=1, ville=2643743, genres='all-genres'):
    params ={ 'city_id': ville,  # ID de la ville de Londres
        'date': date,  # Plage de dates
        'page': page,  # Numéro de la page
        'longitude': longitude,  # Longitude de Londres
        'latitude': latitude,
        'genre_query': genres
    }
    return params

def collect_events(url, delay=1):
    page = 1
    all_events = []
    last_event_ids = set()  # Ensemble pour suivre les IDs des événements collectés
    last_events = []  # Stocker les événements de la dernière page pour comparaison

    while True:  # Boucle infinie jusqu'à ce que nous décidions d'arrêter
        data = get_json_from_url(url, param(page=page))
        
        if data and 'events' in data:
            events = data['events']
            if not events:  # S'il n'y a pas d'événements, nous arrêtons la collecte
                print(f"Aucun événement trouvé sur la page {page}. Arrêt de la collecte.")
                break
            
            # Vérification de l'unicité des événements
            new_events = []
            for event in events:
                event_id = event.get('eventUrl')  # Utiliser l'URL de l'événement comme ID
                if event_id not in last_event_ids:  # Si l'événement n'a pas été collecté
                    new_events.append(event)
                    last_event_ids.add(event_id)  # Ajouter l'ID à l'ensemble
            
            if not new_events:  # Si aucun nouvel événement n'a été trouvé
                print(f"Aucun nouvel événement trouvé sur la page {page}. Arrêt de la collecte.")
                break
            
            all_events.extend(new_events)
            print(f"Collecte des événements de la page {page}. Total des événements collectés : {len(all_events)}")
            
            last_events = events.copy()  # Mettre à jour last_events avec les événements de la page actuelle
            page += 1
            time.sleep(delay)  # Ajout d'un délai entre les requêtes
        else:
            print("Aucun événement trouvé ou données mal formatées. Arrêt de la collecte.")
            break

    return all_events


###########################test###############################

 
if __name__ == '__main__':
    url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents"
    
    events = collect_events(url, delay=1)  # Vous pouvez ajuster le délai ici
    print(len(events))

    """
    # Affichage des événements collectés
    if events:
        for event in events:
            artist_name = event.get('artistName', 'Artiste inconnu')
            event_date = event.get('startsAt', 'Date inconnue')
            venue_name = event.get('venueName', 'Lieu inconnu')
            venue_city = event.get('locationText', 'Ville inconnue')
            print(f"Artiste : {artist_name}, Date : {event_date}, Lieu : {venue_name}, {venue_city}")
    else:
        print("Aucun événement collecté.")
    """