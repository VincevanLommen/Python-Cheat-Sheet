# 📊 Data Processing — Volledige Cheat Sheet
### Pandas · Matplotlib · Datetime · Apply
> Alles wat je nodig hebt, met volledige uitleg en voorbeelden. Elke functie, elke parameter.

---

## IMPORTS — Altijd bovenaan je notebook

```python
import pandas as pd           # DataFrames en Series
import matplotlib.pyplot as plt  # grafieken
import numpy as np            # NaN-waarden, wiskunde
from math import *            # sqrt, floor, ceil, ...
```

---

# DEEL 1 — DATAFRAME AANMAKEN

---

## `pd.DataFrame(data, columns=..., index=...)`

Maakt een DataFrame. `data` kan een **dictionary**, **lijst van lijsten**, of **CSV** zijn.

### Vanuit een dictionary (meest gebruikt)
Elke sleutel = kolomnaam, elke waarde = lijst met kolomdata.

```python
data = {
    'Name':   ['Alice', 'Bob', 'Charlie'],
    'Age':    [25, 30, 35],
    'Salary': [60000, 75000, 80000]
}
df = pd.DataFrame(data)
```
```
     Name  Age  Salary
0   Alice   25   60000
1     Bob   30   75000
2  Charlie  35   80000
```

### Vanuit een lijst van lijsten
Elke binnenste lijst = één rij. Kolomnamen zijn standaard 0, 1, 2, ... — geef ze mee via `columns=`.

```python
data = [['Alice', 25, 'Brussel'],
        ['Bob',   30, 'Gent'],
        ['Carol', 35, 'Antwerpen']]

df = pd.DataFrame(data, columns=['Name', 'Age', 'City'])
```

### Met eigen index
```python
df = pd.DataFrame(data, columns=['Name', 'Age', 'City'],
                  index=['person1', 'person2', 'person3'])
```

---

## `pd.read_csv(filepath, sep=',', index_col=..., header=...)`

Laadt een CSV-bestand in een DataFrame.

```python
df = pd.read_csv('data.csv')                     # basisgebruik
df = pd.read_csv('data.csv', sep=',')            # scheidingsteken (standaard = komma)
df = pd.read_csv('data.csv', sep=';')            # puntkomma als scheidingsteken
df = pd.read_csv('data.csv', index_col=0)        # gebruik kolom 0 als rij-index
df = pd.read_csv('data.csv', index_col='Name')   # gebruik kolomnaam als index
df = pd.read_csv('data.csv', header=0)           # rij 0 = kolomnamen (standaard)
df = pd.read_csv('data.csv', header=None)        # geen kolomnamen in het bestand
```

**Na inlezen: verwijder de naam van de index-kolom (vaak gevraagd):**
```python
df.index.name = None
```

---

## `df.to_csv(filepath, index=True/False)`

Schrijft een DataFrame naar een CSV-bestand.

```python
df.to_csv('output.csv')            # schrijft ook de index-kolom
df.to_csv('output.csv', index=False)  # schrijft GEEN index-kolom (meestal beter)
```

---

# DEEL 2 — INSPECTIE

---

## `df.head(n)` / `df.tail(n)`

Toont de eerste of laatste `n` rijen. Standaard = 5.

```python
df.head()      # eerste 5 rijen
df.head(8)     # eerste 8 rijen
df.tail()      # laatste 5 rijen
df.tail(3)     # laatste 3 rijen
```
> ⚠️ Returnt een **nieuwe DataFrame** — past het origineel niet aan.

---

## `df.info()`

Toont kolomnamen, datatypes en hoeveel non-null waarden elke kolom heeft.

```python
df.info()
# Output:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3 entries, 0 to 2
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
#  0   Name    3 non-null      object   ← string
#  1   Age     3 non-null      int64
#  2   Salary  3 non-null      int64
```

---

## `df.describe()`

Geeft statistieken voor alle **numerieke** kolommen: count, mean, std, min, 25%, 50%, 75%, max.

