# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    long_description_type = 'text/markdown'

try:
    import pypandoc

    long_description = pypandoc.convert_text(long_description, 'rst', format='md')
    long_description = long_description.replace('\r', '')
    long_description_type = 'text/x-rst'
except (ImportError, OSError):
    pass

setup(
    name='FI',
    description='A library of common functions and command line utility used '
    + 'to make financial independence calculations.',
    long_description=long_description,
    long_description_content_type=long_description_type,
    python_requires='>=3.10',
    version='0.0.1',
    author='Brad Busenius',
    author_email='bbusenius@gmail.com',
    packages=find_packages(),
    py_modules=['fi', 'fi_commands'],
    entry_points={
        'console_scripts': [
            'annual_cost = fi_commands:run_annual_cost',
            'average_daily_spend = fi_commands:run_average_daily_spend',
            'buy_a_day_of_freedom = fi_commands:run_buy_a_day_of_freedom',
            'coast_fi = fi_commands:run_coast_fi',
            'cost_of_costs = fi_commands:run_cost_of_costs',
            'cost_per_use = fi_commands:run_cost_per_use',
            'days_covered_by_fi = fi_commands:run_days_covered_by_fi',
            'expected_gross_return = fi_commands:run_expected_gross_return',
            'FI = fi_commands:run_fi',
            'fi_age = fi_commands:run_fi_age',
            'fi_number = fi_commands:run_fi_number',
            'future_value = fi_commands:run_future_value',
            'get_percentage = fi_commands:run_get_percentage',
            'hours_of_life_energy = fi_commands:run_hours_of_life_energy',
            'likely_real_return = fi_commands:run_likely_real_return',
            'monthly_investment_income = fi_commands:run_monthly_investment_income',
            'opportunity_cost = fi_commands:run_opportunity_cost',
            'percent_decrease = fi_commands:run_percent_decrease',
            'percent_increase = fi_commands:run_percent_increase',
            'percent_return_for_percent = fi_commands:run_percent_return_for_percent',
            'pot_score = fi_commands:run_pot_score',
            'real_hourly_wage = fi_commands:run_real_hourly_wage',
            'redeem_chase_points = fi_commands:run_redeem_chase_points',
            'redeem_points = fi_commands:run_redeem_points',
            'remaining_life_expectancy = fi_commands:run_remaining_life_expectancy',
            'rule_of_72 = fi_commands:run_rule_of_72',
            'stock_returns = fi_commands:run_stock_returns',
            'take_home_pay = fi_commands:run_take_home_pay',
            'savings_rate = fi_commands:run_savings_rate',
            'spending_from_savings = fi_commands:run_spending_from_savings',
            'turnover_costs = fi_commands:run_turnover_costs',
        ]
    },
    url='https://github.com/bbusenius/FI',
    license='MIT, see LICENSE.txt',
    include_package_data=True,
    install_requires=['numpy', 'numpy_financial', 'openpyxl', 'pandas'],
    test_suite='tests',
    zip_safe=False,
)
