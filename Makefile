SOURCES_SUGAR = $(wildcard Sources/*.spy)
PRODUCT_PYTHON = $(SOURCES_SUGAR:%.spy=%.py)

all: $(PRODUCT_PYTHON)
	
%.py: %.spy
	sugar -clpy $< > $@

