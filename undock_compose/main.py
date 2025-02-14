#!/usr/bin/env python3
"""Convert your unRAID Docker XML templates to Docker Compose YAML files.

Takes in an unRAID Docker XML template file and parses it into a Docker Compose
compatible dictionary ready for dumping as a YAML file.
"""

from undocker import argparser, UnDocker


def main():
    args, unargs = argparser()

    container = UnDocker(args.input[0], args.output, args.labels)
    container.compose()


if __name__ == "__main__":
    main()
