class Dog:
    def __init__(self, name, birth_year, breed, color, father=None, mother=None):
        self.name = name
        self.birth_year = birth_year
        self.breed = breed
        self.color = color
        self.father = father
        self.mother = mother

    def __eq__(self, other):
        if not isinstance(other, Dog):
            return False
        
        # It is the same dog if the parents are the same, the name is the same and the birth year is the same
        return self.name == other.name and self.birth_year == other.birth_year and self.father == other.father and self.mother == other.mother
     
    def __str__(self):
        return f"{self.name} (born {self.birth_year}) is a {self.breed}."
    
    def __repr__(self):
        return self.__str__()

# Generation 1
rex = Dog("Rex", 2005, "Labrador", "golden")
bella = Dog("Bella", 2006, "Labrador", "black")

buster = Dog("Buster", 2007, "Beagle", "brown-white")
rosie = Dog("Rosie", 2008, "Beagle", "brown-white")

thor = Dog("Thor", 2006, "German Shepherd", "black-tan")
elsa = Dog("Elsa", 2007, "German Shepherd", "black")

# Generation 2
max = Dog("Max", 2010, "Labrador", "golden", father=rex, mother=bella)
luna = Dog("Luna", 2011, "Labrador", "brown", father=rex, mother=bella)

penny = Dog("Penny", 2011, "Beagle", "brown-white", father=buster, mother=rosie)
leo = Dog("Leo", 2012, "German Shepherd", "black", father=thor, mother=elsa)

# Extra dogs in Generation 2
charlie = Dog("Charlie", 2009, "Labrador", "brown")
molly = Dog("Molly", 2010, "Labrador", "black")

# Generation 3
daisy = Dog("Daisy", 2016, "Labrador", "black", father=max, mother=molly)
milo = Dog("Milo", 2015, "Labrador", "black", father=max, mother=molly)

buddy = Dog("Buddy", 2014, "Labrador", "brown", father=charlie, mother=luna)
rocky = Dog("Rocky", 2014, "Labrador", "golden", father=charlie, mother=luna)

maggie = Dog("Maggie", 2015, "Beagador", "black-brown", father=max, mother=penny)  # Labrador x Beagle
zeus = Dog("Zeus", 2016, "Sheprador", "black-tan", father=leo, mother=luna)

# Extra dogs in generation 3
cooper = Dog("Cooper", 2017, "Labrador", "golden")
sophie = Dog("Sophie", 2018, "Border Collie", "black")

# Generation 4
nala = Dog("Nala", 2018, "Labrador", "golden", father=cooper, mother=daisy)
bailey = Dog("Bailey", 2019, "Labrador", "golden", father=buddy, mother=daisy)
shadow = Dog("Shadow", 2019, "Labrador", "brown", father=rocky, mother=daisy)

ruby = Dog("Ruby", 2020, "Labrador", "black", father=buddy, mother=sophie)

#Generation 5
pepper = Dog("Pepper", 2022, "Labracollie", "black", father=shadow, mother=sophie)