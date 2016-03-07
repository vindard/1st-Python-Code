x = 1 #start at this natural number
l = [] #clearing set for reruns in Jupyter notebook
sum = 0 #setting sum variable
below_limit = 1000 #end at this natural number

while x < below_limit:
    if (x % 3 == 0) or (x % 5 == 0):
        l.append(x)
        sum += x
    x += 1
    
print ('Sum: \n{} \n\nNumbers:\n{}'.format(sum,l))

raw_input("Press any key to exit...")
