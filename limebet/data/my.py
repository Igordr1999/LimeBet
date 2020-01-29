from limebet.data.picker import Picker
from multiprocessing import Process
import os


def doubler(number):
    """
    Функция умножитель на два
    """
    result = Picker().get_data(id=number)
    proc = os.getpid()
    print('{0} doubled to {1} by process id: {2}'.format(
        number, result, proc))


if __name__ == '__main__':
    procs = []
    numbers = [1, 2, 3, 4, 5, 6]

    for number in numbers:
        proc = Process(target=doubler, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
