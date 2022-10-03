import random
import mysql.connector


def open_database():
    _connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='Nevermindme',
        autocommit=True)
    return _connection


def execute_sql(_connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    return values


def get_from_database(_connection, column, table, where):
    sql = "SELECT " + column + " FROM " + table + " " + where
    values = execute_sql(_connection, sql)
    return values


def cleanup_list(s):
    for i in range(len(s)):
        s[i] = str(s[i]).replace("'", "")
        s[i] = str(s[i]).replace("(", "")
        s[i] = str(s[i]).replace(")", "")
        s[i] = str(s[i]).replace(",", "")
    return s


def get_weather(_connection, _type, weather_name):
    if _type == "name":
        data_type = "name"
    elif _type == "mod":
        data_type = "modifier"
    else:
        data_type = "description"

    if weather_name == "":
        index = random.randint(1, 11)
    else:
        temp_index = get_from_database(_connection, "id",
                                       "weather", "where name = '" + weather_name + "'")
        temp_index = cleanup_list(temp_index)
        index = int(temp_index[0])
    values = get_from_database(_connection, data_type, "weather", "where id = '" + str(index) + "'")
    values = cleanup_list(values)
    return values[0]


connection = open_database()
weather = get_weather(connection, "desc", "")
print(weather)
