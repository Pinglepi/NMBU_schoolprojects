# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.island import Island
import textwrap
import pytest
from biosim import terrain

"""
Properties of an island are given under, to make a temporary island that 
most tests will be carried out on.
"""
geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WLLHW
           WWWWW
           """
geogr = textwrap.dedent(geogr)

SEED = 124

ini_herbs = [{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 10}
                      for _ in range(5)]}]
ini_carns = [{'loc': (3, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 50}
                      for _ in range(5)]}]

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
        request.param is the parameter list containing string of species and dictionary of
        parameters to be changed, which is passed to Animal.set_animal_parameters()
    """
    if len(request.param[0]) == 2:
        species1 = request.param[0][0]
        p_dict1 = request.param[1][0]
        species2 = request.param[0][1]
        p_dict2 = request.param[1][1]
        Island.change_parameter(species1, p_dict1)
        Island.change_parameter(species2, p_dict2)
    else:
        species = request.param[0]
        p_dict = request.param[1]
        Island.change_parameter(species, p_dict)
    yield
    Island.change_parameter('Herbivore', herbivore_parameter)
    Island.change_parameter('Carnivore', carnivore_parameter)


@pytest.mark.parametrize('set_animal_parameters', [['Herbivore', {'zeta': 0}]], indirect=True)
def test_change_animal_parameter(set_animal_parameters):
    """
    Tests that parameters are changed correctly for the correct species, and that an error is
    raised when the wrong species is given. Parametrization is called to ensure that the
    parameters are reset to appropriate values after testing.
    """
    island = Island(geogr, SEED, ini_herbs)
    island.change_parameter('Herbivore', {'zeta': 100, 'xi': 2.5})
    with pytest.raises(ValueError):
        island.change_parameter('Insect', {'zeta': 10})
    assert 100 == island.island[2][2].herbivores_on_tile[0].parameter['zeta']


def test_change_landscape_parameter():
    """
    Tests that landscape parameters are changed correctly for highland and lowland, and that
    the set_params function raises a valueError for illegal landscape types. The amount of fodder
    on the island is not reset after testing, since the other tests will function
    with the new values as well.
    """
    island = Island(geogr, SEED)
    with pytest.raises(ValueError):
        island.set_params('S', {'f_max': 50})
    island.set_params('H', {'f_max': 50})
    island.set_params('L', {'f_max': 1000})
    island.set_params('D', {'f_max': 1})
    assert 50 == terrain.Highland.F_max and 1000 == terrain.Lowland.F_max and \
           terrain.Desert.F_max == 1


@pytest.mark.parametrize('bad_boundary', ['L', 'H', 'D'])
def test_check_valid_boundaries(bad_boundary):
    """ Tests that boundaries that are not water raises error, both for top and sides of the map"""
    with pytest.raises(ValueError):
        Island(island_text="{}WW\nWLW\nWWW".format(bad_boundary), seed=SEED)
    with pytest.raises(ValueError):
        Island(island_text="WWW\n{}LW\nWWW".format(bad_boundary), seed=SEED)


def test_check_valid_terrain():
    """Tests that illegal terrain types raises an error"""
    with pytest.raises(ValueError):
        Island(island_text="WWW\nWSW\nWWW", seed=SEED)


def test_consistent_lines_map():
    """Tests that inconsistent line lengths raises an error"""
    with pytest.raises(ValueError):
        Island(island_text="WWWW\nWSW\nWWW", seed=SEED)


def test_spawn_animal():
    """
    Test that animals are added to the island when spawn_animals is used.
    An island is initiated with the list of herbivores set on the top, and the same list is added
    in a for loop. The number of animals on the island should increase by the same number every time
    the list of animals is spawned on the island.
    """
    island = Island(geogr, SEED, ini_herbs)
    for n in range(10):
        island.spawn_animal(ini_herbs)
        maps = island.get_maps()
        assert maps[5]+maps[6] == len(ini_herbs[0]['pop']) + \
               (n+1)*len(ini_herbs[0]['pop'])


@pytest.mark.parametrize('set_animal_parameters', [[['Herbivore', 'Carnivore'],
                                                    [{'omega': 0, 'beta': 1},
                                                     {'omega': 0, 'DeltaPhiMax': 0.1,
                                                      'F': 80, 'beta': 1}]]], indirect=True)
def test_all_eat(set_animal_parameters):
    """ Checks if all animals on the island eats by checking if the list of the weights of all
    animals on the island has increased after all_eat is called. The DeltaPhiMAx is set to a very
    small number to ensure that the carnivores will prey on the herbivores. There will only be one
    carnivore, and properties of herbivores and carnivores are set in a way that ensures that the
    carnivore will prey on 4 of the 5 herbivores on the tile. """
    for _ in range(10):
        island = Island(geogr, SEED, ini_herbs)

        island.spawn_animal([{'loc': (3, 3),
                              'pop': [{'species': 'Carnivore',
                                                  'age': 5,
                                                  'weight': 50}]}])
        island.all_die()  # Updates the fitness of all animals

        weight_list = island.get_maps()[4]
        island.all_eat()
        weight_list_updated = island.get_maps()[4]
        assert weight_list_updated[0][0] > weight_list[0][0] \
               and weight_list_updated[1][0] > weight_list[1][0]


