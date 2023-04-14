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

import warnings
from decimal import ROUND_HALF_UP, Decimal
from math import nan
from typing import List

import numpy
import numpy_financial as npf

CENTS = Decimal('0.01')


def annual_cost(cost: float, used_price: float, years_in_service: float) -> Decimal:
    """
    Calculate the depreciation schedule of things bought.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW

    Args:
        cost: original amount paid for the object
        used_price: amount you can sell it for
        years_in_service : number of years you've used it

    Returns:
        The amount something has costed per year
    """
    return (Decimal(cost) - Decimal(used_price)) / Decimal(years_in_service)


def average_daily_spend(money_spent: float, num_days: int) -> float:
    """
    Calculate the average amount of money spent per day over
    a given number of days.

    Args:
        money_spent: the amount of money
        spent.
        num_days: the number of days during which the
        spending occurred.

    Returns:
        The amount of money spent per day.
    """
    return money_spent / num_days


def buy_a_day_of_freedom(annual_spend: float, swr: float = 0.04) -> Decimal:
    """
    Calculate how much it costs to buy a day of freedom based
    on your annual spend and your safe withdrawl rate. Every time
    you save this amount of money, you've covered 1 more day. Once
    you have 365 days, you are financially independent. Credit:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire
    _discussion_july_08_2019/etfdwg1/

    Args:
        annual_spend: the amount of money you plan to spend in retirement.
        swr: your planned safe withdrawl rate. Defaults to 0.04 (4%).

    Returns:
        The amount of money that buys you 1 day of freedom when saved.
    """
    return Decimal(average_daily_spend(annual_spend, 365) / swr).quantize(
        CENTS, ROUND_HALF_UP
    )


