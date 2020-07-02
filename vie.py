#!/usr/bin/python

""" Open ebuild with vi from equery list or emerge output. """

# Import
import sys
import subprocess
import re
import os.path
import logging
import argparse
import glob

def init_log():
    """
    Init log mechanism
    :return:
    :rtype:
    """
    __formatter = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
    logging.VERBOSE = 15
    logging.addLevelName(logging.VERBOSE, 'VERBOSE')
    __logger = logging.getLogger('ip_port_audit')
    __logger.setLevel('INFO')
    __console_handler = logging.StreamHandler(sys.stdout)
    __console_handler.setFormatter(__formatter)
    __logger.addHandler(__console_handler)
    __logger.propagate = False
    return __logger


def parse_args():
    """
    Parse script arguments
    :return: parsed arguments
    :rtype:
    """
    parser = argparse.ArgumentParser()
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('-v', '--verbose', action="store_true")
    log_group.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('ebuild', help='ebuild name', type=str)
    parser.add_argument('-p', '--pretend', action="store_true", default=False)
    args = parser.parse_args()
    return args


def main():
    """
    Main function
    """
    # Argument management
    args = parse_args()

    # Init log
    logs = init_log()

    if args.verbose:
        logs.setLevel('VERBOSE')

    if args.debug:
        logs.setLevel('DEBUG')

    pretend = bool(args.pretend)

    # Store agument in variable
    ebuild = args.ebuild
    # Log
    logs.log(logging.VERBOSE, 'ebuild : %s', ebuild)

    # Test if argument matches right format
    # IE : net-fs/samba-4.11.8
    regex = re.compile(r'[a-z]+-[a-z]+/[a-z0-9\-\._]+')
    # IE : net-fs/samba-4.11.8::gentoo
    source_regex = re.compile(r'[a-z]+-[a-z]+/[a-z0-9\-\._]+[a-zA-Z0-9-_]+')

    # Wildcard variable when ebuild doesn't contain version
    wildcard = False

    # Check if ebuild matchs regex
    if regex.match(ebuild) or source_regex.match(ebuild):
        # Log
        logs.log(logging.VERBOSE, '%s matches ebuild regex', ebuild)
        # Define version regex
        version_regex = re.compile(r'-[r0-9.-]+')
        # Check if ebuild contain version :
        if version_regex.search(ebuild):
            # Log
            logs.log(logging.VERBOSE, '%s contains version', ebuild)
            # Extract category from ebuild name
            clean_category = re.split('-[r0-9.-]+', ebuild)[0]
            # Ebuild file name
            ebuild_file_name = ebuild.split('/')[1].split(':')[0] + ".ebuild"
        else:
            # Log
            logs.log(logging.VERBOSE, '%s doesnt contain version', ebuild)
            # Wildcard will be used when using VI
            wildcard = True
            # No version here, so no processing
            clean_category = ebuild
            # Ebuild file name
            ebuild_file_name = ebuild.split('/')[1].split(':')[0] + "*.ebuild"
    else:
        logs.error("Error : argument format is incorrect")
        sys.exit(-2)

    # Generate complete path
    complete_path = "/usr/portage/"+clean_category+"/"+ebuild_file_name

    # Logs
    logs.log(logging.VERBOSE, 'clean_category : %s', clean_category)
    logs.log(logging.VERBOSE, 'ebuild_file_name : %s', ebuild_file_name)
    logs.log(logging.VERBOSE, 'complete_path : %s', complete_path)

    # If file exists, open it in VI
    if os.path.isfile(complete_path) and not wildcard:
        if pretend:
            print('vi ' + complete_path)
        else:
            subprocess.call(['vi', complete_path])
    elif wildcard:
        ebuilds = glob.glob(complete_path)
        if ebuilds:
            # Get last ebuild
            real_ebuild_file_name = ebuilds[-1]
            # Log
            logs.log(logging.VERBOSE, 'real_ebuild_file_name : %s', real_ebuild_file_name)

            if pretend:
                print('vi ' + real_ebuild_file_name)
            else:
                subprocess.call(['vi', real_ebuild_file_name])
        else:
            logs.error("Ebuild doesn't exist")
    else:
        logs.error("Ebuild doesn't exist")


if __name__ == "__main__":
    main()
