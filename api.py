import requests

def get_json_from_url(mon_url):
    # Définir l'agent utilisateur
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:  # Gestion des exceptions avec un bloc try/except
        response = requests.get(mon_url, headers=headers)
        response.raise_for_status()  # Génère une exception pour les codes d'erreur HTTP
        return response.json()  # Renvoie directement la réponse au format JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    return None




###########################test###############################

 
if __name__ == '__main__':
    url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2643743&date=2024-10-07T14%3A01%3A04%2C2024-10-31T23%3A00%3A00&page=30&longitude=-0.12574&latitude=51.50853&genre_query=all-genres"
    data = get_json_from_url(url)
    
    if data and 'events' in data:
        # Afficher le nom du premier artiste dans la liste des événements
        first_event = data['events'][0]
        artist_name = first_event.get('artistName', 'Artiste inconnu')
        print(f"Le premier artiste est : {artist_name}")
    else:
        print("Aucun événement trouvé ou données mal formatées.")
    
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