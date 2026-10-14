from pathlib import Path
import re

path = Path('reserse.tex')
text = path.read_text(encoding='utf-8')

# Reusable red TODO marker for items that require author-supplied material.
macro = r'''\newcommand{\doplnit}[1]{%
  \par\medskip
  \noindent\textcolor{red}{\textbf{DOPLNIT:} #1}%
  \par\medskip
}
'''
if r'\newcommand{\doplnit}' not in text:
    marker = r'\usepackage{xcolor}'
    if marker not in text:
        raise RuntimeError('xcolor marker not found')
    text = text.replace(marker, marker + '\n' + macro, 1)

# HEFEL loop schematic: the source figure is not available in the repository.
hefel_todo = r'''\doplnit{Vložit schéma experimentální smyčky HEFEL. Ve schématu vyznačit směr proudění, hlavní komponenty smyčky, testovací sekci, měření průtoku, tlaku a teploty a polohu indukčního ohřevu. Schéma není v dostupných podkladech, proto jej nelze korektně doplnit automaticky.}

'''
hefel_marker = r'''\begin{figure}[ht!]
  \centering
  \includegraphics[width=12cm]{chf_1.png}'''
if hefel_todo.strip() not in text:
    if hefel_marker not in text:
        raise RuntimeError('HEFEL insertion marker not found')
    text = text.replace(hefel_marker, hefel_todo + hefel_marker, 1)

# Nukiyama curve / fit: insert after the first paragraph containing Nukiyama.
nuki_todo = r'''\doplnit{Doplnit zdrojovou Nukiyamovu varnou křivku a podle připomínky vedoucího případně také fit původních dat. Bez zdrojových dat nelze fit věrohodně vytvořit ani zkontrolovat.}
'''
if nuki_todo.strip() not in text:
    idx = text.lower().find('nukiyama')
    if idx == -1:
        raise RuntimeError('Nukiyama text not found')
    para_end = text.find('\n\n', idx)
    if para_end == -1:
        raise RuntimeError('Could not locate paragraph after Nukiyama')
    para_end += 2
    text = text[:para_end] + nuki_todo + '\n' + text[para_end:]

