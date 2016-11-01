# -----------------------------------------------------------------------------
#
# Sugar Makefile
# ==============
#
# Updated: 2016-11-01
# Author:  FFunction <ffctn.com>
#
# -----------------------------------------------------------------------------

PROJECT        ?= sugar2
SOURCES_PATH   ?= src
BUILD_PATH     ?= build
DIST_PATH      ?= dist

SOURCES_SUGAR   = $(shell find $(SOURCES_PATH)/ -name "*.spy")
SOURCES_MODULES = $(filter-out $(SOURCES_PATH)/,$(shell find $(SOURCES_PATH)/ -type "d")) 

BUILD_FILES      = $(SOURCES_SUGAR:$(SOURCES_PATH)/%.spy=$(BUILD_PATH)/%.py) $(SOURCES_MODULES:$(SOURCES_PATH)/%=$(BUILD_PATH)/%/__init__.py)

PRODUCT          = $(BUILD_FILES)

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

$(BUILD_PATH)/%.py: $(SOURCES_PATH)/%.spy
	@echo "$(GREEN)📝  $@ [PY]$(RESET)"
	@mkdir -p `dirname $@`
	@sugar -clpy $< > $@
	@cp --attributes-only --preserve=mode $< $@

$(BUILD_PATH)/%/__init__.py: $(SOURCES_PATH)/%
	@echo "$(GREEN)📝  $@ [PY]$(RESET)"
	@mkdir -p `dirname $@`
	@touch $@

# -----------------------------------------------------------------------------
#
# HELPERS
#
# -----------------------------------------------------------------------------

print-%:
	@echo $*=
	@echo $($*) | xargs -n1 echo | sort -dr

# EOF
