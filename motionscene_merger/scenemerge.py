"""
File injection tool to allow reuse of ConstraintSet definitions in multiple MotionScenes.

Requirements:
- In your resources/xml directory, create a MotionScene and ConstraintSet files, each prepended with FILE_PREFIX.
 - e.g. resources/xml/_merge_src_YOUR_MOTIONSCENE_FILENAME.xml
 - e.g. resources/xml/_merge_src_YOUR_CONSTRAINTSET_FILENAME.xml

In the above MotionScene file, add a line with the signature __merge__(_merge_src_YOUR_CONSTRAINTSET_FILENAME)
"""


import argparse
import glob
import logging
import os
import re
from typing import List

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


FILE_PREFIX = '_merge_src_'
MERGE_TAG = '__merge__'
MERGE_TAG_PATTERN = re.compile(rf'^([ ]*){MERGE_TAG}\((.*?)\)', flags=re.DOTALL | re.MULTILINE)
MOTION_SCENE_PATTERN = re.compile(r'.*?<MotionScene.*?>.*?__merge__.*?</MotionScene>', flags=re.DOTALL)
CONSTRAINT_SET_PATTERN = re.compile(r'<ConstraintSet.*?>.*?</ConstraintSet>', flags=re.DOTALL)
CONSTRAINT_SET_START_PATTERN = re.compile(r'[ ]*<ConstraintSet.*')
XML_FILE_HEADER = '<?xml version="1.0" encoding="utf-8"?>'
INJECTION_MESSAGE_START = '<!-- Start injected content from \'{filename}\' -->\n'
INJECTION_MESSAGE_END = '<!-- End injected content from \'{filename}\' -->\n'


class MergeTag:
    def __init__(self, filename: str, indent: int):
        self.filename = filename
        self.indent = indent
        self.source_content = ''

    def resolve_content(self, xml_files: List[str]):
        """Find the referenced file by filename and extract its content."""
        candidate_filenames = [
            self.filename,
            self.filename + '.xml',
        ]

        source_file = None
        for f in xml_files:
            fname = os.path.basename(f)
            if fname in candidate_filenames:
                source_file = f

        if source_file is None:
            raise Exception(f'File not found for filename=\'{self.filename}\' {xml_files}')

        self.source_content = ''
        self._add_content_line(INJECTION_MESSAGE_START.format(filename=self.filename))
        with open(source_file, 'r') as f:
            for line in f.readlines():
                if XML_FILE_HEADER in line:
                    continue
                self._add_content_line(line)
        self._add_content_line(INJECTION_MESSAGE_END.format(filename=self.filename))

    def _add_content_line(self, content):
        indent = ' ' * self.indent
        self.source_content = f'{self.source_content}{indent}{content}'


class MotionSceneSrc:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.src_text = f.read()

    def get_target_file(self) -> str:
        dirname = os.path.dirname(self.filepath)
        fname = os.path.basename(self.filepath)

        fname = fname.replace(FILE_PREFIX, '')
        target_filepath = os.path.join(dirname, fname)
        assert(target_filepath != self.filepath)
        return target_filepath

    def inject(self, merge_tag: MergeTag):
        target = self.get_target_file()
        log.info(f'Merging {merge_tag.filename} into {target}...')
        composed_text = self.src_text.replace(
            f'{MERGE_TAG}({merge_tag.filename})',
            merge_tag.source_content
        )
        self.src_text = composed_text
        with open(target, 'w') as f:
            f.write(composed_text)


def _find_merge_tags(src_text: str) -> List[MergeTag]:
    matches = MERGE_TAG_PATTERN.findall(src_text)
    results = [
        MergeTag(m[1], len(m[0])) for m in matches
    ]
    return results


def _get_xml_resource_filenames(rootdir: str) -> List[str]:
    glb = f'{rootdir}/**/resources/xml/{FILE_PREFIX}*.xml'.replace('//', '/')
    return glob.glob(glb)


def _get_motionscene_files(xml_files: List[str]) -> List[MotionSceneSrc]:
    results = []
    for filename in xml_files:
        with open(filename, 'r') as f:
            src_text = f.read()
            if MOTION_SCENE_PATTERN.match(src_text) is not None:
                results.append(MotionSceneSrc(filename))

    return results


def _merge_sources_for_directory(root: str):
    xml_files = _get_xml_resource_filenames(root)
    _merge_sources(xml_files)


def _merge_sources(xml_files: List[str]):
    motionscene_files = _get_motionscene_files(xml_files)

    for m in motionscene_files:
        merge_tags = _find_merge_tags(m.src_text)
        for tag in merge_tags:
            tag.resolve_content(xml_files)
            m.inject(tag)


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'root',
        default='.',
    )

    return parser.parse_args()


def main():
    _args = _parse_args()
    _merge_sources_for_directory(_args.root)


if __name__ == '__main__':
    main()
