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

import argparse
from decimal import Decimal

import fi


def run_fi():
    """
    Describes the module.
    """
    description = run_annual_cost.__doc__ + str(help(fi.fi))
    parser = argparse.ArgumentParser(  # noqa: F841
        prog='fi modlule',
        description=description,
    )


def run_annual_cost():
    """
    Calculate the depreciation schedule of things bought.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW
    """
    description = run_annual_cost.__doc__
    parser = argparse.ArgumentParser(
        prog='annual_cost',
        description=description,
        epilog='Example use: annual_cost 75 70 2.5',
    )
    parser.add_argument('your_cost', help='int or float, amount paid')
    parser.add_argument('used_price', help='int or float, amount you can sell it for')
    parser.add_argument(
        'years_in_service', help='int or float, number of years you\'ve used it'
    )

    args = parser.parse_args()

    print(fi.annual_cost(args.your_cost, args.used_price, args.years_in_service))


def run_average_daily_spend():
    """
    Calculate the average amount of money spent per day over
    a given number of days.
    """
    description = run_average_daily_spend.__doc__
    parser = argparse.ArgumentParser(
        prog='average_daily_spend',
        description=description,
        epilog='Example use: average_daily_spend 100 10',
    )
    parser.add_argument(
        'money_spent', help='float or Decimal, the amount of money spent'
    )
    parser.add_argument(
        'num_days', help='int, the number of days during which the spending occurred'
    )
    args = parser.parse_args()
    print(fi.average_daily_spend(Decimal(args.money_spent), int(args.num_days)))


def run_buy_a_day_of_freedom():
    """
    Calculate how much it costs to buy a day of freedom based
    on your annual spend and your safe withdrawl rate. Every time
    you save this amount of money, you've covered 1 more day. Once
    you have 365 days, you are financially independent. Credit:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire
    _discussion_july_08_2019/etfdwg1/
    """
    description = run_buy_a_day_of_freedom.__doc__
    parser = argparse.ArgumentParser(
        prog='buy_a_day_of_freedom',
        description=description,
        epilog='Example use: buy_a_day_of_freedom 40000',
    )
    parser.add_argument(
        'annual_spend',
        help='float, the amount of money you plan to spend in retirement',
    )
    parser.add_argument(
        '-r',
        '--rate',
        help='float, your planned safe withdrawl rate. Defaults to 0.04 (4%%)',
        action='store',
    )
    args = parser.parse_args()
    annual_spend = float(args.annual_spend)
    if args.rate:
        print(fi.buy_a_day_of_freedom(annual_spend, float(args.rate)))
    else:
        print(fi.buy_a_day_of_freedom(annual_spend))


def run_coast_fi():
    """
    Calculate your CoastFI number. The number at which you
    can coast to FI without contributing any more to your
    retirement accounts. Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e34uuxh/
    """
    description = run_coast_fi.__doc__
    parser = argparse.ArgumentParser(
        prog='coast_fi',
        description=description,
        epilog="Example use: coast_fi 800000 .07 62 40",
    )
    parser.add_argument(
        'target_fi_num',
        help='Target FI number. The number you will need invested in order to live off interest',
    )
    parser.add_argument('eiar', help='Expected inflation adjusted return e.g. .07')
    parser.add_argument('retirement_age', help='The age you want to retire')
    parser.add_argument('current_age', help='Your current age')

    args = parser.parse_args()

    print(
        fi.coast_fi(
            args.target_fi_num, args.eiar, args.retirement_age, args.current_age
        )
    )


