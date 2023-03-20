from random import choice
from sqlalchemy.exc import SQLAlchemyError

from . import app, db
from .constants import CHARACTERS, LINK_LENGHT
from .error_handlers import DatabaseError
from .models import URLMap


def random_link():
    """Получение уникальной случайной короткой ссылки"""
    unique_link = ''.join(choice(CHARACTERS) for _ in range(LINK_LENGHT))
    while URLMap.query.filter_by(short=unique_link).first():
        unique_link = ''.join(choice(CHARACTERS) for _ in range(LINK_LENGHT))
    return unique_link


def validate_custom_id(custom_id):
    """Валидация предложенной пользователем короткой ссылки"""
    if len(custom_id) > 16:
        return False
    for symbol in custom_id:
        if symbol not in CHARACTERS:
            return False
    return True


def add_to_database(*args):
    try:
        with app.app_context():
            for url in args:
                db.session.add(url)
            db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise DatabaseError('Ошибка при добавлении ссылки в базу данных')
