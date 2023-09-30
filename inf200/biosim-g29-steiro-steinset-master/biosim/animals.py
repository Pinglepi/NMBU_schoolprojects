# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from math import exp
import random


class Animal:
    """All the shared functions between the different species"""
    parameter = {'w_birth': None, 'sigma_birth': None, 'beta': None, 'eta': None,
                 'a_half': None, 'phi_age': None,
                 'w_half': None, 'phi_weight': None, 'mu': None, 'gamma': None, 'zeta': None,
                 'xi': None, 'omega': None, 'F': None, 'DeltaPhiMax': None}

    def __init__(self, weight, age=0):
        """When an animal is created it gets a weight and its age

        Note that an instance of the animal class should never be created. Choose the herbivore or
        carnivore class instead.

        :param weight: The weight of the newly created animal as float

        :param age: The age of the newly created animal as int, defaults to 0
        """
        if weight < 0 or age < 0:
            raise ValueError('Age and weight must be positive numbers.')
        self.weight = weight
        self.age = age
        self.fitness = 0.8

    def __eq__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return self.fitness == rhs.fitness

    def __lt__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return self.fitness < rhs.fitness

    def __ne__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return not (self.fitness == rhs.fitness)

    def __le__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return (self.fitness < rhs.fitness) or (self.fitness == rhs.fitness)

    def __ge__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return not (self.fitness < rhs.fitness)

    def __gt__(self, rhs):
        """Makes the animals compare itself with other animals through fitness"""
        return not (self.fitness <= rhs.fitness)

    def lose_weight(self):
        """Change the animal weight according to its yearly loss"""
        self.weight -= self.parameter['eta'] * self.weight

    def gain_age(self):
        """Change the animals age by one"""
        self.age += 1

    def find_fitness(self):
        """
        Calculates the fitness of the animal

        :returns: Animals current fitness
        :rtype: float
        """
        if self.weight <= 0.000001:
            self.fitness = 0
        else:
            self.fitness = self._q(self.age, self.parameter['a_half'], self.parameter['phi_age']) *\
                           self._q(self.weight, self.parameter['w_half'],
                                   -self.parameter['phi_weight'])

    def check_birth(self, n_animals):
        """
        Finds out if the animal gives birth, if it does, its weight is decreased by some amount
        
        :return: the weight of the newborn
        :rtype: float
        """
        if min(1, self.parameter['gamma'] * self.fitness * (n_animals - 1)) > random.random() and \
                self.weight >= self.parameter['zeta'] * (
                self.parameter['w_birth'] + self.parameter['sigma_birth']):
            weight_newborn = random.gauss(self.parameter['w_birth'], self.parameter['sigma_birth'])
            if self.weight > weight_newborn * self.parameter['xi']:
                self.weight -= weight_newborn * self.parameter['xi']
                return weight_newborn
            else:
                return 0
        else:

            return 0

    def check_death(self):
        """
        Checks if the animal is supposed to die

        :return: True if the animal is supposed to die
        """
        if self.weight <= 0.000001 or self.parameter['omega'] * (
                1 - self.fitness) > random.random():
            return True
        else:
            return False

    @staticmethod
    def _q(x, x_half, phi):
        """
        Calculates the _q value for use in the the fitness method

        :param x: Either the age or weight of the animal as int or float

        :param x_half: Either the a_half or w_half value from the class parameter as int or float

        :param phi: Either the phi_age or -phi_weight as int or float

        :return: A value used for further calculations, between 0 and 1
        :rtype: float
        """
        return 1 / (1 + exp(phi * (x - x_half)))

    @classmethod
    def set_animal_parameters(cls, p_dict):
        """
        Set the animal parameter for all instances of the class

        :param p_dict: A dictionary with keys containing the new values for the parameter
        """
        for key in p_dict:
            if key not in cls.parameter:
                raise ValueError('Invalid parameter name: ' + key)
            if p_dict[key] < 0:
                raise ValueError('Parameter values cannot be negative')
            if key == 'eta':
                if p_dict['eta'] > 1:
                    raise ValueError('eta must be on the interval [0,1]')
            elif key == 'DeltaPhiMax':
                if p_dict['DeltaPhiMax'] == 0:
                    raise ValueError('DeltaPhiMax must be more than 0')
            cls.parameter[key] = p_dict[key]

    def check_migration(self):
        """Finds out if the animal will try to migrate

        :return: True if the animal tries to migrate
        :rtype: bool
        """
        if self.parameter['mu'] * self.fitness > random.random():
            return True
        else:
            return False


class Herbivore(Animal):
    """A Herbivore that eats plants"""

    parameter = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                 'a_half': 40.0, 'phi_age': 0.6,
                 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5,
                 'xi': 1.2, 'omega': 0.4, 'F': 10, 'DeltaPhiMax': None}

    def eat(self, food):
        """Makes the animal eat from the given amount of food

        :param food: The remaining food on the tile the animal is a part of

        :return: the amount of remaining food after the animal has eaten
        :rtype: int, float

        """
        if food >= self.parameter['F']:
            self.weight += self.parameter['beta'] * self.parameter['F']
            return food - self.parameter['F']
        elif food > 0:
            self.weight += self.parameter['beta'] * food
            return 0
        else:
            return 0


class Carnivore(Animal):
    """A carnivore that eats herbivores"""

    parameter = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
                 'a_half': 40.0, 'phi_age': 0.3,
                 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5,
                 'xi': 1.1,
                 'omega': 0.8, 'F': 50, 'DeltaPhiMax': 10.0}

    def c_eat(self, herbivore_list):
        """Makes the carnivore eat from a list of herbivores

        If the carnivore is successful at hunting it will eat towards its capacity and gain
        weight accordingly.
        If it hunts beyond capacity, the remaining food after it has eaten will be wasted.
        When capacity is reached, the carnivore will stop hunting.

        :param herbivore_list: A list of all the herbivores remaining on the tile

        :return: A list of the animals eaten
        :rtype: list
        """
        food_eaten = 0
        animals_eaten = []
        if len(herbivore_list) != 0:
            for i in herbivore_list:
                if food_eaten < self.parameter['F']:
                    p = 1
                    if self.fitness <= i.fitness:
                        p = 0
                    elif 0 < (self.fitness - i.fitness) < self.parameter['DeltaPhiMax']:
                        p = (self.fitness - i.fitness) / self.parameter['DeltaPhiMax']
                    if p > random.random():
                        if food_eaten + i.weight < self.parameter['F']:
                            self.weight += i.weight * self.parameter['beta']
                        else:
                            self.weight += (self.parameter['F'] - food_eaten) * self.parameter[
                                'beta']
                        food_eaten += i.weight
                        self.find_fitness()
                        animals_eaten.append(i)
                else:
                    break
        return animals_eaten
