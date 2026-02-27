import pynapple as nap
from .base import BaseSession
from pathlib import Path
import pandas as pd
import numpy as np
from .base import BaseExperiment
from importlib import resources
import json

class Vandrey2026Experiment(BaseExperiment):

    def __init__(
        self,
        active_projects_folder=None,
    ):
        if active_projects_folder is None:
            raise FileExistsError('Please provide the path to the ActiveProjects folder on the DataStore, using `active_projects_folder = "path/to/folder".')
        self.containing_folder = Path(active_projects_folder)

        with resources.files('loadi.resources.data_paths').joinpath('Vandrey_2026.json').open('r') as f:
            self.data_paths = json.load(f)
        with resources.files('loadi.resources.data_paths').joinpath('Vandrey_2026_file_paths.json').open('r') as f:
            self.file_map = json.load(f)

        self.session_class = Vandrey2026Session

    def get_session(self, mouse, day, session_type):

        mouse_dict = self.file_map.get(mouse)
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
                    return Vandrey2026Session(mouse, day, session_type, path_dict = session_dict, known_data_types=list(session_dict.keys()),containing_folder=self.containing_folder)

class Vandrey2026Session(BaseSession):

    def __init__(self, mouse, date, session, path_dict, known_data_types = None, containing_folder=None):
        self.mouse = mouse
        self.date = date
        self.session = session
        self.path_dict = path_dict
        self.cache = {}
        self.known_data_types = known_data_types
        self.containing_folder = containing_folder

    def _repr_html_(self):

        header_text = f"<b>Mouse</b> {self.mouse}, <b>Date</b> {self.date}, <b>Session</b> {self.session}<br />"
        streams_text = f"{self.known_data_types}"

        return header_text + streams_text

    def load_units(self) -> nap.TsGroup:

        if (clusters := self.cache.get('clusters')) is not None:
            return clusters

        cluster_path = self.path_dict.get('clusters')
        if cluster_path is None:
            return None
        
        clusters_df = pd.read_pickle(self.containing_folder / cluster_path)

        sampling_frequency = 30_000

        spikes_dict = dict(zip(clusters_df['cluster_id'].values, clusters_df['firing_times'].values))
        spikes_dict_s = {key: nap.Ts(t=value/sampling_frequency) for key, value in spikes_dict.items() if len(value) > 0}
        if len(spikes_dict_s) == 0:
            return None
        
        spikes_frame = nap.TsGroup(data=spikes_dict_s)

        self.cache['clusters'] = spikes_frame
        return spikes_frame

    def load_position(self) -> nap.TsdFrame:

        if (positions := self.cache.get('positions')) is not None:
            return positions

        behaviour_path = self.path_dict.get('position')
        if behaviour_path is None:
            return None
        
        position_df = pd.read_pickle(self.containing_folder / behaviour_path)

        position = nap.TsdFrame(position_df['synced_time'].values, np.transpose(np.array([position_df['position_x'].values, position_df['position_y'].values])), columns=["x", "y"])

        self.cache['positions'] = position
        return position
