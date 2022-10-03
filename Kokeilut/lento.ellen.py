import random
import mysql.connector

def open_database():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='ellenonerva',
        autocommit=True)
    return connection

def execute_sql(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values

def get_from_database(connection, column, table, where, distinct):
    sql = "SELECT " + distinct + " " + column + " FROM " + table + " " + where
    values = execute_sql(connection, sql)
    return values
def cleanup_list(s):
    for i in range(len(s)):
        s[i] = str(s[i]).replace("('", "")
        s[i] = str(s[i]).replace("',)", "")
    return s
def get_weather(connection, type, is_random):
    if type == "name":
        data_type = "name"
    elif type == "mod":
        data_type = "mod"
    else:
        data_type = "desc"

    if is_random == "":
        index = random.randint(0, 10)
    else:
        temp_index = get_from_database(connection, "id",
                                  "weather", "where name = '" + is_random + "'", "")

        temp_index = cleanup_list(temp_index)
        print(temp_index)
        index = int(temp_index[0])

    value = get_from_database(connection, data_type, "weather", "where id = '" + str(index) + "'", "")
    return cleanup_list(value)

connection = open_database()
weather = get_weather(connection, "mod", "sunny")
print(weather)