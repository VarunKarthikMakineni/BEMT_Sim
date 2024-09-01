from __init__ import *

    
def simulator(collective):
    atmos = {'temperature': 15, 'pressure': 101325, 'density': 1.225}
    rot = rotor.rotor('input_files/simple_rotor.json')
    blade_inp = {'climb_vel': 0, 'atmosphere': atmos, 'collective': collective*3.14/180}
    msg = message.simMessage()
    t1 = time.time()
    msg.add_payload(blade_inp)
    response=rot.get_performance(msg).get_payload()
    #print(rot.get_performance(msg).get_payload())
    t2 = time.time()
    print(f'Time taken: {(t2-t1)*1000} ms')
    return response
