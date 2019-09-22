from flask_wtf import FlaskForm as Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import login_user, logout_user, \
    login_required, current_user
from project.models import User, Groups


class WalletForm(Form):
    wallet = TextField('wallet', validators=[DataRequired()])
    sum = IntegerField('sum', validators=[DataRequired()])

    def validate(self):
        initial_validation = super(WalletForm, self).validate()
        if not initial_validation:
            return False
        if current_user.balance < self.sum.data:
            self.sum.errors.append("Insufficient funds")
            return False
        return True


class GroupidFrom(Form):
    ids = TextField('ids')


class GroupsForm(Form):
    cookie = TextField('cookie', validators=[DataRequired()])
    Group_id = TextField('Group_id', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[DataRequired()])

    login_proxy = TextField('login_proxy')
    password_proxy = TextField('password_proxy')
    ip_proxy = TextField('ip_proxy')
    port = TextField('port')

    def validate(self):
        initial_validation = super(GroupsForm, self).validate()
        if not initial_validation:
            return False
        return True


class LoginForm(Form):
    login = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(login=self.login.data).first()
        if not user:
            self.login.errors.append("Login not registered")
            return False
        return True


class RegisterForm(Form):
    login = TextField(
        'login',
        validators=[DataRequired(), Length(min=3, max=20)])
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        user = User.query.filter_by(login=self.login.data).first()
        if user:
            self.login.errors.append("Login already registered")
            return False
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )