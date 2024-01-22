#!/usr/bin/env python3
import argparse, textwrap, re, os
from pathlib import Path
"""
Bulk parse unraid config files into, docker compose files.
"""

from undocker import argparser, UnDocker


def main():
    # parse the in and out folders ect via parser then run the same
    # logic as is in main.py, just modified to work on each file
    inputfolder, outputfolder, inputFilter, RX, labels =  parser()

    for file in os.listdir(inputfolder):
        filename = os.fsdecode(file)
        if RX.match(filename):
            print(f"found {filename} processing...")
            filePath = os.path.join(inputfolder.decode("utf-8"), f"{filename}")
            outputName = filename.rsplit( ".", 1)[0] + ".yaml"
            outputPath = os.path.join(outputfolder.decode("utf-8"), outputName)
            print(f"out to -> {outputPath}")
            container = UnDocker(filePath, outputPath, labels)
            container.compose()
        else:
            print(f"skipping {filename}")

def parser():
    # grab environment variables
    inputDir = os.environ.get('UNDOCK_INPUT')
    outputDir = os.environ.get('UNDOCK_OUTPUT')
    inputFilter = os.environ.get('UNDOCK_FILTER')
    args = cli_parser()
    print (args)

    # check that either environment variables or flags are set flags
    # take precident, if neither are set quit!
    if args.input:
        inputfolder = os.fsencode(args.input)
    elif inputDir:
        print ("using environment variable for input")
        inputfolder = os.fsencode(inputDir)
    else:
        print ("input directory has not been set")
        quit()
    if not os.path.isdir(inputfolder):
        print(f"the specified input directory {inputfolder} does not exist")
        quit()


    if args.output:
        outputfolder = os.fsencode(args.output)
    elif outputDir:
        print ("using environment variable for output")
        outputfolder = os.fsencode(outputDir)
    else:
        print ("output directory has not been set")
        quit()
    if not os.path.isdir(outputfolder):
        print(f"the specified output directory {outputfolder} does not exist")
        quit()

    if args.filter:
        inputFilter = args.filter
    elif inputFilter:
        print ("using environment variable for filter")
    else:
        print("the input filter has not been set")

    try:
        RX = re.compile(inputFilter, re.IGNORECASE)
    except re.error:
        print("invalid regex exiting")
        quit()

    # everything checks out return values
    return (inputfolder, outputfolder, inputFilter, RX, args.labels)

def cli_parser():
    # get values passed to program
    parser = argparse.ArgumentParser(
        prog='undocker-bulk',
        description='this does what undocker does but operates on directories instead of single files',
    )
    parser.add_argument(
        "--input",
        "-i",
        nargs="?",
        help=textwrap.dedent("""\
        Path to the input directory
        """),
        )
    parser.add_argument(
        "--output",
        "-o",
        nargs="?",
        help=textwrap.dedent("""\
        Path to the output directory
        """),
    )
    parser.add_argument(
        "--filter",
        "-f",
        nargs="?",
        help=textwrap.dedent("""\
        Filter to use to select input files i.e '.*xml'
        """),
        default=".*.xml",
    )
    parser.add_argument(
        "--labels",
        "-l",
        action="store_true",
        help="Flag to include unRAID Docker labels for the configurations",
        )
    return parser.parse_args()
    # args, unargs = argparser()

    # container = UnDocker(args.input[0], args.output, args.labels)
    # container.compose()


if __name__ == "__main__":
    main()
