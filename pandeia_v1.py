from pandeia.engine import perform_calculation
from pandeia.engine import calc_utils
import json
import matplotlib.pyplot as plt


with open('sw_f070w_rapid_full.json', 'r') as inf:
    calculation = json.loads(inf.read())

#calculation = calc_utils.build_default_calc("jwst","nircam","sw_imaging")

result = perform_calculation.perform_calculation(calculation)

print(result['scalar']['sn'])

plt.imshow(result['2d']['snr'])
plt.colorbar()
plt.show()