TEX := mr_rdt_coupling_theory.tex
PDF := $(TEX:.tex=.pdf)

LATEXMK := latexmk
LATEXMK_FLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all clean distclean

all: $(PDF)

$(PDF): $(TEX)
	$(LATEXMK) $(LATEXMK_FLAGS) $(TEX)

clean:
	$(LATEXMK) -c $(TEX)

distclean:
	$(LATEXMK) -C $(TEX)
