from voyage.models import Airport
for  city in Airport.objects.all():
    print(city)