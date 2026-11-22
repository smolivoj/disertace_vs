from pathlib import Path
import re
import urllib.request
import fitz
url = "https://www.avestia.com/FFHMT2023_Proceedings/files/paper/FFHMT_181.pdf"
pdf = Path("FFHMT_181_source.pdf")
urllib.request.urlretrieve(url, str(pdf))
doc = fitz.open(str(pdf))
page = doc[1]
matches = page.search_for("Fig. 2:")
if not matches:
    raise RuntimeError("Figure 2 caption not found")
caption = matches[0]
print("Caption:", caption, "page:", page.rect)
candidate = []
for info in page.get_images(full=True):
    for rect in page.get_image_rects(info[0]):
        print("Placed image:", rect)
        if rect.y1 <= caption.y0 + 5 and rect.y1 >= caption.y0 - 350 and rect.x0 < page.rect.width/2 and rect.width > 80 and rect.height > 70:
            candidate.append(rect)
if candidate:
    rect = max(candidate, key=lambda r:r.width*r.height)
    if rect.x1 > page.rect.width/2 + 15:
        rect = fitz.Rect(rect.x0,rect.y0,page.rect.width/2-8,rect.y1)
else:
    rect = fitz.Rect(35,caption.y0-250,page.rect.width/2-8,caption.y0-8)
rect = rect & page.rect
print("Selected crop:",rect)
if rect.is_empty or rect.height < 70 or rect.width < 80:
    raise RuntimeError("Invalid figure crop")
page.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect,alpha=False).save("hefel_schematic.png")
src=Path("reserse.tex")
text=src.read_text(encoding="utf-8")
pattern=r"\\doplnit\{Vložit schéma experimentální smyčky HEFEL\.[^\n]*\}"
replacement=r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.78\textwidth]{hefel_schematic.png}
  \caption{Schematic of the HEFEL experimental loop, including the test section, induction heater, flowmeter, circulation pump, auxiliary electric heater and cooler. Reproduced from \mycite{Smolk2023}.}
  \label{fig:hefel_schematic}
\end{figure}

The arrangement of the HEFEL experimental loop is shown in Figure~\ref{fig:hefel_schematic}. The heated sample is located in the replaceable test section, with pressure and temperature monitored on both sides. The induction heater supplies thermal power to the sample, while the flowmeter, pump, electric heater and cooler enable control of the water flow and inlet conditions."""
text,n=re.subn(pattern,lambda m:replacement,text,count=1)
if n!=1: raise RuntimeError(f"Expected one HEFEL TODO, found {n}")
src.write_text(text,encoding="utf-8")
pdf.unlink(missing_ok=True)
print("Inserted HEFEL figure and removed TODO.")
