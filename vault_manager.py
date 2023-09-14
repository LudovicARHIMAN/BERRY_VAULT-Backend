'''
Gère le chiffrement/déchifrement (AES256 avec une clé génére à partir du mot de passe [PWKDF2]) des mots de passes dans le vault en AES-256-CBC ansi que le stockage des mots de passe
'''
import psycopg2
from db_config import db_config
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode
import hashlib
import os
import hmac

# Define a function to derive a key from a password using PBKDF2
def derive_key(password, salt=None):
    if salt is None:
        salt = get_random_bytes(16)  # Generate a random salt
    # Use PBKDF2 with HMAC-SHA256 to derive the key
    key = PBKDF2(
        password.encode('utf-8'),
        salt,
        dkLen=32,  # AES-256 requires a 256-bit key
        count=100000,  # Number of iterations (adjust as needed)
        prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest()
    )
    return key, salt

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
    iv = ciphertext_bytes[:16]  # Extract the IV
    ciphertext_bytes = ciphertext_bytes[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
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



def display_password(pass_name,key, table_name):


    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour vérifier si le login existe
        query = f'SELECT password FROM "{table_name}" WHERE pass_name = %s'

        # Passez le login en tant que tuple (même s'il s'agit d'une seule valeur)
        values = (pass_name,)
        
        # Exécuter la requête
        cursor.execute(query, values)

        # Récupérer le résultat
        result = cursor.fetchone()

        if result:
            # Le user_id se trouve dans la première (et unique) colonne du résultat
            password = result[0]
            return decrypt_AES_CBC_256(key, password)

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL :", error)

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Retourner False en cas d'erreur ou si le login n'existe pas
    return False



def display_login(pass_name,key, table_name):



    try:
        # Établir une connexion à la base de données
        connection = psycopg2.connect(**db_config)

        # Créer un objet curseur
        cursor = connection.cursor()

        # Définir la requête SQL pour vérifier si le login existe
        query = f'SELECT login FROM "{table_name}" WHERE pass_name = %s'

        # Passez le login en tant que tuple (même s'il s'agit d'une seule valeur)
        values = (pass_name,)
        
        # Exécuter la requête
        cursor.execute(query, values)

        # Récupérer le résultat
        result = cursor.fetchone()

        if result:
            # Le user_id se trouve dans la première (et unique) colonne du résultat
            login = result[0]
            return decrypt_AES_CBC_256(key, login)

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL :", error)


# Derive the key and salt
key, salt = derive_key("Password")

to_encrypt = "message_secret"

# Encrypt the message using the derived key
encrypted_message = encrypt_AES_CBC_256(key, to_encrypt)

print(encrypted_message)

decrypt = decrypt_AES_CBC_256(key, encrypted_message)

print(decrypt)