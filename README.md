## ML Course project

The task is to predict player's ELO rating based on moves played in their game.

Dataset: open data from Lichess database (https://database.lichess.org/)

Inspired by **"Guess the ELO"** by GothamChess

Pipeline (these steps correspond to jupyter notebooks):
1. Parse and filter data to a table format
2. Convert cantipawn evaluation to odds of winning
3. (optional) Grid search for features
4. Extract features from data
5. Perform binning
6. Add mean encoding to categorical features
7. (optional) Visualize data using PCA
8. Train and compare regression models
9. (optional) Change task from regression to multi-class classification

Results (CatBoost model, cross-validation):

![pic](https://github.com/maximdu/chessdata/blob/main/chessdata/presentation/images/catboost_r2.png?raw=true)

![pic](https://github.com/maximdu/chessdata/blob/main/chessdata/presentation/images/catboost_mae.png?raw=true)

PCA visualization:
