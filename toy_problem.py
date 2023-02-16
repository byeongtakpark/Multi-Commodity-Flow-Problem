###### Multi Commodity Flow Problem ######
import gurobipy as gp
from gurobipy import GRB

commodity = ['Passenger', 'Cargo']
vertiport = ['Samseong', 'Gimpo', 'Incheon', 'Jongro']
arcs, capacity = gp.multidict({
    ('Samseong', 'Gimpo'): 20, 
    ('Samseong', 'Incheon'): 30,
    ('Samseong', 'Jongro'): 20,
    ('Gimpo', 'Incheon'): 15,
    ('Gimpo', 'Jongro'): 10,
    ('Incheon', 'Jongro'): 10                     
})

distance = {
    ('Samseong', 'Gimpo'): 30, 
    ('Samseong', 'Incheon'): 20,
    ('Samseong', 'Jongro'): 15,
    ('Gimpo', 'Incheon'): 40,
    ('Gimpo', 'Jongro'): 10,
    ('Incheon', 'Jongro'): 60
} # Unit: km

unit_cost = {
    'Passenger': 2000, 
    'Cargo': 1500 
} # Unit: KRW per km

cost_passenger = {}
cost_cargo = {}

for key, value in distance.items():
   cost_passenger[key] = value * unit_cost['Passenger']
   cost_cargo[key] = value * unit_cost['Cargo']
  
# inflow > 0: origin, inflow < 0: destination  
inflow = {
    ('Passenger', 'Samseong'): 14, 
    ('Passenger', 'Gimpo'): 3,
    ('Passenger', 'Incheon'): -10,
    ('Passenger', 'Jongro'): -7,
    ('Cargo', 'Samseong'): 4,
    ('Cargo', 'Gimpo'): 6,
    ('Cargo', 'Incheon'): -5,
    ('Cargo', 'Jongro'): -5
} 

m = gp.Model('MCFP')


flow = m.addVars(commodity, arcs)

m.setObjective(gp.quicksum(cost_passenger[i, j] * flow['Passenger', i, j] + cost_cargo[i, j] * flow['Cargo', i, j] for i, j in arcs), GRB.MINIMIZE)

m.addConstrs(
    flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs 
)

m.addConstrs(
    (flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*')
    for h in commodity for j in vertiport)
)

m.optimize()

# Solution
if m.Status == GRB.OPTIMAL:
    solution = m.getAttr('X', flow)
    for h in commodity:
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print('From {} to {}: {}'.format(i, j, solution[h, i, j]))
