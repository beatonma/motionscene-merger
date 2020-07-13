### scenemerge

File injection tool to allow reuse of ConstraintSet definitions in multiple MotionScenes.

## In your environment:

    git clone https://github.com/motionscene-merger
    python setup install

    scenemerge .


## Creating merge instructions
In your `res/xml` directory:
- Create an XML file with any content you want to be able to inject into other files. This may be a full MotionScene, or some smaller fragment such as a KeyFrameSet or ConstraintSet. The filename must start with `_merge_src_` e.g. `res/xml/_merge_src_my_injectable_motionscene.xml`

- Create a template for your parent MotionScene. Again, the filename must start with `_merge_src_` e.g. `res/xml/_merge_src_my_parent_motionscene.xml`
  - add a line in this file with `__merge__(source_filename)` e.g:

    ```
        <?xml version="1.0" encoding="utf-8"?>
        <MotionScene
            xmlns:android="http://schemas.android.com/apk/res/android"
            xmlns:motion="http://schemas.android.com/apk/res-auto">
    
            <!-- Any other content here -->
        
            __merge__(_merge_src_my_injectable_motionscene)
    
            <!-- Any other content here -->
        
        </MotionScene>
    ```

Now when you run `scenemerge` the content from the MotionScene in `_merge_src_my_injectable_motionscene.xml` will be copied in place into a new MotionScene file called `my_parent_motionscene.xml`. The `<MotionScene...></MotionScene>` tags will not be copied - only the content between them.

Please check the files in `test/example_root_dir/res/xml` for example source files.

## Android Studio File Watcher
- Install the `File Watcher` plugin for Android Studio via `Settings -> Plugins`.
- Restart and open `Settings -> Tools -> File Watchers`, then click the `+` to create a new Watcher.
- Set `File type` to XML.
- Create a Scope with a pattern like `file[app]:src/**/res/xml/_merge_src_*.xml`
- Set `Program` to `scenemerge` in your environment. e.g. env/Scripts/scenemerge
- Set `Arguments` to `.`
- Set `Working directory`to your app root.
- `OK`

Now `scenemerge` should run automatically whenever you edit a `_merge_src_YOUR_FILENAME.xml` file,
creating/updating the merged MotionScene file `YOUR_FILENAME.xml`.


This project was written on a Sunday evening. It is unlikely to have any major updates but feel free to make pull requests or whatever.
Hopefully MotionScene will someday have some kind built-in include/merge functionality and make this obsolete but this will have to do for now...
