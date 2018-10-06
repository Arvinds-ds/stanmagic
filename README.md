# jupyterstan

`jupyterstan` is a package to help development of Stan models (using `pystan`)
in jupyter notebooks.

The package is heavily based on @Arvinds-ds
[stanmagic](https://github.com/Arvinds-ds/stanmagic) package, but provides an
interface that simply returns a `pystan.Model` object.

In addition, it bundles @Arvinds-ds `stan_code_helper` package to improve
syntax highlighting for stan cells.

## Installation

To install the library:

```
pip install git+https://github.com/janfreyberg/jupyterstan.git
```

To enable the syntax highlighting:

```
jupyter nbextension install --py stan_syntax --sys-prefix
jupyter nbextension enable stan_syntax --py --sys-prefix
```

## Usage

To define a stan model inside a jupyter notebook, start a cell with the `%%stan`
magic. You can also provide a variable name, which is the variable name that
the `pystan.Model` object will be assigned to. For example:

```
%%stan paris_female_births
data {
    int male;
    int female;
}

parameters {
    real<lower=0, upper=1> p;
}

model {
    female ~ binomial(male + female, p);
}

```

Then, to use your defined model:

```
fit = paris_female_births.sampling(
    data={'male': 251527, 'female': 241945},
    iter=1000,
    chains=4
)
```
