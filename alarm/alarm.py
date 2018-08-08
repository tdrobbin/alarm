import datetime
import random
from time import sleep
import os
import re
import multiprocessing
import fire


def solve_arithmetic_problem():
    x, y = random.randint(10, 100), random.randint(10, 100)
    solution = x + y

    while 1:
        try:
            attempt = int(input('solve {} + {}: '.format(x, y)))
        except ValueError:
            # typo in inupt
            print('solution not accepted')
            print('\n')
            continue

        if attempt == solution:
            print('solution accepted')
            print('\n')
            break

        print('solution not accepted')
        print('\n')


def alarm_loop(phrase='chelate', beep=True):
    while 1:
        os.system('say "{}"'.format(phrase))
        sleep(1)


def main(*args):
    args = [str(a) + ':00' if re.search(':', str(a)) is None else str(a) for a in args]
    start = datetime.datetime.now()
    times = [datetime.datetime(start.year, start.month, start.day, int(a.split(':')[0]), int(a.split(':')[1])) for a in args]
    # print(times)
    # import pdb; pdb.set_trace()
    alarms = [datetime.datetime(t.year, t.month, t.day, t.hour, t.minute) + datetime.timedelta(days=1) if t < start else t for t in times]
    alarms_passed = []
    alarms_remaining = [a for a in alarms]

    print('following alarms are set:')
    for a in alarms:
        print('    ' + str(a))
    print('\n')

    while 1:
        try:
            if [a for a in alarms_remaining if a < datetime.datetime.now()]:
                sound_alarm = multiprocessing.Process(target=alarm_loop)
                sound_alarm.start()

                solve_arithmetic_problem()

                sound_alarm.terminate()

                # add any alarms that may have passed while we were solving the arithmetic for this alarm
                alarms_passed = [a for a in alarms if a < datetime.datetime.now()]
                alarms_remaining = [a for a in alarms if a not in alarms_passed]

                if len(alarms_passed) == len(alarms):
                    return 'ALL ALARMS PASSED'

                print('following alarms are set:')
                for a in alarms_remaining:
                    print('    ' + str(a))
                print('\n')

            sleep(1)

        except KeyboardInterrupt:
            return 'INTERRUPED'

        finally:
            try:
                # in case we left the process running
                sound_alarm.terminate()
            except NameError:
                pass


if __name__ == '__main__':
    fire.Fire(main)