```python
df.describe()
#         Age         Salary
# count   3.000000     3.000000
# mean   30.000000  71666.666667
# std     5.000000  10408.329997
# min    25.000000  60000.000000
# 25%    27.500000  67500.000000
# 50%    30.000000  75000.000000
# 75%    32.500000  77500.000000
# max    35.000000  80000.000000
```

---

## `df.shape`

Returnt `(aantal rijen, aantal kolommen)` als tuple. **Geen haakjes** — het is een attribuut, geen methode.

```python
print(df.shape)     # → (3, 3)
print(df.shape[0])  # → 3  (aantal rijen)
print(df.shape[1])  # → 3  (aantal kolommen)
```

---

## `df.dtypes`

Toont het datatype van elke kolom.

```python
print(df.dtypes)
# Name      object   ← string
# Age        int64
# Salary     int64
```

---

## `df.columns` / `df.index`

```python
print(df.columns)   # → Index(['Name', 'Age', 'Salary'], dtype='object')
print(df.index)     # → RangeIndex(start=0, stop=3, step=1)
```

---

# DEEL 3 — KOLOMNAMEN EN INDEX AANPASSEN

---

## Kolomnamen wijzigen

### Alle kolomnamen tegelijk:
```python
df.columns = ['Naam', 'Leeftijd', 'Loon']
```

### Specifieke kolommen via `df.rename()`:
```python
# Zonder inplace → returnt nieuwe DataFrame, origineel ongewijzigd:
nieuwe_df = df.rename(columns={'Name': 'Naam', 'Age': 'Leeftijd'})

# Met inplace=True → past df zelf aan:
df.rename(columns={'Name': 'Naam'}, inplace=True)
```

---

## Index (rijnamen) wijzigen

### Alle indices tegelijk:
```python
df.index = ['person1', 'person2', 'person3']
```

### Specifieke indices via `df.rename()`:
```python
df.rename(index={'person1': 'p1', 'person2': 'p2'}, inplace=True)
```

### Kolom als index gebruiken via `df.set_index()`:
```python
df = df.set_index('Name')       # 'Name' wordt de index
df.index.name = None            # verwijder de naam boven de index (vaak gevraagd)
```

### Index resetten via `df.reset_index()`:
```python
df = df.reset_index(drop=True)   # reset naar 0, 1, 2, ... — gooit oude index weg
df = df.reset_index(drop=False)  # reset naar 0, 1, 2, ... — oude index wordt nieuwe kolom
```

---

# DEEL 4 — INDEXING EN SLICING

> **Gouden regel:** `loc` = labels, `iloc` = integers (positie).

---

## Een kolom selecteren

```python
df['Name']          # → Series (één kolom)
df[['Name', 'Age']] # → DataFrame (meerdere kolommen, dubbele haakjes!)
```

---

## `df.loc[rij, kolom]` — op basis van LABELS

- `loc` werkt met de namen/labels van rijen en kolommen.
- Bij slicen: **eindpunt is INCLUSIEF** (anders dan Python normaal).

```python
df.loc['person1']                     # hele rij met label 'person1'
df.loc['person1', 'Name']             # één cel: rij 'person1', kolom 'Name'
df.loc['person1':'person3']           # rijen person1 t/m person3 (inclusief!)
df.loc['person1':'person3', 'Name':'Age']  # rijen én kolommen op label
df.loc[:, 'Name':'Age']               # alle rijen, kolommen Name t/m Age
df.loc['person1':'person3', ['Name', 'City']]  # specifieke kolommen
```

---

## `df.iloc[rij, kolom]` — op basis van INTEGER POSITIE

- `iloc` werkt altijd met 0, 1, 2, ...
- Bij slicen: **eindpunt is EXCLUSIEF** (zoals gewone Python slicing).

```python
df.iloc[0]            # eerste rij (positie 0)
df.iloc[-1]           # laatste rij
df.iloc[0, 1]         # rij 0, kolom 1
df.iloc[1:4]          # rijen 1, 2, 3 (niet 4!)
df.iloc[1:4, 0:2]     # rijen 1-3, kolommen 0-1
df.iloc[:, 0]         # alle rijen, eerste kolom
df.iloc[-2:, :]       # laatste 2 rijen, alle kolommen
```

---

## `df.at[rij_label, kolom_label]` — één specifieke cel (snel)

