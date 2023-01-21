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
        epilog="example use: spending_from_savings 5000 2750",
    )
    parser.add_argument('take_home_pay', help='float or int, monthly take-home pay')
    parser.add_argument('savings', help='float or int, amount of money saved')
    args = parser.parse_args()
    print(fi.spending_from_savings(args.take_home_pay, args.savings))


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
