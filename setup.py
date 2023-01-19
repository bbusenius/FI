# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='FI',
    description='A library of common functions used in financial '
    + 'independence (FI, FIRE) calculations.',
    version='0.0.1',
    author='Brad Busenius',
    author_email='bbusenius@gmail.com',
    packages=find_packages(),
    py_modules=['fi'],
    entry_points={
        'console_scripts': [
            'annual_cost = fi_commands:run_annual_cost',
            'average_daily_spend = fi_commands:run_average_daily_spend',
            'buy_a_day_of_freedom = fi_commands:run_buy_a_day_of_freedom',
            'coast_fi = fi_commands:run_coast_fi',
            'cost_per_use = fi_commands:run_cost_per_use',
            'days_covered_by_fi = fi_commands:run_days_covered_by_fi',
            'fi_age = fi_commands:run_fi_age',
            'future_value = fi_commands:run_future_value',
            'percent_increase = fi_commands:run_percent_increase',
            'redeem_chase_points = fi_commands:run_redeem_chase_points',
            'redeem_points = fi_commands:run_redeem_points',
            'rule_of_72 = fi_commands:run_rule_of_72',
            'take_home_pay = fi_commands:run_take_home_pay',
            'savings_rate = fi_commands:run_savings_rate',
            'spending_from_savings = fi_commands:run_spending_from_savings',
        ]
    },
    url='https://github.com/bbusenius/FI',
    license='MIT, see LICENSE.txt',
    include_package_data=True,
    install_requires=['numpy', 'numpy_financial'],
    test_suite='tests',
    zip_safe=False,
)
