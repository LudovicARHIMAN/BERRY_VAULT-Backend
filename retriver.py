'''
Ce fichier se charge de retrouver des valeurs précises dans la db pour les réutiliser ailleurs
'''
import psycopg2 

#configuration de la db sous forme de dictionnaire
db_config = { 
    'dbname': 'postgres',
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '32768'
}



# recupère le hash du mot de passe de l'utilisateur depuis la db
def get_hashed_password(user_id, login):
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour récupérer le mot de passe haché en fonction de user_id et login
        query = "SELECT master_password_hash FROM users WHERE user_id = %s AND login = %s"

        # Définir les valeurs pour user_id et login
        values = (user_id, login)

        # Exécuter la requête
        cursor.execute(query, values)

        # Récupérer le résultat (en supposant que vous attendez un seul résultat)
        result = cursor.fetchone()

        if result:
            # Le mot de passe hashé se trouve dans la première (et unique) colonne du résultat
            hashed_password = result[0]
            return hashed_password

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée (par exemple, la journaliser, lever une exception)
        print("Erreur SQL :", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    # Retourner None si aucun mot de passe haché n'est trouvé
    return None



# get user_id from login
def get_userid(login):
    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour récupérer le user_id depuis le login
        query = "SELECT user_id FROM users WHERE login = %s"

        # Passez le login en tant que tuple (même s'il s'agit d'une seule valeur)
        values = (login,)

        # Exécuter la requête
        cursor.execute(query, values)

        # Récupérer le résultat
        result = cursor.fetchone()

        if result:
            # Le user_id se trouve dans la première (et unique) colonne du résultat
            user_id = result[0]
            return user_id

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée (par exemple, la journaliser, lever une exception)
        print("Erreur SQL :", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Retourner None si aucun user_id correspondant n'est trouvé
    return None



# recupère la clé de chiffrement/déchiffrement utilisé pour l'utilisateur 
def get_aes_key(login):
    try:
        user_id = get_userid(login)
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT key_bytes FROM aes_keys WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        aes_key = cursor.fetchone()

        if aes_key:
            # Convert from bytea to bytes
            return bytes(aes_key[0])
        else:
            return None

    except psycopg2.Error as error:
        print("SQL Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


