#!/usr/bin/env python3
import argparse
from expense import expense

import operator
from collections import OrderedDict

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

    for f in args.csv_files:
        b.read(f)


    # get totals

    d_tot = OrderedDict()

    d_tot['expense'] = b.get_expense().sum()
    d_tot['income'] = b.get_income().sum()
    d_tot['balance'] = d_tot['expense'] + d_tot['income']

    for k, v in d_tot.items():
        print("{:10.2f}  {}".format(v, k))


    e = b.get_expense()
    i = b.get_income()


    # get list of category in expensive order
    print("Expensive category:")

    # dict with category : amount
    d = {x: e.get_category(x).sum() for x in e.categories()}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1)))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['expense'], k))


    print("Expensive account:")

    # dict with account : amount
    d = {x: e.get_account(x).sum() for x in e.accounts()}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1)))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['expense'], k))


    print("Incoming account:")

    # dict with account : amount
    d = {x: i.get_account(x).sum() for x in i.accounts()}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['income'], k))


    print("Balance account:")

    # dict with account : amount
    d = {x: b.get_account(x).sum() for x in b.accounts()}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['balance'], k))


    print("Incoming category:")

    # dict with category : amount
    d = {x: i.get_category(x).sum() for x in i.categories()}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['income'], k))

    # dict with category : amount
    d = {x: i.get_subcategory(x, 'Income').sum() for x in i.subcategories('Income')}
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

    for k, v in d.items():
        print("{:10.2f}  {:4.1f}%  {}".format(v, 100.0*v/d_tot['income'], k))


if __name__ == '__main__':
   main()

