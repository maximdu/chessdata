## ML Course project

The task is to predict player's ELO rating based on moves played in their game.
Dataset: open data from Lichess database (https://database.lichess.org/)

Pipeline (these steps correspond to jupyter notebooks):
1. Parse data to a table format
2. Extract features from data
3. Perform binning (to prevent overfitting)
4. Add mean encoding to categorical features
5. Train and compare models
6. (additional) Visualize data using PCA
7. (additional) Change task from regression to multi-class classification
