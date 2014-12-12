all: markdown

markdown: final-report pdf-nips

final-report: src/final-report.md
	mkdir -p build/
	pandoc src/final-report.md -o build/final-report.tex

pdf: template/templateacm.tex build
	cp template/sig-alternate.cls ./
	pdflatex template/templateacm.tex
	bibtex templateacm
	pdflatex template/templateacm.tex
	pdflatex template/templateacm.tex
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f related.bib
	rm -f sig-alternate.cls
	mv templateacm.pdf final-report.pdf

pdf-nips: template/nips2014.tex build
	cp template/nips14submit_e.sty ./
	pdflatex template/nips2014.tex
	bibtex nips2014
	pdflatex template/nips2014.tex
	pdflatex template/nips2014.tex
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f related.bib
	rm -f nips14submit_e.sty
	mv nips2014.pdf final-report.pdf

clean:
	rm -rf build/*
	rm -f *.log *.aux *.out *.bbl *.blg
	