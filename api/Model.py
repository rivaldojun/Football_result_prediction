# Import the necessary libraries.
import pandas as pd
import numpy as np
import xgboost as xgb
# from sklearn.linear_model import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from IPython.display import display
from datetime import datetime
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,precision_score

# %matplotlib inline


def reading(string):
    data=pd.read_csv(string)
    # Remove first 3 matchweeks
    data = data[data.MW > 3]

    data.drop(['Unnamed: 0','HomeTeam', 'AwayTeam', 'Date', 'MW', 'HTFormPtsStr', 'ATFormPtsStr', 'FTHG', 'FTAG',
            'HTGS', 'ATGS', 'HTGC', 'ATGC','HomeTeamLP', 'AwayTeamLP','DiffPts','HTFormPts','ATFormPts',
            'HM4','HM5','AM4','AM5','HTLossStreak5','ATLossStreak5','HTWinStreak5','ATWinStreak5',
            'HTWinStreak3','HTLossStreak3','ATWinStreak3','ATLossStreak3'],1, inplace=True)
    # Preview data.
    data=data.dropna(axis=0)
    # Total number of students.
    n_matches = data.shape[0]

    # Calculate number of features.
    n_features = data.shape[1] - 1

    # Calculate matches won by home team.
    n_homewins = len(data[data.FTR == 'H'])

    # Calculate win rate for home team.
    win_rate = (float(n_homewins) / (n_matches)) * 100

    # Print the results
    # print ("Total number of matches: {}".format(n_matches))
    # print ("Number of features: {}".format(n_features))
    # print ("Number of matches won by home team: {}".format(n_homewins))
    # print ("Win rate of home team: {:.2f}%".format(win_rate))
    # Visualising distribution of data
    scatter_matrix(data[['HTGD','ATGD','HTP','ATP','DiffFormPts','DiffLP']], figsize=(10,10))   
    X_all = data.drop(['FTR'],1)
    y_all = data['FTR']
    X_all.HM1 = X_all.HM1.astype('str')
    X_all.HM2 = X_all.HM2.astype('str')
    X_all.HM3 = X_all.HM3.astype('str')
    X_all.AM1 = X_all.AM1.astype('str')
    X_all.AM2 = X_all.AM2.astype('str')
    X_all.AM3 = X_all.AM3.astype('str')

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    def preprocess_features(X):
        ''' Preprocesses the football data and converts catagorical variables into numeric variables using LabelEncoder. '''
        
        # Initialize LabelEncoder
        

        # Iterate over columns
        for col in X.columns:

            # If data type is categorical, transform to numeric
            if X[col].dtype == object:
                X[col] = le.fit_transform(X[col].astype(str))
        return X
    
    preprocess_features(X_all)
    X_all=X_all.iloc[:,1:]

    
   

    # Shuffle and split the dataset into training and testing set.
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, 
                                                        test_size = 0.2,
                                                        random_state = 2,
                                                        stratify = y_all)   


    # preprocess_features(X_all)
    # print("Processed feature columns ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns)))



    return le,X_train, X_test, y_train, y_test

le_PL,X_train_PL, X_test_PL, y_train_PL, y_test_PL = reading('Dataset/final_dataset_PL.csv')
le_L1,X_train_L1, X_test_L1, y_train_L1, y_test_L1 = reading('Dataset/final_dataset_L1.csv')
le_LL,X_train_LL, X_test_LL, y_train_LL, y_test_LL = reading('Dataset/final_dataset_LL.csv')
le_BL,X_train_BL, X_test_BL, y_train_BL, y_test_BL = reading('Dataset/final_dataset_BL.csv')
le_SA,X_train_SA, X_test_SA, y_train_SA, y_test_SA = reading('Dataset/final_dataset_SA.csv')


from time import time 
from sklearn.metrics import f1_score

def train_classifier(clf, X_train, y_train):
    ''' Fits a classifier to the training data. '''
    
    # Start the clock, train the classifier, then stop the clock
    start = time()
    clf.fit(X_train, y_train)
    end = time()
    
    # Print the result

    
