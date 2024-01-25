'''
Ce fichier permet de centraliser la config poour la db pour les autres fichiers, afin de modifier les paramètres de connexion à un seul endroit 
Il permet aussi de créer les tables indispensables 
'''
import psycopg2



db_config = { 
    'dbname': 'postgres',
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': '5432'
}


def create_users_table():
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour créer une table en fonction du nom de l'utilisateur
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY NOT NULL,
                login VARCHAR(255) NOT NULL,
                master_password_hash VARCHAR(255) NOT NULL
            );
        '''

        # Execute la requête 
        cursor.execute(query)
        connection.commit()

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL: ", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def create_aes_key_table():
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour créer une table en fonction du nom de l'utilisateur
        query = '''
            CREATE TABLE IF NOT EXISTS aes_keys (
                user_id uuid PRIMARY KEY,
                key_bytes bytea,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        '''

        # Execute la requête 
        cursor.execute(query)
        connection.commit()

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL: ", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# table individuel nommé en fonction de l'utilisateur qui stocke les mots de passe des utilisateurs
def create_vault_table(table_name):

    table_name = table_name+"'s Personal Vault"

    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour créer une table en fonction du nom de l'utilisateur
        query = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                user_id uuid,
                pass_name VARCHAR(255) PRIMARY KEY,
                login VARCHAR(255),
                password VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        '''

        # Execute la requête 
        cursor.execute(query)
        connection.commit()

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL: ", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def init():

    '''
    Cette fonction permet d'appeler les autres fonctions pour créer toutes les tables nécessaires pour constituer la db
    '''

    return create_aes_key_table(), create_users_table()




