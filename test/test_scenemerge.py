"""

"""

import logging
import os
from unittest import TestCase

from motionscene_merger.scenemerge import (
    MERGE_FILE_PREFIX,
    _find_merge_tags,
    _get_motionscene_files,
    _get_xml_resource_filenames,
    _merge_sources_for_directory,
)

log = logging.getLogger(__name__)


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

    __merge__(constraintset_two)

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


def _get_xml_path(filename: str):
    return os.path.join(
        TEST_XML_DIR,
        filename
    )


class MergeTestCase(TestCase):
    def _clean_generated_files(self):
        for f in os.listdir(TEST_XML_DIR):
            if f.endswith('.xml') and not f.startswith(MERGE_FILE_PREFIX) and 'example' in f:
                os.remove(os.path.join(TEST_XML_DIR, f))

    def setUp(self) -> None:
        self._clean_generated_files()

    def tearDown(self) -> None:
        self._clean_generated_files()

    def test_merge_tag_regex(self):
        results = _find_merge_tags(MOTION_SCENE)
        self.assertEqual(1, len(results))

        m = results[0]
        self.assertEqual(
            m.filename,
            'constraintset_two'
        )
        self.assertEqual(
            m.indent,
            4
        )

    def test_get_xml_resource_filenames(self):
        expected_files = [
            '_merge_src_another_example_constraintset.xml',
            '_merge_src_example_constraintset.xml',
            '_merge_src_example_motion_scene.xml',
            '_merge_src_example_motion_scene_2.xml',
            '_merge_src_example_motion_scene_3.xml',
        ]
        results = _get_xml_resource_filenames(EXAMPLE_ROOT_DIR)
        actual_files = [os.path.basename(r) for r in results]
        self.assertListEqual(actual_files, expected_files)

    def test_get_motionscene_files(self):
        files = _get_xml_resource_filenames(EXAMPLE_ROOT_DIR)
        motionscenes = _get_motionscene_files(files)

        self.assertEqual(len(motionscenes), 3)
        self.assertEqual(
            os.path.basename(motionscenes[0].filepath),
            '_merge_src_example_motion_scene.xml'
        )

    def test_motionscene_target_filename(self):
        root = EXAMPLE_ROOT_DIR
        files = _get_xml_resource_filenames(root)
        motionscene_files = _get_motionscene_files(files)

        self.assertEqual(
            motionscene_files[0].get_target_file(),
            _get_xml_path('example_motion_scene.xml')
        )

    def test_complete(self):
        expected_output_path = _get_xml_path('example_motion_scene.xml')
        self.assertFalse(os.path.exists(expected_output_path))

        _merge_sources_for_directory(EXAMPLE_ROOT_DIR)

        self.assertTrue(os.path.exists(expected_output_path))

        with open(expected_output_path, 'r') as f:
            content = f.readlines()

            for n, line in enumerate(content):
                log.info(f'{n}: {line}')

            self.assertTrue("<!-- Start injected content from '_merge_src_example_constraintset' -->" in content[23])
            self.assertTrue("<!-- End injected content from '_merge_src_example_constraintset' -->" in content[26])

            self.assertTrue("<!-- Start injected content from '_merge_src_another_example_constraintset' -->" in content[29])
            self.assertTrue("<!-- End injected content from '_merge_src_another_example_constraintset' -->" in content[32])

    def test_merge_motionscene_into_motionscene(self):
        expected_output_path = _get_xml_path('example_motion_scene_2.xml')
        self.assertFalse(os.path.exists(expected_output_path))
        _merge_sources_for_directory(EXAMPLE_ROOT_DIR)
        self.assertTrue(os.path.exists(expected_output_path))

        with open(expected_output_path, 'r') as f:
            content = f.read()
            self.assertEqual(content.count('MotionScene'), 2)
            self.assertTrue('clickAction="toggle"' in content)
