#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20140904

import argparse


def main():
	

	parser = argparse.ArgumentParser(description='Demo of argparse')
	parser.add_argument("dirname", help='directory in cui ci sono i film da analizzare')
	
	
	args = parser.parse_args()

	run(args)

if __name__ == '__main__':
    main()