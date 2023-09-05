import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime as dt
import datetime



def read_data_path(leaguename,leaguecode):
    
    pathlist=[]
    
    
    for i in range(31,0,-1):
            
        sales = leaguename+'/'+leaguecode+' ('+str(i)+')'+'.csv'
          
        if(os.path.isfile(sales)):
                pathlist.append(sales)
    
    sales1 = leaguename+'/'+leaguecode+'.csv'
    if(os.path.isfile(sales1)):
        pathlist.append(sales1)
    return pathlist




# premleague=read_data_path("premierleague","E0")
# ligue1=read_data_path("ligue1","F1")
# laliga=read_data_path("laliga","SP1")
# bundesliga=read_data_path("bundesligua","D1")
# serieA=read_data_path("serieA","I1")


def get_team(data):
    dfs=[]
    for filename in data:
        df= pd.read_csv(filename)
        df.set_index
        df=df.dropna(subset=["HomeTeam"])
        df=df.dropna(subset=["AwayTeam"])
        a=df.isna().sum().value_counts
        dfs.append(df)
    merged_df = pd.concat(dfs, axis=0)
    teams=merged_df.HomeTeam.unique()
    return teams
def merge_data(list):
    dfs=[]
    for filename in list:
        df= pd.read_csv(filename)
        df.set_index
        df=df.dropna(subset=["HomeTeam"])
        df=df.dropna(subset=["AwayTeam"])
        a=df.isna().sum().value_counts
        
        df.Date=df.Date.apply(lambda x:x.replace("/","-"))
        dfs.append(df)
    
    merged_df = pd.concat(dfs, axis=0)
    return merged_df


# teamPL=get_team(premleague)
# teamL1=get_team(ligue1)
# teamLL=get_team(laliga)
# teamBL=get_team(bundesliga)
# teamSA=get_team(serieA)



