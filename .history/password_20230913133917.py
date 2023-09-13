'''
Chiffrement et stockage du mot de passe maître, il permet aussi de gérer la comparaison de hash avec le mot de passe fournit en connexion
'''
# importation des modules 
import bcrypt # hash les mots de passe
import retriver


# hash le mot de passe maître pour le stocker dans la db
def password_hash(password):
    # Genere un "salt" qui permet de différentier des mots de passes au cas ou 2 utilisateurs on le même mot de passe
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    return hashed_password.decode('utf-8')



# vérifie si le mot de passe que l'on donne est le mot de passe stocker dan la db, si on donne le bon login et mot de passe on peux se connecter 
def login_check(login, input_password): 
    # recup l' user_id depuis la db de l'utilisateur donné par le client 
    user_id = retriver.get_userid(login) 

    # recupère le mot de passe hashé depuis la db
    hashed_password = retriver.get_hashed_password(user_id, login) 

    # Regarde si le nom d'utilisateur qui est prompt par le cient existe et si le mot de passe donné correspond au hash dans la db
    if retriver.get_userid(login) == None or ( bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8')))  == False:
        return False

    return True    


