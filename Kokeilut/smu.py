import mysql.connector
import random

continents_visited = set()
# Haetaan yhdessä string muutujassa mahdolliset edelliset muuttujat
continent_sql = ["EUNASA"]
#
for i in range(0, len(continent_sql[0]), 2):
    if continent_sql[0][i:i + 2] != "":
        continents_visited.add(continent_sql[0][i:i + 2])

x = 0
for i in continents_visited:
    x += 1
    print(x)
    print(i)
