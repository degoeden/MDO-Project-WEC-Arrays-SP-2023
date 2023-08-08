import numpy as np

# new econ mod ? heck yeah

def run(size,Power):
    nWEC = len(Power)
    c_vol = 1500                        # [$/m^3] cost of WEC per unit volume (taken from pelamis WEC specs)
    rWEC = size
    wec_vol = (4/3)*np.pi*(rWEC**3)     # volume of each WEC
    cWEC = c_vol*wec_vol*nWEC           # total capital cost of all WECs
    c_moor = 150000*nWEC                # cost of mooring all WECs
    c_install = 750000*nWEC             # installation costs for all WECs
    c_ship = 75000*nWEC                 # shipping cost of each WEC
    capex = cWEC + c_moor + c_install + c_ship    # total capital expenses
    

    t = 25                              # lifetime [years]
    capex = capex/t
    main = 40000*nWEC                   # annual maintenance 
    refit = 40000*nWEC/t                # mid-life refit cost normalized to per yer
    decomish = 500000/t                 # decomissioning cost normalized to per year
    opex = main + refit + decomish      # annual operational expenses
    
    # CW = 0.3                            # capture width (aka WEC efficiency)
    n_avail = 0.95                        # available wave power
    n_trans = 0.945                        # transmission line efficiency
    
    P = np.sum(Power)
    #print(f'Power is: {P/1e6} MW')
    AEP = P*n_avail*n_trans                           # annual energy production
    
    FCR = 0.108                          # fixed charge rate (value for wind)
    LCOE = ((FCR*capex) + opex)/AEP     # levelized cost of energy
    #print('da LCOE',LCOE)
    return AEP, LCOE
