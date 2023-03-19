from random import choice
from flask import flash, redirect, render_template, request

from . import app, db
from .constants import CHARACTERS, LINK_LENGHT
from .forms import LinksForm
from .models import URLMap


def random_link():
    return ''.join(choice(CHARACTERS) for _ in range(LINK_LENGHT))


def validate_custom_id(custom_id):
    if len(custom_id) > 16:
        return False
    for symbol in custom_id:
        if symbol not in CHARACTERS:
            return False
    return True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinksForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        short = ''
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Cсылка {custom_id} уже занята')
                return render_template('index.html', form=form)
            elif not validate_custom_id(custom_id):
                flash('Предлагаемый вариант короткой ссылки должен состоять '
                      'только из латинских букв и цифр. Количество символов '
                      ' не должно превышать 16.')
                return render_template('index.html', form=form)
            else:
                short = custom_id
        if not short:
            short = random_link()
            while URLMap.query.filter_by(short=short).first():
                short = random_link()
        new_url = URLMap(original=form.original_link.data, short=short)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', form=form, url=new_url)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET', 'POST'])
def short_link_redirect(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
