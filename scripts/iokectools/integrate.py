from functools import cached_property


class Integrate:
    def __init__(self, df):
        self._df = df

    @cached_property
    def df(self):
        r"""
        Returns a copy of the input Pandas DataFrame.
        """
        return self._df.copy()

    @classmethod
    def integrate(cls, df, xcol, ycol, absolute=False):
        r"""
        Returns the absolute value of the incremental integration of two columns of a Pandas Dataframe.
        In each step the integrated value can be positive or negative.
        For example, the total charge of a complete period of a sine wave is zero.

        The Absolute integration turns all negative values of the y-axis into positive values.
        Hence the charge will always increase.
        For example, the total charge of a complete period of a sine wave is four.

        In both cases identical values are obtained when the sine wave is negative (-sin(x)).
        """
        from scipy import integrate

        if absolute:
            return abs(integrate.cumtrapz(x=df[xcol], y=abs(df[ycol]), initial=0))
        return abs(integrate.cumtrapz(x=df[xcol], y=df[ycol], initial=0))

    def charge_j(self, start, stop):
        from scipy import integrate

        cvs = self.df[start:stop].copy()
        cvs = cvs.reset_index(drop=True)
        cvs["ChargeShort"] = abs(
            integrate.cumtrapz(x=cvs["time"], y=abs(cvs[self.current_]), initial=0)
        )
        return cvs

    def charge_m(self, start, stop):
        from scipy import integrate

        cvs = self.df[start:stop].copy()
        cvs = cvs.reset_index(drop=True)
        cvs[f"ChargeShort_M{mass}_norm"] = abs(
            integrate.cumtrapz(x=cvs["time"], y=cvs[self.ion_current], initial=0)
        )
        return cvs


