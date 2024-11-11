class Timeshift:
    def __init__(self, df, K_prefactor, K_power, interval=0, mass=44, ion_current=None):
        self._df = df
        self.interval = interval
        self.K_prefactor = K_prefactor
        self.K_power = K_power
        self.K = self.K_prefactor * self.K_power
        self.mass = mass
        self.ion_current = ion_current or f"ion_current_M{self.mass}_UVS_ALS_sub_norm_filt"

    @property
    def dfj(self):
        r"""
        A dataframe with the electrochemical data, sliced from the original dataframe.
        """
        dfj = (
            self._df[["time", "potential", "current1_muA_geo"]].copy().set_index("time")
        )
        return dfj

    @property
    def dfm(self):
        r"""
        A dataframe with the MSCV data sliced from the original dataframe,
        where the time axis is shifted by the value of the input parameter `interval'.
        """
        dfm = self._df[["time", self.ion_current]].copy()
        dfm["time2"] = dfm["time"] - self.interval
        dfm2 = dfm[["time2", self.ion_current]].copy().set_index("time2")
        return dfm2

    @property
    def df(self):
        r"""
        A combined dataframe of the sliced dataframes `dfj` and `dfm`,
        where the time axis is shifted by the value
        of the input parameter `interval'.
        """
        # there seems to be an issue with the indexes, when using `pd.concat' to combine the dataframes.
        # dfnew = pd.concat([self.dfj, self.dfm], axis=1).dropna(axis=0, how="any").reset_index(drop=True)
        dfnew = self.dfj.join(self.dfm).dropna(axis=0, how="any")
        dfnew["time"] = dfnew.index
        dfnew["sim_current"] = (
            dfnew[f"ion_current_M{self.mass}_UVS_ALS_sub_norm_filt"] / self.K * 1000000
        )
        dfnew["current_H_sub"] = dfnew["current1_muA_geo"] - dfnew["sim_current"]
        dfnew = dfnew.reset_index(drop=True)
        return dfnew

    def plot(self, filename="unknown"):
        import matplotlib.pyplot as plt

        fig2, ax = plt.subplots(1, 1, figsize=(6, 6))
        # plt.close(fig2)
        ax.clear()

        fig2.patch.set_facecolor("white")

        ax.scatter(
            self.df["potential"], self.df["sim_current"], c="r", marker=".", s=20
        )
        ax.plot(self.df["potential"], self.df["sim_current"], c="b")

        ax.plot(self.df["potential"], self.df["current1_muA_geo"], c="orange")
        ax.plot(self.df["potential"], self.df["current_H_sub"], c="g")
        ax.hlines(0, -0.4, 1.4, linestyle="--", color="black")
        ax.set_xlabel("U / V vs. RHE")
        ax.set_ylabel("j / $\mu$ A$\cdot$ cm$^{-1}$")
        # plt.ylim(-160,60)
        ax.legend([filename])
        #plt.close(fig2)
        return fig2

    def interactive(self):
        from IPython.display import clear_output
        from ipywidgets import (HBox, Layout, Output, VBox, interact,
                                interactive, interactive_output, widgets)

        def interactive_integrate(interval, K_prefactor):
            # This might be an odd approach, but we store a timeshift object modified with the interactive widget,
            # within the original timeshift object. This allows us to extract the modified values.
            self.ts = Timeshift(
                df=self._df,
                K_prefactor=K_prefactor,
                K_power=self.K_power,
                interval=interval,
            )
            with out:
                self.ts.plot()
            with out2:
                clear_output(wait=True)
                print("K factor: ", self.ts.K)

        out = widgets.Output()
        out2 = widgets.Output()

        t_slider = widgets.FloatSlider(
            min=-2,
            max=2,
            step=0.05,
            value=self.interval,
            description="time adjust",
            layout=Layout(width="75%"),
            continuous_update=False,
        )
        K_slider = widgets.FloatSlider(
            description="K pre. fac.",
            min=0,
            max=10,
            step=0.001,
            value=self.K_prefactor,
            layout=Layout(width="75%"),
            continuous_update=False,
        )  # , value=0, title="Integration start",

        ui1 = widgets.VBox([t_slider, K_slider, out, out2])

        w = interactive_output(
            interactive_integrate,
            {
                "interval": t_slider,
                "K_prefactor": K_slider,
            },
        )

        display(ui1, w)
