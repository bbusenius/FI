"""
Unit testing for library functions.
Every method should start with "test".
"""

import unittest
from decimal import Decimal
from math import isnan

import fi

TWOPLACES = Decimal('0.01')


class test_fi(unittest.TestCase):
    def test_annual_cost(self):
        # Examples from Early Retirement Extreme
        val1 = fi.annual_cost(75, 70, 2.5)
        val2 = fi.annual_cost(300, 100, 3)

        self.assertEqual(val1, Decimal(2), 'Should return 2, returned ' + str(val1))
        self.assertEqual(
            round(val2.quantize(TWOPLACES)),
            Decimal(67),
            'Should return 67, returned ' + str(val2),
        )

    def test_coast_fi(self):
        val1 = fi.coast_fi(2000000, 7, 62, 31)
        val2 = fi.coast_fi(2000000, 0, 62, 31)

        # https://www.reddit.com/r/financialindependence/comments/92d35t/what_is_this_coast_number_people_are_talking_about/e34uuxh/
        self.assertEqual(
            int(val1), 245546, 'Should return the value from reddit thread'
        )
        self.assertEqual(
            val2, 2000000, 'Should return the target FI number if interest is 0'
        )

    def test_cost_of_costs(self):
        val1 = fi.cost_of_costs(100, 0, 0, 10)
        val2 = fi.cost_of_costs(2, 50, 50, 1)
        self.assertEqual(val1, Decimal(0))
        self.assertEqual(val2, Decimal(1))
        # Page 47 of "The Little Book of Common Sense Investing"
        # Stretching out the timeline longer than this doesn't match
        # Bogle's examples. I'm pretty sure this is because he's
        # rounding (a lot by the looks of it).
        val2 = fi.cost_of_costs(10000, 7, 2, 1)
        self.assertAlmostEqual(val2, Decimal(200))

    def test_cost_per_use(self):
        # Example from Early Retirement Extreme
        args = (75, 15, 15)
        val1 = fi.cost_per_use(*args)

        self.assertEqual(val1, Decimal(4), 'Should return 4, returned ' + str(val1))
        self.assertEqual(
            val1, fi.annual_cost(*args), 'Should return the same as annual_cost'
        )

    def test_expected_gross_return(self):
        # Pages 102-105 of "The Little Book of Common Sense Investing"
        val1 = fi.expected_gross_return(4, 3.1, 60, 40)
        self.assertAlmostEqual(val1, 3.6, 1)

    def test_fi_age(self):
        current_age = 20
        years_to_double = fi.rule_of_72(8, False)
        interest = 8
        val1 = fi.fi_age(interest, 0, 400000, 800000, current_age)

        self.assertEqual(
            val1,
            current_age + years_to_double,
            'Without making payments, the money should double in 9 years',
        )

    def test_fi_number(self):
        val1 = fi.fi_number(40000, 4)
        self.assertEqual(val1, 1000000)

        # https://radicalfire.com/your-fi-number/
        val2 = fi.fi_number(12000, 4)
        val3 = fi.fi_number(12000, 3.5)
        val4 = fi.fi_number(24000, 4)
        self.assertEqual(val2, 300000)
        self.assertAlmostEqual(val3, 342857, 0)
        self.assertEqual(val4, 600000)

    def test_future_value(self):
        # Test without drawdown
        val1 = fi.future_value(2, 50, 1, 1)
        val2 = fi.future_value(2, 50, 1, 2)
        self.assertEqual(val1, 3, 'The value should be 3, returned ' + str(val1))
        self.assertEqual(val2, 4.5, 'The value should be 4.5, returned')

        # Test with drawdown parameter explicitly set to 0 (should match above)
        val3 = fi.future_value(2, 50, 1, 1, 0)
        val4 = fi.future_value(2, 50, 1, 2, 0)
        self.assertEqual(val3, val1, 'Explicit drawdown=0 should match default')
        self.assertEqual(val4, val2, 'Explicit drawdown=0 should match default')

        # Test with actual drawdown
        val5 = fi.future_value(100000, 7, 1, 5, 10000)
        self.assertAlmostEqual(
            float(val5),
            82747.78,
            places=2,
            msg='Drawdown calculation should be approximately correct',
        )

        # Test portfolio depletion
        val6 = fi.future_value(50000, 5, 1, 10, 20000)
        self.assertEqual(
            val6, 0, 'Portfolio should be depleted with excessive drawdown'
        )

        # Test edge case: drawdown equals growth
        val7 = fi.future_value(100000, 10, 1, 3, 11000)
        self.assertGreater(
            val7, 0, 'Portfolio should have positive value with balanced drawdown'
        )

    def test_get_percentage(self):
        val1 = fi.get_percentage(25, 100)
        val2 = round(fi.get_percentage(159.5078, 28523.34), 4)
        val3 = round(fi.get_percentage(34.292, 62.1), 2)
        val4 = fi.get_percentage(34.292, 62.1, False, True)
        # val5 = fi.get_percentage(34.292, 62.1, True, False)
        assert val1 == 25, "The value should be 25, returned " + str(val1)
        assert val2 == 0.5592, "The value should be 0.5592, returned " + str(val2)
        assert val3 == 55.22, "The value should be 55.22, returned " + str(val3)
        assert val4 == 55.22, "The value should be 55.22, returned " + str(val4)
        # assert val5 == 55, "The value should be 55, returned " + str(val5)

    def test_hours_of_life_energy(self):
        val1 = fi.hours_of_life_energy(80, 10)
        val2 = fi.hours_of_life_energy(20, 10)
        val3 = fi.hours_of_life_energy(0, 0)
        self.assertEqual(val1, 8)
        self.assertEqual(val2 * 60, 120)
        self.assertEqual(val3, 0)

    def test_likely_real_return(self):
        # Pages 105-106 of "The Little Book of Common Sense Investing"
        val1 = fi.likely_real_return(3.6, 1.5, 2)
        self.assertAlmostEqual(val1, 0.1, 15)

    def test_monthly_investment_income(self):
        # From "Your Money or Your Life", Chapter 8
        val1 = fi.monthly_investment_income(100, 4)
        val2 = fi.monthly_investment_income(1000, 4)
        val3 = fi.monthly_investment_income(1500, 4)
        val4 = fi.monthly_investment_income(900000, 4)
        val5 = fi.monthly_investment_income(500000, 0)
        val6 = fi.monthly_investment_income(1000000, 4)
        self.assertAlmostEqual(val1, Decimal(0.333), 3)
        self.assertAlmostEqual(val2, Decimal(3.33), 2)
        self.assertEqual(val3, Decimal(5.00))
        self.assertEqual(val4, Decimal(3000))
        self.assertEqual(val5, Decimal(0))
        self.assertEqual(val6 * 12, Decimal(40000))

    def test_monthly_payment(self):
        # 30-year mortgage at 6%, $200k principal
        # Known value: ~$1,199.10/month
        val1 = fi.monthly_payment(200000, 6, 30)
        self.assertAlmostEqual(val1, Decimal('1199.10'), 0)

        # 15-year mortgage at 4%, $150k principal
        # Known value: ~$1,109.53/month
        val2 = fi.monthly_payment(150000, 4, 15)
        self.assertAlmostEqual(val2, Decimal('1109.53'), 0)

        # 0% interest edge case - should be simple division
        val3 = fi.monthly_payment(12000, 0, 5)
        self.assertEqual(val3, Decimal('200.00'))  # 12000 / 60 months

    def test_total_interest(self):
        # Same 30-year mortgage at 6%: should pay ~$231,676 in interest
        val1 = fi.total_interest(200000, 6, 30)
        self.assertAlmostEqual(val1, Decimal('231676'), -3)

        # 15-year mortgage at 4%: should pay ~$49,716 in interest
        val2 = fi.total_interest(150000, 4, 15)
        self.assertAlmostEqual(val2, Decimal('49716'), -3)

        # 0% interest - should be exactly 0
        val3 = fi.total_interest(12000, 0, 5)
        self.assertEqual(val3, Decimal('0.00'))

    def test_net_operating_income(self):
        # Example: $30,000 rental income minus $12,000, $2,000, $1,500 in expenses
        val1 = fi.net_operating_income(30000, [12000, 2000, 1500])
        # Example: $24,000 rental income minus $8,000, $1,200 in expenses
        val2 = fi.net_operating_income(24000, [8000, 1200])
        # Example: No expenses
        val3 = fi.net_operating_income(30000, [])
        # Example: Expenses equal income (break even)
        val4 = fi.net_operating_income(20000, [20000])
        self.assertEqual(val1, 14500)
        self.assertEqual(val2, 14800)
        self.assertEqual(val3, 30000)
        self.assertEqual(val4, 0)

    def test_opportunity_cost(self):
        # From "The Simple Path to Wealth: Your road map to financial independence and a rich, free life"
        val1 = fi.opportunity_cost(20000)
        val2 = fi.opportunity_cost(0)
        self.assertAlmostEqual(val1, Decimal(1600), 10)
        self.assertEqual(val2, Decimal(0))

    def test_percent_decrease(self):
        val1 = fi.percent_decrease(10, 5)
        val2 = fi.percent_decrease(10, 8)
        self.assertEqual(val1, 50, 'This should be a 50% decrease')
        self.assertEqual(val2, 20, 'This should be a 20% decrease')

        # Example from:
        # https://www.omnicalculator.com/math/percentage-increase#how-to-calculate-percent-increase
        val3 = fi.percent_decrease(1445, 1300)
        self.assertAlmostEqual(val3, 10, 1, 'This should be close to a 10% decrease')

        val4 = fi.percent_decrease(-5, -10)
        val5 = fi.percent_decrease(10, 0)
        val6 = fi.percent_decrease(2, 2)
        val7 = fi.percent_decrease(5, -5)
        val8 = fi.percent_decrease(0, -5)
        self.assertEqual(val4, 100, 'This should be a 100% decrease')
        self.assertEqual(val5, 100, 'This should be a 100% decrease')
        self.assertEqual(val6, 0, 'This should be a 0% decrease')
        self.assertEqual(val7, 200, 'This should be a 200% decrease')
        self.assertTrue(isnan(val8), 'This should be a NaN')

    def test_percent_increase(self):
        val1 = fi.percent_increase(5, 10)
        val2 = fi.percent_increase(10, 12)
        self.assertEqual(val1, 100, 'This should be a 100% increase')
        self.assertEqual(val2, 20, 'This should be a 20% increase')

        # Example from:
        # https://www.omnicalculator.com/math/percentage-increase#how-to-calculate-percent-increase
        val3 = fi.percent_increase(1250, 1445)
        self.assertEqual(val3, 15.6, 'This should be a 15.6% increase')

        val4 = fi.percent_increase(-10, 10)
        val5 = fi.percent_increase(0, 10)
        self.assertEqual(val4, 200, 'This should be a 200% increase')
        self.assertTrue(isnan(val5), 'This should be NaN')

    def test_percent_return_for_percent(self):
        val1 = fi.percent_return_for_percent(100, 50)
        val2 = fi.percent_return_for_percent(100, 25)
        val3 = fi.percent_return_for_percent(0, 35)
        val4 = fi.percent_return_for_percent(0, 0)
        self.assertEqual(val1, Decimal(50))
        self.assertEqual(val2, Decimal(25))
        self.assertEqual(val3, Decimal(0))
        self.assertEqual(val4, Decimal(0))

    def test_pot_score(self):
        val1 = fi.pot_score(27000, 11, 42600)
        val2 = fi.pot_score(72330, 11, 42600)
        self.assertAlmostEqual(val1, Decimal(0.1), 1)
        self.assertAlmostEqual(val2, Decimal(1.2), 1)

    def test_price_to_rent(self):
        # Example: $300,000 home, $18,000/year rent = ratio of 16.67 (gray area)
        val1 = fi.price_to_rent(300000, 18000)
        # Example: $450,000 home, $30,000/year rent = ratio of 15 (favors buying)
        val2 = fi.price_to_rent(450000, 30000)
        # Example: $500,000 home, $20,000/year rent = ratio of 25 (favors renting)
        val3 = fi.price_to_rent(500000, 20000)
        self.assertAlmostEqual(val1, Decimal(16.67), 2)
        self.assertEqual(val2, 15)
        self.assertEqual(val3, 25)

    def test_real_hourly_wage(self):
        val1 = fi.real_hourly_wage(40, 1000, 0, 30, 300)
        self.assertEqual(val1, 10)

    def test_remaining_life_expectancy(self):
        # From Figure 2-1 in Chapter 2 of "Your Money or Your Life"
        # by Vicki Robin and Joe Dominguez
        val1 = fi.remaining_life_expectancy(45, time_unit='years')
        val2 = fi.remaining_life_expectancy(40, time_unit='years')
        val3 = fi.remaining_life_expectancy(60, time_unit='years')
        val4 = fi.remaining_life_expectancy(45, time_unit='hours', more_accurate=False)
        val5 = fi.remaining_life_expectancy(65, time_unit='hours', more_accurate=False)
        val6 = fi.remaining_life_expectancy(40, time_unit='hours', more_accurate=False)
        val7 = fi.remaining_life_expectancy(
            40, time_unit='hours', more_accurate=False, exclude_time_asleep=True
        )
        self.assertAlmostEqual(val1, Decimal(36.1), 1)
        self.assertAlmostEqual(val2, Decimal(40.7), 1)
        # The book says 23.3 but this is wrong, the table has 23.2.
        self.assertAlmostEqual(val3, Decimal(23.2), 1)
        self.assertAlmostEqual(val4, Decimal(316236), 0)
        self.assertAlmostEqual(val5, Decimal(169068), 0)
        self.assertAlmostEqual(val6, Decimal(356532), 0)
        # The book says "about half your time" and gives 178,000 hours of life energy.
        # It is not using a precise number.
        self.assertAlmostEqual(val7, Decimal(178266), 0)

    def test_rule_of_72(self):
        # Less accurate, examples 2-4 from:
        # http://investinganswers.com/financial-dictionary/technical-analysis/rule-72-1615
        val1 = fi.rule_of_72(8, False)
        val2 = fi.rule_of_72(4, False)
        val3 = fi.rule_of_72(2, False)
        val4 = fi.rule_of_72(3, False)
        self.assertEqual(val1, 9, 'The money should double in 9 years')
        self.assertEqual(val2, 18, 'The money should double in 18 years')
        self.assertEqual(val3, 36, 'The money should double in 36 years')
        self.assertEqual(val4, 24, 'The money should double in 24 years')

        # More accurate (69.3). Examples from:
        # https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/rule-of-72-double-investment/
        val5 = fi.rule_of_72(2, True)
        val6 = fi.rule_of_72(10, True)
        val7 = fi.rule_of_72(5, True)
        val8 = fi.rule_of_72(30, True)
        self.assertEqual(val5, 34.65, 'The money should double in 34.65 years')
        self.assertEqual(val6, 6.93, 'The money should double in 6.93 years')
        self.assertEqual(val7, 13.86, 'The money should double in 13.86 years')
        self.assertEqual(val8, 2.31, 'The money should double in 2.31 years')

        # Zero division
        val9 = fi.rule_of_72(0)
        val10 = fi.rule_of_72(0, True)
        self.assertEqual(val9, float('inf'), 'The money will never double')
        self.assertEqual(val10, float('inf'), 'The money will never double')

    def test_savings_rate(self):
        val1 = fi.savings_rate(13839.0, 8919.0)
        val2 = fi.savings_rate(600, 300)
        self.assertEqual(
            val1.quantize(TWOPLACES),
            Decimal(35.55).quantize(TWOPLACES),
            'The savings rate should be approximately 35.55%, returned ' + str(val1),
        )
        self.assertEqual(
            val2, 50, "The savings rate should be 50%, returned " + str(val2)
        )

    def test_spending_from_savings(self):
        val1 = fi.spending_from_savings(100, 50)
        val2 = fi.spending_from_savings(100, 0)
        val3 = fi.spending_from_savings(100, 100)
        self.assertEqual(val1, 50, 'Spending should be 50, returned ' + str(val1))
        self.assertEqual(val2, 100, 'Spending should be 100, returned ' + str(val2))
        self.assertEqual(val3, 0, 'Spending should be 0, returned ' + str(val3))

    # Test take_home_pay
    # http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/
    # (There are rounding differences)
    # Gross Pay + Employer 401(k) match - taxes and fees
    # = $8620 gross pay + $300 employer 401(k) match
    # - $1724 federal tax
    # - $689 state tax
    # - $200 professional fees
    # = $6407 biweekly or $13,839 per month
    def test_take_home_pay(self):
        # There are 2.16 pay periods in a month
        val1 = fi.take_home_pay(8620, 300, [1724, 689, 200]) * Decimal(2.16)
        val1 = val1.quantize(TWOPLACES)
        self.assertEqual(
            val1,
            Decimal(13623.12).quantize(TWOPLACES),
            'Take-home pay should be $13,623.12 per month, returned ' + str(val1),
        )

    def test_redeem_points(self):
        points = 50000
        val1 = fi.redeem_points(points)
        val2 = fi.redeem_points(points, 1.25)
        val3 = fi.redeem_points(points, 1.5)
        self.assertEqual(val1, Decimal(500))
        self.assertEqual(val2, Decimal(625))
        self.assertEqual(val3, Decimal(750))

    def test_redeem_chase_points(self):
        points = 50000
        cp = fi.redeem_chase_points(points)
        val1 = cp['Cash value']
        val2 = cp['Sapphire Preferred portal']
        val3 = cp['Sapphire Reserve portal']
        val4 = cp['Target partner exchange']
        self.assertEqual(val1, Decimal(500))
        self.assertEqual(val2, Decimal(625))
        self.assertEqual(val3, Decimal(750))
        self.assertEqual(val4, Decimal(1000))

    def test_stock_returns(self):
        # From page 97-99 of "The Little Book of Common Sense Investing"
        val1 = fi.stock_returns(2, 4, -2)
        val2 = fi.stock_returns(2, 4, 1.5)
        self.assertEqual(val1, Decimal(4))
        self.assertEqual(val2, Decimal(7.5))

    def test_turnover_costs(self):
        # From page 55 of "The Little Book of Common Sense Investing"
        val1 = fi.turnover_costs(50)
        val2 = fi.turnover_costs(10)
        self.assertAlmostEqual(val1, Decimal(0.5), 15)
        self.assertAlmostEqual(val2, Decimal(0.1), 15)

    def test_average_daily_spend(self):
        val1 = fi.average_daily_spend(100, 10)
        val2 = fi.average_daily_spend(2100, 30)
        val3 = fi.average_daily_spend(1000000, 25)
        self.assertEqual(val1, 10)
        self.assertEqual(val2, 70)
        self.assertEqual(val3, 40000)

    def test_days_covered_by_fi(self):
        val1 = fi.days_covered_by_fi(40000, 500000)
        val2 = fi.days_covered_by_fi(30000, 750000)
        val3 = fi.days_covered_by_fi(40000, 500000, 3)
        val4 = fi.days_covered_by_fi(40000, 500000, 5)
        val5 = fi.days_covered_by_fi(40000, 0)
        val6 = fi.days_covered_by_fi(40000, 500000, 2)
        self.assertEqual(val1, 182.5)
        self.assertEqual(val2, 365)
        self.assertLess(val3, val1)
        self.assertGreater(val4, val1)
        self.assertEqual(val5, 0)
        self.assertEqual(val6, 91.25)

    # Test buy_a_day_of_freedom
    # Examples from https://www.reddit.com/r/leanfire/comments/caka4t/
    # weekly_leanfire_discussion_july_08_2019/etfdwg1/
    def test_buy_a_day_of_freedom(self):
        annual_rent = 2100 * 12
        rent_per_day = Decimal(annual_rent / 365)
        val1 = fi.buy_a_day_of_freedom(25200, 4)
        val2 = fi.buy_a_day_of_freedom(12000, 4)
        val3 = fi.buy_a_day_of_freedom(27375, 4)
        val4 = fi.buy_a_day_of_freedom(36500)
        self.assertAlmostEqual(
            val1,
            Decimal(rent_per_day / Decimal(0.04)),
            5,
        )
        self.assertAlmostEqual(val2, Decimal((12000 / 365) / 0.04), 5)
        self.assertAlmostEqual(val3, Decimal((27375 / 365) / 0.04), 5)
        self.assertEqual(val4, Decimal(2500))

    def test_cap_rate(self):
        # Example: $300,000 property with $18,000 NOI = 6% cap rate
        val1 = fi.cap_rate(18000, 300000)
        # Example: $500,000 property with $40,000 NOI = 8% cap rate
        val2 = fi.cap_rate(40000, 500000)
        # Example: $200,000 property with $10,000 NOI = 5% cap rate
        val3 = fi.cap_rate(10000, 200000)
        # Zero division test
        val4 = fi.cap_rate(10000, 0)
        self.assertEqual(val1, 6)
        self.assertEqual(val2, 8)
        self.assertEqual(val3, 5)
        self.assertEqual(val4, 0)


# Run all tests
if __name__ == '__main__':
    unittest.main()
