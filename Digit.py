__author__ = 'anev'


class Digit:
    DIGITS = ['1110111',  # 0
              '0010010',  # 1
              '1011101',  # 2
              '1011011',  # 3
              '0111010',  # 4
              '1101011',  # 5
              '1101111',  # 6
              '1010010',  # 7
              '1111111',  # 8
              '1111011']  # 9

    DIGITS_BIN = map(lambda x: int(x, 2), DIGITS)

    def __init__(self, order=1):
        self.assumed = []  # history of assuming, list of lists
        self.history = []  # history of observations
        #
        self.order = order
        self.firstOrder = order == 1  # order of the digit
        self.broken = 0  # broken sections
        #
        self.current = int('-1', 2)  # current light sections
        self.working = int('0', 2)  # working sections
        self.changed = False  #


    def analyze(self, code):

        new = int(code, 2)
        self.changed = self.current != new
        self.current = new
        self.working = self.working | self.current

        starts = self.calculateStarts()
        self.analyzeBroken()
        self.history.append(new)
        return starts

    def stop(self):
        self.changed = self.order == 1
        self.current = 0
        step = len(self.assumed)

        self.analyzeBroken()

        if (self.changed and self.accordingToPrev(step % 10, step)):
            return [step % 10]
        elif (self.changed == False and self.accordingToPrev(step / 10, step)):
            return [step / 10]


    def accordingToPrev(self, assumedStart, step):
        return step == 0 or (assumedStart in self.assumed[-1])

    def calculateStarts(self):
        # we can do inheritance...
        if (self.firstOrder):
            return self.calculateStarts1()
        else:
            return self.calculateStarts2()

    def calculateStarts1(self):
        result = []
        step = len(self.assumed)

        for i, ethalon in enumerate(self.DIGITS_BIN):
            fitEthalon = (ethalon | self.current) == ethalon

            assumedStart = (i + step) % 10
            if (fitEthalon and self.accordingToPrev(assumedStart, step) and self.checkPrevObservations(assumedStart)):
                result.append(assumedStart)

        self.assumed.append(result)
        return result

    def checkPrevObservations(self, assumed):
        return len(self.history) == 0 or self.DIGITS_BIN[assumed] & self.working == self.history[0]

    def calculateStarts2(self):
        result = []
        step = len(self.assumed)
        if (self.changed == False):
            self.assumed.append(self.assumed[-1])
            return self.assumed[-1]

        for i, ethalon in enumerate(self.DIGITS_BIN):
            fitEthalon = (ethalon | self.current) == ethalon
            assumedStart = i + min(1, step)
            if (fitEthalon and self.accordingToPrev(assumedStart, step) and self.checkPrevObservations(assumedStart)):
                result.append(assumedStart)
        self.assumed.append(result)
        return result

    def analyzeBroken(self):
        # inheritance ?
        if (self.firstOrder):
            self.analyzeBroken1()
        else:
            self.analyzeBroken2()

    def analyzeBroken2(self):
        weKnowTheStart = len(self.assumed) > 0 and len(self.assumed[-1]) == 1
        if (weKnowTheStart == False):
            return

        stepsBack = len(self.assumed) - 1
        shouldLight = 0

        for i in range(0, min(stepsBack / 10, 9)):
            shouldLight = shouldLight | self.DIGITS_BIN[i]

        self.broken = shouldLight ^ self.working

    def analyzeBroken1(self):
        weKnowStart = len(self.assumed) > 0 and len(self.assumed[-1]) == 1
        if (weKnowStart == False):
            return

        stepsBack = len(self.assumed) - 1
        shouldLight = 0

        for i in range(0, min(stepsBack / self.order, 9)):
            shouldLight = shouldLight | self.DIGITS_BIN[i]

        self.broken = shouldLight ^ self.working


class Panel:
    def __init__(self):
        self.digit1 = Digit(order=2)
        self.digit2 = Digit(order=1)
        self.stopped = False
        self.starts = []


    def analyze(self, observation):

        if (self.stopped and observation['color'] == 'green'):
            return {'status': 'error', 'msg': 'The red observation should be the last'}

        if (observation['color'] == 'red'):
            self.stopped = True

            self.combine(self.digit1.stop(), self.digit2.stop())

            return {
                'status': 'ok',
                'response': {
                    'start': self.combination,
                    'missing': [format(self.digit1.broken, '#009b')[2:], format(self.digit2.broken, '#009b')[2:]]}
            }

        self.combine(
            self.digit1.analyze(observation['numbers'][0]),
            self.digit2.analyze(observation['numbers'][1]))

        if (len(self.combination) == 0):
            return {'status': 'error', 'msg': 'No solutions found'}

        return {
            'status': 'ok',
            'response': {
                'start': self.combination,
                'missing': [format(self.digit1.broken, '#009b')[2:], format(self.digit2.broken, '#009b')[2:]]}
        }


    def combine(self, poss1, poss2):
        result = []
        for a in poss1:
            for b in poss2:
                c = str(a) + str(b)
                result.append(int(c))
        self.combination = result
        return result
