from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, url_for

from additional.classes import OlympiadsAll, Olympiad

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

olympiads_all = OlympiadsAll()
olymps_all_dict = olympiads_all.get_all_olymp_dict()
olymps_all_list = olympiads_all.get_all_olymp_list()


class LoginForm(FlaskForm):
    username = StringField('id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username1 = StringField('id капитана', validators=[DataRequired()])
    password1 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class ClassForm(FlaskForm):
    number_class = IntegerField('Номер класса', validators=[DataRequired()])
    submit = SubmitField('Искать')


@app.route('/subjects/<sub>', methods=['GET', 'POST'])
def main(sub):
    class_num = 'all'
    url_style = url_for('static', filename='css/style.css')
    class_form = ClassForm()
    if class_form.validate_on_submit():
        class_num = class_form.number_class.data

    olymps_dict = {}
    for subj, olymps in olymps_all_dict.items():

        if sub != 'all' and subj != sub:
            continue

        if class_num != 'all':
            for i in olymps:
                print(type(i.sch_class), type(class_num))
            olymps = list(filter(lambda x: int(x.sch_class) == class_num, olymps))
        olymps_dict[subj] = olymps

    return render_template('main.html', url_style=url_style, olymps_all_dict=olymps_dict,
                           class_form=class_form, subject=sub, class_num=class_num)


@app.route('/olympiad/<int:olymp_id>')
def olympiad(olymp_id):
    print('зашел')
    olymp = list(filter(lambda x: x.id == int(olymp_id), olymps_all_list))[0]
    return render_template('olymp.html', olymp=olymp, subject=olymp.subject)


@app.route('/olympiad-change/<int:olymp_id>')
def olympiad_change(olymp_id):
    print('зашел')
    olymp = list(filter(lambda x: x.id == int(olymp_id), olymps_all_list))[0]
    return render_template('olymp.html', olymp=olymp, subject=olymp.subject)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