```python
df.at['person1', 'Name']   # → 'Alice'
```

## `df.iat[rij_int, kolom_int]` — één cel op positie

```python
df.iat[0, 0]   # → 'Alice'
```

---

## Boolean filtering — rijen filteren op voorwaarde

```python
df[df['Age'] >= 30]                         # rijen waar leeftijd ≥ 30
df[df['City'] == 'Gent']                    # rijen waar stad = 'Gent'
df[df['Salary'] < 70000]                    # rijen waar loon < 70000

# Meerdere voorwaarden — gebruik & (en) of | (of), ALTIJD haakjes!
df[(df['Age'] >= 25) & (df['Age'] <= 35)]   # leeftijd tussen 25 en 35
df[(df['City'] == 'Gent') | (df['City'] == 'Brussel')]  # Gent of Brussel
df[~(df['City'] == 'Gent')]                 # ~ = NOT (niet Gent)

# isin() — waarde zit in een lijst:
df[df['City'].isin(['Gent', 'Brussel', 'Antwerpen'])]
```

---

# DEEL 5 — KOLOMMEN TOEVOEGEN EN VERWIJDEREN

---

## Nieuwe kolom toevoegen

```python
# Vaste waarde:
df['Country'] = 'Belgium'

# Op basis van een andere kolom:
df['Salary_Increase'] = df['Salary'] * 1.10   # 10% verhoging

# Op basis van meerdere kolommen:
df['Total'] = df['Pigeons'] + df['Sparrows'] + df['Others']

# Met een voorwaarde (np.where):
import numpy as np
df['Senior'] = np.where(df['Age'] >= 60, True, False)
# np.where(voorwaarde, waarde_als_waar, waarde_als_niet_waar)
```

---

## `df.drop()` — kolom of rij verwijderen

```python
# Kolom verwijderen:
df = df.drop(columns=['Experience'])
df = df.drop(columns=['Col1', 'Col2'])   # meerdere tegelijk

# Alternatieve syntax (axis=1 = kolom):
df = df.drop(['Experience'], axis=1)

# Rij verwijderen:
df = df.drop('person3')         # rij met label 'person3'
df = df.drop([0, 1, 2])        # rijen met labels 0, 1, 2

# ⚠️ zonder inplace/toewijzing past het origineel NIET aan:
df.drop(columns=['Experience'])     # GEEN EFFECT op df
df = df.drop(columns=['Experience'])  # JUIST
df.drop(columns=['Experience'], inplace=True)  # ook juist
```

---

# DEEL 6 — SORTEREN

---

## `df.sort_values(by, ascending=True, inplace=False)`

Sorteert rijen op basis van één of meerdere kolommen.

```python
# A→Z / klein→groot (ascending=True is standaard):
df = df.sort_values(by='Name')
df = df.sort_values(by='Name', ascending=True)   # zelfde

# Z→A / groot→klein:
df = df.sort_values(by='Age', ascending=False)

# Op meerdere kolommen:
df = df.sort_values(by=['City', 'Age'])                      # beide ascending
df = df.sort_values(by=['City', 'Age'], ascending=[True, False])  # City A→Z, Age Z→A

# Met inplace:
df.sort_values(by='Name', inplace=True)

# ⚠️ VALKUIL: zonder toewijzing of inplace heeft het geen effect:
df.sort_values(by='Name')   # GEEN EFFECT!
```

---

## `df.sort_index(ascending=True)`

Sorteert op basis van de **index** (rijnamen), niet op een kolom.

```python
df = df.sort_index()              # index A→Z of 0→n
df = df.sort_index(ascending=False)  # omgekeerd
```

---

# DEEL 7 — ONTBREKENDE WAARDEN (NaN)

---

## `df.isna()` / `df.isnull()` — controleer op NaN

```python
df.isna()          # DataFrame van True/False: True = NaN
df.isna().sum()    # aantal NaN-waarden per kolom
df.isna().any()    # True als er minstens één NaN is per kolom
```

---

## `df.dropna()` — rijen met NaN verwijderen