def test_all_lose_weight():
    """
    Checks if all animals on the island lose weight by checking that the list of the weights of all
    animals on the island has decreased after all_lose_weights is called.
    """
    island = Island(geogr, SEED, ini_herbs)
    island.spawn_animal(ini_carns)
    for _ in range(10):
        weight_list = island.get_maps()[4]
        island.all_lose_weight()
        for h in range(len(island.get_maps()[4][0])):
            assert island.get_maps()[4][0][h] < weight_list[0][h]
        for c in range(len(island.get_maps()[4][1])):
            assert island.get_maps()[4][1][c] < weight_list[1][c]


def test_all_age():
    """
    Checks if all animals on the island age one year by checking that the list of the ages of all
    animals on the island has increased after all_lose_weights is called.
    """
    island = Island(geogr, SEED, ini_herbs)
    island.spawn_animal(ini_carns)
    for n in range(10):
        island.all_age()
        age_list = island.get_maps()[2]
        assert age_list == [len(age_list[0])*[6+n], len(age_list[1])*[6+n]]


def test_all_certain_death():
    """
    Checks if all animals on the island die if weight of all spawned animals is set to 0.
    """
    dying_herbs = [{'loc': (2, 2),
                    'pop': [{'species': 'Herbivore',
                             'age': 0,
                             'weight': 0}
                            for _ in range(5)]}]
    dying_carns = [{'loc': (2, 2),
                    'pop': [{'species': 'Carnivore',
                             'age': 0,
                             'weight': 0}
                            for _ in range(5)]}]
    island = Island(geogr, SEED)
    for n in range(10):
        island.spawn_animal(dying_carns)
        island.spawn_animal(dying_herbs)
        island.all_die()
        assert island.get_maps()[5] == 0 and island.get_maps()[6] == 0


@pytest.mark.parametrize('set_animal_parameters', [[['Herbivore', 'Carnivore'],
                                                    [{'omega': 0, 'gamma': 10, 'zeta': 0.1,
                                                      'w_birth': 2, 'sigma_birth': 0.5},
                                                     {'omega': 0, 'gamma': 10, 'zeta': 0.1,
                                                      'w_birth': 2, 'sigma_birth': 0.5}]]],
                         indirect=True)
def test_all_breed(set_animal_parameters):
    """
    Checks that the breeding function works properly by setting the breeding parameters to optimal
    values, and check that the population of the island doubles when all_breed is called.
    """
    island = Island(geogr, SEED)
    island.spawn_animal(ini_carns)
    island.spawn_animal(ini_herbs)
    herbivores = island.get_maps()[5]
    carnivores = island.get_maps()[6]
    island.all_breed()
    assert island.get_maps()[5] == herbivores*2 and island.get_maps()[6] == carnivores*2


@pytest.mark.parametrize('set_animal_parameters', [[['Herbivore', 'Carnivore'],
                                                    [{'mu': 10}, {'mu': 10}]]], indirect=True)
def test_all_migrate(set_animal_parameters, mocker):
    """
    Checks that there are no animals on the tile where they are spawned after calling
    all_migrate_herb, while mu (migration parameter) is set to 10 to ensure migration. By using
    mocker, the direction of migration will be set to up every time, and the test therefore
    asserts wether all animals have moved one tile up.
    """
    for _ in range(10):
        island = Island(geogr, SEED)
        island.spawn_animal(ini_herbs)
        island.spawn_animal(ini_carns)
        mocker.patch('random.randrange', return_value=0)
        island.all_migrate()
        assert len(island.island[1][2].herbivores_on_tile) == 5 and \
               len(island.island[1][2].carnivores_on_tile) == 5


def test_get_maps():
    """
    Tests that all maps given by the get_maps function are correct when spawning a known
    number of animals on the island, all with known properties.
    The get_maps function returns the following list:
    [herbivores_map, carnivores_map, age_list, fitness_list, weight_list, num_herb, num_carn].
    """
    island = Island(geogr, SEED)
    island.spawn_animal(ini_carns)
    island.spawn_animal(ini_herbs)
    for _ in range(10):
        maps = island.get_maps()
        assert maps == [[[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 5, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]],
                        [[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 5, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]],
                        [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
                        [[0.8, 0.8, 0.8, 0.8, 0.8], [0.8, 0.8, 0.8, 0.8, 0.8]],
                        [[10, 10, 10, 10, 10], [50, 50, 50, 50, 50]], 5, 5]