def run_cost_of_costs():
    """
    Calculate the "tyranny of compounding costs" as laid out by Jack Bogle
    on pages 47-49 of "The Little Book of Common Sense Investing". This is how
    much your investing expenses cost you over time. According to Jack Bogle
    there are three primary sources of costs: 1. The fund's expense ratio, 2.
    The sales charge paid on each purchase of shares (loads), and 3. The cost
    of the purchase and sale of securities within a fund (turnover costs).
    https://a.co/d/7mVz5Ud
    """
    description = run_cost_of_costs.__doc__
    parser = argparse.ArgumentParser(
        prog='cost_of_costs',
        description=description,
        epilog="Example use: cost_of_costs 10000 7 2 50",
    )
    parser.add_argument(
        'money_invested',
        help='principal, dollar amount',
    )
    parser.add_argument(
        'interest_rate', help='expected annual return expressed as a whole percentage'
    )
    parser.add_argument(
        'investment_costs',
        help='annual investment costs expressed as a whole percentage. This could simply \
        be a fund\'s expense ratio, however, more accurate input might include turnover \
        costs, loads, and any other fees',
    )
    parser.add_argument(
        'time_period',
        help='investing time horizon, how long the investment will be held, \
        should be a number of years',
    )

    args = parser.parse_args()

    print(
        fi.cost_of_costs(
            Decimal(args.money_invested),
            Decimal(args.interest_rate),
            Decimal(args.investment_costs),
            Decimal(args.time_period),
        )
    )


def run_cost_per_use():
    """
    Calculate how much something has costed while considering
    how many times it has been used. Wrapper function for
    annual_cost.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW
    """
    description = run_cost_per_use.__doc__
    parser = argparse.ArgumentParser(
        prog='cost_per_use',
        description=description,
        epilog='Example use: cost_per_use 75 15 15',
    )
    parser.add_argument('your_cost', help='int or float, amount paid')
    parser.add_argument('used_price', help='int or float, amount you can sell it for')
    parser.add_argument(
        'times_used', help='int or float, number of times you\'ve used it'
    )

    args = parser.parse_args()

    print(fi.cost_per_use(args.your_cost, args.used_price, args.times_used))


def run_days_covered_by_fi():
    """
    Calculate the number of days per year covered by your savings.
    This is a way of seeing where you are on your FI journey. For
    example, 182.5 days would put you at 50% FI. 365 days would put
    you at 100% FI or full financial independence. Inspired by:
    https://www.reddit.com/r/leanfire/comments/caka4t/weekly_leanfire
    _discussion_july_08_2019/etfdwg1/
    """
    description = run_days_covered_by_fi.__doc__
    parser = argparse.ArgumentParser(
        prog='days_covered_by_fi',
        description=description,
        epilog='Example use: days_covered_by_fi 40000 500000 .03',
    )
    parser.add_argument(
        'annual_spend',
        help='float, the amount of money you plan to spend in retirement',
    )
    parser.add_argument('stash', help='float, the amount of money you\'ve saved')
    parser.add_argument(
        '-r',
        '--rate',
        help='float, your planned safe withdrawl rate. Defaults to 0.04 (4%%)',
        action='store',
    )
    args = parser.parse_args()
    if args.rate:
        print(
            fi.days_covered_by_fi(
                float(args.annual_spend), float(args.stash), float(args.rate)
            )
        )
    else:
        print(fi.days_covered_by_fi(float(args.annual_spend), float(args.stash)))


def run_expected_gross_return():
    """
    Model the expected gross nominal annual return of a stock and bond
    portfolio before investment costs, based on Jonh C. Bogle's forumla
    on p. 102-104 of "The Little Book of Common Sense Investing".
    https://a.co/d/7mVz5Ud
    """
    description = run_expected_gross_return.__doc__
    parser = argparse.ArgumentParser(
        prog='expected_gross_return',
        description=description,
        epilog='Example use: expected_gross_return 4 3.1 60 40',
    )
    parser.add_argument(
        'expected_return_from_stocks',
        help='expected stock \
        market return expressed as a whole percentage(can be calculated with \
        stock_returns)',
    )
    parser.add_argument(
        'expected_bond_yield', help='bond yield expressed as a whole percentage'
    )
    parser.add_argument(
        'percent_in_stocks',
        help='percentage of the portfolio in stocks expressed as a whole percentage',
    )
    parser.add_argument(
        'percent_in_bonds',
        help='percentage of the portfolio in bonds expressed as a whole percentage',
    )

    args = parser.parse_args()
    print(
        fi.expected_gross_return(
            float(args.expected_return_from_stocks),
            float(args.expected_bond_yield),
            float(args.percent_in_stocks),
            float(args.percent_in_bonds),
        )
    )