```python
df = df.dropna()             # verwijder alle rijen met minstens één NaN
df = df.dropna(how='all')    # verwijder rijen waar ALLE waarden NaN zijn
df = df.dropna(subset=['Salary'])  # verwijder rijen waar 'Salary' NaN is
df = df.dropna(subset=['Col1', 'Col2'])  # NaN in Col1 OF Col2 → weg

# ⚠️ VALKUIL: returnt nieuwe DataFrame, origineel ongewijzigd!
df.dropna()                  # GEEN EFFECT op df
df = df.dropna()             # JUIST
df.dropna(inplace=True)      # ook juist
```

---

## `df.fillna(value)` — NaN-waarden vervangen

```python
df = df.fillna(0)              # vervang alle NaN door 0
df = df.fillna('onbekend')     # vervang door een string
df['Salary'] = df['Salary'].fillna(df['Salary'].mean())  # vervang door gemiddelde

# Per kolom een andere waarde:
df = df.fillna({'Age': 0, 'City': 'Unknown'})
```

---

# DEEL 8 — STATISTIEKEN EN AGGREGATIE

---

## Basisstatistieken op een kolom of heel DataFrame

```python
df['Age'].sum()      # som
df['Age'].min()      # kleinste waarde
df['Age'].max()      # grootste waarde
df['Age'].mean()     # gemiddelde
df['Age'].median()   # mediaan (middelste waarde)
df['Age'].std()      # standaardafwijking
df['Age'].var()      # variantie
df['Age'].count()    # aantal non-null waarden
df['Age'].nunique()  # aantal unieke waarden

# Op heel DataFrame (geeft resultaat per kolom):
df.sum()
df.mean()
df.min()
df.max()
```

---

## `df.agg(['func1', 'func2', ...])` — meerdere statistieken tegelijk

```python
df_grades.agg(['sum', 'min', 'max', 'mean', 'median'])
#         math   Eng   Geo
# sum      35    37    40
# min       5     6     6
# max       9     9    10
# mean      7.0   7.4   8.0
# median    7.0   7.0   8.0
```

---

## `df.value_counts()` — tel hoe vaak elke waarde voorkomt

```python
df['City'].value_counts()
# Gent        5
# Brussel     3
# Antwerpen   2

# Gesorteerd op index (naam) i.p.v. waarde:
df['City'].value_counts().sort_index()
```

---

# DEEL 9 — GROEPEREN

---

## `df.groupby(kolom)` — groepeer en bereken per groep

```python
# Gemiddeld loon per stad:
df.groupby('City')['Salary'].mean()

# Aantal mensen per stad (count = telt non-null):
df.groupby('City').count()
df.groupby('City')['Name'].count()   # enkel Name-kolom tonen

# Totaal loon per afdeling:
df.groupby('Department')['Salary'].sum()

# Min en max per groep:
df.groupby('City')['Age'].min()
df.groupby('City')['Age'].max()

# Groeperen op meerdere kolommen:
df.groupby(['City', 'Department'])['Salary'].mean()
```

### `size()` vs `count()` na groupby

```python
df.groupby('City').size()    # telt ALLE rijen incl. NaN
df.groupby('City').count()   # telt enkel non-null waarden per kolom
```

### `agg()` na groupby — meerdere functies tegelijk

```python
df.groupby('City')['Salary'].agg(['min', 'max', 'mean'])
```

---

# DEEL 10 — SAMENVOEGEN VAN DATAFRAMES

---

## `pd.concat([df1, df2], axis=...)` — DataFrames samenvoegen

```python
# Rijen samenvoegen (onder elkaar plakken), axis=0 is standaard:
df_total = pd.concat([df1, df2])
df_total = pd.concat([df1, df2], axis=0)

# Kolommen samenvoegen (naast elkaar plakken):
df_wide = pd.concat([df1, df2], axis=1)

# Na concat: indices resetten (vermijd dubbele indices):
df_total = pd.concat([df1, df2]).reset_index(drop=True)

# ignore_index=True: meteen opnieuw nummeren:
df_total = pd.concat([df1, df2], ignore_index=True)
```

---

# DEEL 11 — DATETIME

---

## `pd.to_datetime(waarde, format=..., dayfirst=...)` — zet om naar datetime

