# Fixture provenance

`dpkg-l.out` is the raw `dpkg -l` excerpt supplied by @EmperorArthur in
https://github.com/kellyjonbrazil/jc/issues/784. The reporter identified the
system as Ubuntu 26.04.1 LTS (resolute). It contains the single package row
provided in that report; no package rows or column padding were generated.
The terminal-truncated divider ending in `>` is preserved as reported.

This is a copy of the reporter's capture, not a new local capture. The previous
constructed `acpi`/`uWR` row was removed. Three-character status codes remain
covered by the existing Ubuntu 18.04 `dpkg-l-codes` edge-case fixture.
