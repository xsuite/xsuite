"""Build, inspect, and plot an aperture model for one FODO cell."""

import argparse
from pathlib import Path

# start-lattice
import matplotlib.pyplot as plt
import numpy as np
import xtrack as xt

bend_length = 2.0
bend_angle = 0.02

env = xt.Environment()

env.new('qf', 'Quadrupole', length=1.0, k1=0.12)
env.new('qd', 'Quadrupole', length=1.0, k1=-0.12)
env.new('drift', 'Drift', length=2.0)
env.new('bend', 'Bend', length=bend_length, angle=bend_angle)

line = env.new_line(name='fodo', components=['qf', 'drift', 'qd', 'bend'])
line.set_particle_ref('proton', p0c=3e9)
line.twiss_default['method'] = '4d'

twiss = line.twiss()
twiss.cols['s betx bety'].show(digits=5)
# => name                  s         betx         bety
# => qf                    0       21.219       16.751
# => drift                 1       21.217       16.751
# => qd                    3       16.651       21.343
# => bend                  4       16.653       21.343
# => _end_point            6       21.219       16.751
# end-lattice

# start-profiles
round_profile = env.aperture.new_profile('round', 'Circle', radius=0.030)
narrow_profile = env.aperture.new_profile('narrow', 'Ellipse', a=0.022, b=0.016)
wide_profile = env.aperture.new_profile('wide', 'Rectangle', max_x=0.026, max_y=0.022)

straight_pipe = env.aperture.new_pipe('straight_pipe', positions=[
    round_profile.place(at=0.0, tol_r=0.0002),
    round_profile.place(at=1.0, tol_r=0.0002),
    narrow_profile.place(at=3.0, tol_r=0.0004),
    narrow_profile.place(at=4.0, tol_r=0.0004),
])

pipe_curvature = 0.004  # 1/m, independently of the bend's 0.01 1/m curvature.
pipe_length = 1.99  # Keep the tilted end profile just inside the bend's exit.
bend_pipe = env.aperture.new_pipe(
    'bend_pipe', curvature=pipe_curvature,
    positions=[
        narrow_profile.place(at=0.0, tol_r=0.0004),
        wide_profile.place(at=pipe_length, tol_r=0.0002),
    ],
)
# end-profiles

# start-placements
aperture = line.aperture
aperture.place_pipe('upstream', straight_pipe, at='qf', tol_x=0.0003)
aperture.place_pipe('downstream', bend_pipe, at='bend', tol_x=0.0003)
aperture.build_model()
# end-placements

# start-exploration
print(list(env.aperture.profiles.keys()))
# => ['round', 'narrow', 'wide']

print(env.aperture.profiles['narrow'])
# => <ProfileView 'narrow': Ellipse(a=0.022, b=0.016)>

for position in env.aperture.pipes['straight_pipe']:
    print(position.profile.name, position.shift_s, position.tol_r)
    # => round 0.0 0.0002
    # => round 1.0 0.0002
    # => narrow 3.0 0.0004
    # => narrow 4.0 0.0004

print(aperture.pipe_positions['downstream'].tol_x)
# => 0.0003
# end-exploration

# start-tables
pipes = aperture.get_pipe_table()
pipes.cols['name pipe_name s_start s_end length'].show(digits=5)
# => name       pipe_name          s_start        s_end       length
# => upstream   straight_pipe            0            4            4
# => downstream bend_pipe                4         5.99         1.99

bounds = aperture.get_bounds_table()
bounds.cols['name profile_name s s_start s_end'].show(digits=5)
# => name          profile_name            s      s_start        s_end
# => upstream::0   round                   0            0            0
# => upstream::1   round                   1            1            1
# => upstream::2   narrow                  3            3            3
# => upstream::3   narrow                  4            4            4
# => downstream::0 narrow                  4            4            4
# => downstream::1 wide                 5.99       5.9896       5.9902
# end-tables

# start-sections
sections = aperture.get_cross_sections_at_s([0.0, 2.0, 4.0, 5.0, 5.95], extents=True)
sections.cols['s min_x max_x min_y max_y'].show(digits=5, max_col_width=12)
# => index            s        min_x        max_x        min_y        max_y
# => 0                0    -0.029991         0.03    -0.029993     0.029993
# => 1                2    -0.025991        0.026    -0.022995     0.022995
# => 2                4     -0.02199        0.022    -0.015997     0.015997
# => 3                5    -0.021005      0.02701    -0.018969     0.018971
# => 4             5.95    -0.014513      0.03733    -0.021862     0.021862

sections.cols['s tol_x tol_y tol_r'].show(digits=5, max_col_width=12)
# => index            s        tol_x        tol_y        tol_r
# => 0                0       0.0003            0       0.0002
# => 1                2       0.0003            0       0.0003
# => 2                4       0.0003            0       0.0004
# => 3                5       0.0003            0    0.0002995
# => 4             5.95       0.0003            0   0.00020402

polygon = sections.cross_section[1]  # (x, y) vertices at s = 2 m
# end-sections

# start-halo
aperture.halo_params.update(
    nemitt_x=2.5e-6,
    nemitt_y=2.5e-6,
    tol_co=0.0005,
    delta_rms=1e-4,
    halo_x=1.0,
    halo_y=1.0,
    halo_r=1.0,
    halo_primary=1.0,
)
# end-halo

# start-computation
# Stay inside the tilted end profile rather than sampling the pipe's end cap.
s_sample = np.arange(0.0, line.get_length(), 0.05)
clearance, sampled_twiss = aperture.get_aperture_sigmas_at_s(
    s_sample, method='rays', num_rays=64, with_progress=False,
)
limiting_index = np.argmin(clearance.n1)
print(f'Minimum n1: {clearance.n1[limiting_index]:.3f} '
      f'at s = {clearance.s[limiting_index]:.2f} m')
