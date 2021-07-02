from flask import Flask , render_template ,request ,redirect , url_for , flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import datastructures


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cin = db.Column(db.String(80), unique=True ,nullable=False)
    nom = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    tlf = db.Column(db.Integer, unique=True, nullable=False)
    Salaire = db.Column(db.Integer,  nullable=False)

    def __init__(self , cin , nom , email , tlf , Salaire):
        self.cin = cin
        self.nom = nom
        self.email = email
        self.tlf = tlf
        self.Salaire = Salaire



@app.route('/')
def index():
    all_data = Employer.query.all()
    return render_template("index.html", mydata= all_data)


@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        cin = request.form['cin']
        nom = request.form['nom']
        email = request.form['email']
        tlf = request.form['tlf']
        Salaire = request.form['Salaire']
        data = Employer(cin , nom ,email , tlf, Salaire)
        db.session.add(data)
        
        try :
            db.session.commit()
            flash("Employé ajouté" ,"success")

            
        except:
            db.session.rollback()
            flash("Employé non ajoute" , "warning")
        return redirect(url_for('index'))

@app.route('/modifier', methods = ['GET', 'POST'])
def modifier():
    if request.method == "POST":
        data = Employer.query.get(request.form.get('id'))
        data.cin = request.form['cin']
        data.nom = request.form['nom']
        data.email = request.form['email']
        data.tlf = request.form['tlf']
        data.Salaire = request.form['Salaire']
        try :
            db.session.commit()
            flash("les données de l'employée ont été modifiées")

            
        except:
            db.session.rollback()
            flash("Les données de l'employé n'ont pas été modifiées")
        return redirect(url_for('index'))

@app.route('/supprimer/<id>/', methods = ['GET', 'POST'])
def supprimer(id):
    data = Employer.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("l'employé est supprimé")
    return redirect(url_for('index'))






if __name__ == "__main__":
    app.run(debug=True , port=8000)