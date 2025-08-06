from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Event(db.Model):
    event_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    location: so.Mapped[str] = so.mapped_column(sa.String(30))
    total_seats: so.Mapped[int] = so.mapped_column()
    seats_left: so.Mapped[int] = so.mapped_column()
    created_by: so.Mapped[str] = so.mapped_column(sa.String(64))

