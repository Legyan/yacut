from http import HTTPStatus

from flask import jsonify, request

from . import app, db

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import validate_custom_id, random_link


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        custom_id = data.get('custom_id')
        if not validate_custom_id(custom_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        if not custom_id:
            data['custom_id'] = random_link()
    else:
        data['custom_id'] = random_link()
    data['original'] = data['url']
    data['short'] = data['custom_id']
    del data['url']
    del data['custom_id']
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    if not short_id:
        raise InvalidAPIUsage('Поле "short_id" является оязательным')
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
