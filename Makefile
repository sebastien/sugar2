SOURCES_SUGAR = $(wildcard Sources/*.spy)
PRODUCT_PYTHON = $(SOURCES_SUGAR:%.spy=%.py) #Sources/sugar2.so

all: $(PRODUCT_PYTHON)
	chmod +x Sources/sugar2.py
	
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
