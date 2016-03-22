#!/usr/bin/env python3
import csv
import argparse
import datetime
import monthdelta

class data(list):

    fields = []

    def __init__(self, _list):
        super(data, self).__init__(_list)
        self['Date'] = datetime.datetime.strptime(self['Date'], '%d-%m-%Y').date()
        self['Amount'] = float(self['Amount'])

    @staticmethod
    def set_fields(fields):
        data.fields = fields

    def _get_key_index(self, key):
        return self.fields.index(key)

    def __getitem__(self, key):
        if isinstance(key, int):
            return super(data, self).__getitem__(key)
        else:
            if not self.fields:
                raise KeyError("%s not in fields list" % key)
            return self[self._get_key_index(key)]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            super(data, self).__setitem__(key, value)
        else:
            if not self.fields:
                raise KeyError("%s not in fields list" % key)
            self[self._get_key_index(key)] = value

    def is_expense(self):
        return self['Amount'] < 0

    def is_income(self):
        return self['Amount'] > 0



class expense(object):

    def __init__(self, fields=[], data=[]):
        self._fields = fields
        self._data = data

    def read(self, filename):
        with open(filename, 'r') as fp:
            f = fp.readline()
            d = fp.readlines()

        _data = [l.strip().split(',') for l in d]
        fields = f.strip().split(',')

        data.set_fields(fields)

        self._data.extend([data(d) for d in _data])
        self._fields = self._check_fields(fields)

    def _check_fields(self, fields):
        # check fields
        pass
        return fields

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self._data):
            raise StopIteration
        self.index+=1
        return self._data[self.index-1]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        s = ''
        for i in self:
            s += "%s\n" % str(i)
        return s

    def _get_key_index(self, key):
        return self._fields.index(key)

    def fields(self):
        return self._fields

    def data(self):
        return self._data

    def get(self, key, value):
        l = [ i for i in self if i[key] == value ]
        f = self.fields()
        return expense(f, l)

    def sort(self, key='Date', reverse=False, inplace=True):
        l = sorted(self, key= lambda x: x[key], reverse=reverse)
        f = self.fields()
        if inplace:
           self.__init__(f, l)
        else:
           return expense(f, l)

    def sum(self, key=None, value=None):
        if key and value:
            l = self.get(key, value)
        else:
            l = self._data
        return sum([ a['Amount'] for a in l ])

    def keys(self, key):
        l = set([i[key] for i in self ])
        l = sorted(l)
        return list(l)

    def accounts(self):
        return self.keys('Account')

    def categories(self):
        return self.keys('Category')

    def subcategories(self, category=None):
        if category:
            x = self.get_category(category)
        else:
            x = self
        return x.keys('Subcategory')


    def get_date(self, value):
        return self.get('Date', value)

    def get_amount(self, value):
        return self.get('Amount', value)

    def get_account(self, value):
        return self.get('Account', value)

    def get_category(self, value, exclude=None):
        return self.get('Category', value)

    def get_subcategory(self, value, category=None):
        if category:
            x = self.get_category(category)
        else:
            x = self
        return x.get('Subcategory', value)


    def get_expense(self):
        l = [i for i in self if i.is_expense()]
        f = self.fields()
        return expense(f, l)

    def get_income(self):
        l = [i for i in self if i.is_income()]
        f = self.fields()
        return expense(f, l)


    def get_range(self, key, _from, _to):
        l = [ i for i in self if i[key] >= _from and i[key] <= _to]
        l = sorted(l, key= lambda x: x[key])
        f = self.fields()
        return expense(f, l)

    def get_range_amount(self, from_amount, to_amount):
        return self.get_range('Amount', from_amount, to_amount)

    def get_range_date(self, from_day, to_day=datetime.datetime.today().isoformat()):
        _from = datetime.datetime.strptime(from_day, '%Y-%m-%d').date()
        _to = datetime.datetime.strptime(to_day, '%Y-%m-%d').date()
        return self.get_range('Date', _from, _to)

    def get_year(self, year):
        s = datetime.date(year, 1, 1)
        e = s + monthdelta.monthdelta(12) - datetime.timedelta(days=1)
        return self.get_range_date(s.isoformat(), e.isoformat())

    def get_month(self, year, month):
        s = datetime.date(year, month, 1)
        e = s + monthdelta.monthdelta(1) - datetime.timedelta(days=1)
        return self.get_range_date(s.isoformat(), e.isoformat())

    def get_day(self, year, month, day):
        s = datetime.date(year, month, day)
        e = datetime.date(year, month, day)
        return self.get_range_date(s.isoformat(), e.isoformat())


    def get_extreme(self, key, reverse=False):
        s = self.sort(key, reverse=reverse, inplace=False)
        return (s.data()[0][key], s.data()[-1][key])

    def get_extreme_date(self, reverse=False):
        return self.get_extreme('Date', reverse=reverse)

    def get_extreme_amount(self, reverse=False):
        return self.get_extreme('Amount', reverse=reverse)


def main():

    parser = argparse.ArgumentParser(prog='',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-f', '--files',
                        dest='csv_files',
                        nargs='+',
                        help='')


    args = parser.parse_args()

    #print(args)

    b = expense()

    #print(b)

    for f in args.csv_files:
        #print(f)
        b.read(f)

    print(b)

if __name__ == '__main__':
   main()

