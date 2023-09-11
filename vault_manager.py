'''
Gère le chiffrement/déchifrement () des mots de passes dans le vault en AES-256-CBC ansi que le stockage des mots de passe
'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import retriver
import psycopg2


#configuration de la db sous forme de dictionnaire
db_config = { 
    'dbname': 'postgres',
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '32768'
}


# Code incomprehensible de stackoverflow pour encoder et décoder en AES-256-CBC
# Define a function to generate a random AES key
def random_AES_key():
    return get_random_bytes(32)  


# Define the encryption function
def encrypt_AES_CBC_256(key, message):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext_bytes = cipher.encrypt(padded_message)
    ciphertext = b64encode(iv + ciphertext_bytes).decode('utf-8')
    return ciphertext


# Define the decryption function
def decrypt_AES_CBC_256(key, ciphertext):
    ciphertext_bytes = b64decode(ciphertext)
    iv = ciphertext_bytes[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_bytes = ciphertext_bytes[AES.block_size:]
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    plaintext_bytes = unpad(decrypted_bytes, AES.block_size)
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext

# définit la fonction qui va chiffrer les logins, mots de passes 
'''
Chaques utilisateurs aura sa propre table pour gerer les mots de passes du vault la table user_login aura comme attributs : 

user_id = identifier à qui appartient le mot de passe
login = login du mot de passe que l'on souhaite stocker 
password = mot de passe à stocker
pass_name = nom du mot de passe permet de donner un nom au mot de passe pour le retrouver plus tard (ex : gamail_1 )

key en argument permet de chiffrer les mots de passes 
table_name =  créer une table au nom de l'utilisateur

Example: pour stocker le mot de passe gmail_1 avec comme login = "bob" et comme password = "secret" 
'''

# table individuel nommé en fonction de l'utilisateur qui stocke les mots de passe des utilisateurs
def create_vault_table(table_name):
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


def store_password(user_id, pass_name,login, password,key, table_name):
    
    # Chiffre le login et password utilisant la clé de l'utilisateur
    login_crypted = encrypt_AES_CBC_256(key, login)
    pass_crypted = encrypt_AES_CBC_256(key, password)

    try:
        # Connection à la db 
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Requête SQ pour ajouter des valeurs dans la table
        query = f'INSERT INTO "{table_name}" (user_id, pass_name, login, password) VALUES (%s, %s, %s, %s)'


        # Definies les valeurs à ajouter dans la table sous forme tuples
        values = (user_id, pass_name, login_crypted, pass_crypted)

        # Execute la requête
        cursor.execute(query, values)
        connection.commit()

    except psycopg2.Error as error:
        print("Erreur SQL: ", error)
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()












'''

# message_to_encrypt = "password"
encrypted_message = "C7XGVZ9P0XVKYY07OutBaubtNqRAj5Pt3/Nz8Xw9SZ8="
print("Encrypted:", encrypted_message)

decrypted_message = decrypt_AES_CBC_256(key, encrypted_message)
print("Decrypted:", decrypted_message)
'''