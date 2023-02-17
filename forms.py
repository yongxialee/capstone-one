from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SelectField,EmailField
from wtforms.validators import InputRequired,Email



class RegisterForm(FlaskForm):
    """add user form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    email = EmailField('Email', validators=[Email(message='Enter a valid email.')])

class LoginForm(FlaskForm):
    """log in form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
    
class CustomizeForm(FlaskForm):
    """customize your own item form """
    choice=[('Hot','Hot'),('Iced','Iced')]
    title=StringField("Title",validators=[InputRequired()],render_kw={"placeholder": "Title"})
    type = SelectField("Type",choices=choice)
    ingredients = StringField("Ingredients", validators=[InputRequired()],render_kw={"placeholder": "Ingredients"})
    description=StringField("Description",render_kw={"placeholder": "description"})
    image = StringField("Image_URL",render_kw={"placeholder": "Image_URL"})


class EditUserForm(FlaskForm):
    """Edit user info form."""
    
    username = StringField('Username', validators=[InputRequired(message='Enter a username.')])
    password = PasswordField("Password",validators=[InputRequired()])
    email = EmailField('Email', validators=[Email(message='Enter a valid email.')])