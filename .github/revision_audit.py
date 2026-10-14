from pathlib import Path
import re
p=Path('reserse.tex')
if r'\begin{tabular*}{\textwidth}' in p.read_text():
    print('Audited revision already applied')
    raise SystemExit(0)
s=p.read_text()

# 1) Title page 2: stable one-page layout
start=s.index('\\textbf{Czech Technical University}', s.index('\\pagebreak'))
end=s.index('\\setcounter{tocdepth}{2}', start)
new_title=r'''\thispagestyle{empty}
\begin{center}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l r}
\textbf{Czech Technical University} & České Vysoké Učení Technické \\
\textbf{in Prague} & v Praze \\
\textbf{Faculty of Mechanical Engineering} & Fakulta Strojní \\
\textbf{Department of Energetics} & Ústav Energetiky \\
\textbf{Energy Engineering} & Energetika \\
\end{tabular*}

\vspace*{4.2cm}
{\Large\bfseries Thermohydraulic parameters\\[0.25em]
of porous material based cooling channels\par}

\vspace{0.9cm}
{\large Termohydraulické parametry chladících kanálů\\[0.25em]
s využitím pórovitých materiálů\par}

\vfill
\begin{minipage}{\textwidth}
\raggedright
\textbf{Author}\\[0.15em]
{\large Ing. Vojtěch Smolík}\\[0.65em]
\textbf{Supervisor}\\[0.15em]
{\large Doc. Ing. Slavomír Entler, Ph.D.}\\[0.65em]
\textbf{Supervisor-consultant}\\[0.15em]
{\large doc. Ing. Pavel Zácha, Ph.D.}
\end{minipage}
\end{center}
\pagebreak
'''
s=s[:start]+new_title+s[end:]

# 2) Part III intro: numerical -> experiment, avoid claiming TEALC first
old=re.search(r'\\part\{Numerical and Experimental Investigation\}.*?Together, the presented experimental and numerical investigations provide a comprehensive assessment of porous material based cooling channels and demonstrate their potential as an alternative high-performance cooling technology for future magnetic confinement fusion devices\.', s, re.S)
if old:
    new=r'''\part{Numerical and Experimental Investigation}
This part presents the original research carried out within the framework of the doctoral project. The work combines numerical simulations and experimental measurements to investigate the hydraulic and thermal behaviour of porous-material-based cooling channels intended for high-heat-flux applications in magnetic-confinement fusion devices.

The research is arranged in the same order as the underlying methodology. Chapter~8 summarizes preliminary numerical and experimental work that established methods subsequently used in the main programme. Chapter~9 then uses controlled substitute geometries to quantify the influence of porosity and tortuosity and to assess the accuracy of computational fluid dynamics (CFD) for pore-resolved flow. Chapter~10 provides the corresponding experimental characterization and hydraulic measurements of real porous samples in the TEALC facility. Chapter~11 increases the geometrical fidelity by analysing microCT-reconstructed porous structures, including conjugate heat transfer. Finally, Chapter~12 presents the high-heat-flux proof-of-concept experiment and the comparison between a plain channel and a porous insert.

This sequence separates preliminary method development from the main porous-channel investigation and follows the logic numerical model $\rightarrow$ experimental validation $\rightarrow$ realistic geometry $\rightarrow$ high-heat-flux demonstration.'''
    s=s[:old.start()]+new+s[old.end():]

# 3) Basic Research: only the two preliminary research tasks
basic_start=s.index('\\section{Basic Research}')
hyp=s.index('\\subsection{Numerical research of the hypervapotron}', basic_start)
basic_head=r'''\section{Basic Research}
The preliminary work performed before the main porous-channel programme established two methods used later in the dissertation. First, numerical modelling of a hypervapotron was used to assess the treatment of subcooled boiling under fusion-relevant high heat fluxes. Second, a dedicated induction-heated experiment was used to reproduce the characteristic boiling regimes represented by the Nukiyama curve through the Leidenfrost effect. These studies are summarized here because they provide methodological background for the subsequent porous-channel research.

'''
s=s[:basic_start]+basic_head+s[hyp:]

