[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.streaming"></a>

# jc.streaming

## Table of Contents

* [jc.streaming](#jc.streaming)
  * [add_jc_meta](#jc.streaming.add_jc_meta)
  * [raise_or_yield](#jc.streaming.raise_or_yield)
  * [stream_error](#jc.streaming.stream_error)
  * [stream_success](#jc.streaming.stream_success)
  * [streaming_input_type_check](#jc.streaming.streaming_input_type_check)
  * [streaming_line_input_type_check](#jc.streaming.streaming_line_input_type_check)

jc - JSON Convert streaming utils

<a id="jc.streaming.add_jc_meta"></a>

### add_jc_meta

```python
def add_jc_meta(func: ~F) -> ~F
```

Decorator for streaming parsers to add `stream_success` and
`stream_error` objects. This simplifies the `yield` lines in the
streaming parsers.

With the decorator on parse():

    # successfully parsed line:
    yield output_line if raw else _process(output_line)

    # unsuccessfully parsed line:
    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, line)

Without the decorator on parse():

    # successfully parsed line:
    if raw:
        yield stream_success(output_line, ignore_exceptions)
    else:
        stream_success(_process(output_line), ignore_exceptions)

    # unsuccessfully parsed line:
    except Exception as e:
        yield stream_error(raise_or_yield(ignore_exceptions, e, line))

In all cases above:

    output_line:  (Dict)  successfully parsed line yielded as a dict

    e:            (BaseException)  exception object as the first value
                  of the tuple if the line was not successfully parsed.

    line:         (str)  string of the original line that did not
                  successfully parse.

    ignore_exceptions:  (bool)  continue processing lines and ignore
                        exceptions if `True`.

<a id="jc.streaming.raise_or_yield"></a>

### raise_or_yield

```python
def raise_or_yield(ignore_exceptions: bool, e: BaseException,
                   line: str) -> Tuple[BaseException, str]
```

Return the exception object and line string if `ignore_exceptions` is
`True`. Otherwise, re-raise the exception from the exception object with
an annotation.

<a id="jc.streaming.stream_error"></a>

### stream_error

```python
def stream_error(e: BaseException, line: str) -> Dict[str, Any]
```

Return an error `_jc_meta` field.

<a id="jc.streaming.stream_success"></a>

### stream_success

```python
def stream_success(output_line: Dict[str, Any],
                   ignore_exceptions: bool) -> Dict[str, Any]
```

Add `_jc_meta` object to output line if `ignore_exceptions=True`

<a id="jc.streaming.streaming_input_type_check"></a>

### streaming_input_type_check

```python
def streaming_input_type_check(data: Iterable[Union[str, bytes]]) -> None
```

Ensure input data is an iterable, but not a string or bytes. Raises
`TypeError` if not.

<a id="jc.streaming.streaming_line_input_type_check"></a>

### streaming_line_input_type_check

```python
def streaming_line_input_type_check(line: str) -> None
```

Ensure each line is a string. Raises `TypeError` if not.


