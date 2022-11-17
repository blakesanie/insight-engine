import pandas as pd
import json
import numpy as np
import time


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    stocksDf = pd.read_parquet('./stocks_all.parquet')
    etfsDf = pd.read_parquet('./etfs_all.parquet')

    df = pd.concat((stocksDf, etfsDf))

    df.to_parquet('./combined.parquet')
    
    with open('combined.csv', 'w') as f:
        f.write(str(int(time.time())) + '\n')
        
    df.to_csv('combined.csv', mode='a')
    
