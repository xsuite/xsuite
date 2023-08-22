# copyright ################################# #
# This file is part of the Xfields Package.   #
# Copyright (c) CERN, 2021.                   #
# ########################################### #

import time

import numpy as np
from matplotlib import pyplot as plt
from mpi4py import MPI
import xobjects as xo
import xtrack as xt
import xfields as xf
import xpart as xp

context = xo.ContextCpu(omp_num_threads=0)

####################
# Pipeline manager #
####################
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
my_rank   = comm.Get_rank()

pipeline_manager = xt.PipelineManager(comm)
if nprocs == 2:
    pipeline_manager.add_particles('B1b1',0)
    pipeline_manager.add_particles('B2b1',1)
    pipeline_manager.add_element('IP1')
    pipeline_manager.add_element('IP2')
else:
    print('Need 2 MPI processes for this test')
    exit()

#################################
# Generate particles            #
#################################

n_macroparticles = int(1e4)
bunch_intensity = 2.3e11
physemit_x = 2E-6*0.938/7E3
physemit_y = 2E-6*0.938/7E3
beta_x_IP1 = 1.0
beta_y_IP1 = 1.0
beta_x_IP2 = 1.0
beta_y_IP2 = 1.0
sigma_z = 0.08
sigma_delta = 1E-4
beta_s = sigma_z/sigma_delta
Qx = 0.31
Qy = 0.32
Qs = 2.1E-3

#Offsets in sigma
mean_x_init = 0.1
mean_y_init = 0.0

p0c = 7000e9

print('Initialising particles')
if my_rank == 0:
    particles = xp.Particles(_context=context,
        p0c=p0c,
        x=np.sqrt(physemit_x*beta_x_IP1)*(np.random.randn(n_macroparticles)+mean_x_init),
        px=np.sqrt(physemit_x/beta_x_IP1)*np.random.randn(n_macroparticles),
        y=np.sqrt(physemit_y*beta_y_IP1)*(np.random.randn(n_macroparticles)-mean_y_init),
        py=np.sqrt(physemit_y/beta_y_IP1)*np.random.randn(n_macroparticles),
        zeta=sigma_z*np.random.randn(n_macroparticles),
        delta=sigma_delta*np.random.randn(n_macroparticles),
        weight=bunch_intensity/n_macroparticles
    )
    particles.init_pipeline('B1b1')
    partner_particles_name = 'B2b1'
elif my_rank == 1:
    particles = xp.Particles(_context=context,
        p0c=p0c,
        x=np.sqrt(physemit_x*beta_x_IP1)*(np.random.randn(n_macroparticles)+mean_x_init),
        px=np.sqrt(physemit_x/beta_x_IP1)*np.random.randn(n_macroparticles),
        y=np.sqrt(physemit_y*beta_y_IP1)*(np.random.randn(n_macroparticles)-mean_y_init),
        py=np.sqrt(physemit_y/beta_y_IP1)*np.random.randn(n_macroparticles),
        zeta=sigma_z*np.random.randn(n_macroparticles),
        delta=sigma_delta*np.random.randn(n_macroparticles),
        weight=bunch_intensity/n_macroparticles
    )
    particles.init_pipeline('B2b1')
    partner_particles_name = 'B1b1'
else:
    print('No need for rank',my_rank)
    exit()

#############
# Beam-beam #
#############
nb_slice = 11
bin_edges = sigma_z*np.linspace(-3.0,3.0,nb_slice+1)
slicer = xf.TempSlicer(bin_edges = bin_edges)
config_for_update_IP1=xf.ConfigForUpdateBeamBeamBiGaussian3D(
   pipeline_manager=pipeline_manager,
   element_name='IP1',
   partner_particles_name = partner_particles_name,
   slicer=slicer,
   update_every=1
   )
config_for_update_IP2=xf.ConfigForUpdateBeamBeamBiGaussian3D(
   pipeline_manager=pipeline_manager,
   element_name='IP2',
   partner_particles_name = partner_particles_name,
   slicer=slicer,
   update_every=1
   )
print('build bb elements...')
bbeamIP1 = xf.BeamBeamBiGaussian3D(
            _context=context,
            other_beam_q0 = particles.q0,
            phi = 500E-6,alpha=0.0,
            config_for_update = config_for_update_IP1)

bbeamIP2 = xf.BeamBeamBiGaussian3D(
            _context=context,
            other_beam_q0 = particles.q0,
            phi = 500E-6,alpha=np.pi/2,
            config_for_update = config_for_update_IP2)

#################################################################
# arcs (here they are all the same with half the phase advance) #
#################################################################

arc12 = xt.LinearTransferMatrix(
        alpha_x_0=0.0, beta_x_0=beta_x_IP1, disp_x_0=0.0,
        alpha_x_1=0.0, beta_x_1=beta_x_IP2, disp_x_1=0.0,
        alpha_y_0=0.0, beta_y_0=beta_y_IP1, disp_y_0=0.0,
        alpha_y_1=0.0, beta_y_1=beta_y_IP2, disp_y_1=0.0,
        Q_x=Qx/2, Q_y=Qy/2,beta_s=beta_s, Q_s=Qs/2)

arc21 = xt.LinearTransferMatrix(
        alpha_x_0=0.0, beta_x_0=beta_x_IP2, disp_x_0=0.0,
        alpha_x_1=0.0, beta_x_1=beta_x_IP1, disp_x_1=0.0,
        alpha_y_0=0.0, beta_y_0=beta_y_IP2, disp_y_0=0.0,
        alpha_y_1=0.0, beta_y_1=beta_y_IP1, disp_y_1=0.0,
        Q_x=Qx/2, Q_y=Qy/2,beta_s=beta_s, Q_s=Qs/2)

#################################################################
# Tracker                                                       #
#################################################################

elements = [bbeamIP1,arc12,bbeamIP2,arc21]
line = xt.Line(elements=elements)
tracker = xt.Tracker(line=line)
branch = xt.PipelineBranch(tracker,particles)
multitracker = xt.PipelineMultiTracker(branches=[branch])

#################################################################
# Tracking                                                      #
#################################################################
print('Tracking...')
time0 = time.time()
nTurn = 1024
multitracker.track(num_turns=nTurn,turn_by_turn_monitor=True)
print('Done with tracking.',(time.time()-time0)/1024,'[s/turn]')

#################################################################
# Post-processing: raw data and spectrum                        #
#################################################################

if my_rank == 0:
    if False:
        for i in range(10):
            plt.figure(1000+i)
            plt.plot(tracker.record_last_track.x[i,:],tracker.record_last_track.px[i,:],'x')

    positions_x_b1 = np.average(tracker.record_last_track.x,axis=0)
    positions_y_b1 = np.average(tracker.record_last_track.y,axis=0)
    plt.figure(0)
    plt.plot(np.arange(nTurn),positions_x_b1/np.sqrt(physemit_x*beta_x_IP1),'x')
    plt.plot(np.arange(nTurn),positions_y_b1/np.sqrt(physemit_y*beta_y_IP1),'x')
    plt.figure(1)
    freqs = np.fft.fftshift(np.fft.fftfreq(nTurn))
    mask = freqs > 0
    myFFT = np.fft.fftshift(np.fft.fft(positions_x_b1))
    plt.semilogy(freqs[mask], (np.abs(myFFT[mask])))
    myFFT = np.fft.fftshift(np.fft.fft(positions_y_b1))
    plt.semilogy(freqs[mask], (np.abs(myFFT[mask])))
    plt.show()


