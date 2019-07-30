all : slides.pdf

slides.pdf : slides.tex $(wildcard graphics/*.eps)
	latex $<
	dvipdf slides

.PHONY : clean cleanall

clean :
	rm -f slides.aux slides.log slides.out slides.toc slides.dvi

cleanall : clean
	rm -f slides.pdf
