from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SelectField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    """add user form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    

class LoginForm(FlaskForm):
    """log in form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
    
class CustomizForm(FlaskForm):
    """customize your own item form """
    size_choice=[('S','Small'),('M','Medium'),('L','Large')]
    title=StringField("Title",validators=[InputRequired()])
    size = SelectField("Size",choices=size_choice)
    ingredients = StringField("Ingredients", validators=[InputRequired()])
    description=StringField("Description")
    image = StringField("Image_URL")
    