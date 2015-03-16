import unittest
from Digit import Digit, Panel

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)


class TestDigit(unittest.TestCase):
    def test_1(self):
        d = Digit()

        poss = d.analyze('1101001')
        self.assertEquals(4, len(poss))
        poss = d.analyze('1101101')
        self.assertEquals(1, len(poss))


    def test_2(self):
        d = Digit()

        starts = d.analyze('0011011')
        self.assertEquals(3, len(starts))

        starts = d.analyze('0011111')
        self.assertEquals(1, len(starts))
        self.assertEquals(9, starts[0])

        starts = d.analyze('0010010')
        self.assertEquals(1, len(starts))
        self.assertEquals(9, starts[0])

    def test_3(self):
        d = Digit(2)

        poss = d.analyze('0011101')
        self.assertEqual([2, 8], poss)

        poss = d.analyze('0011101')
        self.assertEqual([2, 8], poss)

        poss = d.analyze('0010010')
        self.assertEqual([2], poss)


    def test_panel_1(self):
        panel = Panel()

        obs1 = {'color': 'green', 'numbers': ['0010111', '0011011']}
        starts = panel.analyze(obs1)
        self.assertIn(9, starts['response']['start'])

        obs1 = {'color': 'green', 'numbers': ['0010111', '0011111']}
        starts = panel.analyze(obs1)
        self.assertIn(9, starts['response']['start'])


    def test_panel_combination(self):
        panel = Panel()

        self.assertEqual(
            [21, 22],
            panel.combine([2], [1, 2]))

        self.assertEqual(
            [8, 9, 98, 99],
            panel.combine([0, 9], [8, 9]))

    def test_missed(self):
        digit1 = Digit(1)
        digit1.analyze('0010000')
        self.assertEquals([1], digit1.stop())

        self.assertEquals(2, digit1.broken)