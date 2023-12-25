import requests

#zu generell liefert falsche ergebnisse zurück in absehbarer Zeit auch nicht möglich eine sinnvolle implementierung hinzubekommen. 
def validate_address(street, city):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{street}, {city}",
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.ok and data and data[0]['addresstype'] == 'place':
        return True
    else:
        return False
#google lösung Datenschutztechnisch komplizierter und umfangreicher und für use case eher ungeeignet