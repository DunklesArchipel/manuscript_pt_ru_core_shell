from functools import cached_property


class BatchIntegration:
    r"""
    K_modifier: allows varying the K pre-factor by a specified value.
    This is an absolute offset and is usually a float in the range of 0.05 to 0.2.
    """
    def __init__(self, experiment_description, cathodic_limit=0.5, interval=None, K_modifier=0, fixed_K=None, limits=None):
        self._input_experiment_description = experiment_description
        self.cathodic_limit = cathodic_limit
        self.K_modifier = K_modifier
        self.fixed_K = fixed_K
        self._limits = limits

        if interval == 0:
            self.interval = interval
            print('The interval was 0')
        else:
            self.interval = (
                interval
                or self._experiment_description.experiment_description["interval"]
                or 0
            )

    def cycle_info(self):
        pass

    @cached_property
    def _experiment_description(self):
        import copy
        return copy.deepcopy(self._input_experiment_description)

    @cached_property
    def charges(self):
        from .baseline import Baseline
        from .integrate import COIntegral
        from .timeshift import Timeshift

        cycle_description = self._experiment_description.cycle_description

        charges = {}
        for key in cycle_description:

            baseline = Baseline(cycle_description[key]["df"])

            K_prefactor = (self.fixed_K or cycle_description[key]["K_prefactor"]) + self.K_modifier
            K_power = cycle_description[key]["K_power"]

            timeshift = Timeshift(
                baseline.df,
                K_prefactor=K_prefactor,
                K_power=K_power,
                interval=self.interval,
            )

            charge = COIntegral(timeshift.df, K=timeshift.K, cathodic_limit=self.cathodic_limit, limits=self._limits)
            charges[key] = charge

        return charges

    @cached_property
    def cycle_description(self):
        r"""
        Returns a dict with charges evaluated from different potential regions for each cycle.
        """
        cycle_description = {}
        for key in self.charges:
            cycle_description[key] = {
                **self.charges[key].summary(),
                **self._experiment_description.cycle_description[key],
            }
            del cycle_description[key]["df"]

        return cycle_description

    @cached_property
    def experiment_description(self):
        experiment_description = self._experiment_description.experiment_description
        experiment_description["cycles"] = self.cycle_description
        return experiment_description

    def cycles(self):
        r"""
        Return a list of available cycles.
        """
        return list(
            self._experiment_description.experiment_description["cycles"].keys()
        )

    @cached_property
    def df(self):
        r"""
        Return a dataframe with charges evaluated from different potential regions for each cycle.
        """
        import pandas as pd

        return pd.DataFrame.from_dict(self.cycle_description, orient="index")

    def plot_charges(self):
        r"""
        Returns a plot of the eveluated charges.
        """
        import matplotlib.pyplot as plt

        y = [
            "Q_tot_j",
            "Q_tot_M",
            "Q_tot_M_pos",
            "Q_tot_j_pos",
            "Q_tot_j_neg",
            "Q_tot_M_neg",
            "Q cathodic",
        ]
        y2 = [
            "Q_tot_j - Q_tot_M",
            "Q_diff_pos = Q_tot_j_pos - Q_tot_M_pos",
            "Q_diff_neg = Q_tot_j_neg - Q_tot_M_neg",
            "Q_diff_pos - Q_diff_neg",
            "Q_diff_neg - Q cathodic",
            "Q_tot_j_sim_pos",
            "Q_tot_j_sim_neg",
        ]

        fig, [ax0, ax1] = plt.subplots(2, 1, figsize=[5, 10])
        for i in y:
            #     df.plot.scatter(x='vertex potential', y=i, ax=ax0)
            ax0.scatter(x=self.df["vertex potential"], y=self.df[i], label=i)
            ax0.legend()
        for i in y2:
            ax1.scatter(x=self.df["vertex potential"], y=self.df[i], label=i)
            ax1.legend()
            ax1.set_xlabel("Upper potential limit / V vs. RHE")
            ax0.set_ylabel("Q / uC cm-2")
            ax1.set_ylabel("Q / uC cm-2")

    def plot_curves(self, cycle=None):
        import matplotlib.pyplot as plt

        if not cycle:
            raise Exception("Provide a cycle number or set cycle to `all`.")
        if cycle == "all":
            for key, charge in self.charges.items():
                charge.plot(title=f"cycle {key}")

        else:
            return self.charges[cycle].plot(title=f"cycle {cycle}")
