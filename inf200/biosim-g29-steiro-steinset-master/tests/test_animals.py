# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.animals import Herbivore, Carnivore
import pytest
import scipy.stats as stats
import random
import math

"""
Tests all animals through testing herbivore animals, except for 
functions that differs between species. Many tests are inspired by 
Hans Ekkhard Plesser's biolab_project and its tests.
"""

herbivore_parameter = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                       'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                       'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                       'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
                       'F': 10}
carnivore_parameter = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
                       'a_half': 40.0, 'phi_age': 0.3,
                       'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5,
                       'xi': 1.1,
                       'omega': 0.8, 'F': 50, 'DeltaPhiMax': 10.0}


@pytest.fixture
def set_animal_parameters(request):
    """
    Fixture setting class parameters on Animal.

    The fixture sets Animal parameters when called for setup,
    and resets them when called for teardown. This ensures that modified
    parameters are always reset before leaving a test. The default parameters that will be reset
    to are listed over, called carnivore_parameter and herbivore_parameter.

    This fixture should be called via parametrize with indirect=True.

    Based on https://stackoverflow.com/a/33879151

    Parameters
    ----------
    request
        Request object automatically provided by pytest.
        request.param is the parameter dictionary to be passed to
        Animal.set_params()
    """

    Carnivore.set_animal_parameters(request.param)
    Herbivore.set_animal_parameters(request.param)
    yield
    Herbivore.set_animal_parameters(herbivore_parameter)
    Carnivore.set_animal_parameters(carnivore_parameter)


@pytest.mark.parametrize('set_animal_parameters', [{'mu': 10}], indirect=True)
def test_set_animal_parameters(set_animal_parameters):
    h = Herbivore(5)
    c = Carnivore(5)
    h.set_animal_parameters({'omega': 10})
    c.set_animal_parameters({'mu': 10})
    assert h.parameter['omega'] == 10 and c.parameter['mu'] == 10


def test_misspelled_parameter():
    c = Carnivore(5)
    with pytest.raises(ValueError):
        c.set_animal_parameters({'Gamam': 0.5})


def test_illegal_parameter_values():
    c = Carnivore(5)
    with pytest.raises(ValueError):
        c.set_animal_parameters({'mu': -1})


def test_illegal_eta():
    h = Herbivore(5)
    with pytest.raises(ValueError):
        h.set_animal_parameters({'eta': 2})


def test_illegal_deltaphimax():
    c = Carnivore(5)
    with pytest.raises(ValueError):
        c.set_animal_parameters({'DeltaPhiMax': 0})


def test_eq():
    """
    Tests the overriding __eq__ function in animals.py 
    """
    for _ in range(10):
        assert Herbivore(10, 0).__eq__(Herbivore(10, 0))


def test_newborns_age():
    """
    Test that all newborn animals have age 0.
    """
    h = Herbivore(10)
    assert h.age == 0


def test_illegal_age_or_weight():
    """Tests that animals spawned with negative age or weight raises a ValueError"""
    with pytest.raises(ValueError):
        Herbivore(weight=-5, age=-5)


def test_animal_aging():
    """
    This test is *determinstic*: for each call to ages(), the age must increase by one year.
    """
    h = Herbivore(10)
    for n in range(100):
        h.gain_age()
        assert h.age == n + 1


def test_lose_weight():
    """
    Test that an animal gains weight when eating.
    """
    weight = 8
    for n in range(10):
        h = Herbivore(weight)
        h.lose_weight()
        assert h.weight == weight - 0.05 * weight


def test_certain_death():
    """
    This test is *deterministic*: We set weight to 0, to make sure fitness will be 0, and then
    when check_death is called, the return value should always be True
    """
    for _ in range(100):
        h = Herbivore(weight=0)
        h.find_fitness()
        assert h.check_death()


@pytest.mark.parametrize('set_animal_parameters', [{'omega': 0}], indirect=True)
def test_animal_certain_survival(set_animal_parameters):
    """
    This test is *deterministic*: We set death probability to 0,
    thus the animal must never die. The animal is spawned with a weight over
    the death limit, so in this case, the death is only dependent on the probability
    determined by omega.
    We call dies() multiple times to test this.
    """
    for _ in range(100):
        h = Herbivore(10)
        assert not h.check_death()


