# Sugar test makefile (02-Oct-2007)
TEST_DIR=tests
SOURCE_SG:=
SOURCE_SG=$(filter-out bug-%,$(filter-out todo-%,$(wildcard *.sg)))
PRODUCT_JS=$(SOURCE_SG:%.sg=$(TEST_DIR)/js/%.js)
PRODUCT_PY=$(SOURCE_SG:%.sg=$(TEST_DIR)/py/%.py)
SUGAR=sugar2

.PHONY: all clean

all: $(PRODUCT_JS) $(PRODUCT_AS) $(PRODUCT_PY) $(PRODUCT_PNUTS)

clean:
	rm -rf $(TEST_DIR)

$(TEST_DIR)/js/%.js: %.sg $(TEST_DIR)/js
	$(SUGAR) -cljavascript $< > $@

$(TEST_DIR)/py/%.py: %.sg $(TEST_DIR)/py
	$(SUGAR) -clpython $< > $@

$(TEST_DIR)/js:
	mkdir -p $@

$(TEST_DIR)/py:
	mkdir -p $@

# EOF
