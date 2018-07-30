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
            'coast_fi = fi_commands:run_coast_fi',
            'future_value = fi_commands:run_future_value',
            'rule_of_72 = fi_commands:run_rule_of_72',
            'take_home_pay = fi_commands:run_take_home_pay',
            'savings_rate = fi_commands:run_savings_rate',
            'spending_from_savings = fi_commands:run_spending_from_savings',
        ],
    },
    url='https://github.com/bbusenius/FI',
    license='MIT, see LICENSE.txt',
    test_suite='tests',
    zip_safe=False
)