```python
# Vanuit string:
df['date'] = pd.to_datetime(df['date'])

# Met formaat meegeven (als pandas het verkeerd parseert):
date = pd.to_datetime('01-05-2025', format='%d-%m-%Y')
# %d = dag, %m = maand, %Y = jaar 4 cijfers, %y = jaar 2 cijfers

# dayfirst=True: eerste getal = dag (Belgische notatie):
date = pd.to_datetime('01-05-2025', dayfirst=True)

# Vanuit aparte day/month/year kolommen:
df['date'] = pd.to_datetime(df[['day', 'month', 'year']])
```

### Formaat-codes

| Code | Betekenis          | Voorbeeld |
|------|--------------------|-----------|
| `%d` | Dag (01-31)        | 25        |
| `%m` | Maand (01-12)      | 05        |
| `%Y` | Jaar (4 cijfers)   | 2025      |
| `%y` | Jaar (2 cijfers)   | 25        |
| `%H` | Uur (00-23)        | 14        |
| `%M` | Minuten (00-59)    | 30        |
| `%S` | Seconden (00-59)   | 00        |

---

## Datetime-eigenschappen uitlezen via `.dt`

Na `pd.to_datetime()` kun je datumonderdelen uitlezen via `.dt`:

```python
df['date'] = pd.to_datetime(df['date'])

df['year']    = df['date'].dt.year
df['month']   = df['date'].dt.month
df['day']     = df['date'].dt.day
df['weekday'] = df['date'].dt.dayofweek   # 0=maandag, 6=zondag
df['weekday_name'] = df['date'].dt.day_name()  # 'Monday', 'Tuesday', ...
df['month_name']   = df['date'].dt.month_name()  # 'January', 'February', ...
df['hour']    = df['date'].dt.hour
df['quarter'] = df['date'].dt.quarter     # 1, 2, 3 of 4
```

---

## Datums van elkaar aftrekken → Timedelta

```python
date1 = pd.to_datetime('01-05-2025', dayfirst=True)
date2 = pd.to_datetime('10-05-2025', dayfirst=True)

verschil = date2 - date1

print(verschil)                    # → 9 days 00:00:00
print(verschil.days)               # → 9
print(verschil.components)        # → Components(days=9, hours=0, ...)
print(verschil.components.minutes) # → 0
```

---

# DEEL 12 — APPLY

---

## `df.apply(func, axis=...)` — pas een functie toe op elke rij of kolom

- `axis=0` of `axis='index'` → functie wordt toegepast **per kolom** (standaard)
- `axis=1` of `axis='columns'` → functie wordt toegepast **per rij**

### Functie op elke cel van het hele DataFrame (axis weglaten):

```python
def sqrt(x):
    return x ** (1/2)

df.apply(sqrt)   # past sqrt toe op elke cel
```

### Functie per rij (axis=1) — meest gebruikt voor nieuwe kolom berekenen:

```python
def label(row):
    if row['open'] > row['close']:
        return 'daling'
    elif row['open'] < row['close']:
        return 'stijging'
    else:
        return 'stabiel'

df['label'] = df.apply(label, axis=1)
```

### Functie per kolom (axis=0):

```python
df.apply(sum, axis=0)    # som van elke kolom
df.apply(max, axis=0)    # maximum van elke kolom
```

### Functie per rij met ingebouwde functie:

```python
df.apply(sum, axis=1)    # som van elke rij
df.apply(max, axis=1)    # maximum van elke rij
```

### Met lambda (voor simpele berekeningen):

```python
df['Salary_K'] = df['Salary'].apply(lambda x: x / 1000)   # op één kolom
df['Age_doubled'] = df['Age'].apply(lambda x: x * 2)
```

### Categorieën toekennen op basis van drempelwaarden:

```python
def categorize_lead(days):
    if days > 365:
        return 'early bird'
    elif days > 183:
        return 'planner'
    elif days > 90:
        return 'seasonal booker'
    elif days >= 14:
        return 'late booker'
    else:
        return 'last minute'

df['category'] = df['purchase_lead'].apply(categorize_lead)
```

---

# DEEL 13 — VISUALISATIE (MATPLOTLIB)

