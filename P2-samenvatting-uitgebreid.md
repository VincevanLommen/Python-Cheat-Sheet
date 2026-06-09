# Samenvatting P2 — Volledige Studiegids 2025-2026

> Deze samenvatting legt **alles stap voor stap uit**, met codevoorbeelden en uitleg zodat je de stof ook echt begrijpt zonder het cursusmateriaal bij de hand te hebben.

---

## DEEL 1 — Object-Oriented Programming (OOP)

---

### 1.1 Classes (herhaling)

Een **klasse** is een blauwdruk voor objecten. Ze bundelt data (**attributen**) en gedrag (**methoden**) op één plek.

```python
class BankAccount:
    def __init__(self, owner):   # constructor: wordt uitgevoerd bij aanmaken
        self.owner = owner       # publiek attribuut
        self.__balance = 0       # privaat attribuut (__ = niet van buiten aanpasbaar)
        self.__transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Bedrag moet positief zijn.")
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

**Hoe gebruik je dit?**

```python
account = BankAccount("Vince")   # aanmaken van een object
account.deposit(100)             # methode aanroepen
print(account.get_balance())     # → 100
print(account.owner)             # → "Vince"
```

**Wat doet `self`?**  
`self` verwijst naar het object zelf. Elke methode krijgt `self` als eerste parameter mee — zo weet Python op welk object de methode wordt aangeroepen. Je hoeft `self` niet mee te geven bij het aanroepen, Python doet dat automatisch.

**Wat zijn `__` (double underscore) attributen?**  
Attributen die beginnen met `__` zijn **privaat**. Python maakt ze moeilijk bereikbaar van buiten de klasse. Dit is een beschermingsmechanisme zodat niemand zomaar de interne toestand van een object kapot kan maken.

```python
account.__balance = -999   # Dit lukt niet (geeft een fout of werkt niet zoals verwacht)
```

---

### 1.2 Encapsulation

**Encapsulation** = het verbergen van hoe iets intern werkt, achter een nette publieke interface. Vergelijk het met een televisie: je hoeft niet te weten hoe de electronica werkt, je gebruikt gewoon de afstandsbediening (de publieke interface).

In Python doe je dit via `__` (private). Dit is een **conventie** — Python kan het niet helemaal afdwingen, maar andere programmeurs begrijpen dat ze er niet aan mogen.

```python
class Wall:
    def __init__(self, height):
        self.__height = height   # privaat, niet rechtstreeks aanpasbaar

    def get_height(self):        # publieke methode om toch de waarde op te vragen
        return self.__height
```

```python
wall = Wall(3)
print(wall.get_height())   # → 3
wall.__height = 10          # doet NIETS nuttigs, Python maakt een nieuw attribuut aan
print(wall.get_height())   # → 3 (onveranderd)
```

---

### 1.3 Properties

**Het probleem zonder properties:** als je een publiek attribuut hebt en later wil valideren, moet je overal in je code de syntax aanpassen (van `person.age` naar `person.get_age()`). Dat is vervelend.

**De oplossing: `@property`** laat je een methode schrijven die zich gedraagt als een attribuut.

#### Stap 1: Readonly property (alleen lezen, niet schrijven)

```python
class Person:
    def __init__(self, age):
        self.__age = age   # sla op als privaat

    @property
    def age(self):         # getter: wordt aangeroepen bij person.age
        return self.__age
```

```python
person = Person(18)
print(person.age)    # → 18  (roept de getter aan)
person.age = 20      # → AttributeError! Geen setter gedefinieerd
```

#### Stap 2: Computed property (berekend attribuut)

Soms hoef je een waarde niet op te slaan — je berekent ze gewoon elke keer opnieuw. Zo vermijd je redundantie (twee keer dezelfde info opslaan leidt tot inconsistenties).

```python
class Person:
    def __init__(self, birthday):
        self.__birthday = birthday

    @property
    def age(self):
        today = date.today()
        difference = today - self.__birthday
        return difference.days // 365   # berekend, niet opgeslagen
```

Als je `age` én `birthday` zou opslaan, kan je eindigen met een persoon van 18 jaar die geboren is in 1980 — dat klopt niet. Door `age` te berekenen vanuit `birthday` is dit onmogelijk.

#### Stap 3: Setter met validatie

```python
class Person:
    def __init__(self, age):
        self.age = age   # Let op: roept de setter aan (niet self.__age)!

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):       # wordt aangeroepen bij person.age = iets
        if value < 0:
            raise ValueError('Leeftijd moet positief zijn')
        self.__age = value
```

```python
person = Person(25)
print(person.age)     # → 25
person.age = 30       # OK
person.age = -5       # → ValueError!
person = Person(-1)   # → ValueError! (constructor roept setter aan)
```

**Belangrijk patroon:** in de constructor gebruik je `self.age = age` (roept de setter aan) in plaats van `self.__age = age` (gaat er rechtstreeks in). Zo staat de validatielogica maar op één plek.

---

### 1.4 Static Methods

Normaal roep je een methode aan op een **object**: `person.greet()`. Maar soms heeft een methode het object niet nodig — ze hoort logisch bij de klasse, maar heeft geen `self` nodig.

```python
class Distance:
    def __init__(self, *, size_in_meters):   # * = keyword-only argument
        self.size_in_meters = size_in_meters

    @staticmethod
    def from_meters(amount):
        return Distance(size_in_meters=amount)

    @staticmethod
    def from_miles(amount):
        return Distance(size_in_meters=amount * 1609.34)

    @staticmethod
    def from_millimeters(amount):
        return Distance(size_in_meters=amount / 1000)
