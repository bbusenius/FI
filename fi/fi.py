# Copyright (C) 2018 Brad Busenius
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. <https://opensource.org/licenses/MIT/>

from decimal import Decimal


def coast_fi(target_fi_num, eiar, retirement_age, current_age):
    """
    Calculate the amount of money your would need to "coast to FI" if
    your were to stop working but never touch your savings.

    Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e34uuxh/

    Args:
        target_fi_num: Target FI number, the amount you'll need
        invested in order to live off interest and dividends.

        eiar: Expected inflation adjusted return e.g. .07 (7%)

        retirement_age: The age you want to retire.

        current_age: Your current age.

    Returns:
        CoastFI number, Decimal
    """
    return Decimal(target_fi_num) / (Decimal(1) + Decimal(eiar)) ** (Decimal(retirement_age) - Decimal(current_age))


def future_value(present_value, annual_rate, periods_per_year, years):
    """
    Calculates the future value of money invested at an interest rate,
    x times per year, for a given number of years. Can also be used to
    calculate the future equivalent of money due to inflation.

    Args:
        present_value: int or float, the current quantity of money (principal).

        annual_rate: float 0 to 1 e.g., .5 = 50%, the interest rate paid out.

        periods_per_year: int, the number of times money is invested per year.
        years: int, the number of years invested.

    Returns:
        Decimal, the future value of the money invested with compound interest.
    """

    # The nominal interest rate per period (rate) is how much interest you earn
    # during a particular length of time, before accounting for compounding.
    # This is typically expressed as a percentage.
    rate_per_period = Decimal(annual_rate) / Decimal(periods_per_year)

    # How many periods in the future the calculation is for.
    periods = Decimal(periods_per_year) * Decimal(years)

    return Decimal(present_value) * (1 + rate_per_period) ** periods


def rule_of_72(interest_rate, accurate=False):
    """
    Calculate the time it will take for money to double
    based on a given interest rate: 

    Years to double = 72 / Interest Rate

    Args:
        interest_rate: integer or floating point number
        written with the decimal moved two places to the 
        left, e.g. 7 for 7%

        accurate: Boolean, when set to True the more accurate
        69.3 is used instead of 72.

    Returns:
        Years to double, float
    """
    if interest_rate == 0:
        return float('inf')

    if accurate:
        return 69.3 / interest_rate
    return 72. / interest_rate


def savings_rate(take_home_pay, spending):
    """
    Calculate your savings_rate based on take home pay and spending,
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        take_home_pay: float or int, monthly take-home pay

        spending: float or int, monthly spending

    Returns:
        your monthly savings rate expressed as a percentage.
    """

    try:
        return ((Decimal(take_home_pay) - Decimal(spending)) / (Decimal(take_home_pay))) * Decimal(100)
    except(ZeroDivisionError):
        return Decimal(0)


def spending_from_savings(take_home_pay, savings):
    """
    Calculate your spending based on your take home pay and how much
    you save. This is useful if you use what Paula Pant calls the anti-budget,
    instead of tracking your spending in detail. This number can be used as
    input for the savings_rate function.

    Args:
        take_home_pay: float or int, monthly take-home pay

        savings: the amount of money saved towards FI

    Returns:
        Decimal, the amount of money spent
    """
    return Decimal(take_home_pay) - Decimal(savings)


def take_home_pay(gross_pay, employer_match, taxes_and_fees):
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        gross_pay: float or int, gross monthly pay.

        employer_match: float or int, the 401(k) match from your employer.

        taxes_and_fees: list, taxes and fees that are deducted from your paycheck.

    Returns:
        Your monthly take-home pay.
    """
    taxes_and_fees = [Decimal(item) for item in taxes_and_fees]
    return (Decimal(gross_pay) + Decimal(employer_match)) - sum(taxes_and_fees)
