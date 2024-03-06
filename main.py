from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import subprocess,os
from config import *
app = Flask(__name__)

app.secret_key = SECRET_KEY

def verifier_authentification(f):
    @wraps(f)
    def fonction_de_verification(*args, **kwargs):
        if 'utilisateur' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return fonction_de_verification

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        if nom_utilisateur in utilisateurs_enregistres and utilisateurs_enregistres[nom_utilisateur] == mot_de_passe:
            session['utilisateur'] = nom_utilisateur
            return redirect(url_for('index'))
        else:
            # Sinon, affiche un message d'erreur
            erreur = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render_template('login.html', erreur=erreur)
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
@verifier_authentification
def index():
    if request.method == 'POST':
        commentaire = request.form['commentaire']
        subprocess.run('echo ' + commentaire + ' > /tmp/logs', shell=True)
        result = subprocess.run(["cat", "/tmp/logs"], capture_output=True, text=True)
        if result.returncode == 0:
            return render_template('index.html', commentaire=result.stdout)
        else:
            return render_template('index.html', commentaire=commentaire)
    try:
        os.remove('/tmp/logs')
    except:
        pass
    # Si la méthode est GET ou si le formulaire n'a pas été soumis, affiche simplement la page
    return render_template('index.html', commentaire=None)

if __name__ == '__main__':
    app.run(debug=False)