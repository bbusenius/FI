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
    parser = argparse.ArgumentParser(prog='annual_cost',
                                     description=description,
                                     epilog='Example use: annual_cost 75 70 2.5')
    parser.add_argument(
        'your_cost', help='int or float, amount paid')
    parser.add_argument(
        'used_price', help='int or float, amount you can sell it for')
    parser.add_argument('years_in_service',
                        help='int or float, number of years you\'ve used it')

    args = parser.parse_args()

    print(fi.annual_cost(args.your_cost, args.used_price, args.years_in_service))


def run_coast_fi():
    """
    Calculate your CoastFI number. The number at which you
    can coast to FI without contributing any more to your
    retirement accounts. Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e34uuxh/
    """
    description = run_coast_fi.__doc__
    parser = argparse.ArgumentParser(prog='coast_fi',
                                     description=description,
                                     epilog="Example use: coast_fi 800000 .07 62 40")
    parser.add_argument(
        'target_fi_num', help='Target FI number. The number you will need invested in order to live off interest')
    parser.add_argument(
        'eiar', help='Expected inflation adjusted return e.g. .07')
    parser.add_argument('retirement_age', help='The age you want to retire')
    parser.add_argument('current_age', help='Your current age')

    args = parser.parse_args()

    print(fi.coast_fi(args.target_fi_num, args.eiar,
                      args.retirement_age, args.current_age))


def run_cost_per_use():
    """
    Calculate how much something has costed while considering
    how many times it has been used. Wrapper function for
    annual_cost.

    Credit: Early Retirement Extreme by Jacob Lund Fisker
    http://a.co/4vgBczW
    """
    description = run_cost_per_use.__doc__
    parser = argparse.ArgumentParser(prog='cost_per_use',
                                     description=description,
                                     epilog='Example use: cost_per_use 75 15 15')
    parser.add_argument(
        'your_cost', help='int or float, amount paid')
    parser.add_argument(
        'used_price', help='int or float, amount you can sell it for')
    parser.add_argument('times_used',
                        help='int or float, number of times you\'ve used it')

    args = parser.parse_args()

    print(fi.cost_per_use(args.your_cost, args.used_price, args.times_used))


def run_fi_age():
    """
    Calculate the age at which you will reach FIRE. Credit: eseligsohn
    https://www.reddit.com/r/financialindependence/comments/92d35t/
    what_is_this_coast_number_people_are_talking_about/e36titl/
    """
    description = run_fi_age.__doc__
    parser = argparse.ArgumentParser(prog='fi_age',
                                     description=description,
                                     epilog='Example use: fi_age .07, 30000, 200000, 800000, 40')
    parser.add_argument(
        'eiar', help='expected inflation adjusted return e.g. .07')
    parser.add_argument(
        'awa', help='annual withdrawl amount, the amount of money you will withdraw each year')
    parser.add_argument(
        'stash', help='invested assests, the amount of money you have currently saved and invested for FI')
    parser.add_argument('fi_num', help='the number you need to reach FI')
    parser.add_argument('ca', help='your current age')

    args = parser.parse_args()

    print(fi.fi_age(float(args.eiar), float(args.awa), float(
        args.stash), float(args.fi_num), float(args.ca)))


def run_future_value():
    """
    Calculates the future value of money invested at an interest rate,
    x times per year, for a given number of years. Can also be used to
    calculate the future equivalent of money due to inflation.
    """
    description = run_future_value.__doc__
    parser = argparse.ArgumentParser(prog='future_value',
                                     description=description,
                                     epilog="Example use: future_value 800000 .03 1 20")
    parser.add_argument(
        'present_value',
        help='int or float, the current quantity of money, principal')
    parser.add_argument(
        'annual_rate',
        help='float 0 to 1 e.g., .5 = 50 percent, the interest rate paid out')
    parser.add_argument(
        'periods_per_year',
        help='int, the number of times money is invested per year')
    parser.add_argument('years', help='int, the number of years invested')
    args = parser.parse_args()
    print(fi.future_value(args.present_value, args.annual_rate,
                          args.periods_per_year, args.years))


def run_rule_of_72():
    """
    Calculate the time it will take for money to double
    based on a given interest rate:

    Years to double = 72 / Interest Rate
    """
    description = run_rule_of_72.__doc__
    parser = argparse.ArgumentParser(prog='rule_of_72',
                                     description=description,
                                     epilog="Example use: rule_of_72 8 -a")
    parser.add_argument(
        'interest_rate',
        help='Integer or floating point number representing the interest rate \
              at which your money will grow e.g. 7 for 7 percent')
    parser.add_argument(
        '-a',
        '--accurate',
        help='When set to True the more accurate 69.3 is used instead of 72',
        action='store_true')
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
    parser = argparse.ArgumentParser(prog='savings_rate',
                                     description=description,
                                     epilog="Example use: savings_rate 13839 8919")
    parser.add_argument(
        'take_home_pay', help='float or int, monthly take-home pay')
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
    parser = argparse.ArgumentParser(prog='spending_from_savings',
                                     description=description,
                                     epilog="example use: spending_from_savings 5000 2750")
    parser.add_argument(
        'take_home_pay', help='float or int, monthly take-home pay')
    parser.add_argument(
        'savings', help='float or int, amount of money saved')
    args = parser.parse_args()
    print(fi.spending_from_savings(args.take_home_pay, args.savings))


def run_take_home_pay():
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/
    """
    description = run_take_home_pay.__doc__
    parser = argparse.ArgumentParser(prog='rule_of_72',
                                     description=description,
                                     epilog="Example use: take_home_pay 1500 1000 '250 250'")
    parser.add_argument('gross_pay', help='float or int, gross monthly pay')
    parser.add_argument(
        'employer_match', help='float or int, the 401(k) match from your employer')
    parser.add_argument(
        'taxes_and_fees', help='list, taxes and fees that are deducted from your paycheck')
    args = parser.parse_args()
    taxes = [Decimal(item) for item in args.taxes_and_fees.split(' ')]
    print(fi.take_home_pay(args.gross_pay, args.employer_match, taxes))
