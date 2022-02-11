#!/usr/bin/env python3
"""
Author : esilberberg
Date   : 2022-02-10
Purpose: Get Publisher: Look up a journal's publisher through Sherpa Romeo's API
"""
import argparse
# --------------------------------------------------
def get_args():
    """Get a list of journal names or singular journal name"""
    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('positional',
                        metavar='str',
                        help='A positional argument')
    
    return parser.parse_args()
# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()

# --------------------------------------------------
if __name__ == '__main__':
    main()