```

```python
# Je roept ze aan op de KLASSE, niet op een object:
d1 = Distance.from_miles(5)
d2 = Distance.from_meters(100)
print(d1.size_in_meters)   # → 8046.7
```

Dit zijn zogenaamde **factory functions**: methoden wiens enige job het is om objecten te maken. Door ze in de klasse te zetten maak je duidelijk dat ze bij `Distance` horen.

---

### 1.5 Operator Overloading

Standaard werkt `+` voor getallen en strings, maar niet voor je eigen klassen:

```python
p1 = Point(1, 2)
p2 = Point(3, 4)
p1 + p2   # → TypeError!
```

Via **dunder methods** (double underscore methoden) vertel je Python wat `+`, `-`, `*`, enz. moeten doen voor jouw klasse.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):          # wordt aangeroepen bij p1 + p2
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):          # wordt aangeroepen bij p1 - p2
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):                # wordt aangeroepen bij print(p)
        return f"Point({self.x}, {self.y})"
```

```python
p1 = Point(1, 2)
p2 = Point(3, 4)
print(p1 + p2)   # → Point(4, 6)
print(p1 - p2)   # → Point(-2, -2)
```

**Overzicht van veelgebruikte dunder methoden:**

| Operator | Dunder methode  | Voorbeeld        |
|----------|-----------------|------------------|
| `+`      | `__add__`       | `a + b`          |
| `-`      | `__sub__`       | `a - b`          |
| `*`      | `__mul__`       | `a * b`          |
| `/`      | `__truediv__`   | `a / b`          |
| `//`     | `__floordiv__`  | `a // b`         |
| `%`      | `__mod__`       | `a % b`          |
| `**`     | `__pow__`       | `a ** b`         |
| `==`     | `__eq__`        | `a == b`         |
| `<`      | `__lt__`        | `a < b`          |
| `len()`  | `__len__`       | `len(a)`         |
| `str()`  | `__repr__`      | `print(a)`       |

**Opgelet:** een dunder methode moet altijd een **nieuw object** returnen en `self` nooit aanpassen!

```python
# FOUT: past self aan
def __add__(self, other):
    self.x += other.x   # NOOIT DOEN

# JUIST: maakt nieuw object
def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
```

---

### 1.6 Inheritance (Overerving)

**Overerving** laat een klasse (de *child*) alle attributen en methoden van een andere klasse (de *parent*) overnemen. Dit vermijdt herhaling van code (DRY = Don't Repeat Yourself).

**Stelregel:** gebruik overerving alleen als "elke child-instantie ook een parent-instantie is". Elke `Cow` is een `Animal`, maar niet elk `Animal` is een `Cow`.

```python
class Animal:
    def __init__(self, name, num_legs):
        self.name = name
        self.num_legs = num_legs

    def describe(self):
        return f"{self.name} heeft {self.num_legs} poten"

class Cow(Animal):        # Cow erft van Animal
    def __init__(self, name):
        super().__init__(name, 4)   # roep constructor van Animal aan

    def moo(self):
        return "Mooo!"

class Spider(Animal):
    def __init__(self, name):
        super().__init__(name, 8)
```

```python
cow = Cow("Bessie")
print(cow.describe())   # → "Bessie heeft 4 poten" (geërfd van Animal)
print(cow.moo())        # → "Mooo!" (eigen methode van Cow)

spider = Spider("Charlotte")
print(spider.describe())   # → "Charlotte heeft 8 poten"
```

**Overervingshiërarchie** kan meerdere niveaus diep gaan:  
`LivingThing` → `Animal` → `Mammal` → `Cat`  
Maar houd het beperkt: te diepe hiërarchieën worden snel verwarrend.

---

### 1.7 Abstract Classes

Een **abstracte klasse** is een klasse die je *niet rechtstreeks* kunt instantiëren — ze bestaat alleen als blauwdruk voor child classes.

**Waarom?** Soms heeft een parent klasse methoden die afhankelijk zijn van een implementatie die nog niet bestaat. Je wilt kinderen *verplichten* die methode te implementeren.

```python
from abc import ABC, abstractmethod

class ChessPiece(ABC):      # ABC = Abstract Base Class
    def __init__(self, position):
        self.__position = position

    def move(self, new_position):
        if not self.is_legal_move(new_position):   # roept abstracte methode aan
            raise ValueError('Ongeldige zet')
        self.__position = new_position

    @abstractmethod
    def is_legal_move(self, new_position):   # MOET geïmplementeerd worden door child
        ...   # de drie puntjes zijn letterlijk de code hier
```

```python
class Pawn(ChessPiece):
    def is_legal_move(self, new_position):
        # Pion-specifieke regels...
        return True

class King(ChessPiece):
    def is_legal_move(self, new_position):
        # Koning-specifieke regels...
        return True
```

```python
piece = ChessPiece(...)   # → TypeError! Kan abstract niet instantiëren
pawn = Pawn(...)          # → OK
```

**Abstract properties** werken hetzelfde:

```python
class Shape(ABC):
    @property
    @abstractmethod
    def area(self):
        ...
```

---

### 1.8 Overriding

Een child klasse kan een methode van de parent **overschrijven** door een methode met dezelfde naam te definiëren. De versie van de child "wint".

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):        # overschrijft Animal.speak
        return "Woof!"

