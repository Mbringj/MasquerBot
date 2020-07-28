from datetime import datetime
from hashlib import sha512

from flask_sqlalchemy import SQLAlchemy
from ecies.utils import generate_eth_key

db = SQLAlchemy()


class UserAccount(db.Model):
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_hash = db.Column(db.Text(), unique=True, nullable=False)
    private_key = db.Column(db.Text(), unique=True, nullable=False)
    public_key = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, username):
        self.username_hash = sha512(bytes(username, "utf-8")).hexdigest()
        eth_k = generate_eth_key()
        self.private_key = eth_k.to_hex()
        self.public_key = eth_k.public_key.to_hex()
        self.updated_at = self.created_at = datetime.now()
        del eth_k


class EncryptionCache(db.Model):
    __tablename__ = "encryption_cache"
    chat_id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.Text(), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime())

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.created_at = datetime.now()
        self.message = None
        self.public_key = None


class DecryptionCache(db.Model):
    __tablename__ = "decryption_cache"
    chat_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.created_at = datetime.now()
