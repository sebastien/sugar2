# -----------------------------------------------------------------------------
#
# Sugar Makefile
# ==============
#
# Updated: 2016-11-01
# Author:  FFunction <ffctn.com>
#
# -----------------------------------------------------------------------------

PROJECT          ?=sugar2
SOURCES_PATH     ?=src
BUILD_PATH       ?=.build
DIST_PATH        ?=dist

# === SOURCES =================================================================

SOURCES_SUGAR_PY =$(shell find $(SOURCES_PATH)/spy -name "*.spy")
SOURCES_MD       =$(wildcard *.md)
SOURCES_MODULES  =$(filter-out $(SOURCES_PATH)/spy/,$(shell find $(SOURCES_PATH)/spy/ -type "d")) 
SOURCES_ALL      =$(SOURCES_SUGAR)

# === BUILD ===================================================================

BUILD_ALL       =$(SOURCES_SUGAR:$(SOURCES_PATH)/%.spy=$(BUILD_PATH)/%.py) $(SOURCES_MODULES:$(SOURCES_PATH)/%=$(BUILD_PATH)/%/__init__.py)

# === PRODUCT =================================================================

PRODUCT_PY      =$(SOURCES_SUGAR_PY:$(SOURCES_PATH/spy/%.spy=$(SOURCES)/py/%.py)\
                 $(SOURCES_MODULES:$(SOURCES_PATH)/spy/%=$(SOURCES_PATH)/py/%/__init__.py)
PRODUCT_HTML    =$(SOURCES_MD:%.md=%.html)
PRODUCT         =$(PRODUCT_PY)

# === TOOLS ===================================================================

SUGAR           =sugar
PYTHON          =PYTHONPATH=$(SOURCES)/py:$(PYTHONPATH) && python3.5
PANDOC          =pandoc

# === HELPERS =================================================================

YELLOW           =`tput setaf 11`
GREEN            =`tput setaf 10`
CYAN             =`tput setaf 14`
RED              =`tput setaf 1`
GRAY             =`tput setaf 7`
RESET            =`tput sgr0`

TIMESTAMP       :=$(shell date +'%F')
BUILD_ID        :=$(shell git rev-parse --verify HEAD)
MAKEFILE_PATH   := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR    := $(notdir $(patsubst %/,%,$(dir $(MAKEFILE_PATH))))


# From: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL   := all
.PHONY          : all

# -----------------------------------------------------------------------------
#
# RULES
#
# -----------------------------------------------------------------------------


all: $(PRODUCT) ## Builds all the project assets

help: ## Displays a description of the different Makefile rules
	@echo "$(CYAN)★★★ $(PROJECT) Makefile ★★★$(RESET)"
	@grep -E -o '((\w|-)+):[^#]+(##.*)$$'  $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":|##"}; {printf "make \033[01;32m%-15s\033[0m🕮 %s\n", $$1, $$3}'

clean: ## Cleans the build files
	@echo "$(RED)♻  clean: Cleaning $(words $(PRODUCT)) files $(RESET)"
	@test -e $(BUILD_PATH) && rm -r $(BUILD_PATH) ; true

# -----------------------------------------------------------------------------
#
# BUILDING
#
# -----------------------------------------------------------------------------

$(SOURCES_PATH)/py/%.py: $(SOURCES_PATH)/%.spy
	@echo "$(GREEN)📝  $@ [PY]$(RESET)"
	@mkdir -p `dirname $@`
	@$(SUGAR) -clpy $< > $@
	@cp --attributes-only --preserve=mode $< $@

$(SOURCES_PATH)/py/%/__init__.py: $(SOURCES_PATH)/spy/%
	@echo "$(GREEN)📝  $@ [PY]$(RESET)"
	@mkdir -p `dirname $@`
	@touch $@

%.html: %.md
	@echo "$(GREEN)📝  $@ [PANDOC]$(RESET)"
	@mkdir -p `dirname $@`
	@$(PANDOC) $< -thtml -s -c "https://cdn.rawgit.com/sindresorhus/github-markdown-css/gh-pages/github-markdown.css"  | sed 's|<body>|<body><div class=markdown-body style="padding:4em;max-width:55em;">|g' > $@

# -----------------------------------------------------------------------------
#
# HELPERS
#
# -----------------------------------------------------------------------------

print-%:
	@echo $*=
	@echo $($*) | xargs -n1 echo | sort -dr

# EOF