def run_fi_age():
    """
    Calculate the age at which you will reach FIRE. Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e36titl/
    """
    description = run_fi_age.__doc__
    parser = argparse.ArgumentParser(
        prog='fi_age',
        description=description,
        epilog='Example use: fi_age .07, 30000, 200000, 800000, 40',
    )
    parser.add_argument('eiar', help='expected inflation adjusted return e.g. .07')
    parser.add_argument(
        'asa',
        help='annual savings amount, the amount of money you will save towards FI each year',
    )
    parser.add_argument(
        'stash',
        help='invested assests, the amount of money you have currently saved and invested for FI',
    )
    parser.add_argument('fi_num', help='the number you need to reach FI')
    parser.add_argument('ca', help='your current age')

    args = parser.parse_args()

    print(
        fi.fi_age(
            float(args.eiar),
            float(args.asa),
            float(args.stash),
            float(args.fi_num),
            float(args.ca),
        )
    )


def run_fi_number():
    """
    Calculates FI number based on planned yearly expenses and withdrawal rate.
    """
    description = run_fi_number.__doc__
    parser = argparse.ArgumentParser(
        prog='planned_yearly_expenses',
        description=description,
        epilog='Example use: fi_number 1000000 4',
    )
    parser.add_argument(
        'planned_yearly_expenses',
        help='int or float, the amount of money you think you will spend in \
        retirement on an annual basis',
    )
    parser.add_argument(
        'withdrawal_rate',
        help='int or float, the rate you expect to withdral money annually \
        e.g. 4 (for 4%%, based on the Trinity Study)',
    )
    args = parser.parse_args()
    print(
        fi.fi_number(float(args.planned_yearly_expenses), float(args.withdrawal_rate))
    )


def run_future_value():
    """
    Calculates the future value of money invested at an interest rate,
    x times per year, for a given number of years. Can also be used to
    calculate the future equivalent of money due to inflation.
    """
    description = run_future_value.__doc__
    parser = argparse.ArgumentParser(
        prog='future_value',
        description=description,
        epilog="Example use: future_value 800000 .03 1 20",
    )
    parser.add_argument(
        'present_value', help='int or float, the current quantity of money, principal'
    )
    parser.add_argument(
        'annual_rate',
        help='float 0 to 1 e.g., .5 = 50 percent, the interest rate paid out',
    )
    parser.add_argument(
        'periods_per_year', help='int, the number of times money is invested per year'
    )
    parser.add_argument('years', help='int, the number of years invested')
    args = parser.parse_args()
    print(
        fi.future_value(
            args.present_value, args.annual_rate, args.periods_per_year, args.years
        )
    )


def run_get_percentage():
    """
    Calculate what percentage a given number is of another,
    e.g. 50 is 50% of 100.
    """
    description = run_get_percentage.__doc__
    parser = argparse.ArgumentParser(
        prog='get_percentage',
        description=description,
        epilog="Example use: get_percentage 25 100",
    )
    parser.add_argument(
        'a', help='Integer or floating point number that is a percent of another number'
    )
    parser.add_argument(
        'b',
        help='Integer or floating point number of which the first number is a percent',
    )
    args = parser.parse_args()
    print(fi.get_percentage(float(args.a), float(args.b)))


def run_hours_of_life_energy():
    """
    Calculate the hours of life energy something costs by dividing money spent by your
    real hourly wage.
    """
    description = run_hours_of_life_energy.__doc__
    parser = argparse.ArgumentParser(
        prog='hours_of_life_energy',
        description=description,
        epilog="Example use: hours_of_life_energy 80 10",
    )
    parser.add_argument(
        'money_spent', help='The amount of money spent or price of something'
    )
    parser.add_argument(
        'real_hourly_wage',
        help='The true amount of money you earn after adjustments have been made for \
        work related expenses and additional work related time commitments',
    )
    args = parser.parse_args()
    print(
        fi.hours_of_life_energy(float(args.money_spent), float(args.real_hourly_wage))
    )


