# Scripts
Just some useful scripts.

### Python 3
#### test_fluent.py
Used for testing fluent translation files used in apps written in Rust.
Checks for duplicates, unsued and missing fluent keys (key = value).
```
usage: test_fluent.py [-h] [-i I] [-s S] [-e E] [-r R]

Validates the fluent translation files and checks if there are any missing fluent keys in the file based on source files.

optional arguments:
  -h, --help  show this help message and exit
  -i I        i18n directory path. Default: i18n
  -s S        Source directory path. Default: src
  -e E        Source file extension. Default: .rs
  -r R        Regex string for finding the fluent keys in the source files. Default: fl!."(.*?)"
```


## License
Code is distributed under MIT license.
