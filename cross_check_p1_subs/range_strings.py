'''
in_list contains an unsorted list of numbers
The consecutive ranges are displayed. Missing and duplicate numbers are listed.
e.g.
in_list = [25,7,9,8,6, 21,20, 3,2,1, 22,23, 50, 22, 22]
output:
duplicates: [22]
ranges: 50,25,23-20,9-6,3-1
missing: 49-26,24,19-10,5-4

Matthew Oppenheim
Last update: 2023_06_09
'''

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# examples used for testing
in_list = [25,7,9,8,6, 21,20, 3,2,1, 22,23, 50, 22, 22]
ranges = '50,25,23-20,9-6,3-1'

def consecutives(ranges):
    ''' Calculate consecutive ranges from tuple list. '''
    outstring = ''
    for (a, b) in ranges:
        if a == b:
            outstring += ('{}, '.format(a))
        else:
            outstring += ('{}-{}, '.format(a, b))
    return(outstring[:-2])


def find_duplicates(in_list):
    ''' Find repeated values. '''
    seen = set()
    seen_add = seen.add
    seen_twice = set(x for x in in_list if x in seen or seen_add(x))
    return list(seen_twice)


def find_missing(in_list):
    ''' Find missing values in a list of ints. '''
    if len(in_list) == 0:
        return []
    incrementing = is_inc(in_list)
    in_list.sort()
    non_missing = [x for x in range(in_list[0], in_list[-1]+1)]
    missing = list(set(in_list) ^ set(non_missing))
    if incrementing:
        missing = sorted(missing, reverse=False)
    else:
        missing = sorted(missing, reverse=True)
    return missing


def is_inc(in_list):
    ''' Detect if list is incrementing. '''
    if len(in_list) < 2:
        return True
    if in_list[-1] > in_list[0]:
        return True
    return False


def get_ranges(in_list):
    ''' Return ranges of values in in_list. '''
    if len(in_list) == 0:
        return []
    inc = is_inc(in_list)
    duplicates = find_duplicates(in_list)
    if duplicates:
        ('duplicates: {}'.format(duplicates))
    in_list = remove_multiples(in_list)
    ranges = range_tuples(in_list)
    ranges = consecutives(ranges)
    if not inc:
        ranges = reverse_ranges(ranges)
    return ranges


def range_tuples(in_list):
    ''' Create a list of tuples of ranges of consecutive numbers. '''
    if len(in_list) == 0:
        return []
    range_tuples = []
    # in_list = remove_multiples(in_list)
    first = last = None  # first and last number of current consecutive range
    for item in sorted(in_list):
        if first is None:
            first = last = item  # bootstrap
        elif item == last + 1:  # consecutive
            last = item  # extend the range
        else:  # not consecutive
            range_tuples.append((first, last))  # pack up the range
            first = last = item
    # the last range ended by iteration end
    range_tuples.append((first, last))
    logging.debug('range_tuples: {}'.format(range_tuples))
    return range_tuples


def remove_multiples(in_list):
    ''' Remove repeated values. '''
    output_list = set(in_list)
    return list(output_list)


def reverse_ranges(ranges):
    ''' Reverse a list of range tuples. '''
    reversed = []
    ranges = ranges.split(',')
    ranges = ranges[-1::-1]
    for single_range in ranges:
        single_range = single_range.strip()
        subrange = single_range.split('-')
        if len(subrange) > 1:
            subrange = subrange[-1::-1]
            single_range = '-'.join(subrange)
        reversed.append(single_range)
    return ', '.join(reversed)


if __name__ == '__main__':
    logging.info('ranges: {}'.format(get_ranges(in_list)))
    logging.info('missing: {}'.format(get_ranges(find_missing(in_list))))
    logging.info('reversed: {}'.format(reverse_ranges(ranges)))

