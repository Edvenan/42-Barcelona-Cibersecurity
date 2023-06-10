#######################
# TEST TinyStatistician
#######################        

from TinyStatistician import TinyStatistician
import numpy 

#Examples
tstat = TinyStatistician()
a = [1, 42, 300, 10, 59]
b = [13,21,21,40,42,48,55,72]
c = [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 6, 6]
arr = numpy.array([1, 2, 3, 4, 5])


tstat.mean(a)
print(tstat.mean(a))
# Expected result: 82.4

tstat.median(a)
print(tstat.median(a))
# Expected result: 42.0

tstat.quartiles(a)
print(tstat.quartiles(a))
# Expected result: [10.0, 59.0]

tstat.quartiles(b)
print(tstat.quartiles(b))
# Expected result: [21.0, 51.5]

tstat.quartiles(c)
print(tstat.quartiles(c))
# Expected result: [2.0, 5.0]

tstat.quartiles(arr)
print(tstat.quartiles(arr))
# Expected result: [2.0, 4.0]

tstat.var(a)
print(tstat.var(a))
# Expected result: 12279.439999999999

tstat.std(a)
print(tstat.std(a))
# Expected result: 110.81263465868862