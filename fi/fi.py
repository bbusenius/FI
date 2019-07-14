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

from decimal import ROUND_HALF_UP, Decimal

import numpy

CENTS = Decimal('0.01')


def annual_cost(your_cost, used_price, years_in_service):
    """
    Calculate the depreciation schedule of things bought.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW

    Args:
        your_cost: int or float, amount paid

        used_price: int or float, amount you can sell it for

        years_in_service : int or float, number of years you've used it

    Returns:
        The amount something has costed per year, Decimal
    """
    return (Decimal(your_cost) - Decimal(used_price)) / Decimal(years_in_service)


def average_daily_spend(money_spent, num_days):
    """
    Calculate the average amount of money spent per day over
    a given number of days.

    Args:
        money_spent: float or Decimal, the amount of money
        spent.

        num_days: int, the number of days during which the
        spending occurred.

    Returns:
        Decimal, the amount of money spent per day.
    """
    return Decimal(money_spent / num_days).quantize(CENTS, ROUND_HALF_UP)


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
    return Decimal(target_fi_num) / (Decimal(1) + Decimal(eiar)) ** (
        Decimal(retirement_age) - Decimal(current_age)
    )


def cost_per_use(your_cost, used_price, times_used):
    """
    Calculate how much something has costed while considering
    how many times it has been used. Wrapper function for
    annual_cost.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW

    Args:
        your_cost: int or float, amount paid

        used_price: int or float, amount you can sell it for

        times_used : int or float, number of times you've used it

    Returns:
        The amount something has costed per use, Decimal
    """
    return annual_cost(your_cost, used_price, times_used)


def fi_age(eiar, asa, stash, fi_num, ca):
    """
    Calculate the age at which you will reach FIRE.

    Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e36titl/

    Args:
        eiar: Expected inflation adjusted return e.g. .07 (7%)

        asa: annual savings amount, the amount of money you will
        save towards FI each year.

        stash: invested assests, the amount of money you have
        currently saved and invested for FI.

        fi_num: the number you need to reach FI.

        ca: your current age.

    Returns:
        FI age, int, the future age when you will FIRE.
    """
    fi_num = fi_num * -1
    with numpy.errstate(divide='ignore'):
        return int(numpy.nper(eiar, asa, stash, fi_num) + ca)


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


def redeem_points(points, rate=0.01):
    """
    Calculates the value of travel rewards points based on a conversion
    rate. The default rate is 0.01 which is the cash value of awards
    points for most cards.

    Args:
        points: int, the number of awards points to be redeemed.

        rate: float, defaults to 0.01 which is the exchange rate
        for most points to cash (1 cent per point).

    Returns:
        Decimal, dollar amount the points are worth.
    """
    return Decimal(points * rate).quantize(CENTS, ROUND_HALF_UP)


def redeem_chase_points(points):
    """
    Calculates the value of Chase Ultimate Rewards points for different
    exchange scenarios. Based on the ChooseFI Sweet Redemption article:
    https://www.choosefi.com/travel-rewards-part-3-sweet-redemption/

    Args:
        points: int, number of Ultimate Rewards points being redeemed.

    Returns:
        dict containing common Chase Ultimate Rewards redemption scenarios
        where cv = cash value, spp = sapphire preferred portal, srp = sapphire
        reserved portal and tpe = target partner exchange (the guideline for
        direct transfer of pints to Chase Ultimate Reward partners such as
        United Airlines). tpp is the aspirational goal for an exchange with
        a partner, not a guarantee.
    """
    return {
        'cv': redeem_points(points),
        'spp': redeem_points(points, .0125),
        'srp': redeem_points(points, .015),
        'tpe': redeem_points(points, .02),
    }


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
    http: // www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        take_home_pay: float or int, monthly take-home pay

        spending: float or int, monthly spending

    Returns:
        your monthly savings rate expressed as a percentage.
    """

    try:
        return (
            (Decimal(take_home_pay) - Decimal(spending)) / (Decimal(take_home_pay))
        ) * Decimal(100)
    except (ZeroDivisionError):
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
    http: // www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        gross_pay: float or int, gross monthly pay.

        employer_match: float or int, the 401(k) match from your employer.

        taxes_and_fees: list, taxes and fees that are deducted from your paycheck.

    Returns:
        Your monthly take-home pay.
    """
    taxes_and_fees = [Decimal(item) for item in taxes_and_fees]
    return (Decimal(gross_pay) + Decimal(employer_match)) - sum(taxes_and_fees)
