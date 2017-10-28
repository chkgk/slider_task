from otree.api import Page

# from .models import Constants, Slider
from django.forms import modelformset_factory
from math import ceil
from random import randint

class SliderTaskPage(Page):

    template_name = "slider_task/SliderTaskPage.html"

    Constants = None
    Slider = None

    def vars_for_template(self):

        SliderFormSet = modelformset_factory(self.Slider, fields=('end_pos', 'touched'), extra=0)

        def _chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]


        sliders_query_set = self.Slider.objects.filter(player__exact=self.player)
        # assert len(sliders_query_set) == Constants.num_sliders

        slider_formset = SliderFormSet(queryset=sliders_query_set)

        # starting_values = [s.start_pos for s in sliders_query_set]
        # min_values = [s.minimum for s in sliders_query_set]
        # max_values = [s.maximum for s in sliders_query_set]
        # offsets = [randint(0, 10) for _ in sliders_query_set]

        starting_values = []
        min_values = []
        max_values = []
        offsets = []
        for s in sliders_query_set:
            starting_values.append(s.start_pos)
            min_values.append(s.minimum)
            max_values.append(s.maximum)
            offsets.append(randint(0, 10))


        if hasattr(self.Constants, 'slider_columns'):
            if self.Constants.slider_columns > 0:
                slider_columns = self.Constants.slider_columns
        else:
            slider_columns = 1

        chunk_size = ceil(self.player.num_sliders / slider_columns)

        return {
            'slider_formset': slider_formset,
            'slider_values_and_forms': list(_chunks(list(zip(offsets, min_values, max_values, starting_values, slider_formset.forms)), chunk_size)),
            'slider_columns': slider_columns
        }

    def before_next_page(self):
        submitted_data = self.form.data
        slider_objs_by_id = {slider.pk: slider for slider in self.player.slider_set.all()}
        assert len(slider_objs_by_id) == self.player.num_sliders

        for i in range(self.player.num_sliders):
            input_prefix = 'form-%d-' % i

            slider_id = int(submitted_data[input_prefix + 'id'])
            end_pos = submitted_data[input_prefix + 'end_pos']
            touched = submitted_data[input_prefix + 'touched']

            slider = slider_objs_by_id[slider_id]
            slider.end_pos = end_pos
            slider.touched = True if touched == "True" else False
            slider.save()

            slider.is_centered()
            slider.save()

        self.player.count_centered_sliders()
