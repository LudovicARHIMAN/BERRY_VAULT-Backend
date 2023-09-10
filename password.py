'''
Chiffrement et stockage du mot de passe maître ainsi que de gérer la comparaison de hash avec le mot de passe fournit en connexion
'''
# importation des modules 
import bcrypt # hash les mots de passe
import retriver


# hash le mot de passe maître pour le stocker dans la db
def password_hash(password):
    # Genere un "salt" qui permet de différentier des mot de passe au cas ou 2 utilisateur on le même mot de passe
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    return hashed_password.decode('utf-8')



# regarde si le mot de passe que l'on donne et le mot de passe est bien le bon, si on donne le bon login et mot de passe on peux se connecter 
def login_check(login, input_password): 

    user_id = retriver.get_userid(login)

    hashed_password = retriver.get_hashed_password(user_id, login) # recupère le mot de passe hashé depuis la db

    # Check if the input password matches the hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

