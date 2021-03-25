from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo,ValidationError
from flask_api.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2 , max=20) ])
    username = StringField('Username', validators=[DataRequired(), Length(min=2 , max=20) ])
    password =  PasswordField ('Password', validators=[DataRequired()] )
    confirm_password =  PasswordField ('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user =  User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Ce username est déja prit , choissez en un autre')
        
            

class LoginForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired()])
    password =  PasswordField ('Password',validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login ')
    
        