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
