from setuptools import setup

setup(
    name='motionscene-merger',
    version='2.1',
    packages=['motionscene_merger'],
    url='https://beatonma.org',
    license='GNU General Public License v3.0',
    author='Michael Beaton',
    author_email='michael@beatonma.org',
    description=(
        'File injection tool to allow reuse of ConstraintSet definitions in '
        'multiple MotionScenes.',
    ),
    entry_points={
        'console_scripts': [
            'scenemerge=motionscene_merger.scenemerge:main'
        ]
    }
)
