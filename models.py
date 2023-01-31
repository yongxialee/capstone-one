from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """connect to datatbase"""
    db.app=app
    db.init_app(app)
    
class User(db.Model):
    """user model"""
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username= db.Column(db.Text,nullable =False,unique=True)
    password = db.Column(db.Text,nullable =False)
    
    
    favorite = db.relationship("Favorite", backref = "user",cascade="all,delete")
    customize = db.relationship("Customize")
    @classmethod
    def register(cls,username,password):
        """register user with hashed password & return user"""
        # hashed = bcrypt.generate_password_hash(pwd)
        # # turn bytestring into normal (unicode utf8) string
        # hashed_utf8 = hashed.decode("utf8")

        # # return instance of user w/username and hashed pwd
        # return cls(username=username, password=hashed_utf8)
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        
class Product(db.Model):
    """product model"""
    __tablename__="products"
    __table_args__ = {'schema': 'schema_any'}
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.Text,nullable =False,unique=True)
    type = db.Column(db.Text,primary_key=True) 
    description = db.Column(db.Text,nullable =False)
    ingredients=db.Column(db.Text,nullable=False)
    image = db.Column(db.Text)
    
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
    __tablename__ = 'products' 

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
        unique=True
    )
class Customize(db.Model):
    """customze model"""
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable = False,unique =True)
    size = db.Column(db.Text,nullable =False)
    ingredients= db.Column(db.Text,nullable=False)
    description = db.Column(db.Text,nullable =False)
    image = db.Column(db.Text)
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete="CASCADE"),nullable =False
    )
    user=db.relationship('User')