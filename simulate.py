from __init__ import *

atmos = atmosphere.ISA().get_atmosphere(0).get_payload()
rot = rotor.rotor('input_files/simple_rotor.json')
blade_inp = {'climb_vel': 0, 'atmosphere': atmos, 'collective': 6*3.14/180}
msg = message.simMessage()
t1 = time.time()
msg.add_payload(blade_inp)
res = rot.get_performance(msg).get_payload()

print(res['non_dims']['CT'])

t2 = time.time()
print(f'Time taken: {(t2-t1)*1000} ms')