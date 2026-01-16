

def check_and_drop_column(df, column):
    if df[column].eq(df[column].iloc[0]).all():
        df = df.drop(column, axis=1)
    else:
        print('your data not same')
    return df
def chek_data(df) :
   dattype =  df.dtypes
   num_un = df.nunique()
   return pd.DataFrame( {'data type' : dattype,'numbers_uniq ':num_un}).T 