def run_likely_real_return():
    """
    Model the likely return of a portfolio using the relentless rules of humble
    artithmetic as explained by Jack Bogle on page 105 or "The Little Book of Common
    Sense Investing". https://a.co/d/7mVz5Ud
    """
    description = run_likely_real_return.__doc__
    parser = argparse.ArgumentParser(
        prog='likely_real_return',
        description=description,
        epilog="Example use: likely_real_return 3.6 1.5 2",
    )
    parser.add_argument(
        'nominal_gross_return',
        help='expected gross return expressed as a whole percentage \
        (can be calculated by expected_gross_return)',
    )
    parser.add_argument(
        'investment_costs',
        help='fees and investment costs expressed as a whole percentage',
    )
    parser.add_argument(
        'inflation',
        help='inflation rate expressed as a whole percentage',
    )
    args = parser.parse_args()
    print(
        fi.likely_real_return(
            float(args.nominal_gross_return),
            float(args.investment_costs),
            float(args.inflation),
        )
    )


def run_monthly_investment_income():
    """
    Calculate how much monthly income you generate from your investments.
    From "Your Money or Your Life" by Vicki Robin and Joe Dominguez, Chapter 8,
    https://a.co/d/0fBQcbf
    """
    description = run_monthly_investment_income.__doc__
    parser = argparse.ArgumentParser(
        prog='monthly_investment_income',
        description=description,
        epilog="Example use: monthly_investment_income 500000 4",
    )
    parser.add_argument(
        'stash', help='Your capital, the amount of money you have invested'
    )
    parser.add_argument(
        'current_interest_rate',
        help='The interest rate your money earns expressed as a whole percentage, \
        e.g. 4 for 4%%, synonymous with safe withdrawal rate in this context',
    )
    args = parser.parse_args()
    print(
        fi.monthly_investment_income(
            float(args.stash), float(args.current_interest_rate)
        )
    )


def run_opportunity_cost():
    """
    Calculate the opportunity cost of money you might spend. This is the amount
    of money you might earn at a given interest rate over a period of time (usually
    years) if the money were invested instead. From Chapter 4 of "The Simple Path
    to Wealth: Your road map to financial independence and a rich, free life" by
    JL Collins, https://a.co/d/9BMocT1
    """
    description = run_opportunity_cost.__doc__
    parser = argparse.ArgumentParser(
        prog='opportunity_cost',
        description=description,
        epilog="Example use: opportunity_cost 20000 8 1",
    )
    parser.add_argument(
        'cost',
        help='Price or cost of something you are thinking about buying or have bought',
    )
    parser.add_argument(
        'interest_rate',
        help='The interest rate your money will likely earn if it were invested instead',
    )
    parser.add_argument(
        'time_period', help='A given time period, normally a number of years'
    )
    args = parser.parse_args()
    print(
        fi.opportunity_cost(
            Decimal(args.cost), Decimal(args.interest_rate), Decimal(args.time_period)
        )
    )


def run_percent_decrease():
    """
    Calculates the percentage of loss from one number to another.
    """
    description = run_percent_decrease.__doc__
    parser = argparse.ArgumentParser(
        prog='percent_decrease',
        description=description,
        epilog="Example use: percent_decrease 10 5",
    )
    parser.add_argument('original_value', help='int or float, the original number')
    parser.add_argument(
        'final_value', help='int or float, the final number after all losses'
    )
    args = parser.parse_args()
    print(fi.percent_decrease(float(args.original_value), float(args.final_value)))


