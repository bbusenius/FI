# FI

FI calculations at your fingertips is a library of common functions used in financial independence (FI, FIRE) calculations. All functions can be used in a python application or run from the command-line. If you're a nerdy follower of people like [Mr. Money Mustache](http://www.mrmoneymustache.com/), [ChooseFI](https://www.choosefi.com/), [Paula Pant](https://affordanything.com/a), [GoCurryCracker](https://www.gocurrycracker.com/), [Mad FIentist](https://www.madfientist.com/) and other life-optimizers, this library might be something you'd like.

## Installation

This package is pip installable. To get the newest code use one of the following commands. Both should work depending on what kind of an environment you're using. This project requires python3. Use `pip` to install if you're installing into a [Virtualenv](https://virtualenv.pypa.io/en/stable/) otherwise install with `pip3`. If you're a developer and you wish to contribute, see the installation instructions in the **Developers** section.

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
- **future_value**
- **percent_decrease**
- **percent_increase**
- **redeem_points**
- **redeem_chase_points**
- **rule_of_72**
- **savings_rate**
- **spending_from_savings**
- **take_home_pay**

All functions can be used in a python application or run from the command-line.

[Full API](https://fi.readthedocs.io/en/latest/source/fi.html)

### Running from the command-line

To see how to run a function from the command-line, just open a terminal and invoke the command with --help options, e.g.:

```coast_fi -h``` or ```coast_fi --help```

This will display the necessary information to run the command.

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

### Installation for developers

To install for development run:
```
sudo python3 setup.py develop
```
You will need to re-run this command every time you make changes before you can preview them. If you're testing in a python shell, you'll need to exit and reopen the shell.

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
