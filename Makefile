SOURCES_SUGAR = $(wildcard src/*.spy)
PRODUCT_PYTHON = $(SOURCES_SUGAR:%.spy=%.py)

all: $(PRODUCT_PYTHON)
	chmod +x src/sugar2.py

native: src/sugar2.so

debug:
	gdb -ex r --args python src/sugar2.py pouet.sg

callgraph:
	pycallgraph graphviz --output-format=svg --output-file=tooltips.svg -- src/sugar2.py -cljs test-modules/tooltips.sjs

clean:
	rm $(PRODUCT_PYTHON)

%.so: %.pyx
	python setup.py build_ext --inplace

%.pyx: %.py
	cp $< $@

%.py: %.spy
	sugar -clpy $< > $@ 
	sed -i 1d $@

# EOF