class Cat(Animal):
    def speak(self):        # overschrijft Animal.speak
        return "Meow!"
```

```python
animal = Animal()
print(animal.speak())   # → "..."

dog = Dog()
print(dog.speak())      # → "Woof!"

cat = Cat()
print(cat.speak())      # → "Meow!"
```

---

### 1.9 Super

`super()` geeft je toegang tot de **oorspronkelijke versie** van een methode uit de parent klasse. Handig wanneer je de parent-logica wil hergebruiken en uitbreiden in plaats van alles opnieuw te schrijven.

```python
class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class AgeRestrictedItem(Item):
    def __init__(self, name, price, minimum_age):
        super().__init__(name, price)   # delegeer naam en prijs aan Item
        self.minimum_age = minimum_age  # voeg eigen attribuut toe

    def can_be_sold_to(self, customer):
        return customer.age >= self.minimum_age
```

```python
item = AgeRestrictedItem("Alcohol", 3.50, 18)
print(item.name)           # → "Alcohol" (van Item)
print(item.minimum_age)    # → 18 (eigen)
```

**Zonder `super()`** zou je `name` en `price` opnieuw moeten initialiseren — herhaling van code die al in `Item` staat.

---

## DEEL 2 — Functioneel Programmeren

---

### 2.1 Higher-Order Functions

In Python zijn functies "first-class citizens": je kunt ze aan variabelen toewijzen en als argument meegeven aan andere functies. Een functie die een andere functie als parameter ontvangt, heet een **higher-order function**.

**Waarom nuttig?** Stel je hebt een performantietest voor `bubble_sort`. Als je later ook `merge_sort` wil testen, moet je bijna identieke code herhalen. Door de te testen functie als argument mee te geven, schrijf je het maar één keer:

```python
def test_sort(sorting_function):
    import time, random
    for size in [1000, 10000]:
        random_list = random.choices(range(1000), k=size)
        start = time.time()
        sorting_function(random_list)
        end = time.time()
        print(f"Grootte {size}: {end - start:.4f} seconden")
```

```python
test_sort(bubble_sort)   # test bubble sort
test_sort(sorted)        # test ingebouwde Python sort
```

Functies als argument meegeven: let op het verschil!

```python
test_sort(bubble_sort)    # JUIST: geef de functie mee (geen haakjes)
test_sort(bubble_sort())  # FOUT: roept bubble_sort aan en geeft het resultaat mee
```

---

### 2.2 Nested Functions

Een **nested function** is een functie die gedefinieerd wordt *binnen* een andere functie. Ze heeft toegang tot de variabelen van de omringende functie.

**Wanneer heb je dit nodig?** Als je een helperfunctie nodig hebt die toegang moet hebben tot een lokale variabele van de buitenste functie, maar je wil die variabele niet als parameter toevoegen (want de helperfunctie wordt gebruikt als callback met een vaste signatuur).

```python
def count(collection, condition):
    return sum(1 for element in collection if condition(element))

def count_movies_by_director(movies, director):
    def is_by_director(movie):          # nested function
        return movie.director == director   # heeft toegang tot 'director'
    return count(movies, is_by_director)
```

```python
count_movies_by_director(movies, "Spielberg")   # → bijv. 5
count_movies_by_director(movies, "Nolan")       # → bijv. 3
```

Elke keer dat `count_movies_by_director` aangeroepen wordt, wordt `is_by_director` opnieuw gedefinieerd met de nieuwe waarde van `director`.

---

### 2.3 Lambdas

Een **lambda** is een anonieme, éénregelige functie. Je gebruikt ze wanneer je een eenvoudige functie maar één keer nodig hebt.

```python
# Gewone functie:
def is_even(number):
    return number % 2 == 0

# Hetzelfde als lambda:
is_even = lambda number: number % 2 == 0
```

**Syntax:**
```
lambda argument1, argument2: expressie_die_gereturnd_wordt
```

Meer voorbeelden:

```python
# Geen argumenten:
return_5 = lambda: 5
print(return_5())   # → 5

# Twee argumenten:
add = lambda a, b: a + b
print(add(3, 4))    # → 7

