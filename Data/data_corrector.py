import pandas as pd

# Wczytaj dane z pliku CSV
data = pd.read_csv('donations_data.csv')

# Funkcja do konwersji kwoty na liczbę
def convert_amount(amount_str):
    if isinstance(amount_str, str) and amount_str.endswith(' zł'):
        # Usuń ' zł' oraz zamień przecinek na kropkę
        amount_str = amount_str.replace(' zł', '').replace(',', '.')
        # Spróbuj skonwertować na float
        try:
            return float(amount_str)
        except ValueError:
            return None
    else:
        return None

# Dodaj nową kolumnę 'amount_num' do ramki danych
data['amount_num'] = data['amount'].apply(convert_amount)

data.to_csv('EF_X_Stream.csv', index=False)

test=pd.read_csv('EF_X_Stream.csv')
# Wyświetl zaktualizowane dane
print(test['date_time'].head(50))