# 4) Fix hypervapotron preliminary captions unit spacing / prose
s=s.replace('inlet water: 50 °C, 6~bar, 4~m/s', 'inlet water: 50~$^\\circ$C, 6~bar, 4~m/s')
s=s.replace('liquid water a vapour', 'liquid water and vapour')
s=s.replace('The resulting vapour volume ratio in the fluid domain (left) and the corresponding CuCrZr solid temperature profile is shown.', 'The resulting vapour volume fraction in the fluid domain (left) and the corresponding CuCrZr solid-temperature profile (right) are shown.')

# 5) Fix Nukiyama experimental conclusion without inventing missing fit
broken='''All the regions of Nukiyama curve are clearly observable. \nMaximum in the point of critical heat flux $q_{maxi}$ at 30~$^\\circ$C and the minimum at \nAn increase in heat flux for temperatures above the Leidenfrost point (approx. 120~$^\\circ$C) is observable.'''
replacement='''All characteristic regions of the boiling curve are observable in the measured data. The local maximum occurs at a wall superheat of approximately 30~$^\\circ$C. After the transition toward film boiling, the heat flux decreases and subsequently rises again for temperatures above the Leidenfrost point, which was observed at approximately 120~$^\\circ$C. The individual points are retained because the purpose of this experiment was to identify the boiling regimes and their transition temperatures rather than to derive a new empirical boiling correlation.'''
s=s.replace(broken,replacement)

# 6) Stellarator opening: remove repeated/confusing tokamak-current statement
st0=s.index('\\subsection{Magnetic confinement - Stellarator design}')
st1=s.index('\\begin{equation}', st0)
stellar_open=r'''\subsection{Magnetic confinement - Stellarator design}
The stellarator is the second principal concept for magnetic confinement fusion. In contrast to the axisymmetric tokamak, the stellarator produces the required rotational transform predominantly by three-dimensional external coils and therefore does not require a large transformer-driven plasma current for steady-state confinement. This is its principal physical advantage for continuous operation, but it leads to substantially more complex magnetic and mechanical geometry.

The stellarator concept was introduced by Lyman Spitzer in the early 1950s within Project Matterhorn; early devices used a figure-eight geometry to obtain rotational transform. Subsequent concepts, including classical stellarators, torsatrons and heliotrons, replaced this geometry with combinations of toroidal, helical and vertical-field coils. Figure~\ref{fig:prvni_stell} shows an early stellarator concept and Figure~\ref{fig:dva_stell} illustrates representative coil arrangements \cite{spitzer_paw_2024,kniha_2018}.

\begin{figure}[h]
  \centering
  \begin{minipage}{0.35\textwidth}
      \centering
      \includegraphics[width=\linewidth]{prvni_stelarator.png}
      \caption{Early stellarator design developed within Project Matterhorn \cite{spitzer_paw_2024}.}
      \label{fig:prvni_stell}
  \end{minipage}\hfill
  \begin{minipage}{0.60\textwidth}
      \centering
      \includegraphics[width=\linewidth]{stellaratory_dva.png}
      \caption{Representative stellarator coil concepts: classical stellarator (left) and torsatron/heliotron (right) \cite{kniha_2018}.}
      \label{fig:dva_stell}
  \end{minipage}
\end{figure}

\noindent Because the magnetic field is generated almost entirely by external coils, stellarator optimization has many more geometrical degrees of freedom than tokamak design. Modern optimization therefore seeks a compromise between plasma confinement, magnet complexity, maintenance access and manufacturability. The crucial engineering distinction is that tokamaks are axisymmetric, whereas stellarators use rotationally periodic, non-axisymmetric magnetic fields.'''
s=s[:st0]+stellar_open+'\n\n'+s[st1:]

