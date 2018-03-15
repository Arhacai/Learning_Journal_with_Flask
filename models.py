import datetime
import utils

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User already exists.")


class Entry(Model):
    title = CharField(max_length=200)
    slug = CharField(unique=True)
    date = DateField(default=datetime.datetime.now)
    time = IntegerField(default=0)
    learned = TextField()
    resources = TextField()
    tags = CharField(max_length=100)

    class Meta:
        database = DATABASE
        order_by = ('-date',)

    def save(self, *args, **kwargs):
        self.slug = utils.slugify(self.title)
        super(Entry, self).save(*args, **kwargs)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
