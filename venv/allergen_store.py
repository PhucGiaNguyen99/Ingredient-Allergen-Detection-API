# allergen_store.py
allergens = ["peanut", "gluten", "milk", "soy", "egg"]

def get_allergens():
    return allergens

def set_allergens(new_list):
    global allergens
    allergens = new_list
