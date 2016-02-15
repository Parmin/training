BUILD = build
SOURCE = src
EXTENSION = rst

MAKEFLAGS += -j

SOURCE_FILES := $(wildcard $(SOURCE)/*.$(EXTENSION))
PDF_OUTPUT_FILES = $(subst $(EXTENSION),pdf,$(subst $(SOURCE),$(BUILD),$(SOURCE_FILES)))
HTML_OUTPUT_FILES = $(subst $(EXTENSION),html,$(subst $(SOURCE),$(BUILD),$(SOURCE_FILES)))

OUTPUT_FILES = $(HTML_OUTPUT_FILES) $(PDF_OUTPUT_FILES)

HTMLCMD = rst2html.py --exit-status=2
LATEXCMD = rst2latex.py --exit-status=2 --latex-preamble="\usepackage{fullpage} \usepackage{parskip} \usepackage{fancyhdr} \usepackage{graphicx} \pagestyle{fancy} \renewcommand{\headrulewidth}{0pt} \renewcommand{\footrulewidth}{0pt} \PassOptionsToPackage{hyphens}{url}" --documentoptions=letter --documentclass=article
PDFCMD = pdflatex --interaction batchmode --output-directory $(BUILD)/

.PHONY: all clean cleanup builds setup
.DEFAULT_GOAL := help
.SECONDARY:

help:
	@echo "PDF, LaTeX and rST generator generator."
	@echo "Targets:"
	@echo ""
	@echo "	    setup - builds targets for all files in source directory or directories."
	@echo "		    (see bin/builder.py)"
	@echo ""
	@echo "	    all	  - build HTML and PDF files from sources in the '$(SOURCE)' directory with"
	@echo "		    the '.$(EXTENSION)' extension."
	@echo "	    html  - build only HTML test files from sources in the '$(SOURCE)' directory with"
	@echo "		    the '.$(EXTENSION)' extension."
	@echo "	    pdf	  - build only PDF files from sources in the '$(SOURCE)' directory with"
	@echo "		    the '.$(EXTENSION)' extension."
	@echo ""
	@echo "	    (other) - use 'make [filename-without-extension]' to rebuild only this file,"
	@echo "		      after running 'make setup'"

setup:$(BUILD)/makefile.generated 
$(BUILD)/makefile.generated:bin/builder.py $(BUILD) $(SOURCE_FILES) 
	@./$<
	@echo [builder]: \(re\)generated \"makefile.generated\"

-include $(BUILD)/makefile.generated

all:$(OUTPUT_FILES)
all-html:$(BUILD) $(HTML_OUTPUT_FILES)
all-pdf:$(BUILD) $(PDF_OUTPUT_FILES)

html:all-html
pdf:all-pdf

$(BUILD):
	@mkdir -p $@
	@echo [setup]: '$@' directory created.
$(BUILD)/%.tex:$(SOURCE0)/%.$(EXTENSION)
	@$(LATEXCMD) $< >$@
	@echo [rst2latex]: converted $<
$(BUILD)/%.html:$(SOURCE0)/%.$(EXTENSION)
	@$(HTMLCMD) $< >$@
	@echo [rst2html]: converted $<

$(BUILD)/%.tex:$(SOURCE1)/%.$(EXTENSION)
	@$(LATEXCMD) $< >$@
	@echo [rst2latex]: converted $<
$(BUILD)/%.html:$(SOURCE1)/%.$(EXTENSION)
	@$(HTMLCMD) $< >$@
	@echo [rst2html]: converted $<

$(BUILD)/%.tex:$(SOURCE2)/%.$(EXTENSION)
	@$(LATEXCMD) $< >$@
	@echo [rst2latex]: converted $<
$(BUILD)/%.html:$(SOURCE2)/%.$(EXTENSION)
	@$(HTMLCMD) $< >$@
	@echo [rst2html]: converted $<

$(BUILD)/%.pdf:$(BUILD)/%.tex
	@$(PDFCMD) '$<' >|$@.log
	@echo [pdflatex]: \(1/3\) built '$@'
	@$(PDFCMD) '$<' >>$@.log
	@echo [pdflatex]: \(2/3\) built '$@'
	@$(PDFCMD) '$<' >>$@.log
	@echo [pdflatex]: \(3/3\) built '$@'

cleanup:
	rm -f $(BUILD)/*.aux
	rm -f $(BUILD)/*.log
	rm -f $(BUILD)/*.out
	rm -f $(BUILD)/*.toc
	rm -f $(BUILD)/*.tex

clean:
	rm -rf $(BUILD)/
	rm -f makefile.generated
