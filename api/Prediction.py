from datetime import datetime
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


def ligue(string):
    if string=='Premier League':
        return 'Dataset/final_dataset_PL.csv'
    if string=='Ligue 1':
        return 'Dataset/final_dataset_L1.csv'
    if string=='La Liga':
        return 'Dataset/final_dataset_LL.csv'
    if string=='Bundesliga':
        return 'Dataset/final_dataset_BL.csv'
    if string=='Serie A':
        return 'Dataset/final_dataset_SA.csv'
   
def get_model(string):
    if string=='Premier League':
        model= joblib.load('Model/model_PL.pkl')
    if string=='Ligue 1':
        model= joblib.load('Model/model_L1.pkl')
    if string=='La Liga':
        model= joblib.load('Model/model_LL.pkl')
    if string=='Bundesliga':
        model= joblib.load('Model/model_BL.pkl')
    if string=='Serie A':
        model= joblib.load('Model/model_SA.pkl')
    return model


def get_label(string):
    if string=='Premier League':
        model= joblib.load('Model/le_PL.joblib')
    if string=='Ligue 1':
        model= joblib.load('Model/le_L1.joblib')
    if string=='La Liga':
        model= joblib.load('Model/le_LL.joblib')
    if string=='Bundesliga':
        model= joblib.load('Model/le_BL.joblib')
    if string=='Serie A':
        model= joblib.load('Model/le_SA.joblib')
    return model 
    
def prise(team,string):
    path=ligue(string)
    data=pd.read_csv(path)
    df_home = data.loc[data['HomeTeam'] == team].tail(1)
    df_away = data.loc[data['AwayTeam'] == team].tail(1)
    if  datetime.strptime(str(df_home.Date.values[0]), '%d-%m-%Y')<datetime.strptime(str(df_away.Date.values[0]), '%d-%m-%Y'):
        df=df_away
        X=[float(df.ATP.values),str(df.AM1.values[0]),str(df.AM2.values[0]),str(df.AM3.values[0]),float(df.ATGD.values),float(df.AwayTeamLP.values),float(df.ATFormPts.values)] 
    else:
        df=df_home
        X=[float(df.HTP.values),str(df.HM1.values[0]),str(df.HM2.values[0]),str(df.HM3.values[0]),float(df.HTGD.values),float(df.HomeTeamLP.values),float(df.HTFormPts.values)] 
    return X 

def donnee(team1,team2,string):
    X_Home=prise(team1,string)
    X_Away=prise(team2,string)
    X=[X_Home[0],X_Away[0],X_Home[1],X_Home[2],X_Home[3],X_Away[1],X_Away[2],X_Away[3],X_Home[4],X_Away[4],X_Home[6]-X_Away[6],X_Home[5]-X_Away[5]]
    data=[X]
    print(data)
    columns = ['HTP', 'ATP', 'HM1', 'HM2', 'HM3', 'AM1', 'AM2', 'AM3', 'HTGD', 'ATGD', 'DiffFormPts', 'DiffLP']
    df = pd.DataFrame(data, columns=columns)  
    le = get_label(string)
    for col in df.columns:
        # If data type is categorical, transform to numeric
        if df[col].dtype == object:
            df[col] = le.fit_transform(df[col].astype(str))
    df=df.iloc[:,1:]
    model=get_model(string)
    y_pred = model.predict(df)
    if str(y_pred[0])=='H':
        return team1
    else:
        return team2
    
def pourcentages(homeTeam, winner, ligue):

    if ligue == "Premier League":
        vainq_pourcent = 75
    elif ligue == "La Liga":
        vainq_pourcent = 70
    elif ligue == "Ligue 1":
        vainq_pourcent = 72
    elif ligue == "Bundesliga":
        vainq_pourcent = 74
    else:
        vainq_pourcent = 76
    
    if homeTeam == winner:
        pourcentage_home = vainq_pourcent
        pourcentage_away = 100 - vainq_pourcent
    else:
        pourcentage_away = vainq_pourcent
        pourcentage_home = 100 - vainq_pourcent
    return pourcentage_home, pourcentage_away

     

# string=input("Entrez la Ligue:")
# home=input('Entrez lequipe a domicile:')
# away=input('Entrez lequipe a lexterieur:')
# # string=ligue(str)
# # string='PL'
# # home="Arsenal"
# # away="Aston Villa"
# # string='final_dataset_PL.csv'
# print('home:',home)
# print('away:',away)
# print('league:',string)
# gagnant=donnee(home,away,string)

# print("Le vainqueur est :",gagnant)
