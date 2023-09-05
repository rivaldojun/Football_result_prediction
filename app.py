from flask import Flask, render_template,request,jsonify,session,redirect,url_for,make_response,send_file
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import func,and_
import numpy as np
import os
import subprocess
import datetime
import pandas as pd
from api.Prediction import donnee
from api.Prediction import pourcentages
from datetime import date
app = Flask(__name__)
app.secret_key = '123'

# pl=pd.read_csv('premierleague/E0 (1).csv')
# pl=list(pl.HomeTeam.unique())
# l1=pd.read_csv('ligue1/F1.csv')
# l1=list(l1.HomeTeam.unique())
# ll=pd.read_csv('laliga/SP1.csv')
# ll=list(ll.HomeTeam.unique())
# bl=pd.read_csv('bundesligua/D1.csv')
# bl=list(bl.HomeTeam.unique())
# sa=pd.read_csv('serieA/I1.csv')
# sa=list(sa.HomeTeam.unique())
# teams_by_league={'Premier League':pl,'Ligue 1':l1,'La Liga':ll,'Bundesliga':bl,'Serie A':sa}


def Abbrv(ligue):
    if ligue=='Premier League':
        h="PL"
    if ligue=='Ligue 1':
        h="L1"
    if ligue=='La Liga':
        h="LL"
    if ligue=="Bundesliga":
        h="BL"
    if ligue=="Serie A":
        h="SA"
    return h

def delete_past_fix(nom_fich):
    df = pd.read_csv(nom_fich)

    # Convertir la colonne de date en datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Obtenir la date actuelle
    today = date.today()

    # Sélectionner les lignes avec une date supérieure ou égale à la date actuelle
    df = df.loc[df['Date'] >= datetime.combine(today, datetime.min.time())]

    # Enregistrer le dataframe modifié avec le même nom et emplacement
    df.to_csv(nom_fich, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    championnat=['Premier League','Ligue 1','La Liga','Bundesliga','Serie A']
    pl=pd.read_csv('premierleague/E0 (1).csv')
    pl=list(pl.HomeTeam.unique())
    l1=pd.read_csv('ligue1/F1.csv')
    l1=list(l1.HomeTeam.unique())
    ll=pd.read_csv('laliga/SP1.csv')
    ll=list(ll.HomeTeam.unique())
    bl=pd.read_csv('bundesligua/D1.csv')
    bl=list(bl.HomeTeam.unique())
    sa=pd.read_csv('serieA/I1.csv')
    sa=list(sa.HomeTeam.unique())
    teams_by_league={'Premier League':pl,'Ligue 1':l1,'La Liga':ll,'Bundesliga':bl,'Serie A':sa}
    if request.method == 'POST':
        # league=request.form.get('league')
        # home=request.form['team1']
        # away=request.form['team2']
        # print(league)
        # print(away)
        # print(home)
        # donne=donnee(home,away,league)
        # session['winner']=str(donne)
        home = request.form['home']  
        away = request.form['away']  
        league = request.form['league']
        session['league']=str(league)
        homelogo = request.form['homelogo'] 
        awaylogo = request.form['awaylogo'] 
        winner = donnee(home, away, league) 
        pourcentage_home, pourcentage_away = pourcentages(home, winner, league)
        # session['winner'] = winner
        session['winner'] = {
            'home': home,
            'away': away,
            'pourcentage_home': pourcentage_home,
            'pourcentage_away': pourcentage_away,
            'home_logo_url': homelogo,
            'away_logo_url': awaylogo,
            'winner':winner
        }
        # redirect(url_for('result'))
        
        return redirect(url_for('result'))
        
       
    return render_template('index.html')

@app.route('/data')
def data():
 
    winner = session.get('winner')
    # Récupérez les données depuis votre base de données ou autre source
    l=Abbrv(session.get('league'))
    pl=pd.read_csv("Dataset/evolution_"+l+".csv")
    pl = pl.set_index('Unnamed: 0')
    data1=pl.loc[winner['home']].values.tolist()
    data2=list(pl.loc[winner['away']].values.tolist())
    r=[i for i in range(len(data1))]
    # Retournez les données sous forme de JSON
    return jsonify(data1=data1, data2=data2,range=r)

@app.route('/result')
def result():
    winner = session.get('winner')
    l=Abbrv(session.get('league'))
    note=pd.read_csv("Dataset/note_"+l+".csv")
    note= note.set_index('Unnamed: 0')
    classement=pd.read_csv("Dataset/classement_"+l+".csv")
    classement=classement.set_index('Equipe')
    data1=note.loc[winner['home']].values
    data2=note.loc[winner['away']].values
    classement1=classement.loc[winner['home']].values[-1]
    classement2=classement.loc[winner['away']].values[-1]
    return render_template('vainqueur.html', 
        HomeTeam=winner['home'], 
        AwayTeam=winner['away'], 
        HomeLogoUrl=winner['home_logo_url'],
        AwayLogoUrl=winner['away_logo_url'],
        winnerTeam = winner['winner'],
        PourcentageHome=winner['pourcentage_home'],
        PourcentageAway=winner['pourcentage_away'],note1=data1,note2=data2,classement1=classement1,classement2=classement2)
if __name__ == '__main__':
    app.run(debug=True)