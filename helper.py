import pandas as pd

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def df_to_text(df, max_rows=10):
    return df.head(max_rows).to_string(index=False)