def dataprepocessing(leaguename,teams,league):
    dfs=[]
    df_class = pd.DataFrame(index=teams)
    df_class.index.name = 'Equipe'
    df_class.reset_index
    def preprocess(df):
        miss_values=df.isna().mean()*100
        keep=miss_values[miss_values<=10].index
        df=df[keep]
        return df
    def change_date_format(date):
        date=str(date)
        if len(date)<=8:
            date=date[:6]+'20'+date[6:]
        return date
    
    def get_classement(row, classement_dict):
        equipe = row.name
        classement = classement_dict.get(equipe, '-')
        return classement

    def classement(data,df_class):   
            dict_u={}
            teams=data.HomeTeam.unique()

            for i in range(len(teams)):
                dict_u[teams[i]]=0


            for i in range(len(data)):
                if data.iloc[i]['FTR']=='H':
                    dict_u[data.iloc[i].HomeTeam]=dict_u[data.iloc[i].HomeTeam]+3
                elif data.iloc[i]['FTR']=='A':
                    dict_u[data.iloc[i].AwayTeam]=dict_u[data.iloc[i].AwayTeam]+3
                else :
                    dict_u[data.iloc[i].HomeTeam]=dict_u[data.iloc[i].HomeTeam]+1
                    dict_u[data.iloc[i].AwayTeam]=dict_u[data.iloc[i].AwayTeam]+1
            dict_u=dict(sorted(dict_u.items(), key=lambda x: x[1], reverse=True))
            noms_equipes = list(dict_u.keys())
            points = list(dict_u.values())

            # Création du dataframe
            df = pd.DataFrame({'Points': points}, index=noms_equipes)
            df.index.name = 'Equipe'
            df.reset_index(inplace=True)
            df.index += 1
            df.index.name = 'Classement'
            df.reset_index(inplace=True)
            d=data.Date[0]
            if(len(d)>8):
                d=d[6:]
            else:
                d="20"+d[6:]

            l={}
            teams=data.HomeTeam.unique()
            for i in range(len(teams)):
                l[teams[i]]=0
            for i in range(len(df)):
                x=int(df.iloc[i].Classement)
                
                l[df.iloc[i].Equipe]=x

            noms_equipes = list(l.keys())
            classement = list(l.values())
            df_class[d]=df_class.apply(get_classement, axis=1, args=(l,))
        
    # Gets the goals scored agg arranged by teams and matchweek
    def get_goals_scored(playing_stat):
        # Créer un dictionnaire avec les noms d'équipe comme clés
        teams = {}
        for i in playing_stat.groupby('HomeTeam').mean().T.columns:
            if i != 'nan': # Vérifier que le nom de l'équipe n'est pas NaN
                teams[i] = []
        
        # La valeur correspondant aux clés est une liste contenant les buts marqués par match.
        for i in range(len(playing_stat)):
            HTGS = playing_stat.iloc[i]['FTHG']
            ATGS = playing_stat.iloc[i]['FTAG']
            teams[playing_stat.iloc[i].HomeTeam].append(HTGS)        
            teams[playing_stat.iloc[i].AwayTeam].append(ATGS)
        
        max_length = max([len(team) for team in teams.values()])
        for team, goals_scored in teams.items():
            if len(goals_scored) < max_length:
                goals_scored += [float('nan')] * (max_length - len(goals_scored))

        # Create the DataFrame
        goals_scored = pd.DataFrame(teams, index=[i for i in range(1, max_length + 1)]).T
        goals_scored[0]=0

        for i in range(2,max_length+1):
         goals_scored[i] = goals_scored[i] + goals_scored[i-1]

        return goals_scored


    def get_goals_conceded(playing_stat):
        # Create a dictionary with team names as keys
        teams = {}
        for i in playing_stat.groupby('HomeTeam').mean().T.columns:
            teams[i] = []

        # Fill the dictionary with the number of goals conceded by each team in each match
        for i in range(len(playing_stat)):
            ATGC = playing_stat.iloc[i]['FTHG']
            HTGC = playing_stat.iloc[i]['FTAG']
            teams[playing_stat.iloc[i].HomeTeam].append(HTGC)
            teams[playing_stat.iloc[i].AwayTeam].append(ATGC)

        # Add NaN values to teams with missing data
        max_length = max([len(team) for team in teams.values()])
        for team, goals_conceded in teams.items():
            if len(goals_conceded) < max_length:
                goals_conceded += [float('nan')] * (max_length - len(goals_conceded))

        # Create the DataFrame
        goals_conceded = pd.DataFrame(teams, index=[i for i in range(1, max_length + 1)]).T
        goals_conceded[0]=0
        for i in range(2,max_length+1):
            goals_conceded[i] = goals_conceded[i] + goals_conceded[i-1]

        

        return goals_conceded



    def get_gss(playing_stat):
        GC = get_goals_conceded(playing_stat)
        GS = get_goals_scored(playing_stat)

        j = 0
        HTGS = []
        ATGS = []
        HTGC = []
        ATGC = []

        for i in range(len(playing_stat)):
            ht = playing_stat.iloc[i].HomeTeam
            at = playing_stat.iloc[i].AwayTeam
            HTGS.append(GS.loc[ht][j])
            ATGS.append(GS.loc[at][j])
            HTGC.append(GC.loc[ht][j])
            ATGC.append(GC.loc[at][j])

            if ((i + 1) % 10) == 0:
                j = j + 1

        playing_stat['HTGS'] = HTGS
        playing_stat['ATGS'] = ATGS
        playing_stat['HTGC'] = HTGC
        playing_stat['ATGC'] = ATGC

        return playing_stat
    
    
    def get_points(result):
        if result == 'W':
            return 3
        elif result == 'D':
            return 1
        else:
            return 0

    def get_cuml_points(matchres):
        matchres_points = matchres.applymap(get_points)
        for i in range(2,len(matchres.columns)+1):
            matchres_points[i] = matchres_points[i] + matchres_points[i-1]
        matchres_points.insert(loc=0, column=0, value=[0*i for i in range(len(matchres))])
        # print(matchres_points[0]["Aston Villa"])
        return matchres_points


    def get_matchres(playing_stat):
        # Create a dictionary with team names as keys
        teams = {}
        for i in playing_stat.groupby('HomeTeam').mean().T.columns:
            teams[i] = []

        # the value corresponding to keys is a list containing the match result
        for i in range(len(playing_stat)):
            if playing_stat.iloc[i].FTR == 'H':
                teams[playing_stat.iloc[i].HomeTeam].append('W')
                teams[playing_stat.iloc[i].AwayTeam].append('L')
            elif playing_stat.iloc[i].FTR == 'A':
                teams[playing_stat.iloc[i].AwayTeam].append('W')
                teams[playing_stat.iloc[i].HomeTeam].append('L')
            else:
                teams[playing_stat.iloc[i].AwayTeam].append('D')
                teams[playing_stat.iloc[i].HomeTeam].append('D')
        
        max_length = max([len(team) for team in teams.values()])
        for team in teams:
            teams[team] += [''] * (max_length - len(teams[team]))
        

        return pd.DataFrame(teams, index=[i for i in range(1, max_length+1)]).T


    def get_agg_points(playing_stat):
        matchres = get_matchres(playing_stat)
        cum_pts = get_cuml_points(matchres)
        HTP = []
        ATP = []
        j = 0
        for i in range(len(playing_stat)):
            
            ht = playing_stat.iloc[i].HomeTeam
            at = playing_stat.iloc[i].AwayTeam
            HTP.append(cum_pts[j][ht])
            ATP.append(cum_pts[j][at])
            

            if ((i + 1)% 10) == 0:
                j = j + 1
                
        playing_stat['HTP'] = HTP
        playing_stat['ATP'] = ATP
        return playing_stat
    def get_form(playing_stat,num):
        form = get_matchres(playing_stat)
        form_final = form.copy()
        
        for i in range(num,len(form_final)):
            form_final[i] = ''
            j = 0
            while j < num:
                form_final[i] += form[i-j]
                j += 1           
        return form_final
    
    def get_last(playing_stat, Standings, year):
        HomeTeamLP = []
        AwayTeamLP = []
        for i in range(len(playing_stat)):
            ht = playing_stat.iloc[i].HomeTeam
            at = playing_stat.iloc[i].AwayTeam
            HomeTeamLP.append(int(Standings[Standings.Equipe==ht][year].values))
            AwayTeamLP.append(int(Standings[Standings.Equipe==at][year].values))
        playing_stat['HomeTeamLP'] = HomeTeamLP
        playing_stat['AwayTeamLP'] = AwayTeamLP
        return playing_stat

    def add_form(playing_stat,num):
            form = get_form(playing_stat,num)
            # print('form:',form)
            h = ['M' for i in range(num * 10)]  # since form is not available for n MW (n*10)
            a = ['M' for i in range(num * 10)]
            j = num
            for i in range((num*10),len(playing_stat)):
                ht = playing_stat.iloc[i].HomeTeam
                at = playing_stat.iloc[i].AwayTeam
                k=playing_stat.iloc[i].MW 
                past=form.loc[ht][k-num]
                
                if len(past) >= 2:
                     h.append(past[0])
                else:
                    h.append(past)
              

                past=form.loc[at][k-num]
                if len(past)>=2:
                     a.append(past[0])
                else:
                     a.append(past)                 
                    
                # past = form.loc[ht][j]             
                # if len(past) >= num:
                #  h.append(past[num-1])
                # else:
                #  h.append('M')
                #  past = form.loc[at][j] 
                # if len(past) >= num:
                #  a.append(past[num-1])
                # else:
                #  a.append('M')                   # 0 index is most recent
                
                            # get past n results.
                            # 0 index is most recent
                
                if ((i+1)% 10) == 0:
                    j = j + 1
            # print("h:",h)
            # print("a",a)

            playing_stat['HM' + str(num)] = h                 
            playing_stat['AM' + str(num)] = a

            
            return playing_stat


    def add_form_df(playing_statistics):
        playing_statistics = add_form(playing_statistics,1)
        playing_statistics = add_form(playing_statistics,2)
        playing_statistics = add_form(playing_statistics,3)
        playing_statistics = add_form(playing_statistics,4)
        playing_statistics = add_form(playing_statistics,5)
        return playing_statistics 
    def get_mw(playing_stat):
        j = 1
        MatchWeek = []
        for i in range(len(playing_stat)):
            MatchWeek.append(j)
            if ((i + 1)% 10) == 0:
                j = j + 1
        playing_stat['MW'] = MatchWeek
        return playing_stat
    
    def get_form_points(string):
        sum = 0
        for letter in string:
            sum += get_points(letter)
        return sum
    
    def get_3game_ws(string):
        if string[-3:] == 'WWW':
            return 1
        else:
            return 0
    
    def get_5game_ws(string):
        if string == 'WWWWW':
            return 1
        else:
            return 0
        
    def get_3game_ls(string):
        if string[-3:] == 'LLL':
            return 1
        else:
            return 0
        
    def get_5game_ls(string):
        if string == 'LLLLL':
            return 1
        else:
            return 0
    
    def only_hw(string):
        if string == 'H':
            return 'H'
        else:
            return 'NH'
    
    def class_glob(a): 
        a.replace("-",len(teams))   
        l=[]
        for i in range(len(teams)):
            temp=a.iloc[i,7:19].values
        
            r=0
            for j in range(len(temp)): 
                r=r+int(temp[j])
            r=int(r/len(temp))
                
            l.append(r)
        p=[]
        for i in range(len(teams)):
            k=1
            for j in range(len(teams)):
                if l[i]>l[j]:
                    k=k+1
            while k in p:
                k=k+1
            p.append(k)
        
        a["class"]=p
    

    def evolution(f):
        f=pd.read_csv(f)
        def get_points(result):
                if result == 'W':
                    return 3
                elif result == 'D':
                    return 1
                else:
                    return 0

        def get_matchres(playing_stat):
                # Create a dictionary with team names as keys
                teams = {}
                for i in playing_stat.groupby('HomeTeam').mean().T.columns:
                    teams[i] = []

                # the value corresponding to keys is a list containing the match result
                for i in range(len(playing_stat)):
                    if playing_stat.iloc[i].FTR == 'H':
                        teams[playing_stat.iloc[i].HomeTeam].append('W')
                        teams[playing_stat.iloc[i].AwayTeam].append('L')
                    elif playing_stat.iloc[i].FTR == 'A':
                        teams[playing_stat.iloc[i].AwayTeam].append('W')
                        teams[playing_stat.iloc[i].HomeTeam].append('L')
                    else:
                        teams[playing_stat.iloc[i].AwayTeam].append('D')
                        teams[playing_stat.iloc[i].HomeTeam].append('D')
                
                max_length = max([len(team) for team in teams.values()])
                for team in teams:
                    teams[team] += [''] * (max_length - len(teams[team]))
                

                return pd.DataFrame(teams, index=[i for i in range(1, max_length+1)]).T

        def get_cuml_points(matchres):
                matchres_points = matchres.applymap(get_points)
                for i in range(2,len(matchres.columns)+1):
                    matchres_points[i] = matchres_points[i] + matchres_points[i-1]
                matchres_points.insert(loc=0, column=0, value=[0*i for i in range(len(matchres))])
                return matchres_points
        d=get_matchres(f)
        c=get_cuml_points(d)
        c.to_csv("Dataset/evolution_"+league+".csv", index = True)
    
    def note_gen(df):

        # Calculer la moyenne des colonnes pour chaque équipe
        df_home = df.groupby("HomeTeam")["FTHG", "HS", "HST", "HC", "HY"].mean()
        df_away = df.groupby("AwayTeam")["FTAG", "AS", "AST", "AC", "AY"].mean()
        # Fusionner les deux dataframes pour obtenir une seule dataframe contenant les moyennes pour chaque équipe
        df_combined = pd.concat([df_home, df_away], axis=1)

        # Calculer une note générale pour chaque équipe en prenant la moyenne des moyennes de chaque colonne
        df_combined["NoteGenerale"] = df_combined.mean(axis=1) * 10+27
        gen=df_combined["NoteGenerale"]
        gen.to_csv("Dataset/note_"+league+".csv")

        # Trier les équipes par note générale


    for filename in leaguename:
        data= pd.read_csv(filename)
        data.set_index
        data=data.dropna(subset=["HomeTeam"])
        data=data.dropna(subset=["AwayTeam"])
        data.Date=data.Date.apply(change_date_format)
        d=data.Date[0]
        if(len(d)>8):
            d=d[6:]
        else:
            d="20"+d[6:]
        data.Date=data.Date.apply(lambda x:x.replace("/","-"))
        data=preprocess(data)
        classement(data,df_class)
        classement(data,df_class)
        columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']
        statleague=data[columns_req]
        statleague=get_gss(statleague)
        statleague=get_agg_points(statleague)
        statleague=get_mw(statleague)
        statleague=add_form_df(statleague)
        cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HM1', 'HM2', 'HM3',
        'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5' ]
        statleague=statleague[cols]
        df_class.to_csv("Dataset/classement.csv", index = True)
        Standings = pd.read_csv("Dataset/classement.csv",).replace('-',len(teams))
        statleague=get_last(statleague, Standings,d)
        statleague=get_mw(statleague)
        dfs.append(statleague)

    statleague = pd.concat(dfs, axis=0)
    statleague=preprocess(statleague)
    
    statleague['HTFormPtsStr'] = statleague['HM5'] + statleague['HM4'] + statleague['HM3'] + statleague['HM2'] + statleague['HM1']
    statleague['ATFormPtsStr'] = statleague['AM5'] + statleague['AM4'] + statleague['AM3'] + statleague['AM2'] + statleague['AM1']
   

    statleague['HTFormPts'] = statleague['HTFormPtsStr'].apply(get_form_points)
    statleague['ATFormPts'] = statleague['ATFormPtsStr'].apply(get_form_points)
    
    # print('HTFormPts',statleague['HTFormPts'])
    # print('ATFormPts',statleague['ATFormPts'])


    statleague['HTWinStreak3'] = statleague['HTFormPtsStr'].apply(get_3game_ws)
    statleague['HTWinStreak5'] = statleague['HTFormPtsStr'].apply(get_5game_ws)
    statleague['HTLossStreak3'] = statleague['HTFormPtsStr'].apply(get_3game_ls)
    statleague['HTLossStreak5'] = statleague['HTFormPtsStr'].apply(get_5game_ls)

    statleague['ATWinStreak3'] = statleague['ATFormPtsStr'].apply(get_3game_ws)
    statleague['ATWinStreak5'] = statleague['ATFormPtsStr'].apply(get_5game_ws)
    statleague['ATLossStreak3'] = statleague['ATFormPtsStr'].apply(get_3game_ls)
    statleague['ATLossStreak5'] = statleague['ATFormPtsStr'].apply(get_5game_ls)

    # Get Goal Difference
    statleague['HTGD'] = statleague['HTGS'] - statleague['HTGC']
    statleague['ATGD'] = statleague['ATGS'] - statleague['ATGC']

    # Diff in points
    statleague['DiffPts'] = statleague['HTP'] - statleague['ATP']
    statleague['DiffFormPts'] = statleague['HTFormPts'] - statleague['ATFormPts']

    # Diff in last year positions
    statleague['DiffLP'] = statleague['HomeTeamLP'] - statleague['AwayTeamLP']
    cols = ['HTGD','ATGD','DiffPts','DiffFormPts','HTP','ATP']
    statleague.MW = statleague.MW.astype(float)
    for col in cols:
        statleague[col] = statleague[col] / statleague.MW
        
    statleague['FTR'] = statleague.FTR.apply(only_hw)

    # Testing set (2015-16 season)
    # playing_stat_test = statleague[6000:]
    md=merge_data(leaguename)
    note_gen(md)
    statleague.to_csv("Dataset/final_dataset_"+league+".csv")
    # playing_stat_test.to_csv("test.csv")
    df_class.to_csv("Dataset/classement_"+league+".csv", index = True)
    df_class=pd.read_csv("Dataset/classement_"+league+".csv",).replace('-',18)
    class_glob(df_class)
    df_class.to_csv("Dataset/classement_"+league+".csv", index = True)
    evolution(leaguename[-1])
    