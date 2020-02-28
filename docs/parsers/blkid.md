# jc.parsers.blkid
jc - JSON CLI output utility blkid Parser

Usage:

    specify --blkid as the first argument if the piped input is coming from blkid

Compatibility:

    'linux'

Examples:

    $ blkid | jc --blkid -p
    []

    $ blkid | jc --blkid -p -r
    []

## info
```python
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "device":               string,
        "uuid":                 string,
        "type":                 string,
        "usage":                string,
        "part_entry_scheme":    string,
        "part_entry_type":      string,
        "part_entry_flags":     string,
        "part_entry_number":    integer,
        "part_entry_offset":    integer,
        "part_entry_size":      integer,
        "part_entry_disk":      string
        "id_fs_uuid":           string,
        "id_fs_uuid_enc":       string,
        "id_fs_type":           string,
        "id_fs_usage":          string,
        "id_part_entry_scheme": string,
        "id_part_entry_type":   string,
        "id_part_entry_flags":  string,
        "id_part_entry_number": integer,
        "id_part_entry_offset": integer,
        "id_part_entry_size":   integer,
        "id_part_entry_disk":   string
      }
    ]

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of dictionaries. Raw or processed structured data.

