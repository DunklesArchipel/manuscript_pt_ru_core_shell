# parameters such as evaluated cycles, timeshifts (interval) and calibration factors K
# for different measurements

data_folder = r'..\data'

# parameters for the 1.0 ML Pt measurements
experiment_description_1 = {
    'date' : ' 2019-03-19',
    'data folder' : data_folder,
    'interval' : -0.4, # Add this value after experimenting with the BatchIntegrator, minimum -0.3, max -0.5
    'experiment name' : '20190319_DEMS_CV_STMV-100-ML_Ru0001_E_H2SO4_DEMS_COox004_pn_c_',
    'cycles': {
         # Cycles up to 10 do not yeald useful results
         # this is probably because the vertex potential is wihin the region of surface oxidation
         # and thus surface oxidation also occurs in the negative scan
         # it is unclear how to handle this effect in an automated way.
         # Especially since the calibration factor cannot be determined.
         # 101: {'K_prefactor': 1.14, 'K_power': 1E-6},
         # 102: {'K_prefactor': 1.14, 'K_power': 1E-6}, # not working
         # 103: {'K_prefactor': 1.14, 'K_power': 1E-6}, # 0.93
         # 104: {'K_prefactor': 1.00, 'K_power': 1E-6}, # 0.95
         # 105: {'K_prefactor': 1.17, 'K_power': 1E-6}, # 1.06
         # 106: {'K_prefactor': 1.14, 'K_power': 1E-6},
         107: {'K_prefactor': 1.14, 'K_power': 1E-6}, # from here # 1.14
         108: {'K_prefactor': 1.33, 'K_power': 1E-6}, # 1.31
         109: {'K_prefactor': 1.34, 'K_power': 1E-6}, # 1.30
         110: {'K_prefactor': 1.33, 'K_power': 1E-6}, # 1.34
         111: {'K_prefactor': 1.32, 'K_power': 1E-6}, # 1.31
         112: {'K_prefactor': 1.33, 'K_power': 1E-6}, # 1.333
         113: {'K_prefactor': 1.32, 'K_power': 1E-6}, # 1.315
         114: {'K_prefactor': 1.31, 'K_power': 1E-6},
         115: {'K_prefactor': 1.31, 'K_power': 1E-6},
         116: {'K_prefactor': 1.30, 'K_power': 1E-6},
         117: {'K_prefactor': 1.29, 'K_power': 1E-6},
         118: {'K_prefactor': 1.29, 'K_power': 1E-6},
         119: {'K_prefactor': 1.29, 'K_power': 1E-6},
         120: {'K_prefactor': 1.275, 'K_power': 1E-6},
         # # 121: {'K_prefactor': 1.25, 'K_power': 1E-6}, # raus
              }
}

integration_limits_1ML = {"Q_tot_j": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_pos": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_neg": {'current': 'positive'},
                "Q_tot_M": {'lower': 0.5},
                "Q_tot_M_pos": {'lower': 0.5},
                "Q_tot_M_neg": {'lower': 0.4}, #  only usefule for noisy data
                "Q cathodic": {'upper': None, 'lower': 0.2, 'current': 'negative'},
                "Q_tot_j_sim_pos": {'upper': 1.05, 'lower': 0.6, 'current': 'positive'}, # upper 1.35 for 2 ML
                "Q_tot_j_sim_neg": {'upper': 1.05, 'lower': 0.3, 'current': 'negative'}, # 2ML: lower should be None
        }

# parameters for the 2.2 ML Pt measurements
experiment_description_2 = {
    'date' : ' 2019-04-11',
    'data folder' : data_folder,
    'interval' : 0.2, # Add this value after experimenting with the BatchIntegrator
    'experiment name' : '20190411_DEMS_CV_STMV-200-ML_Ru0001_E_H2SO4_DEMS_COox003_pn_c_',
    'cycles': {
         # In a preceeding experiment the electrode restructured.
         # This is apparent from a COOR peak before the actual increase of the COOR.
         # Cycles up to 10 do not yield useful results
         # this is probably because the vertex potential is wihin the region of surface oxidation
         # and thus surface oxidation also occurs in the negative scan
         # it is unclear how to handle this effect in an automated way.
         # Especially since the calibration factor cannot be determined.
         # 7: {'K_prefactor': 1.4, 'K_power': 1E-6},
         # 8: {'K_prefactor': 0.12, 'K_power': 1E-6},
         # 9: {'K_prefactor': 0.20, 'K_power': 1E-6},
         # 10: {'K_prefactor': 0.15, 'K_power': 1E-6}, # Cycles <=10 are not meaningful, possible they have another timeshift.
         11: {'K_prefactor': 0.126, 'K_power': 1E-6},
         12: {'K_prefactor': 0.115, 'K_power': 1E-6},
         13: {'K_prefactor': 0.11, 'K_power': 1E-6},
         14: {'K_prefactor': 0.104, 'K_power': 1E-6},
         15: {'K_prefactor': 0.175, 'K_power': 1E-6},
         16: {'K_prefactor': 0.229, 'K_power': 1E-6},
         17: {'K_prefactor': 0.257, 'K_power': 1E-6},
         18: {'K_prefactor': 0.38, 'K_power': 1E-6},
         19: {'K_prefactor': 0.48, 'K_power': 1E-6}, #high voltages
         20: {'K_prefactor': 0.58, 'K_power': 1E-6}, # ok until here
         21: {'K_prefactor': 0.6, 'K_power': 1E-6},
         22: {'K_prefactor': 0.65, 'K_power': 1E-6},
         23: {'K_prefactor': 0.67, 'K_power': 1E-6},
         24: {'K_prefactor': 0.7, 'K_power': 1E-6},
         25: {'K_prefactor': 0.762, 'K_power': 1E-6},
         26: {'K_prefactor': 0.82, 'K_power': 1E-6},
         27: {'K_prefactor': 0.872, 'K_power': 1E-6},
         28: {'K_prefactor': 0.955, 'K_power': 1E-6}, # from here TODO
         29: {'K_prefactor': 1.0, 'K_power': 1E-6},
         30: {'K_prefactor': 1.03, 'K_power': 1E-6},
         35: {'K_prefactor': 1.044, 'K_power': 1E-6},
         40: {'K_prefactor': 0.93, 'K_power': 1E-6},
         50: {'K_prefactor': 0.483, 'K_power': 1E-6},
         60: {'K_prefactor': 0.516, 'K_power': 1E-6},
         62: {'K_prefactor': 0.516, 'K_power': 1E-6}, # last cycle
              }
}

