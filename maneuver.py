from __init__ import *

class maneuver:
        
    def __init__(self, maneuver_params):
        
        self.parameters = maneuver_params
        self.altitude = self.parameters["altitude"]
        self.atmosphere = atmosphere.ISA(self.parameters["temp_dev_isa"])
        self.headwind = self.parameters["headwind"]
        self.crosswind = self.parameters["crosswind"]
        self.climb_vel = self.parameters["climb_vel"]
        self.rotor_input = self.atmosphere + message.simMessage(payload={'headwind':self.headwind, 'crosswind':self.crosswind, 'climb_vel':self.climb_vel})

### For now this class doesn't account for wind conditions or unwanted effects of tail rotor. Should be added later
class hover(maneuver):

    def get_fuel_burn_rate(self, vehicle_state):

        # Calculate the power consumed by the main rotor to match the weight of the vehicle
        vehicle_parameters_main_rotor = message.simMessage(payload={'mass':vehicle_state['mass'], 'desired_thrust': vehicle_state['mass']*g}) # For passing to the rotor
        main_rotor_performance = vehicle_state['main_rotor'].set_thrust(self.rotor_input + vehicle_parameters_main_rotor).get_payload()

        # Calculate the thrust required by the tail rotor to match the torque of the main rotor
        # !!! In the future, offload this to the fbd class ////////////////////////////
        tail_rotor_thrust = main_rotor_performance['torque'] / (vehicle_state['fbd'].get_tr_position()[0] - vehicle_state['fbd'].get_cg_position()[0])
        # /////////////////////////////////////////////////////////////////////////////

        # Calculate the power consumed by the tail rotor to match the torque of the main rotor
        vehicle_parameters_tail_rotor = message.simMessage(payload={'mass':vehicle_state['mass'], 'desired_thrust': tail_rotor_thrust})
        tail_rotor_performance = vehicle_state['tail_rotor'].set_thrust(self.rotor_input + vehicle_parameters_tail_rotor).get_payload()

        # Calculate fuel consumption rate for both rotors
        power_required = main_rotor_performance['power'] + tail_rotor_performance['power']
        fuel_burn_rate_parameters = message.simMessage(payload={'power_required':power_required,
                                                                'altitude':self.parameters['altitude'],
                                                                'temp_dev_isa':self.parameters['temp_dev_isa']})
        fuel_burn_rate = vehicle_state['powerplant'].get_fuel_rate(fuel_burn_rate_parameters)
        
        # Return the fuel burn rate
        response = message.simMessage()
        response.add_payload({'power_required':power_required})
        response = response + fuel_burn_rate

        return response


def create_maneuvers(maneuver_params):

    for man in maneuver_params:

        if man['type'] == 'hover':
            return hover(man)
        
        # elif man['type'] == 'climb':
        #     return climb(man)
            