class COIntegral(Integrate):
    def __init__(self, df, K, mass=44, cathodic_limit=0.5, j_sim_pos_max=1.1, limits=None):
        Integrate.__init__(self, df)
        self.K = K
        self.mass = mass
        self._limits = limits
        self.cathodic_limit = cathodic_limit
        self.ion_current = 'sim_current'
        self.current_density = 'current1_muA_geo'
        self.redox_CV_current = 'current_H_sub'
        # limits
        self.j_sim_pos_max = j_sim_pos_max

    @cached_property
    def limits(self):
        """Defines the limits for the integration regions.
        Provide an entry for each integration function within the class.

        It should be a dict of kind

        limits = {"Q cathodic": {upper: 1.1, lower: 0.2}, "Q_tot_M_neg": {lower: 0.2}}

        In case you want to integrate the entire potential region, simply choose a value beyond the vertex potentials:

        limits = {"Q cathodic": {upper: 100, lower: -100}}
        """
        # default limits
        # We need to add some value to the vertex limits from the df.
        # Otherwise the point at the vertex will not be considered during the integration process.
        def default_none():
            return {'upper': self.df['potential'].max() + 1, 'lower': self.df['potential'].min() - 1, 'current': None }

        _limits = {"Q_tot_j": default_none(),
                "Q_tot_j_pos": default_none(),
                "Q_tot_j_neg": default_none(),
                "Q_tot_M": default_none(),
                "Q_tot_M_pos": default_none(),
                "Q_tot_M_neg": default_none(),
                "Q cathodic": default_none(),
                "Q_tot_j_sim_pos": default_none(),
                "Q_tot_j_sim_neg": default_none(),
        }

        import copy

        provided_limits = copy.deepcopy(self._limits)

        # print(provided_limits)

        if provided_limits == None:
            print('no limits provided')
            return _limits

        for charge_name, _ in provided_limits.items():
            provided_limits[charge_name].setdefault('upper', None)
            provided_limits[charge_name].setdefault('lower', None)
            provided_limits[charge_name].setdefault('current', None)

        # update limits
        for charge_name, _ in provided_limits.items():
            if charge_name not in _limits.keys():
                raise Warning(f"Key `{charge_name} not part of the integration program.")
            else:

                for _key, _ in provided_limits[charge_name].items():
                    if provided_limits[charge_name][_key] is not None:
                        # _limits[charge_name][_key] = provided_limits[charge_name][_key]   #####
                        _limits[charge_name].update({_key: provided_limits[charge_name][_key]})   #####

        return _limits



    @staticmethod
    def charge_description(func):
        """A decorator, returning the dataframe and metadata from evaluated charges."""

        def inner(self):
            df, axis = func(self)
            return {"df": df, "total charge": df["Q_total"].iloc[-1], 'axis': axis}

        return inner

    @cached_property
    def vertex_point(self):
        return self.df[self.df["potential"] == self.df["potential"].max()].index.values[
            0
        ]

    @cached_property
    def vertex_potential(self):
        return self.df["potential"].max()

    @cached_property
    def df_pos(self):
        r"""
        Positive going scan.
        """
        return self.df[: self.vertex_point + 1]

    @cached_property
    def df_neg(self):
        r"""
        Negative going scan.
        """
        return self.df[self.vertex_point :].reset_index(drop=True)

    @cached_property
    @charge_description
    def charge_total_j(self):
        axis = self.current_density
        ipos2 = self.df["current1_muA_geo"] > 0
        U_limit_lower = self.df["potential"] > self.limits['Q_tot_j']['lower']
        df_j = self.df[ipos2 & U_limit_lower].copy()
        df_j["Q_total"] = self.integrate(df_j, "time", axis)
        return df_j, axis

    @cached_property
    @charge_description
    def charge_total_j_pos(self):
        axis = self.current_density
        ipos2 = self.df_pos["current1_muA_geo"] > 0
        U_limit_lower = self.df_pos["potential"] > self.limits['Q_tot_j_pos']['lower']
        df_j = self.df_pos[ipos2 & U_limit_lower].copy()
        df_j["Q_total"] = self.integrate(df_j, "time", axis)
        return df_j, axis

    @cached_property
    @charge_description
    def charge_total_j_neg(self):
        axis = self.current_density
        ipos2 = self.df_neg["current1_muA_geo"] > 0
        # U_limit_lower = self.df_neg["potential"] > 0.6
        # df_j = self.df_neg[ipos2 & U_limit_lower].copy()
        df_j = self.df_neg[ipos2].copy()
        df_j["Q_total"] = self.integrate(df_j, "time", axis)
        return df_j, axis

    @cached_property
    @charge_description
    def charge_total_j_cathodic(self):
        axis = self.current_density
        ipos2 = self.df_neg["current1_muA_geo"] < 0
        # U_limit_upper = self.df_neg["potential"] > self.cathodic_limit # old
        U_limit_upper = self.df_neg["potential"] > self.limits['Q cathodic']['lower']
        df_j = self.df_neg[ipos2 & U_limit_upper].copy()
        if len(df_j) == 0:
            df_j = self.df_neg[0:2].copy()
            df_j["Q_total"] = 0
            return df_j, axis

        df_j["Q_total"] = self.integrate(df_j, "time", axis, absolute=True)
        return df_j, axis

    @cached_property
    @charge_description
    def charge_total_M(self):
        axis = self.ion_current
        U_limit_lower = self.df["potential"] > self.limits['Q_tot_M']['lower']
        df_M = self.df[U_limit_lower].copy()
        df_M["Q_total"] = self.integrate(df_M, "time", axis)
        return df_M, axis

    @cached_property
    @charge_description
    def charge_total_M_pos(self):
        axis = self.ion_current
        U_limit_lower = self.df_pos["potential"] > self.limits['Q_tot_M_pos']['lower']
        df_M = self.df_pos[U_limit_lower].copy()
        df_M["Q_total"] = self.integrate(df_M, "time", axis)
        return df_M, axis

    @cached_property
    @charge_description
    def charge_total_M_neg(self):
        axis = self.ion_current
        U_limit_lower = self.df_neg["potential"] > self.limits['Q_tot_M_neg']['lower']
        df_M = self.df_neg[U_limit_lower].copy()
        df_M["Q_total"] = self.integrate(df_M, "time", axis)
        return df_M, axis

    @cached_property
    @charge_description
    def charge_total_j_sim_pos(self):
        axis = self.redox_CV_current
        # ipos2 = self.df_pos[axis] > 0
        U_limit_lower = self.df_pos["potential"] > self.limits['Q_tot_j_sim_pos']['lower']
        U_limit_upper = self.df_pos["potential"] < self.limits['Q_tot_j_sim_pos']['upper']
        # df_j = self.df_pos[ipos2 & U_limit_lower].copy()
        df_j = self.df_pos[U_limit_lower & U_limit_upper].copy()
        df_j["Q_total"] = self.integrate(df_j, "time", axis)
        return df_j, axis

    @cached_property
    @charge_description
    def charge_total_j_sim_neg(self):
        axis = self.redox_CV_current
        # ipos2 = self.df_neg[axis] < 0
        # ipos2 = self.df_neg[axis] < 0
        U_limit_lower = self.df_neg["potential"] > self.limits['Q_tot_j_sim_neg']['lower']
        U_limit_upper = self.df_neg["potential"] < self.limits['Q_tot_j_sim_neg']['upper']
        ipos2 = self.df_neg["current_H_sub"] < 0
        # df_j = self.df_neg[ipos2 & U_limit_lower].copy()
        df_j = self.df_neg[U_limit_lower & U_limit_upper & ipos2].copy()
        df_j["Q_total"] = self.integrate(df_j, "time", axis)
        return df_j, axis

    @cached_property
    def charges(self):
        charges = {"Q_tot_j": self.charge_total_j,
                "Q_tot_j_pos": self.charge_total_j_pos,
                "Q_tot_j_neg": self.charge_total_j_neg,
                "Q_tot_M": self.charge_total_M,
                "Q_tot_M_pos": self.charge_total_M_pos,
                "Q_tot_M_neg": self.charge_total_M_neg,
                "Q cathodic": self.charge_total_j_cathodic,
                "Q_tot_j_sim_pos": self.charge_total_j_sim_pos,
                "Q_tot_j_sim_neg": self.charge_total_j_sim_neg,
        }
        return charges

    def summary(self, round_values=None):
        diff_pos = (
            self.charge_total_j_pos["total charge"] - self.charge_total_M_pos["total charge"]
        )
        diff_neg = (
            self.charge_total_j_neg["total charge"] - self.charge_total_M_neg["total charge"]
        )

        summary = {
            "Q_tot_j": self.charge_total_j["total charge"],
            "Q_tot_M": self.charge_total_M["total charge"],
            "Q_tot_j - Q_tot_M": self.charge_total_j["total charge"]
            - self.charge_total_M["total charge"],
            "Q_tot_j_pos": self.charge_total_j_pos["total charge"],
            "Q_tot_M_pos": self.charge_total_M_pos["total charge"],
            "Q_diff_pos = Q_tot_j_pos - Q_tot_M_pos": diff_pos,
            "Q_tot_j_neg": self.charge_total_j_neg["total charge"],
            "Q_tot_M_neg": self.charge_total_M_neg["total charge"],
            "Q_diff_neg = Q_tot_j_neg - Q_tot_M_neg": diff_neg,
            "Q_diff_neg - Q cathodic": diff_neg - self.charge_total_j_cathodic["total charge"],
            "Q cathodic": self.charge_total_j_cathodic["total charge"],
            "Q_diff_pos - Q_diff_neg": diff_pos + diff_neg,
            "vertex potential": self.vertex_potential,
            "Q_tot_j_sim_pos": self.charge_total_j_sim_pos["total charge"],
            "Q_tot_j_sim_neg": self.charge_total_j_sim_neg["total charge"],
            "Q_tot_j_sim_neg + cathodic": self.charge_total_j_sim_neg["total charge"] + self.charge_total_j_cathodic["total charge"],
        }
        if not round_values:
            return summary

        return {key: round(item, round_values) for key, item in summary.items()}

    def plot(self, title=None):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 1, figsize=[6, 6])
        ax.axhline(0, color="k", linewidth=0.5, alpha=0.5)
        self.charge_total_M["df"].plot("potential", "current1_muA_geo", ax=ax)
        self.charge_total_M_pos["df"].plot("potential", "sim_current", ax=ax)
        self.charge_total_M_neg["df"].plot("potential", "sim_current", ax=ax)
        self.charge_total_j_cathodic["df"].plot(
            "potential", "current1_muA_geo", ax=ax
        )
        self.df.plot("potential", "current_H_sub", ax=ax, color="k")
        if title:
            plt.title(title)

        return fig
