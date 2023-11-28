"""Flask app for happy coffee"""
from flask import Flask, flash,request,json, jsonify, redirect,render_template,url_for
from models import connect_db,db,User,Customize,Product,Favorite
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from forms import RegisterForm,LoginForm,CustomizeForm,EditUserForm
from sqlalchemy.exc import IntegrityError
from models import User,Product,Favorite
import requests
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
 #app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///happy_coffee'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://fozucbun:JraCb-1BH17RtDz1BeLtbHrWWjJf7Vl8@bubble.db.elephantsql.com/fozucbun"
app.config['SQLCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']="Hello123"


debug = DebugToolbarExtension(app)
app.debug = True
app.app_context().push()
connect_db(app)


login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
def get_user(user_id):
    return User.query.get(int(user_id))
@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login first.', 'danger')
    
    return redirect(url_for('login'))

login_manager.login_view = 'login'

########################################
##### home page route ##################

@app.route('/')
def index():
    """index"""
   
    return render_template('index.html')
@app.route('/home')
def homepage():
    """homepage"""
    
    return render_template('home.html')


##############################################
#############User routes#####################

@app.route('/register', methods=["GET","POST"])
def register():
    """show form for creating a user"""
    # if the cur user is logged in, redirect user to home page
           
    form = RegisterForm()
    try:
        if form.validate_on_submit():
            user=User.register(form.data)
            
            db.session.commit()
            login_user(user)
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect('/home')
    except IntegrityError as err:
        err_info = jsonify(err.orig.args[0]).get_json()
        
        if "users_username_key" in err_info:
            flash('Username already taken.', 'danger')
        if "users_email_key" in err_info:
            flash('Email already taken.', 'danger')
    
    return render_template('/user/register.html', form=form)  
    
@app.route('/login', methods=["GET","POST"])
def login():
    """render the user to login page"""
   
    form = LoginForm()
    if form.validate_on_submit():
        user= User.authenticate(form.username.data,form.password.data)
        if user:
            login_user(user,remember=True)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/home")
        flash('Invalid username/password',"danger")
            
            
    return render_template('/user/login.html', form=form)    
    
@app.route('/logout')
@login_required
def logout():
    """handle loging out a user, remove user from session"""    
       
    
    logout_user()
    flash("You have been loged out!! Thank you!","success")
    return redirect('/')
@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show user details page."""
    
    user = User.query.get_or_404(user_id)
    
    return render_template('/user/details.html', user=user)


@app.route('/users/delete', methods = ["POST"])
@login_required
def delete_user():
    user=User.query.get_or_404(current_user.id)
    
    logout_user()
    db.session.delete(user)
    
    db.session.commit()
    
    flash('Your Account Has Been DELETED',"info")
    
    return redirect('/home')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Update info for current user."""
    
    user = User.query.get_or_404(user_id)   
    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        
        db.session.commit()
        
        flash(f"{user.username}'s info has been updated.", 'info')
        
        return redirect(url_for('user_details', user_id=user_id))
    
    return render_template('/user/edit_user.html', form=form, user=user)


@app.route('/users/<int:user_id>/favorite',methods=["GET"])
@login_required
def show_favorites(user_id):
    """gets all the coffee that a user liked"""
    user= User.query.get_or_404(user_id)
    
   
    return render_template('/user/favorite.html',user=user,favorites=user.favorites)

    
###################################################
########### Coffee routes########################

@app.route('/hot')
def show_hot_coffee():
    """show lists of hot coffee"""            
    all_data = Product.query.filter_by(type="hot")
    
    return render_template('/product/show_hot_coffee.html',all_data=all_data)

@app.route('/iced')
def show_iced_coffee():
    """show list of iced coffee"""
    all_data = Product.query.filter_by(type="iced")
    return render_template('/product/show_iced_coffee.html',all_data=all_data)

@app.route('/product/<int:id>')
def show_details(id):
    """show detail of indivitual coffee"""
    
    product = Product.query.get_or_404(id)
    
    return render_template('/product/details.html',product=product)
        
############################################
##### customize route ####################
@app.route('/customize',methods=["GET"])
@login_required
def customize():
    """process to the form"""
    all_coffee= Customize.query.filter(Customize.user_id == current_user.id).all()
    print(all_coffee)
    print(current_user)
    
    form = CustomizeForm()
    return render_template('/product/add_item.html',form=form,all_coffee=all_coffee)


@app.route('/api/coffee/<int:coffee_id>')
def show_coffee(coffee_id):
    """show individual coffee and return json {}"""
    coffee = Customize.query.get_or_404(coffee_id)
    return render_template('/product/coffee_detail.html',product=coffee)
@app.route('/api/coffee',methods=["POST"])

def create_coffee():
    """create your own item"""
    all_coffee = Customize.query.filter(Customize.user_id == current_user.id).all()
    # form =CustomizeForm()
    data = request.form
       
        
    new_item = Customize(title=data['title'],
                               type=data['type'],
                            ingredients=data['ingredients'],
                            image=data['image'],
                   
                  description=data['description'],
                  user_id=current_user.id)
        
    db.session.add(new_item)
    db.session.commit()
    print(new_item)
    serialized = jsonify(new_item.serialize_coffee())
    # return (jsonify(coffee = serialized),201)
    return redirect('/customize')

@app.route('/api/coffee/<int:id>', methods=['DELETE'])
def delete_coffee(id):
    coffee = Customize.query.get_or_404(id)
    db.session.delete(coffee)
    db.session.commit()
    return jsonify(message="Delete")

 
##############################################
######### favorites route ####################

@app.route('/coffee/<int:product_id>/favorite', methods=["POST"])
@login_required
def favorite_product(product_id):
    """toggle favorite coffee for logged in user and add or remove favorite from favoriteCoffee"""
    user = User.query.get_or_404(current_user.id)
    favorite_product = Product.query.get_or_404(product_id)
    user_favorites = db.session.query(Product).join(Favorite).filter(Favorite.user_id==user.id).all()
    if favorite_product in user_favorites:
        user_favorites= [ favorite for favorite in user_favorites if favorite != favorite_product]
        favorite= Favorite.query.filter(Favorite.product_id == favorite_product.id) .first()
        db.session.delete(favorite)
    else: 
        user_favorites.append(favorite_product)
        new_favorite = Favorite(product_id=favorite_product.id,user_id=user.id)
        db.session.add(new_favorite)
    db.session.commit()
    
    return redirect(url_for('show_favorites',user_id=user.id))
