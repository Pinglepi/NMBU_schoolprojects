# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

import subprocess
import matplotlib.pyplot as plt

_FFMPEG_BINARY = 'ffmpeg'


class Graphics:
    """Responsible for creating all the graphics"""

    def __init__(self, island_map, herb_map, carn_map, age_map, fitness_map, weight_map, hist_specs,
                 animal_count_history, img_base, img_fmt, ymax_animals=None, cmax_animals=None,
                 num_years=None):
        """Updates the graphics with the new values from the simulation.

            :param island_map: A list of list containing all the terrain objects
            :param herb_map: A list of list containing the number of herbivores on each coordinate.
            :param carn_map: A list of list containing the number of carnivores on each coordinate.
            :param age_map: A list of the ages of all the animals on the island
            :param fitness_map: A list of all the fitness values of all the animals on the island.
            :param weight_map: a list of all the weights of all the animals on the island.
            :param animal_count_history: A dictionary where every year is a key containing a list with the population of
             all
             herbivores and carnivores on the island.
            :param hist_specs: A dictionary of dictionaries, where the various histogram attributes can be keys.
             These keys contain a new dictionary with the keys max and delta for deciding the way the hisograms look.
            :param img_base: The location of where the pictures should be stored
            :param img_fmt: The kind of image should be stored, eg. png
            :param ymax_animals: Sets a maximum value for the y values shown on the graph, default gives automatic
             adjustments.
            :param cmax_animals: A dictionary with species as key, contains the max values for the distribution map

                """
        self._image_base = img_base
        self._image_fmt = img_fmt
        self._img_no = 0

        hist_specs = self.update_histogram_specs(hist_specs)
        self.f_bins = int(hist_specs['fitness']['max'] / hist_specs['fitness']['delta'])
        self.a_bins = int(hist_specs['age']['max'] / hist_specs['age']['delta'])
        self.w_bins = int(hist_specs['weight']['max'] / hist_specs['weight']['delta'])
        self.f_max = hist_specs['fitness']['max']
        self.a_max = hist_specs['age']['max']
        self.w_max = hist_specs['weight']['max']
        self.ymax_animals = ymax_animals
        if not cmax_animals:
            self.cmax_animals = {'Herbivore': 200, 'Carnivore': 50}
        else:
            self.cmax_animals = cmax_animals

        # normal subplots
        self.fig = plt.figure()
        self.fig.suptitle('Rossumøya')
        self.fig.set_size_inches(10, 10)

        # axes for herb_map
        self.ax2 = self.fig.add_subplot(3, 3, 4)
        self.herbs = self.ax2.imshow(herb_map, vmin=0, vmax=self.cmax_animals['Herbivore'])
        self.fig.colorbar(self.herbs, ax=self.ax2, shrink=0.5)
        self.ax2.set_title('Herbivore Density')

        # axes for carn_map
        self.ax3 = self.fig.add_subplot(3, 3, 6)
        self.carns = self.ax3.imshow(carn_map, vmin=0, vmax=self.cmax_animals['Carnivore'])
        self.fig.colorbar(self.carns, ax=self.ax3, shrink=0.5)
        self.ax3.set_title('Carnivore Density')

        # axes for map
        ax1 = self.fig.add_subplot(3, 3, 5)

        map_rgb = self.get_map(island_map)
        ax1.imshow(map_rgb)
        ax1.axis('off')

        # axes for age map
        self.ax4 = self.fig.add_subplot(3, 3, 7)
        self.ax4.hist(age_map, histtype='step', bins=self.a_bins, range=(0, self.a_max))
        self.ax4.set_title('Age distribution')
        self.ax4.legend(['Carnivores', 'Herbivores'])

        # axes for fitness map
        self.ax5 = self.fig.add_subplot(3, 3, 8)
        self.ax5.hist(fitness_map, histtype='step', bins=self.f_bins, range=(0, self.f_max))
        self.ax5.set_title('Fitness distribution')
        self.ax5.legend(['Carnivores', 'Herbivores'])

        # axes for weight map
        self.ax6 = self.fig.add_subplot(3, 3, 9)
        self.ax6.hist(weight_map, histtype='step', bins=self.w_bins, range=(0, self.w_max))
        self.ax6.set_title('Weight distribution')
        self.ax6.legend(['Carnivores', 'Herbivores'])

        # axes for animal_count
        self.ax7 = self.fig.add_subplot(3, 3, 1)
        self.ax7.set_xlim([0, num_years])
        self.ax7.set_ylim([0, self.ymax_animals])
        self.ax7.plot((animal_count_history.keys()), animal_count_history.values())
        self.ax7.set_title('Number of animals')
        self.ax7.legend(['Herbivores', 'Carnivores'])

        axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])
        axt.axis('off')

        template = 'Year: {:5}'
        self.year = axt.text(0.5, 0.5, template.format(0),
                             horizontalalignment='center',
                             verticalalignment='center',
                             transform=axt.transAxes)
        plt.draw()
        self.save()
        plt.pause(1e-6)

    def update_graphics(self, year, herb_map, carn_map, age_map, fitness_map, weight_map,
                        animal_count_history,
                        vis_years, img_years):
        """Updates the graphics with the new values from the simulation.

        :param year: The current year of the island
        :param herb_map: A list of list containing the number of herbivores on each coordinate.
        :param carn_map: A list of list containing the number of carnivores on each coordinate.
        :param age_map: A list of the ages of all the animals on the island
        :param fitness_map: A list of all the fitness values of all the animals on the island.
        :param weight_map: a list of all the weights of all the animals on the island.
        :param animal_count_history: A dictionary where every year is a key containing a
            list with the population of all herbivores and carnivores on the island.
        :param vis_years: How often the graphic should be updated.
        :param img_years: How often an image of island should be saved.
        """
        if year % vis_years == 0:
            self.year.set_text("Year: %d" % year)
            self.update_herb_map(herb_map)
            self.update_carn_map(carn_map)
            self.update_age_map(age_map)
            self.update_fitness_map(fitness_map)
            self.update_weight_map(weight_map)
            self.update_num_animals(animal_count_history)
            plt.draw()
            if year % img_years == 0:
                self.save()
        plt.pause(1e-6)

    def save(self):
        """Save the graphic as an image"""
        if self._image_base is not None or self._image_fmt is not None:
            plt.savefig('{}_{:05d}.{}'.format(self._image_base, self._img_no, self._image_fmt))
            self._img_no += 1

    @staticmethod
    def update_histogram_specs(new_hist_specs):
        """Helps the initialization assign proper specs for the histograms

        :param new_hist_specs: Changes to the histogram specifications.

        :return hist_specs: The final, complete histogram specifications"""
        hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                      'age': {'max': 60.0, 'delta': 2},
                      'weight': {'max': 60, 'delta': 2}}
        if new_hist_specs is not None:
            for key in new_hist_specs:
                hist_specs[key] = new_hist_specs[key]
            return hist_specs
        else:
            return hist_specs

    def make_movie(self):
        """
        Sees trough all the images at a given location and makes
        an mp4 movie of them called output.mp4
        """
        try:
            # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
            # section "Compatibility"
            subprocess.check_call([_FFMPEG_BINARY,
                                   '-i', '{}_%05d.png'.format(self._image_base),
                                   '-y',
                                   '-profile:v', 'baseline',
                                   '-level', '3.0',
                                   '-pix_fmt', 'yuv420p',
                                   '{}.{}'.format(self._image_base, 'output.mp4')])
        except subprocess.CalledProcessError as err:
            raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))

    def update_herb_map(self, herb_map):
        """Updates the herbivore density map"""
        self.herbs.set_data(herb_map)

    def update_carn_map(self, carn_map):
        """Updates the carnivore density map"""
        self.carns.set_data(carn_map)

    def update_age_map(self, age_map):
        """Updates the age distribution histogram"""
        self.ax4.cla()
        self.ax4.hist(age_map, histtype='step', bins=self.a_bins, range=(0, self.a_max))
        self.ax4.set_title('Age distribution')
        self.ax4.legend(['Carnivores', 'Herbivores'])

    def update_fitness_map(self, fitness_map):
        """Updates the fitness distribution histogram"""
        self.ax5.cla()
        self.ax5.hist(fitness_map, histtype='step', bins=self.f_bins, range=(0, self.f_max))
        self.ax5.set_title('Fitness distribution')
        self.ax5.legend(['Carnivores', 'Herbivores'])

    def update_weight_map(self, weight_map):
        """Updates the weight distribution histogram"""
        self.ax6.cla()
        self.ax6.hist(weight_map, histtype='step', bins=self.w_bins, range=(0, self.w_max))
        self.ax6.set_title('Weight distribution')
        self.ax6.legend(['Carnivores', 'Herbivores'])

    def update_num_animals(self, animal_count_history):
        """Updates the population counter"""
        self.ax7.cla()
        self.ax7.plot(animal_count_history.keys(), animal_count_history.values())
        self.ax7.set_title('Number of animals')
        self.ax7.set_ylim([0, self.ymax_animals])
        self.ax7.legend(['Herbivores', 'Carnivores'])

    @staticmethod
    def get_map(uncolored_map):
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in uncolored_map.splitlines()]
        return map_rgb
