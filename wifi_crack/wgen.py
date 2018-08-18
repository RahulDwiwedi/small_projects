import os
import sys
import time
import string
import argparse
import itertools


def createWordList(chrs, min_length, max_length, output):
    """
    :param `chrs` is characters to iterate.
    :param `min_length` is minimum length of characters.
    :param `max_length` is maximum length of characters.
    :param `output` is output of wordlist file.
    """
    if min_length > max_length:
        print ("[!] Please `min_length` must smaller or same as with `max_length`")
        sys.exit()

    # if os.path.exists(os.path.dirname(output)) == False:
    #     os.makedirs(os.path.dirname(output))

    print ('[+] Creating wordlist at `%s`...' % output)
    print ('[i] Starting time: %s' % time.strftime('%H:%M:%S'))

    output = open(output, 'w+')

    for n in range(min_length, max_length + 1):
        for xs in itertools.product(chrs, repeat=n):
            chars = ''.join(xs)
            output.write("%s\n" % chars)
            sys.stdout.write('\r[+] saving character `%s`' % chars)
            sys.stdout.flush()
    output.close()

    print ('\n[i] End time: %s' % time.strftime('%H:%M:%S'))


a=string.digits
createWordList(a,min_length=4,max_length=4,output='output')