# Rechtstreeks als argument meegeven (anoniem):
result = count([1, 2, 3, 4, 5], lambda n: n % 2 == 0)
print(result)   # → 2  (er zijn 2 even getallen)
```

**Beperking:** een lambda kan maar één expressie bevatten. Voor complexere logica gebruik je een gewone `def`-functie.

**Expressie vs statement** — een expressie heeft een waarde (je kunt ze in een `print()` steken), een statement niet:
- Expressie: `3 + 4`, `"hello".upper()`, `[x for x in lijst]`
- Statement: `if ...`, `def ...`, `for ...`

Lambdas zijn expressies → je kunt ze rechtstreeks als argument meegeven.

---

### 2.4 Comprehensions

Comprehensions zijn een beknopte, Pythonische manier om lijsten, sets of dictionaries te bouwen.

#### List comprehension — Mapping (transformeren)

```python
# Traditioneel:
squares = []
for n in range(5):
    squares.append(n ** 2)

# Met list comprehension:
squares = [n ** 2 for n in range(5)]
# → [0, 1, 4, 9, 16]
```

**Algemene vorm:** `[expressie for element in iterable]`

#### List comprehension — Filtering (filteren)

```python
# Traditioneel:
adults = []
for person in people:
    if person.age >= 18:
        adults.append(person)

# Met list comprehension:
adults = [person for person in people if person.age >= 18]
```

**Algemene vorm:** `[expressie for element in iterable if voorwaarde]`

#### Combineren van mapping én filtering

```python
# Namen van alle volwassenen:
adult_names = [person.name for person in people if person.age >= 18]
```

#### Set comprehension

Gebruik accolades `{}` in plaats van rechte haakjes `[]`. Duplicaten verdwijnen automatisch, volgorde is niet gegarandeerd.

```python
squares = {n ** 2 for n in range(-5, 6)}
# → {0, 1, 4, 9, 16, 25}  (geen duplicaten zoals twee keer 1, 4, enz.)
```

#### Dictionary comprehension

```python
# Studenten snel opzoekbaar maken via hun id:
students_by_id = {student.id: student for student in students}

# Woordlengte per woord:
word_lengths = {word: len(word) for word in ["hallo", "wereld", "python"]}
# → {"hallo": 5, "wereld": 6, "python": 6}
```

#### Handige ingebouwde functies die goed combineren met comprehensions

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

len(numbers)          # → 8       (aantal elementen)
min(numbers)          # → 1       (kleinste)
max(numbers)          # → 9       (grootste)
sum(numbers)          # → 31      (som)
all(n > 0 for n in numbers)   # → True  (zijn ALLE elementen positief?)
any(n > 8 for n in numbers)   # → True  (is er MINSTENS ÉÉN groter dan 8?)

# zip: koppel twee lijsten element per element
xs = ['a', 'b', 'c']
ys = [1, 2, 3]
list(zip(xs, ys))    # → [('a', 1), ('b', 2), ('c', 3)]

# enumerate: voeg index toe
list(enumerate(['a', 'b', 'c']))   # → [(0, 'a'), (1, 'b'), (2, 'c')]
```

---

### 2.5 Iterables en Generators

**Iterable:** elk object waarover je kunt itereren met een `for`-lus. Lijsten, tuples, strings, sets, dictionaries zijn allemaal iterables.

**Generator:** een speciale functie die waarden één voor één produceert met `yield`. Ze berekent waarden *on-the-fly* zonder alles tegelijk in geheugen te laden.

```python
def integers(n):
    current = 0
    while current < n:
        yield current      # geeft waarde terug, maar pauzeert (niet gestopt!)
        current += 1

for i in integers(5):
    print(i)
# → 0, 1, 2, 3, 4
```

**Hoe werkt `yield`?** Anders dan `return`:
- `return`: functie stopt volledig
- `yield`: functie *pauzeert* en geeft waarde terug. Bij de volgende iteratiestap gaat ze verder waar ze gestopt was.

```python
def languages():
    print("Geef Python")
    yield "Python"
    print("Geef Java")
    yield "Java"
    print("Geef Haskell")
    yield "Haskell"

for lang in languages():
    print(lang)

# Output:
# Geef Python
# Python
# Geef Java
# Java
# Geef Haskell
# Haskell
```

Als je de loop vroeg stopt, wordt de rest van de generator nooit uitgevoerd:

```python
for lang in languages():
    print(lang)
    break   # stop na de eerste

# Output: alleen "Geef Python" en "Python"
```

**Waarom generators?** Ze zijn veel zuiniger met geheugen:
```python
# Lijst: slaat alle 10 000 getallen op in geheugen (80 KB)
list(range(10000))

# Generator: gebruikt slechts 112 bytes
integers(10000)
```

**Verschil generator vs iterable:** een generator kun je maar één keer doorlopen. Erna is hij "op". Een lijst kun je meerdere keren doorlopen.

```python
g = integers(3)
list(g)   # → [0, 1, 2]
list(g)   # → []  (generator is al leeg!)

# Oplossing: roep de generator opnieuw aan
list(integers(3))   # → [0, 1, 2]
list(integers(3))   # → [0, 1, 2]
```

**Oneindige generators** (handig met `next()`):

```python
def counting():
    n = 0
    while True:        # gaat voor altijd door
        yield n
        n += 1

gen = counting()
next(gen)   # → 0
next(gen)   # → 1
next(gen)   # → 2
```

**Generator comprehension:** gebruik ronde haakjes in plaats van rechte:
```python
squares_gen = (n**2 for n in range(10))   # generator, niet lijst
```

