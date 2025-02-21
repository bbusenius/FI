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

import os
import warnings
from decimal import ROUND_HALF_UP, Decimal
from math import nan
from typing import List, Literal, NewType, TypeVar, Union

import numpy
import numpy_financial as npf
import pandas as pd

Money = NewType('Money', Decimal)
Percent = NewType('Percent', Decimal)
MeasureOfTime = Literal['hours', 'days', 'months', 'years']
Time = TypeVar('Time', bound=Decimal)
Hours = NewType('Hours', Time)
Days = NewType('Days', Time)
Months = NewType('Months', Time)
Years = NewType('Years', Time)
TimeUnit = Union[Hours, Days, Months, Years]
CENTS = Decimal('0.01')


def annual_cost(cost: float, used_price: float, years_in_service: float) -> Money:
    """Calculate the depreciation schedule of things.
    Credit: Early Retirement Extreme by Jacob Lund Fisker
    https://a.co/4vgBczW

    Args:
        cost: original amount you paid.
        used_price: amount you can sell it for.
        years_in_service: number of years you've used it.

    Returns:
        Cost per year.
    """
    return Money(Decimal(cost) - Decimal(used_price)) / Decimal(years_in_service)


def average_daily_spend(money_spent: float, num_days: int) -> Money:
    """Calculate the average amount of money spent per day over a given
    number of days.

    Args:
        money_spent: the amount of money spent.
        num_days: the number of days during which the spending occurred.

    Returns:
        The amount of money spent per day.
    """
    return Money(money_spent / num_days)


def buy_a_day_of_freedom(
    annual_spend: float, safe_withdrawal_rate: float = 4.0
) -> Money:
    """Calculate how much it costs to buy a day of freedom based on your
    annual spending habits and your safe withdrawl rate. Every time
    you save this amount of money, you've covered 1 more day. Once
    you have 365 days, you are financially independent. Credit:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire_discussion_july_08_2019/etfdwg1/

    Args:
        annual_spend: the amount of money you plan to spend in retirement.
        safe_withdrawal_rate: your planned safe withdrawl rate expressed
        as a whole percentage. Defaults to 4 for 4%.

    Returns:
        The amount of money it costs to buy 1 day of freedom assuming the
        money is saved and invested.
    """
    return Money(
        Decimal(
            average_daily_spend(annual_spend, 365) / (safe_withdrawal_rate / 100.00)
        )
    )


def coast_fi(
    target_fi_num: float, eiar: float, retirement_age: float, current_age: float
) -> Money:
    """Calculate the amount of money you would need to "coast to FI" if you
    were to stop working but never touch your savings. Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/what_is_this_coast_number_people_are_talking_about/e34uuxh/

    Args:
        target_fi_num: target FI number, the amount you'll need to invest
        in order to live off interest and dividends.
        eiar: expected inflation adjusted return expressed as a whole
        percentage, e.g. 7 for 7%.
        retirement_age: the age you want to retire.
        current_age: your current age.

    Returns:
        CoastFI number
    """
    return Money(
        Decimal(target_fi_num)
        / (Decimal(1) + (Decimal(eiar) / 100))
        ** (Decimal(retirement_age) - Decimal(current_age))
    )


def cost_of_costs(
    money_invested: float,
    interest_rate: float,
    investment_costs: float,
    time_period: float,
) -> Money:
    """Calculate the "tyranny of compounding costs" as laid out by Jack Bogle
    on pages 47-49 of "The Little Book of Common Sense Investing". This is how
    much your investing expenses cost you over time. According to Jack Bogle
    there are three primary sources of costs: 1. The fund's expense ratio, 2.
    The sales charge paid on each purchase of shares (loads), and 3. The cost
    of the purchase and sale of securities within a fund (turnover costs).
    https://a.co/d/7mVz5Ud

    Args:
        money_invested: principal, dollar amount.
        interest_rate: expected annual return expressed as a whole percentage.
        investment_costs: annual investment costs expressed as a whole
        percentage. This could simply be a fund's expense ratio, however, more
        accurate input might include turnover costs, loads, and any other fees.
        time_period: investing time horizon, how long the investment will be
        held, should be a number of years.

    Returns:
        Dollar amount, how much your investment expenses costed (or will cost)
        you over the lifetime of an investment, the "tyranny of compounding
        costs".
    """
    real_rate = interest_rate - investment_costs
    gross = future_value(money_invested, interest_rate, 1, time_period)
    net = future_value(money_invested, real_rate, 1, time_period)
    return Money(gross - net)


