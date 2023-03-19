from random import choice

from .constants import CHARACTERS, LINK_LENGHT
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
