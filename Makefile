SOURCES_SUGAR = $(wildcard Sources/*.spy)
PRODUCT_PYTHON = $(SOURCES_SUGAR:%.spy=%.py)

all: $(PRODUCT_PYTHON)
	chmod +x Sources/sugar2.py
	
%.py: %.spy
	sugar -clpy $< > $@
	sed -i 1d $@


