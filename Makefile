show:
	uv run quarto preview --profile thesis
html:
	uv run quarto render --to html --profile thesis
pdf:
	uv run quarto render --to titlepage-pdf --profile thesis
	mv _book/Fast-analysis-of-long-gravitational-wave-signals.pdf Fast-analysis-of-long-gravitational-wave-signals.pdf
all:
	rm -rf thesis
	uv run quarto render --profile thesis
	mv _book thesis
	tar -cvf thesis.tar thesis/*
refresh:
	rm -rf thesis
	uv run quarto render --profile thesis --cache-refresh
	mv _book thesis
	tar -cvf thesis.tar thesis/*
