import sklearn
import xgboost
import pandas as pd
import scipy
import numpy as np
import _pickle as cPickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (
    cross_val_score,
    GridSearchCV,
    KFold,
    RandomizedSearchCV,
    train_test_split,
)
import xgboost as xgb
from scipy.stats import uniform, randint
from modules import constants


def model(df):
    df = df.fillna(0)
    y = df.pop("FPL_points")
    df = df.T.reset_index(drop=True).T
    categorical_preprocessing = Pipeline([
    ('onehot', OneHotEncoder(handle_unknown='ignore')),])

    numerical_preprocessing = Pipeline([
    ('KNNImputer', KNNImputer()),
    ('scaler', StandardScaler()),])

    
    preprocessing = ColumnTransformer(
                    [
                        ('catecorical', categorical_preprocessing,
                         make_column_selector(dtype_include=object)),
                        ('numerical', numerical_preprocessing,
                         make_column_selector(dtype_exclude=object)),
                    ])

    model = Pipeline(
        steps=[("preprocessing", preprocessing), ("model", xgb.XGBRegressor())]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        df, y, test_size=0.2, random_state=0
    )

    RANDSCV_PARAMS = {
        "model__colsample_bytree": uniform(0.7, 0.3),
        "model__gamma": uniform(0, 0.5),
        "model__learning_rate": uniform(0.03, 0.3),
        "model__max_depth": randint(2, 6),
        "model__n_estimators": randint(100, 150),
        "model__subsample": uniform(0.6, 0.4),
    }
    search = RandomizedSearchCV(
        model,
        param_distributions=RANDSCV_PARAMS,
        random_state=3791,
        n_iter=100,
        cv=10,
        verbose=1,
        return_train_score=True,
    )
    search.fit(X_train, y_train)
    y_pred = search.best_estimator_.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    return search, y_pred, mse, rmse, r2