s=s.replace('n T \\tau_E \\geq \\mathrm{const.}', 'n T \\tau_\\mathrm{E} \\geq \\mathrm{const.}')
s=s.replace('energy confinement time $\\tau_E$', 'energy confinement time $\\tau_\\mathrm{E}$')
s=s.replace('energy confinement $\\tau_E$', 'energy confinement $\\tau_\\mathrm{E}$')
s=s.replace('\\tau_E^{\\mathrm{ISS04}}', '\\tau_\\mathrm{E}^{\\mathrm{ISS04}}')
s=s.replace('P_h^{-0.61}', 'P_\\mathrm{h}^{-0.61}')
s=s.replace('$P_h$ is the heating power', '$P_\\mathrm{h}$ is the heating power')
s=s.replace('plasma volume ($V_p$)', 'plasma volume ($V_\\mathrm{p}$)')
s=s.replace('The volume of plasma ($V_p$)', 'The plasma volume ($V_\\mathrm{p}$)')
s=s.replace('Plasma volume $V_p$', 'Plasma volume $V_\\mathrm{p}$')
s=s.replace('B^4 V_p T', 'B^4 V_\\mathrm{p} T')
s=s.replace('V_p \\propto', 'V_\\mathrm{p} \\propto')

old_island=re.search(r'\\noindent The rotational transform.*?Wendelstein 7-X\.', s, re.S)
if old_island:
    new_island=r'''\noindent The rotational transform $\iota$ describes the poloidal advance of a field line per toroidal turn and is used to characterize magnetic surfaces in both tokamaks and stellarators. In a tokamak, a substantial part of the poloidal field is produced by the plasma current, whereas in a stellarator the transform is produced predominantly by external coils. For irrational values of the transform, field lines densely cover nested magnetic surfaces. At rational surfaces, resonant perturbations can form magnetic islands, as illustrated in Figure~\ref{fig:ruzne_tvary_vrstev}. In the confined plasma of a tokamak such islands are generally undesirable because they degrade energy confinement and, if sufficiently large, can contribute to loss of plasma stability. In optimized stellarators, by contrast, edge islands can be deliberately used to form an island divertor and thereby control particle and heat exhaust; this concept was demonstrated on Wendelstein~7-AS and is employed on Wendelstein~7-X \cite{Chen2011,Barton2015,Wang2020}.'''
    s=s[:old_island.start()]+new_island+s[old_island.end():]

