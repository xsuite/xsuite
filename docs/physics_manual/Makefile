TEX := physics_man.tex
PDF := $(TEX:.tex=.pdf)

LATEXMK := latexmk
LATEXMK_FLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all clean distclean

all:
	$(LATEXMK) $(LATEXMK_FLAGS) $(TEX)

clean:
	$(LATEXMK) -c $(TEX)

distclean:
	$(LATEXMK) -C $(TEX)
