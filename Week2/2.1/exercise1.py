import numpy as np
import matplotlib.pyplot as plt

## Initialization
# Length of simulation (time steps)
simlen = 30
# Output
y_nodelay = np.zeros((simlen))
y_delayed = np.zeros((simlen))
y_corrected = np.zeros((simlen))
# Target
target = 0.0

# Controller gain
K = 1.0
K_corrected = 0.1

# Set first output
y_nodelay[0] = 1
y_delayed[0] = 1
y_corrected[0] = 1

# TODO define the time delay
delay_time = 3

## Simulation
for t in range(simlen-1):
    # Compute output
    # TODO include the time delay
    u_nodelay = K * (target - y_nodelay[t])
    y_nodelay[t+1]=0.5*y_nodelay[t] + 0.4*u_nodelay # 1st order dynamics

    u_delayed = K * (target - y_delayed[t-delay_time])
    y_delayed[t+1]=0.5*y_delayed[t] + 0.4*u_delayed # 1st order dynamics

    u_corrected = K_corrected * (target - y_corrected[t-delay_time])
    y_corrected[t+1]=0.5*y_corrected[t] + 0.4*u_corrected # 1st order dynamics

## Plot
time = range(simlen)
plt.plot(time, y_nodelay)
plt.plot(time, y_delayed)
plt.plot(time, y_corrected)
plt.legend(['no delay', 'delay', 'corrected'])
plt.xlabel('time step')
plt.ylabel('y')
plt.show()