def cost_per_use(your_cost: float, used_price: float, times_used: float) -> Money:
    """Calculate how much something costed per use. Credit: Early Retirement
    Extreme by Jacob Lund Fisker https://a.co/4vgBczW

    Args:
        your_cost: amount paid.
        used_price: amount you can sell it for.
        times_used: number of times you've used it.

    Returns:
        The amount something has costed per use.
    """
    return annual_cost(your_cost, used_price, times_used)


def days_covered_by_fi(
    annual_spend: float, stash: float, withdrawal_rate: float = 4
) -> float:
    """Calculate the number of days per year that are currently covered by
    your savings. This is a way of seeing where you are on your FI journey.
    For example, 182.5 days would put you at 50% FI. 365 days would put
    you at 100% FI or full financial independence. Inspired by:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire_discussion_july_08_2019/etfdwg1/

    Args:
        annual_spend: the amount of money you plan to spend in retirement.
        stash: the amount of money you've saved.
        withdrawal_rate: your planned safe withdrawl rate expressed as a
        whole percentage. Defaults to 4 for 4%.

    Returns:
        The number of days covered by your stash. This is how many days
        you've already paid for with your savings and the amount of time
        you could theoretically take off every year if you wanted to.
    """
    return (stash * (withdrawal_rate / 100)) / average_daily_spend(annual_spend, 365)


def expected_gross_return(
    expected_return_from_stocks: float,
    expected_bond_yield: float,
    percent_in_stocks: float,
    percent_in_bonds: float,
) -> Percent:
    """Model the expected gross nominal annual return of a stock and bond
    portfolio before investment costs, based on Jonh C. Bogle's forumla
    on p. 102-104 of "The Little Book of Common Sense Investing".
    https://a.co/d/7mVz5Ud

    Args:
        expected_return_from_stocks: expected stock market return expressed
        as a whole percentage (can be calculated with stock_returns).
        expected_bond_yield: bond yield expressed as a whole percentage.
        percent_in_stocks: percentage of the portfolio in stocks expressed as
        a whole percentage.
        percent_in_bonds: percentage of the portfolio in bonds expressed as a
        whole percentage.

    Returns:
        Expected return from a portfolio made up of stocks and bonds.
    """
    bonds = percent_return_for_percent(expected_bond_yield, percent_in_bonds)
    stocks = percent_return_for_percent(expected_return_from_stocks, percent_in_stocks)
    return Percent(sum([stocks, bonds]))


def fi_age(
    expected_inflation_adjusted_return: float,
    annual_savings_amount: float,
    stash: float,
    fi_number: float,
    current_age: int,
) -> int:
    """Calculate the age at which you will reach FIRE based on your current
    trajectory. Credit: eseligsohn https://www.reddit.com/r/financialindependence/comments/92d35t/what_is_this_coast_number_people_are_talking_about/e36titl/

    Args:
        expected_inflation_adjusted_return: Expected inflation adjusted return
        expressed as a whole percentage, e.g. 7 for 7%.
        annual_savings_amount: annual savings amount, the amount of money you
        save towards FI each year.
        stash: invested assests, the amount of money you have currently saved
        and invested for FI.
        fi_number: the number you need to reach FI.
        current_age: your current age.

    Returns:
        FI age, int, the age at which you will FIRE based on your current
        habits.
    """
    fi_num = fi_number * -1
    with numpy.errstate(divide='ignore'):
        return int(
            npf.nper(
                (expected_inflation_adjusted_return / 100),
                annual_savings_amount,
                stash,
                fi_num,
            )
            + current_age
        )


def fi_number(planned_yearly_expenses: float, withdrawal_rate: float) -> Money:
    """Calculate your FI number based on your planned yearly expenses and withdrawal
    rate.

    Args:
        planned_yearly_expenses: the amount of money you think you will spend in
        retirement on an annual basis.
        withdrawal_rate: the rate you expect to withdral money annually e.g. 4
        (for 4%, based on the Trinity Study).

    Returns:
        FI number.
    """
    return Money(Decimal(planned_yearly_expenses) * Decimal(100.0)) / Decimal(
        withdrawal_rate
    )