def coast_fi(
    target_fi_num: float, eiar: float, retirement_age: float, current_age: float
) -> Decimal:
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
        CoastFI number
    """
    return Decimal(target_fi_num) / (Decimal(1) + Decimal(eiar)) ** (
        Decimal(retirement_age) - Decimal(current_age)
    )


def cost_per_use(your_cost: float, used_price: float, times_used: float) -> Decimal:
    """
    Calculate how much something has costed while considering
    how many times it has been used. Wrapper function for
    annual_cost.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW

    Args:
        your_cost: amount paid
        used_price: amount you can sell it for
        times_used: number of times you've used it

    Returns:
        The amount something has costed per use
    """
    return annual_cost(your_cost, used_price, times_used)


def days_covered_by_fi(annual_spend: float, stash: float, wr: float = 0.04) -> float:
    """
    Calculate the number of days per year covered by your savings.
    This is a way of seeing where you are on your FI journey. For
    example, 182.5 days would put you at 50% FI. 365 days would put
    you at 100% FI or full financial independence. Inspired by:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire
    _discussion_july_08_2019/etfdwg1/

    Args:
        annual_spend: the amount of money you plan to spend in retirement.
        stash: the amount of money you've saved.
        wr: your planned safe withdrawl rate. Defaults to 0.04 (4%).

    Returns:
        The number of days covered by your stash. This is how
        many days you have already paid for with your savings and
        the amount of time you could theoretically take off every
        year if you wanted to.
    """
    return (stash * wr) / average_daily_spend(annual_spend, 365)


def fi_age(eiar: float, asa: float, stash: float, fi_num: float, ca: int) -> int:
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
        return int(npf.nper(eiar, asa, stash, fi_num) + ca)


def fi_number(planned_yearly_expenses: float, withdrawal_rate: float) -> Decimal:
    """
    Calculate your FI number based on your planned yearly expenses and
    withdrawal rate.

    Args:
        planned_yearly_expenses: the amount of money you think you will
        spend in retirement on an annual basis.
        withdrawal_rate: the rate you expect to withdral money annually
        e.g. 4 (for 4%, based on the Trinity Study).

    Returns:
        FI number.
    """
    return (Decimal(planned_yearly_expenses) * Decimal(100.0)) / Decimal(
        withdrawal_rate
    )


def future_value(
    present_value: float, annual_rate: float, periods_per_year: int, years: int
) -> Decimal:
    """
    Calculates the future value of money invested at an interest rate,
    x times per year, for a given number of years. Can also be used to
    calculate the future equivalent of money due to inflation.

    Args:
        present_value: the current quantity of money (principal).
        annual_rate: number 0 to 1 e.g., .5 = 50%, the interest rate paid out.
        periods_per_year: the number of times money is invested per year.
        years: the number of years invested.

    Returns:
        The future value of the money invested with compound interest.
    """

    # The nominal interest rate per period (rate) is how much interest you earn
    # during a particular length of time, before accounting for compounding.
    # This is typically expressed as a percentage.
    rate_per_period = Decimal(annual_rate) / Decimal(periods_per_year)

    # How many periods in the future the calculation is for.
    periods = Decimal(periods_per_year) * Decimal(years)

    return Decimal(present_value) * (1 + rate_per_period) ** periods


def get_percentage(a: float, b: float, i: bool = False, r: bool = False) -> float:
    """
    Finds the percentage of one number over another.

    Args:
        a: The number that is a percent, int or float.
        b: The base number that a is a percent of, int or float.
        i: Boolean, True if the user wants the result returned as a whole
        number. Assumes False.
        r: Boolean, True if the user wants the result rounded. Rounds to the
        second decimal point on floating point numbers. Assumes False.

    Returns:
        The argument a as a percentage of b. Throws a warning if integer is set to True
        and round is set to False.
    """
    # Round to the second decimal
    if i is False and r is True:
        percentage = round(100.0 * (float(a) / b), 2)

    # Round to the nearest whole number
    elif (i is True and r is True) or (i is True and r is False):
        percentage = int(round(100 * (float(a) / b)))

        # A rounded number and an integer were requested
        if r is False:
            warnings.warn(
                "If integer is set to True and Round is set to False, you will still get a rounded number if you pass floating point numbers as arguments."
            )

    # A precise unrounded decimal
    else:
        percentage = 100.0 * (float(a) / b)

    return percentage


def percent_decrease(original_value: float, final_value: float) -> float:
    """
    Calculate the percentage of loss from one number to another.

    Args:
        original_value: int or float, the starting number.
        final_value: int or float, the final number after all losses.

    Returns:
        The decrease from one number to another expressed as a percentage.
    """
    try:
        return abs(float(((original_value - final_value) / original_value)) * 100)
    except (ZeroDivisionError):
        return nan


def percent_increase(original_value: float, final_value: float) -> float:
    """
    Calculate the percentage of growth from one number to another.

    Args:
        original_value: int or float, the starting number.
        final_value: int or float, the final number after all gains.

    Returns:
        The increase from one number to another expressed as a percentage.
    """
    try:
        return float(((final_value - original_value) / abs(original_value)) * 100)
    except (ZeroDivisionError):
        return nan


def redeem_points(points: int, rate: float = 0.01) -> Decimal:
    """
    Calculates the value of travel rewards points based on a conversion
    rate. The default rate is 0.01 which is the cash value of awards
    points for most cards.

    Args:
        points: the number of awards points to be redeemed.
        rate: defaults to 0.01 which is the exchange rate for most points
        to cash (1 cent per point).

    Returns:
        Dollar amount the points are worth.
    """
    return Decimal(points * rate).quantize(CENTS, ROUND_HALF_UP)


def redeem_chase_points(points: int) -> dict:
    """
    Calculates the value of Chase Ultimate Rewards points for different
    exchange scenarios. Based on the ChooseFI Sweet Redemption article:
    https://www.choosefi.com/travel-rewards-part-3-sweet-redemption/

    Args:
        points: number of Ultimate Rewards points being redeemed.

    Returns:
        A dictionary containing common Chase Ultimate Rewards redemption scenarios
        where cv = cash value, spp = sapphire preferred portal, srp = sapphire
        reserved portal and tpe = target partner exchange (the guideline for
        direct transfer of pints to Chase Ultimate Reward partners such as
        United Airlines). tpp is the aspirational goal for an exchange with
        a partner, not a guarantee.
    """
    return {
        'cv': redeem_points(points),
        'spp': redeem_points(points, 0.0125),
        'srp': redeem_points(points, 0.015),
        'tpe': redeem_points(points, 0.02),
    }


def rule_of_72(interest_rate: float, accurate: bool = False) -> float:
    """
    Calculate the time it will take for money to double based on a given
    interest rate:

    Years to double = 72 / Interest Rate

    Args:
        interest_rate: float written with the decimal moved two
        places to the left, e.g. 7 for 7%
        accurate: Boolean, when set to True the more accurate
        69.3 is used instead of 72.

    Returns:
        The number of years it will take for money to double based
        on an interest rate.
    """
    if interest_rate == 0:
        return float('inf')

    if accurate:
        return 69.3 / interest_rate
    return 72.0 / interest_rate


def savings_rate(take_home_pay: float, spending: float) -> Decimal:
    """
    Calculate your savings_rate based on take home pay and spending,
    using the formula laid out by Mr. Money Mustache:
    http: // www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        take_home_pay: monthly take-home pay
        spending: monthly spending

    Returns:
        your monthly savings rate expressed as a percentage.
    """

    try:
        return (
            (Decimal(take_home_pay) - Decimal(spending)) / (Decimal(take_home_pay))
        ) * Decimal(100)
    except (ZeroDivisionError):
        return Decimal(0)


def spending_from_savings(take_home_pay: float, savings: float) -> Decimal:
    """
    Calculate your spending based on your take home pay and how much
    you save. This is useful if you use what Paula Pant calls the anti-budget,
    instead of tracking your spending in detail. This number can be used as
    input for the savings_rate function.

    Args:
        take_home_pay: monthly take-home pay
        savings: amount of money saved towards FI

    Returns:
        The amount of money spent
    """
    return Decimal(take_home_pay) - Decimal(savings)


def take_home_pay(
    gross_pay: float, employer_match: float, taxes_and_fees: List[float]
) -> Decimal:
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http: // www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        gross_pay: gross monthly pay.
        employer_match: the 401(k) match from your employer.
        taxes_and_fees: taxes and fees deducted from your paycheck.

    Returns:
        Your monthly take-home pay.
    """
    taxes_and_fees = [Decimal(item) for item in taxes_and_fees]
    return (Decimal(gross_pay) + Decimal(employer_match)) - sum(taxes_and_fees)
