import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def save_master_password(password):
    with open("file.txt", "w") as masterpass:
        masterpass.write(hash_password(password))


save_master_password("HEllo")