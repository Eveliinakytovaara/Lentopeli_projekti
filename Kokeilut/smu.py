# Haetaan lentoasemien indet-koodeja listaan valitusta maanosasta
airports = ["a", "b", "c", "d"]
# Luodaan muuttuja for loopin ulkopuolelle, jotta muistetaan käytettävä säätila
weather_name = ""
# Luodaan lista, joka pitää sisällään kaiken tulostettavan datan lentoasemista
airport_data = []

for i in range(len(airports)):
    # Luodaan tilapäinen lista, joka sisältää ykittäisiä arvoja lentoasemasta
    temp = []
    # Haetaan lentoaseman nimi
    temp.append(airports[i])
    # Haetaan satunnainen säätilan nimi
    weather_name = "windy"
    temp.append("wind blows hard")
    # Lasketaan etäisyys
    temp_distance = 1000
    # Lisätään etäisyys listaan
    temp.append(str(temp_distance))
    # Haetaan lentokoneen koko nimenä etäisyyden perusteella
    temp.append("big")
    # Lisätään tilapäinen lista airport_data listaan
    airport_data.append(temp)

# Tulostetaan listan arvot
for i in range(len(airport_data)):
    print(i)
    for o in airport_data[i]:
        print(o)
    print("")
