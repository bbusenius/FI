# FI

FI is a Python library of functions for the financial independence (FI, FIRE) community. Functions can be run as standalone utilities on the command line or used in Python code. The FI library powers the auto-generated site [FI Widgets](https://fi-widgets.com/) which is a GUI representation of the library. It also powers [FI API](https://github.com/bbusenius/FI-API) and is used in [MMM Savings Rate](https://github.com/bbusenius/MMM_Savings_Rate).

## Installation

This package is pip installable. To get the newest code use one of the commands below. FI requires python3. Use `pip` to install it if you're installing into a [Virtualenv](https://virtualenv.pypa.io/en/stable/) otherwise install with `pip3`. If you're a developer and you wish to contribute, see the installation instructions in the **Developers** section.

```
pip install git+https://github.com/bbusenius/FI.git#egg=FI
```

or

```
pip3 install -e git+https://github.com/bbusenius/FI.git#egg=FI
```
Pass the -e flag to retain the editable source.

## Using

The following functions are packaged in this library:

- **annual_cost**
- **average_daily_spend**
- **buy_a_day_of_freedom**
- **coast_fi**
- **cost_per_use**
- **days_covered_by_fi**
- **fi_age**
- **fi_number**
- **future_value**
- **get_percentage**
- **hours_of_life_energy**
- **percent_decrease**
- **percent_increase**
- **redeem_points**
- **redeem_chase_points**
- **rule_of_72**
- **savings_rate**
- **spending_from_savings**
- **take_home_pay**

All functions can be run from the command-line or used in Python directly.

[Full API](https://fi.readthedocs.io/en/latest/source/fi.html)

### Running from the command-line

List available functions:

```FI --help```

To see how to run a function from the command-line, just open a terminal and invoke the command with --help options, e.g.:

```coast_fi -h``` or ```coast_fi --help```

This will display instructions on how to run the command.

Running the `coast_fi` command might look something like this:

```
coast_fi 800000 .07 62 40
```

Other functions are run in a similar way. Use `-h` or `--help` to see all the options.

### Advanced use from the command-line

By using variables and backticks, commands can be combined to produce more robust output. The following example shows how to calculate savings rate from money saved rather than money spent.

```
THP="$(take_home_pay 5215.71 417.27 514.09)"
savings_rate "${THP}" `spending_from_savings "${THP}" 2600`
```

Another useful example might be to calculate CoastFI using your "retire today" number, a projected inflation rate and a future value calculation.

```
coast_fi `future_value 800000 .03 1 22` .07 62 40
```

## Developers

FI is written with type hints and relies on the built in typing module. This allows FI to be used more robustly in third party applications. Docstrings are considered forward facing since they are sometimes exposed to the public as on [FI Widgets](https://fi-widgets.com/). 

### Installation for developers

To install for development run the following command from the root of the cloned directory:
```
pip3 install -e .
```

### Run unit tests

```
python -m unittest tests.test_fi
```

### Documentation

Documentation is automatically generated from docstrings using [Sphinx](https://docs.readthedocs.io/en/latest/getting_started.html#write-your-docs).

```
cd docs/
sphinx-apidoc -o source/ ../fi
make html
```
