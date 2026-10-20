# latexmk configuration for the thesis. Build with:  latexmk -pdfxe report.tex
#
# XeLaTeX (TU Delft house-style fonts) + biber (biblatex backend). latexmk hashes the
# sources and runs only the passes that are needed, so a prose edit is one fast pass.
# batchmode sends the Underfull/Overfull and font-warning firehose to report.log instead
# of the terminal; latexmk still parses the log and prints a final summary.
# -halt-on-error makes a real error fail fast instead of waiting at the "?" prompt.

$pdf_mode = 5;
$xelatex  = 'xelatex -interaction=batchmode -halt-on-error -synctex=1 %O %S';
$pdflatex = 'pdflatex -interaction=batchmode -halt-on-error -synctex=1 %O %S';
$biber    = 'biber %O %S';
$clean_ext = 'bbl run.xml synctex.gz';

# Useful commands:
#   latexmk -pdfxe report.tex       minimum passes
#   latexmk -C                      wipe generated files
#   latexmk -pdfxe -gg report.tex   force a full rebuild
#   latexmk -pdf report.tex         pdfLaTeX fallback with free fonts
