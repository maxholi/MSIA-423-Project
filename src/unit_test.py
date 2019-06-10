import load_data, fit_model, test_model, similarity
import os
import pandas as pd
import numpy as np
import random
import pickle
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from sklearn.metrics import make_scorer
from sklearn.neighbors import NearestNeighbors



def test_create_df():
    inputs = {
        'Unnamed: 0': [1,2,3,4,5],
        'Year': [np.nan,1950.0, 1975.0, 1980.0, 1990.0],
        'Player': [np.nan,'John Smith', 'Joe Dirt*', 'William Wallace', 'Peter Pan*'],
        'Pos': [np.nan, 'G', 'SG', 'C','F'],
        'Age': [np.nan, 28.0,26.0,27.0,31.0],
        'Tm': [np.nan,'TOT','ATL','NYK','BOS'],
        'G': [np.nan, 68.0, 75.0, 50.0,82.0],
        'GS': [np.nan,np.nan,45.0,55.0,65.0],
        'MP': [np.nan, 500.0, 234.0, 1000.0, 345.0],
        'PER': [np.nan, np.nan, 12.5, 13.8, 17.8],
        'TS%': [np.nan, 0.345, 0.456, 0.765, 0.567 ],
        '3PAr': [np.nan, 0.453, 0.234,0.367,0.567],
        'FTr': [np.nan, 0.234, 0.345, 0.678, 0.345],
        'ORB%': [np.nan, 10.1, 8.7, 9.8, 3.5],
        'DRB%': [np.nan, 12.3, 5.5, 3.4, 4.6],
        'TRB%': [np.nan, 13.4,  5.9, 9.0, 6.7],
        'AST%': [np.nan, 6.0, 5.5, 1.2, 8.9],
        'STL%': [np.nan, 5.6, 8.9, 1.3, 0.4],
        'BLK%': [np.nan, 1.5, 3.4, 5.6, 2.4],
        'TOV%': [np.nan, 1.6, 5.7, 4.5, 0.4],
        'USG%': [np.nan, 13.4, 45.8, np.nan, 45.9],
        'blanl': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'OWS': [np.nan, -0.4, 0.67, 0.4, -0.1],
        'DWS': [np.nan, -0.23, 0.45, 0.8, 0.7],
        'WS': [np.nan, 10.5, 9.7, 3.4, 3.5],
        'WS/48': [np.nan, 0.067, -0.678, 0.123, 0.345],
        'blank2': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'OBPM': [np.nan, -3.4, 3.6, 6.7, 7.8],
        'DBPM': [np.nan, 0.5, 9.8, -4.5, 3.4],
        'BPM': [np.nan, 4.5, -3.4, 3.5, 6.7],
        'VORP': [np.nan, 0.0, -0.3, 0.75, 1.2],
        'FG': [np.nan, 89.0, 123.0, 56.0, 76.0],
        'FGA': [np.nan, 100.0, 145.0, 67.0, 88.0],
        'FG%': [np.nan, 0.456, 0.678, 0.123, 0.367],
        '3P': [np.nan, 9.0, 123.0, 256.0, 67.0],
        '3PA': [np.nan, 19.0, 145.0, 300.0, 78.0],
        '3P%': [np.nan, 0.234, 0.456, 0.189, 0.478],
        '2P': [np.nan, 17.0, 57.0, 78.0, 190.0],
        '2PA': [np.nan, 45.0, 60.0, 80.0, 200.0],
        '2P%': [np.nan, 0.123, 0.367, 0.654, 0.516],
        'eFG%': [np.nan, 0.456, 0.510, 0.345, 0.534],
        'FT': [np.nan, 100.0, 89.0, 17.0, 45.0],
        'FTA': [np.nan, 109.0, 99.0, 20.0, 50.0],
        'FT%': [np.nan, 0.567, 0.789, 0.897, 0.750],
        'ORB': [np.nan, 55.0, 14.0, 50.0, 98.0],
        'DRB': [np.nan, 14.0, 100.0, 78.0, 56.0],
        'TRB': [np.nan, 69.0, 114.0, 128.0, 154.0],
        'AST': [np.nan, 45.0, 56.0, 67.0, 77.0],
        'STL': [np.nan, 12.0, 45.0, 16.0, 23.0],
        'BLK': [np.nan, np.nan, 12.0, 11.0, 10.0],
        'TOV': [np.nan, 100.0, 77.0, 22.0, 23.0],
        'PF': [np.nan, 55.0, 23.0, 17.0, 33.0],
        'PTS': [np.nan, 2000.0, 567.0, 333.0, 499.0]

    }

    test_inputs = pd.DataFrame(data=inputs)

    expected = {
        'Year': [1975.0, 1980.0, 1990.0],
        'Player': ['Joe Dirt','William Wallace','Peter Pan'],
        'Tm': ['ATL','NYK','BOS'],
        'G': [75.0, 50.0, 82.0],
        'WS': [9.7, 3.4, 3.5],
        '3P': [123.0, 256.0, 67.0],
        'TRB': [114.0, 128.0, 154.0],
        'AST': [56.0, 67.0, 77.0],
        'STL': [45.0, 16.0, 23.0],
        'BLK': [12.0, 11.0, 10.0],
        'PTS': [567.0, 333.0, 499.0],
        'HOF': [1,0,1]
    }

    test_outputs = pd.DataFrame(data=expected)

    assert isinstance(test_outputs, pd.DataFrame)

    assert False not in (test_outputs.values == load_data.create_df(test_inputs).values)