---

## Basisstructuur van elke plot

```python
plt.figure(figsize=(10, 6))   # maak figuur aan met breedte×hoogte in inches
# ... voeg plots toe ...
plt.title('Mijn Grafiek')     # titel
plt.xlabel('X-as label')      # label x-as
plt.ylabel('Y-as label')      # label y-as
plt.legend()                  # toon legenda
plt.grid(True)                # toon raster
plt.xticks(rotation=45)       # x-labels 45° draaien
plt.tight_layout()            # voorkomt overlapping van labels
plt.show()                    # toon de grafiek
```

---

## Lijngrafiek — `plt.plot(x, y, ...)`

```python
plt.plot(df['year'], df['Pigeons'])   # simpelste vorm

# Met stijl-opties:
plt.plot(
    df['year'], df['Pigeons'],
    label='Pigeons',          # naam in legenda
    color='blue',             # kleur: 'blue', 'red', '#FF5733', ...
    linestyle='-',            # lijnstijl: '-'=vol, '--'=streep, ':'=stip, '-.'=stip-streep
    linewidth=2,              # dikte van de lijn
    marker='o',               # punt op datapunt: 'o'=cirkel, 's'=vierkant, '^'=driehoek, '<'/>='=pijl
    markersize=8,             # grootte van de marker
    markeredgecolor='red',    # randkleur van de marker
    markeredgewidth=1,        # randdikte van de marker
)
```

### Overzicht markers

| Code | Vorm             |
|------|-----------------|
| `'o'`  | Cirkel          |
| `'s'`  | Vierkant        |
| `'^'`  | Driehoek omhoog |
| `'v'`  | Driehoek omlaag |
| `'<'`  | Driehoek links  |
| `'>'`  | Driehoek rechts |
| `'*'`  | Ster            |
| `'+'`  | Plus            |
| `'x'`  | Kruis           |
| `'D'`  | Diamant         |

### Overzicht lijnstijlen

| Code    | Stijl       |
|---------|-------------|
| `'-'`   | Volle lijn  |
| `'--'`  | Gestreept   |
| `':'`   | Gestippeld  |
| `'-.'`  | Stip-streep |

---

## Staafgrafiek — `plt.bar(x, height, ...)`

```python
plt.bar(
    x,                  # x-posities (lijst, range, of labels)
    height,             # hoogtes van de balken
    width=0.35,         # breedte van de balk (standaard 0.8)
    color='blue',       # kleur
    label='Pigeons',    # naam in legenda
    edgecolor='black',  # randkleur
)
```

### Gegroepeerde staafgrafiek (meerdere groepen naast elkaar):

```python
import numpy as np

categories = ['A', 'B', 'C', 'D']
values1 = [10, 20, 15, 25]
values2 = [12, 18, 20, 22]

x = np.arange(len(categories))   # [0, 1, 2, 3]
width = 0.35                      # breedte van één balk

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, values1, width, label='Groep 1')   # links van het midden
ax.bar(x + width/2, values2, width, label='Groep 2')   # rechts van het midden

ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=45)
ax.set_xlabel('Categorie')
ax.set_ylabel('Waarde')
ax.set_title('Gegroepeerde staafgrafiek')
ax.legend()
plt.tight_layout()
plt.show()
```

### Voor 5 groepen (landen) naast elkaar:

```python
n_countries = 5
n_categories = len(pl_categories)
x = np.arange(n_categories)
width = 0.15   # kleiner zodat alle 5 balken naast elkaar passen

for i, country in enumerate(countries):
    # offset: -2*width, -1*width, 0, +1*width, +2*width
    offset = (i - n_countries/2 + 0.5) * width
    counts = [counts_per_country.get((country, cat), 0) for cat in pl_categories]
    ax.bar(x + offset, counts, width, label=country)
```

### Gestapelde staafgrafiek:

```python
plt.bar(x, values1, label='Groep 1')
plt.bar(x, values2, bottom=values1, label='Groep 2')   # bottom = bovenkant vorige balk
```

---

## Histogram — `plt.hist(data, bins=...)`