def predict_labels(clf, features, target):
    y_pred = clf.predict(features)
    return f1_score(target, y_pred, pos_label='H'), sum(target == y_pred) / float(len(y_pred)),precision_score(target,y_pred, pos_label='H')


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Train and predict using a classifer based on F1 score. '''
    
    # Indicate the classifier and the training set size
    # print ("Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train)))
    
    # Train the classifier
    train_classifier(clf, X_train, y_train)
    
    # Print the results of prediction for both training and testing
    f1, acc,precision = predict_labels(clf, X_train, y_train)
    print ("F1 score, accuracy score  and precision for training set: {:.2f}% , {:.2f}%. , {:.2f}%.".format(f1*100 , acc*100,precision*100))
    
    f1, acc ,precision= predict_labels(clf, X_test, y_test)
    print ("F1 score, accuracy score and precision for test set: {:.2f}% , {:.2f}%. , {:.2f}%.".format(f1*100 , acc*100,precision*100))
    return acc,precision


clf_A_PL = RandomForestClassifier(n_estimators=100)
clf_A_L1 = RandomForestClassifier(n_estimators=200)
clf_A_LL = RandomForestClassifier(n_estimators=100)
clf_A_BL = RandomForestClassifier(n_estimators=100,bootstrap=True,criterion='linear')
clf_A_SA = RandomForestClassifier(n_estimators=100)

clf_B_PL = MLPClassifier(activation='tanh', hidden_layer_sizes= (50,2), learning_rate='adaptive', max_iter= 3000, solver= 'adam')
clf_B_L1 = SVC(kernel='poly',C=10)
clf_B_LL =MLPClassifier(activation='tanh', hidden_layer_sizes= (20,10),  max_iter= 3000, solver= 'adam')
clf_B_BL =SVC(kernel='poly',C=10)
clf_B_SA = SVC(kernel='rbf',C=8)


print ('SCORE MODEL PL:')
print("Random Forest:")
acc_A_PL,Precision_A_PL=train_predict(clf_A_PL, X_train_PL, y_train_PL, X_test_PL, y_test_PL)
print ('MLPClassifier:')
acc_B_PL,Precision_B_PL=train_predict(clf_B_PL, X_train_PL, y_train_PL, X_test_PL, y_test_PL)
print ('')
print ('SCORE MODEL L1:')
print("Random Forest:")
acc_A_L1,Precision_A_L1=train_predict(clf_A_L1, X_train_L1, y_train_L1, X_test_L1, y_test_L1)
print ('')
print ('SVC:')
acc_B_L1,Precision_B_L1=train_predict(clf_B_L1, X_train_L1, y_train_L1, X_test_L1, y_test_L1)
print ('')
print ('SCORE MODEL LL:')
print("Random Forest:")
acc_A_LL,Precision_A_LL=train_predict(clf_A_LL, X_train_LL, y_train_LL, X_test_LL, y_test_LL)
print ('')
print ('MLPClassifier:')
acc_B_LL,Precision_B_LL=train_predict(clf_B_LL, X_train_LL, y_train_LL, X_test_LL, y_test_LL)
print ('')
print ('SCORE MODEL BL:')
print("Random Forest:")
acc_A_BL,Precision_A_BL=train_predict(clf_A_BL, X_train_BL, y_train_BL, X_test_BL, y_test_BL)
print ('')
print ('SVC:')
acc_B_BL,Precision_B_BL=train_predict(clf_B_BL, X_train_BL, y_train_BL, X_test_BL, y_test_BL)
print ('')
print ('SCORE MODEL SA:')
print("Random Forest:")
acc_A_SA,Precision_A_SA=train_predict(clf_A_SA, X_train_SA, y_train_SA, X_test_SA, y_test_SA)
print ('')
print ('SVC:')
acc_B_SA,Precision_B_SA=train_predict(clf_B_SA, X_train_SA, y_train_SA, X_test_SA, y_test_SA)
print ('')

def meilleur_model(clfa,clfb,preca,precb):
    if preca>precb:
        print('model choisi:',str(clfa)," precision=",preca)
        return clfa
    else:
        print('model choisi:',str(clfb),"precision =",precb)
        return clfb

    


import joblib

joblib.dump(meilleur_model(clf_A_PL,clf_B_PL,Precision_A_PL,Precision_B_PL), 'Model/model_PL.pkl')
joblib.dump(meilleur_model(clf_A_L1,clf_B_L1,Precision_A_L1,Precision_B_L1), 'MOdel/model_L1.pkl')
joblib.dump(meilleur_model(clf_A_LL,clf_B_LL,Precision_A_LL,Precision_B_LL), 'Model/model_LL.pkl')
joblib.dump(meilleur_model(clf_A_BL,clf_B_BL,Precision_A_BL,Precision_B_BL), 'Model/model_BL.pkl')
joblib.dump(meilleur_model(clf_A_SA,clf_B_SA,Precision_A_SA,Precision_B_SA), 'Model/model_SA.pkl')
joblib.dump(le_PL,"Model/le_PL.joblib")
joblib.dump(le_L1,"Model/le_L1.joblib")
joblib.dump(le_LL,"Model/le_LL.joblib")
joblib.dump(le_BL,"Model/le_BL.joblib")
joblib.dump(le_SA,"Model/le_SA.joblib")