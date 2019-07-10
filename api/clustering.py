# import hdbscan
import pandas as pd

def hdbscan():
    # Load the dataset in a dataframe object and include only four features as mentioned
    # url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
    df = pd.read_csv(open('data/Chicago_Crimes_2005.csv'))
    include = ['Latitude' , 'Longitude'] # features
    df_ = df[include]

    # Data Preprocessing
    categoricals = []
    for col, col_type in df_.dtypes.iteritems():
         if col_type == 'O':
              categoricals.append(col)
         else:
              df_[col].fillna(0, inplace=True)

    df_ohe = pd.get_dummies(df_, columns=categoricals, dummy_na=True)
