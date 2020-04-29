import numpy.random as random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from copy import copy
from operator import itemgetter

# inisialisasi
M = 100      #panjang lintasan
p = 0.3      #probabilitas
v0 = 0       #kecepatan awal
N = 10       #banyaknya mobil
t_max = 100  #waktu max
v_max = 5    #kecepatan max

random.seed(1)
roads = np.array( [ [[0,M+0.5], [0.5,0.5]], [[0,M+0.5], [1.5,1.5]] ] )
cars = np.array([[random.randint(1,M), random.randint(1,2)] for i in range(1,N+1)])
cars = np.array(sorted(cars, key=itemgetter(0)))

jml = []
muter = 0
a = 0
v = v0
count = 0
movement = []
queue_cars = [i for i in range(N)]
# print(queue_cars)

# program
for t in range(t_max):
    x_row = []
    for i in queue_cars:
        car = cars[i]
        next_car = cars[i+1 if i+1 < N else 0]        
        # v1
        v = np.min([v+1, v_max])        
        # v2
        if (next_car[0] < car[0]):
            d = M - car[0] + next_car[0]
        else: 
            d = (next_car[0]-car[0])
        v = np.min([v, d-1])
        # v3
        pr = random.rand()
        if (pr < p):
            v = np.max([0, v-1])

        # update jarak
        x = copy(car[0])
        x = x + v
        if (x >= M):
            x = x - M
        x_row.append(copy([x,car[1]]))

    cars = copy(x_row)
    movement.append(cars)

    #kepadatan
    print ('Detik ',t)
    for j in (movement[t]):
        if j[0]>=80 and j[0]<=90:
            count+=1
    print(count/len(movement[t])*100,'%')
    count = 0
print('movement', movement)
#ratarata
for i in range(len(movement) - 1):
    if a>=len(movement) - 1:
        break
    a = i + 1
    nextemp = movement[a][2]
    temp = movement[i][2]
    if nextemp[0]<temp[0]:
        if nextemp[0] == movement[a][2][0] or nextemp[0] >= movement[a][2][0]:  
            jml.append(a)
            muter+=1

avg = jml[-1]/muter
print('Perputaran =',muter)
print('Rata-rata waktu =',avg)

# animasi
fig = plt.figure()
fig.set_size_inches(10, 10)
ax = plt.axes(ylim=(0,2), xlim=(0,M+0.5))
for road in roads:
    plt.plot(road[0], road[1], c="red")
    x = np.arange(10)
car1 = [x[0] for x in movement[0]]
car2 = [x[1] for x in movement[1]]
color = ['pink', 'blue', 'red', 'green', 'yellow', 'black', 'brown', 'grey', 'orange', 'purple']
car_marker = ax.scatter(car1, car2, c=color, s=100, marker="o")

def animate(i):
    cars_position = movement[i]
    car_marker.set_offsets(cars_position)
    return car_marker

anim = animation.FuncAnimation(fig, animate, frames=len(movement), interval=100)
plt.show()