```python
plt.hist(df['Age'], bins=10)                  # 10 gelijke intervallen
plt.hist(df['Age'], bins=[20, 30, 40, 50])    # eigen grenzen
plt.hist(df['Age'], bins=10, edgecolor='black')  # rand om elke staaf
plt.hist(df['Age'], density=True)             # toon relatieve frequentie (%)
```

---

## Subplots — meerdere grafieken naast/onder elkaar

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))   # 1 rij, 2 kolommen

axes[0].plot(x, y1)
axes[0].set_title('Grafiek 1')

axes[1].bar(x, y2)
axes[1].set_title('Grafiek 2')

plt.tight_layout()
plt.show()
```

---

## Handige plt-functies

```python
plt.xlim(0, 100)             # grenzen van de x-as
plt.ylim(0, 500)             # grenzen van de y-as
plt.axhline(y=50, color='r', linestyle='--')   # horizontale lijn
plt.axvline(x=10, color='g', linestyle=':')    # verticale lijn
plt.text(x, y, 'label')      # tekst op positie (x, y)
plt.savefig('grafiek.png')   # sla op als bestand
```

---

# DEEL 14 — TYPISCHE EXAMENSTAPPEN

---

## Stap-voor-stap: CSV laden en eerste analyse

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Laden
df = pd.read_csv('customer_booking.csv')

# 2. Eerste inspectie
print(df.head())         # eerste 5 rijen
print(df.info())         # kolomtypes en non-null counts
print(df.describe())     # statistieken
print(df.shape)          # (rijen, kolommen)

# 3. NaN verwijderen
df = df.dropna()

# 4. Nieuwe kolom toevoegen
df['duration_cat'] = df['flight_duration'].apply(
    lambda h: 'Short' if h <= 3 else ('Long' if h > 6 else 'Medium')
)

# 5. Groeperen
avg_per_country = df.groupby('booking_origin')['purchase_lead'].mean().sort_values()
print(avg_per_country)

# 6. Één waarde opvragen
print(avg_per_country.loc['Australia'])

# 7. Top 5 meest voorkomende waarden
top5 = df['booking_origin'].value_counts().head(5)
countries = top5.index.tolist()
print(countries)
```

---

## Stap-voor-stap: Gefilterde DataFrame maken

```python
# Selecteer specifieke kolommen EN filter rijen:
cols = ['num_passengers', 'purchase_lead', 'booking_origin', 'booking_complete']
completed = df[cols][df['booking_complete'] == 1]

# OF (equivalent):
completed = df[df['booking_complete'] == 1][cols]

# OF (nettere aanpak via loc):
completed = df.loc[df['booking_complete'] == 1, cols]
```

---

## Stap-voor-stap: Premium klanten berekenen

```python
# Premium = wil extra bagage ÉN voorkeursstoel ÉN maaltijd
df['premium_customer'] = (
    (df['wants_extra_baggage'] == 1) &
    (df['wants_preferred_seat'] == 1) &
    (df['wants_in_flight_meals'] == 1)
)
# Omzetten naar 0/1:
df['premium_customer'] = df['premium_customer'].astype(int)
```

---

## Stap-voor-stap: Percentage berekenen

```python
# % afgeronde boekingen:
pct_complete = df['booking_complete'].mean() * 100
print(f"{pct_complete:.1f}%")

# % per sales channel:
pct_per_channel = df.groupby('sales_channel')['booking_complete'].mean() * 100
print(pct_per_channel)

# % premium klanten onder lange vluchten die geboekt zijn:
long_completed = df[(df['duration_cat'] == 'Long') & (df['booking_complete'] == 1)]
pct_premium = long_completed['premium_customer'].mean() * 100
print(f"{pct_premium:.1f}%")
```

---

## Stap-voor-stap: Top 5 routes

```python
# Op basis van totaal aantal passagiers:
top5_routes = df.groupby('route')['num_passengers'].sum().sort_values(ascending=False).head(5)
print(top5_routes)

# Op basis van aantal boekingen:
top5_routes = df['route'].value_counts().head(5)
```

---

# SNELLE REFERENTIE — Wat doet wat?