def future_value(
    present_value: float, annual_rate: float, periods_per_year: int, years: int
) -> Money:
    """Calculates the future value of money invested at an interest rate,
    x times per year, for a given number of years. Can also be used to
    calculate the future equivalent of money due to inflation.

    Args:
        present_value: the current quantity of money (principal).
        annual_rate: interest rate expressed as a whole percentage, e.g.
        5 for 5%, the interest rate paid out.
        periods_per_year: the number of times money is invested per year.
        years: the number of years invested.

    Returns:
        The future value of the money invested with compound interest.
    """

    # The nominal interest rate per period (rate) is how much interest you earn
    # during a particular length of time, before accounting for compounding.
    # This is typically expressed as a percentage.
    rate_per_period = Decimal(annual_rate / 100) / Decimal(periods_per_year)

    # How many periods in the future the calculation is for.
    periods = Decimal(periods_per_year) * Decimal(years)

    return Money(Decimal(present_value) * (1 + rate_per_period) ** periods)


def get_percentage(a: float, b: float, i: bool = False, r: bool = False) -> Percent:
    """Calculate the percentage that one number is of another.

    Args:
        a: the lesser number.
        b: the greater number that the lesser number is a percentage of.
        i: bool, True if the user wants the result returned as a whole number.
        r: bool, True if the user wants the result rounded. Rounds to the
        second decimal point.

    Returns:
        Argument a as a percentage of b. Throws a warning if integer is set to
        True and round is set to False.
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

    return Percent(percentage)


def hours_of_life_energy(money_spent: float, real_hourly_wage: float) -> Decimal:
    """Calculate the hours of life energy something costs by dividing money
    spent by your real hourly wage. From "Your Money or Your Life" by
    Vicki Robin and Joe Dominguez, Chapter 3, https://a.co/d/0fBQcbf

    Args:
        money_spent: int or float, the amount of money spent or price of something.
        real_hourly_wage: float, the true amount of money you earn after adjustments
        have been made for work related expenses and additional work related time
        commitments, e.g. commuting, work clothes, time decompressing, etc.

    Returns:
        Hours of life energy you spent to pay for the money spent.
    """
    try:
        return Decimal(money_spent / real_hourly_wage)
    except (ZeroDivisionError):
        return Decimal(0)


def likely_real_return(
    nominal_gross_return: float, investment_costs: float, inflation: float
) -> Percent:
    """Model the likely return of a portfolio using the relentless rules of humble
    artithmetic as explained by Jack Bogle on page 105 or "The Little Book of Common
    Sense Investing". https://a.co/d/7mVz5Ud


    Args:
        nominal_gross_return: expected gross return expressed as a whole percentage
        (can be calculated by expected_gross_return).
        investment_costs: fees and investment costs expressed as a whole percentage.
        inflation: inflation rate expressed as a whole percentage.

    Returns:
        The likely real return of a portfolio after investing costs and inflation
        have been taken out.
    """
    nominal_net_return = nominal_gross_return - investment_costs
    real_annual_return = nominal_net_return - inflation
    return Percent(real_annual_return)


def monthly_investment_income(stash: float, current_interest_rate: float) -> Money:
    """Calculate how much monthly income you generate from your investments.
    From "Your Money or Your Life" by Vicki Robin and Joe Dominguez, Chapter 8,
    https://a.co/d/0fBQcbf

    Args:
        stash: your capital, the amount of money you have invested.
        current_interest_rate: the interest rate your money earns expressed as a whole
        percentage, e.g. 4 for 4%, synonymous with safe withdrawal rate in this context.

    Returns:
        Monthly investment income, the amount of money you can expect to make
        from your investments monthly.
    """
    return Money(
        (Decimal(stash) * (Decimal(current_interest_rate) / Decimal(100))) / Decimal(12)
    )


def opportunity_cost(
    cost: float, interest_rate: float = 8, time_period: float = 1
) -> Money:
    """Calculate the opportunity cost of money you might spend. This is the amount
    of money you might earn at a given interest rate over a period of time (usually
    years) if the money were invested instead. From Chapter 4 of "The Simple Path
    to Wealth: Your road map to financial independence and a rich, free life" by
    JL Collins, https://a.co/d/9BMocT1

    Args:
        cost: price or cost of something you are thinking about buying or have
        bought.
        interest_rate: the interest rate your money will likely earn if it were
        invested instead.
        time_period: a given time period, normally a number of years.

    Returns:
        Opportunity cost, the amount of money you might lose over a period of
        time by spending the money rather than investing it.
    """
    return Money(future_value(cost, interest_rate, 1, time_period) - Decimal(cost))


def percent_decrease(original_value: float, final_value: float) -> Percent:
    """Calculate the percentage of loss from one number to another.

    Args:
        original_value: int or float, the starting number.
        final_value: int or float, the final number after all losses.

    Returns:
        The decrease from one number to another expressed as a percentage.
    """
    try:
        return Percent(
            abs(float(((original_value - final_value) / original_value)) * 100)
        )
    except (ZeroDivisionError):
        return nan


def percent_increase(original_value: float, final_value: float) -> Percent:
    """Calculate the percentage of growth from one number to another.

    Args:
        original_value: int or float, the starting number.
        final_value: int or float, the final number after all gains.

    Returns:
        The increase from one number to another expressed as a percentage.
    """
    try:
        return Percent(((final_value - original_value) / abs(original_value)) * 100)
    except (ZeroDivisionError):
        return nan


def percent_return_for_percent(
    percent_return: float, percentage_of_portfolio: float
) -> Percent:
    """Calculate the percent of a potential return to attribute to a
    percentage of a portfolio. This function is used in modeling projected
    returns for portfolios of different asset classes.

    Args:
        percent_return: the expected percent return expressed as a whole
        percentage.
        percentage_of_portfolio: the percentage of your portfolio that
        the return applies to.

    Returns:
        Given a % return for an asset class, this function will return the
        percent returned for that asset class as it represents x% of a
        portfolio.
    """
    return Percent((percent_return / 100) * percentage_of_portfolio)


def pot_score(
    median_starting_salary: float, hourly_minimum_wage: float, total_tuition_cost: float
) -> Decimal:
    """Calculate Pay-Over-Tuition to evaluate whether a degree is worth it to see
    how much you can expect to raise your annual earning power per dollar spent
    on a degree. Credit for this calculation goes to Kristy Shen and Bryce Leung
    https://a.co/d/6k3t1oH

    Args:
        median_starting_salary: the median annual starting salary for the job a
        given degree will pay in the state where you plan to live.

        hourly_minimum_wage: the hourly minimum wage in the state where you plan
        to live.

        total_tuition_cost: the total cost of tuition for a given degree.

    Returns:
        Pay-Over-Tuition, a score for comparing degrees between various possible
        career paths. Though expressed as a decimal, the POT score correlates to
        money, e.g. a POT score of 1.3 will return $1.30 for every dollar spent
        on tuition, every year after graduation, assuming you earn an average salary
        in your chosen profession. Multiply the full cost of a degree (tuition) by
        the POT score to see how much money you will earn above minimum wage, per
        year, after graduation.
    """
    annual_minimum_wage = (Decimal(hourly_minimum_wage) * Decimal(40)) * Decimal(52)
    pot = (Decimal(median_starting_salary) - annual_minimum_wage) / Decimal(
        total_tuition_cost
    )
    return pot


def real_hourly_wage(
    hours_worked: float,
    money_paid: float,
    benefits: float,
    additional_work_related_hours: float,
    additional_work_related_expenses: float,
) -> Money:
    """Calculate your real hourly wage by adjusting your money paid by
    subtracting auxiliary work related expenses (e.g. work clothes, cost
    of commuting, etc.) and by adjusting your hours worked by adding
    auxiliary work related time committments (e.g. time spent commuting,
    time spent decompressing, etc.). From "Your Money or Your Life" by
    Vicki Robin and Joe Dominguez, Chapter 2, https://a.co/d/0fBQcbf

    Args:
        hours_worked: the number of hours worked.
        money_paid: how much you were paid.
        benefits: the value of employer supplied benefits (401k match, health
        insurance, etc.).
        additional_work_related_hours: additional time spent for work such as
        time commuting or time spent on escape entertainment after work.
        additional_work_related_expenses: additional work related expenses
        such as the cost of commuting, lunches out, work clothes, etc.

    Returns:
        Your real hourly wage adjusted for additional work related time
        commitments and additional work related expenses.
    """
    real_pay = money_paid + benefits - additional_work_related_expenses
    real_hours = hours_worked + additional_work_related_hours
    return Money(real_pay / real_hours)


def redeem_points(points: int, rate: float = 1) -> Money:
    """Calculates the value of travel rewards points based on a conversion
    rate. The default rate is 1% which is the cash value of awards points
    for most cards.

    Args:
        points: the number of awards points to be redeemed.
        rate: defaults to 1 which is the exchange rate for most points
        to cash (1 cent per point).

    Returns:
        Dollar amount the points are worth.
    """
    return Money(Decimal(points * (rate / 100)).quantize(CENTS, ROUND_HALF_UP))


def redeem_chase_points(points: int) -> dict:
    """Calculates the value of Chase Ultimate Rewards points for different
    exchange scenarios. Based on the ChooseFI Sweet Redemption article:
    https://www.choosefi.com/travel-rewards-part-3-sweet-redemption/

    Args:
        points: number of Ultimate Rewards points to redeem.

    Returns:
        A dictionary containing common Chase Ultimate Rewards redemption
        scenarios including cash value, Sapphire Preferred portal, Sapphire
        Reserve portal and target partner exchange (the guideline for direct
        transfer of points to Chase Ultimate Reward partners such as United
        Airlines). Target partner exchange is the aspirational goal for an
        exchange with a partner, not a guarantee.
    """
    return {
        'Cash value': redeem_points(points),
        'Sapphire Preferred portal': redeem_points(points, 1.25),
        'Sapphire Reserve portal': redeem_points(points, 1.5),
        'Target partner exchange': redeem_points(points, 2),
    }


def remaining_life_expectancy(
    your_age: int,
    time_unit: MeasureOfTime = 'hours',
    more_accurate: bool = True,
    exclude_time_asleep: bool = False,
) -> TimeUnit:
    """Calculate the amount of time you have left to live based on averages
    from the "United States Life Tables, 2013," National Vital Statistics
    Reports 66, no. 3 (2017): 1–64 which can be found at https://ftp.cdc.gov/pub/health_Statistics/nchs/publications/NVSR/66_03/Table01.xlsx
    This is the same data used in "Your Money or Your Life" by Vicki Robin and
    Joe Dominguez, Chapter 2, https://a.co/d/0fBQcbf which is the inspiration
    for this function.

    Args:
        your_age: int, your age.
        time_unit: str, "hours", "days", "months", or "years".
        more_accurate: bool, if True, will use 365.2425 as the length of
        a year instead of the proverbial 365 used by Vicki Robin and Joe
        Dominguez.
        exclude_time_asleep: bool, if set to True, the function will
        assume you lose half your time to sleep and other mundane tasks.

    Returns:
        The amount of time more on average that you are expected to live
        based on your current age, how much time you *might* have left.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    spreadsheet = os.path.join(root_dir, 'data', 'Table01.xlsx')
    life_table = pd.read_excel(
        spreadsheet, sheet_name='Table 1', skiprows=1, skipfooter=1
    )

    age_ranges = life_table['Age (years)'].str.split('–', expand=True)
    age_ranges = age_ranges.map(lambda x: pd.to_numeric(x, errors='coerce'))
    age_ranges.iloc[-1, 0] = float(100)
    age_ranges.iloc[-1, 1] = float('inf')

    mask = (age_ranges[0] <= your_age) & (your_age < age_ranges[1])
    life_expectancy = life_table.loc[mask, 'Expectation of life at age x'].iloc[0]

    years = round(Decimal(life_expectancy), 1)
    year_len = Decimal(365)
    if more_accurate is True:
        year_len = Decimal(365.2425)

    if exclude_time_asleep is True:
        years = years / 2
    days = years * year_len
    if time_unit == 'years':
        return Years(years)
    elif time_unit == 'months':
        return Months(years * Decimal(12))
    elif time_unit == 'days':
        return Days(days)
    # Hours
    return Hours(days * Decimal(24))


