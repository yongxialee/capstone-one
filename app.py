"""Flask app for happy coffee"""
from flask import Flask, flash,request, jsonify,session, g, redirect,render_template
from models import connect_db,db,User,Customize,Product
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm,LoginForm,CustomizForm
from sqlalchemy.exc import IntegrityError
from models import User,Product,Favorite
import requests

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///happy_coffee'
app.config['SQLCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']="Hello123"
debug = DebugToolbarExtension(app)
app.debug = True
app.app_context().push()
connect_db(app)


API_BASE_URL="https://api.sampleapis.com/coffee"
CURR_USER_KEY="curr_user"
@app.before_request
def add_user_to_g():
    """if we're logged in, add current user to Flask global"""
    if CURR_USER_KEY in session:
        g.user =User.query.get(session[CURR_USER_KEY])
    else:
        g.user=None
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
   

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def index():
    """index"""
    return render_template('index.html')
@app.route('/home')
def homepage():
    """homepage"""
    return render_template('home.html')

@app.route('/register', methods=["GET","POST"])
def register_user():
    """show form for creating a user"""
    # if the cur user is logged in, redirect user to home page
    if g.user:
        return redirect('/')
    else: 
        
        form = UserForm()
        if form.validate_on_submit():
            try:
                user= User.register(
                    username=form.username.data,
                    password = form.password.data
                )
                db.session.commit()
            except IntegrityError:  # if the input is invalid, notify the user and rerender the page
                flash("Username is already taken","danger")
                return render_template('register.html', form=form)
            except ValueError:
                flash("Please enter a valid username/password","danger")
                return render_template('register.html',form=form)
            do_login(user)
        
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect('/home')
        # if it's GET request, render register form
        return render_template('register.html',form = form)
    
@app.route('/login', methods=["GET","POST"])
def login_user():
    """render the user to login page"""
   
    form = LoginForm()
    if form.validate_on_submit():
        user= User.authenticate(form.username.data,form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/home")
            flash('Invalid username/password',"danger")
            
            
    return render_template('login.html', form=form)    
    
@app.route('/logout')
def logout_user():
    """handle loging out a user"""    
       
    
    do_logout()
    flash("You have been loged out!! Thank you!","success")
    return redirect('/')


    

@app.route('/hot')
def show_hot_cofee():
    res = requests.get(f"{API_BASE_URL}/hot")
    all_data = res.json()
    print(all_data)
    
    
    # for item in all_data:
        
    # for item in all_data:
       
    #             id=item['id']
    #             title = item['title']
    #             ingredients=item['ingredients']
    #             image=item['image']
    #             description =item['description']
            
    #             product = Product(id=id,title=title,ingredients=ingredients,
    #                   image=image,description=description)
    #             # db.session.add(product)
    #             # db.session.commit()
    #             # session.append('item')
            
    
    
    return render_template('show_hot_coffee.html',all_data=all_data)
@app.route('/hot/<int:id>')
def show_hot_details(id):
    """show detail of indivitual coffee"""
    
    # data = requests.get(f"{API_BASE_URL}/hot", id=id)
    # all_data=data.json()
    product = Product.query.get_or_404(id)
    return render_template('details.html',product=product)
        
@app.route('/iced')
def show_iced_cofee():
    res = requests.get(f"{API_BASE_URL}/iced")
    data = res.json()

    return render_template('show_iced_coffee.html',all_data=data)
@app.route('/iced/<int:id>')
def show_iced_details(id):
    """show detail of indivitual coffee"""
    
    
    p = Product.query.get_or_404(id)
    return render_template('details.html',p=p)

@app.route('/customize',methods=["GET","POST"])
def create_item():
    """create your own item"""
    
    form = CustomizForm()
    if form.validate_on_submit():
        c = Customize(title=form.title.data,
                      
                      ingredients=form.ingredients.data,
                      image=form.image.data,
                      description=form.description.data)
    
        db.session.add(c)
        db.session.commit()
        return redirect('/')
    return render_template('customize.html', form=form)