| Functie/Methode | Wat het doet | Returnt |
|---|---|---|
| `pd.read_csv(f)` | CSV inladen | DataFrame |
| `df.to_csv(f)` | Naar CSV schrijven | — |
| `pd.DataFrame(d)` | Dict/lijst → DataFrame | DataFrame |
| `df.head(n)` | Eerste n rijen | DataFrame |
| `df.tail(n)` | Laatste n rijen | DataFrame |
| `df.info()` | Kolommen + types + non-null | print |
| `df.describe()` | Statistieken numerieke kolommen | DataFrame |
| `df.shape` | (rijen, kolommen) | tuple |
| `df.dtypes` | Type per kolom | Series |
| `df.columns` | Kolomnamen | Index |
| `df.rename(columns={})` | Kolommen hernoemen | DataFrame* |
| `df.set_index('col')` | Kolom als index | DataFrame* |
| `df.reset_index(drop=T)` | Index resetten naar 0,1,2,... | DataFrame* |
| `df['col']` | Kolom selecteren | Series |
| `df[['c1','c2']]` | Meerdere kolommen | DataFrame |
| `df.loc[r, c]` | Selectie op label | Series/DataFrame |
| `df.iloc[r, c]` | Selectie op positie | Series/DataFrame |
| `df.at[r, c]` | Één cel op label | waarde |
| `df.iat[r, c]` | Één cel op positie | waarde |
| `df[df['x']>5]` | Boolean filter | DataFrame |
| `df.sort_values(by='col')` | Sorteren op kolom | DataFrame* |
| `df.sort_index()` | Sorteren op index | DataFrame* |
| `df.drop(columns=['x'])` | Kolom verwijderen | DataFrame* |
| `df.dropna()` | Rijen met NaN verwijderen | DataFrame* |
| `df.fillna(0)` | NaN vervangen | DataFrame* |
| `df.isna().sum()` | Aantal NaN per kolom | Series |
| `df['x'].sum()` | Som van kolom | getal |
| `df['x'].mean()` | Gemiddelde | getal |
| `df['x'].min/max()` | Min/max | getal |
| `df['x'].count()` | Aantal non-null | getal |
| `df['x'].nunique()` | Aantal unieke waarden | getal |
| `df['x'].value_counts()` | Frequentie per waarde | Series |
| `df.agg([...])` | Meerdere statistieken | DataFrame |
| `df.groupby('x')` | Groepeer op kolom | GroupBy |
| `pd.concat([d1,d2])` | DataFrames samenvoegen | DataFrame |
| `pd.to_datetime(x)` | Naar datetime | datetime |
| `df['d'].dt.year` | Jaar uit datetime | Series |
| `df.apply(func, axis=1)` | Functie per rij | Series/DataFrame |
| `df.apply(func, axis=0)` | Functie per kolom | Series/DataFrame |

> \* = returnt nieuwe DataFrame, origineel ongewijzigd tenzij `inplace=True` of `df = df.methode()`

---

## ⚠️ De 5 grootste valkuilen

```python
# 1. sort() returnt None — gebruik sorted() of sort_values()
new = lijst.sort()            # new = None !
new = sorted(lijst)           # correct

# 2. Pandas-methoden passen origineel NIET aan
df.dropna()                   # geen effect op df
df.sort_values(by='Age')      # geen effect op df
df = df.dropna()              # correct
df.dropna(inplace=True)       # ook correct

# 3. loc is INCLUSIEF, iloc is EXCLUSIEF aan het einde
df.loc['p1':'p3']    # → p1, p2, p3 (p3 zit erin!)
df.iloc[0:3]         # → rij 0, 1, 2 (rij 3 zit er NIET in!)

# 4. Boolean filtering: gebruik & en |, NIET 'and' en 'or', ALTIJD haakjes
df[df['Age'] > 25 and df['Age'] < 40]          # FOUT — werkt niet
df[(df['Age'] > 25) & (df['Age'] < 40)]        # correct

# 5. groupby geeft een GroupBy-object, niet meteen een DataFrame
result = df.groupby('City')                    # GroupBy-object
result = df.groupby('City')['Salary'].mean()   # correct: Series
result = df.groupby('City').mean()             # correct: DataFrame
```
