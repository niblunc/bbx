import os, glob
import pandas as pd

class BBXQC:
    def __init__(self, study_path):
        self.tudy_path=study_path

    def setup_dict(self):
        