def test_create_max():
    inputs = {

        'Player': ['max', 'joe', 'max','joe'],
        'Year': [1997.0, 2000.0, 2001.0, 1990.0]

    }

    test_inputs = pd.DataFrame(data=inputs)

    expected = {
        'Player': ['joe','max'],
        'Year' : [2000.0, 2001.0]

    }

    test_outputs = pd.DataFrame(data=expected)

    assert isinstance(test_outputs, pd.DataFrame)

    assert False not in (test_outputs.values == load_data.create_max(test_inputs).values)


def test_create_agg():

    inputs = {
        'Year': [1975.0, 1976.0, 1990.0, 1991.0, 1993.0],
        'Player': ['Joe Dirt', 'Joe Dirt', 'William Wallace','William Wallace', 'Peter Pan'],
        'Tm': ['ATL', 'ATL','NYK', 'NYK','BOS'],
        'G': [75.0, 25.0, 82.0, 18.0, 38.0],
        'WS': [9.7, 5.5, 9.8,3.4, 3.5],
        '3P': [123.0, 77.0, 256.0, 67.0, 100.0],
        'TRB': [114.0, 110.0, 125.0,128.0, 154.0],
        'AST': [56.0, 38.0, 57.0, 67.0, 77.0],
        'STL': [45.0, 45.0, 12.0, 16.0, 23.0],
        'BLK': [12.0, 1.0, 12.0, 11.0, 10.0],
        'PTS': [567.0,800.0, 490.0, 333.0, 499.0],
        'HOF': [1,1,0,0,1]
    }

    test_inputs = pd.DataFrame(data=inputs)

    expected = {

        'Playr': ['Joe Dirt', 'William Wallace'],
        'G': [100.0, 100.0],
        'Year': [2,2],
        'WS': [9.7, 9.8],
        '3P': [2.0, 3.23],
        'TRB': [2.24, 2.53],
        'AST': [0.94, 1.24],
        'STL': [0.9, 0.28],
        'BLK': [0.13, 0.23],
        'PTS': [13.67, 8.23],
        'HOF': [1,0]
    }

    test_outputs = pd.DataFrame(data=expected)

    assert isinstance(test_outputs, pd.DataFrame)

    assert False not in (test_outputs.values == load_data.create_agg(test_inputs,['3P', 'TRB', 'AST','STL', 'BLK','PTS'],True,2).values)


