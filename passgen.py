from random import choice
import argparse
import re
from typing import Optional


parser = argparse.ArgumentParser()

parser.add_argument('length', type=int, help='Number of characters')
parser.add_argument('-l', '--letters', action='store_true', help='Exclude letters (aA)')
parser.add_argument('-d', '--digits', action='store_true', help='Exclude numbers (0-9)')
parser.add_argument('-s', '--symbols', action='store_true', help='Exclude symbols (!@#$)')

parser.add_argument('-i', '--include', type=str, default=None, help='Whitelist characters from their char-set')
parser.add_argument('-e', '--exclude', type=str, default=None, help='Blacklist characters')

parser.add_argument('-r', '--regex', type=str, help='Result MUST match regex')
parser.add_argument('-R', '--antiregex', type=str, help='Result must NOT match regex')

args = parser.parse_args()


def whitelist(charstr: str, whitelist: Optional[str]) -> str:
    if whitelist is not None:
        charset = set(charstr)
        whiteset = set(whitelist)

        charset.intersection_update(whiteset)

        if len(charset) != 0:
            charstr = ''.join(charset)

    return charstr


def mkpasswd(charset, size):
    return ''.join([choice(charset) for _ in range(size)])


def main():
    letters = whitelist(''.join([chr(ord('A') + i) + chr(ord('a') + i) for i in range(26)]), args.include)
    digits = whitelist(''.join([str(i) for i in range(10)]), args.include)
    symbols = whitelist('!@#$\%^&*()_+`-=\\|{}[];\':",./<>?', args.include)

    alphabet = ''

    if not args.letters:
        alphabet += letters
    if not args.digits:
        alphabet += digits
    if not args.symbols:
        alphabet += symbols

    alphaset = set(alphabet)
    if args.exclude is not None:
        alphaset.difference_update(args.exclude)

    alphabet = ''.join(alphaset)

    passwd = mkpasswd(alphabet, args.length)

    if args.regex is not None:
        regex = re.compile(args.regex)
        while not regex.search(passwd):
            passwd = mkpasswd(alphabet, args.length)

    elif args.antiregex is not None:
        regex = re.compile(args.antiregex)
        while regex.search(passwd):
            passwd = mkpasswd(alphabet, args.length)

    print(passwd)


if __name__ == "__main__":
    main()
