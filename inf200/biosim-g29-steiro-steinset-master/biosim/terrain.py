# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from .animals import Herbivore, Carnivore
import random


class Terrain:
    """
    Implements a terrain tile containing herbivores and carnivores,
    as well as info about amount of food on the tile.
    """

    def __init__(self):
        self.terrain_type = None
        self.herbivores_on_tile = []
        self.carnivores_on_tile = []
        self.animals_on_tile = [self.herbivores_on_tile, self.carnivores_on_tile]
        self.all_animals = self.herbivores_on_tile + self.carnivores_on_tile

    def spawn_animal(self, spawn):
        """
        Places a number of animals on the current tile

        :param spawn: list of animals with tuple containing the keys: species, weight and age
        """
        for i in spawn:
            if i['species'] == 'Herbivore':
                self.herbivores_on_tile.append(Herbivore(i['weight'], i['age']))
            elif i['species'] == 'Carnivore':
                self.carnivores_on_tile.append(Carnivore(i['weight'], i['age']))

    def eat_on_tile(self):
        """
        Calls both herbivores and carnivores on tile to eat.
        """
        self.herb_eat_on_tile()
        self.carn_eat_on_tile()

    def carn_eat_on_tile(self):
        """Makes all the present carnivore try to eat"""
        self.herbivores_on_tile.sort()
        self.carnivores_on_tile.sort(reverse=True)
        for k in range(len(self.carnivores_on_tile)):
            eaten = (self.carnivores_on_tile[k].c_eat(self.herbivores_on_tile))
            for i in reversed(range(len(eaten))):
                self.herbivores_on_tile.remove(self.herbivores_on_tile[i])

    def herb_eat_on_tile(self):
        total_food = self.F_max
        random.shuffle(self.herbivores_on_tile)
        for k in range(len(self.herbivores_on_tile)):
            total_food = self.herbivores_on_tile[k].eat(total_food)
            if total_food == 0:
                break
            self.herbivores_on_tile[k].find_fitness()

    def migration_herb(self, legal_moves):
        """
        Returns list of all herbivores on tile that will move, in lists of where they will move.

        :param legal_moves: list of boolean values indicating what neighboring
         tiles are available for immigration.
        """
        up = []
        down = []
        left = []
        right = []
        migrate_list = [up, down, right, left]
        remaining_herbivores = []
        for k in range(len(self.herbivores_on_tile)):
            if self.herbivores_on_tile[k].check_migration():
                index = random.randrange(len(legal_moves))
                if legal_moves[index]:
                    migrate_list[index].append(self.herbivores_on_tile[k])
                else:
                    remaining_herbivores.append(self.herbivores_on_tile[k])
            else:
                remaining_herbivores.append(self.herbivores_on_tile[k])
        self.herbivores_on_tile = remaining_herbivores
        return migrate_list

    def migration_carn(self, legal_moves):
        """Returns list of all carnivores on tile that will move, in lists of where they will move.

        :param legal_moves: list of boolean values indicating what neighboring
         tiles are available for immigration.
        """
        up = []
        down = []
        left = []
        right = []
        migrate_list = [up, down, right, left]
        remaining_carnivores = []
        for k in range(len(self.carnivores_on_tile)):
            if self.carnivores_on_tile[k].check_migration():
                index = random.randrange(len(legal_moves))
                if legal_moves[index]:
                    migrate_list[index].append(self.carnivores_on_tile[k])
                else:
                    remaining_carnivores.append(self.carnivores_on_tile[k])
            else:
                remaining_carnivores.append(self.carnivores_on_tile[k])
        self.carnivores_on_tile = remaining_carnivores
        return migrate_list

    def breed_on_tile(self):
        """
        Makes all animals on a tile breed, if number of animals is high enough,
        and adds the newborn to the list of its species on the tile.
        """
        n_herbs = self.count_herbivores()
        if n_herbs > 1:
            for k in range(n_herbs):
                birth_weight = self.herbivores_on_tile[k].check_birth(n_herbs)
                if not birth_weight <= 0:
                    self.herbivores_on_tile.append(Herbivore(birth_weight))
        n_carns = self.count_carnivores()
        if n_carns > 1:
            for k in range(n_carns):
                birth_weight = self.carnivores_on_tile[k].check_birth(n_carns)
                if birth_weight != 0:
                    self.carnivores_on_tile.append(Carnivore(birth_weight))

    def die_on_tile(self):
        """
        Removes all animals on the tile that are dying.
        """
        alive_herb = []
        alive_carn = []
        for k in reversed(range(len(self.herbivores_on_tile))):
            self.herbivores_on_tile[k].find_fitness()
            if not self.herbivores_on_tile[k].check_death():
                alive_herb.append(self.herbivores_on_tile[k])
        for k in reversed(range(len(self.carnivores_on_tile))):
            self.carnivores_on_tile[k].find_fitness()
            if not self.carnivores_on_tile[k].check_death():
                alive_carn.append(self.carnivores_on_tile[k])
        self.herbivores_on_tile = alive_herb
        self.carnivores_on_tile = alive_carn

    def age_on_tile(self):
        """
        Calls on all the animals on the tile to age by one year
        """
        for k in range(len(self.carnivores_on_tile)):
            self.carnivores_on_tile[k].gain_age()
        for k in range(len(self.herbivores_on_tile)):
            self.herbivores_on_tile[k].gain_age()

    def lose_weight_on_tile(self):
        """
        Calls on all the animals on the tile to lose weight
        """
        for k in range(len(self.herbivores_on_tile)):
            self.herbivores_on_tile[k].lose_weight()
        for k in range(len(self.carnivores_on_tile)):
            self.carnivores_on_tile[k].lose_weight()

    def count_herbivores(self):
        """
        Returns the number of herbivores on the tile
        """
        return len(self.herbivores_on_tile)

    def count_carnivores(self):
        """
        Returns the number of carnivores on the tile
        """
        return len(self.carnivores_on_tile)

    def count_animals(self):
        """
        Returns the number of animals on the tile
        """
        return self.count_herbivores() + self.count_carnivores()

    def get_values_herb(self):
        """
        Returns a list of lists containing all ages, fitness and weights, respectively, of
        the herbivores on the tile.
        """
        age_list = []
        fitness_list = []
        weight_list = []
        for i in self.herbivores_on_tile:
            age_list.append(i.age)
            fitness_list.append(i.fitness)
            weight_list.append(i.weight)
        return [age_list, fitness_list, weight_list]

    def get_values_carn(self):
        """
        Returns a list of lists containing all ages, fitness and weights, respectively, of
        the carnivores on the tile.
        """
        age_list = []
        fitness_list = []
        weight_list = []
        for i in self.carnivores_on_tile:
            age_list.append(i.age)
            fitness_list.append(i.fitness)
            weight_list.append(i.weight)
        return [age_list, fitness_list, weight_list]

    @classmethod
    def set_params(cls, params):
        """
        Changes the maximum value of fodder on a tile.

        :param params: dictionary containing terrain type as key, fodder amount as attribute
        """
        cls.F_max = params['f_max']


class Lowland(Terrain):
    """
    Implements a tile with a high amount of fodder for herbivores, which is
    possible to be entered by animals.
    """
    movable = True
    terrain_type = "Lowland"
    F_max = 800


class Highland(Terrain):
    """
    Implements a tile with some fodder for herbivores, which is
    possible to be entered by animals.
    """
    movable = True
    terrain_type = "Highland"
    F_max = 300


class Desert(Terrain):
    """
    Implements a tile with no fodder for herbivores, which is possible to be entered by animals.
    """
    movable = True
    terrain_type = "Desert"
    F_max = 0


class Water(Terrain):
    """
    Implements a tile without any fodder, which is not possible to be entered by animals.
    """
    movable = False
    terrain_type = "Water"
    F_max = 0