# 7) Replace ITER/DEMO power exhaust subsection through before W7-X
pe0=s.index('\\subsection{ITER and DEMO}')
pe1=s.index('\\subsection{Wendelstein-7x heat load analysis}', pe0)
new_pe=r'''\subsection{ITER and DEMO}
ITER and DEMO illustrate two different stages of fusion technology: ITER is an experimental burning-plasma device, whereas DEMO is intended to demonstrate electricity production and a substantially more reactor-like duty cycle. For the present dissertation, the relevant issue is the local thermal load imposed on plasma-facing and nearby in-vessel components rather than the complete plant heat-transport and power-conversion architecture.

\subsubsection{First-wall heat load}
The ITER first wall is divided into blanket modules with different design heat-flux capabilities according to their position. During normal operation, the nominal steady-state surface load is of the order of 0.5~MW/m$^2$, while local design capabilities are higher in enhanced-heat-flux regions. Volumetric nuclear heating caused by 14.1~MeV fusion neutrons represents an additional thermal load inside the blanket structure. The exact combination of surface and volumetric heating therefore depends on position and operating scenario \cite{Mitteau2010,Merola2014-zi}.

\begin{figure}[h]
  \centering
  \begin{minipage}{0.70\textwidth}
      \centering
      \includegraphics[width=\linewidth]{mapa_load.jpg}
      \caption{Distribution of ITER blanket modules and first-wall heat-flux design categories; black regions indicate ports and openings \cite{Mitteau2010}.}
      \label{fig:mapatoku1}
  \end{minipage}\hfill
  \begin{minipage}{0.25\textwidth}
      \centering
      \includegraphics[width=\linewidth]{profil_load.jpg}
      \caption{Representative steady-state design heat flux for ITER first-wall panels \cite{Merola2014-zi}.}
      \label{fig:mapatoku2}
  \end{minipage}
\end{figure}

DEMO is expected to operate with a substantially larger fraction of the fusion power processed continuously by reactor systems. Figure~\ref{fig:mapatoku3} illustrates two calculated radiative-load distributions for a DEMO configuration. One case assumes 457~MW of total radiated power distributed on flux surfaces, while the second assumes 150~MW radiated from the X-point region. The comparison demonstrates that the spatial distribution of the radiation source is as important for first-wall design as the total radiated power \cite{Wenninger_2017}.

\begin{figure}[h]
  \centering
  \includegraphics[width=15cm]{DEMO_load.png}
  \caption{Calculated radiative heat-load distributions in a DEMO cross-section for two radiation-source assumptions \cite{Wenninger_2017}.}
  \label{fig:mapatoku3}
\end{figure}

Short transient events such as disruptions and edge-localized modes can produce surface heat fluxes far above steady-state values. Their duration is much shorter, so component survival depends not only on the cooling system but also on the thermal inertia, armour material and allowable transient surface temperature.

\subsubsection{Divertor heat load}
The divertor experiences the highest steady-state surface heat loads in a tokamak. ITER divertor targets are designed for local steady-state heat fluxes of approximately 10~MW/m$^2$, with still higher transient loads possible during ELMs, disruptions and vertical displacement events \cite{Loarte2003-zo,Li2019}. These conditions explain why divertor cooling concepts are evaluated separately from first-wall cooling.

Figure~\ref{fig:mapatoku4} summarizes representative magnitudes and time scales of divertor thermal loads. Figure~\ref{fig:mapatoku5} shows a calculated surface-temperature response during a millisecond-scale ELM, illustrating that transient loading can approach or exceed the melting limit of tungsten even when the time-averaged heat load is acceptable \cite{Hassanein2021-cg}.

\begin{figure}[h]
  \centering
  \begin{minipage}{0.5\textwidth}
      \centering
      \includegraphics[width=\linewidth]{Thermal-loads-on-the-divertor.png}
      \caption{Representative thermal loads on the ITER divertor \cite{Loarte2003-zo,Li2019}.}
      \label{fig:mapatoku4}
  \end{minipage}\hfill
  \begin{minipage}{0.45\textwidth}
      \centering
      \includegraphics[width=\linewidth]{div_load.png}
      \caption{Calculated thermal response of an ITER divertor surface during a 1~ms ELM \cite{Hassanein2021-cg}.}
      \label{fig:mapatoku5}
  \end{minipage}
\end{figure}

The ITER and DEMO cooling systems contain separate circuits for the first wall/blanket, divertor and vacuum vessel because these components operate under different thermal, hydraulic and nuclear-heating conditions. The detailed Primary Heat Transfer System (PHTS), Energy Storage System (ESS) and power-conversion architecture are outside the scope of this thesis; the following chapters therefore focus on the local cooling-channel geometries that ultimately determine the achievable surface heat flux.'''
s=s[:pe0]+new_pe+'\n\n'+s[pe1:]

s=s.replace('Cooling of plasma facing components in research fusion reactors is described in comparison to the challenges designing a full scale fusion power plant.', 'The actively cooled in-vessel components of Wendelstein~7-X provide a useful lower-heat-flux reference case for comparison with reactor-scale plasma-facing components.')
s=s.replace('its necessary', "it is necessary")
s=s.replace('dont require', 'do not require')
s=s.replace('around 0.4 to 1 kg.s$^{-1}$ ,', 'approximately 0.4--1~kg/s,')
s=s.replace('15-30~$^\\circ$C', '15--30~$^\\circ$C')