integration_limits_2ML = {"Q_tot_j": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_pos": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_neg": {'current': 'positive'},
                "Q_tot_M": {'lower': 0.5},
                "Q_tot_M_pos": {'lower': 0.5},
                "Q_tot_M_neg": {'lower': 0.3}, #  only usefule for noisy data
                "Q cathodic": {'current': 'negative'},
                "Q_tot_j_sim_pos": {'upper': 1.35, 'lower': 0.6, 'current': 'positive'}, # upper 1.35 for 2 ML
                "Q_tot_j_sim_neg": {'upper': 1.1, 'current': 'negative'}, # 2ML: lowe should be None
        }

# parameters for the 3.5 ML Pt measurements
experiment_description_3 = {
    'date' : ' 2019-03-28',
    'data folder' : data_folder,
    'interval' : -0.4, # Add this value after experimenting with the BatchIntegrator
    'experiment name' : '20190328_DEMS_CV_STMV-330-ML_Ru0001_B_H2SO4_DEMS_COox001_pn_c_',
    'cycles': {
         # Cycles up to 104 do not yeald useful results
         # this is probably because the vertex potential is wihin the region of surface oxidation
         # and thus surface oxidation also occurs in the negative scan
         # it is unclear how to handle this effect in an automated way.
         # Especially since the calibration factor cannot be determined.
         # # 91: {'K_prefactor': 1.15, 'K_power': 1E-7}, # TODO
         # 96: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 97: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 98: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 99: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 100: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 102: {'K_prefactor': 1.15, 'K_power': 1E-7}, # 10 mV / s
         # 103: {'K_prefactor': 1.15, 'K_power': 1E-7},
         # 104: {'K_prefactor': 1.15, 'K_power': 1E-7}, # from here ok
         105: {'K_prefactor': 1.15, 'K_power': 1E-7},
         106: {'K_prefactor': 1.15, 'K_power': 1E-7}, # from here
         107: {'K_prefactor': 1.15, 'K_power': 1E-7}, # 1.15 # 1.50
         108: {'K_prefactor': 2.30, 'K_power': 1E-7}, # 2.30 # 2.70 # eventually a bubble in the system
         109: {'K_prefactor': 1.22, 'K_power': 1E-7}, # 1.22 # 1.45
         110: {'K_prefactor': 1.03, 'K_power': 1E-7}, # 1.03 # 1.20
         111: {'K_prefactor': 1.02, 'K_power': 1E-7}, # 1.02 # 1.20
         112: {'K_prefactor': 0.975, 'K_power': 1E-7}, # 0.975 # 1.15
         113: {'K_prefactor': 0.915, 'K_power': 1E-7}, # 0.95 # 1.12
         114: {'K_prefactor': 0.93, 'K_power': 1E-7}, # 0.93 # 1.10
         115: {'K_prefactor': 0.865, 'K_power': 1E-7},
         116: {'K_prefactor': 0.905, 'K_power': 1E-7},
         117: {'K_prefactor': 0.865, 'K_power': 1E-7},
         118: {'K_prefactor': 0.805, 'K_power': 1E-7},
         119: {'K_prefactor': 0.86, 'K_power': 1E-7},
         # # 120: {'K_prefactor': None, 'K_power': None} # Strong changes in flow conditions
              }
}


integration_limits_35ML = {"Q_tot_j": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_pos": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_neg": {'current': 'positive'},
                "Q_tot_M": {'lower': 0.5},
                "Q_tot_M_pos": {'lower': 0.5},
                "Q_tot_M_neg": {'lower': 0.3}, #  only usefule for noisy data
                "Q cathodic": {'upper': None, 'lower': 0.2, 'current': 'negative'},
                "Q_tot_j_sim_pos": {'upper': 1.15, 'lower': 0.6, 'current': 'positive'}, # upper 1.35 for 2 ML
                "Q_tot_j_sim_neg": {'upper': 1.0, 'lower': 0.3, 'current': 'negative'}, # 2ML: lower should be None
        }



#### DEFAULTS
integration_limits_default = {"Q_tot_j": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_pos": {'lower': 0.5, 'current': 'positive'},
                "Q_tot_j_neg": {'current': 'positive'},
                "Q_tot_M": {'lower': 0.5},
                "Q_tot_M_pos": {'lower': 0.5},
                "Q_tot_M_neg": {'lower': 0.3}, #  only usefule for noisy data
                "Q cathodic": {'upper': None, 'lower': 0.2, 'current': 'negative'},
                "Q_tot_j_sim_pos": {'upper': 1.1, 'lower': 0.6, 'current': 'positive'}, # upper 1.35 for 2 ML
                "Q_tot_j_sim_neg": {'upper': 1.1, 'lower': 0.3, 'current': 'negative'}, # 2ML: lower should be None
        }
