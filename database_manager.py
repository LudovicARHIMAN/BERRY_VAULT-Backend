'''

Ce fichier permet de manipuler des données dans la base de donées => ajout d'utilisateurs et de mots de passes dans la db

'''
# Importation des modules 
import psycopg2 # permet d'utiliser une base de de donnée postgrès
import uuid # génere un id unique aléatoire pour chaque utilisateur 
import password # import le fichier 'password.py' qui lui gère le mot de passe mâtre et les mots de passes à stocker  

# connection à la base de donnée

#configuration de la db sous forme de dictionnaire
db_config = { 
    'dbname': 'postgres',
    'user': 'root',
    'password': 'root',
    'host': '192.168.1.140',
    'port': '32768'
}


#génere un id unique aléatoire pour chaque utilisateur 
def random_user_id():
    return str(uuid.uuid4())


def not_in_db(data,table,db):
    pass # regarde si une donnée n'ai pas dans la base de données








def add_user(login, master_password):
    user_id = random_user_id()  
    hashed = password.password_hash(master_password)

    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour insérer un utilisateur dans la table 'users'
        query = "INSERT INTO users (user_id, login, password_hash) VALUES (%s, %s, %s)"

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


def get_user_id(login):
    pass





def get__hashed_password_db(login,user_id):
    pass





add_user("login","masterpassword")