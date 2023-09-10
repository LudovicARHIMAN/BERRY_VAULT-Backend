'''
Chiffrement et stockage du mot de passe maître ainsi que des mot de passe à stocker
'''
# importation des modules 
import bcrypt # hash les mots de passe
import psycopg2 





# hash le mot de passe maître pour le stocker
def password_hash(master_password):
    
  
    # encode le mdp en utf-8
    bytes = master_password.encode('utf-8')
    
    # génère un salt du mdp, 
    salt = bcrypt.gensalt()
    
    # Hash le mot de pass
    hash = bcrypt.hashpw(bytes, salt)
  
    return hash




def password_ckeck(user_password):

    #hashed_password_from_db = .encode('utf-8') 

    password_match = bcrypt.checkpw(user_password)#,hashed_password_from_db )

    if password_match:
        # les mdp matchs, on autorise l'utilisateur à se login
        return True
    else:
         # les mdp ne matchs pas, on n'autorise pas l'utilisateur à se login
        return False


def vault_pass(vault_pass,KDF):
    pass # chiffre un mot de passe que l'on ajoute au vault, ce mot de passe sera chifré à partir d'une clé KDF