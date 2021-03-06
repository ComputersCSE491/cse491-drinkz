"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = parse_csv(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
        
        n += 1
        db.add_bottle_type(mfg, name, typ)

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = parse_csv(fp)

    x = []
    n = 0

    for line in reader:
        try:
            (mfg, name, amount) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
    
        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n

def load_recipes(fp):
    import recipes
    n = 0

    this_recipe = ""
    ingredients = []
    for line in parse_csv(fp):
        # take in multiple lines of NAME, INGREDIENT, AMOUNT
        # where successive liens of NAME add INGREDIENT, AMOUNT to the recipe.
        recipe_name, ingredient, amount = line

        # new recipe?
        if this_recipe != recipe_name:
            if this_recipe and ingredients:
                r = recipes.Recipe(this_recipe, ingredients)
                db.add_recipe(r)
                n += 1

            this_recipe = recipe_name
            ingredients = [(ingredient, amount)]
        else:
            ingredients.append((ingredient, amount))
            
    # new recipe?
    if this_recipe and ingredients:
        r = recipes.Recipe(this_recipe, ingredients)
        db.add_recipe(r)
        n += 1

    return n

def parse_csv(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line
