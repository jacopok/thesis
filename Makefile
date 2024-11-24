show:
	uv run quarto preview --profile thesis
html:
	uv run quarto render --to html --profile thesis
pdf:
	uv run quarto render --to pdf --profile thesis