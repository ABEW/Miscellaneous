#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def rk4_single_step(fun, dt, x0, t0):
    f1 = fun(x0, t0)
    f2 = fun(x0 + ((dt / 2) * f1), t0 +(dt / 2))
    f3 = fun(x0 + ((dt / 2) * f2), t0 +(dt / 2))
    f4 = fun(x0 + (dt * f3), t0 + dt)
    
    x1 = x0 + (dt / 6) * (f1 + 2 * f2 + 2 * f3 + f4)
    return x1

def my_fun(x, t):
    return np.array(
            [
                SIGMA * (x[1] - x[0]),
                x[0] * (RHO - x[2]),
                (x[0] * x[1]) - (BETA * x[2])
            ]
    )


def main():
    x0 = [-8, 8, 27]
    dt = 0.01
    T = 10

    time_steps = list(np.arange(0,T,dt))

    x_traj = np.zeros([int(T/dt)+1,3])
    x_traj[0] = np.array(x0)

    for i,t in enumerate(time_steps):
        x_new = rk4_single_step(my_fun, dt, x_traj[i], t)
        x_traj[i+1] = x_new
    
    x_traj_ref = solve_ivp(lambda a,b: my_fun(b,a), (0,T), x0, t_eval=time_steps).y.T

    ax = plt.figure().add_subplot(projection="3d")
    ax.plot(x_traj[:,0],x_traj[:,1],x_traj[:,2])
    ax.plot(x_traj_ref[:,0],x_traj_ref[:,1],x_traj_ref[:,2],"--")
    plt.show()
    
if __name__ == "__main__":
    SIGMA = 10.0
    BETA = (8 / 3.0)
    RHO = 28
    
    main()
