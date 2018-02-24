# Copyright: Lustralisk
# Author: Cedric Liu
# Date: 2015-11-08

# Revision: MaxXing
# Date: 2018-01-19

import sys, time

class ProgressBar:
    def __init__(self, count=0, total=0, width=50, fill='#', empty=' '):
        self.__count = count
        self.total = total
        self.__width = width
        self.__fill = fill
        self.__empty = empty
        self.__percent = 0.0
    
    @property
    def percent(self):
        return self.__percent * 100

    def move(self, offset=1):
        self.__count += offset
        if self.__count < 0:
            self.__count = 0
        elif self.__count > self.total:
            self.__count = self.total
        return self
    
    def log(self, s=''):
        if s != '':
            sys.stdout.write(' ' * (self.__width + 9) + '\r')
            sys.stdout.flush()
            print(s)
        self.__percent = self.__count / self.total
        progress = int(self.__width * self.__percent)
        sys.stdout.write(' {0}/{1}: '.format(self.__count, self.total))
        sys.stdout.write(self.__fill * progress + \
                            self.__empty * (self.__width - progress) + \
                            ' ' + '%.1f' % (self.__percent * 100) + '%\r')
        if progress == self.__width:
            sys.stdout.write('\n')
        sys.stdout.flush()
        return self
