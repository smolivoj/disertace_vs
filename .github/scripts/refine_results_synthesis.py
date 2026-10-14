from pathlib import Path
import re

p = Path('reserse.tex')
text = p.read_text(encoding='utf-8')

# Remove obsolete/red TODOs that do not belong to the author's remaining work.
text = re.sub(r'\\doplnit\{Doplnit zdrojovou Nukiyamovu varnou křivku.*?\}\s*', '', text, flags=re.S)
text = re.sub(r'\\clearpage\s*\\part\{Appendices\}.*?\\end\{document\}', r'\\end{document}', text, flags=re.S)

# Tighten two CHF statements without changing the underlying data.
text = text.replace(
    'Increasing the heat flux on the tested samples resulted in various results.',
    'The two samples showed different thermal responses as the imposed heat flux was increased.'
)
text = text.replace(
    'Although the exact value of the critical heat flux value of the porous sample was not found, the results clearly indicate that the CHF value of the porous sample is significantly increased compared to that of the plain sample.',
    'The absolute CHF of the porous sample was not reached. The experiment therefore demonstrates only that, under the investigated boundary conditions, the porous configuration sustained a higher heat flux than the plain channel before the available heating power became the limiting factor.'
)

# Replace the complete dissertation-level results/conclusion block by a more explicit
# separation of concrete results, interpretation, cross-study synthesis, objectives,
# hypotheses, scientific contribution and concise conclusion.
replacement = r'''\part{Results}

This chapter collects the principal outputs of the four research work packages. The purpose is to state the concrete findings and their immediate interpretation without repeating the full methods and intermediate discussion given in the preceding chapters.

\section{Controlled porous geometries: parametric numerical study}
\subsection*{Principal results}
\begin{itemize}
    \item A controlled family of substitute porous geometries was used to isolate the influence of porosity $\varepsilon$ and tortuosity $\tau$ on hydraulic resistance.
    \item Permeability increased with porosity and decreased with tortuosity. The fitted relationship was
    \[
    K = 9.439\times10^{-7}\,\tau^{-3.091}\varepsilon^{3.143}\;\mathrm{m^2},
    \qquad R^2_{\log K}=0.9531.
    \]
    \item The inertial contribution represented by the Forchheimer coefficient followed the opposite tendency,
    \[
    \beta = 6.801\times10^{1}\,\tau^{1.661}\varepsilon^{-2.709}\;\mathrm{m^{-1}},
    \qquad R^2_{\log \beta}=0.9549.
    \]
    \item Validation against additively manufactured reference samples showed agreement of the predicted and measured pressure losses generally within approximately 10\,\% over most of the investigated range.
\end{itemize}

\subsection*{Interpretation}
The controlled geometry study establishes the clearest causal relationship obtained in this dissertation: hydraulic performance cannot be attributed to porosity alone. Tortuosity modifies both the viscous and inertial parts of the pressure loss and must therefore be considered together with porosity. The value of the substitute geometries is that they remove much of the morphological ambiguity present in commercial foams and make it possible to distinguish these effects independently. At the same time, the correlations are valid for the investigated family of geometries and should not be interpreted as universal correlations for arbitrary porous materials.

\section{Experimental hydraulic characterization of real porous materials}
\subsection*{Principal results}
\begin{itemize}
    \item Commercial porous samples were characterized by microscopy and pressure-drop measurements and described using Darcy--Forchheimer parameters.
    \item Materials with similar nominal porosity or PPI exhibited different pressure-loss characteristics.
    \item Porosity and PPI were therefore insufficient as stand-alone descriptors for predicting the hydraulic response of the investigated real porous materials.
    \item Measured permeability and Forchheimer coefficients provided a more useful engineering description of the tested samples than a single manufacturer-specified morphology parameter.
\end{itemize}

\subsection*{Interpretation}
This experimental result provides an important qualification to the parametric numerical study. The controlled study shows that hydraulic behaviour can be related quantitatively to well-defined geometrical parameters, whereas the real materials demonstrate that common nominal descriptors do not contain enough information to reconstruct those governing geometrical features. In practical design, the missing information is associated with features such as pore connectivity, local constrictions, strut morphology and effective tortuosity. Consequently, real porous materials require either richer geometrical characterization or direct hydraulic calibration before their pressure losses can be predicted reliably.

\section{MicroCT-based CFD of the real porous structure}
\subsection*{Principal results}
\begin{itemize}
    \item The real porous geometry reconstructed from micro-computed tomography was used directly for detailed CFD and conjugate heat-transfer analysis.
    \item The reconstructed model reproduced the measured hydraulic behaviour with a difference of approximately 17\,\% and the thermal response with a difference of approximately 6\,\% under the investigated validation conditions.
    \item The material comparison showed a strong effect of solid thermal conductivity on heat spreading inside the porous structure. Copper distributed heat most effectively, while lower-conductivity materials confined the thermal field closer to the heated region.
    \item The effective heat-sink height $h_{\mathrm{eff90}}$ showed that only a limited region of the porous matrix adjacent to the heated wall contributes substantially to heat removal, particularly at higher inlet velocities.
\end{itemize}

\subsection*{Interpretation}
The microCT study bridges the gap between the idealized and real material descriptions. Unlike a porous-zone model, the reconstructed geometry resolves the local flow paths and solid matrix directly and therefore captures effects that cannot be represented by porosity or PPI alone. The results also show that increasing the total porous volume does not necessarily increase useful heat transfer: once the thermally active region becomes thin relative to the total foam thickness, additional material contributes little to heat removal while it can still contribute to hydraulic resistance and manufacturing complexity. The quantity $h_{\mathrm{eff90}}$ is therefore useful primarily as a design interpretation of the simulations rather than as a universal material constant.

\section{High-heat-flux proof-of-concept experiment}
\subsection*{Principal results}
\begin{itemize}
    \item A plain CuCrZr cooling channel and a channel containing a porous copper insert were compared experimentally under identical hydraulic boundary conditions.
    \item The plain channel reached boiling crisis at approximately 4~MW/m$^2$.
    \item The porous configuration remained thermally stable up to 4.7~MW/m$^2$, where the available induction-heating power became the limiting factor. The absolute CHF of the porous configuration was therefore not determined.
    \item The porous insert introduced a hydraulic penalty, while post-test inspection also identified the quality of the soldered thermal contact as an important manufacturing limitation.
\end{itemize}

\subsection*{Interpretation}
The experiment provides a proof of concept rather than a complete CHF characterization. It demonstrates that, for the investigated samples and operating conditions, the porous channel sustained a heat flux above the CHF observed for the plain channel. It does not determine the absolute CHF enhancement factor and does not separate the contributions of capillary transport, phase redistribution, local mixing and solid heat spreading. The result is nevertheless important because it connects the preceding hydraulic and numerical studies to the high-heat-flux operating regime for which the cooling concept is ultimately intended.

\pagebreak
\part{Synthesis and Discussion of the Research Results}

\section{Progression from controlled geometry to high-heat-flux demonstration}
The four research work packages form a sequence of increasing geometrical and experimental realism. The substitute geometries first isolate the effects of porosity and tortuosity under controlled conditions. Experiments on commercial porous materials then show the limitation of transferring simple morphology descriptors directly to real structures. The microCT-based CFD resolves the actual geometry and provides local information about flow and heat transfer that cannot be obtained from bulk pressure-drop data alone. Finally, the high-heat-flux experiment tests whether the porous concept retains a thermal advantage when approaching boiling crisis.

This progression is central to the interpretation of the dissertation. No single model or experiment is sufficient by itself. The idealized geometries are suitable for identifying trends, the hydraulic experiments are necessary for characterizing real materials, the microCT model explains local transport in the real structure, and the CHF experiment demonstrates the relevance of the concept under severe thermal loading.

\section{Hydraulic resistance versus thermal benefit}
The main engineering trade-off identified by the work is the competition between thermal enhancement and hydraulic resistance. Increasing the complexity or amount of porous material may increase internal heat-transfer area and promote liquid redistribution, but it simultaneously increases the pressure loss. The results therefore do not support maximizing porosity, foam thickness or surface area independently. A useful porous cooling design must be selected as a coupled hydraulic--thermal problem.

The parametric correlations provide a quantitative description of this trade-off for the controlled geometries. The real-material experiments then show why this trade-off cannot be evaluated from porosity or PPI alone. For a practical component, permeability and inertial resistance must either be measured or obtained from a numerical model that resolves enough of the real geometry to reproduce the hydraulic behaviour.

\section{Role of solid thermal conductivity and active porous volume}
The microCT calculations show that the solid matrix participates directly in heat spreading and that this contribution depends strongly on material thermal conductivity. At the same time, the effective heat-sink-height analysis indicates that only a fraction of the total porous volume may carry most of the transferred heat. These two findings must be considered together: a high-conductivity matrix can distribute heat efficiently, but simply increasing the foam thickness does not guarantee additional benefit once the thermally active region is already contained within a much thinner layer.

This result provides a direct design implication from the available data. Porous-layer thickness should be treated as an optimization variable and should not be chosen solely from manufacturing convenience or the assumption that more porous material automatically provides more cooling capacity.

\section{Interpretation of the CHF proof of concept}
The high-heat-flux experiment supports the use of porous structures close to the boiling limit, but the conclusion must remain within the experimental evidence. The plain channel reached CHF at approximately 4~MW/m$^2$, whereas the porous channel remained stable to the maximum applied heat flux of 4.7~MW/m$^2$. Because the heating system reached its power limit first, the CHF of the porous configuration is known only to be above the maximum heat flux achieved in this campaign.

The experiment therefore demonstrates a higher \emph{observed operating margin} for the porous configuration, not a quantified universal CHF enhancement factor. The measurements also do not identify one unique physical mechanism responsible for the improvement. Capillary rewetting, flow redistribution, mixing and solid heat spreading remain plausible and mutually interacting mechanisms. Separating them would require additional dedicated experiments, which are outside the scope of this dissertation and are not necessary for the proof-of-concept conclusion established here.

\section{Limits of generalization}
The results define a consistent engineering picture but they should not be generalized beyond the investigated geometries, materials and operating conditions without validation. The fitted permeability and Forchheimer correlations describe the controlled substitute-geometry family. The commercial-foam experiments demonstrate that simpler nominal descriptors are insufficient for real materials. The microCT results apply to the reconstructed samples and boundary conditions, while the CHF experiment establishes a comparative result for the tested plain and porous channels rather than a universal porous-channel CHF correlation.

These limitations do not reduce the value of the results; they define the appropriate level at which each result can be used. The main transferable outcome is therefore the combined methodology and design logic rather than one universal numerical coefficient.

\pagebreak
\part{Fulfilment of the Research Objectives and Scientific Contribution}

\section{Fulfilment of the research objectives}

\subsection{Objective 1: Develop and experimentally validate numerical models capable of predicting flow and heat transfer inside porous cooling channels}
\textbf{Status: Fulfilled within the investigated geometries and operating range.}
\begin{itemize}
    \item The substitute-geometry CFD methodology was validated against additively manufactured reference samples using pressure-drop measurements.
    \item The microCT-based model was validated against hydraulic measurements and against the measured thermal response.
    \item Together, the two modelling levels provide a parametric tool for identifying trends and a detailed geometry-resolved tool for local transport analysis.
\end{itemize}

\subsection{Objective 2: Experimentally characterize the hydraulic and thermal behaviour of selected porous materials}
\textbf{Status: Fulfilled for the selected materials and tested conditions.}
\begin{itemize}
    \item Hydraulic characteristics of the investigated porous materials were measured and reduced to Darcy--Forchheimer parameters.
    \item Thermal behaviour was assessed by comparison with the validated microCT-based conjugate heat-transfer model and by the high-heat-flux proof-of-concept experiment.
    \item The porous-sample CHF itself was not reached; therefore the experiment defines a demonstrated lower bound of thermal performance rather than the absolute CHF of the porous configuration.
\end{itemize}

\subsection{Objective 3: Quantify the influence of key microstructural parameters on pressure losses and heat-transfer performance}
\textbf{Status: Fulfilled for controlled geometries; only partially transferable to real foams.}
\begin{itemize}
    \item Quantitative correlations between porosity, tortuosity, permeability and inertial resistance were obtained for the controlled geometry family.
    \item Measurements on real porous samples showed that porosity and PPI alone are not sufficient to transfer these relationships directly to commercial foams.
    \item The microCT analysis demonstrated the importance of solid thermal conductivity and of the thermally active porous-layer thickness for heat transfer.
\end{itemize}

\subsection{Objective 4: Assess advantages and limitations of porous cooling channels relative to conventional high-heat-flux cooling concepts}
\textbf{Status: Partially fulfilled by direct experiment and completed by engineering interpretation.}
\begin{itemize}
    \item The direct experiment demonstrated a higher observed heat-flux margin for the porous channel than for the tested plain CuCrZr channel.
    \item The principal limitations identified experimentally and numerically are higher pressure loss, sensitivity to microstructure and the quality of the thermal joint between the porous insert and the cooled wall.
    \item No direct common-rig comparison with swirl-tube or hypervapotron geometries was performed; conclusions relative to these established concepts therefore remain based on the literature review and engineering comparison rather than a direct experiment.
\end{itemize}

\subsection{Objective 5: Formulate recommendations for design and optimization of porous cooling structures}
\textbf{Status: Fulfilled on the basis of the combined numerical and experimental results.}
\begin{itemize}
    \item Porous materials should not be selected from porosity or PPI alone; permeability and Forchheimer resistance should be measured or validated numerically.
    \item Hydraulic resistance and heat-transfer enhancement must be optimized simultaneously.
    \item Porous layers substantially thicker than the thermally active region identified by $h_{\mathrm{eff90}}$ should be avoided unless another design requirement justifies the added material.
    \item Thermal contact between the porous insert and the cooled wall must be treated as a primary design parameter.
    \item Final component assessment should combine hydraulic characterization, validated CFD and high-heat-flux testing rather than relying on one morphology descriptor or one porous-medium correlation.
\end{itemize}

\section{Evaluation of the research hypotheses}

\subsection{H1: Hydraulic resistance does not constitute a fundamental limitation if the porous geometry is optimized}
\textbf{Evaluation: Supported within the investigated parameter range.}

The investigated porous structures produced higher hydraulic losses than smooth channels, but these losses varied systematically with geometry and were described by permeability and the Forchheimer coefficient. The results therefore support the hypothesis that hydraulic resistance is a design constraint rather than an automatic disqualification of the concept. The conclusion is limited to the investigated geometries and operating range and does not imply that every porous structure is hydraulically acceptable.

\subsection{H2: Microstructural characteristics can be used to predict hydraulic behaviour prior to flow testing}
\textbf{Evaluation: Not confirmed in its original general form.}

For the controlled substitute geometries, porosity and tortuosity were quantitatively related to hydraulic parameters. For the real porous materials, however, the descriptors available from conventional characterization, particularly porosity and PPI, did not uniquely determine the measured hydraulic response. The hypothesis is therefore valid only when the microstructural description contains the geometrical information that actually controls flow resistance, or when the material is calibrated directly by hydraulic testing. This negative qualification is itself an important result of the dissertation because it identifies the limit of simplified morphology-based prediction.

\subsection{H3: Porous structures increase the critical heat-flux margin}
\textbf{Evaluation: Supported by the comparative proof of concept, but not quantified as an absolute CHF enhancement factor.}

The plain channel reached CHF at approximately 4~MW/m$^2$, whereas the porous sample remained stable at 4.7~MW/m$^2$. The experiment therefore supports the hypothesis that the porous configuration can extend the operating margin before boiling crisis under the investigated conditions. Because the heating-power limit was reached before CHF occurred in the porous sample, the absolute porous-channel CHF and the exact enhancement factor were not determined.

\section{Original scientific contribution}
The original scientific contribution of the dissertation can be summarized in five connected points:
\begin{enumerate}
    \item \textbf{Controlled hydraulic correlations.} Quantitative relationships were obtained between porosity, tortuosity and Darcy--Forchheimer hydraulic parameters for the investigated substitute-geometry family, allowing the independent effects of these geometrical variables to be interpreted.
    \item \textbf{Identification of the limit of nominal foam descriptors.} Experiments on real porous materials demonstrated that porosity and PPI alone are insufficient for reliable prediction of hydraulic behaviour, establishing the need for richer morphology information or direct hydraulic calibration.
    \item \textbf{Geometry-resolved microCT methodology.} A microCT-based CFD approach was developed and validated for both hydraulic and thermal behaviour of the real porous structure, enabling local transport mechanisms to be studied without replacing the foam by a homogeneous porous zone.
    \item \textbf{Effective heat-sink-height interpretation.} The quantity $h_{\mathrm{eff90}}$ was used to describe the thermally active part of the porous structure and to show that additional foam thickness does not necessarily produce a proportional thermal benefit.
    \item \textbf{High-heat-flux proof of concept.} A porous copper cooling channel sustained the maximum applied heat flux of 4.7~MW/m$^2$ without reaching CHF, while the plain reference channel reached CHF at approximately 4~MW/m$^2$, demonstrating a higher observed operating margin of the porous concept under the investigated conditions.
\end{enumerate}

The broader contribution is the connection of these five results into one design framework. The dissertation shows that a porous cooling channel cannot be assessed from thermal performance or morphology alone: geometrical characterization, hydraulic resistance, local heat transfer, material conductivity, thermal contact and boiling-limit behaviour must be considered together.

\pagebreak
\part{Conclusion}

\section{Main conclusions}
\begin{enumerate}
    \item Porous cooling structures provide a credible route to extending the thermal operating margin of water-cooled high-heat-flux components, but the thermal benefit is coupled directly to increased hydraulic resistance.
    \item For controlled geometries, porosity and tortuosity provide a strong quantitative description of hydraulic behaviour. For real foams, common nominal parameters such as porosity and PPI are not sufficient by themselves, and hydraulic calibration or richer geometrical information is required.
    \item Geometry-resolved microCT simulations show that solid thermal conductivity and the thickness of the thermally active porous region strongly influence heat removal. Increasing total foam thickness alone is therefore not a reliable route to higher performance.
    \item The high-heat-flux proof-of-concept experiment demonstrated a higher observed operating margin for the porous channel: the plain reference reached CHF at approximately 4~MW/m$^2$, whereas the porous channel remained stable up to the available experimental limit of 4.7~MW/m$^2$.
    \item The performance of a practical porous cooling component depends not only on pore morphology but also on manufacturing quality, particularly the thermal contact between the porous insert and the structural material.
\end{enumerate}

\section{Design implications}
The results indicate that porous cooling structures should be designed as coupled hydraulic--thermal systems. The objective is not to maximize one parameter such as porosity, surface area or foam thickness, but to select a structure that provides an acceptable balance between permeability, inertial resistance, active heat-transfer volume, solid heat spreading and manufacturing quality. The combined use of hydraulic measurements, validated CFD and high-heat-flux testing provides a practical route for this optimization.

\section{Scope of the conclusions}
The conclusions are restricted to the investigated samples, geometries and operating conditions. The work does not provide a universal porous-medium pressure-loss correlation, does not determine the absolute CHF of the porous proof-of-concept sample and does not experimentally compare the porous concept with swirl-tube or hypervapotron channels in a common test rig. These are boundaries of the available dataset, not missing steps required to support the principal conclusions of this dissertation.

\section{Overall outcome}
Taken together, the work demonstrates why porous cooling cannot be reduced to the simple statement that a larger internal area produces better heat transfer. The hydraulic response depends on the real flow-path geometry, the thermal response depends on both fluid transport and solid heat spreading, and the useful porous volume can be substantially smaller than the total installed volume. Within these constraints, the proof-of-concept experiment shows that the concept can provide additional margin close to the boiling limit. The principal outcome of the dissertation is therefore a physically consistent route from porous microstructure to hydraulic characterization, local heat-transfer analysis and high-heat-flux performance assessment.

\pagebreak

\part{Bibliography}'''

pattern = re.compile(r'\\part\{Results\}.*?\\part\{Bibliography\}', re.S)
text, n = pattern.subn(lambda m: replacement, text, count=1)
if n != 1:
    raise RuntimeError(f'Expected one Results-to-Bibliography block, replaced {n}')

p.write_text(text, encoding='utf-8')
print('Refined dissertation-level results, synthesis, objectives, hypotheses and conclusion.')