---

### 2.6 Itertools

De `itertools` module biedt handige functies voor het werken met iterables:

```python
from itertools import pairwise, combinations, permutations, chain

# pairwise: koppel aangrenzende elementen
list(pairwise([1, 2, 3, 4]))
# → [(1, 2), (2, 3), (3, 4)]

# combinations: alle combinaties van k elementen
list(combinations([1, 2, 3], 2))
# → [(1, 2), (1, 3), (2, 3)]

# permutations: alle volgorden
list(permutations([1, 2, 3]))
# → [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

# chain: plak iterables aan elkaar
list(chain([1, 2], [3, 4], [5]))
# → [1, 2, 3, 4, 5]
```

---

### 2.7 Recursie

Een **recursieve functie** roept zichzelf aan. Elke recursieve functie heeft twee onderdelen:
1. **Base case:** het geval dat direct opgelost kan worden (stop-conditie)
2. **Recursive case:** het geval waarbij de functie zichzelf aanroept met een kleiner probleem

```python
def factorial(n):
    if n == 1:              # base case: 1! = 1
        return 1
    return n * factorial(n - 1)   # recursive case: n! = n × (n-1)!
```

```python
factorial(5)
# = 5 * factorial(4)
# = 5 * 4 * factorial(3)
# = 5 * 4 * 3 * factorial(2)
# = 5 * 4 * 3 * 2 * factorial(1)
# = 5 * 4 * 3 * 2 * 1
# = 120
```

Elke aanroep voegt een **stack frame** toe aan de call stack. Als je de base case vergeet, krijg je een oneindige recursie en een `RecursionError`.

---

## DEEL 3 — Testen

---

### 3.1 Wat zijn goede tests?

Tests controleren automatisch of je code correct werkt. Goede tests zijn:

- **Geautomatiseerd:** geen manuele controle — de machine checkt
- **Fijnmazig:** één test, één mogelijke reden voor falen
- **Leesbaar:** duidelijk wat getest wordt
- **Snel:** tests worden heel vaak uitgevoerd
- **Geïsoleerd:** tests beïnvloeden elkaar niet

**Slechte aanpak (doe dit nooit):**
```python
print(some_function(5))   # manueel kijken of output klopt → weggooien na check
```

**Goede aanpak:**
```python
assert some_function(5) == 100   # machine checkt, code blijft staan
```

### Pytest

Pytest is het testframework dat in de cursus gebruikt wordt. Je schrijft testfuncties die beginnen met `test_`. Pytest voert ze allemaal uit en meldt welke slagen/falen.

```python
# tests.py
from intervals import overlapping_intervals

def test_overlapping():
    assert overlapping_intervals((1, 5), (3, 6))     # verwacht True

def test_not_overlapping():
    assert not overlapping_intervals((1, 3), (5, 8))  # verwacht False
```

```bash
$ pytest          # voer alle tests uit
$ pytest -x       # stop bij eerste fout
$ pytest -v       # uitgebreidere output
```

Gebruik altijd `assert` en niet manueel `raise AssertionError()` — Pytest herschrijft je `assert`s om betere foutmeldingen te geven:

```
FAILED tests.py::test_1
E   assert [1, 2, 4] == [1, 2, 3]
E     At index 2 diff: 4 != 3    ← Pytest toont exact het verschil
```

---

### 3.2 Geparametriseerde Tests

Als je meerdere inputs wil testen voor dezelfde functie, gebruik je `@pytest.mark.parametrize` in plaats van alles te copy-pasten.

**Zonder parametrize (slecht):**
```python
def test_1():
    assert overlapping_intervals((1, 5), (3, 6))
def test_2():
    assert overlapping_intervals((1, 5), (5, 6))
def test_3():
    assert overlapping_intervals((1, 10), (3, 6))
# ... enorm veel herhaling
```

**Met parametrize (goed):**
```python
import pytest

@pytest.mark.parametrize('interval1, interval2', [
    ((1, 5), (3, 6)),    # test 1: verwacht True
    ((1, 5), (5, 6)),    # test 2: verwacht True
    ((1, 10), (3, 6)),   # test 3: verwacht True
])
def test_overlapping(interval1, interval2):
    assert overlapping_intervals(interval1, interval2)

@pytest.mark.parametrize('interval1, interval2', [
    ((1, 2), (3, 4)),    # test 4: verwacht False
    ((8, 9), (6, 7)),    # test 5: verwacht False
])
def test_not_overlapping(interval1, interval2):
    assert not overlapping_intervals(interval1, interval2)
```

Pytest genereert automatisch aparte tests voor elke combinatie van inputs. Zo zie je bij een fout exact welke input het probleem veroorzaakte.

**Meerdere `@parametrize` decorators** → Pytest combineert alle mogelijkheden (cartesisch product):

```python
@pytest.mark.parametrize('left', [[], [1], [1, 2]])
@pytest.mark.parametrize('right', [[], [5], [5, 6]])
def test_merge(left, right):
    # wordt 3 × 3 = 9 keer aangeroepen
    ...
```

---

### 3.3 Floating Point en `approx`

Computers werken in binair. Getallen zoals `0.1` kunnen niet exact in binair worden voorgesteld, waardoor er afrondingsfouten optreden:

```python
>>> sum([0.1] * 10)
0.9999999999999999        # niet exact 1.0!

>>> sum([0.1] * 10) == 1
False
```

Bij tests met kommagetallen gebruik je daarom `pytest.approx`:

```python
from pytest import approx

# Zonder approx: kan falen door afrondingsfout
assert average([0.1, 0.1, 0.1]) == 0.1   # kan falen!

# Met approx: tolereert kleine afwijkingen
assert average([0.1, 0.1, 0.1]) == approx(0.1)          # standaard tolerantie
assert average([0.1, 0.1, 0.1]) == approx(0.1, abs=0.01) # eigen tolerantie
```

---

### 3.4 Exceptions Testen

Als een functie bij foute input een fout moet gooien, test je dat met `pytest.raises`:

```python
import pytest
from book import Book

def test_lege_titel_geeft_fout():
    with pytest.raises(RuntimeError):
        Book('', '978-1779501127')   # lege titel → verwacht RuntimeError

def test_ongeldige_isbn_geeft_fout():
    with pytest.raises(RuntimeError):
        Book('Watchmen', '000-0000000000')   # ongeldig ISBN → verwacht RuntimeError

def test_geldig_boek():
    book = Book('Watchmen', '978-1779501127')   # geen fout verwacht
    assert book.title == 'Watchmen'
```

Houd de code *binnen* het `with`-blok zo kort mogelijk — hoe meer code, hoe meer mogelijke bronnen van fouten, en dan weet je niet meer welke lijn de fout veroorzaakte.

---

### 3.5 Slimme Testverwachtingen (Expected Values)

Soms is het moeilijk om verwachte waarden te berekenen. Je kunt de relatie tussen input en output gebruiken om tests te genereren:

**Voorbeeld: `sqrt` testen zonder de waarde hard te coderen**

```python
# In plaats van: sqrt(49) == 7
# Gebruik: sqrt(x*x) == x

@pytest.mark.parametrize('n, expected', [
    (x * x, x) for x in range(1, 100)   # genereer 99 testcases automatisch!
])
def test_sqrt(n, expected):
    assert approx(expected) == sqrt(n)
```

Of gebruik de inverse relatie (als je een resultaat makkelijk kunt verifiëren maar moeilijk kunt berekenen):

```python
@pytest.mark.parametrize('n', range(1, 100))
def test_sqrt_inverse(n):
    result = sqrt(n)
    assert approx(result * result) == n   # controleer dat sqrt(n)² ≈ n
```

**Nooit randomness in tests!** Tests moeten reproduceerbaar zijn:
```python
# FOUT: random zorgt dat je fout misschien verdwijnt bij de volgende run
import random
n = random.randint(1, 100)

# JUIST: deterministische waarden
for n in range(1, 100):
    ...
```

---

### 3.6 Reference Implementation

Soms is de verwachte output makkelijk te berekenen met een eenvoudig (maar traag) algoritme. Je vergelijkt dan het snelle met het trage algoritme:

```python
# Twee implementaties van hetzelfde:
# - simple_sort: makkelijk te begrijpen, traag
# - merge_sort: complex maar snel

@pytest.mark.parametrize('ns', [
    [], [1], [3, 1, 2], [5, 4, 3, 2, 1], list(range(100))
])
def test_merge_sort(ns):
    expected = sorted(ns)     # simpel maar traag → dit is de referentie
    actual = merge_sort(ns)   # complex maar snel → dit testen we
    assert expected == actual
```

---

### 3.7 Arrange-Act-Assert

Elke test volgt dit patroon:

```python
def test_task_becomes_overdue():
    # ARRANGE: zet alles op
    today = date(2024, 1, 1)
    tomorrow = today + timedelta(days=1)
    task = Task('cake bakken', tomorrow)
    tasks = TaskList()
    tasks.add_task(task)

    # ACT: voer de actie uit
    tasks.calendar.today = today + timedelta(days=2)   # twee dagen later

    # ASSERT: controleer het resultaat
    assert task in tasks.overdue_tasks
```

---

### 3.8 Dependency Injection

**Het probleem:** als je code `date.today()` direct gebruikt, kun je in tests niet simuleren dat het een andere datum is zonder echt te wachten.

**De oplossing:** maak de datum een parameter (injecteer de afhankelijkheid):

```python
# Productie-versie
class Calendar:
    @property
    def today(self):
        return date.today()    # echte datum

# Test-versie
class CalendarStub:
    def __init__(self, start_date):
        self.today = start_date   # volledig controleerbaar

    # je kunt ook today instellen: calendar.today = date(2025, 1, 1)
```

```python
# In productie:
task_list = TaskList(Calendar())

# In tests:
fake_calendar = CalendarStub(date(2024, 1, 1))
task_list = TaskList(fake_calendar)
fake_calendar.today = date(2024, 1, 3)   # simuleer 2 dagen later
assert task in task_list.overdue_tasks
```

Andere voorbeelden van dependency injection:
- Dobbelstenen in een spel: `RandomDice` vs `ControlledDice`
- Database: echte database vs nep in-memory versie
- Input/output: `print`/`input` vs netwerk-io

