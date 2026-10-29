import hashlib
import secrets
import json
import os

DB_FILE = "users.json"

SCRYPT_N = 2 ** 14
SCRYPT_R = 8 
SCRYPT_P = 1 


def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def hash_password(password, salt):
    pwd_bytes = password.encode("utf-8")
    hash_bytes = hashlib.scrypt(
        pwd_bytes,
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return hash_bytes.hex()


def register(username, password):
    db = load_db()

    if username in db:
        return False, "User already exists"

    salt = secrets.token_bytes(32)
    pwd_hash = hash_password(password, salt)

    db[username] = {
        "salt": salt.hex(),
        "hash": pwd_hash,
    }
    save_db(db)
    return True, "Registration successful"


def login(username, password):
    db = load_db()

    if username not in db:
        return False, "User not found"

    salt = bytes.fromhex(db[username]["salt"])
    stored_hash = db[username]["hash"]

    pwd_hash = hash_password(password, salt)

    if secrets.compare_digest(pwd_hash, stored_hash):
        return True, "Login successful"
    return False, "Wrong password"


if __name__ == "__main__":
    print("AUTH SYSTEM TESTS")

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    print("\n Registration ")
    print(register("alice", "password123"))
    print(register("bob", "hunter2"))
    print(register("alice", "another_pass"))

    print("\n Login (correct password) ")
    print(login("alice", "password123"))
    print(login("bob", "hunter2"))

    print("\n Login (wrong password) ")
    print(login("alice", "wrongpass"))
    print(login("bob", "hunter3"))

    print("\n Login (unknown user) ")
    print(login("charlie", "whatever"))

    print("\n Stored data ")
    db = load_db()
    for user, info in db.items():
        print(f"  {user}:")
        print(f"    salt: {info['salt'][:32]}...  ({len(info['salt'])//2} bytes)")
        print(f"    hash: {info['hash'][:32]}...")

    print("\nSame password, different salt => different hash")
    register("dave1", "same_password")
    register("dave2", "same_password")
    db = load_db()
    print(f"  dave1 hash: {db['dave1']['hash'][:32]}...")
    print(f"  dave2 hash: {db['dave2']['hash'][:32]}...")
    print(f"  Hashes equal? {db['dave1']['hash'] == db['dave2']['hash']}")