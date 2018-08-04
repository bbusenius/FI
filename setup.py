# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='FI',
    description='A library of common functions used in financial ' +
                'independence (FI, FIRE) calculations.',
    version='0.0.1',
    author='Brad Busenius',
    author_email='bbusenius@gmail.com',
    packages=find_packages(),
    py_modules=[
        'fi',
    ],
    entry_points={
        'console_scripts': [
            'annual_cost = fi_commands:run_annual_cost',
            'coast_fi = fi_commands:run_coast_fi',
            'cost_per_use = fi_commands:run_cost_per_use',
            'fi_age = fi_commands:run_fi_age',
            'future_value = fi_commands:run_future_value',
            'rule_of_72 = fi_commands:run_rule_of_72',
            'take_home_pay = fi_commands:run_take_home_pay',
            'savings_rate = fi_commands:run_savings_rate',
            'spending_from_savings = fi_commands:run_spending_from_savings',
        ],
    },
    url='https://github.com/bbusenius/FI',
    license='MIT, see LICENSE.txt',
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    test_suite='tests',
    zip_safe=False
)
