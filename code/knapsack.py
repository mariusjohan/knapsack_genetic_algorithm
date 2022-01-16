from pyomo.environ import *
import sys

values = {"kort": 150, "kompas": 35, "vand": 200, "sandwich":160, "sukker":60,"dåsemad": 45,"banan":60, "æble":40, "ost": 30, "øl": 10, "solcreme":70, "kamera":30, "T-shirt":15, "bukser":10, "paraply": 40, "vandtætte bukser": 70, "vandtæt overtøj": 75, "pung": 80, "solbriller": 20, "håndklæde":12, "sokker": 50, "bog":10, "notesbog": 1, "telt": 150}
weights = {"kort": 90, "kompas": 130, "vand": 1530, "sandwich":500, "sukker":150,"dåsemad": 680,"banan":270, "æble":390, "ost": 230, "øl": 520, "solcreme":110, "kamera":320, "T-shirt":240, "bukser":480, "paraply": 730, "vandtætte bukser": 420, "vandtæt overtøj": 430, "pung": 220, "solbriller": 70, "håndklæde":180, "sokker": 40, "bog":300, "notesbog": 900, "telt": 2000}


limit = 5000

M = ConcreteModel()
M.I = Set(initialize=values.keys())
M.x= Var(M.I, within=Binary)
M.value = Objective(expr=sum(values[i]*M.x[i] for i in M.I), sense=maximize)
M.weight = Constraint(expr=sum(weights[i]*M.x[i] for i in M.I) <= limit)
