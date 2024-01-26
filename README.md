## ML Course project

The task is to predict player's ELO rating based on moves played in their game.

Dataset: open data from Lichess database (https://database.lichess.org/)

Inspired by **"Guess the ELO"** by GothamChess

Pipeline (these steps correspond to jupyter notebooks):
1. Parse and filter data to a table format
2. Extract features from data
3. Perform binning (to prevent overfitting)
4. Add mean encoding to categorical features
5. Train and compare models
6. (optional) Visualize data using PCA
7. (optional) Change task from regression to multi-class classification
8. (optional) Try neural network model

Results (CatBoost model, cross-validation):

![pic](https://github.com/maximdu/chessdata/blob/main/chessdata/presentation/images/catboost_r2.png?raw=true)

![pic](https://github.com/maximdu/chessdata/blob/main/chessdata/presentation/images/catboost_mae.png?raw=true)

PCA visualization:
![pic](https://github.com/maximdu/chessdata/blob/main/chessdata/presentation/images/pca.png?raw=true)
