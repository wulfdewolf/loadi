import pynapple as nap
from .base import BaseSession
from pathlib import Path
import pandas as pd
import numpy as np
from .base import BaseExperiment
from importlib import resources
import json
import spikeinterface.full as si


class Clark2026Session(BaseSession):

    def __init__(self, mouse, day, session, known_data_types = None, containing_folder=None):
        self.mouse = mouse
        self.day = day
        self.session = session
        self.cache = {}
        self.known_data_types = known_data_types
        self.containing_folder = containing_folder

    def _repr_html_(self):

        header_text = f"<b>Mouse</b> {self.mouse}, <b>Date</b> {self.day}, <b>Session</b> {self.session}<br />"
        streams_text = f"{self.known_data_types}"

        return header_text + streams_text

    def load_units(self, output="pynapple") -> nap.TsGroup:
        return 

    def load_behaviour(self) -> nap.TsdFrame:
        return 
    
    def load_ephys(self):

        neuropixels_folder = self.containing_folder / 'Harry/EphysNeuropixelData'

        if 'OF' in self.session:
            typ_folder = neuropixels_folder / 'of'
        elif 'VR' in self.session:
            typ_folder = neuropixels_folder / 'vr'

        ephys_path = list(typ_folder.glob(f'M{self.mouse}_D{self.day}_*_{self.session}*'))[0]
        recording = si.read_openephys(ephys_path)

        return recording


class Clark2026Experiment(BaseExperiment):

    def __init__(
        self,
        active_projects_folder=None,
    ):
        if active_projects_folder is None:
            raise FileExistsError('Please provide the path to the ActiveProjects folder on the DataStore, using `active_projects_folder = "path/to/folder".')
        self.containing_folder = Path(active_projects_folder)

        with resources.files('loadi.resources.data_paths').joinpath('Clark_2026.json').open('r') as f:
            self.data_paths = json.load(f)

        self.session_class = Clark2026Session

    def get_session(self, mouse, day, session_type) -> Clark2026Session:

        mouse_dict = self.data_paths.get(mouse)
        if mouse_dict is None:
             raise ValueError(f"No mouse called {mouse}. Possible mice are {self.data_paths.keys()}.")
        else:
             day_dict = mouse_dict.get(day)
             if day_dict is None:
                 raise ValueError(f"No day called {day}. Possible days are {mouse_dict.keys()}.")
             else:
                  session_dict = day_dict.get(session_type)
                  if session_dict is None:
                      raise ValueError(f"No session_type called {session_type}. Possible session_types are {day_dict.keys()}.")
                  else:
                    return Clark2026Session(mouse, day, session_type, known_data_types=session_dict,containing_folder=self.containing_folder)

