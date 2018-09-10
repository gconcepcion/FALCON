from __future__ import absolute_import

import argparse
import logging
import os
import sys
from .. import io
from .. import bash  # for write_script

LOG = logging.getLogger()

def run(daligner_settings_fn, daligner_script_fn, job_done_fn):
    cwd = os.getcwd()
    LOG.info('Running daligner from {!r} (using {!r}) to write {!r}'.format(
        daligner_script_fn, daligner_settings_fn, job_done_fn))
    script = open(daligner_script_fn).read()
    #daligner_settings = io.deserialize(daligner_settings_fn) # not used

    script_fn = 'run_daligner.sh'
    bash.write_script(script, script_fn, job_done_fn)
    io.syscall('bash -vex {}'.format(script_fn))


class HelpF(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(argv):
    description = 'Run daligner (including LAsort and first-level LAmerge) using the script generated by HPC.daligner.'
    epilog = 'The real .las output will be next to the job-done sentinel file, but we would have to parse HPD.daligner to learn the actual filename.'
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=HelpF,
    )
    parser.add_argument(
        '--daligner-settings-fn',
        help='Input. Any extra settings for daligner.',
    )
    parser.add_argument(
        '--daligner-script-fn',
        help='Input. Part of the output of HPC.daligner.',
    )
    parser.add_argument(
        '--job-done-fn',
        help='Output. Just a sentinel. The real .las output is next to this file, implicitly.',
    )
    args = parser.parse_args(argv[1:])
    return args


def main(argv=sys.argv):
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    run(**vars(args))


if __name__ == '__main__':  # pragma: no cover
    main()