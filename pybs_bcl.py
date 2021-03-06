#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
import sys
import argparse
import hashlib
import os.path
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from BaseSpacePy.model.QueryParameters import QueryParameters as qp


__author__ = "Jialei Duan"


def md5_hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(10240), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
                        help='specify download directory. \
                        The default is the current directory')
    parser.add_argument('--offset', dest='offset', required=False,
                        type=int,
                        default=0,
                        help='specify the starting offset to read. \
                              The default is 0')
    parser.add_argument('-n', '--num_items', dest='num_items', required=False,
                        type=int,
                        default=10,
                        help='specify the maximum number of items to return \
                              (max 1024). The default is 10')
    parser.add_argument('-e', '--excluded_path', dest='excluded_path', required=False,
                        type=str,
                        default=None,
                        help='specify files to skip (comma separated). \
                              If file paths contain \
                              this(ese) strings, it will be skipped.)\
                              The default is None')

    args = parser.parse_args()

    client_key = args.key
    client_secret = args.secret
    client_token = args.token
    run_name = args.run
    download_directory = args.directory

    if args.excluded_path:
        excluded_file_path_strings = args.excluded_path.split(',')
    else:
        excluded_file_path_strings = []

    num_items = args.num_items
    offset = args.offset

    base_space_url = 'https://api.basespace.illumina.com/'

    my_bs_api = BaseSpaceAPI(client_key,
                             client_secret,
                             base_space_url,
                             'v1pre3',
                             '',
                             client_token)

    user = my_bs_api.getUserById('current')
    print('User: {}'.format(str(user)),
          sep='', file=sys.stderr)

    runs = user.getRuns(my_bs_api, queryPars=qp({'Limit': num_items}))
    print('Run(s): {}'.format(runs), sep='', file=sys.stderr)

    if run_name:
        run = runs[[index for index, value
                    in enumerate(runs) if value.Name == run_name][0]]

        print('Total size ({}): {} GB'.format(run.Name,
                                              run.TotalSize / 1000000000),
              sep='', file=sys.stderr)
        print('Offset: {}'.format(offset),
              sep='', file=sys.stderr)
        print('Number of items to return: {}'.format(num_items),
              sep='', file=sys.stderr)

        for f in run.getFiles(my_bs_api,
                              queryPars=qp({'Limit': num_items,
                                            'Offset': offset})):

            file_path = f.Path

            if any([i in file_path for i in excluded_file_path_strings]):
                print('Skipping file: {}'.format(file_path),
                      file=sys.stderr)

            else:
                print('Downloading file: {}'.format(file_path),
                      '...', sep=' ', end='', file=sys.stderr)

                try:
                    f.downloadFile(my_bs_api, download_directory, createBsDir=True)

                    etag = f.getFileS3metadata(my_bs_api)['etag']
                    file_path = download_directory + '/' + file_path

                    if len(etag) == 32:
                        f_md5 = md5_hash(file_path)

                        if f_md5 == etag:
                            print(' done (md5 correct)!',
                                  file=sys.stderr)
                        else:
                            print(' error (md5 incorrect)!',
                                  f.Id,
                                  etag,
                                  f_md5,
                                  file=sys.stderr)

                    else:
                        if f.Size == os.path.getsize(file_path):
                            print(' done (file size correct)!',
                                  file=sys.stderr)
                        else:
                            print(' error (file size incorrect)!',
                                  f.Id,
                                  etag,
                                  file=sys.stderr)

                except Exception as e:
                    print(' error ({})!!'.format(e),
                          file=sys.stderr)


if __name__ == '__main__':
    main()
