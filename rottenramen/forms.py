from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rottenramen.models import User
from flask_login import current_user


class FormCreatAccount(FlaskForm):
    username = StringField('Nome do usúario', validators=[DataRequired(), Length(5, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmation_password = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('password')])
    button_submit_creataccount = SubmitField('Criar Conta')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('Nome de usuário ja cadastrado. Tente novamente.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    remember_data = BooleanField('Lembrar dados de acesso')
    button_submit_login = SubmitField('Fazer Login')


class FormEditProfile(FlaskForm):
    username = StringField('Nome do usúario', validators=[DataRequired(), Length(5, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_photo = FileField('Atualizar a Foto do Perfil', validators=[FileAllowed(['jpg', 'png'])])
    button_submit_editprofile = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-mail já em uso por outro usuário. Cadastre outro e-mail.')

    def validate_username(self, username):
        if current_user.username != username.data:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError('Nome de usuário ja cadastrado. Tente novamente.')


class FormCreatPost(FlaskForm):
    body = TextAreaField('Escreva seu comentário aqui', validators=[DataRequired()])
    button_submit_post = SubmitField('Comentar')