def run_percent_increase():
    """
    Calculates the percentage of growth from one number to another.
    """
    description = run_percent_increase.__doc__
    parser = argparse.ArgumentParser(
        prog='percent_increase',
        description=description,
        epilog="Example use: percent_increase 5 10",
    )
    parser.add_argument('original_value', help='int or float, the original number')
    parser.add_argument(
        'final_value', help='int or float, the final number after all gains'
    )
    args = parser.parse_args()
    print(fi.percent_increase(float(args.original_value), float(args.final_value)))


def run_percent_return_for_percent():
    """
    Calculate the percent of a potential return to attribute to a
    percentage of a portfolio. This function is used in modeling projected
    returns for portfolios of different asset classes.
    """
    description = run_percent_return_for_percent.__doc__
    parser = argparse.ArgumentParser(
        prog='percent_return_for_percent',
        description=description,
        epilog="Example use: percent_return_for_percent 100 50",
    )
    parser.add_argument(
        'percent_return',
        help='the expected percent return expressed as a whole percentage',
    )
    parser.add_argument(
        'percentage_of_portfolio',
        help='the percentage of your portfolio that the return applies to',
    )
    args = parser.parse_args()
    print(
        fi.percent_return_for_percent(
            float(args.percent_return), float(args.percentage_of_portfolio)
        )
    )


def run_pot_score():
    """
    Pay-Over-Tuition: evaluate whether a degree is worth it by calculating
    how much you can expect to raise your annual earning power per dollar spent
    on the degree.
    """
    description = run_pot_score.__doc__
    parser = argparse.ArgumentParser(
        prog='pot_score',
        description=description,
        epilog="Example use: pot_score 27000 11 42600",
    )
    parser.add_argument(
        'median_starting_salary',
        help='median annual starting salary for the job you will get with \
        the degree where you plan to live',
    )
    parser.add_argument(
        'hourly_minimum_wage',
        help='hourly minimum wage in the state where you plan to live',
    )
    parser.add_argument(
        'total_tuition_cost',
        help='the total cost of tuition for a given degree',
    )
    args = parser.parse_args()
    print(
        fi.pot_score(
            float(args.median_starting_salary),
            float(args.hourly_minimum_wage),
            float(args.total_tuition_cost),
        )
    )


def run_real_hourly_wage():
    """
    Calculate your real hourly wage by adjusting your money paid by
    subtracting auxiliary work related expenses (e.g. work clothes, cost
    of commuting, etc.) and by adjusting your hours worked by adding
    auxiliary work related time committments (e.g. time spent commuting,
    time spent decompressing, etc.).
    """
    description = run_real_hourly_wage.__doc__
    parser = argparse.ArgumentParser(
        prog='real_hourly_wage',
        description=description,
        epilog="Example use: real_hourly_wage 40 1000 0 30 300",
    )
    parser.add_argument('hours_worked', help='float, the number of hours worked')
    parser.add_argument('money_paid', help='float, how much you were paid')
    parser.add_argument(
        'benefits',
        help='float, the value of employer supplied benefits (401k match, health \
        insurance, etc.)',
    )
    parser.add_argument(
        'additional_work_related_hours',
        help='float, additional time spent for work such as time commuting or time \
        spent on escape entertainment after work',
    )
    parser.add_argument(
        'additional_work_related_expenses',
        help='float, additional work related expenses such as the cost of commuting, \
        lunches out, work clothes, etc.',
    )
    args = parser.parse_args()
    print(
        fi.real_hourly_wage(
            float(args.hours_worked),
            float(args.money_paid),
            float(args.benefits),
            float(args.additional_work_related_hours),
            float(args.additional_work_related_expenses),
        )
    )


