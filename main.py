import pandas as pd
from collections import Counter
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

data = pd.read_csv('./Data/EF_X_Stream.csv')
data['date_time'] = pd.to_datetime(data['date_time'])
data['lower_name'] = data['name'].str.lower()
data['lower_message'] = data['message'].str.lower().replace('ź', 'z').replace('ż', 'z').replace('ę', 'e').replace('ą', 'a').replace('ó', 'o').replace('ć', 'c').replace('ł', 'l').replace('ś', 's')
data['message_no_space'] = data['lower_message'].str.replace(' ', '')
data['message_name']=data['lower_name'].str.replace(' ', '').replace('ź', 'z').replace('ż', 'z').replace('ę', 'e').replace('ą', 'a').replace('ó', 'o').replace('ć', 'c').replace('ł', 'l').replace('ś', 's')+' '+data['message_no_space']
data['message_name_spaces']=data['lower_name'].replace('ź', 'z').replace('ż', 'z').replace('ę', 'e').replace('ą', 'a').replace('ó', 'o').replace('ć', 'c').replace('ł', 'l').replace('ś', 's')+' '+ data['lower_message']
data = data.sort_values('date_time')



plt.figure(figsize=(12,10))

#sns.lineplot(x='date_time', y='amount_num', data=data.head(50))
plt.subplot(2, 2, 1)
sns.barplot(data=data.groupby('goal').goal.count())
plt.xlabel('Cel')
plt.ylabel('')
plt.title('Liczba wpłat podczas poszczególnych celów')

plt.subplot(2, 2, 2)
sns.barplot(data=data.groupby('goal').amount_num.sum(), color='orange')
plt.xlabel('Cel')
plt.ylabel('[zł]')
plt.title('Suma wpłat podczas poszczególnych celów')

plt.subplot(2,2,3)
duration = data.groupby('goal').date_time.max() - data.groupby('goal').date_time.min()
duration_in_minutes = duration.dt.total_seconds() / 60
duration_in_minutes.iloc[0] -= 168
sns.barplot(data=duration_in_minutes, color='purple')
plt.xlabel('Cel')
plt.ylabel('[min]')
plt.title('Czas trwania poszczególnych celów')

plt.subplot(2,2,4)
avg_donation = data.groupby('goal').amount_num.sum()/duration_in_minutes
sns.barplot(data=avg_donation, color='green')
print(avg_donation)
plt.xlabel('Cel')
plt.ylabel('[zł/min]')
plt.title('Średnia wpłat na minutę podczas poszczególnych celów')

plt.tight_layout()

plt.show()

#~~~~~~~~~~~~~~

plt.figure(figsize=(12,10))

plt.subplot(2, 1, 1)
sns.lineplot(data=data, x='date_time', y='amount_num', color='blue')
plt.xlabel('Czas')
plt.ylabel('[zł]')
plt.title('Wartość wpłat')
plt.xlim(data['date_time'].iloc[0], data['date_time'].iloc[-1])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

plt.subplot(2, 1, 2)
data['accumulated_values'] = data['amount_num'].cumsum()
#print(accumulated_values.head(100))
sns.lineplot(data=data, x='date_time', y='accumulated_values', color='orange')
plt.fill_between(data['date_time'], data['accumulated_values'], alpha=0.3, color='orange')
plt.xlim(data['date_time'].iloc[0], data['date_time'].iloc[-1])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.xlabel('Czas')
plt.ylabel('[zł]')
plt.title('Kumulowana wartość wpłat')
plt.tight_layout()

plt.show()

# ~~~~~~~~~~~~~~~~~~~~

plt.figure(figsize=(12,10))

most_common_amounts = data.groupby('amount').count().sort_values(ascending=False, by='name').head(30)
sns.barplot(data=most_common_amounts, y='amount', x='name' , orient='h', color='purple')

for i, v in enumerate(most_common_amounts['name']):
    plt.text(v + 0.1, i, str(v), color='black', va='center', fontweight='bold')

donations_above_50 = data['amount_num'].loc[(data.amount_num >= 50)].count()
print(donations_above_50)
plt.xlabel('Ilość wpłat')
plt.ylabel('Wartość wpłaty')
plt.title('Ilość poszczególnych kwot wpłat (top30)')
plt.tight_layout()
plt.show()

#~~~~~~~~~~~~~~~~~~~~

bins = [0, 2.49, 4.99, 9.99, 24.99, 49.99, 99.99, 249.99, 499.99, 999.99, 2499.99, 10000]
labels = ['1-2.5 zł', '2.5-5 zł', '5-10 zł', '10-25 zł', '25-50 zł', '50-100 zł', '100-250 zł', '250-500 zł', '500-1000 zł', '1000-2500 zł', '2500+zł']

data['amount_range'] = pd.cut(data['amount_num'], bins=bins, labels=labels, right=False)

# print(data[['amount_range','amount_num']].head(100))

heatmap_data = data.pivot_table(index='goal', columns='amount_range', aggfunc='size', fill_value=0)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Ilość wystąpień'})
plt.xlabel('Przedział kwotowy')
plt.ylabel('Numer celu')
plt.title('Ilość wystąpień wpłat każdego przedziału kwotowego podczas każdego celu')
plt.tight_layout()
plt.show()

# piotr_p = data[data['lower_name'].str.contains('p. dał|p dał|p  dał|pdał|p dal|p. dal', case=False)]
# polish_misiura=data[data['message_name'].str.contains('halamadrid', case=False)]
# print(piotr_p.head(100))