# => Minimum n1: 3.296 at s = 5.95 m

envelopes, _ = aperture.get_envelope_at_s(
    s_sample, sigmas=3.0, include_aper_tols=True, extents=True, with_progress=False,
)

envelopes.rows[[0, 40, 80, 100, 119]].cols['s min_x max_x min_y max_y'].show(
    digits=5, max_col_width=12,
)
# => index            s        min_x        max_x        min_y        max_y
# => 0                0    -0.013344     0.013344    -0.011557     0.011557
# => 40               2    -0.012723     0.012723     -0.01234      0.01234
# => 80               4    -0.012136     0.012136    -0.013155     0.013155
# => 100              5    -0.012723     0.012723     -0.01234      0.01234
# => 119           5.95    -0.013311     0.013311    -0.011594     0.011594
# end-computation

# start-plot-data
extents = aperture.get_extents_at_s(s_sample)
extents.rows[[0, 40, 80, 100, 119]].cols['s min_x max_x tol_x tol_r'].show(
    digits=5, max_col_width=12,
)
# => index            s        min_x        max_x        tol_x        tol_r
# => 0                0    -0.029991         0.03       0.0003       0.0002
# => 40               2    -0.025991        0.026       0.0003       0.0003
# => 80               4     -0.02199        0.022       0.0003       0.0004
# => 100              5    -0.021005      0.02701       0.0003    0.0002995
# => 119           5.95    -0.014513      0.03733       0.0003   0.00020402
beam_limits, _ = aperture.get_envelope_at_s(
    s_sample, sigmas=3.0, include_aper_tols=False, polygons=False, extents=True,
    with_progress=False,
)
beam_limits.rows[[0, 40, 80, 100, 119]].cols['s min_x max_x'].show(digits=5, max_col_width=12)
# => index            s        min_x        max_x
# => 0                0    -0.012844     0.012844
# => 40               2    -0.012123     0.012123
# => 80               4    -0.011436     0.011436
# => 100              5    -0.012123     0.012123
# => 119           5.95    -0.012807     0.012807

clearance.rows[[0, 40, 80, 100, 119]].cols['s n1'].show(digits=5, max_col_width=12)
# => index            s           n1
# => 0                0        7.087
# => 40               2        5.766
# => 80               4       3.6955
# => 100              5         4.72
# => 119           5.95       3.2958
# end-plot-data

# start-profile-plot
fig_profiles, axs = plt.subplots(1, 3, figsize=(10, 3.5))
for profile, ax in zip([round_profile, narrow_profile, wide_profile], axs):
    profile.plot(ax=ax)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
fig_profiles.tight_layout()
# end-profile-plot

# start-pipe-plot
fig_pipes, axs = plt.subplots(1, 2, figsize=(10, 3))
for pipe, ax in zip([straight_pipe, bend_pipe], axs):
    pipe.plot(plane='zx', ax=ax, max_curve_angle_rad=0.001)
    ax.set_aspect('auto')  # Enlarge the transverse scale to see the pipe shape.
fig_pipes.tight_layout()
# end-pipe-plot

# start-pipe-3d
fig_pipes_3d = plt.figure(figsize=(12, 4))
for index, pipe in enumerate([straight_pipe, bend_pipe]):
    ax = fig_pipes_3d.add_subplot(1, 2, index + 1, projection='3d')
    pipe.plot_3d(frame='curved', ax=ax, max_curve_angle_rad=0.001)
    ax.set_xlim(0, pipe.length)
    ax.set_ylim(-0.065, 0.04)
    ax.set_zlim(-0.035, 0.035)
    ax.set_box_aspect((4, 1, 1))  # Enlarge transverse dimensions for visibility.
fig_pipes_3d.tight_layout()
# end-pipe-3d

# start-floor-plot
fig_floor, ax = plt.subplots(figsize=(10, 3))
aperture.plot_floor_projection(ax=ax, max_curve_angle_rad=0.001)
fig_floor.tight_layout()
# end-floor-plot

# start-extent-plot
fig_extents, _ = aperture.plot_extents(
    s_sample, sigmas=3.0, with_progress=False,
)
fig_extents.set_size_inches(10, 6)
fig_extents.suptitle('Aperture limits and three-sigma beam envelope')
fig_extents.tight_layout()
# end-extent-plot

# start-transverse-plot
fig_transverse, ax = plt.subplots(figsize=(6, 5))
aperture.plot_transverse(
    s_positions=[2.0, 5.0], sigmas=3.0, ax=ax, with_progress=False,
)
ax.set_title('Cross-sections at 2 m and 5 m, with three-sigma envelopes')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
fig_transverse.tight_layout()
# end-transverse-plot

# start-clearance-plot
fig_clearance, ax = plt.subplots(figsize=(10, 3))
ax.plot(clearance.s, clearance.n1)
ax.set_xlabel('s [m]')
ax.set_ylabel(r'$n_1$')
ax.set_title('Maximum beam size that fits in the aperture')
fig_clearance.tight_layout()
# end-clearance-plot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, help='Save the example figures here.')
    args = parser.parse_args()
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, fig in [
            ('profiles', fig_profiles), ('floor', fig_floor), ('extents', fig_extents),
            ('transverse', fig_transverse), ('clearance', fig_clearance),
            ('pipes', fig_pipes), ('pipes_3d', fig_pipes_3d),
        ]:
            fig.savefig(args.output_dir / f'aperture_fodo_{name}.png', dpi=150)
    plt.show()
