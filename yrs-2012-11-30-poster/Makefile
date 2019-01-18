.PHONY: all clean cleanall

all: poster.pdf

poster.pdf: poster.tex posterAccelerator.tex posterAcknowledgments.tex posterAsymmetry.tex posterBeamProfile.tex posterNumbers.tex posterPolarLosses.tex posterPolarPrinciples.tex posterPolarimeters.tex posterPolarization.tex posterProtonSpin.tex posterRhic.tex posterSummary.tex
	latexmk -pdfdvi poster.tex

clean:
	latexmk -c
	@rm -f poster.dvi a0header.ps

cleanall: clean
	@rm -f poster.pdf
