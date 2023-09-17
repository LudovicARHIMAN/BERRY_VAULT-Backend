# PyPass-Backend
Backend for a password manager in python 

Secured (almost) password manager with master password hashed in bcrypt and vault crypted in AES-256-CBC using PostgresSQL as database 

<H2>How it works</H2>


**Account Creation:**
- To create an account, you need to provide a Login (email) and a strong 24-characters password (containing uppercase, lowercase, digits and special characters of course).

**Data Storage:**
- Once your account is created, we establish a personal table in our server's database to store all your passwords. This essentially serves as your personal vault.

**Master Password Security:**
- Your master password is securely hashed and stored in the database using the bcrypt algorithm

**Encryption and Decryption:**
- Your master password plays a crucial role in encrypting and decrypting the information within your vault. Each time you want to perform these actions, you'll be required to provide your master password.
- To ensure security, your master password generates a key using the PBKDF2 algorithm, which is then used for encrypting and decrypting information in your vault using AES-256-CBC.

**NO MASTER PASSWORD RECOVER**
- If you loose your master password you loose everything for ever :)   






Authors: ARHIMAN Ludovic, CAYAMBO Pierre, GRONDIN Dany
