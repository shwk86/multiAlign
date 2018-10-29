# multiAlign

[[Features]](#features) [[Usage]](#usage) [[Configuration]](#configuration) [[Available settings]](#available-settings) [[Installation]](#installation) [[License]](#license)

I tried some of the various alignment plugins already available for [Sublime Text](https://www.sublimetext.com) but I was not satisfied with their capabilities. For example I wanted to align multiple characters in the same lines and be able to align inline comments and keywords with a more complex configuration of how to align. In the end I decided to write my own plugin from scratch to implement all the capabilities I would like to have. As the implementation is pretty flexible and can easily be configured to the user's needs I would like to share it with everyone who is interested in using it.

I developed the plugin for Sublime Text 3 on Windows but I it should also work on Linux/OS X and in Sublime Text 2.

------------------------------------------

## Features

- Stepwise alignment of multiple alignment characters in multiple lines around multiple cursors across multiple indentation levels (so I guess the name multiAlign fits well :sweat_smile:).
- The plugin can be called multiple times in the same rows to align multiple alignment characters in them.
- Alignment characters can have a specific number of mandatory spaces left and right of them.
- Alignment characters can have optional prefixes which are considered during the alignment.
- Alignment characters can consist of multiple characters (keywords can be aligned as well).
- Alignment characters can be limited to specific scopes (programming languages).
- Alignment characters can be set up to exclude specific scopes (programming languages).
- Alignment characters can have conditions when they are considered valid for alignment.

**Important**: Alignment characters match without surrounding spaces thus aligning at keywords might produce matches in substrings of you code. Please make sure to define [strict limits](#available-settings) for keyword alignment characters!

[[top]](#multialign)

------------------------------------------

## Usage

Place one or multiple cursors where you want to align your code and press:

        (Windows/Linux): (Ctrl+Alt+A)

        (OS X):          (Ctrl+Cmd+A)

**Please note**

- If multiple cursors have been set they will all get a common alignment.
- If multiple alignment characters can be aligned each keystroke aligns the first in line which is not aligned.
- If the alignment character is at the beginning of the line the number of spaces left of it is not changed.
- If the alignment character is at the end of the line no space will be added right of it.

**Here is how it works**

- An overall regular expression (overall regex) containing all alignment characters is compiled.
- With this overall regex the row with the main cursor (main row) is parsed to get the reference list of alignment characters (main alignment characters) which could potentially be aligned.
- For all cursors the cursor row is parsed with the overall regex and compared to the main alignment characters.
- The alignment characters have to be in the same order like in the main row to be considered valid for alignment.
- If an alignment character is invalid the alignment characters right of it are also invalid.
- If at least one valid alignment character was detected in the cursor row the rows above and below are also checked until at least one condition is true:
    - The indentation level changes (based on the individual cursor indentation level).
    - An empty line is detected (can be turned off - see [Configuration](#configuration)).
    - No valid alignment character can be found.
    - Reached the beginning or end of file.
- With all alignment characters and rows potentially to be aligned being identified, the common alignment positions (target positions) are determined.
- For each main alignment character the position of the alignment character in all rows potentially getting aligned is checked.
- If the alignment character is already aligned correctly in all identified rows the next main alignment character is checked.
- If at least in one row the alignment is not positioned correctly the current main alignment character is getting aligned in all identified rows.

[[top]](#multialign)

------------------------------------------

## Configuration

multiAlign comes with a [default configuration](#default-settings) of some basic alignment characters but the user can overwrite these settings using either a seperate [plugin settings file](#plugin-settings-file) (`multiAlign.sublime-settings`) or entering them in the general [Sublime Text settings file](#sublime-text-settings-file) (`Preferences.sublime-settings`).

The order of importance is:

1. [Plugin settings file](#plugin-settings-file)
2. [Sublime Text settings file](#sublime-text-settings-file)
3. [Default settings](#default-settings)

Please go to [available settings](#available-settings) for more information on the individual settings.

------------------------------------------

### Default settings

Below you can find the default setting that come with the multiAlign plugin. As I am currently working in Python and Fortran I only added spcific setting for those two programming languages but you can easily set up your own alignment characters in the [plugin settings file](#plugin-settings-file) or the [Sublime Text settings file](#sublime-text-settings-file).

```
{
    "break_at_empty_lines": true,
    "break_at_non_matching_lines": true,
    "align_chars": [
        {
            'char':            'import',
            'alignment':       'right',
            'spaces_left':     1,
            'spaces_right':    1,
            'is_in_scope':     ['source.python'],
            'is_left_of_char': ['from']
        },
        {
            'char':            'as',
            'alignment':       'right',
            'spaces_left':     1,
            'spaces_right':    1,
            'is_in_scope':     ['source.python'],
            'is_left_of_char': ['import']
        },
        {
            'char':         '#',
            'alignment':    'right',
            'spaces_left':  3,
            'spaces_right': 1,
            'is_in_scope':  ['source.python']
        },
        {
            'char':         '::',
            'alignment':    'right',
            'spaces_left':  1,
            'spaces_right': 1,
            'is_in_scope':  ['source.modern-fortran', 'source.fixedform-fortran']
        },
        {
            'char':             'intent',
            'alignment':        'right',
            'spaces_left':      1,
            'spaces_right':     0,
            'is_in_scope':      ['source.modern-fortran', 'source.fixedform-fortran'],
            'is_right_of_char': ['::']
        },
        {
            'char':         '&',
            'alignment':    'right',
            'spaces_left':  1,
            'spaces_right': 0,
            'is_in_scope':  ['source.modern-fortran', 'source.fixedform-fortran']
        },
        {
            'char':         '=>',
            'alignment':    'right',
            'spaces_left':  1,
            'spaces_right': 1
        },
        {
            'char':         '=',
            'alignment':    'right',
            'spaces_left':  1,
            'spaces_right': 1,
            'prefixes':     ['+', '-', '*', '/', '.', '%', '<', '>', '!', '=', '~', '&', '|']
        },
        {
            'char':            ':',
            'alignment':       'left',
            'spaces_left':     0,
            'spaces_right':    1,
            'not_enclosed_by': ['[]']
        }
    ]
}
```

[[top]](#multialign)

------------------------------------------

### Plugin settings file

- Go to your package directory through Sublime Text:

        (Windows/Linux): Preferences -> Browse Packages...

        (OS X):          Sublime Text -> Preferences -> Browse Packages...

- Go to the `User` directory and create or edit the `multiAlign.sublime-settings` file.

- Add your custom configuration using the keys `break_at_empty_lines` or `align_chars` for the setting you want to overwrite.

```
{
    "break_at_empty_lines": true,
    "break_at_non_matching_lines": true,
    "align_chars": [
        {
            "char": "=",
            "alignment":       "right",
            "spaces_left":     1,
            "spaces_right":    1
        }
    ]
}
```


[[top]](#multialign)

------------------------------------------

### Sublime Text settings file

- Open the general `Preferences.sublime-settings` file through Sublime Text:

        (Windows/Linux): Preferences -> Settings...

        (OS X):          Sublime Text -> Preferences -> Settings...

- Add your custom configuration using the keys `mulitAlign_break_at_empty_lines` or `mulitAlign_align_chars` for the setting you want to overwrite.

```
{
    "multiAlign_break_at_empty_lines": true,
    "multiAlign_break_at_non_matching_lines": true,
    "multiAlign_align_chars": [
        {
            "char": "=",
            "alignment":       "right",
            "spaces_left":     1,
            "spaces_right":    1
        }
    ]
}
```

[[top]](#multialign)

------------------------------------------

## Available settings

**Top level settings**

**`break_at_empty_lines: <bool>` / `multiAlign_break_at_empty_lines: <bool>`**

Boolean value specifying whether the alignment check process should break at empty lines. If set to `false` the plugin continues to check lines after empty lines as long as they have the same indentation level.

------------------------------------------

**`break_at_non_matching_lines: <bool>` / `multiAlign_break_at_non_matching_lines: <bool>`**

Boolean value specifying whether the alignment check process should break at lines without a match of the alignment character to be aligned. If set to `false` the the plugin continues to check lines after empty lines as long as they have the same indentation level.

------------------------------------------

**`align_chars: <list>` / `multiAlign_align_chars: <list>`**

List of dictionary objects spcifying the configuration of the individual alignment characters. As the configuration of the alignment characters is essential for the plugin to work properly I will explain the individual settings in detail.

------------------------------------------

<a name="list_of_settings"></a>
**List of `align_chars` settings**

- [`char:              <str>`](#char)
- [`alignment:         <str>`](#alignment)
- [`spaces_left:       <int>`](#spaces_left)
- [`spaces_right:      <int>`](#spaces_right)
- [`prefixes:          <list>`](#prefixes)
- [`is_in_scope:       <list>`](#is_in_scope)
- [`not_in_scope:      <list>`](#not_in_scope)
- [`is_enclosed_by:    <list>`](#is_enclosed_by)
- [`not_enclosed_by:   <list>`](#not_enclosed_by)
- [`is_left_of_char:   <list>`](#is_left_of_char)
- [`not_left_of_char:  <list>`](#not_left_of_char)
- [`is_right_of_char:  <list>`](#is_right_of_char)
- [`not_right_of_char: <list>`](#not_right_of_char)

Except for the basic `char` setting all other settings of an alignment character configuration are optional. If not configured for the alignment character the following default values will be used for the alignment:

```
default_settings = {
    "alignment":         "right",
    "spaces_left":       1,
    "spaces_right":      1,
    "prefixes":          [],
    "is_in_scope":       [],
    "not_in_scope":      [],
    "not_enclosed_by":   [],
    "not_left_of_char":  [],
    "not_right_of_char": [],
    "is_enclosed_by":    [],
    "is_left_of_char":   [],
    "is_right_of_char":  []
}
```

**Example**

```
{
    "align_chars": [
        {
            'char':              'bar',
            'alignment':         'right',
            'spaces_left':       4,
            'spaces_right':      1,
            'prefixes':          ['+', '-', 'foo'],
            'is_in_scope':       ['source.python'],
            'not_in_scope':      ['source.perl'],
            'not_enclosed_by':   ['()', ('[', ']'), ['{', '}']],
            'not_left_of_char':  ['baz'],
            'not_right_of_char': ['bar'],
            'is_enclosed_by':    [('<', '>'), ';;'],
            'is_left_of_char':   ['#'],
            'is_right_of_char':  ['baz']
        }
    ]
}
```

An now here is the explanation what the individual setting are used for and what you have to consider when using them:

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="char"></a>
**`char: <str>`**

The character where the alignment should be made. To be precise the `char` can consist of multiple characters so it is possible to align keyword for example. As `char` is matched without spaces please consider adding mandatory spaces to `char` for keyword alignment characters and define strict limits to avoid unexpected matches in substrings of your code.

**Example**

> `'char': '='`

_before alignment_
```
    foobar= 1
    baz =2
```

_after alignment_
```
    foobar = 1
    baz    = 2
```

**Example**

> `'char': 'import'`

_before alignment_
```
    from os import path
    from sys   import exit
```

_after alignment_
```
    from os  import path
    from sys import exit
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="alignment"></a>
**`alignment: <str>`**

The direction where the alignment character should be positioned after alignment.

-`left`: Places the alignment character to the left and fills in spaces right of it in order to align the characters following the alignment character. It is for example used for `:` alignment in the [default setting](#default-settings).


**Example** (`'char': ':'`)

> `'alignment': 'left'`

_before alignment_
```
    foobar  : 1
    baz :  2
```

_after 'left' alignment_
```
    foobar: 1
    baz:    2
```

-`right`: Places the alignment character to the right and fills in spaces left of it in order to align the characters following the alignment character. It is for example used for `=` alignment in the [default setting](#default-settings).

**Example** (`'char': '='`)

> `'alignment': 'right'`

_before alignment_
```
    foobar= 1
    baz =2
```

_after 'right' alignment_
```
    foobar = 1
    baz    = 2
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="spaces_left"></a>
**`spaces_left: <int>`**

An integer number specifying the minimum number of spaces that should be left of the alignment character when the alignment has been completed. The actual number of spaces left of the alignment character might be higher depending on the `alignment` and position of corresponding alignment character in the other lines getting aligned.

**Example** (`'char': '='`)

> `'spaces_left': 0`

_before alignment_
```
    foobar= 1
    baz =2
```

_after alignment_
```
    foobar= 1
    baz   = 2
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="spaces_right"></a>
**`spaces_right: <int>`**

An integer number specifying the minimum number of spaces that should be right of the alignment character when the alignment has been completed. The actual number of spaces right of the alignment character might be higher depending on the `alignment` and position of corresponding alignment character in the other lines getting aligned.

**Example** (`'char': '='`)

> `'spaces_right': 0`

_before alignment_
```
    foobar= 1
    baz =2
```

_after alignment_
```
    foobar =1
    baz    =2
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="prefixes"></a>
**`prefixes: <list>`**

A list of strings containing the potential prefixes the alignment character might have. If a prefix exists it will be treated as if it was part of the `char` during the alignment process. The prefixes can consist of multiple characters in case there is a use case for that.

**Example** (`'char': '='`)

> `'prefixes': ['+', '-']`

_before alignment_
```
    foobar+= 1
    baz =2
```

_after alignment_
```
    foobar += 1
    baz     = 2
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="is_in_scope"></a>
**`is_in_scope: <list>`**

A list of strings specifying the programming languages the alignment character should be applied to. The strings have to match the [scope](https://www.sublimetext.com/docs/3/scope_naming.html) in Sublime Text. To determine the scope place your cursor in a corresponding file and press:

        (Windows/Linux): (Ctrl+Alt+Shift+P)

        (OS X):          (Ctrl+Shift+P)

If the list is empty the alignment character is used for every alignment regardless of the current programming language. If the list `is_in_scope` is not empty and the current scope is not one of them the alignment character will not even be added to the [overall regex](#usage). As a result the same character can have different alignment character settings for different programming languages.

**Example**

> `'is_in_scope': ['source.python', 'source.modern-fortran', 'source.fixedform-fortran']`

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="not_in_scope"></a>
**`not_in_scope: <list>`**

A list of strings specifying the programming languages the alignment character should not be applied to. The strings have to match the [scope](https://www.sublimetext.com/docs/3/scope_naming.html) in Sublime Text. To determine the scope place your cursor in a corresponding file and press:

        (Windows/Linux): (Ctrl+Alt+Shift+P)

        (OS X):          (Ctrl+Shift+P)

If the list is empty the alignment character is used for every alignment regardless of the current programming language. If the list `not_in_scope` is not empty and the current scope is one of them the alignment character will not even be added to the [overall regex](#usage). As a result the application of the alignment character can be suppressed for specific programming languages only.

**Example**

> `'not_in_scope': ['source.perl']`

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="is_enclosed_by"></a>
**`is_enclosed_by: <list>`**

A list of indexable data types (string, list or tuple) specifying characters the alignment character has to be enclosed by to be considered valid. The feature is intended to be used to **enforce** the alignment character being enclosed by brackets. The first index [0] of the list element is considered the opening bracket and the second index [1] is considered the closing bracket.

For each potential match of the alignment character the plugin will parse the string left of the alignment character and determine the bracket level (+1 for opening and -1 for closing bracket characters). In case for both the opening and the closing bracket the same character is defined the plugin will just check if the opening/closing bracket character is at least once left and right of the alignment character.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': '='`)

> `'is_enclosed_by': ['()', ('[', ']'), ['{', '}']]`

_before alignment_
```
    foobar= foo(bar   =1)
    baz =bar(foo=  2)
```

_after alignment_
```
    foobar= foo(bar = 1)
    baz =bar(foo    = 2)
```

**Example** (`'char': '='`)

> `'is_enclosed_by': [';;']`

_before alignment_
```
    ;foo;bar= foo;(bar =1)
    baz =bar;(foo= 2);
```

_after alignment_
```
    ;foo;bar      = foo;(bar =1)
    baz =bar;(foo = 2);
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="not_enclosed_by"></a>
**`not_enclosed_by: <list>`**

A list of indexable data types (string, list or tuple) specifying characters the alignment character must not be enclosed by to be considered valid. The feature is intended to be used to **suppress** the alignment character being enclosed by brackets. The first index [0] of the list element is considered the opening bracket and the second index [1] is considered the closing bracket.

For each potential match of the alignment character the plugin will parse the string left of the alignment character and determine the bracket level (+1 for opening and -1 for closing bracket characters). In case for both the opening and the closing bracket the same character is defined the plugin will just check if the opening/closing bracket character is at least once left and right of the alignment character.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': '='`)

> `'not_enclosed_by': ['()', ('[', ']'), ['{', '}']]`

_before alignment_
```
    foobar(bar =1)= foo
    baz(foo= 2) =bar
```

_after alignment_
```
    foobar(bar =1) = foo
    baz(foo= 2)    = bar
```

**Example** (`'char': '='`)

> `'not_enclosed_by': [';;']`

_before alignment_
```
    ;foo;bar= foo;(bar =1)
    baz; =bar(foo= 2)
```

_after alignment_
```
    ;foo;bar= foo;(bar = 1)
    baz;               = bar(foo= 2)
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="is_left_of_char"></a>
**`is_left_of_char: <list>`**

A list of string objects specifying characters which **must be** to the left of the alignment character in the same line to consider the alignment character valid. Those strings can consist of multiple characters in order to check for keywords. In case the list has multiple entries every single entry has to be left of the alignment character. It is intended to be used to define stricter limits when aligning at keywords.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': 'import'`)

> `'is_left_of_char': ['from']`

_before alignment_
```
    # import math
    from os import path
    from sys   import exit
```

_after alignment_
```
    # import math
    from os  import path
    from sys import exit
```

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="not_left_of_char"></a>
**`not_left_of_char: <list>`**

A list of string objects specifying characters which **must not be** to the left of the alignment character in the same line to consider the alignment character valid. Those strings can consist of multiple characters in order to check for keywords. In case the list has multiple entries every single entry has to be left of the alignment character. It is intended to be used to define stricter limits when aligning at keywords.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': ':'`)

> `'not_left_of_char': ['[']`

_before alignment_
```
    foo[0,:]   : bar
    baz: [:, 3]
    foobar: 2
```

_after alignment_
```
    foo[0,:]   : bar
    baz:    [:, 3]
    foobar: 2
```

_**Note:** You might have expected all lines to get aligned but through_ `'not_left_of_char': 'as'` _in the third line the alignment character is invalid (see getp**as**s). As mentioned before you could consider adding mandatory spaces `'not_left_of_char': ' as '` _to avoid matches in substrings._

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="is_right_of_char"></a>
**`is_right_of_char: <list>`**

A list of string objects specifying characters which **must be** to the right of the alignment character in the same line to consider the alignment character valid. Those strings can consist of multiple characters in order to check for keywords. In case the list has multiple entries every single entry has to be right of the alignment character. It is intended to be used to define stricter limits when aligning at keywords.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': 'intent'`)

> `'is_right_of_char': ['::']`

_before alignment_
```
    integer,   intent(in)  :: cnt
    real, intent(inout) ::  value
```

_after alignment_
```
    integer, intent(in)  :: cnt
    real,    intent(inout) ::  value
```
_**Note:** `::` would get aligned on the next keystroke if configured as alignment character._

[[list of settings]](#list_of_settings)

------------------------------------------

<a name="not_right_of_char"></a>
**`not_right_of_char: <list>`**

A list of string objects specifying characters which **must not be** to the right of the alignment character in the same line to consider the alignment character valid. Those strings can consist of multiple characters in order to check for keywords. In case the list has multiple entries every single entry has to be right of the alignment character. It is intended to be used to define stricter limits when aligning at keywords.

_Please note: This check is applied to matches of the [overall regex](#usage) thus it consumes a potential alignment character._

**Example** (`'char': 'import'`)

> `'not_right_of_char': ['as']`

_before alignment_
```
    from datetime import time
    from os import path
    from sys import argv as arguments
```

_after alignment_
```
    from datetime import time
    from os       import path
    from sys import argv as arguments
```

[[top]](#multialign) [[list of settings]](#list_of_settings)

------------------------------------------

## Installation

**Using the Package Control plugin:**

This is the easiest way and will automatically keep multiAlign up to date with the latest version.

- Install the [Package Control](https://packagecontrol.io/installation) plugin (if not already installed).

- Open the Command Palette (`Ctrl+Shift+P`) in Sublime Text and select:

        Package Control: Install Package...

        multiAlign

**Using Git:**

- Go to your package directory through Sublime Text:

        (Windows/Linux): Preferences -> Browse Packages...

        (OS X):          Sublime Text -> Preferences -> Browse Packages...

- Clone the [multiAlign](git://github.com/shwk86/multiAlign.git) repository into your package directory.

        git clone git://github.com/shwk86/multiAlign.git

**Manual Download:**

- Browse to the [multiAlign](https://github.com/shwk86/multiAlign) plugin on GitHub.

- Download the repository as a [zip file](https://github.com/shwk86/multiAlign/archive/master.zip).

- Go to your package directory through Sublime Text:

        (Windows/Linux): Preferences -> Browse Packages...

        (OS X):          Sublime Text -> Preferences -> Browse Packages...

- Unzip the downloaded resposiory in your package directory.

- Remove the Git branch suffix in the directory name if you like to.

[[top]](#multialign)

------------------------------------------

## License

    MIT License

    Copyright (c) 2018 Jens Gorny

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

[[top]](#multialign)
