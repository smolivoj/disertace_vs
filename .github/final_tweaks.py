from pathlib import Path
p=Path('reserse.tex')
s=p.read_text()

s=s.replace('The development of commercially viable nuclear fusion reactors', 'The development of commercial fusion reactors')

s=s.replace(
'The theoretical part therefore serves not only as a review of the current state of knowledge but also as a logical transition toward the original experimental and numerical investigations presented in the second part of the dissertation.',
'The theoretical part therefore serves as an introduction to the original experimental and numerical investigations presented in the second part of the dissertation, while identifying the limitations of conventional cooling technologies that motivate porous-material-based channels.'
)

s=s.replace('Experimental facilities such as JET demonstrated reactor-relevant plasma performance', 'Experimental facilities such as JET demonstrated fusion-relevant plasma performance')

s=s.replace(
'   & JET & LHD & W7-X & ITER \\\\\n  \\hline\n  Major radius',
'   & JET & LHD & W7-X & ITER \\\\\n  \\hline\n  Device type & Tokamak & Stellarator & Stellarator & Tokamak \\\\\n  \\hline\n  Major radius'
)
s=s.replace('2.96 m & 3.9 m & 5.5 m & 6.2 m', '2.96~m & 3.9~m & 5.5~m & 6.2~m')
s=s.replace('100 $m^3$ & 30 $m^3$ & 30 $m^3$ & 900 $m^3$', '100~m$^3$ & 30~m$^3$ & 30~m$^3$ & 900~m$^3$')

old='It is important to note the large helical coils shown in Figure~\\ref{fig:dva_stell}. In both cases presented in Figure~\\ref{fig:dva_stell}, those coils can be substituted by a set of modular coils. The number of modular coils can be up to 100, depending on the design of the stellarator.'
new='Classical stellarators and torsatrons can use continuous helical windings, whereas modern optimized stellarators such as W7-X employ discrete non-planar modular coils. Modular coils provide the three-dimensional field required by the optimized plasma shape, but their geometry also imposes demanding manufacturing and assembly tolerances. Compared with an axisymmetric tokamak, stellarator optimization therefore involves a much larger geometrical design space.'
s=s.replace(old,new)

s=s.replace(
'An extensive numerical study was performed by M. Ghambalez to estimate the thermal performance of twisted tape inserts under fusion-relevant operating conditions.',
'An extensive numerical study was performed by M. Ghalambaz to estimate the thermal performance of twisted-tape inserts under fusion-relevant operating conditions \\cite{Ghalambaz2020}.'
)
s=s.replace('energy efficiency \\cite{Ghalambaz2020}.', 'energy efficiency.')

s=s.replace(
'The Nukiyama curve is a fundamental concept used to describe heat transfer during boiling processes.',
'The Nukiyama curve is a fundamental concept used to describe heat transfer during boiling processes \\cite{Leong2017-ag}.'
)
s=s.replace(
'Porosity ($\\Phi$) is defined as the ratio of the volume occupied by pores or voids to the total volume of the porous material, including both the solid and void components.',
'Porosity ($\\Phi$) is defined as the ratio of the volume occupied by pores or voids to the total volume of the porous material, including both the solid and void components \\cite{Calmidi}.'
)
s=s.replace(
'PPI, or "pores per inch," is a measure used to describe the density of pores in a porous material or structure.',
'PPI, or "pores per inch," is a measure used to describe the density of pores in a porous material or structure \\cite{Chen2021}.'
)
s=s.replace(
'Mathematically, tortuosity can be defined as the ratio of the actual path length of a fluid particle through the porous medium to the straight-line distance between the inlet and outlet of the porous material.',
'Mathematically, tortuosity can be defined as the ratio of the actual path length of a fluid particle through the porous medium to the straight-line distance between the inlet and outlet of the porous material \\cite{Cooper2014}.'
)

p.write_text(s)
print('final tweaks applied')
