import argparse
import getpass
import logging

def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--version',
        action='version',
        version=('Evolution Cli Client v0.0'),
        help='Version')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        parents=[parent_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    parser = subparsers.add_parser(
        'room_new',
        parents=[parent_parser],
        description='Creates new room',
        help='Creates new room')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')

    parser = subparsers.add_parser(
        'room_connect',
        parents=[parent_parser],
        description='Connects to existing room',
        help='Connects to existing room')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')
    parser.add_argument(
        'player',
        type=str,
        help='Player nick')

    parser = subparsers.add_parser(
        'room_start',
        parents=[parent_parser],
        description='Starts the game',
        help='Starts the game')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')


    return parser
