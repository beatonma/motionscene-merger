### scenemerge

File injection tool to allow reuse of ConstraintSet/KeyFrameSet/etc definitions in multiple MotionScenes.

## Installation

    pip install motionscene-merger

or 

    git clone https://github.com/motionscene-merger
    python setup.py install

Then run with:

    scenemerge .


## Creating merge instructions
In your Android project `res/xml` directory:
- Create a MotionScene file with content that you want to inject into some other file. The filename must start with `_` e.g. `res/xml/_my_injectable_motionscene.xml`
- Create a template for your parent MotionScene. Again, the filename must start with `_` e.g. `res/xml/_my_parent_motionscene.xml`
  - add a line in this file with `<inject src="source_filename"/>` e.g:

    ```
        <?xml version="1.0" encoding="utf-8"?>
        <MotionScene
            xmlns:android="http://schemas.android.com/apk/res/android"
            xmlns:motion="http://schemas.android.com/apk/res-auto">
    
            <!-- Any other content here -->
        
            <inject src="my_injectable_motionscene"/>
    
            <!-- Any other content here -->
        
        </MotionScene>
    ```

Now when you run `scenemerge` the content from the MotionScene in `_my_injectable_motionscene.xml` will be copied in place into a new MotionScene file called `my_parent_motionscene.xml` in your `res/xml` directory. The `<MotionScene...></MotionScene>` tags will not be copied - only the content between them.

Please check the files in `test/example_root_dir/res/inject` for example source files.

## Android Studio File Watcher
- Install the `File Watcher` plugin for Android Studio via `Settings -> Plugins`.
- Restart and open `Settings -> Tools -> File Watchers`, then click the `+` to create a new Watcher.
- Set `File type` to XML.
- Create a Scope with a pattern like `file[app]:src/**/res/xml/_*.xml`
- Set `Program` to `scenemerge` in your environment. e.g. env/Scripts/scenemerge
- Set `Arguments` to `.`
- Set `Working directory`to your app root.
- `OK`

Now `scenemerge` should run automatically whenever you edit a `res/xml/_YOUR_FILENAME.xml` file,
creating/updating the merged MotionScene file `res/xml/YOUR_FILENAME.xml`.


This project was written on a Sunday evening. It is unlikely to have any major updates but feel free to make pull requests or whatever.
Hopefully MotionScene will someday have some kind built-in include/merge functionality and make this obsolete but this will have to do for now...


