
IMGS=path.png path2.png

%.png: %.tex
	pdflatex $<
	convert -density 300 $*.pdf -quality 90 -background white -flatten $@

all: $(IMGS)

clean:
	rm -f *.aux *.fdb_latexmk *.fls *.log *.pdf *.png

publish: $(IMGS)
	cp $(IMGS) ../assets

