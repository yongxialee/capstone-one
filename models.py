from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
db = SQLAlchemy()
bcrypt = Bcrypt()
DEFAULT="https://qph.cf2.quoracdn.net/main-qimg-6d475776ad6b16125871fefffa388e5a-lq"
def connect_db(app):
    """connect to datatbase"""
    db.app=app
    db.init_app(app)
    
class User(db.Model,UserMixin):
    """user model"""
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username= db.Column(db.Text,nullable =False,unique=True)
    password = db.Column(db.Text,nullable =False)
    email = db.Column(db.String(),nullable=False,unique=True)
    
    
    favorites = db.relationship("Product",secondary="favorites",cascade="all,delete")
    customize = db.relationship("Customize")
   
    
    def __repr__(self) :
        return f"<User #{self.id}:{self.username},{self.email}>"
    @classmethod
    def register(cls,form):
        """register user with hashed password & return user"""
        # hashed = bcrypt.generate_password_hash(pwd)
        # # turn bytestring into normal (unicode utf8) string
        # hashed_utf8 = hashed.decode("utf8")

        # # return instance of user w/username and hashed pwd
        # return cls(username=username, password=hashed_utf8)
        hashed_pwd = bcrypt.generate_password_hash(form['password']).decode('UTF-8')

        user = User(
            username=form['username'],
            password=hashed_pwd,
            email=form['email']
        )
        db.session.add(user)
        
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = cls.query.filter_by(username=username).first()

        # if u and bcrypt.check_password_hash(u.password, pwd):
        #     # return user instance
        #     return u
        # else:
        #     return False
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
        
class Product(db.Model):
    """product model"""
    __tablename__="products"
  
    
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title =db.Column(db.Text,nullable =False)
    type = db.Column(db.Text) 
    description = db.Column(db.Text,nullable =False)
    ingredients=db.Column(db.Text,nullable=False)
    image = db.Column(db.Text,default=DEFAULT)
    
    # likes = db.relationship('DeckLikes', cascade='all, delete')
    user = db.relationship('User',secondary="favorites")
    # favorite = db.relationship("Favorite",backref="product")
    
    # @classmethod
    # def cold(cls,title,type,description,ingredients,image):
    #     return 
    
   
    
    
    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'type':self.type,
            'description':self.description,
            'ingredients': self.ingredients,
            'image':self.image
            
        }
        
    
class Favorite(db.Model):
    """favorite model"""
    __tablename__ = 'favorites' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='cascade'),
        
    )
    
    
class Customize(db.Model):
    """customze model"""
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable = False,unique=True)
    type = db.Column(db.Text,nullable =False)
    ingredients= db.Column(db.Text,nullable=False)
    description = db.Column(db.Text,nullable =False)
    image = db.Column(db.Text)
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete="CASCADE"),nullable=False
    )
    user=db.relationship('User')
    def serialize_coffee(self):
        """serialize coffee to json dict"""
        return {
            'id':self.id,
            'title':self.title,
            'type':self.type,
            'description':self.description,
            'ingredients': self.ingredients,
            'image':self.image
            
        }
    def __repr__(self) :
        return f"<Customize #{self.id}:{self.title},{self.type},{self.ingredients},{self.description},{self.image}>"