# Replace the previous Summary + Conclusion with a clear separation between
# concrete research results and the dissertation-level fulfilment of objectives.
replacement = r'''\part{Results}

This chapter summarizes the concrete outputs of the four principal research work packages presented in the dissertation. Detailed methods, intermediate results and discussion remain in the corresponding research chapters; only the principal quantitative and engineering outcomes are collected here.

\section{Controlled porous geometries: parametric numerical study}
\begin{itemize}
    \item A controlled family of substitute porous geometries was used to separate the influence of porosity $\varepsilon$ and tortuosity $\tau$ on hydraulic resistance.
    \item Permeability increased strongly with increasing porosity and decreased with increasing tortuosity. The fitted relationship was
    \[
    K = 9.439\times10^{-7}\,\tau^{-3.091}\varepsilon^{3.143}\;\mathrm{m^2},
    \qquad R^2_{\log K}=0.9531.
    \]
    \item The inertial contribution represented by the Forchheimer coefficient followed the opposite trend,
    \[
    \beta = 6.801\times10^{1}\,\tau^{1.661}\varepsilon^{-2.709}\;\mathrm{m^{-1}},
    \qquad R^2_{\log \beta}=0.9549.
    \]
    \item Validation against additively manufactured reference samples showed that the numerical methodology reproduces the measured pressure losses with engineering accuracy, generally within approximately 10\,\% over most of the investigated range.
\end{itemize}

\section{Experimental hydraulic characterization of real porous materials}
\begin{itemize}
    \item Commercial porous samples were characterized using microscopy and pressure-drop measurements and described using Darcy--Forchheimer coefficients.
    \item The experiments demonstrated that nominal descriptors such as porosity and PPI are not sufficient by themselves to uniquely predict the hydraulic behaviour of real porous structures.
    \item Samples with similar nominal properties exhibited different pressure-loss characteristics because the hydraulic response is also governed by pore connectivity, strut morphology and tortuosity.
    \item For engineering use, measured or validated values of permeability and the Forchheimer coefficient therefore provide a more reliable description than a single manufacturer-specified morphology parameter.
\end{itemize}

\section{MicroCT-based CFD of the real porous structure}
\begin{itemize}
    \item A real porous structure reconstructed from micro-computed tomography was used directly for detailed CFD and conjugate heat-transfer analysis.
    \item The reconstructed model reproduced the measured hydraulic behaviour with a difference of approximately 17\,\% and the thermal response with a difference of approximately 6\,\% under the investigated validation conditions.
    \item The material comparison showed a strong influence of solid thermal conductivity on heat spreading inside the porous structure. Copper distributed heat most effectively, whereas tin and alumina confined the thermal field closer to the loaded region.
    \item The introduced effective heat-sink height $h_{\mathrm{eff90}}$ showed that only a limited region of the porous matrix adjacent to the heated wall contributes substantially to heat removal, particularly at higher inlet velocities. This result provides a direct design criterion for avoiding unnecessarily thick porous inserts.
\end{itemize}

\section{High-heat-flux proof-of-concept experiment}
\begin{itemize}
    \item A plain CuCrZr cooling channel and a channel containing a porous copper insert were compared experimentally under identical hydraulic boundary conditions.
    \item The plain channel reached the boiling crisis at approximately 4~MW/m$^2$.
    \item The porous configuration remained thermally stable up to 4.7~MW/m$^2$, at which point the available induction-heating power became the limiting factor. The absolute CHF of the porous configuration was therefore not reached in the experiment.
    \item The experiment demonstrates an increased CHF margin of the porous configuration under the investigated conditions, while also showing the hydraulic penalty associated with the porous insert.
    \item Post-test inspection identified the quality of the soldered thermal contact between the porous copper and CuCrZr body as an important practical limitation that must be controlled in future samples.
\end{itemize}

\pagebreak
\part{Fulfilment of the Research Objectives and Scientific Contribution}

The purpose of this chapter is not to repeat the individual results, but to evaluate whether the objectives and hypotheses formulated in the Introduction were fulfilled and to identify the original scientific contribution of the dissertation.

\section{Fulfilment of the research objectives}

\subsection{Objective 1: Develop and experimentally validate numerical models for porous cooling channels}
\textbf{Status: Fulfilled.}
\begin{itemize}
    \item Substitute-geometry CFD models were validated against additively manufactured reference samples.
    \item A microCT-based model of the real structure was validated against both hydraulic and thermal measurements.
    \item The work therefore provides numerical approaches at two different levels of geometrical fidelity: an efficient parametrized model for systematic studies and a detailed reconstructed model for local transport analysis.
\end{itemize}

\subsection{Objective 2: Experimentally characterize the hydraulic and thermal behaviour of selected porous materials}
\textbf{Status: Fulfilled within the investigated operating range.}
\begin{itemize}
    \item Hydraulic characteristics were measured for the investigated porous samples and reduced to Darcy--Forchheimer parameters.
    \item Thermal behaviour was assessed through the validated microCT-based conjugate heat-transfer study and the high-heat-flux proof-of-concept experiment.
    \item The available CHF experiment established a lower bound for the porous-channel performance rather than its absolute CHF because the induction-heating power limit was reached first.
\end{itemize}

\subsection{Objective 3: Quantify the influence of microstructural parameters on pressure loss and heat transfer}
\textbf{Status: Fulfilled, with an important qualification for real foams.}
\begin{itemize}
    \item For controlled geometries, quantitative correlations between porosity, tortuosity, permeability and inertial resistance were obtained.
    \item For real porous materials, the experiments showed that porosity and PPI alone are insufficient predictors. Connectivity, strut geometry and tortuosity must also be captured, or the hydraulic parameters must be measured directly.
    \item The microCT study further demonstrated the role of solid thermal conductivity and active porous-layer thickness in heat removal.
\end{itemize}

\subsection{Objective 4: Assess advantages and limitations relative to conventional high-heat-flux cooling concepts}
\textbf{Status: Partially fulfilled experimentally and completed by engineering comparison.}
\begin{itemize}
    \item The principal demonstrated advantage is the increased CHF margin relative to the tested plain channel together with enhanced internal heat-transfer area and liquid redistribution.
    \item The principal disadvantages are increased pressure loss, strong sensitivity to microstructure and the additional manufacturing challenge of obtaining a reliable thermal joint between the porous insert and the cooled wall.
    \item The dissertation does not contain a direct experimental comparison with swirl-tube or hypervapotron geometries; comparison with these established concepts is therefore based on the literature review rather than on a common experimental campaign.
\end{itemize}

\subsection{Objective 5: Formulate design and optimization recommendations}
\textbf{Status: Fulfilled.}
\begin{itemize}
    \item Do not select porous materials using porosity or PPI alone; use measured/validated permeability and Forchheimer coefficients together with geometrical characterization.
    \item Optimize hydraulic resistance and heat-transfer enhancement simultaneously, because improving one quantity by increasing the amount or complexity of porous material can penalize the other.
    \item Avoid porous layers substantially thicker than the thermally active region identified by $h_{\mathrm{eff90}}$ unless another design requirement justifies the additional material.
    \item Treat the thermal contact between the porous insert and the cooled wall as a primary design parameter rather than as a secondary manufacturing detail.
    \item For final component design, combine pressure-drop experiments or validated CFD with conjugate heat-transfer analysis and high-heat-flux testing under representative operating conditions.
\end{itemize}

\section{Evaluation of the research hypotheses}

\subsection{H1: Hydraulic resistance does not constitute a fundamental limitation if the porous geometry is optimized}
\textbf{Evaluation: Supported within the investigated parameter range.}

The porous structures produced substantially higher hydraulic losses than smooth channels, but these losses were systematically related to the geometry through permeability and the Forchheimer coefficient. The results show that hydraulic resistance is a critical design constraint, but not an intrinsically prohibitive one when the porous structure and operating point are optimized together.

\subsection{H2: Microstructural characteristics can be used to predict hydraulic behaviour}
\textbf{Evaluation: Partially confirmed.}

The controlled numerical study established clear quantitative relationships between porosity, tortuosity and hydraulic parameters. The experiments on real foams, however, showed that porosity and PPI alone do not uniquely determine the hydraulic response. The hypothesis is therefore valid only when the microstructural description is sufficiently rich to include the geometrical features controlling flow resistance.

\subsection{H3: Porous structures increase the critical heat-flux margin}
\textbf{Evaluation: Supported qualitatively; the absolute porous-channel CHF was not determined.}

The plain channel reached CHF at approximately 4~MW/m$^2$, whereas the porous sample remained stable at 4.7~MW/m$^2$. The experiment therefore demonstrates an increased CHF margin under the investigated conditions. Because the available heating power was exhausted before CHF occurred in the porous sample, the exact enhancement factor cannot be stated from the present dataset.

\section{Original scientific contribution}
The principal original contributions of the dissertation are summarized as follows:
\begin{enumerate}
    \item Quantitative correlations linking controlled porous geometry, porosity and tortuosity to Darcy--Forchheimer hydraulic parameters over a broad investigated porosity range.
    \item Demonstration that conventional nominal foam descriptors such as porosity and PPI are insufficient for reliable hydraulic prediction of real porous materials without additional morphological information or direct calibration.
    \item Development and validation of a microCT-based CFD methodology that resolves the real porous geometry and enables local conjugate heat-transfer analysis, including the definition of the effective heat-sink height $h_{\mathrm{eff90}}$.
    \item Experimental proof of concept showing a higher demonstrated CHF margin for a porous copper cooling channel than for a plain CuCrZr channel under the investigated boundary conditions.
    \item A combined numerical--experimental design framework in which porous cooling structures are evaluated simultaneously from the hydraulic, thermal and manufacturability perspectives.
\end{enumerate}

\pagebreak
\part{Conclusion}

\section{Main conclusions}
\begin{enumerate}
    \item Porous cooling channels can extend the thermal operating envelope of water-cooled high-heat-flux components, but the benefit is inseparable from increased hydraulic resistance.
    \item The hydraulic response of real porous media cannot be predicted reliably from porosity or PPI alone. Permeability, inertial resistance and a sufficiently detailed description of the real microstructure are required.
    \item Detailed microCT-based simulations show that only part of the porous volume may be thermally active. Consequently, increasing the porous-layer thickness does not automatically improve heat removal and can unnecessarily increase pressure loss and material volume.
    \item The proof-of-concept experiment demonstrated a higher CHF margin for the porous sample: the plain channel reached CHF at approximately 4~MW/m$^2$, while the porous channel remained stable up to the experimental limit of 4.7~MW/m$^2$.
    \item The practical performance of a porous cooling concept depends not only on the porous morphology but also on manufacturing quality, particularly the thermal contact between the porous insert and the cooled structural material.
\end{enumerate}

\section{Engineering implication}
The results support porous materials as a credible candidate for advanced fusion cooling channels, particularly in applications where maintaining liquid contact with the heated wall close to the boiling limit is more important than minimizing pumping power. The most promising design route is therefore not to maximize porosity, surface area or foam thickness independently, but to optimize the complete coupled system: microstructure, hydraulic operating point, thermally active layer thickness, material conductivity and the thermal joint to the cooled wall.

\section{Scope of the conclusion}
The dissertation establishes the hydraulic trends, validates numerical approaches at multiple geometrical scales and demonstrates an increased CHF margin in a proof-of-concept experiment. It does not determine the absolute CHF of the porous configuration under reactor-relevant conditions, nor does it provide a direct experimental comparison with established swirl-tube or hypervapotron concepts. These points define the most important continuation of the work rather than invalidating the conclusions reached within the investigated parameter range.

\pagebreak

\part{Bibliography}'''

pattern = re.compile(r'\\section\{Summary\}.*?\\part\{Bibliography\}', re.S)
text, n = pattern.subn(lambda m: replacement, text, count=1)
if n != 1:
    raise RuntimeError(f'Expected to replace one Summary/Conclusion block, replaced {n}')

# Mark the missing publication PDFs in the appendix.
appendix_old = r'''The full texts of the author's publications forming the basis of this dissertation are to be inserted in the submitted version of the thesis. Their complete bibliographic records, with all authors listed, are provided in the preceding section \textit{Publications of the Author}.'''
appendix_new = r'''\doplnit{Do odevzdávané verze vložit plné texty publikací tvořících podklad disertace. Jejich PDF soubory nejsou v repozitáři, proto je nelze vložit automaticky.}

Their complete bibliographic records, with all authors listed, are provided in the preceding section \textit{Publications of the Author}.'''
if appendix_old not in text:
    raise RuntimeError('Appendix publication placeholder not found')
text = text.replace(appendix_old, appendix_new, 1)

path.write_text(text, encoding='utf-8')
print('Restructured results/objectives/conclusion and inserted author TODO markers.')
