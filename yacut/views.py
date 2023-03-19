from flask import flash, redirect, render_template

from . import app, db
from .forms import LinksForm
from .models import URLMap
from .utils import random_link, validate_custom_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Создание для длинной ссылки соответствующей короткой ссылки"""
    form = LinksForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        short = ''
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Имя {custom_id} уже занято!')
                return render_template('index.html', form=form)
            elif not validate_custom_id(custom_id):
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('index.html', form=form)
            else:
                short = custom_id
        if not short:
            short = random_link()
        new_url = URLMap(original=form.original_link.data, short=short)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', form=form, url=new_url)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_link_redirect(short):
    """Перенаправление с короткой ссылки на оригинальную ссылку"""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
