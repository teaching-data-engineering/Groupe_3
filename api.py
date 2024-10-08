import requests
import os
import json
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
                break
            
            # Vérification de l'unicité des événements
            new_events = []
            for event in events:
                event_id = event.get('eventUrl')  # Utiliser l'URL de l'événement comme ID
                if event_id not in last_event_ids:  # Si l'événement n'a pas été collecté
                    new_events.append(event)
                    last_event_ids.add(event_id)  # Ajouter l'ID à l'ensemble
            
            if not new_events:  # Si aucun nouvel événement n'a été trouvé
               break
            
            all_events.extend(new_events)
            
            last_events = events.copy()  # Mettre à jour last_events avec les événements de la page actuelle
            page += 1
            time.sleep(delay)  # Ajout d'un délai entre les requêtes
        else:
           break
    
    page_finale= page - 1
    return print(page_finale)


def scrap_one_page(page):
    data = get_json_from_url(url,param(page=page))
    if data and 'events' in data:
        # Afficher tous les artistes entre le 8 et le 9 octobre 2024
        for event in data['events']:
            artist_name = event.get('artistName', 'Artiste inconnu')
            event_date = event.get('startsAt', 'Date inconnue')
            venue_name = event.get('venueName', 'Lieu inconnu')
            venue_city = event.get('locationText', 'Ville inconnue')
            print(f"Artiste : {artist_name}, Date : {event_date}, Lieu : {venue_name}, {venue_city}")
    else:
        print("Aucun événement trouvé ou données mal formatées.")

def save_json(response, idx_page):
    # Vérifier si la réponse est valide
    if response is None:
        print("Aucune donnée à sauvegarder.")
        return

    # Créer un dossier pour les pages si cela n'existe pas
    folder_name = 'json_data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Définir le nom du fichier avec l'index de la page
    file_name = f"{folder_name}/data_page_{idx_page}.json"

    # Écrire les données dans le fichier JSON
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

    print(f"Données sauvegardées dans {file_name}")
    return None

def scrap_multiple_pages(start_date, end_date, max_page=None, url="https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents"):
    if max_page == None :
        max_page =  int(collect_events(url))
    for page in range(1, max_page + 1):
        print(f"Scraping page {page}...")
        
        # Récupérer les paramètres pour la requête de la page
        params = param(date=f"{start_date},{end_date}", page=page)
        
        # Récupérer les données JSON de la page
        response = get_json_from_url(url, params)
        
        if response and 'events' in response:
            print(f"Page {page} récupérée avec succès.")
            
            # Sauvegarder les données de la page dans un fichier JSON
            save_json(response, page)
        else:
            print(f"Fin de la collecte ou problème rencontré à la page {page}.")
            break

    print("Collecte terminée.")


###########################test###############################

 
if __name__ == '__main__':
    url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents"
    data = get_json_from_url(url,param(page=2))
    #collect_events(url, delay=1)
    scrap_multiple_pages("2024-10-07T14:01:04","2024-10-31T23:00:00")
    #print(scrap_one_page(2))
    #save_json(data, 1)
    #print(type(collect_events(url)))