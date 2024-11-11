class Baseline:
    def __init__(self, df, mass=44, start=0, stop=50):
        self._df = df
        self.mass = mass
        self.start = start
        self.stop = stop

    def remove_baseline(self):
        self._df[f"ion_current_M{self.mass}_UVS_ALS_sub_norm"] = (
            self._df[f"ion_current_M{self.mass}_UVS_ALS_sub"]
            - self._df[f"ion_current_M{self.mass}_UVS_ALS_sub"]
            .iloc[self.start : self.stop]
            .mean()
        )
        self._df[f"ion_current_M{self.mass}_norm"] = (
            self._df[f"ion_current_M{self.mass}"]
            - self._df[f"ion_current_M{self.mass}"].iloc[self.start : self.stop].mean()
        )

    def med_filter(self, filter_value=9):
        from scipy.signal import medfilt

        self._df[f"ion_current_M{self.mass}_UVS_ALS_sub_norm_filt"] = medfilt(
            self._df[f"ion_current_M{self.mass}_UVS_ALS_sub_norm"], filter_value
        )
        self._df[f"ion_current_M{self.mass}_UVS_ALS_sub_filt"] = medfilt(
            self._df[f"ion_current_M{self.mass}_UVS_ALS_sub"], filter_value
        )

    @property
    def df(self):
        self.remove_baseline()
        self.med_filter()

        return self._df

    def plot(self):
        import matplotlib.pyplot as plt

        fig1, [ax1, ax2] = plt.subplots(2, 1, figsize=(10, 5))
        ax1.plot(self.df["time"], self.df["current1_muA_geo"])
        ax1.plot(
            self.df["time"],
            -self.df[f"ion_current_M{self.mass}_UVS_ALS_sub"] * 500000000000,
            c="g",
        )  # BL subtracted curve
        ax1.plot(
            self.df["time"],
            -self.df[f"ion_current_M{self.mass}_norm"] * 500000000000,
            c="r",
        )
        ax1.plot(
            self.df["time"],
            -self.df[f"ion_current_M{self.mass}_UVS_ALS_sub_norm"] * 200000000000,
            c="purple",
        )  # BL subtracted curve
        ax1.plot(
            self.df["time"][self.start : self.stop],
            self.df["current1_muA_geo"][self.start : self.stop],
        )

        ax1.set_ylabel("j / $\mu$ A")

        ax2.plot(self.df["time"], self.df["potential"])
        ax2.set_xlabel("time / s")
        ax2.set_ylabel("U / V vs. RHE")
