# =========================================================
# Makefile for Running NatureCode Detection on Transcripts
# =========================================================
# Purpose:
# This Makefile automates running the detect_naturecodes.py script
# on all transcript text files in the `transcripts` folder.
# For each transcript, it generates a separate output log file
# in the `keywordsOutput` folder containing matched NatureCodes.
#
# Usage:
# 1. Run `make`        -> Processes all transcripts and outputs logs.
# 2. Run `make clean`  -> Removes all generated output logs.
#
# Notes:
# - The detect_naturecodes.py script must be in the same folder
#   as this Makefile (backend/).
# - Input transcripts should be .txt files in the `transcripts/` folder.
# - Output logs are written to `keywordsOutput/` folder.
# - Each output file is named <transcript_name>_naturecodes.txt
# =========================================================


# Folder paths
TRANSCRIPTS_DIR = transcripts
OUTPUT_DIR = keywordsOutput

# All transcript files
TRANSCRIPTS = $(wildcard $(TRANSCRIPTS_DIR)/*.txt)
OUTPUTS = $(patsubst $(TRANSCRIPTS_DIR)/%.txt,$(OUTPUT_DIR)/%_naturecodes.txt,$(TRANSCRIPTS))

# Default target: run detection on all transcripts
all: $(OUTPUTS)
	@echo "✅ All transcripts processed."

# Rule for each transcript
$(OUTPUT_DIR)/%_naturecodes.txt: $(TRANSCRIPTS_DIR)/%.txt | $(OUTPUT_DIR)
	@echo "Processing $< ..."
	@python3 detect_naturecode.py $< --output $(OUTPUT_DIR)

# Ensure output folder exists
$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

# Clean only contents, keep folder
clean:
	@test -d $(OUTPUT_DIR) || exit 0
	@echo "Cleaning output folder contents..."
	@rm -rf $(OUTPUT_DIR)/*
	@echo "Output folder cleaned (folder preserved)"

# Phony targets
.PHONY: all clean
