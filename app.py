# from re import template
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
######
db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Categoria(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    eventos = db.relationship('Evento',backref='categoria')

    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Evento(db.Model,UserMixin):
   
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    categoria_id = db.Column(db.Integer,db.ForeignKey('categoria.id'),nullable=False)
    direccion = db.Column(db.String(200),nullable=False)
    

    def __repr__(self):
        return f'<Evento: {self.nombre}>'

    
#####
@app.route("/",methods=['GET','POST'])
def login():
    
    if request.method=="GET":
        return render_template("front/login.html")

    usuario = request.form.get("usuario")
    password = request.form.get("password")
    user = User.query.filter_by(name=usuario).first()
    #if not user or not check_password_hash(user.password, password):
    if not user or not user.password == password:
        flash("Credenciales no validas intente nuevamente")
        return redirect(url_for("login"))

    return redirect(url_for("escritorio"))
        

@app.route("/escritorio",methods=['GET','POST'])
def escritorio():

    if request.method=="POST":
        print("debug1")
        id_evento = request.json["id"]
        print("debug2")
        evento = db.session.query(Evento).get(id_evento)
        db.session.delete(evento)
        print("debug3")
        db.session.commit()
        print("debug4")
        
    eventos = db.session.query(Evento).all()
    categorias = db.session.query(Categoria).all()
    return render_template("app/escritorioUsuario.html",eventos=eventos,categorias=categorias)



if __name__=='__main__':
    app.run(debug=True)
