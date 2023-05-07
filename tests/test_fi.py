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

    def test_cost_per_use(self):
        # Example from Early Retirement Extreme
        args = (75, 15, 15)
        val1 = fi.cost_per_use(*args)

        self.assertEqual(val1, Decimal(4), 'Should return 4, returned ' + str(val1))
        self.assertEqual(
            val1, fi.annual_cost(*args), 'Should return the same as annual_cost'
        )

    def test_fi_age(self):
        current_age = 20
        years_to_double = fi.rule_of_72(8)
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
        val1 = fi.future_value(2, 50, 1, 1)
        val2 = fi.future_value(2, 50, 1, 2)
        self.assertEqual(val1, 3, 'The value should be 3, returned ' + str(val1))
        self.assertEqual(val2, 4.5, 'The value should be 4.5, returned')

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

    def test_real_hourly_wage(self):
        val1 = fi.real_hourly_wage(40, 1000, 0, 30, 300)
        self.assertEqual(val1, 10)

    def test_rule_of_72(self):
        # Less accurate, examples 2-4 from:
        # http://investinganswers.com/financial-dictionary/technical-analysis/rule-72-1615
        val1 = fi.rule_of_72(8)
        val2 = fi.rule_of_72(4)
        val3 = fi.rule_of_72(2)
        val4 = fi.rule_of_72(3)
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


# Run all tests
if __name__ == '__main__':
    unittest.main()