def rule_of_72(interest_rate: float, accurate: bool = True) -> float:
    """Calculate the time it will take for money to double based on a given
    interest rate: Years to double = 72 / Interest Rate.

    Args:
        interest_rate: float written as a whole percentage, e.g. 7 for 7%.
        accurate: Boolean, when set to True the more accurate 69.3 is used
        instead of 72.

    Returns:
        The number of years it will take for money to double based on an
        interest rate.
    """
    if interest_rate == 0:
        return float('inf')

    if accurate:
        return 69.3 / interest_rate
    return 72.0 / interest_rate


def savings_rate(take_home_pay: float, spending: float) -> Percent:
    """Calculate your savings_rate based on take home pay and spending,
    using the formula laid out by Mr. Money Mustache:
    https://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        take_home_pay: monthly take-home pay.
        spending: monthly spending.

    Returns:
        your monthly savings rate expressed as a percentage.
    """

    try:
        return Percent(
            (Decimal(take_home_pay) - Decimal(spending)) / (Decimal(take_home_pay))
        ) * Decimal(100)
    except (ZeroDivisionError):
        return Percent(Decimal(0))


def spending_from_savings(take_home_pay: float, savings: float) -> Money:
    """Calculate your spending based on your take home pay and how much
    you save. This is useful if you use what Paula Pant calls the anti-budget,
    instead of tracking your spending in detail. This number can be used as
    input for the savings_rate function.

    Args:
        take_home_pay: monthly take-home pay.
        savings: amount of money saved towards FI.

    Returns:
        The amount of money spent.
    """
    return Money(Decimal(take_home_pay) - Decimal(savings))


