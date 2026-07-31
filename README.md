## My PhD thesis --- read it at [this link](https://jacopok.github.io/thesis/)!

--- 

This thesis is written using quarto, documentation [here](https://quarto.org/docs/guide/).

The dependencies are managed with `uv` ([installation](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)).
If `uv` is installed, the commands defined in the `Makefile` can be used:

- `make show` will render the HTML version of the thesis in a browser window, updated in real time as the underlying files change;
- `make html` will render the HTML version of the thesis as a static website;
- `make pdf` will render the PDF version of the thesis.
- `make showp` will render the revealjs version of the defense presentation.

### Usage tricks

#### Figures

A figure based on code can be made like:

```{python}
#| label: fig-my-figure
#| fig-cap: "Caption"

# Matplotlib calls
```

Code execution can be controlled with the [freeze](https://quarto.org/docs/projects/code-execution.html) argument.

Figures can be rendered optionally only when making html, see [here](https://quarto.org/docs/authoring/conditional.html#content-visible).

Examples with [figures on the side](https://quarto-dev.github.io/quarto-gallery/page-layout/tufte.html).

Alternatively, importing an existing figure can be simply achieved with the pandoc syntax:

```
![Caption](figure-filename.png){#fig-my-figure}
```

##### Figures side by side

See the example [here](https://quarto.org/docs/authoring/figures.html#block-layout). Arbitrary-width columns and divs.

##### 3D figures


```{python}
# Import dependencies
import plotly
import plotly.graph_objs as go

# Configure Plotly to be rendered inline in the notebook.
plotly.offline.init_notebook_mode()

# Configure the trace.
trace = go.Scatter3d(
    x=[1, 2, 3],  # <-- Put your data instead
    y=[4, 5, 6],  # <-- Put your data instead
    z=[7, 8, 9],  # <-- Put your data instead
    mode='markers',
    marker={
        'size': 10,
        'opacity': 0.8,
    }
)

# Configure the layout.
layout = go.Layout(
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
)

data = [trace]

plot_figure = go.Figure(data=data, layout=layout)

# Render the plot.
plotly.offline.iplot(plot_figure)
```

#### References

See [here](https://quarto.org/docs/authoring/citations.html). 
To vary the citation style see [here](https://quarto.org/docs/authoring/citations.html#sec-citations-style).

- Section title: `## Title {#sec-title}`
- Equation: `{#eq-title}` _after_ the final `$$`

Example:

```
$$ 
e^{i \pi} + 1 = 0
$$ {#eq-euler-identity}
```

Example with multiple lines. Do __not__ use the `align` environment!

```
$$ 
\begin{aligned}
e^{i \pi} + 1 &= 0 \\ 
e^{i \pi} &= -1
\end{aligned}
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

#### Title page

Info [here](https://nmfs-opensci.github.io/quarto_titlepages/).

#### Programmatic paragraphs and tables

See the [tables](https://quarto.org/docs/authoring/tables.html) documentation. 

Simple example:

```{python}
import astropy.units as u
from IPython.display import Markdown

x = 10 * u.m

Markdown(f'The value of $x$ is {x.to_string(precision=2, format="latex_inline")}')
```

### Known issues

- even when activating the `link-citations: true` option in the 
    document yaml, the citations do not appear as links in the pdf output
    (but they do in the html output)


### Useful refs

- [Tips and tricks](https://danielborek.me/2023/pdf-quarto-tips/)
- [Code execution and caching options](https://quarto.org/docs/projects/code-execution.html)
- [HTML customization](https://quarto.org/docs/output-formats/html-themes.html)

### Making a single-file PDF

`uv run quarto render path/to/file.qmd`

## Presentation tricks

## Revealjs tips and tricks

- press `g` to jump to a slide number
- press `o` to go into "overview mode"
- press `s` to get the speaker view
- navigate without pauses with `Alt+arrow`
- press `r` for scroll view
- `Ctrl+click` to zoom
- `c` to get the canvas:
    - `x` to cycle colors
    - `backspace` to erase the drawing