def test_create_agg_filter():
    d = {'create_agg_filter': {
        'create_agg': {
            'num_years': 2,
            'per_game': True,
            'per_game_cols': ['3P', 'TRB', 'AST', 'STL', 'BLK', 'PTS']}}}

    inputs = {
        'Year': [1975.0, 1976.0, 1990.0, 2012.0, 2013.0],
        'Player': ['Joe Dirt', 'Joe Dirt', 'William Wallace', 'Peter Pan', 'Peter Pan'],
        'Tm': ['ATL', 'ATL', 'NYK', 'NYK', 'BOS'],
        'G': [75.0, 25.0, 82.0, 50.0, 50.0],
        'WS': [9.7, 5.5, 9.8, 3.4, 3.5],
        '3P': [123.0, 77.0, 256.0, 67.0, 100.0],
        'TRB': [114.0, 110.0, 125.0, 128.0, 154.0],
        'AST': [56.0, 38.0, 57.0, 67.0, 77.0],
        'STL': [45.0, 45.0, 12.0, 16.0, 23.0],
        'BLK': [12.0, 1.0, 12.0, 11.0, 10.0],
        'PTS': [567.0, 800.0, 490.0, 333.0, 499.0],
        'HOF': [1, 1, 0, 0, 0]
    }

    test_inputs = pd.DataFrame(data=inputs)

    expected_model = {
        'PLAYER': ['Joe Dirt'],
        'YEARS': [2],
        'WS': [9.7],
        'THREE': [2],
        'REB': [2.24],
        'AST': [.94],
        'STL': [0.9],
        'BLK': [.13],
        'PTS': [13.67],
        'HOF_A': [1]
    }

    test_outputs_m = pd.DataFrame(data=expected_model)

    expected_non_model = {
        'PLAYER': ['Peter Pan'],
        'YEARS': [2],
        'WS': [3.5],
        'THREE': [1.67],
        'REB': [2.82],
        'AST': [1.44],
        'STL': [.39],
        'BLK': [.21],
        'PTS': [8.32],
        'HOF_A': [0]
    }

    test_outputs_nm = pd.DataFrame(data=expected_non_model)

    assert isinstance(test_outputs_m, pd.DataFrame)
    assert isinstance(test_outputs_nm, pd.DataFrame)

    assert False not in (test_outputs_m.values == load_data.create_agg_filter(test_inputs,**d['create_agg_filter'])[0].values)
    assert False not in (test_outputs_nm.values == load_data.create_agg_filter(test_inputs, **d['create_agg_filter'])[1].values)



def test_get_params():

    params = {'learning_rate':0.2, 'n_estimators':85, 'max_depth' : 6}

    exp_lr = params['learning_rate']
    exp_n_est = params['n_estimators']
    exp_max_depth = params['max_depth']

    assert exp_lr == fit_model.get_params(params)[0]
    assert exp_n_est == fit_model.get_params(params)[1]
    assert exp_max_depth == fit_model.get_params(params)[2]


def test_get_cv_params():

    cv_params = {'n_splits':10, 'n_repeats':10}

    exp_split = cv_params['n_splits']
    exp_repeat = cv_params['n_repeats']

    assert exp_split == fit_model.get_cv_params(cv_params)[0]
    assert exp_repeat == fit_model.get_cv_params(cv_params)[1]

