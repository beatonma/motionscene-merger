"""

"""

import logging
import os
from unittest import TestCase

from motionscene_merger.scenemerge import (
    DEFAULT_SOURCE_RES_DIR,
    SourceFile,
    _build_sourcemap,
    _find_merge_tags,
    _get_source_filepaths,
    _merge_sources_for_directory,
)

log = logging.getLogger(__name__)


TEST_SOURCE_FILES = [
    '_another_example_constraintset.xml',
    '_commented.xml',
    '_example_constraintset.xml',
    '_example_motion_scene.xml',
    '_example_motion_scene_2.xml',
    '_example_motion_scene_3.xml',
    '_nested_1.xml',
    '_nested_2.xml',
    '_nested_3.xml',
]
TEST_FILES = TEST_SOURCE_FILES + [
    'some_other_file.xml',
]


def _join_dirs(dirpath: str, separator='/'):
    parts = dirpath.split(separator)
    result = parts.pop(0)
    while len(parts) > 0:
        result = os.path.join(result, parts.pop(0))
    return result


MOTION_SCENE = """<?xml version="1.0" encoding="utf-8"?>
<MotionScene xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:motion="http://schemas.android.com/apk/res-auto">
    <StateSet>
        <State
            motion:constraints="@xml/constraints_one"/>
        <State
            motion:constraints="@xml/constraints_two"/>
    </StateSet>

    <Transition
        motion:constraintSetStart="@+id/constraintset_one"
        motion:constraintSetEnd="@+id/constraintset_two"
        >
        <OnClick
            motion:clickAction="toggle"
            motion:targetId="@+id/root"/>

    </Transition>

    <ConstraintSet
        android:id="@+id/constraintset_one"
        motion:deriveConstraintsFrom="@+id/constraintset_one_default"/>

    <inject src="constraintset_two"/>

</MotionScene>
"""

INJECTED_CONSTRAINT_SET = """<ConstraintSet
    android:id="@+id/constraintset_two"
    motion:deriveConstraintsFrom="@+id/constraintset_two_default"/>"""

MERGED = """
<?xml version="1.0" encoding="utf-8"?>
<MotionScene xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:motion="http://schemas.android.com/apk/res-auto">
    <StateSet>
        <State
            motion:constraints="@xml/constraints_one"/>
        <State
            motion:constraints="@xml/constraints_two"/>
    </StateSet>

    <Transition
        motion:constraintSetStart="@+id/constraintset_one"
        motion:constraintSetEnd="@+id/constraintset_two"
        >
        <OnClick
            motion:clickAction="toggle"
            motion:targetId="@+id/root"/>

    </Transition>

    <ConstraintSet
        android:id="@+id/constraintset_one"
        motion:deriveConstraintsFrom="@+id/constraintset_one_default"/>

    <ConstraintSet
        android:id="@+id/constraintset_two"
        motion:deriveConstraintsFrom="@+id/constraintset_two_default"/>

</MotionScene>

"""

EXAMPLE_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'example_root_dir')

TEST_XML_DIR = os.path.join(
    EXAMPLE_ROOT_DIR,
    _join_dirs('main/res/xml/')
)
TEST_SOURCE_DIR = TEST_XML_DIR

TEST_TEMP_DIR = 'temp-scenemerge/'


def _get_xml_path(filename: str):
    return os.path.join(
        TEST_XML_DIR,
        filename
    )


def _get_source_path(filename: str):
    return os.path.join(
        TEST_SOURCE_DIR,
        filename
    )


def _get_temp_path(filename: str):
    return os.path.join(
        TEST_TEMP_DIR,
        filename
    )


def _clean_generated_files():
    for d in [TEST_TEMP_DIR, TEST_XML_DIR]:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f not in TEST_FILES:
                    os.remove(os.path.join(d, f))
            if not os.listdir(d):
                os.rmdir(d)