# 8) Hypervapotron claims citation and alternative citation spacing
hp_claim='''The term "vapotron" refers to a channel with cooling fins designed to enhance heat transfer from the heated wall to the cooling liquid. In a "supervapotron," the cooling fins are aligned parallel to the liquid's forced flow, allowing for a maximum heat flux of 3~MW/m$^2$. \nBy narrowing the gaps between the fins, this heat flux can be increased to 5~MW/m$^2$. In a "hypervapotron," the cooling fins are arranged perpendicular to the liquid flow, a design that promotes more intense vapor production in the slots and enables heat fluxes up to 20~MW/m$^2$.'''
hp_repl='''The term "vapotron" refers to a finned water-cooled channel in which the geometry promotes recirculation and nucleate boiling near the heated wall. Supervapotron variants use fins broadly aligned with the main flow, whereas hypervapotrons place deep slots transverse to the flow and thereby create intense recirculation within the cavities. Reported heat-flux capabilities depend strongly on pressure, velocity, subcooling and geometry; values from several MW/m$^2$ up to approximately 20~MW/m$^2$ have been demonstrated for optimized hypervapotron-type channels \cite{Ciric,Smolk2023}.'''
s=s.replace(hp_claim,hp_repl)
s=s.replace('20~MW/m$^2$\\cite{Gorbis1993}', '20~MW/m$^2$ \\cite{Gorbis1993}')
s=s.replace('''Each of these alternative solutions offers unique advantages for managing the extreme heat fluxes encountered in fusion reactors. A related design direction is the use of strongly structured or finned internal channels, including concepts investigated in the GyroSTEAM/STEAM cooling work, where geometry is optimized to increase heat-transfer area while maintaining acceptable structural deformation and hydraulic losses. Porous structures follow the same general design philosophy but extend it to a three-dimensional interconnected network; they are therefore treated separately in Section~\\ref{sec:porous_channels}.\nAnother broad field of alternative solutions for high heat flux cooling are porous media channels and other similar structures (the gyroid model or the triply periodic minimum surfaces), examined in this thesis \\cite{Saghir2024}.''','''Each of these alternatives seeks to increase the usable heat-transfer area or to intensify coolant mixing. The same design principle is used in highly structured internal cooling channels, including the STEAM/GyroSTEAM concept investigated in related work. Porous structures extend this approach to a three-dimensional interconnected network and are therefore treated separately in Section~\\ref{sec:porous_channels}. Related architected structures, including gyroids and other triply periodic minimal surfaces, are also being investigated for high-performance cooling \\cite{Saghir2024}.''')

# 9) TEALC: add heating subsection after table and before general experiment paragraph
marker='''\nThe experimental setup is designed to evaluate the hydraulic performance of various porous material samples.'''
heating=r'''
\subsubsection{Heat source and induction-heating methodology}
The high-heat-flux experiments associated with the doctoral work use electromagnetic induction as the external heat source. The method was selected because it provides contactless heating, allows thermocouples to be installed directly in the test specimen and can deliver a controllable load for repeated laboratory tests. Its main limitation is that the deposited power depends strongly on the electrical and magnetic properties of the heated material and is therefore not intrinsically uniform.

The induction-heating methodology was developed through coupled electromagnetic and thermal-flow simulations and subsequent experimental validation. Because CuCrZr couples only weakly to the induction field, ferromagnetic steel sheets were added to the heated body to increase power deposition. The numerical workflow used ANSYS Maxwell to calculate electromagnetic losses and transferred the resulting volumetric heat source to the thermal/CFD model. Temperatures measured inside the specimen were then used to verify the predicted thermal response \mycite{S2023}. Figure~\ref{fig:indukce} summarizes the developed numerical and experimental workflow.

\begin{figure}[ht!]
  \centering
  \includegraphics[width=13cm]{schema_indukce.jpg}
  \caption{Numerical and experimental induction-heating methodology developed for high-heat-flux testing \mycite{S2023}.}
  \label{fig:indukce}
\end{figure}

The same induction-heating principle was subsequently used for the porous-copper proof-of-concept experiment described in Chapter~12 \mycite{Smolk2024}.
'''
if marker in s:
    s=s.replace(marker,heating+marker,1)

