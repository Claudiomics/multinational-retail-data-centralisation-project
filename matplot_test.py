import matplotlib.pyplot as plt
import numpy as np


#y = [44.557729, 22.357841, 15.853934, 9.048969, 8.181527]
#plt.pie(y)
#plt.show()

# cool!!!

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
store_type = ['Local', 'Web Portal', 'Super Store', 'Mall Kiosk', 'Outlet']
percentage_total = np.array([44.557729, 22.357841, 15.853934, 9.048969, 8.181527])
ax.pie(percentage_total, labels=store_type, autopct='%1.2f%%')
plt.show()