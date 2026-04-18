One day there will be a universally agreed Neuroscience data standard. Until then, there's `loadi`.

Install
-------

``` bash
git clone https://github.com/chrishalcow/loadi
cd loadi
```

Then install into your environment:

``` bash
pip install .
```

or run directly with `uv` from the loadi directory:

``` bash
uv run python
```

Use
---

Can be used to load data. E.g:

``` python
from loadi import NagelhusMoser2023Experiment
experiment = NagelhusMoser2023Experiment()

session = experiment.get_session('27207', 'CA3_12', 'object moved')

units = session.load_units()
positions = session.load_positions()

# Now that you've loadi'd the data, you can compute stuff
import pynapple as nap
tuning_curves = nap.compute_tuning_curves(
    data=units,
    features=position,
    bins=40,
)
```

Looping will loop through every session in the experiment

``` python
for session in experiment:
    if session.subject_id == '27207':
        print(session.load_subject_position())
```
