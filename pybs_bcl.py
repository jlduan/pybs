#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
import sys
import argparse
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from BaseSpacePy.model.QueryParameters import QueryParameters as qp


__author__ = "Jialei Duan"


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-k', '--key', dest='key', required=True,
                        type=str,
                        help='specify client key')
    parser.add_argument('-s', '--secret', dest='secret', required=True,
                        type=str,
                        help='specify client secret')
    parser.add_argument('-t', '--token', dest='token', required=True,
                        type=str,
                        help='specify access token')
    parser.add_argument('-r', '--run', dest='run', required=False,
                        type=str,
                        help='specify the run name to download')
    parser.add_argument('-d', '--directory', dest='directory', required=False,
                        type=str,
                        default='./',
                        help='specify download file directory. \
                        The default is current directory')
    parser.add_argument('-offset', dest='offset', required=False,
                        type=int,
                        default=0,
                        help='specify the offset')
    parser.add_argument('-n', '--number', dest='number', required=False,
                        type=int,
                        default=10,
                        help='specify the number of iterms to retrieve')

    args = parser.parse_args()

    client_key = args.key
    client_secret = args.secret
    client_token = args.token
    run_id = args.run
    download_directory = args.directory

    num_iterms = args.number
    offset = args.offset

    BaseSpaceUrl = 'https://api.basespace.illumina.com/'

    my_bs_api = BaseSpaceAPI(client_key,
                             client_secret,
                             BaseSpaceUrl,
                             'v1pre3',
                             '',
                             client_token)


    user = my_bs_api.getUserById('current')
    print('The current user is:\n',
          ' ' * 4,
          str(user), sep='', file=sys.stderr)

    runs = user.getRuns(my_bs_api, queryPars=qp({'Limit': num_iterms}))
    print('The project(s) for this user is/are:\n',
          ' ' * 4,
          runs, sep='', file=sys.stderr)

    if run_id:
        run = runs[[index for index, value
                    in enumerate(runs) if str(value) == run_id][0]]

        print('The total size of this run is (Gb):\n',
              ' ' * 4,
              run.TotalSize / 1000000000,
              sep='', file=sys.stderr)
        print('The file offset is:\n',
              ' ' * 4,
              offset,
              sep='', file=sys.stderr)
        print('The number of iterms is:\n',
              ' ' * 4,
              num_iterms,
              sep='', file=sys.stderr)
        print('Downloading file:', sep='', file=sys.stderr)

        for f in run.getFiles(my_bs_api,
                              queryPars=qp({'Limit': num_iterms})):
            print(' ' * 4,
                  str(f),
                  sep='', file=sys.stderr)
            f.downloadFile(my_bs_api, download_directory, createBsDir=True)

if __name__ == '__main__':
    main()
