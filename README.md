Thesis being written using quarto, documentation [here](https://quarto.org/docs/guide/).


### Usage tricks

A figure can be made like:

```{python}
#| label: fig-my-figure
#| fig-cap: "Caption"

# Matplotlib calls
```

Execution can be controlled with the [freeze](https://quarto.org/docs/projects/code-execution.html) argument.

### Known issues

- even when activating the `link-citations: true` option in the 
    document yaml, the citations do not appear as links in the pdf output
    (but they do in the html output)