def test_low_fitness():
    """
    This tests that an animal has a fitness of 0 when their weight is 0. The find_fitness function
    is called after spawning the animal of weight 0 to set the fitness attribute.
    """
    for _ in range(100):
        h = Herbivore(0)
        h.find_fitness()
        assert h.fitness == 0


def test_animal_no_births():
    """
    This test asserts that if there is only one animal in a cell,
    it will not give birth.
    """
    h = Herbivore(10)
    for _ in range(100):
        assert h.check_birth(1) == 0


@pytest.mark.parametrize('set_animal_parameters', [{'omega': 0, 'gamma': 1}], indirect=True)
def test_animal_certain_birth(set_animal_parameters, mocker):
    """
    Tests that an animal will certainly give birth by setting several
    parameters to optimal values, and assuring a high weight of mother animal.
    Since Animal.check_birth returns the weight of the newborn, the mocker is used to assure a
    known newborn weight that will not exceed the mother's weight.
    """
    mocker.patch('random.gauss', return_value=4)
    h = Herbivore(100)
    for _ in range(10):
        assert h.check_birth(100) == 4


@pytest.mark.parametrize('set_animal_parameters', [{'xi': 100}], indirect=True)
def test_no_birth_because_of_weight(set_animal_parameters):
    """
    Tests that the Animal.check_birth function returns 0 when the weight of
    the mother animal is smaller than the weight of the newborn. This is
    assured by setting the xi value very high, and the input of check_birth is
    a high number of animals.
    """
    h = Herbivore(weight=50)
    for _ in range(10):
        assert h.check_birth(100) == 0


def test_spawned_animal_values():
    """
    Tests that animals have the given values of weight and age when spawned.
    """
    h = Herbivore(age=5, weight=10)
    for _ in range(10):
        assert h.age == 5 and h.weight == 10


def test_herbivore_eat():
    """
    Tests that food is always eaten by a herbivore when there is enough
    fodder on the tile.
    """
    h = Herbivore(8.0)
    h.find_fitness()
    for _ in range(10):
        food = h.parameter['F'] + 1
        assert h.eat(food) == 1


@pytest.mark.parametrize('set_animal_parameters', [{'beta': 1}], indirect=True)
def test_herbivore_gain_weight(set_animal_parameters):
    """
    Tests that a herbivore gains the right amount of weight when eating a
    certain amount of fodder.
    """
    h = Herbivore(weight=0)
    h.find_fitness()
    for n in range(10):
        h.eat(10)
        assert h.weight == 10 * n + 10


def test_herbivore_no_food():
    """
    Tests that a herbivore doesn't eat when there is no more fodder
    left on the tile.
    """
    h = Herbivore(10)
    h.find_fitness()
    for _ in range(10):
        assert h.eat(0) == 0


@pytest.mark.parametrize('set_animal_parameters', [{'beta': 1, 'F': 12}], indirect=True)
def test_herbivore_eat_rest(set_animal_parameters):
    """
    Tests that a herbivore only eats the rest of the fodder on a tile, when there
    is less fodder available than what the animal wants, by checking that it
    gains a weight equivalent of the weight of the fodder, when beta
    is set to 1.
    """
    h = Herbivore(weight=0)
    h.find_fitness()
    for n in range(10):
        food = h.parameter['F'] - 2
        h.eat(food)
        assert h.weight == 10 * n + 10


@pytest.mark.parametrize('set_animal_parameters', [{'DeltaPhiMax': 0.01}], indirect=True)
def test_carnivore_always_eats(set_animal_parameters):
    """
    Tests that a carnivore definitely eats a herbivore by setting DeltaPhiMax to a very
    small number, that assures a probability of >=1 of preying on a herbivore.
    """
    for _ in range(100):
        c = Carnivore(10)
        h = Herbivore(10)
        c.find_fitness()
        h.find_fitness()
        assert len(c.c_eat([h])) == 1


