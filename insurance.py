import numpy as np
import matplotlib.pyplot as plt
import math
import copy

# Fixing random state for reproducibility
np.random.seed(19680801)

class Expense:

    def __init__(self, name, avgcost):
        self.name = name
        self.cost = avgcost

class Coverage:

    def __init__(self, name, cad, copay, afterdeductible):
        self.name = name
        self.coverage = cad
        self.copay = copay
        self.afterdeductible = afterdeductible

class Plan:

    def __init__(self, name, deductible, oopm, biweeklycost):
        self.name = name
        self.outofpocketmax = oopm
        self.deductible = deductible
        self.coverage = []
        self.spent = 26*biweeklycost
        self.capture = []

    def AddCoverage(self, newcov):
        self.coverage.append(newcov)

    def AddHsaContribution(self, contribution):

        self.spent -= contribution

    def AssessExpense(self, expense):
        for e in self.coverage:
            if e.name == expense.name:
                    
                truecost = expense.cost
                
                if (e.afterdeductible == False):
                    truecost -= truecost*(e.coverage/100)
                    if (truecost > self.deductible):
                        self.deductible = 0
                    else:
                        self.deductible -= truecost
                else:
                    if (truecost > self.deductible):
                        truecost = (self.deductible) + (truecost - self.deductible)*((100-e.coverage)/100)
                        self.deductible = 0
                    else:
                        self.deductible -= truecost

                print(self.name, truecost, expense.name, self.deductible, self.outofpocketmax)

                truecost += e.copay

                if (self.outofpocketmax < truecost):
                    self.spent += self.outofpocketmax
                    self.outofpocketmax = 0
                else:
                    self.spent += truecost
                    self.outofpocketmax -= truecost

    def Capture(self):
        self.capture.append(self.spent)

ppo = Plan('PPO', 400, 2500, 39.23)
ppo.AddCoverage(Coverage('Office', 100, 20, False))
ppo.AddCoverage(Coverage('Hospital', 90, 0, True))
ppo.AddCoverage(Coverage('Urgent Care', 100, 50, False))
ppo.AddCoverage(Coverage('Ambulance', 90, 0, True))
ppo.AddCoverage(Coverage('Emergency Room', 100, 150, False))
ppo.AddCoverage(Coverage('Mental', 100, 20, False))
ppo.AddCoverage(Coverage('Drug', 100, 20, False))
ppo.Capture()

acct = Plan('Account-based', 1500, 3000, 25.38)
acct.AddCoverage(Coverage('Office', 90, 0, True))
acct.AddCoverage(Coverage('Hospital', 90, 0, True))
acct.AddCoverage(Coverage('Urgent Care', 90, 0, True))
acct.AddCoverage(Coverage('Ambulance', 90, 0, True))
acct.AddCoverage(Coverage('Emergency Room', 90, 0, True))
acct.AddCoverage(Coverage('Mental', 90, 0, True))
acct.AddCoverage(Coverage('Drug', 90, 0, True))
acct.AddHsaContribution(750)
acct.Capture()

plans = [ppo,acct]

office = Expense('Office', 75)
hospital = Expense('Hospital', 6493)
urgentcare = Expense('Urgent Care', 125)
ambulance = Expense('Ambulance', 600)
emergencyroom = Expense('Emergency Room', 656)
mental = Expense('Mental', 60)
drug = Expense('Drug', 5000)

scenarios = [
            [office, mental, office, emergencyroom, mental, mental, mental],
            [office, emergencyroom, ambulance, hospital, mental, hospital, urgentcare, hospital, mental, mental, mental],
            [office, ambulance, mental, hospital, urgentcare, hospital, mental, office, office, office, office, office],
            [mental, mental, mental, mental, mental, mental, mental, mental, mental, mental, mental, urgentcare, mental, mental],
            [hospital, hospital, ambulance, hospital, hospital, emergencyroom],
            [office, mental],
            [office, urgentcare, office, office, mental],
            [office],
            ]

fig = plt.figure()

cnt = math.ceil(math.sqrt(len(scenarios)))

for index,a in enumerate(scenarios):
    ax = fig.add_subplot(cnt,cnt,index+1)
    for p in plans:
        plan = copy.deepcopy(p)
        for s in a:
            plan.AssessExpense(s)
            plan.Capture()
        ax.plot(plan.capture, label=plan.name)
    ax.legend()

plt.show()
