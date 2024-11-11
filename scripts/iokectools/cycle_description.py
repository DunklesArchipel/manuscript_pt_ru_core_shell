from functools import cached_property


class CycleDescription:
    def __init__(self, experiment_description):
        self._experiment_description = experiment_description
        self._cycle_description = self._experiment_description["cycles"]
        self.datafolder = self._experiment_description["data folder"]
        self.experiment_name = self._experiment_description["experiment name"]

    @property
    def filenames(self):
        return [
            self.experiment_description["cycles"][key]["filename"]
            for key in self.experiment_description["cycles"]
        ]

    @cached_property
    def dfs(self):
        return [
            self.experiment_description["cycles"][key]["df"]
            for key in self.experiment_description["cycles"]
        ]

    def get_df(self, filename):
        from .workingfiles import WorkingFiles

        return WorkingFiles(self.datafolder, [filename]).create_concat_df()

    @cached_property
    def experiment_description(self):
        import copy
        experiment_description = copy.deepcopy(self._experiment_description)
        for key in experiment_description["cycles"]:
            filename = f"{self.experiment_name}{key}.csv"
            experiment_description["cycles"][key].setdefault("filename", filename)
            experiment_description["cycles"][key].setdefault("cycle", key)
            experiment_description["cycles"][key].setdefault(
                "df", self.get_df(filename)
            )

        return experiment_description

    @cached_property
    def cycle_description(self):
        return self.experiment_description["cycles"]

class ExperimentDescriptions:

    def __init__(self, exp_description, K_min, K_max, K_prefactor, K_increment=0.05):
        self._exp_description = exp_description
        self.K_min = K_min
        self.K_max = K_max
        self.K_increment = K_increment
        self.K_prefactor = K_prefactor

    @property
    def exp_description(self):
        import copy
        return copy.deepcopy(self._exp_description)

    @property
    def K_values(self):
        r"""
        Returns possible K values based on a minimumm and maximum K value,
        and in increment between the values.
        """
        import numpy as np
        return [round(K,2) for K in np.arange(self.K_min, self.K_max, self.K_increment)]

    @property
    def cycles(self):
        r"""
        Returns the available cycles in the data description that should be evaluated.
        """
        return list(self.exp_description['cycles'].keys())

    @property
    def cycles_min(self):
        r"""
        The lowest cycle number in the experimental description.
        """
        return min(self.cycles)

    @property
    def cycles_max(self):
        r"""
        The highers cycle number in the experimental description.
        """
        return max(self.cycles)

    def _cycle_K(self, K1, K2):
        r"""
        A dict defining the k values for the initial and final cycle.
        """
        return {'K_prefactor':[K1, K2], 'cycle':[self.cycles_min, self.cycles_max]}

    # @property
    # def _df_cycle_K(self):
    #     import pandas as pd
    #     return pd.DataFrame(self._cycle_K)

    @property
    def cycles_K(self):
        r"""
        Returns a list of cycles with initial and final K values,
        as well as the initial and final cycle number.
        """
        import pandas as pd

        cycles_K = {}
        n=0
        for _K_min in self.K_values:
            for _K_max in self.K_values:
                cycles_K.setdefault(n, {})
                _cycle_K = self._cycle_K(_K_min, _K_max)
                cycles_K[n] = _cycle_K
                #cycles_K[n]['df'] = pd.DataFrame(_cycle_K)
                n+=1
        return cycles_K

    def K_change(self):
        r"""
        Returns a list with K factors, which has the same length than the number of cycles,
        where each value of the list corresponds to the K factor of a specific cycle.
        """
        for key, item in self.cycles_K.items():
            item['K_prefactor']

    @property
    def dfs_cycles_K(self):
        import pandas as pd

        cycles_K = []

        for _K_min in self.K_values:
            for _K_max in self.K_values:
                # cycles_K.setdefault(n, {})
                # _cycle_K = self._cycle_K(_K_min, _K_max)
                # cycles_K[n] = _cycle_K
                cycles_K.append(pd.DataFrame(self._cycle_K(_K_min, _K_max)))
        return cycles_K

    def regression_stats_K(self, df):
        from scipy.stats import linregress
        return linregress(df['cycle'], df['K_prefactor'])

    def regression_K(self, regression):
        return [cycle*regression.slope + regression.intercept for cycle in self.cycles]

    @property
    def K_lines(self):
        K_lines = []
        for df in self.dfs_cycles_K:
            regression = self.regression_stats_K(df)
            K_lines.append(self.regression_K(regression))
        return K_lines

    @property
    def exp_descriptions(self):
        eds = []

        for K_line in self.K_lines:
            experiment = self.exp_description.copy()

            for idx, cycle in enumerate(self.cycles):
                experiment['cycles'][cycle]['K_prefactor'] = K_line[idx]

            eds.append(experiment)
            # exp = self.exp_description.copy()

        return eds

    @cached_property
    def eds(self):
        from .cycle_description import CycleDescription
        return [CycleDescription(ed) for ed in self.exp_descriptions]

    @property
    def plot_K_parameter_space(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1)
        for line in self.K_lines:
            ax.plot(self.cycles, line)

        ax.set_xlabel('cycle number')
        ax.set_ylabel('K prefactor')
        ax.set_title('K parameter space')
        plt.close(fig)
        return fig
