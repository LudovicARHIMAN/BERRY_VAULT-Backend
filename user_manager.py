'''
Ce fichier permet de manipuler des données dans la base de donées => ajout d'utilisateurs
'''
import psycopg2 # permet d'utiliser une base de de donnée postgrès
import uuid # génere un id unique aléatoire pour chaque utilisateur 
import password # import le fichier 'password.py' qui lui gère le mot de passe mâtre et les mots de passes à stocker  
import valt_manager
import retriver

#configuration de la db sous forme de dictionnaire
db_config = { 
    'dbname': 'postgres',
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '32768'
}



# génere un id unique aléatoire pour chaque utilisateur 
def random_user_id():
    return str(uuid.uuid4())



# vérifie que le login ne soit pas dans la db 
def user_exist(login):
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour vérifier si le login existe
        query = "SELECT 1 FROM users WHERE login = %s"

        # Passez le login en tant que tuple (même s'il s'agit d'une seule valeur)
        values = (login,)

        # Exécuter la requête
        cursor.execute(query, values)

        # Vérifiez si des lignes ont été renvoyées (le login existe)
        if cursor.fetchone():
            return True
        else:
            return False

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée (par exemple, la journaliser, lever une exception)
        print("Erreur SQL :", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Retourner False en cas d'erreur ou si le login n'existe pas
    return False



# Ajoute un utilisateur avec comme attribut (user_id,login,master_password)
def add_user(login, master_password):
    user_id = random_user_id()
    hashed = password.password_hash(master_password) # hash le mot de passe maître

    if user_exist(login) == False:

        try:
            # Établir une connexion à la base de données
            connection = psycopg2.connect(**db_config)

            # Créer un objet curseur
            cursor = connection.cursor()

            # Définir la requête SQL pour insérer un utilisateur dans la table 'users'
            query = "INSERT INTO users (user_id, login, master_password_hash) VALUES (%s, %s, %s)"

            # Définir les valeurs à insérer dans la table
            values = (user_id, login, hashed)

            # Exécuter la requête
            cursor.execute(query, values)

            # Valider la transaction
            connection.commit()

        except psycopg2.Error as error:
            # Gérer l'erreur de manière appropriée (par exemple, la journaliser, lever une exception)
            print("Erreur SQL :", error)
        
        finally:
            # Toujours fermer le curseur et la connexion, même en cas d'erreur
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return False



def add_aes_key(login):

    user_id = retriver.get_userid(login)

    key = valt_manager.random_AES_key()

    
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour insérer un utilisateur dans la table 'users'
        query = "INSERT INTO user_key (user_id, key) VALUES (%s, %s)"

        # Définir les valeurs à insérer dans la table
        values = (user_id,key)

        # Exécuter la requête
        cursor.execute(query, values)

        # Valider la transaction
        connection.commit()

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée (par exemple, la journaliser, lever une exception)
        print("Erreur SQL :", error)
    
    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return False


