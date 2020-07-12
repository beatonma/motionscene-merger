### scenemerge

File injection tool to allow reuse of ConstraintSet definitions in multiple MotionScenes.

## In your environment:

    git clone https://github.com/motionscene-merger
    python setup install

    scenemerge .


## Creating merge instructions:
- In your resources/xml directory, create your MotionScene and ConstraintSet files, each prepended with `_merge_src_`.
 - e.g. `resources/xml/_merge_src_YOUR_MOTIONSCENE_FILENAME.xml`
 - e.g. `resources/xml/_merge_src_YOUR_CONSTRAINTSET_FILENAME.xml`

- In your MotionScene file, add a line with the signature `__merge__(_merge_src_YOUR_CONSTRAINTSET_FILENAME)`
- The content from the specified ConstraintSet file will be copied in place into a new MotionScene file called `YOUR_MOTIONSCENE_FILENAME.xml`.

Please check the files in `test/example_root_dir/resources/xml` for example source files.

This project was written on a Sunday evening. It is unlikely to have any major updates but feel free to make pull requests or whatever.
Hopefully MotionScene will someday have some kind built-in include/merge functionality and make this obsolete but this will have to do for now...
