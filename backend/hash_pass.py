import bcrypt

plain_password = "angelo125"
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

print("Hashed Password:", hashed_password.decode('utf-8'))
