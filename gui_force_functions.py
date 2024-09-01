import numpy as np
from flight_simulator import flight_dynamics

# Class to handle data generation
class SimulationData:
    def __init__(self):
        pass

    # Functions to generate forces data
    def generate_forces_x(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.force_x(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_forces_y(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.force_y(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_forces_z(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.force_y(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_forces_xyz(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        # Separate the components
        force_x = np.ones(100)*heli.force_x(collective_pitch,tail_rotor_collective)
        force_y = np.ones(100)*heli.force_y(collective_pitch,tail_rotor_collective)
        force_z = np.ones(100)*heli.force_z(collective_pitch,tail_rotor_collective)

        # Combine the individual components
        return x, force_x, force_y, force_z

    # Functions to generate moments data
    def generate_moments_x(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.moment_x(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_moments_y(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.moment_y(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_moments_z(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        y = np.ones(100)*heli.moment_z(collective_pitch,tail_rotor_collective)
        return x, y

    def generate_moments_xyz(self, collective_pitch, lateral_pitch, longitudinal_pitch, tail_rotor_collective):
        collective_pitch=collective_pitch*np.pi/180
        tail_rotor_collective=tail_rotor_collective*np.pi/180
        heli=flight_dynamics("input_files/helicopter.json")
        x = np.linspace(0, 10, 100)
        # Separate the components
        moment_x = np.ones(100)*heli.moment_x(collective_pitch,tail_rotor_collective)
        moment_y = np.ones(100)*heli.moment_y(collective_pitch,tail_rotor_collective)
        moment_z = np.ones(100)*heli.moment_z(collective_pitch,tail_rotor_collective)

        # Combine the individual components
        return x, moment_x, moment_y, moment_z
