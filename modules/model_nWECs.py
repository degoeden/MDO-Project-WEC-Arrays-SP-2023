import modules.Econ as Econ
import modules.hydro as hydro
from modules.wec_dyn import wec_dyn as wec_dyn
from modules.time_avg_power import time_avg_power as time_avg_power
from numpy import pi as pi
import numpy as np

# x = [radius all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]