# 10) CHF HEFEL: explicit loop role and instrumentation
s=s.replace('''The proof-of-concept measurements were performed on the Heat Flux Experimental Loop (HEFEL), a dedicated closed water loop developed for high-heat-flux testing and previously used for hypervapotron experiments \\cite{Smolk2023}. The loop provides controlled coolant flow through a replaceable test section while the specimen is heated by electromagnetic induction. Coolant conditions and solid temperatures are monitored during the test, enabling both hydraulic characterization and identification of the onset of boiling crisis.''','''The proof-of-concept measurements were performed on the Heat Flux Experimental Loop (HEFEL), a dedicated closed water loop developed for high-heat-flux testing and previously used for hypervapotron experiments \\cite{Smolk2023}. HEFEL is distinct from TEALC: it is configured specifically for heated tests approaching boiling crisis. A circulation pump drives water through a replaceable test section; coolant pressure, inlet temperature and flow rate are controlled and measured, while the specimen is heated by electromagnetic induction. Thermocouples embedded in the solid body record the thermal response. This instrumentation allows the hydraulic pressure drop and the onset of boiling crisis to be evaluated under the same controlled boundary conditions.''')

# 11) correct dimensional labels in porous-material table
s=s.replace('Forchheimer c. & Permeability\\\\', 'Forchheimer coefficient & Permeability\\\\')
s=s.replace('$d_p$ [mm] & $d_f$ [mm] & $\\epsilon  [\\%]$ & c [m$^{2}$] & K [-]', '$d_p$ [mm] & $d_f$ [mm] & $\\epsilon$ [\\%] & $\\beta$ [m$^{-1}$] & $K$ [m$^2$]')
s=s.replace('4.725199 . 10$^{-9}$', '$4.725199 \\times 10^{-9}$')

# 12) remove result-dump appendices; article PDFs are not present in the repository
app=s.index('\\clearpage\n\\part{Appendices}')
enddoc=s.index('\\end{document}',app)
new_app=r'''\clearpage
\part{Appendices}
\section*{Publications forming the basis of the dissertation}
\addcontentsline{toc}{section}{Publications forming the basis of the dissertation}
The full texts of the author's publications forming the basis of this dissertation are to be inserted in the submitted version of the thesis. Their complete bibliographic records, with all authors listed, are provided in the preceding section \textit{Publications of the Author}.

'''
s=s[:app]+new_app+s[enddoc:]

# 13) citation punctuation and simple percentage spacing
s=re.sub(r'\.\s*(\\(?:my)?cite\{[^{}]+\})', r' \1.', s)
s=re.sub(r'(?<![,~])(?<=\d)\\%', r'\\,\\%', s)

# 14) common marked prose/typos
repls={
'One of the case with comparable heat load is':'One engineering case with a comparable heat load is',
'Its important':'It is important',
'based on its magnitude':'based on their magnitude',
'heat load in DEMO first wall are going achieve':'heat loads on the DEMO first wall are expected to achieve',
'FW pannel':'first-wall panel',
'by he capillary effect':'by the capillary effect',
'one of the plasma heating system':'one of the plasma heating systems',
'3.1~MW of the total 3.6~MW are loaded':'Approximately 3.1~MW of the total 3.6~MW is deposited',
}
for a,b in repls.items():
    s=s.replace(a,b)

# Close the first title-page centering environment before the second title page.
s=s.replace('    \\thispagestyle{empty}\n\n\\pagebreak\n\n\n\\thispagestyle{empty}', '    \\thispagestyle{empty}\n\\end{center}\n\\pagebreak\n\n\\thispagestyle{empty}',1)
p.write_text(s)
print('wrote',p,'lines',len(s.splitlines()),'chars',len(s))
