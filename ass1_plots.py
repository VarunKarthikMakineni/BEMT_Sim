# Blades stall at 192 kg wet weight at 2000 m above sea level
# 
from __init__ import *
import flight_simulator

class plots:
    def endurance_vs_weight(input):
        weights=np.linspace(80,190,10)
        endurance=[]
        for i in weights:
            heli=flight_simulator.mission_planner(input,True,i)
            endurance.append(heli.main().payload["Time"][-1])
        plt.plot(weights,np.array(endurance)/3600)
        plt.xlabel("Weight (kg)")
        plt.ylabel("Endurance (hrs)")
        plt.title("Endurance vs Initial Wet Weight")
        plt.show()

    def fuel_rate_vs_weight(input):
        heli=flight_simulator.mission_planner(input)
        output=heli.main()
        output.payload["Fuel_burn_rate"].append(output.payload["Fuel_burn_rate"][-1])
        plt.scatter(output.payload["Mass"],np.array(output.payload["Fuel_burn_rate"])*3600)
        plt.xlabel("Weight (kgf)")
        plt.ylabel("Fuel burn rate (kg/hr)")
        plt.title("Fuel burn rate vs Weight")
        plt.show()

plots.fuel_rate_vs_weight("input_files/helicopter_for_endurance.json")