---

### 3.9 Setup en Fixtures

Als meerdere tests dezelfde objecten nodig hebben, vermijd je herhaling via **fixtures**.

**`setup_function` (oudere aanpak):**
```python
today = None

def setup_function():
    global today
    today = date(2024, 1, 1)   # wordt voor ELKE test opnieuw aangemaakt

def test_1():
    # today is hier beschikbaar
    ...
```

**`@pytest.fixture` (moderne aanpak, beter):**

```python
import pytest
from datetime import date, timedelta

@pytest.fixture
def today():
    return date(2024, 1, 1)

@pytest.fixture
def tomorrow(today):            # fixture kan andere fixtures als dependency hebben
    return today + timedelta(days=1)

@pytest.fixture
def calendar(today):
    return CalendarStub(today)

@pytest.fixture
def task_list(calendar):
    return TaskList(calendar)

# Tests vragen fixtures op via parameters:
def test_task_not_overdue(task_list, tomorrow):
    task = Task('beschrijving', tomorrow)
    task_list.add_task(task)
    assert task not in task_list.overdue_tasks

def test_task_becomes_overdue(task_list, calendar, tomorrow):
    task = Task('beschrijving', tomorrow)
    task_list.add_task(task)
    calendar.today = tomorrow + timedelta(days=1)
    assert task in task_list.overdue_tasks
```

**Voordeel van fixtures vs `setup_function`:** alleen de fixtures die een test nodig heeft worden aangemaakt. Als één fixture crasht, falen alleen de tests die die fixture gebruiken — niet alle tests.

---

### 3.10 Assertions in productie-code

`assert` kun je ook buiten tests gebruiken als self-check in je algoritmen:

```python
def max(ns):
    result = ns[0]
    for n in ns:
        if n > result:
            result = n
    assert result in ns                        # check: resultaat zit in de lijst
    assert all(n <= result for n in ns)        # check: geen enkel element is groter
    return result
```

**Opgelet:** in "release mode" (`python -O`) worden `assert`s genegeerd. Gebruik ze nooit voor logica die altijd moet werken — alleen als debug-hulpmiddel.

---

## DEEL 4 — Regular Expressions (Regex)

---

### 4.1 Wat zijn Regular Expressions?

Regular expressions (regex) zijn een minilanguage om **patronen in tekst** te beschrijven. Nuttig voor: validatie (is dit een geldig e-mailadres?), zoeken, vervangen.

In Python gebruik je de `re` module:

```python
import re

# re.fullmatch: controleer of de VOLLEDIGE string matcht
if re.fullmatch(r'patroon', string):
    print("Match!")
```

De `r` voor de string (`r'...'`) staat voor "raw string" — backslashes worden niet geïnterpreteerd door Python, maar doorgegeven aan de regex engine.

---

### 4.2 Regex Syntax

#### Letterlijke tekens
```
a       → exact de letter 'a'
abc     → exact de string 'abc'
```

#### Jokers en klassen
```
.       → elk willekeurig karakter (behalve newline)
\d      → één cijfer (= [0-9])
\w      → één woord-karakter (letter, cijfer of _)
\s      → één witruimte (spatie, tab, ...)
[abc]   → één van: a, b of c
[a-z]   → één kleine letter
[A-Z]   → één hoofdletter
[0-9]   → één cijfer
[^abc]  → alles behalve a, b of c
```

#### Kwantoren (hoeveelheid)
```
a+      → één of meer keer 'a'
a*      → nul of meer keer 'a'
a?      → nul of één keer 'a' (optioneel)
a{3}    → exact 3 keer 'a'
a{2,5}  → 2 tot 5 keer 'a'
a{3,}   → minstens 3 keer 'a'
```

#### Ankers
```
^       → begin van string (of regel in MULTILINE mode)
$       → einde van string (of regel in MULTILINE mode)
```

#### Groepering en alternatieven
```
(abc)   → groepeer 'abc' (ook een capturing group)
a|b     → 'a' of 'b'
```

**Voorbeelden:**

```python
re.fullmatch(r'a', 'a')            # → Match
re.fullmatch(r'a', 'b')            # → None
re.fullmatch(r'\d+', '123')        # → Match (een of meer cijfers)
re.fullmatch(r'\d+', 'abc')        # → None
re.fullmatch(r'[A-Z][a-z]+', 'Hallo')   # → Match (hoofdletter + kleine letters)
re.fullmatch(r'\d{2}:\d{2}:\d{2}', '12:34:56')   # → Match (tijdformaat)
re.fullmatch(r'r\d{7}', 'r1234567')     # → Match (student-ID: r + 7 cijfers)
```

---

### 4.3 Capturing Groups

Haakjes in een regex vangen een stuk van de gematchte tekst op. Handig om substrings te extraheren.

`fullmatch` (en `match`, `search`) returnen bij een match een `Match` object — bij geen match `None`.

```python
match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2})', '12:34:56')

if match:
    h = match.group(1)   # → '12'
    m = match.group(2)   # → '34'
    s = match.group(3)   # → '56'

    # Of in één keer:
    h, m, s = match.groups()
```

