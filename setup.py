from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='motionscene-merger',
    version='2.4.1',
    packages=['motionscene_merger'],
    url='https://github.com/beatonma/motionscene-merger',
    license='GNU General Public License v3.0',
    author='Michael Beaton',
    author_email='michael@beatonma.org',
    description=(
        'File injection tool for Android developers using MotionLayout. '
        'Use scenemerge to reuse ConstraintSet/KeyFrameSet/etc definitions in '
        'multiple MotionScenes via a templating system.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'scenemerge=motionscene_merger.scenemerge:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    python_requires='>=3.6',  # May work in earlier versions but only actually tested on 3.8
)
