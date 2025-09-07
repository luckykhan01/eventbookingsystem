from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login, app
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from time import time
import jwt


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False, default='user')

    bookings: so.Mapped[list["Booking"]] = so.relationship(back_populates="user",
                                                  cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms='HS256')['reset_password']
        except:
            return
        return db.session.get(User, id)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Event(db.Model):
    event_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    time: so.Mapped[datetime.time] = so.mapped_column(sa.Time, nullable=False)
    location: so.Mapped[str] = so.mapped_column(sa.String(30))
    total_seats: so.Mapped[int] = so.mapped_column()
    seats_left: so.Mapped[int] = so.mapped_column(default=0)
    created_by: so.Mapped[str] = so.mapped_column(sa.String(64))

    bookings: so.Mapped[list["Booking"]] = so.relationship(back_populates="event",
                                                           cascade="all, delete-orphan")

    def __repr__(self):
        return '<Event {}>'.format(self.title)


class Booking(db.Model):
    booking_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('event.event_id'))
    booked_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    user: so.Mapped["User"] = so.relationship(back_populates="bookings")
    event: so.Mapped["Event"] = so.relationship(back_populates="bookings")

    def __repr__(self):
        return '<User: {} Booking: {}>'.format(self.user_id, self.booking_id)