**Optionele groepen** geven `None` terug als ze niet gematcht worden:

```python
# Tijdformaat met optionele milliseconden: hh:mm:ss of hh:mm:ss.fff
match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2})(\.\d{3})?', '12:34:56')
h, m, s, ms = match.groups()
ms = ms or '.000'   # als ms None is, gebruik '.000' als default

# Met een expliciete default:
h, m, s, ms = match.groups('.000')
```

---

### 4.4 Substitutie

`re.sub(patroon, vervanging, tekst)` vervangt alle matches van het patroon door de vervanging.

```python
# Verwijder spaties aan het einde van regels:
result = re.sub(r'\s+$', '', text, flags=re.MULTILINE)
# \s+ = een of meer witruimtes
# $   = einde van de regel
# re.MULTILINE = $ matcht ook na elke newline (niet alleen einde van hele string)

# Verberg e-mailadressen:
result = re.sub(r'\b[\w.]+@[\w.]+\b', '[REDACTED]', text)

# Herhaalde woorden verwijderen ("de de" → "de"):
result = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
# \1 verwijst terug naar de eerste capturing group
```

---

## DEEL 5 — Data Processing

---

### 5.1 Setup: Jupyter, Pandas, Matplotlib

```bash
pip install jupyter pandas matplotlib
```

**Jupyter Notebooks** (`.ipynb` bestanden) laten je code, output en tekst combineren in één document. Je voert cellen individueel uit.

**Import conventies** (gebruik altijd deze afkortingen — ze zijn standaard in de Python-gemeenschap):
```python
import pandas as pd
import matplotlib.pyplot as plt
```

---

### 5.2 Pandas

Pandas is de standaard bibliotheek voor data-analyse in Python.

#### Series — één kolom data

```python
s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40

print(s[2])    # → 30
print(s.mean()) # → 25.0
```

#### DataFrame — tabel met rijen en kolommen

```python
data = {
    'naam': ['Alice', 'Bob', 'Carol'],
    'leeftijd': [25, 30, 22],
    'stad': ['Brussel', 'Gent', 'Antwerpen']
}
df = pd.DataFrame(data)
```

```
     naam  leeftijd     stad
0   Alice        25  Brussel
1     Bob        30     Gent
2   Carol        22  Antwerpen
```

**Veelgebruikte operaties:**

```python
# Kolom selecteren:
df['naam']           # → Series met namen
df[['naam', 'stad']] # → DataFrame met twee kolommen

# Rijen filteren:
df[df['leeftijd'] >= 25]   # → enkel rijen met leeftijd ≥ 25

# Statistieken:
df['leeftijd'].mean()   # gemiddelde
df['leeftijd'].max()    # maximum
df.describe()           # overzicht van alle statistieken

# CSV inlezen:
df = pd.read_csv('data.csv')

# Groeperen:
df.groupby('stad')['leeftijd'].mean()   # gemiddelde leeftijd per stad
```

---

### 5.3 Data Visualisatie met Matplotlib

```python
import matplotlib.pyplot as plt

# Lijngrafiek:
plt.plot([1, 2, 3, 4], [10, 20, 15, 25])
plt.xlabel('X-as')
plt.ylabel('Y-as')
plt.title('Mijn grafiek')
plt.show()

# Rechtstreeks vanuit Pandas:
df['leeftijd'].plot(kind='bar')   # staafgrafiek
df['leeftijd'].hist()             # histogram
plt.show()
```

---

### 5.4 Datetime en Apply

**Datum/tijd-kolommen in Pandas:**

```python
df['datum'] = pd.to_datetime(df['datum'])   # zet string om naar datetime
df['jaar'] = df['datum'].dt.year             # extraheer jaar
df['maand'] = df['datum'].dt.month           # extraheer maand
```

**`.apply()` — pas een functie toe op elke rij/kolom:**

```python
# Verdubbel elke leeftijd:
df['dubbele_leeftijd'] = df['leeftijd'].apply(lambda x: x * 2)

# Categorie toekennen op basis van leeftijd:
def categorie(leeftijd):
    if leeftijd < 18:
        return 'minderjarig'
    elif leeftijd < 65:
        return 'volwassen'
    else:
        return 'senior'

df['categorie'] = df['leeftijd'].apply(categorie)
```

---

## Overzichtstabel

| Hoofdstuk | Kern-concepten | Sleutelwoorden |
|-----------|---------------|----------------|
| **OOP** | Classes, encapsulation, properties | `@property`, `@setter`, `__init__`, `self`, `super()`, `ABC`, `@abstractmethod` |
| **Functioneel** | Functies als waarden, compacte transformaties | `lambda`, `yield`, `[... for ... in ...]`, `itertools` |
| **Testen** | Automatisch verifiëren van correctheid | `pytest`, `assert`, `@parametrize`, `approx`, `raises`, `@fixture` |
| **Regex** | Patroonherkenning in tekst | `re.fullmatch`, `re.sub`, `.group()`, `\d`, `+`, `*`, `?`, `{n}` |
| **Data** | Tabulaire data analyseren en visualiseren | `pd.DataFrame`, `.apply()`, `matplotlib.pyplot` |
