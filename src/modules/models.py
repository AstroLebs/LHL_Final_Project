import sklearn
import xgboost
import pandas as pd
import scipy
import numpy as np
import _pickle as cPickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    auc,
    accuracy_score,
    confusion_matrix,
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


def model():
    with open(r"../Data/test_optimize.pickle", "rb") as inputfile:
        df = cPickle.load(inputfile)

    y = df.pop("FPL_points")
    df = df.T.reset_index(drop=True).T

    numeric_features = df.T[2:].T.columns.to_list()
    numeric_transformer = StandardScaler()

    categorical_features = df.T[:2].T.columns.to_list()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    X = df[categorical_features + numeric_features]

    print(X.shape)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("model", xgb.XGBRegressor())]
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    params = {
        "model__colsample_bytree": uniform(0.7, 0.3),
        "model__gamma": uniform(0, 0.5),
        "model__learning_rate": uniform(0.03, 0.3),
        "model__max_depth": randint(2, 6),
        "model__n_estimators": randint(100, 150),
        "model__subsample": uniform(0.6, 0.4),
    }

    search = RandomizedSearchCV(
        model,
        param_distributions=params,
        random_state=3791,
        n_iter=1000,
        cv=10,
        verbose=1,
        return_train_score=True,
    )

    search.fit(X_train, y_train)

    report_best_scores(search.cv_results_)

    y_pred = search.best_estimator_.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    return y_pred, mse, rmse, r2