def stock_returns(
    dividend_yield: float, earnings_growth: float, change_in_pe: float
) -> Percent:
    """Model the expectation of stock returns for the next decade  based on
    Jack Bogle's formula using the sources of stock returns presented on pages
    97-105 of "The Little Book of Common Sense Investing". Bogle believes that
    stock returns come from stock dividends, earnings growth (tied to GDP) and
    swings in the P/E multiple (speculative return). Bond returns come from
    the interest a bond pays. https://a.co/d/7mVz5Ud

    Args:
        dividend_yield: percentage that stocks are currently yielding. Bogle
        used the S&P 500 or Total Stock Market Index.
        earnings_growth: percentage you think stocks will grow per year. Bogle
        notes that this has typically been at the nominal growth rate of GDP
        (4-5% per year) which has a 0.98% correlation with corporate profits.
        change_in_pe: negative or positive percentage of change in today's
        P/E multiple. This number represents the "speculative return".

    Returns:
        The percentage you might expect to earn on an annual basis given the
        current state of the market. This number has no factual basis and is
        not a prediction. It should not be taken as a certainty or advice.
        It's just an educated guess based on common sense.
    """
    return Percent(
        sum([Decimal(dividend_yield), Decimal(earnings_growth), Decimal(change_in_pe)])
    )


def take_home_pay(
    gross_pay: float, employer_match: float, taxes_and_fees: List[float]
) -> Money:
    """Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    https://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        gross_pay: gross monthly pay.
        employer_match: the 401(k) match from your employer.
        taxes_and_fees: taxes and fees deducted from your paycheck.

    Returns:
        Your monthly take-home pay.
    """
    taxes_and_fees = [Decimal(item) for item in taxes_and_fees]
    return Money((Decimal(gross_pay) + Decimal(employer_match)) - sum(taxes_and_fees))


def turnover_costs(turnover_rate: float) -> Percent:
    """Make an educated guess at the cost of portfolio turnover using the rule of
    thumb presented by Jack Bogle on page 55 of "The Little Book of Common Sense
    Investing". https://a.co/d/7mVz5Ud

    Args:
        turnover_rate: turnover rate of an index or mutual fund. This can normally
        be found with the normal characteristics and data on the fund's web page.

    Returns:
        What the turnover might cost based on Jack Bogle's rule of thumb. This
        is not a precise number. It's an educated guess and could be subject to
        change as systems change with technology in the future.
    """
    return Percent(Decimal(0.01) * Decimal(turnover_rate))
