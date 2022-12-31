import pandas as pd
import json
import numpy as np
import time


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    

def camelCaseSplit(s):
    lastWasLower = False
    out = ""
    for char in s:
        isUpper = char == char.upper()
        if lastWasLower and isUpper and char.isalpha():
            out += " "
        out += char
        lastWasLower = not isUpper
    print('split', s, '=>', out.title())
    return out.title()
            
            
candleMap = {"2CROWS":"Two Crows","3BLACKCROWS":"Three Black Crows","3INSIDE":"Three Inside Up/Down","3LINESTRIKE":"Three-Line Strike","3OUTSIDE":"Three Outside Up/Down","3STARSINSOUTH":"Three Stars In The South","3WHITESOLDIERS":"Three Advancing White Soldiers","ABANDONEDBABY":"Abandoned Baby","ADVANCEBLOCK":"Advance Block","BELTHOLD":"Belt-hold","BREAKAWAY":"Breakaway","CLOSINGMARUBOZU":"Closing Marubozu","CONCEALBABYSWALL":"Concealing Baby Swallow","COUNTERATTACK":"Counterattack","DARKCLOUDCOVER":"Dark Cloud Cover","DOJI":"Doji","DOJISTAR":"Doji Star","DRAGONFLYDOJI":"Dragonfly Doji","ENGULFING":"Engulfing Pattern","EVENINGDOJISTAR":"Evening Doji Star","EVENINGSTAR":"Evening Star","GAPSIDESIDEWHITE":"Up/Down-Gap Side-by-Side White Lines","GRAVESTONEDOJI":"Gravestone Doji","HAMMER":"Hammer","HANGINGMAN":"Hanging Man","HARAMI":"Harami Pattern","HARAMICROSS":"Harami Cross Pattern","HIGHWAVE":"High-Wave Candle","HIKKAKE":"Hikkake Pattern","HIKKAKEMOD":"Modified Hikkake Pattern","HOMINGPIGEON":"Homing Pigeon","IDENTICAL3CROWS":"Identical Three Crows","INNECK":"In-Neck Pattern","INVERTEDHAMMER":"Inverted Hammer","KICKING":"Kicking","KICKINGBYLENGTH":"Kicking","LADDERBOTTOM":"Ladder Bottom","LONGLEGGEDDOJI":"Long Legged Doji","LONGLINE":"Long Line Candle","MARUBOZU":"Marubozu","MATCHINGLOW":"Matching Low","MATHOLD":"Mat Hold","MORNINGDOJISTAR":"Morning Doji Star","MORNINGSTAR":"Morning Star","ONNECK":"On-Neck Pattern","PIERCING":"Piercing Pattern","RICKSHAWMAN":"Rickshaw Man","RISEFALL3METHODS":"Rising/Falling Three Methods","SEPARATINGLINES":"Separating Lines","SHOOTINGSTAR":"Shooting Star","SHORTLINE":"Short Line Candle","SPINNINGTOP":"Spinning Top","STALLEDPATTERN":"Stalled Pattern","STICKSANDWICH":"Stick Sandwich","TAKURI":"Takuri (Dragonfly Doji with very long lower shadow)","TASUKIGAP":"Tasuki Gap","THRUSTING":"Thrusting Pattern","TRISTAR":"Tristar Pattern","UNIQUE3RIVER":"Unique 3 River","UPSIDEGAP2CROWS":"Upside Gap Two Crows","XSIDEGAP3METHODS":"Upside/Downside Gap Three Methods"}
    
    
def renameDf(df):
    print(df)
    df.drop(columns=["len", "date"], inplace=True)
    
    renamings = {}
    translations = {
        "natr": "Vol. Range",
        "sup": "Support",
        "res": "Resistance",
        "drawup": "Max Gain",
        "drawdown": "Max Loss",
        "div": "Dividend Yield",
        "rsi": "Rel. Strength",
        "adx": "Trend Dir."
    }
    for colName in df.columns:
        if "pattern" in colName.lower():
            newCol = "num " + colName
            df[newCol] = df[colName].apply(lambda x: len(x) if x is not None else None)
            df[colName] = df[colName].apply(lambda x: ' | '.join([candleMap[candle] for candle in x]) if x is not None else None)
    toDrop = []
    for colName in df.columns:
        print(colName)
        split = colName.split('_')
        key = split[0]
        out = key
        if key[-1] == '%':
            toDrop.append(colName)
        if out in translations:
            out = translations[out]
        else:
            out = camelCaseSplit(out)
        if len(split) > 1:
            timeframe = split[1]
            out += " "
            out += timeframe
            if not out.endswith('mo'):
                out += 'y'
        print(out)
        renamings[colName] = out
        
    df.index.names = ['Symbol']
    df.drop(columns=toDrop, inplace=True)
    df.rename(columns=renamings, inplace=True)
    sortedCols = sorted(df.columns, key=lambda x: x.lower().replace("10y", "0").replace("5y", "1").replace("1y", "2"))
    print('duplicated cols', df.index.duplicated())
    df = df.reindex(sortedCols, axis=1)
    
    for colName, dtype in zip(df.columns, df.dtypes):
        if np.issubdtype(dtype, np.number):
            N = 3
            def rounder(x):
                try:
                    return round(x, N - int(np.floor(np.log10(abs(x)))))
                except:
                    return x
            df[colName] = df[colName].apply(rounder)
    
    return df
        
        
    

if __name__ == '__main__':

    stocksDf = pd.read_parquet('./stocks_all.parquet')
    etfsDf = pd.read_parquet('./etfs_all.parquet')

    df = pd.concat((stocksDf, etfsDf))

    df.to_parquet('./combined.parquet')
    
    df = renameDf(df)
    
    with open('combined.csv', 'w') as f:
        f.write(str(int(time.time())) + '\n')
        
    with np.printoptions(linewidth=100000000):
        df.to_csv('combined.csv', mode='a')
