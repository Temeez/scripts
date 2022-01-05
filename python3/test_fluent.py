#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import argparse
from glob import glob
from os import listdir, walk
from os.path import isdir, join, splitext

# Defaults
I18N_DIR = "i18n"
SRC_DIR = "src"
SRC_EXT = ".rs"
REGEX = r'fl!."(.*?)"'

def validate_fluent_file(file_path):
    """Check if the fluent file has duplicate keys.
    Returns "fluent keys" in array.
    """
    print("\nValidating file:", file_path)
    fluent_keys = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.find("=") != -1:
                translation_key = line.split("=")[0].strip()
                try:
                    fluent_keys.index(translation_key)
                    print(" - Duplicate [ " + translation_key +" ]. One of them can be removed.")
                except ValueError:
                    pass
                fluent_keys.append(translation_key)
    return fluent_keys


def read_source_file(file_path, regex):
    """Finds all fluent keys from the supplied source file."""
    keys = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.find("fl!") != -1:
                finds = re.findall(regex, line)
                if finds:
                    keys.append(finds[0])
    return keys


def fluent_translation_keys(fluent_key):
    for (dirpath, dirnames, filenames) in walk(SRC_DIR):
        print(dirnames)


def main(args):
    i18n_dir = args.i or I18N_DIR
    src_dir = args.s or SRC_DIR
    src_ext = args.e or SRC_EXT
    regex = args.r or REGEX

    language_dirs_success = []
    language_dirs_fail = []

    # Get all source files which can contain fluent keys
    source_files = glob('{}/**/*{}'.format(src_dir, src_ext), recursive=True)

    keys_in_sources = []
    for source_file in source_files:
        keys_in_sources = keys_in_sources + read_source_file(source_file, regex)

    # List of fluent keys found in source files without duplicates
    all_fluent_keys = list(set(keys_in_sources))

    if not isdir(i18n_dir):
        print("i18n directory not found: [ {} ].".format(i18n_dir))
        sys.exit(1)

    if not isdir(src_dir):
        print("Source directory not found: [ {} ].".format(src_dir))
        sys.exit(1)

    if not all_fluent_keys:
        print("No source files found in path: [ {} ] with extension: [ {} ].".format(src_dir, src_ext))
        sys.exit(1)

    for lang_dir in listdir(i18n_dir):
        path = join(i18n_dir, lang_dir)
        print("Checking language:", lang_dir)
        lang_path = join(i18n_dir, lang_dir)
        for lang_file in listdir(lang_path):
            filename, file_extension = splitext(lang_file)
            # Check the file extension
            if file_extension != '.ftl':
                print("Wrong file extension [ {} ]. It should be: [ {}{} ].".format(lang_file, filename, ".ftl"))
                language_dirs_fail.append(lang_dir)
                continue

            file_path = join(lang_path, lang_file)
            keys_in_fluent_file = validate_fluent_file(file_path)

            print("\n")
            for key_in_fluent_file in keys_in_fluent_file:
                try:
                    all_fluent_keys.index(key_in_fluent_file)
                except ValueError:
                    print("Unused fluent key found: {}".format(key_in_fluent_file))
                    # This shouldn't fail anything since this is just clutter,
                    # but doesn't break anything.

            for fluent_key in all_fluent_keys:
                try:
                    keys_in_fluent_file.index(fluent_key)
                except ValueError:
                    print("Missing fluent key found! [ {} ] is not present in the fluent file: {}".format(fluent_key, file_path))
                    language_dirs_fail.append(lang_dir)

        # If the language is not in the fail array
        # then add it to the success array
        try:
            language_dirs_fail.index(lang_dir)
        except ValueError:
            language_dirs_success.append(lang_dir)

    if language_dirs_fail:
        print("\n=== FAILURE ===")
        print("The following languages failed to validate: {}".format(', '.join(language_dirs_fail)))
        sys.exit(1)
    else:
        print("\n=== SUCCESS ===")
    print("The following languages were validated successfully: {}".format(', '.join(language_dirs_success) or "NONE"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Validates the fluent translation files and checks if there are any missing fluent keys in the file based on source files.")
    parser.add_argument("-i", help="i18n directory path. Default: i18n")
    parser.add_argument("-s", help="Source directory path. Default: src")
    parser.add_argument("-e", help="Source file extension. Default: .rs")
    parser.add_argument("-r", help="Regex string for finding the fluent keys in the source files. Default: {}".format('fl!."(.*?)"'))

    args = parser.parse_args()

    main(args)
