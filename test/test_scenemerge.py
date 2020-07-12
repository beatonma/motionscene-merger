"""

"""

import logging
import os
from unittest import TestCase

from motionscene_merger.scenemerge import (
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
GENERATED_FILE_EXPECTED_PATH = os.path.join(
    os.path.join(
        EXAMPLE_ROOT_DIR,
        _join_dirs('main/resources/xml/')
    ),
    'example_motion_scene.xml'
)


class MergeTestCase(TestCase):
    def setUp(self) -> None:
        if os.path.exists(GENERATED_FILE_EXPECTED_PATH):
            os.remove(GENERATED_FILE_EXPECTED_PATH)

    def tearDown(self) -> None:
        if os.path.exists(GENERATED_FILE_EXPECTED_PATH):
            os.remove(GENERATED_FILE_EXPECTED_PATH)

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
        ]
        results = _get_xml_resource_filenames(EXAMPLE_ROOT_DIR)
        actual_files = [os.path.basename(r) for r in results]
        self.assertListEqual(actual_files, expected_files)

    def test_get_motionscene_files(self):
        files = _get_xml_resource_filenames(EXAMPLE_ROOT_DIR)
        motionscenes = _get_motionscene_files(files)

        self.assertEqual(len(motionscenes), 1)
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
            os.path.join(os.path.join(root, _join_dirs('main/resources/xml')), 'example_motion_scene.xml')
        )

    def test_complete(self):
        self.assertFalse(os.path.exists(GENERATED_FILE_EXPECTED_PATH))

        _merge_sources_for_directory(EXAMPLE_ROOT_DIR)

        self.assertTrue(os.path.exists(GENERATED_FILE_EXPECTED_PATH))

        with open(GENERATED_FILE_EXPECTED_PATH, 'r') as f:
            content = f.readlines()
            self.assertTrue("<!-- Start injected content from '_merge_src_example_constraintset' -->" in content[24])
            self.assertTrue("<!-- End injected content from '_merge_src_example_constraintset' -->" in content[28])

            self.assertTrue("<!-- Start injected content from '_merge_src_another_example_constraintset' -->" in content[31])
            self.assertTrue("<!-- End injected content from '_merge_src_another_example_constraintset' -->" in content[35])
