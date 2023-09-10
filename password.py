'''
Chiffrement et stockage du mot de passe maître ainsi que de gérer la comparaison de hash avec le mot de passe fournit en connexion
'''
# importation des modules 
import bcrypt # hash les mots de passe
import retriver




# hash le mot de passe maître pour le stocker
def password_hash(master_password):
    
  
    # encode le mdp en utf-8
    bytes = master_password.encode('utf-8')
    
    # génère un salt du mdp, 
    salt = bcrypt.gensalt()
    
    # Hash le mot de pass
    hash = bcrypt.hashpw(bytes, salt)
  
    return hash



# regarde si le mot de passse que l'on donne lors de la connexion est identique (au hash) à celui dans la db
def password_check(user_id, login, prompted_password):
    hashed_password_from_db = retriver.get_hashed_password(user_id, login)

    # Encode the prompted_password as bytes
    prompted_password_bytes = prompted_password.encode('utf-8')

    password_match = bcrypt.checkpw(prompted_password_bytes, hashed_password_from_db.encode('utf-8'))

    if password_match:
        # The passwords match; allow the user to log in
        return True
    else:
        # The passwords do not match; do not allow the user to log in
        return False




