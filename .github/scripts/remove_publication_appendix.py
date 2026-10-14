from pathlib import Path
import re

p = Path('reserse.tex')
text = p.read_text(encoding='utf-8')
pattern = re.compile(r'\n\\clearpage\n\\part\{Appendices\}\n\\section\*\{Publications forming the basis of the dissertation\}.*?\n\\end\{document\}', re.S)
new = '\n\\end{document}'
text, n = pattern.subn(new, text, count=1)
if n != 1:
    raise RuntimeError(f'Expected one publication appendix block, found {n}')
p.write_text(text, encoding='utf-8')
print('Removed publication appendix block; Publications of the Author remains unchanged.')
