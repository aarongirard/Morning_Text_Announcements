from ..user_interactions import phase0,phase1,phase2,phase3

"""
I think its going to be better to test user 'routes' instead of phase 
functions directly
"""

#generate random phone numbers:
"""
for i in range(1,10):
  print randint(10000000,99999999)

51728737
67126358
49440558
60088969
83575221
27823573
32057906
92218094
85955494
"""

#assumption:number is integer
#assumption: text is string



print 'testing No signup'
number = 67126358
print phase0(number,'hello')
print phase1(number, 'No')

print 'testing regular signup with > 1 locations returned'
number = 67126358
print phase0(number,'hello')
print phase1(number, 'New York')
print phase2(number, '1')

#testing signup with 1 locations returned
number = 60088969
print phase0(number, 'hello')
print phase1(number, 'hello')

print 'testing signup rejection when > 15 cities returned'
number = 83575221
print phase0(number, 'hello')
print phase1(number, 'historic')

