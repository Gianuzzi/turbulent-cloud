from __future__ import print_function

import numpy as np
from turbulence import VelocityGrid
from uniform_sphere import Sphere
from libs.const import G, msol, parsec
from libs.utils import save_particles


if __name__ == "__main__":

    Mcloud = 1e4*msol
    Rcloud = 1*parsec
    N = 10000 # desired number of cells to represent cloud
    print("We want {:d} gas cells to represent the cloud".format(N))

    # where we want to place the cloud's center of mass
    r_com = np.array([0.,0.,0.])

    # first, determine position of particles given total number of
    # desired cells
    cloud = Sphere(N=N, center=r_com, radius=Rcloud)
    dx = cloud.dx

    # produce the velocity grid for turbulent ICs
    vg = VelocityGrid(xmax=2*Rcloud, dx=dx, N=128)

    pos = cloud.pos
    Ngas = cloud.Npart
    mpart = Mcloud / Ngas
    mass = np.full(Ngas, mpart)

    vel = np.zeros((Ngas, 3))

    vg.coordinate_grid(xstart=r_com[0]-Rcloud, xend=r_com[0]+Rcloud)
    vel = vg.add_turbulence(pos=pos, vel=vel)

    # now we need to normalize the velocity values
    # we do it such that the cloud is marginally bound
    v2 = np.linalg.norm(vel, axis=1)**2
    Ekin = np.sum(0.5*mpart*v2)
    Epot = 3./5. * G * Mcloud**2 / Rcloud
    Avel = np.sqrt(Epot/(2*Ekin))
    vel *= Avel


    save_particles(pos, vel, mass, 'ics_cloud.dat')






