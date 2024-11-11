import os

import numpy as np
import pandas as pd


class WorkingFiles:
    """Based on a specific workingdirectory containing all files (folder) and the names of files of interest
    this class creates a list of files with full path which can be processed with several sub functions"""

    def __init__(self, folder, files, endswith=".csv", sample_diameter=0.7):
        self.folder = folder
        self.endswith = endswith
        self.folderfiles = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(self.folder)
            for file in files
            if file.endswith(self.endswith)
        ]
        if not type(files) == list:
            raise Exception(f"files must be a list and not {type(files)}")
        self.files = files
        self.filesfullpath = [
            file for item in self.files for file in self.folderfiles if item in file
        ]
        self._df_list = [pd.read_csv(file) for file in self.filesfullpath]
        self.df_concat = "Can be created with create_concat_df()"
        self.diameter = sample_diameter

    def list_colnames(self):
        self.colnames = list(self.df_list[0])  # .sort()
        self.colnames.sort()
        return self.colnames

    @property
    def df_list(self):
        _df_list_new = []
        for df in self._df_list:
            _df_list_new.append(self.modify_df(df))

        return _df_list_new

    def modify_df(self, df):
        r"""
        Modifies a Dataframe by adding additional axis,
        such as the current density.
        """
        df["current1_muA_geo"] = df["current1_muA"] / (
            np.pi * (self.diameter / 2) ** 2
        )

        return df

    def create_concat_df(self):
        r"""
        Returns a single pandas Dataframe, from all selected files.
        """
        if len(self.files) == 1:
            self.df_concat = self.df_list[0]
            return self.df_concat

        if len(self.files) > 1:

            self.df_concat = pd.DataFrame()

            for _, df in enumerate(self.df_list):
                self.df_concat = pd.concat([self.df_concat, df]).reset_index(drop=True)

            return self.df_concat

    def plot(self, x_axis='potential', y_axis="current1_muA_geo"):
        r"""
        Returns a current density vs potential plot.
        The x and y-axis can be set manually.
        """
        return self.df_concat.plot(x_axis, y_axis)


# To Do
# * list_colnames: fetch all collnames from all df and remove duplicate
