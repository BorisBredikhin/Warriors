class Averager:
    '''
    класс для быстрого подсчёта среднег значения
    '''

    def __init__(self):
        self._sum = 0.0
        self._count = 0

    def add(self, other):
        self._sum += other
        self._count += 1

    def __float__(self):
        return self._sum / self._count

    def __str__(self):
        return str(float(self))


sgn = lambda x: -1 if x < 0 else 1 if x > 0 else 0
