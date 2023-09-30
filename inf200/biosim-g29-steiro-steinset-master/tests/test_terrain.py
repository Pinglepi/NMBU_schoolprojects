# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.terrain import Lowland, Highland

seed = 123


def test_spawn_animal():
    """Tries to spawn 100 herbivores and tests if all spawned correctly"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(100)])
    assert terrain.count_herbivores() == 100


def test_eat_on_title_herbivore():
    """
    Make it so a tile cant support all the animals and
    makes sure that the right amount of animals get to eat
    """
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(100)])
    terrain.eat_on_tile()
    n_starving = 0
    for i in range(len(terrain.herbivores_on_tile)):
        if terrain.herbivores_on_tile[i].weight == 20:
            n_starving += 1
    assert n_starving == 100 - (terrain.F_max / terrain.herbivores_on_tile[0].parameter['F'])


def test_eat_on_tile_carnivore():
    """Makes it almost certain that one of the carnivores should be able to eat a herbivore and checks that their
    weight gain is corrent"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 500, 'weight': 1}])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 1, 'weight': 500} for _ in range(1000)])
    max_weight = 500
    num_weight = 0
    herb_weight = terrain.herbivores_on_tile[0].weight + terrain.herbivores_on_tile[0].parameter[
        'beta'] * terrain.herbivores_on_tile[0].parameter['F']
    carn_weight = terrain.carnivores_on_tile[0].weight
    terrain.eat_on_tile()
    for i in range(len(terrain.carnivores_on_tile)):
        if max_weight < terrain.carnivores_on_tile[i].weight:
            max_weight = terrain.carnivores_on_tile[i].weight
            num_weight += 1
    assert max_weight == terrain.carnivores_on_tile[0].parameter['beta'] * \
           herb_weight + carn_weight and num_weight == 1


def test_get_values():
    """Test if get_values return expected values"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 10},
                          {'species': 'Herbivore', 'age': 15, 'weight': 12}])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 5, 'weight': 15},
                          {'species': 'Carnivore', 'age': 10, 'weight': 5}])
    values_herb = terrain.get_values_herb()
    values_carn = terrain.get_values_carn()
    assert values_herb[0][0] == 5 and values_herb[2][1] == 12 and len(values_carn[1]) == 2


def test_migration():
    """
    Test if animals migrate to tiles they shouldn't, by giving lists of only illegal
    surrounding tiles for carnivores, and all legal surrounding tiles for herbivores. Test asserts
    that no carnivore migrates, and that herbivores migrate to all surrounding tiles."""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 1, 'weight': 500} for _ in range(200)])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 1, 'weight': 500} for _ in range(200)])
    migrating_carn = len(terrain.migration_carn([False, False, False, False])[0]) + len(
        terrain.migration_carn([False, False, False, False])[1]) + len(
        terrain.migration_carn([False, False, False, False])[2]) + len(
        terrain.migration_carn([False, False, False, False])[3])
    migrating_herb = len(terrain.migration_herb([True, True, True, True])[0]) + len(
        terrain.migration_herb([True, True, True, True])[1]) + len(
        terrain.migration_herb([True, True, True, True])[2]) + len(
        terrain.migration_herb([True, True, True, True])[3])
    assert migrating_carn == 0 and migrating_herb != 0


def test_breed_on_tile():
    """Give a large enough number of animals and ensure they have optimal fitness such that they
    are guaranteed to breed"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 2, 'weight': 500} for _ in range(300)])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 2, 'weight': 500} for _ in range(300)])
    terrain.breed_on_tile()
    assert len(terrain.herbivores_on_tile) == 600 and len(terrain.carnivores_on_tile) == 600


def test_die_on_tile_weight():
    """Checks if the animals die properly when their weight is set to 0"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 0} for _ in range(300)])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 5, 'weight': 0} for _ in range(300)])
    terrain.die_on_tile()
    assert len(terrain.herbivores_on_tile) == 0 and len(terrain.carnivores_on_tile) == 0


def test_age_on_tile():
    """Age all animals on the tile and checks individually if their ages has gone up by one"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 2, 'weight': 20}])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 4, 'weight': 20}])
    terrain.age_on_tile()
    assert terrain.herbivores_on_tile[0].age == 3 and terrain.carnivores_on_tile[0].age == 5


def test_count_animals():
    """Tests if the counting of animals returns the right amount"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 0} for _ in range(15)])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 5, 'weight': 0} for _ in range(12)])
    assert terrain.count_animals() == 15 + 12


def test_set_terrain_param():
    """Tests if setting the terrain parameter on one tile changes it on all similar, but not different"""
    terrain1 = Lowland()
    terrain2 = Lowland()
    terrain3 = Highland()
    terrain1.set_params({'f_max': 100})
    assert terrain2.F_max == 100 and terrain3.F_max != 100


def test_loose_weight_on_tile():
    """Tests if all animals on the given terrain loose weight when the lose weight function is called"""
    terrain = Lowland()
    terrain.spawn_animal([{'species': 'Herbivore', 'age': 5, 'weight': 10} for _ in range(15)])
    terrain.spawn_animal([{'species': 'Carnivore', 'age': 5, 'weight': 10} for _ in range(12)])
    terrain.lose_weight_on_tile()
    num_no_change = 0
    for i in terrain.herbivores_on_tile:
        if i.weight >= 10:
            num_no_change += 1
    for i in terrain.carnivores_on_tile:
        if i.weight >= 10:
            num_no_change += 1
    assert num_no_change == 0
