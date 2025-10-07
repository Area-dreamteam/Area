from dataclasses import dataclass



@dataclass
class Wagon:
    source_service: str
    source_action: str
    ingredients: dict[str, str]


class DataSubway:
    def __init__(self):
        self.wagon_list: list[Wagon] = []
    
    def get_ingredients(self):
        ingredients = {}
        for wagon in self.wagon_list:
            ingredients.update(wagon.ingredients)
        return ingredients

    def add_wagon(self, wagon):
        self.wagon_list.append(wagon)
