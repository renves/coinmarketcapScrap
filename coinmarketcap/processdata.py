import pandas as pd

data = pd.read_csv('raw_data.csv')

data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

data['market_cap'] = data['market_cap'].str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False).astype(float)

data['price'] = data['price'].astype(str).str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False)

data['volume'] = data['price'].str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False)

data['circulating_supply'] = data['circulating_supply'].str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False)

data['%_24h'] = data['%_24h'].str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False)

data['%_7d'] = data['%_7d'].str.replace(
    '$', '', regex=False).str.replace(',', '', regex=False)

data.sort_values(['date', 'rank'], inplace=True)

data = data[data['rank'] <= 20]
data.to_csv('data.csv', index=False)
data.to_excel('data.xlsx', index=False)
