all: markdown

markdown: progress pdf

progress: src/progress.md
	mkdir -p build/
	pandoc src/progress.md -o build/progress.tex

pdf: template/templateacm.tex build
	cp template/sig-alternate.cls ./
	pdflatex template/templateacm.tex
	bibtex templateacm
	pdflatex template/templateacm.tex
	pdflatex template/templateacm.tex
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f related.bib
	rm -f sig-alternate.cls
	mv templateacm.pdf progress.pdf

clean:
	rm -rf build/*
	rm -f *.log *.aux *.out *.bbl *.blg
	