class MergeTestCase(TestCase):
    """"""

    def setUp(self) -> None:
        _clean_generated_files()

    def tearDown(self) -> None:
        _clean_generated_files()

    def test_merge_tag_regex(self):
        results = _find_merge_tags(MOTION_SCENE)
        self.assertEqual(1, len(results))

        m = results[0]
        self.assertEqual(
            m.src,
            'constraintset_two.xml'
        )
        self.assertEqual(
            m.indent,
            4
        )

    def test_get_xml_resource_filenames(self):
        expected_files = TEST_SOURCE_FILES
        results = _get_source_filepaths(EXAMPLE_ROOT_DIR, sourceset='main', res_dir=DEFAULT_SOURCE_RES_DIR)
        actual_files = [os.path.basename(r) for r in results]
        self.assertListEqual(actual_files, expected_files)

    def test_complete(self):
        expected_output_path = _get_xml_path('example_motion_scene.xml')
        self.assertFalse(os.path.exists(expected_output_path))
    #
        _merge_sources_for_directory(EXAMPLE_ROOT_DIR, 'main')
    #
        self.assertTrue(os.path.exists(expected_output_path))
    #
        with open(expected_output_path, 'r') as f:
            content = f.readlines()

            for n, line in enumerate(content):
                line = line.replace("\n", "")
                log.info(f'{n}: {line}')

            self.assertTrue("<!-- Start injected content from '_example_constraintset.xml' -->" in content[28])
            self.assertTrue("<!-- End injected content from '_example_constraintset.xml' -->" in content[31])

            self.assertTrue("<!-- Start injected content from '_another_example_constraintset.xml' -->" in content[34])
            self.assertTrue("<!-- End injected content from '_another_example_constraintset.xml' -->" in content[37])

    def test_merge_motionscene_into_motionscene(self):
        expected_output_path = _get_xml_path('example_motion_scene_2.xml')
        self.assertFalse(os.path.exists(expected_output_path))
        _merge_sources_for_directory(EXAMPLE_ROOT_DIR, 'main')
        self.assertTrue(os.path.exists(expected_output_path))

        with open(expected_output_path, 'r') as f:
            content = f.read()
            self.assertEqual(content.count('MotionScene'), 2)
            self.assertTrue('clickAction="toggle"' in content)

    def test_parse_mergetag(self):
        text = '  <inject src="_some_file"/>'
        tags = _find_merge_tags(text)
        self.assertEqual(tags[0].indent, 2)
        self.assertEqual(tags[0].src, '_some_file.xml')

    def test_sourcefile_resolve_injections(self):
        sourcefile_one = SourceFile(_get_source_path('_example_constraintset.xml'))
        sourcefile_two = SourceFile(_get_source_path('_example_motion_scene_2.xml'))
        sourcefile_three = SourceFile(_get_source_path('_example_motion_scene_3.xml'))

        sources = _build_sourcemap([
            sourcefile_one,
            sourcefile_two,
            sourcefile_three,
        ])
        self.assertFalse(sources['_example_constraintset.xml'].resolved)
        self.assertFalse(sources['_example_motion_scene_2.xml'].resolved)

        sourcefile_one.resolve_injections(sources)
        self.assertTrue(sourcefile_one.resolved)
        self.assertTrue(sources['_example_constraintset.xml'].resolved)

        sourcefile_two.resolve_injections(sources)
        self.assertFalse(sourcefile_two.resolved)
        self.assertFalse(sources['_example_motion_scene_2.xml'].resolved)

    def test_transitive_injections(self):
        expected_output_path = _get_xml_path('nested_1.xml')
        _merge_sources_for_directory(EXAMPLE_ROOT_DIR, 'main')
        self.assertTrue(os.path.exists(expected_output_path))

        with open(expected_output_path, 'r') as f:
            content = f.read()
            self.assertTrue('android:id="@+id/should_be_transitively_injected_to__nested_one"' in content)

    def test_ignore_commented_injections(self):
        expected_output_path = _get_xml_path('commented.xml')
        _merge_sources_for_directory(EXAMPLE_ROOT_DIR, 'main')

        self.assertTrue(os.path.exists(expected_output_path))

        with open(expected_output_path, 'r') as f:
            content = f.read()
            self.assertTrue('<!--    <inject src="_example_constraintset"/>-->' in content)
            self.assertFalse('android:id="@+id/constraintset_two"/>' in content)
