# 2.4.1
- Minor improvement to handling IGNORED_LINES content.

# 2.4
- Published to pypi: https://pypi.org/project/motionscene-merger/
- Reverted default source directory to `res/xml` due to behaviour of Android Studio.

# 2.3
- Content within `<merge>` and `<injected>` tags are now unwrapped (same behaviour as `<MotionScene>`).

# 2.2
- <inject ../> tags are now ignored if they are on a line starting with '<!--' (commented out)

# 2.1
- Add commandline option `--resdir` so you can choose to store your source files
  in a different directory than the default `inject`.
  This must still be a direct child of the `res` directory.

# 2.0

- Transitive injections are now supported - you can inject content from a file
  which has injected content from some other file...etc.

### BREAKING CHANGES
- Source files are now placed in their own directory: `res/inject/`
- Source filename prefix changed from `_merge_src_` to `_`
- Merge tag signature has changed
  - from `__merge__(target_filename)`
  - to `<inject src="target_filename"/>`

### Migration from 1.0
- Move any files in `res/xml` with a filename starting `_merge_src_` to new directory `res/inject`.
- Replace `_merge_src_` with `_` in those filenames.
- Replace `__merge__(filename)` tags with `<inject src="filename"/>` in those files.
