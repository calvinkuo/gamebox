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
`import pygame` is no longer required to be imported separately in gamebox projects,
as the key constants are now included in gamebox. PyGame still needs to be installed, however.

I would recommend using `from gamebox import *` to reduce the amount of boilerplate in student code,
so that all the methods and classes don't have to be called as `gamebox.foo`.  

#### Event loop
* The `pause` and `unpause` functions have been removed. Because `pause` stops the event loop, there is no way to check
  for user input and call `unpause` without an external timer, so providing these as built-in functions is misleading.
* The `freeze_loop` function replaces `pause` for win screens, game over screens, etc. where nothing else needs to be
  drawn to the screen and no more user input needs to be read.
* The `keys_loop` function (where a tick occurs only when a key is pressed or mouse is clicked) has been removed.
  Use `timer_loop` with an appropriate frame rate instead.

#### SpriteBox
The `from_image`, `from_color`, `from_circle`, `from_polygon`, and `from_text` functions are now methods within the
SpriteBox class.
```python
"""Filenames, URLs, and Surfaces"""
gamebox.from_image(x, y, filename_or_url)    # Old
SpriteBox.from_image(x, y, filename_or_url)  # New

"""Colors"""
gamebox.from_color(x, y, color, width, height)    # Old
SpriteBox.from_color(x, y, color, width, height)  # New

"""Circles"""
gamebox.from_circle(x, y, color, radius, *args)    # Old
SpriteBox.from_circle(x, y, color, radius, *args)  # New

"""Polygons"""
gamebox.from_polygon(x, y, color, *pts)    # Old
SpriteBox.from_polygon(x, y, color, *pts)  # New

"""Text"""
gamebox.from_text(x, y, text, fontsize, color, bold=False, italic=False)    # Old
SpriteBox.from_text(x, y, text, fontsize, color, bold=False, italic=False)  # New
```

Note that the `bold` and `ìtalic` parameters of `from_text` are now keyword-only arguments.
This makes it clearer whether bold or italics is desired and prevents accidental mix-ups.
```python
"""Italic text"""
gamebox.from_text(x, y, text, size, color, True, False)    # Old
SpriteBox.from_text(x, y, text, size, color, italic=True)  # New

"""Bold text"""
gamebox.from_text(x, y, text, size, color, False, True)  # Old
SpriteBox.from_text(x, y, text, size, color, bold=True)  # New

"""Bold italic text"""
gamebox.from_text(x, y, text, size, color, True, True)                # Old
SpriteBox.from_text(x, y, text, size, color, italic=True, bold=True)  # New
```

The `box.draw(camera)` method in the SpriteBox class has been removed,
to reinforce the "there should only be one way to do it" philosophy. Instead, call `camera.draw(box)`.
This also removes the ability to draw a SpriteBox directly onto a Surface.

The `box.mousehover` and `box.mouseclick` properties have been added to make checking for mouse actions easier.
```python
if box.mousehover:
    ...  # do something if the mouse is hovering over this box

if box.mouseclick:
    ...  # do something if the mouse is clicking this box
```

#### Camera
The Camera constructor now has a default size of 800 &times; 600 pixels.
The `full_screen` parameter is now a keyword-only argument.
```python
"""800 &times; 600 resolution, window"""
gamebox.Camera(800, 600)  # Old
Camera()                  # New

"""800 &times; 600 resolution, full-screen"""
gamebox.Camera(800, 600, True)  # Old
Camera(full_screen=True)        # New

"""1920 &times; 1080 resolution, full-screen"""
gamebox.Camera(1920, 1080, True)      # Old
Camera(1920, 1080, full_screen=True)  # New
```

The `camera.draw(thing)` method can no longer be called to print a Surface or a string directly.
Instead, create the equivalent SpriteBox and call `camera.draw(box)`.
```python
"""If `thing` is a Surface"""
camera.draw(surface, x, y)                        # Old
camera.draw(SpriteBox.from_image(x, y, surface))  # New

"""If `thing` is a string"""
camera.draw(text, x, y, size, color)                       # Old
camera.draw(SpriteBox.from_text(x, y, text, size, color))  # New
```

#### Keyboard
Keys are now represented using an IntEnum class. This allows for autocomplete to suggest the `K_*` constant names,
while still allowing for the descriptive names to be used.
```python
"""Old"""
pygame.K_PERIOD in keys        # legacy
gamebox.is_pressing('period')  # Game Engine

"""New"""
Key('.').is_pressed()
Key.K_PERIOD.is_pressed()
Key('period').is_pressed()
```

[PyCharm doesn't currently warn in the IDE for invalid attributes of an Enum](https://youtrack.jetbrains.com/issue/PY-21371/Unresolved-reference-false-negative-Invalid-Enum-members-is-not-detected),
unfortunately, but it will still throw an AttributeError at runtime though.

Entering an invalid identifier using the constructor will show a custom error message:
```
ValueError: 'coma' is not a valid key name. Did you mean: 'comma'?
Check https://www.pygame.org/docs/ref/key.html#key-constants-label for a full list
```

The static method `Key.is_any_pressed()` can be used to check if *any* key is being pressed:
```python
"""Old"""
if keys:          # legacy
    ...
if gamebox.keys:  # Game Engine
    ...

"""New"""
if Key.is_any_pressed():
    ...
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