def run_redeem_chase_points():
    """
    Calculates the value of Chase Ultimate Rewards points for different
    exchange scenarios. Based on the ChooseFI Sweet Redemption article:
    https://www.choosefi.com/travel-rewards-part-3-sweet-redemption/
    """
    description = run_redeem_chase_points.__doc__
    parser = argparse.ArgumentParser(
        prog='redeem_chase_points',
        description=description,
        epilog="Example use: redeem_chase_points 50000",
    )
    parser.add_argument('points', help='int, number of points you plan to redeem')
    args = parser.parse_args()
    cp = fi.redeem_chase_points(float(args.points))
    cv = str(cp['cv'])
    spp = str(cp['spp'])
    srp = str(cp['srp'])
    tpe = str(cp['tpe'])
    print(f'Cash Value ------------------ {cv}')
    print(f'Sapphire Preferred Portal --- {spp}')
    print(f'Sapphire Reserved Portal ---- {srp}')
    print(f'Target Partner Exchange ----- {tpe}*')
    print()
    print('* Target Partner Exchange is only a guideline. Shoot for this amount')
    print('  or better when trading points for miles with a Chase Ultimate')
    print('  Rewards partner.')


def run_redeem_points():
    """
    Calculates the value of travel rewards points based on a conversion
    rate. The default rate is 0.01 which is the cash value of awards
    points for most cards.
    """
    description = run_redeem_points.__doc__
    parser = argparse.ArgumentParser(
        prog='redeem_points',
        description=description,
        epilog="Example use: redeem_points 50000 -r .0125",
    )
    parser.add_argument('points', help='int, number of points you plan to redeem')
    parser.add_argument(
        '-r',
        '--rate',
        help='float, exchange rate for points. Defaults to 0.01 which is the exchange \
        rate for cash for the majority of cards (1 cent per point)',
        action='store',
    )
    args = parser.parse_args()
    if args.rate:
        print(fi.redeem_points(float(args.points), float(args.rate)))
    else:
        print(fi.redeem_points(float(args.points)))


def run_remaining_life_expectancy():
    """
    Calculate the amount of time you have left to live based on averages
    from the "United States Life Tables, 2013," National Vital Statistics
    Reports 66, no. 3 (2017): 1–64. This is the same data used in "Your
    Money or Your Life" by Vicki Robin and Joe Dominguez, Chapter 2,
    https://a.co/d/0fBQcbf which is the inspiration for this function.
    """
    description = run_remaining_life_expectancy.__doc__
    parser = argparse.ArgumentParser(
        prog='remaining_life_expectancy',
        description=description,
        epilog="Example use: remaining_life_expectancy 45 -t hours -e",
    )
    parser.add_argument('your_age', type=int, help='int, your age')
    parser.add_argument(
        '-t',
        '--time_unit',
        help='str, "hours", "days", "months", or "years"',
        required=False,
        default='hours',
        action='store',
    )
    parser.add_argument(
        '-l',
        '--less_accurate',
        dest='more_accurate',
        help='bool, if set the function will use 365 as the length of a year \
        to match what Vicki Robin and Joe Dominguez did in "Your Money or Your Life"',
        required=False,
        action='store_false',
    )
    parser.add_argument(
        '-e',
        '--exclude_time_asleep',
        help='bool, if set to True, the function will assume you lose half your \
        time to sleep and other mundane tasks',
        required=False,
        action='store_true',
    )
    args = parser.parse_args()
    print(fi.remaining_life_expectancy(**vars(args)))


def run_rule_of_72():
    """
    Calculate the time it will take for money to double
    based on a given interest rate:

    Years to double = 72 / Interest Rate
    """
    description = run_rule_of_72.__doc__
    parser = argparse.ArgumentParser(
        prog='rule_of_72',
        description=description,
        epilog="Example use: rule_of_72 8 -a",
    )
    parser.add_argument(
        'interest_rate',
        help='Integer or floating point number representing the interest rate \
              at which your money will grow e.g. 7 for 7 percent',
    )
    parser.add_argument(
        '-a',
        '--accurate',
        help='When set to True the more accurate 69.3 is used instead of 72',
        action='store_true',
    )
    args = parser.parse_args()
    if args.accurate:
        print(fi.rule_of_72(float(args.interest_rate), True))
    else:
        print(fi.rule_of_72(float(args.interest_rate)))


