# gamebox
 Rewrite of the gamebox library used at UVA

The goal of this project is to modernize gamebox using [type annotations](https://docs.python.org/3/library/typing.html)
and [managed attributes](https://docs.python.org/3/howto/descriptor.html#managed-attributes) to create a more idiomatic
and maintainable library that takes advantage of modern Python syntax.


## Why make these changes?
PyCharm, the IDE used in CS 111x, can provide warnings when functions are called with parameters of the wrong type.
Additionally, it can autocomplete the names of class/instance methods and properties, as well as infer their types.

As Python is a dynamic language, to take full advantage of these features, libraries must provide that information
in the correct format. Python 3.5 introduced type hints, which allow variable types, argument types, and return types 
to be specified explicitly.

By adding full type hints to the library, student code will display warnings within the IDE if functions are called with
incorrect parameters, even when the students do not use type annotations in their own code. Similarly, when attributes
are defined using the managed attribute syntax, the IDE will also be able to determine the types of them, and warn if
they are used incorrectly. This matches the behavior that students would expect from the standard library methods that
they are familiar with.


## Contents
A completely overhauled version of gamebox:
* [gamebox.py](gamebox.py) (compatible with Python 3.10+)

This repository also contains drop-in replacements for previous versions of the library:
* [gamebox_compat_ge.py](gamebox_compat_ge.py) is a drop-in replacement for the UVA Game Engine, which was used in the
  Fall 2022 semester (compatible with Python 3.7+)
* Drop-in replacements for the version of gamebox.py used from Spring 2018 through Summer 2022:
  * [gamebox_compat.py](gamebox_compat.py) (compatible with Python 3.9+)
  * [gamebox_compat_37.py](gamebox_compat_37.py) (compatible with Python 3.7+)
* [gamebox_compat_uni.py](gamebox_compat_uni.py) is a universal drop-in replacement for both the UVA Game Engine and
  gamebox.py (compatible with Python 3.7+)
* [gamebox_legacy.py](gamebox_legacy.py) is the legacy version of gamebox used from Spring 2018 through Summer 2022
  (compatible with both Python 2 and Python 3)

### Sample projects

* [sample.py](sample.py), an example project using gamebox rewrite
* [sample_ge.py](sample_ge.py), an example project using the UVA Game Engine
* [sample_legacy.py](sample_legacy.py), an example project using legacy gamebox


## History
gamebox was originally written by Luther Tychonievich for the CS 111x course during the Fall 2015 semester,
when the course switched from using Java to Python. At the time, the latest version of Python was 3.4.3.
In Spring 2018, sound and font support were removed from the library, and it remained unchanged until Fall 2022,
when several changes were made by Adam Dirting, and it was renamed the UVA Game Engine.


## Changelog
### Changes between gamebox and the rewrite
#### Imports
`import pygame` is no longer required in gamebox projects, as the key constants are now included in gamebox.

#### Event loop
* The `pause` and `unpause` functions have been removed. Because `pause` stops the event loop, there is no way to check
  for user input and call `unpause` without an external timer, so providing these as built-in functions is misleading.
* The `freeze_loop` function replaces `pause` for win screens, game over screens, etc. where nothing else needs to be
  drawn to the screen and no more user input needs to be read.
* The `keys_loop` function (where a tick occurs only when a key is pressed or mouse is clicked) has been removed.
  Use `timer_loop` with an appropriate frame rate instead.

#### Drawing
The `from_image`, `from_color`, `from_circle`, `from_polygon`, and `from_text` functions are now methods within the
SpriteBox class.
* Old:
  * `gamebox.from_image(x, y, filename_or_url)`
  * `gamebox.from_color(x, y, color, width, height)`
  * `gamebox.from_circle(x, y, color, radius, *args)`
  * `gamebox.from_polygon(x, y, color, *pts)`
  * `gamebox.from_text(x, y, text: str, fontsize, color, bold=False, italic=False)`
* New:
  * `gamebox.SpriteBox.from_image(x, y, filename_or_url)`
  * `gamebox.SpriteBox.from_color(x, y, color, width, height)`
  * `gamebox.SpriteBox.from_circle(x, y, color, radius, *args)`
  * `gamebox.SpriteBox.from_polygon(x, y, color, *pts)`
  * `gamebox.SpriteBox.from_text(x, y, text: str, fontsize, color, bold=False, italic=False)`

The `box.draw(camera)` method in the SpriteBox class has been removed,
to reinforce the "there should only be one way to do it" philosophy. Instead, call `camera.draw(box)`.
This also removes the ability to draw a SpriteBox directly onto a Surface.

The `camera.draw(thing)` method can no longer be called to print a Surface or a string directly.
Instead, create the equivalent SpriteBox and call `camera.draw(box)`.
* If `thing` is a Surface:
  * Old: `camera.draw(surface, x, y)`
  * New: `camera.draw(gamebox.SpriteBox.from_image(x, y, surface))`
* If `thing` is a string:
  * Old: `camera.draw(text, x, y, size, color)`
  * New: `camera.draw(gamebox.SpriteBox.from_text(x, y, text, size, color))`

The `bold` and `ìtalic` parameters of `gamebox.from_text()` are now keyword-only arguments.
This makes it clearer which one is being called and prevents accidental mix-ups.
* Italic text:
  * Old: `gamebox.from_text(x, y, text, size, color, True, False)`
  * New: `gamebox.SpriteBox.from_text(x, y, text, size, color, italic=True)`
* Bold text:
  * Old: `gamebox.from_text(x, y, text, size, color, False, True)`
  * New: `gamebox.SpriteBox.from_text(x, y, text, size, color, bold=True)`
* Bold italic text:
  * Old: `gamebox.from_text(x, y, text, size, color, True, True)`
  * New: `gamebox.SpriteBox.from_text(x, y, text, size, color, italic=True, bold=True)`

#### Keyboard
Keys are now represented using an IntEnum class. This allows for autocomplete to suggest the `K_*` constant names,
while still allowing for the descriptive names to be used.
* Old:
  * `pygame.K_PERIOD in keys` (legacy)
  * `gamebox.is_pressing('period')` (Game Engine)
* New:
  * `gamebox.Key.K_PERIOD.is_pressed()`
  * `gamebox.Key('period').is_pressed()`
  * `gamebox.Key('.').is_pressed()`

[PyCharm doesn't currently warn in the IDE for invalid attributes of an Enum](https://youtrack.jetbrains.com/issue/PY-21371/Unresolved-reference-false-negative-Invalid-Enum-members-is-not-detected),
unfortunately, but it will still throw an AttributeError at runtime though.

Entering an invalid identifier using the constructor will show a custom error message:
```
ValueError: 'coma' is not a valid key name. Did you mean: 'comma'?
Check https://www.pygame.org/docs/ref/key.html#key-constants-label for a full list
```

#### Internal changes
* Rendered text is now cached. This prevents memory leaks when `gamebox.from_text()` is called continuously.
* Various refactors.


### Changes between gamebox and UVA Game Engine
* Drops support for Python 2
* Wraps exception returned when a filepath/URL for an image is incorrect instead of always raising a `urllib` error
* Adds `keys` and `key_constants` as public global variables
* Adds a new method `is_pressing(key)`
* Changes the expected signature of the `callback` parameter in `timer_loop(fps, callback, limit=None)`
  from `callback(keys)` to `callback()`

This last change is a breaking change that affects games and examples made with earlier versions of gamebox.
[gamebox_compat_uni.py](gamebox_compat_uni.py) inspects the function signature of `callback` and provides the `keys`
parameter only if needed, so it is backwards-compatible with both versions.
