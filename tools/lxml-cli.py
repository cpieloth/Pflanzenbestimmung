import abc
import argparse
import os
import sys

import lxml.etree as ET


class SubCommand(abc.ABC):
    """
    Abstract base class for sub commands.
    A new sub command can be added by calling the init_subparser().
    """

    @classmethod
    @abc.abstractmethod
    def _name(cls):
        """
        Return name of the command.
        :return: Command name
        :rtype: str
        """
        raise NotImplementedError()

    @classmethod
    def _help(cls):
        """
        Return help description.
        :return: Help description
        :rtype: str
        """
        return cls.__doc__

    @classmethod
    @abc.abstractmethod
    def _add_arguments(cls, parser):
        """
        Initialize the argument parser and help for the specific sub-command.
        Must be implemented by a sub-command.
        :param parser: A parser.
        :type parser: argparse.ArgumentParser
        :return: void
        """
        raise NotImplementedError()

    @classmethod
    def init_subparser(cls, subparsers):
        """
        Initialize the argument parser and help for the specific sub-command.
        :param subparsers: A subparser.
        :type subparsers: argparse.ArgumentParser
        :return: void
        """
        parser = subparsers.add_parser(cls._name(), help=cls._help())
        cls._add_arguments(parser)
        parser.set_defaults(func=cls.execute)

    @classmethod
    @abc.abstractmethod
    def execute(cls, args):
        """
        Execute the command.
        Must be implemented by a sub-command.
        :param args: argparse arguments.
        :return: 0 on success.
        """
        raise NotImplementedError()


class TransformCmd(SubCommand):
    """Transform a XML using a XSL/XSLT."""

    @classmethod
    def _name(cls):
        return 'transform'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('--xml', help='XML to transform.')
        parser.add_argument('--xsl', help='XSL/XSLT use to transform.')
        parser.add_argument('--out', help='Output file path.')
        return parser

    @classmethod
    def execute(cls, args):
        dom = ET.parse(os.path.abspath(args.xml))
        xslt = ET.parse(os.path.abspath(args.xsl))

        transform = ET.XSLT(xslt)
        newdom = transform(dom)

        with open(os.path.abspath(args.out), mode='wb') as file:
            file.write(ET.tostring(newdom, pretty_print=True))

        return 0


def main(argv=None):
    if not argv:
        argv = sys.argv

    # Parse arguments
    parser = argparse.ArgumentParser(prog=argv[0])

    subparser = parser.add_subparsers(title='CLI wrapper for lxml,', description='Valid commands.')
    TransformCmd.init_subparser(subparser)

    args = parser.parse_args(argv[1:])
    try:
        # Check if a sub-command is given, otherwise print help.
        getattr(args, 'func')
    except AttributeError:
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