def run_savings_rate():
    """
    Calculate your savings_rate based on take home pay and spending,
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/
    """
    description = run_savings_rate.__doc__
    parser = argparse.ArgumentParser(
        prog='savings_rate',
        description=description,
        epilog="Example use: savings_rate 13839 8919",
    )
    parser.add_argument('take_home_pay', help='float or int, monthly take-home pay')
    parser.add_argument('spending', help='float or int, monthly spending')
    args = parser.parse_args()
    print(fi.savings_rate(args.take_home_pay, args.spending))


def run_spending_from_savings():
    """
    Calculate your spending based on your take home pay and how much
    you save. This is useful if you use what Paula Pant calls the anti-budget,
    instead of tracking your spending in detail. This number can be used as
    input for the savings_rate function.
    """
    description = run_spending_from_savings.__doc__
    parser = argparse.ArgumentParser(
        prog='spending_from_savings',
        description=description,
        epilog="Example use: spending_from_savings 5000 2750",
    )
    parser.add_argument('take_home_pay', help='float or int, monthly take-home pay')
    parser.add_argument('savings', help='float or int, amount of money saved')
    args = parser.parse_args()
    print(fi.spending_from_savings(args.take_home_pay, args.savings))


def run_stock_returns():
    """
    Model the expectation of stock returns for the next decade  based on
    Jack Bogle's formula using the sources of stock returns presented on pages
    97-105 of "The Little Book of Common Sense Investing". Bogle believes that
    stock returns come from stock dividends, earnings growth (tied to GDP) and
    swings in the P/E multiple (speculative return). Bond returns come from
    the interest a bond pays. https://a.co/d/7mVz5Ud
    """
    description = run_stock_returns.__doc__
    parser = argparse.ArgumentParser(
        prog='stock_returns',
        description=description,
        epilog="Example use: stock_returns 2 4 -2",
    )
    parser.add_argument(
        'dividend_yield',
        help='percentage that stocks are \
        currently yielding. Bogle used the S&P 500 or Total Stock Market Index',
    )
    parser.add_argument(
        'earnings_growth',
        help='percentage you think stocks will grow per year. Bogle notes that \
        this has typically been at the nominal growth rate of GDP (4-5%% per year) \
        which has a 0.98%% correlation with corporate profits',
    )
    parser.add_argument(
        'change_in_pe',
        help='negative or positive percentage of change in today\'s P/E multiple. \
        This number represents the "speculative return"',
    )
    args = parser.parse_args()
    print(
        fi.stock_returns(args.dividend_yield, args.earnings_growth, args.change_in_pe)
    )


def run_take_home_pay():
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/
    """
    description = run_take_home_pay.__doc__
    parser = argparse.ArgumentParser(
        prog='rule_of_72',
        description=description,
        epilog="Example use: take_home_pay 1500 1000 '250 250'",
    )
    parser.add_argument('gross_pay', help='float or int, gross monthly pay')
    parser.add_argument(
        'employer_match', help='float or int, the 401(k) match from your employer'
    )
    parser.add_argument(
        'taxes_and_fees',
        help='list, taxes and fees that are deducted from your paycheck',
    )
    args = parser.parse_args()
    taxes = [Decimal(item) for item in args.taxes_and_fees.split(' ')]
    print(fi.take_home_pay(args.gross_pay, args.employer_match, taxes))


def run_turnover_costs():
    """
    Make an educated guess at the cost of portfolio turnover using the rule of
    thumb presented by Jack Bogle on page 55 of "The Little Book of Common Sense
    Investing". https://a.co/d/7mVz5Ud
    """
    description = run_turnover_costs.__doc__
    parser = argparse.ArgumentParser(
        prog='turnover_costs',
        description=description,
        epilog="Example use: turnover_costs 40",
    )
    parser.add_argument(
        'turnover_rate',
        help='turnover rate of an index or mutual fund. This can normally be found \
        with the normal characteristics and data on the fund\'s web page',
    )
    args = parser.parse_args()
    print(fi.turnover_costs(args.turnover_rate))
