# oTree Slider Task

An easy to configure, ready to use slider task for oTree.
This is a beta version, you can help to enhance it by submitting issues and pull requests.

## Installation
```bash
pip3 install slider_task
```

In `settings.py` add `slider_task` to `INSTALLED_APPS`
```python
INSTALLED_APPS = ['otree', 'slider_task']
```

For installing on your server, your `requirements_base.txt` should include `slider_task`.

## Integrating with your experiment
### `models.py`
Add these two import statements at the top:
```python
from otree.db.models import ForeignKey
from slider_task.models import BaseSlider, SliderPlayer
```

If you want to show your sliders in multiple columns, add `slider_columns` to your `Constants`
```python
class Constants(BaseConstants):
    slider_columns = 3
    # ...
```

Make sure your `Player` class inherits from `SliderPlayer`
```python
class Player(SliderPlayer):
    pass
```

Add the `Slider` class, which inherits from `BaseSlider`.
The foreign key assignemnt is required.
```python
class Slider(BaseSlider):
    player = ForeignKey(Player)
```

Finally, make sure to call `prepare_sliders()` for each player when creating the session.
Here you can also specify how many sliders you want to show to players as well as their minimum and maximum values which. (The defaults are num=50, min=0, max=100.)
```python
class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.prepare_sliders(num=20, min=0, max=4)
``` 

### `views.py`
Add these two import statements at the top:
```python
from .models import Slider
from slider_task.pages import SliderTaskPage
```

Let the page, which is supposed to show the slider task inherit from `SliderTaskPage` and assign the Constants and Slider objects. Don't forget to include it in the `page_sequence`.
```python
class Sliders(SliderTaskPage):
    Constants = Constants
    Slider = Slider
    # ...
page_sequence = [
    Sliders
]
```
