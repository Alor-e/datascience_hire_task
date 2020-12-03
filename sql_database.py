import mysql.connector
import csv

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='0011',
    database='recommender_db'
)

cursor = db.cursor()


def csv_to_database(directory):
    """
    Inserts product data from a csv file into the database.
    """
    product_csv = csv.reader(open(directory), delimiter=',')

    try:
        cursor.execute(
            '''CREATE TABLE product_info (
            id INT NOT NULL,
            links TEXT(65535) NOT NULL,
            product_name TEXT(65535) NOT NULL,
            product_brand VARCHAR(255),
            product_type VARCHAR(255),
            product_rating TEXT(65535),
            product_price TEXT(65535),
            image_link TEXT(65535),
            PRIMARY KEY(id))'''
        )
    except mysql.connector.errors.ProgrammingError:
        pass

    next(product_csv)

    try:
        for row in product_csv:
            cursor.execute('INSERT INTO product_info (id, links, product_name,\
                product_brand, product_type, product_rating, product_price,\
                image_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)

    except mysql.connector.errors.IntegrityError:
        pass

    db.commit()


csv_to_database('csv_files/database.csv')


def store_user_data(phone_number, link):
    """
    Inserts users phone number and corresponding url link into the database
    """
    try:
        cursor.execute(
            '''CREATE TABLE user_numbers (
            phone_number VARCHAR(255) NOT NULL UNIQUE,
            user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)'''
        )
    except mysql.connector.errors.ProgrammingError:
        pass

    try:
        cursor.execute(
            '''CREATE TABLE user_links (
            link_url VARCHAR(255) NOT NULL,
            link_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_num VARCHAR(255),
            FOREIGN KEY (user_num) REFERENCES user_numbers (phone_number))'''
        )
    except mysql.connector.errors.ProgrammingError:
        pass

    try:
        cursor.execute(
            'INSERT INTO user_numbers (phone_number) VALUES(%s)'
            % (phone_number))
    except mysql.connector.errors.IntegrityError:
        pass

    cursor.execute(
        'INSERT INTO user_links (link_url, user_num) VALUES("%s", %s)'
        % (link, phone_number))
    db.commit()


def fetch_cluster_rows(list_of_ids):
    """
    Fetches product data from specific rows and returns the data
    """
    format_strings = ','.join(['%s'] * len(list_of_ids))
    cursor.execute("SELECT * FROM product_info WHERE id IN (%s)" %
                   format_strings, tuple(list_of_ids))

    rows = cursor.fetchall()

    return rows
