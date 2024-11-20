Thesis being written using quarto, documentation [here](https://quarto.org/docs/guide/).

To compile:
```bash
make preview
```

or `quarto preview --to pdf` to get pdf output. 

Known issues:

- even when activating the `link-citations: true` option in the 
    document yaml, the citations do not appear as links in the pdf output
    (but they do in the html output)