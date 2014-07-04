SOURCES_SUGAR = $(wildcard Sources/*.spy)
PRODUCT_PYTHON = $(SOURCES_SUGAR:%.spy=%.py)

all: $(PRODUCT_PYTHON)
	chmod +x Sources/sugar2.py

native: Sources/sugar2.so
	
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