@pytest.mark.parametrize('set_animal_parameters', [{'beta': 1, 'DeltaPhiMax': 0.01}], indirect=True)
def test_carnivore_gain_weight(set_animal_parameters):
    """
    Tests that a carnivore gains weight in the correct way when eating a
    herbivore. When setting beta = 1, the carnivore will gain all of the weight
    from its prey, and this test utilize the fact that the carnivore will always
    gain 10 in weight when eating a herbivore of weight 10.
    Setting DeltaPhiMax to a very low number assures that the possibility of the carnivore
    preying on the chosen herbivore is high enough.
    """
    c = Carnivore(weight=10)
    c.find_fitness()
    for n in range(10):
        h = Herbivore(weight=10)
        h.find_fitness()
        c.c_eat([h])
        assert c.weight == 10 * n + 20


def test_carnivore_no_food():
    """
    Tests that a carnivore will not prey on a herbivore of higher fitness by
    setting the weight of the carnivore to 0, to ensure a fitness of 0
    """
    c = Carnivore(weight=0)
    h = [Herbivore(10)]
    c.find_fitness()
    h[0].find_fitness()
    for _ in range(10):
        assert c.c_eat(h) == []


def test_carnivore_full(mocker):
    """Tests that a carnivore will not eat all herbivores on the tile when it has eaten F amount"""
    for _ in range(10):
        c = Carnivore(10)
        c.find_fitness()
        h = [Herbivore(10) for _ in range(10)]
        mocker.patch('random.random', return_value=0)
        assert len(c.c_eat(h)) == 5


def test_check_always_migrate(mocker):
    """
    Tests that an animal will always migrate when possibility of migrating is fitness*mu,
    in this case always 0.2. With mocker, the random migration threshold is always set to 0,
    which means the animal will always move.
    """
    h = Herbivore(5)
    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        assert h.check_migration()


def test_check_never_migrate(mocker):
    """
    Tests that an animal will always migrate when possibility of migrating is fitness*mu,
    in this case always 0.2. With mocker, the random migration threshold is always set to 1,
    which means the animal will never move.
    """
    h = Herbivore(5)
    mocker.patch('random.random', return_value=1)
    for _ in range(10):
        assert not h.check_migration()


@pytest.mark.parametrize('set_animal_parameters', [{'omega': 2}], indirect=True)
def test_animal_death_z_test(set_animal_parameters):
    """
    This test is a probabilistic test: It executes dies() N times.
    The number n of "successes" (dies() returns True) should be
    distributed according to the binomial distribution B(N, p),
    where p is short for p_death. For large N, the distribution
    is approximately normal (law of large numbers) with mean
    Np and variance Np(1-p).

    To obtain p_death, omega is set to 2, thus
    p_death = Herbivore.parameter['omega'] * (1 - h.fitness) will be 0.4, since an animal that is
    not part of the island simulation will have a default fitness of 0.8

    Then, Z = ( n - Np ) / sqrt( N p (1-p) ) is distributed according
    to the normal distribution with mean 0 and variance 1. Thus,
    if dies() works correctly, we will observe Z < -Z* or Z > Z* only
    with probability Phi(-Z*) + ( 1-Phi(Z*) ) = 2 * Phi(-Z*), where
    equality follows from the symmetry of the normal distribution.
    This is the probability mass in the tails of the distribution.

    We can choose a signficance level alpha, e.g. 0.01, and
    pass the test if 2*Phi(-|Z|) > alpha: The test passes if the
    probability mass outside (-|Z], |Z]) is at least alpha (the
    observed value of Z is not in the alpha-tail of the distribution).
    """
    alpha = 0.01
    random.seed()
    N = 100
    h = Herbivore(5)
    p = Herbivore.parameter['omega'] * (1 - h.fitness)  # obtain parameter set by fixture
    n = sum(h.check_death() for _ in range(N))  # True == 1, False == 0

    mean = N * p
    var = N * p * (1 - p)
    Z = (n - mean) / math.sqrt(var)
    phi = 2 * stats.norm.cdf(-abs(Z))
    assert phi > alpha
