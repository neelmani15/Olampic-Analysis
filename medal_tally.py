import pandas as pd

def process(df,df_region):
    df= df.merge(df_region,on='NOC',how='left')
    df = df[df['Season']=='Summer']
    # Dropping duplicates
    df.drop_duplicates(inplace=True)
    # Get dummy data for medal
    dummy = pd.get_dummies(df['Medal'])
    df1 = pd.concat([df, dummy], axis=1)
    return df1