keywords = {
    'girona': 'Girona FC',
    'real|halamadrid': 'Real Madrid',
    'atletico': 'Atletico Madrid',
    'barcelona|barca|visca': 'FC Barcelona',
    'valencia': 'Valencia',
    'liverpool': 'Liverpool',
    'arsenal|kanonierzy': 'Arsenal',
    'astonvilla': 'Aston Villa',
    'manchestercity|mancity': 'Manchester City',
    'tottenham|totki': 'Tottenham',
    'manchesterunited|manutd|united': 'Manchester United',
    'newcastle': 'Newcastle United',
    'brighton': 'Brighton',
    'westham': 'West Ham United',
    'chelsea|czelsi': 'Chelsea',
    'bayern': 'Bayern Munich',
    'stuttgart': 'Stuttgart',
    'bayerl': 'Bayer Leverkusen',
    'rblipsk|rbleipzig': 'RB Leipzig',
    'bvb|borussia|dortmund|borusia': 'Borussia Dortmund',
    'hoffenheim': 'Hoffenheim',
    'wolfsburg': 'Wolfsburg',
    'inter': 'Inter Mediolan',
    'juventus|juve': 'Juventus',
    'milan': 'AC Milan',
    'roma': 'AS Roma',
    'bologna': 'Bologna',
    'napoli': 'Napoli',
    'fiorentina': 'Fiorentina',
    'atalanta': 'Atalanta',
    'lazio': 'Lazio',
    'hilal': 'Al-Hilal',
    'ajax': 'Ajax',
    'lens': 'Lens',
    'benfica': 'Benfica Lisbon',
    'salzburg': 'RB Salzburg',
    'feyenoord': 'Feyenoord',
    'psg': 'Paris Saint Germain',
    'celtic': 'Celtic Glasgow',
    'porto': 'FC Porto',
    'nassr|alnasr': 'Al-Nassr',
    'lech|kolejorz': 'Lech Poznań',
    'legia|legionista': 'Legia Warszawa',
    'slask': 'Śląsk Wrocław',
    'jagiellonia': 'Jagiellonia Białystok',
    'pogon': 'Pogoń Szczecin',
    'zaglebielubin': 'Zaglębie Lubin',
    'radomiak': 'Radomiak Radom',
    'gornik': 'Górnik Zabrze',
    'widzew': 'Widzew Łódź',
    'piast': 'Piast Gliwice',
    'warta': 'Warta Poznań',
    'puszcza': 'Puszcza Niepołomice',
    'cracovia': 'Cracovia Kraków',
    'ruchch': 'Ruch Chorzów',
    'lks': 'ŁKS Łódź',
    'wisla': 'Wisła Kraków',
    'wieczysta': 'Wieczysta Kraków'
}

results_list = []

for key, team_name in keywords.items():
    total_amount = data[data['message_name'].str.contains(key, case=False)]['amount_num'].sum()
    if team_name == 'ŁKS Łódź':
        total_amount = 132
    results_list.append({'Team': team_name, 'Total Amount': total_amount})


results = pd.DataFrame(results_list)

print(results.sort_values(by='Total Amount', ascending=False))

plt.figure(figsize=(12,10))
sns.barplot(data=results.sort_values('Total Amount',ascending=False).head(30), x='Total Amount', y='Team', orient='h', color='green')
plt.tight_layout()
plt.ylabel('Team')
plt.xlabel('Łączna kwota wpłat [zł]')
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~
hashtags = data['message_name_spaces'].str.findall(r'#\w+').explode()

hashtag_counts = hashtags.value_counts()

top_30_hashtags = hashtag_counts.head(30)

hashtag_counts_dict = {}

for hashtag in top_30_hashtags.index:
    hashtag_counts_dict[hashtag] = top_30_hashtags[hashtag]

sorted_hashtag_counts = dict(sorted(hashtag_counts_dict.items(), key=lambda x: x[1], reverse=True))

df_plot = pd.DataFrame(list(sorted_hashtag_counts.items()), columns=['Hasztag', 'Ilość wystąpień'])

hashtag_sums = {}

for hashtag in top_30_hashtags.index:
    filtered_data = data[data['message_name_spaces'].str.contains(str(hashtag), case=False, regex=True)]
    hashtag_sums[hashtag] = filtered_data['amount_num'].sum()

sorted_hashtag_sums = dict(sorted(hashtag_sums.items(), key=lambda x: x[1], reverse=True))
df_plot_sums = pd.DataFrame(list(sorted_hashtag_sums.items()), columns=['Hasztag', 'Suma wartości donejtów'])

plt.figure(figsize=(12, 10))
sns.barplot(data=df_plot, x='Ilość wystąpień', y='Hasztag', orient='h')
plt.xlabel('')
plt.title('Najpopularniejsze hasztagi - ilość wystąpień')

plt.tight_layout()

plt.show()

#~~~~~~~~~~~~~~

all_words = ' '.join(data['message']).lower().split()

word_counter = Counter(all_words)

most_common_word = word_counter.most_common(2)[1][1]

print(f"Najczęściej występujące słowo: {most_common_word}")

common_words_df = pd.DataFrame(word_counter.most_common(10), columns=['Słowo', 'Ilość wystąpień'])
plt.bar(common_words_df['Słowo'], common_words_df['Ilość wystąpień'])
plt.xlabel('Słowo')
plt.ylabel('Ilość wystąpień')
plt.title('Najczęściej występujące słowa')
plt.show()