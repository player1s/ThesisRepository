# Epoching based on events
"""
Created on Fri Nov  3 10:24:21 2023
@author: elpid



Segmentation of continuous data based on events array
    % data : continuous data
    % events : events array in the format (onset, duration, event id)
    
    
"""

import matplotlib.pyplot as plt
import pandas as pd
import pyxdf
import mne
import numpy as np


class Epoching:
    
    def _init_(
            self, 
            raw, 
            events, 
            event_id=None, 
            tmin=-0.2,
            tmax=0.5,
            baseline=(None,0),
            reject=None,    #create the reject criterion
            ):
        
        self.raw = raw
        self.events = events
        
    