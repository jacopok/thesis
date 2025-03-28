Thesis being written using quarto, documentation [here](https://quarto.org/docs/guide/).


### Usage tricks

#### Figures

A figure can be made like:

```{python}
#| label: fig-my-figure
#| fig-cap: "Caption"

# Matplotlib calls
```

Code execution can be controlled with the [freeze](https://quarto.org/docs/projects/code-execution.html) argument.

Figures can be rendered optionally only when making html, see [here](https://quarto.org/docs/authoring/conditional.html#content-visible).

Examples with [figures on the side](https://quarto-dev.github.io/quarto-gallery/page-layout/tufte.html).

##### Figures side by side

See the example [here](https://quarto.org/docs/authoring/figures.html#block-layout). Arbitrary-width columns and divs.

#### References

See [here](https://quarto.org/docs/authoring/citations.html). 

- Section title: `## Title {#sec-title}`
- Equation: `{#eq-title}` _after_ the final `$$`

Example:

```
$$ 
e^{i \pi} + 1 = 0
$$ {#eq-euler-identity}
```

Reference as `@eq-title` or `[Equation @eq-title]`

#### Bibliography

Generally, `@citekey`, `[@citekey]`, `[@citekey, some page]`


#### Equations

To get aligned multiple lines, use the `aligned` environment instead of `align`.

All mathjax symbols: see [here](https://www.onemathematicalcat.org/MathJaxDocumentation/TeXSyntax.htm).

Using Unicode characters such as ☾ in equations works for HTML output, but they do not render correctly to LaTeX.

#### Callout blocks

Snippet:

```quarto
::: {#nte-title .callout-note collapse="true"}
##### Title

Text
:::
```

where `note` can be substituted by `warning`, `important`, `tip` or `caution`, see the [docs](https://quarto.org/docs/authoring/callouts.html).


### Known issues

- even when activating the `link-citations: true` option in the 
    document yaml, the citations do not appear as links in the pdf output
    (but they do in the html output)


### Useful refs

- [Tips and tricks](https://danielborek.me/2023/pdf-quarto-tips/)

### Making a single-file PDF

