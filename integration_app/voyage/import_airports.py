import sys
import os
import django
import csv

# Ajoutez la racine de votre projet au chemin
sys.path.append('/home/francois/Documents/ZZ3/integration/integration_app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integration_app.settings')
django.setup()


from voyage.models import Airport
# Votre code ici

# Maintenant vous pouvez importer les modèles
from voyage.models import Airport

def reset_airport_data(file_path):
    # 1. Vider la table
    Airport.objects.all().delete()
    print("La table Airport a été vidée.")

    # 2. Réinsérer les données depuis le fichier CSV
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                Airport.objects.create(
                    airport_name=row['Airport_Name'],
                    airport_id=row['Id'],
                    iata_code=row['Airport_Id'],
                    country=row['Country'],
                    city=row['City'],
                    latitude=float(row['Latitude']),
                    longitude=float(row['Longitude'])
                )
            except ValueError as e:
                print(f"Erreur sur la ligne : {row}")
                print(f"Détails de l'erreur : {e}")
    print("Données importées avec succès.")

# Chemin vers le fichier CSV
file_path = 'airports.csv'
reset_airport_data(file_path)