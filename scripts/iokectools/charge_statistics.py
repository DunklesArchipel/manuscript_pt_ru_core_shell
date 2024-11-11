from functools import cached_property


class charge_statistics:

    def __init__(self, experiment_descriptions, cathodic_limit=None,
                 time_shifts=[-0.3, -0.35, -0.4, -0.45], K_shifts=[-0.02, 0, 0.02], fixed_Ks=[],
                 vertex_limit_lower=None, vertex_limit_upper=None, test=False, limits=None):

        self.eds = [experiment_descriptions] if type(experiment_descriptions) != list else experiment_descriptions
        self.time_shifts = time_shifts
        self.K_shifts = K_shifts
        self.fixed_Ks = fixed_Ks
        self.cathodic_limit = cathodic_limit
        self._vertex_limit_lower = vertex_limit_lower
        self._vertex_limit_upper = vertex_limit_upper
        self.test = test
        self.limits = limits

    @property
    def vertex_limit_lower(self):
        return self._vertex_limit_lower or min(self.vertex_potentials)

    @property
    def vertex_limit_upper(self):
        return self._vertex_limit_upper or max(self.vertex_potentials)

    @classmethod
    def boundary_conditions(cls, overview):
        r"""
        A boolean indicating if the charges are within certain limits.
        """
        for cycle in overview.cycles():
            # print(cycle)
            if overview.charges[cycle].summary()['Q_diff_pos = Q_tot_j_pos - Q_tot_M_pos'] < 0:
                # print(overview.charges[cycle].summary()['Q_diff_pos = Q_tot_j_pos - Q_tot_M_pos'])
                print('rejected Q_diff_pos')
                return False
            if overview.charges[cycle].summary()['Q_tot_j - Q_tot_M'] < 0:
                print("rejected 'Q_tot_j - Q_tot_M'")
                return False

        return True

    @cached_property
    def overviews(self):
        from .batchintegration import BatchIntegration
        overviews = []
        print(len(self.eds))
        processed_eds = 0

        for ed in self.eds:
            # Remove EDs that do have K factors which do not yield results compliant with the boundary conditions.
            for time_shift in self.time_shifts:
                for K_shift in self.K_shifts:
                    if self.fixed_Ks:
                        for fixed_K in self.fixed_Ks:
                            overview = BatchIntegration(ed, cathodic_limit=self.cathodic_limit, interval=time_shift, K_modifier=K_shift, fixed_K=fixed_K, limits=self.limits)

                            # Test if the overview is with self.boundary_conditions(overview)
                            if self.test:
                                if self.boundary_conditions(overview):
                                    overviews.append(overview)
                                else:
                                    pass
                            else:
                                overviews.append(overview)
                    else:
                        overview = BatchIntegration(ed, cathodic_limit=self.cathodic_limit, interval=time_shift, K_modifier=K_shift, limits=self.limits)
                        if self.test:
                            if self.boundary_conditions(overview):
                                overviews.append(overview)
                            else:
                                pass
                        else:
                            overviews.append(BatchIntegration(ed, cathodic_limit=self.cathodic_limit, interval=time_shift, K_modifier=K_shift, limits=self.limits))
                        print('no fixed_K: ', processed_eds)
                    processed_eds +=1
        # print('processed edsprocessed eds: ', processed_eds)
        return overviews

    @classmethod
    def get_vertex(cls, vertex):
        r"""
        Test if a vertex potential is within a certain range and return the value in the center of that range.
        For example the vertex potential might be 1.01 or 0.99, which are both set to 1.0, since they are between 0.95 and 1.05.
        """
        vertex_regions = [round((0.725 + 0.05*n),3) for n in range(0,40,1)]
        vertex_potentials = [round((0.75 + 0.05*n),3) for n in range(0,40,1)]

        for idx, item in enumerate(vertex_regions):
            if len(vertex_regions) == idx:
                pass
            if vertex > vertex_regions[idx] and vertex < vertex_regions[idx+1]:
                return vertex_potentials[idx]

    @cached_property
    def data(self):
        import copy
        data = copy.deepcopy(self._data_dummy)

        n = 0
        cycles = []
        for overview in self.overviews:
            print('Processing overview number: ', n)
            for cycle in overview.cycles():
                data['vertex potential'].append(overview.charges[cycle].summary()['vertex potential'])
                # print('Processing overview number: ', n, ' - ADDING vertex')
                cycles.append(cycle)
                for item in data.keys():
                    if not item == 'vertex potential':
                        # print('Processing overview number: ', n, ' - ADDING charge summary')
                        data[item].append(overview.charges[cycle].summary()[item])
                        # print('Processing overview number: ', n, ' Next cycle')
            n +=1
        data['cycle'] = cycles
        return data

    @cached_property
    def _df(self):
        import pandas as pd

        df = pd.DataFrame(self.data)
        df = df.sort_values('vertex potential')
        return df

    @cached_property
    def df(self):
        df = self._df.copy()
        df['vertex potential'] = df['vertex potential'].apply(charge_statistics.get_vertex)#lambda x: charge_statistics.get_vertex(x))
        return df

    # vertex_limit = 1.40

    @property
    def vertex_potentials(self):
        return list(self.df.drop_duplicates(subset=['vertex potential']).copy()['vertex potential'].values)

    @cached_property
    def _data_dummy(self):
        return {item : [] for item in self.charge_indexes}

    @cached_property
    def data_short(self):
        import copy

        data_short = copy.deepcopy(self._data_dummy) #!

        for vertex_potential in self.vertex_potentials:
            if vertex_potential >= self.vertex_limit_lower and vertex_potential <= self.vertex_limit_upper:
                df_vertex = self.df[self.df['vertex potential'] == vertex_potential].copy()
                data_short['vertex potential'].append(vertex_potential)
                for item in data_short:
                    if not item == 'vertex potential':
                        mean_value = df_vertex[item].mean()

                        data_short[item].append(mean_value)

        return data_short

    @cached_property
    def df_short(self):
        import pandas as pd
        return pd.DataFrame(self.data_short)

    @cached_property
    def charge_indexes(self):
        if not self.overviews:
            raise Exception('No overview files evaluated.')

        cycle = self.overviews[0].cycles()[0]
        return list(self.overviews[0].charges[cycle].summary().keys())# if not item == 'vertex potential']

    def plot_short(self, index='Q_diff_pos = Q_tot_j_pos - Q_tot_M_pos', error=True):
        import matplotlib.pyplot as plt
        if index == 'all':
            for index in self.charge_indexes:
                self.plot_short(index=index)

        if index:
            fig, ax = plt.subplots(1,1)
            #self.df_short.plot.scatter('vertex potential', 'Q_tot_j')
            if error:
                ax.scatter(self.df['vertex potential'], self.df[index], alpha=0.2)
            ax.scatter(self.df_short['vertex potential'], self.df_short[index], color='red')
            ax.set_title(index)

    def plot(self):
        r"""
        Returns a plot of the eveluated average charges.
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
            ax0.scatter(x=self.df_short["vertex potential"], y=self.df_short[i], label=i)
            ax0.legend()
        for i in y2:
            ax1.scatter(x=self.df_short["vertex potential"], y=self.df_short[i], label=i)
            ax1.legend()
            ax1.set_xlabel("Upper potential limit / V vs. RHE")
            ax0.set_ylabel("Q / uC cm-2")
            ax1.set_ylabel("Q / uC cm-2")

        #plt.close(fig)

        return fig
