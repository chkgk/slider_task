from otree.api import models, BasePlayer
from otree.db.models import Model, ForeignKey
from random import randint

class BaseSlider(Model):

    class Meta:
        abstract = True

    minimum = models.IntegerField(initial=0)
    maximum = models.IntegerField(initial=100)

    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    touched = models.BooleanField(initial=False)
    centered = models.BooleanField(initial=False)


    def set_starting_pos(self):
        self.start_pos = randint(self.minimum, self.maximum)

    def distance_from_center(self):
        return abs((self.minimum + self.maximum)/2 - int(self.end_pos))

    def is_centered(self):
        self.centered = self.distance_from_center() == 0
        return self.centered


class SliderPlayer(BasePlayer):

    class Meta:
        abstract = True

    centered_sliders = models.PositiveIntegerField()
    num_sliders = models.PositiveIntegerField()
    slider_min = models.IntegerField()
    slider_max = models.IntegerField()

    def prepare_sliders(self, num=50, min=0, max=100):
        self.num_sliders = num
        self.slider_min = min
        self.slider_max = max
        for _ in range(self.num_sliders):
            slider = self.slider_set.create()
            slider.minimum = self.slider_min
            slider.maximum = self.slider_max
            slider.set_starting_pos()
            slider.save()

    def count_centered_sliders(self):
        sum_of_centered = 0
        for s in self.slider_set.all():
            if s.touched and s.centered:
                sum_of_centered += 1
        self.centered_sliders = sum_of_centered