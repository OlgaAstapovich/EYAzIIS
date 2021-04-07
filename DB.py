import mysql.connector


def connect():
    database = mysql.connector.connect(
        user='root',
        password='Bkk.vbyfwbz813924',
        host='localhost',
        database='dictionaries')
    return database


def create_table(name, *args):
    database = connect()
    my_cursor = database.cursor()
    my_cursor.execute(
        "CREATE TABLE {} (word VARCHAR(30), frequency_of_appearance FLOAT, additional_information VARCHAR(50), PRIMARY KEY (word));".format(
            name))
    database.commit()
    database.close()


def add_word(DB_table_name, word, frequency, additional_info):
    database = connect()
    my_cursor = database.cursor()
    my_cursor.execute(
        "INSERT INTO {} VALUES('{}', {}, '{}');".format(
            DB_table_name,
            word,
            frequency,
            additional_info))
    database.commit()
    database.close()


def load_table(DB_table_name, view_table):
    database = connect()
    my_cursor = database.cursor()
    my_cursor.execute(
        "SELECT word, frequency_of_appearance, additional_information FROM {};".format(DB_table_name))
    rows = my_cursor.fetchall()
    for row in rows:
        view_table.insert("", "end", values=row)
    database.close()


def save_table(DB_table_name, view_table):
    for item in view_table.get_children():
        add_word(DB_table_name, view_table.item(item)["values"][0:1][0], view_table.item(item)["values"][1:2][0],
                 view_table.item(item)["values"][2:3][0])


if __name__ == "__main__":
    # create_table("my_test_dictionary")
    add_word("my_test_dictionary", "word", 3245, "information")
