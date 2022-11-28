import pandas as pd
import logging
import numpy as np
import pickle
import modules.constants


class Cleaning:
    def __init__(self, data):
        self.data = data
        pass

    def convert_to_float(self):
        for col in self.data:
            if self.data[col].dtype != "string":
                continue
            try:
                self.data[col] = self.data[col].astype("float")
            except ValueError as e:
                logging.exception(f"{col}: e")