def test_model_fit():

    d = {'model_fit':
    {
        'get_params': {
            'params': {'learning_rate': 0.2, 'n_estimators': 85, 'max_depth': 6}},
        'get_cv_params': {
            'cv_params': {'n_splits': 5, 'n_repeats': 5}}
    }
    }

    np.random.seed(seed=0)
    df = pd.DataFrame(columns=['PLAYER', 'YEARS', 'WS', 'THREE', 'REB', 'AST', 'STL', 'BLK', 'PTS', 'HOF_A'])

    PLAYER = ['a' for i in range(100)]
    YEARS = np.random.randint(2, 7, 100).tolist()
    WS = np.random.randint(1, 11, 100).tolist()
    THREE = np.random.randint(0, 3, 100).tolist()
    REB = np.random.randint(2, 12, 100).tolist()
    AST = np.random.randint(2, 10, 100).tolist()
    STL = np.random.randint(0, 2, 100).tolist()
    BLK = np.random.randint(0, 2, 100).tolist()
    PTS = np.random.randint(6, 25, 100).tolist()
    HOF_A = np.random.choice(2, 100, replace=True, p=[.9, .1]).tolist()

    df['PLAYER'] = PLAYER
    df['YEARS'] = YEARS
    df['WS'] = WS
    df['THREE'] = THREE
    df['REB'] = REB
    df['AST'] = AST
    df['STL'] = STL
    df['BLK'] = BLK
    df['PTS'] = PTS
    df['HOF_A'] = HOF_A


    with open('model_test.pkl', "wb") as f:
        #logger.info("model saved as a .pkl file")
        pickle.dump(fit_model.model_fit(df,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'],132,**d['model_fit'])[0], f)

    print(fit_model.model_fit(df,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'],132,**d['model_fit'])[1].index.tolist())

    assert type(fit_model.model_fit(df,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'],132,**d['model_fit'])[0]) is GradientBoostingClassifier

    assert fit_model.model_fit(df,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'],132,**d['model_fit'])[1].index.tolist() == ['PTS', 'WS', 'REB', 'BLK', 'YEARS', 'AST', 'THREE', 'STL']

    assert np.round(fit_model.model_fit(df,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'],132,**d['model_fit'])[2],2) == .26


def test_model_score():


    df = pd.DataFrame(columns=['PLAYER', 'YEARS', 'WS', 'THREE', 'REB', 'AST', 'STL', 'BLK', 'PTS', 'HOF_A'])

    np.random.seed(seed=0)
    PLAYER = ['a' for i in range(20)]
    YEARS = np.random.randint(2, 7, 20).tolist()
    WS = np.random.randint(1, 11, 20).tolist()
    THREE = np.random.randint(0, 3, 20).tolist()
    REB = np.random.randint(2, 12, 20).tolist()
    AST = np.random.randint(2, 10, 20).tolist()
    STL = np.random.randint(0, 2, 20).tolist()
    BLK = np.random.randint(0, 2, 20).tolist()
    PTS = np.random.randint(6, 25, 20).tolist()
    HOF_A = [0 for i in range(20)]

    df['PLAYER'] = PLAYER
    df['YEARS'] = YEARS
    df['WS'] = WS
    df['THREE'] = THREE
    df['REB'] = REB
    df['AST'] = AST
    df['STL'] = STL
    df['BLK'] = BLK
    df['PTS'] = PTS
    df['HOF_A'] = HOF_A

    df_predict = test_model.model_score(df,'model_test.pkl',['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'])

    os.remove("model_test.pkl")

    assert isinstance(df_predict, pd.DataFrame)

    assert len(df_predict[df_predict.HOF_P == 'Y']) == 5

    assert len(df_predict[(df_predict.PROB < 0) |(df_predict.PROB > 1) ]) == 0

    assert df_predict.shape[1] == 12

def test_euc_dist():

    df_new = pd.DataFrame(
        columns=['PLAYER', 'YEARS', 'WS', 'THREE', 'REB', 'AST', 'STL', 'BLK', 'PTS', 'HOF_A', 'PROB', 'HOF_P'])

    df_new = df_new.append(
        {'PLAYER': 'Max', 'YEARS': 7, 'WS': 6.7, 'THREE': 1.2, 'REB': 7.8, 'AST': 4.8, 'STL': 1.3, 'BLK': 1.7,
         'PTS': 21.5, 'HOF_A': 0, 'PROB': 0.67, 'HOF_P': 'Y'}, ignore_index=True)

    df_new = df_new.append({'PLAYER': 'Joe', 'YEARS': 7, 'WS': 5, 'THREE': 1.2, 'REB': 9.8, 'AST': 4.8, 'STL': 1.3, 'BLK': 1.4,
                    'PTS': 15.5, 'HOF_A': 0, 'PROB': 0.2, 'HOF_P': 'N'}, ignore_index=True)

    old = {
        'PLAYER': ['Joe Dirt', 'Peter Pan', 'William Wallace'],
        'YEARS': [8, 6, 7],
        'WS': [9.7, 5.5, 4.3],
        'THREE': [2, 1.5, 0.7],
        'REB': [10.5, 6.7, 4.3],
        'AST': [5.6, 1.6, 4.2],
        'STL': [0.9, 1.1, 2.1],
        'BLK': [.13, 1.1, 1.0],
        'PTS': [20.1, 12.3, 14.5],
        'HOF_A': [1, 0, 0]
    }

    old_df = pd.DataFrame(data=old)

    euc = similarity.euc_dist(df_new,old_df,'Max',2,['YEARS','WS','THREE','REB','AST','STL','BLK','PTS'])

    assert len(euc) == 2

    assert euc.shape[1] == 3

































