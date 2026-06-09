from dog import *

###############
#
# Ok, let's have a look at the import above.
# It imports the Dog class and a lot of Dog objects
# Let's see how we can use them 
#
###############

# First, we will make 1 list with all dogs in it
all_dogs = [
    rex, bella, max, luna, charlie, molly,
    daisy, milo, buddy, rocky, cooper, sophie,
    nala, bailey, shadow, ruby, pepper, 
    buster, rosie, thor, elsa,
    penny, leo,
    maggie, zeus
]

###############
#
# We want to count the number of dogs for a certain breed and/or the number of dogs for a certain color
# We will do this by using a generic count method, which will receive a lambda to do the counting
#
###############

def count(collection, condition):
    ... # TODO: implement the generic count method

def count_breed(dogs, breed):
    ... # TODO: implement the count_breed method, using the generic count method

# Example Usage
labrador_count = count_breed(all_dogs, "Labrador")
print(f"Number of Labradors: {labrador_count}") #15

labracollie_count = count_breed(all_dogs, "Labracollie")
print(f"Number of Labracollies: {labracollie_count}") #1

def count_color(dogs, color):
    ... # TODO: implement the count_color method, using the generic count method

# Example Usage
black_count = count_color(all_dogs, "black")
print(f"Number of black dogs: {black_count}") #9

brown_count = count_color(all_dogs, "brown")
print(f"Number of brown dogs: {brown_count}") #4

###############
#
# Let's try to solve this problem in a different way
# We can also do this by using recursion
# It is not the most efficient way to do this, but it is a good exercise :-) 
#
###############

def count_breed_recursive(dogs, breed):
    ... # TODO: implement the recursive count_breed method

# Example usage
labrador_count_recursive = count_breed_recursive(all_dogs, "Labrador")
print(f"Number of Labradors (recursive): {labrador_count_recursive}") # 15

labracollie_count_recursive = count_breed_recursive(all_dogs, "Labracollie")
print(f"Number of Labracollies (recursive): {labracollie_count_recursive}") # 1

# Recursive method to count certain type of color
def count_color_recursive(dogs, color):
    ... # TODO: implement the recursive count_color method

# Example usage
black_count_recursive = count_color_recursive(all_dogs, "black")
print(f"Number of black dogs (recursive): {black_count_recursive}") # 9

brown_count_recursive = count_color_recursive(all_dogs, "brown")
print(f"Number of brown dogs (recursive): {brown_count_recursive}") # 4

###############
#
# Let's implement a method to see if two dogs are from the same nest
#
###############

def from_same_nest(dog1, dog2):
    # Check of they have the same father
    if dog1.father != dog2.father:
        return False

    # Check of they have the same mother
    if dog1.mother != dog2.mother:
        return False
    
    # Check if they were born in the same year
    if dog1.birth_year != dog2.birth_year:
        return False
    
    # Check if it is not the same dog
    if dog1 == dog2:
        return False
    
    # Ok let's assume they are from the same nest
    return True

###############
#
# Now let's implement the necessary tests in tests.py to test the above method
# Make sure to test every case possible!
#
###############

###############
#
# Time for regex! And let's combine this with some comprehensions
# Find all dogs with a name that starts with the letter 'B' and whose name contains two same characters in a row
# Return the names of those dogs in a list, and use comprehensions for this
#
###############

def find_dog_names_regex(dogs):
    ... # TODO: implement the regex method

# Example usage
dog_names = find_dog_names_regex(all_dogs)
print(dog_names) # ['Bella', 'Buddy']

###############
#
# Since recursion is everybody's favorite topic, let's implement another recursive method
# Given, a specific dog and a color, return how many of it's ancestors in the family tree have that color.
# 
###############

def count_ancestors(dog, color):
    ... # TODO: implement the recursive count_ancestors method

# Example usage
rex_ancestors = count_ancestors(rex, "golden")
print(f"Number of ancestors of golden dogs in Rex's family tree: {rex_ancestors}") # 1

max_ancestors = count_ancestors(max, "golden")
print(f"Number of ancestors of golden dogs in Max's family tree: {max_ancestors}") # 2

buddy_ancestors = count_ancestors(buddy, "golden")
print(f"Number of ancestors of golden dogs in Buddy's family tree: {buddy_ancestors}") # 1

rocky_ancestors = count_ancestors(rocky, "golden")
print(f"Number of ancestors of golden dogs in Rocky's family tree: {rocky_ancestors}") # 2

pepper_ancestors = count_ancestors(pepper, "golden")
print(f"Number of ancestors of golden dogs in Pepper's family tree: {pepper_ancestors}") # 4

###############
#
# Let's implement a pedigree purity checker!
# We want to know if a dog is a purebred of a certain breed.
# Create a recursive function that checks whether the dog and all known ancestors are of the same given breed.
# If even one known ancestor has a different breed, the dog is NOT considered purebred.
#
###############

def is_pure_breed(dog, breed):
    ... # TODO: implement the is_pure_breed method

# Example Usage
print(is_pure_breed(rex, "Labrador"))         # True — no known parents, we assume Rex is a purebred
print(is_pure_breed(max, "Labrador"))         # True — both parents are Labradors
print(is_pure_breed(penny, "Beagle"))         # True — both parents are Beagles
print(is_pure_breed(leo, "German Shepherd"))  # True
print(is_pure_breed(ruby, "Labrador"))        # False — Sophie's not a Labrador

###############
#
# Let's go back to comprehensions
# Using only comprehensions, give an overview of all years in which a dog was born, between a start_year and an end_year
# 
###############

def years_of_birth(dogs, start_year, end_year):
    ... # TODO: implement the years_of_birth method
 
# Example usage
years = years_of_birth(all_dogs, 2010, 2015)
print(f"Years of birth between 2010 and 2015: {years}") # {2010, 2011, 2012, 2014, 2015}

# Example usage
years = years_of_birth(all_dogs, 2012, 2017)
print(f"Years of birth between 2012 and 2017: {years}") # {2016, 2017, 2012, 2014, 2015}

###############
#
# Oops, maybe you noticed that the years are not sorted. And we want them sorted
# 
###############

def years_of_birth_sorted(dogs, start_year, end_year):
    ... # TODO: implement the years_of_birth_sorted method

# Example usage
years = years_of_birth_sorted(all_dogs, 2010, 2015)
print(f"Years of birth between 2010 and 2015 (sorted): {years}") # [2010, 2011, 2012, 2014, 2015]

years = years_of_birth_sorted(all_dogs, 2012, 2017)
print(f"Years of birth between 2012 and 2017 (sorted): {years}") # [2012, 2014, 2015, 2016, 2017]

###############
#
# Update tests.py by implementing new tests for your newly added methods.
# Make sure to test every case possible!
#
###############

###############
# 
# For the challenge seekers:
# Your goal is to print a dog's family tree using indentation and branch-like structure.
#
# Example Output:
#
# Pepper (2022) - Labracollie
# ├── Father: Shadow (2019) - Labrador
# │   ├── Father: Rocky (2014) - Labrador
# │   │   ├── Father: Charlie (2009) - Labrador
# │   │   └── Mother: Luna (2011) - Labrador
# │   └── Mother: Daisy (2016) - Labrador
# │       ├── Father: Max (2010) - Labrador
# │       └── Mother: Molly (2010) - Labrador
# └── Mother: Sophie (2018) - Border Collie
#
# Use special characters (├──, └──, │) to indicate branches!
# Tip: use a 'prefix' string for the intendation.
###############

def print_visual_family_tree(dog, prefix=""):
    ... # TODO: implement the print_visual_family_tree method    