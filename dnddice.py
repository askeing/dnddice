#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import random

progname = 'dnddice'


def print_usage():
    print 'Usage:'
    print '\t!dnddice [dice_sides]'
    print '\t!dnddice [dice_number]d[dice_sides]'
    print '\t!dnddice [dice_number]d[dice_sides][modifier_with_sign]'
    print '\t!dnddice d[dice_sides]'
    print '\t!dnddice d[dice_sides][modifier_with_sign]'
    print 'ex: 1d20, 3d4, 2d6+10, 3d20-10, d6, d10-5'
    return


def to_int(s):
    """String to Integer Converter."""
    try:
        ret = int(s)
    except ValueError:
        print '{} is not an integer.'.format(s)
        sys.exit(1)
    return ret


def parser(s):
    dice_number = 1
    dice_sides = 6
    modifier = 0
    try:
        ret = re.match(r'^(?P<x>\d+)*(d*(?P<y>\d+))*(?P<z>[\+\-]\d+)*$', s, flags=re.IGNORECASE).groupdict()
    except:
        print 'Cannot parse {}.'.format(s)
        sys.exit(1)
    # x => dice_sides=x
    if ret['x'] is None and ret['y'] is None:
        print 'Cannot parse {}.'.format(s)
        sys.exit(1)
    elif ret['x'] is not None and ret['y'] is None:
        dice_sides = ret['x']
    # dy => dice_sides=y
    elif ret['x'] is None and ret['y'] is not None:
        dice_sides = ret['y']
    # xdy => dice_number=x, dice_sides=y
    elif ret['x'] is not None and ret['y'] is not None:
        dice_number = ret['x']
        dice_sides = ret['y']

    # xdy+-z => dice_number=x, dice_sides=y, modifier=z
    if ret['z'] is not None:
        modifier = ret['z']
    return (to_int(dice_sides), to_int(dice_number), to_int(modifier))


def dice(dice_sides, dice_number=1, modifier=0):
    if dice_sides <= 1:
        print 'The sides of dice should more than one.'
        sys.exit(1)
    if dice_number <= 0:
        print 'The number of dice should more than zero.'
        sys.exit(1)

    dice_result = [random.randint(1, dice_sides) for i in range(0, dice_number)]
    result = sum(dice_result) + modifier
    print '[{0:d}d{1:d}{2:+d}]'.format(dice_number, dice_sides, modifier), '+'.join('{}'.format(k) for k in dice_result), '{:+d}'.format(modifier), '= {:d}'.format(result)


def main(args):
    """The DnD Dice Roller Entry Point."""

    if len(args) <= 0:
        # Roll a 1d20 dice
        dice(20, 1, 0)
        return

    cmd = args[0]
    if cmd == 'help':
        print_usage()
    else:
        if len(args) == 1:
            dice_sides, dice_number, modifier = parser(args[0])
            dice(dice_sides, dice_number, modifier)
            return

if __name__ == '__main__':
    main(sys.argv[1:])
