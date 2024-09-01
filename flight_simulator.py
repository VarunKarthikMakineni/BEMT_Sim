from __init__ import *

class flight_dynamics:
    
    def __init__(self, helicopter_file_path):
        self.helicopter_data_file=helicopter_file_path
        with open(self.helicopter_data_file) as file:
                self.raw_data = json.load(file)
        #print(self.raw_data)
        self.main_rotor=rotor.rotor(self.raw_data['rotor_file_path'])
        self.tail_rotor=rotor.rotor(self.raw_data['tail_rotor_file_path'])
        self.rotor_collective=0
        self.tail_collective=0
        self.current_altitude=0
        self.xmrcg=self.raw_data["xmrcg"]
        self.xtrcg=self.raw_data["xtrcg"]
        self.zmrcg=self.raw_data["zmrcg"]
        self.ztrcg=self.raw_data["ztrcg"]
 
 

    def force_z(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return main_rotor.payload['thrust']

    def force_y(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return tail_rotor.payload['thrust']

    def force_x(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return 0
    
    def moment_z(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return main_rotor.payload['torque']-tail_rotor.payload["thrust"]*self.xtrcg

    def moment_x(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return 0

    def moment_y(self,main_rotor_collective,tail_rotor_collective,climb_vel=0,altitude=0):
        self.climb_vel=climb_vel
        self.current_altitude=altitude
        self.rotor_collective=main_rotor_collective
        self.tail_collective=tail_rotor_collective
        main_rotor,tail_rotor=self.main()
        return -tail_rotor.payload['torque']-self.xmrcg*main_rotor.payload['thrust']    
    
    def hover(self,collectives,climb_vel,altitude,fz,mz):
        return self.force_z(collectives[0],collectives[1],climb_vel,altitude)-fz, self.moment_z(collectives[0],collectives[1],climb_vel,altitude)-mz


    def main(self):
        control_message=message.simMessage()
        atm=atmosphere.ISA()
        self.engine=powerplant.powerplant()
        control_message.add_payload({"atmosphere":atm.get_atmosphere(self.current_altitude).payload})
        control_message.add_payload({"temp_dev_isa": 0})
        control_message.add_payload({"climb_vel": self.climb_vel})
        control_message_main_rotor=control_message
        control_message_main_rotor.add_payload({'collective':self.rotor_collective})
        main_rotor_results=self.main_rotor.get_performance(control_message_main_rotor)
        #print(control_message_main_rotor.payload)
        control_message_tail_rotor=control_message
        control_message_tail_rotor.add_payload({'collective':self.tail_collective})
        tail_rotor_results=self.tail_rotor.get_performance(control_message_tail_rotor)
        #print(control_message_tail_rotor.payload['collective'])
        return main_rotor_results,tail_rotor_results


    
#heli=flight_dynamics("input_files/helicopter.json")
#print(heli.force_z(12/180*pi,0.1))

class mission_planner:

    def __init__(self, helicopter_file_path,override_weight=False,new_gross_weight=0):
        self.helicopter_data_file=helicopter_file_path
        with open(self.helicopter_data_file) as file:
                self.raw_data = json.load(file)
        self.heli=flight_dynamics(helicopter_file_path)
        self.dry_mass=self.raw_data['dry_mass']
        self.engine_efficiency=self.raw_data["engine_efficiency"]
        self.initial_fuel_mass=self.raw_data["initial_fuel_mass"]
        self.fuel_mass=[self.raw_data["initial_fuel_mass"]]
        self.payload_mass=self.raw_data["payload_mass"]
        self.times=self.raw_data["times"]
        self.altitudes=self.raw_data["altitudes"]
        self.current_altitude=[self.altitudes[0]]
        self.climb_vel=[]
        self.current_time=[0]
        self.current_mass=[self.dry_mass+self.initial_fuel_mass+self.payload_mass]
        if override_weight:
            self.current_mass=[new_gross_weight]
        self.fuel_burn_rate=[]
        self.rotor_collective=[]
        self.tail_collective=[]
        self.power=[]
        self.upward_force=[]
        self.engine=powerplant.powerplant()

    def main(self):
        
        output_message=message.simMessage()
        for i in range(1, len(self.times)):
            if self.current_altitude[-1]<=self.altitudes[i]:
                for t in range(self.times[i-1],self.times[i],dT):
                    self.power.append(self.hover_and_climb(i))
                    control_message=message.simMessage()
                    control_message.add_payload({"power_required":self.power[-1]*self.engine_efficiency,"temp_dev_isa":0,"altitude":self.current_altitude[-1]})
                    self.fuel_burn_rate.append(self.engine.get_fuel_rate(control_message).get_payload()['fuel_burn_rate'])

                    print(self.current_time[-1])
                    #updating helicopter parameters

                    self.fuel_mass.append(self.fuel_mass[-1]-self.fuel_burn_rate[-1]*dT)
                    self.current_altitude.append(self.current_altitude[-1]+self.climb_vel[-1]*dT)
                    self.current_mass.append(self.current_mass[-1]-self.fuel_burn_rate[-1]*dT)
                    self.current_time.append(self.current_time[-1]+dT)
                    if self.fuel_mass[-1]<0:
                        output_message.add_error({"Error":"Helicopter out of fuel"})
                        break
        output_message.add_payload({"Altitudes":self.current_altitude,"Mass":self.current_mass,"Time":self.current_time,"Main_collective":self.rotor_collective,"Tail_collective":self.tail_collective,"Thrust":self.upward_force,"Power_required":self.power,"Fuel_burn_rate":self.fuel_burn_rate}) 
        return output_message
    
    def hover_and_climb(self,i):
        self.climb_vel.append((self.altitudes[i]-self.current_altitude[-1])/(self.times[i]-self.current_time[-1]))
        main_collective,tail_collective=self.collectives()
        self.rotor_collective.append(main_collective)
        self.tail_collective.append(tail_collective)
        self.heli.climb_vel=self.climb_vel[-1]
        self.heli.current_altitude=self.current_altitude[-1]
        self.heli.rotor_collective=main_collective
        self.heli.tail_collective=tail_collective
        main_rotor,tail_rotor=self.heli.main()
        self.upward_force.append(main_rotor.payload["thrust"])
        #print(main_rotor.payload["power"],tail_rotor.payload['power'],self.current_mass[-1]*self.climb_vel[-1]*g)
        return main_rotor.payload["power"]+tail_rotor.payload['power']+self.current_mass[-1]*self.climb_vel[-1]*g

    def collectives(self):
        main=0
        tail=0
        n=1000
        for i in range(0,301,1):
            if self.heli.force_z(i/n,0,self.climb_vel[-1],self.current_altitude[-1])>self.current_mass[-1]*g:
                main=i/n
                break
        for i in range(0,300,1):
            if self.heli.moment_z(main,i/n,self.climb_vel[-1],self.current_altitude[-1])>self.current_mass[-1]*g:
                tail=i/n
                break
        return main,tail
        #return fsolve(self.heli.hover,[0,0],(self.climb_vel[-1],self.current_altitude[-1],self.current_mass[-1],0),epsfcn=0.001,factor=0.1)

'''
heli=mission_planner("input_files/helicopter.json")
out=heli.main()
print(out.payload["Power_required"])
#ax=plt.Axes()
#plt.plot(out.payload["Mass"])
#ax.plot(out.payload["Power_required"])
#plt.show()
'''