from __init__ import *
import simulate
import matplotlib.pyplot as plt

##########################################################################
Thrust=np.zeros((4,6))
Power=np.zeros((4,6))
blades=np.array([2,3,4,5,6,7])

with open('input_files/simple_rotor.json', 'r') as file: 
    data = json.load(file)

with open('input_files/simple_rotor.json', 'r') as file: 
    data1 = json.load(file)

for number_of_blades in range(2,8):
    data['number_of_blades'] = number_of_blades
    with open('input_files/simple_rotor.json', 'w') as file: 
        json.dump(data, file) 
    for collective in range(2,18,5):
        result=simulate.simulator(collective)
        Thrust[int((collective-2)/5)][number_of_blades-2]= result['thrust']
        Power[int((collective-2)/5)][number_of_blades-2]= result['power']

with open('input_files/simple_rotor.json', 'w') as file: 
        json.dump(data1, file)


plt.plot(blades,Thrust[0],'--o',label='${theta}$= $2^o$')
plt.plot(blades,Thrust[1],'--o',label='${theta}$= $7^o$')
plt.plot(blades,Thrust[2],'--o',label='${theta}$= $12^o$')
plt.plot(blades,Thrust[3],'--o',label='${theta}$= $17^o$')
plt.title("Thrust vs Number of Blades")
plt.xlabel("Number of blades")
plt.ylabel("Thrust")
plt.legend()
plt.grid()
plt.show()

plt.plot(blades,Power[0],'--o',label='${theta}$= $2^o$')
plt.plot(blades,Power[1],'--o',label='${theta}$= $7^o$')
plt.plot(blades,Power[2],'--o',label='${theta}$= $12^o$')
plt.plot(blades,Power[3],'--o',label='${theta}$= $17^o$')
plt.title("Power vs Number of Blades")
plt.xlabel("Number of blades")
plt.ylabel("Power")
plt.legend()
plt.grid()
plt.show()

################################################################################

with open('input_files/simple_blade.json', 'r') as file: 
    data = json.load(file)

with open('input_files/simple_blade.json', 'r') as file: 
    data1 = json.load(file)

Thrust=np.zeros((4,5))
Power=np.zeros((4,5))
taper_ratio=np.array([1,0.8,0.6,0.4,0.2])

for i in range(5):
    data["chord"] = [0.0508,taper_ratio[i]*0.0508]
    with open('input_files/simple_blade.json', 'w') as file: 
        json.dump(data, file) 
    for collective in range(2,18,5):
        result=simulate.simulator(collective)
        Thrust[int((collective-2)/5)][i]= result['thrust']
        Power[int((collective-2)/5)][i]= result['power']

with open('input_files/simple_blade.json', 'w') as file: 
        json.dump(data1, file)

plt.plot(taper_ratio,Thrust[0],'--o',label='${theta}$= $2^o$')
plt.plot(taper_ratio,Thrust[1],'--o',label='${theta}$= $7^o$')
plt.plot(taper_ratio,Thrust[2],'--o',label='${theta}$= $12^o$')
plt.plot(taper_ratio,Thrust[3],'--o',label='${theta}$= $17^o$')
plt.title("Thrust vs Taper ratio")
plt.xlabel("Taper Ratio")
plt.ylabel("Thrust")
plt.legend()
plt.grid()
plt.show()

plt.plot(taper_ratio,Power[0],'--o',label='${theta}$= $2^o$')
plt.plot(taper_ratio,Power[1],'--o',label='${theta}$= $7^o$')
plt.plot(taper_ratio,Power[2],'--o',label='${theta}$= $12^o$')
plt.plot(taper_ratio,Power[3],'--o',label='${theta}$= $17^o$')
plt.title("Power vs Taper ratio")
plt.xlabel("Taper ratio")
plt.ylabel("Power")
plt.legend()
plt.grid()
plt.show()

####################################################################

with open('input_files/simple_blade.json', 'r') as file: 
    data = json.load(file)

with open('input_files/simple_blade.json', 'r') as file: 
    data1 = json.load(file)

with open('input_files/simple_rotor.json', 'r') as file: 
    data2 = json.load(file)

with open('input_files/simple_rotor.json', 'r') as file: 
    data3 = json.load(file)

#print(data)

Thrust=np.zeros((4,6))
Power=np.zeros((4,6))
twist=np.array([20.0,17.0,14.0,11.0,8.0,5.0])
twist=twist*(np.pi/180)

for i in range(6):
    data['twist'] = [twist[i],0]
    with open('input_files/simple_blade.json', 'w') as file: 
        json.dump(data, file) 
    for N in range(2,6):
        data2['number_of_blades'] = N
        with open('input_files/simple_rotor.json', 'w') as file: 
            json.dump(data2, file) 
        result=simulate.simulator(3)
        Thrust[N-2][i]= result['thrust']
        Power[N-2][i]= result['power']

with open('input_files/simple_blade.json', 'w') as file: 
        json.dump(data1, file)

with open('input_files/simple_rotor.json', 'w') as file: 
        json.dump(data3, file)

plt.plot(twist*180/np.pi,Thrust[0],'--o',label='N=2')
plt.plot(twist*180/np.pi,Thrust[1],'--o',label='N=3')
plt.plot(twist*180/np.pi,Thrust[2],'--o',label='N=4')
plt.plot(twist*180/np.pi,Thrust[3],'--o',label='N=5')
plt.title("Thrust vs Twist")
plt.xlabel("Twist")
plt.ylabel("Thrust")
plt.legend()
plt.grid()
plt.show()

plt.plot(twist*180/np.pi,Power[0],'--o',label='N=2')
plt.plot(twist*180/np.pi,Power[1],'--o',label='N=3')
plt.plot(twist*180/np.pi,Power[2],'--o',label='N=4')
plt.plot(twist*180/np.pi,Power[3],'--o',label='N=5')
plt.title("Power vs Twist")
plt.xlabel("Twist")
plt.ylabel("Power")
plt.legend()
plt.grid()
plt.show()