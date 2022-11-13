import pandas as pd
import json

if __name__ == '__main__':

    stocksDf = pd.read_parquet('./stocks_all.parquet')
    etfsDf = pd.read_parquet('./etfs_all.parquet')

    df = pd.concat((stocksDf, etfsDf))

    df.to_parquet('./combined.parquet')

    big = {}
    for symbol in df.index.values:
        val = df.loc[symbol].dropna().to_dict()
        big[symbol] = val
        
    with open(f'combined.json', 'w') as outfile:
        json.dump(big, outfile)