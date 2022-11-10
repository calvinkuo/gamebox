# -*- coding: utf-8 -*-
"""A library file for simplifying pygame interaction.
You MUST place this file in the same directory as your game py files."""

from __future__ import annotations

import difflib
import enum
import functools
import os.path
import sys
import urllib.parse
import urllib.request
from collections.abc import Callable, Sequence
from typing import Any, NamedTuple, NoReturn

import pygame
from pygame import Surface

pygame.init()


__all__ = [
    'Key',
    'Camera',
    'SpriteBox',
    'load_sprite_sheet',
    'timer_loop',
    'freeze_loop',
    'stop_loop'
]

# Typing hints copied from pygame._common
_RgbaOutput = tuple[int, int, int, int]
_ColorValue = pygame.Color | int | str | tuple[int, int, int] | list[int] | _RgbaOutput
_Coordinate = tuple[float, float] | Sequence[float]  # pygame._common._Coordinate, but without pygame.math.Vector2


class _ImageKey(NamedTuple):
    """Used as a dictionary key for retrieving cached images."""
    key: str
    flip: bool = False
    w: int = 0
    h: int = 0
    angle: int = 0


class _TextKey(NamedTuple):
    """Used as a dictionary key for retrieving cached rendered text."""
    text: str
    fontsize: int
    color: _ColorValue
    bold: bool
    italic: bool


class Key(enum.IntEnum):
    """A key on the keyboard.

    :example:

    To check if the space bar is pressed, you can use ``gamebox.Key.K_SPACE.is_pressed()``,
    ``gamebox.Key(' ').is_pressed()``, or ``gamebox.Key('space').is_pressed()``."""
    K_BACKSPACE = pygame.K_BACKSPACE
    K_TAB = pygame.K_TAB
    K_CLEAR = pygame.K_CLEAR
    K_RETURN = pygame.K_RETURN
    K_PAUSE = pygame.K_PAUSE
    K_ESCAPE = pygame.K_ESCAPE
    K_SPACE = pygame.K_SPACE
    K_EXCLAIM = pygame.K_EXCLAIM
    K_QUOTEDBL = pygame.K_QUOTEDBL
    K_HASH = pygame.K_HASH
    K_DOLLAR = pygame.K_DOLLAR
    K_AMPERSAND = pygame.K_AMPERSAND
    K_QUOTE = pygame.K_QUOTE
    K_LEFTPAREN = pygame.K_LEFTPAREN
    K_RIGHTPAREN = pygame.K_RIGHTPAREN
    K_ASTERISK = pygame.K_ASTERISK
    K_PLUS = pygame.K_PLUS
    K_COMMA = pygame.K_COMMA
    K_MINUS = pygame.K_MINUS
    K_PERIOD = pygame.K_PERIOD
    K_SLASH = pygame.K_SLASH
    K_0 = pygame.K_0
    K_1 = pygame.K_1
    K_2 = pygame.K_2
    K_3 = pygame.K_3
    K_4 = pygame.K_4
    K_5 = pygame.K_5
    K_6 = pygame.K_6
    K_7 = pygame.K_7
    K_8 = pygame.K_8
    K_9 = pygame.K_9
    K_COLON = pygame.K_COLON
    K_SEMICOLON = pygame.K_SEMICOLON
    K_LESS = pygame.K_LESS
    K_EQUALS = pygame.K_EQUALS
    K_GREATER = pygame.K_GREATER
    K_QUESTION = pygame.K_QUESTION
    K_AT = pygame.K_AT
    K_LEFTBRACKET = pygame.K_LEFTBRACKET
    K_BACKSLASH = pygame.K_BACKSLASH
    K_RIGHTBRACKET = pygame.K_RIGHTBRACKET
    K_CARET = pygame.K_CARET
    K_UNDERSCORE = pygame.K_UNDERSCORE
    K_BACKQUOTE = pygame.K_BACKQUOTE
    K_a = pygame.K_a
    K_b = pygame.K_b
    K_c = pygame.K_c
    K_d = pygame.K_d
    K_e = pygame.K_e
    K_f = pygame.K_f
    K_g = pygame.K_g
    K_h = pygame.K_h
    K_i = pygame.K_i
    K_j = pygame.K_j
    K_k = pygame.K_k
    K_l = pygame.K_l
    K_m = pygame.K_m
    K_n = pygame.K_n
    K_o = pygame.K_o
    K_p = pygame.K_p
    K_q = pygame.K_q
    K_r = pygame.K_r
    K_s = pygame.K_s
    K_t = pygame.K_t
    K_u = pygame.K_u
    K_v = pygame.K_v
    K_w = pygame.K_w
    K_x = pygame.K_x
    K_y = pygame.K_y
    K_z = pygame.K_z
    K_DELETE = pygame.K_DELETE
    K_KP0 = pygame.K_KP0
    K_KP1 = pygame.K_KP1
    K_KP2 = pygame.K_KP2
    K_KP3 = pygame.K_KP3
    K_KP4 = pygame.K_KP4
    K_KP5 = pygame.K_KP5
    K_KP6 = pygame.K_KP6
    K_KP7 = pygame.K_KP7
    K_KP8 = pygame.K_KP8
    K_KP9 = pygame.K_KP9
    K_KP_PERIOD = pygame.K_KP_PERIOD
    K_KP_DIVIDE = pygame.K_KP_DIVIDE
    K_KP_MULTIPLY = pygame.K_KP_MULTIPLY
    K_KP_MINUS = pygame.K_KP_MINUS
    K_KP_PLUS = pygame.K_KP_PLUS
    K_KP_ENTER = pygame.K_KP_ENTER
    K_KP_EQUALS = pygame.K_KP_EQUALS
    K_UP = pygame.K_UP
    K_DOWN = pygame.K_DOWN
    K_RIGHT = pygame.K_RIGHT
    K_LEFT = pygame.K_LEFT
    K_INSERT = pygame.K_INSERT
    K_HOME = pygame.K_HOME
    K_END = pygame.K_END
    K_PAGEUP = pygame.K_PAGEUP
    K_PAGEDOWN = pygame.K_PAGEDOWN
    K_F1 = pygame.K_F1
    K_F2 = pygame.K_F2
    K_F3 = pygame.K_F3
    K_F4 = pygame.K_F4
    K_F5 = pygame.K_F5
    K_F6 = pygame.K_F6
    K_F7 = pygame.K_F7
    K_F8 = pygame.K_F8
    K_F9 = pygame.K_F9
    K_F10 = pygame.K_F10
    K_F11 = pygame.K_F11
    K_F12 = pygame.K_F12
    K_F13 = pygame.K_F13
    K_F14 = pygame.K_F14
    K_F15 = pygame.K_F15
    K_NUMLOCK = pygame.K_NUMLOCK
    K_CAPSLOCK = pygame.K_CAPSLOCK
    K_SCROLLOCK = pygame.K_SCROLLOCK
    K_RSHIFT = pygame.K_RSHIFT
    K_LSHIFT = pygame.K_LSHIFT
    K_RCTRL = pygame.K_RCTRL
    K_LCTRL = pygame.K_LCTRL
    K_RALT = pygame.K_RALT
    K_LALT = pygame.K_LALT
    K_RMETA = pygame.K_RMETA
    K_LMETA = pygame.K_LMETA
    K_LSUPER = pygame.K_LSUPER
    K_RSUPER = pygame.K_RSUPER
    K_MODE = pygame.K_MODE
    K_HELP = pygame.K_HELP
    K_PRINT = pygame.K_PRINT
    K_SYSREQ = pygame.K_SYSREQ
    K_BREAK = pygame.K_BREAK
    K_MENU = pygame.K_MENU
    K_POWER = pygame.K_POWER
    K_EURO = pygame.K_EURO
    K_AC_BACK = pygame.K_AC_BACK

    def is_pressed(self) -> bool:
        """Returns a boolean that represents whether this key is being pressed."""
        return self in Camera.instance.keys

    @staticmethod
    def is_any_pressed() -> bool:
        """Returns a boolean that represents whether any key is being pressed."""
        return bool(Camera.instance.keys)

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            # check pygame descriptive key name
            try:
                return cls(pygame.key.key_code(value))
            except ValueError:
                pass

            # check pygame key constant name
            try:
                return cls[f'K_{value.upper()}']
            except KeyError:
                pass

            # check possible key names and return the most similar one
            possible = {}
            value_cf = value.casefold()
            for key in Key:
                name = pygame.key.name(key).casefold()
                name_ratio = difflib.SequenceMatcher(lambda x: not x.isalnum(), value_cf, name).ratio()
                possible[name] = name_ratio
                alt_name = key.name.removeprefix('K_').casefold()
                if name != alt_name:
                    alt_name_ratio = difflib.SequenceMatcher(lambda x: not x.isalnum(), value_cf, alt_name).ratio()
                    if alt_name_ratio > name_ratio:
                        possible[alt_name] = alt_name_ratio
            most_likely = max((k for k in possible), key=lambda k: possible[k]).lower()
            raise ValueError(f"'{value}' is not a valid key name. Did you mean: '{most_likely}'?\n"
                             "Check https://www.pygame.org/docs/ref/key.html#key-constants-label for a full list")
        return super()._missing_(value)


class Camera:
    """A camera defines what is visible.
    It has a width, height, full screen status, and can be moved.
    Moving a camera changes what is visible.
    You can add as many other attributes as you want, by (e.g.) saying ``camera.number_of_coins_found = 5``."""

    instance: Camera = None  # singleton

    def __init__(self, width: int = 800, height: int = 600, *, full_screen: bool = False) -> None:
        """
        * ``Camera()`` makes a window that is 800 pixels wide and 600 pixels tall.
        * ``Camera(pixelsWide, pixelsTall)`` makes a window with the given size.
        * ``Camera(pixelsWide, pixelsTall, full_screen=True)`` makes it display in full-screen.

        :param width: How many pixels wide the window should be
        :param height: How many pixels tall the window should be
        :param full_screen: False will display the game in a window; True will display it in full-screen
        """
        if self.__class__.instance is not None:
            raise RuntimeError("You can only have one Camera at a time")
        self._surface: Surface
        if full_screen:
            self._surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self._surface = pygame.display.set_mode((width, height))
        self._x: float = 0.0
        self._y: float = 0.0
        self.keys: set[Key] = set()
        self.__class__.instance = self

    @functools.singledispatchmethod
    def move(self, x: float, y: float) -> None:
        """``camera.move(3, -7)`` moves the screen's center to be 3 more pixels to the right and 7 more up.
        If only x given, assumed to be a point [x,y]."""
        self.x += x
        self.y += y

    @move.register(tuple)
    @move.register(Sequence)
    def _(self, coords: _Coordinate) -> None:
        if len(coords) > 2:
            raise ValueError(f"Expected 2 coordinates, but got {len(coords)} instead")
        self.x += coords[0]
        self.y += coords[1]

    def draw(self, box: SpriteBox) -> None:
        """Draws the provided SpriteBox object."""
        if box.color is not None:
            region = box.rect.move(-self._x, -self._y)
            region = region.clip(self._surface.get_rect())
            self._surface.fill(box.color, region)
        elif box.image is not None:
            self._surface.blit(box.image, [box.left - self._x, box.top - self._y])

    @staticmethod
    def display() -> None:
        """Causes what has been drawn recently by calls to ``draw(...)`` to be displayed on the screen."""
        pygame.display.flip()

    def clear(self, color: _ColorValue) -> None:
        """Erases the screen by filling it with the given color."""
        self._surface.fill(color)

    @property
    def left(self) -> float:
        """The x coordinate of the left edge of the viewable area."""
        return self._x

    @left.setter
    def left(self, value: float) -> None:
        self._x = value

    @property
    def right(self) -> float:
        """The x coordinate of the right edge of the viewable area."""
        return self._x + self.width

    @right.setter
    def right(self, value: float) -> None:
        self._x = value - self.width

    @property
    def top(self) -> float:
        """The y coordinate of the top edge of the viewable area."""
        return self._y

    @top.setter
    def top(self, value: float) -> None:
        self._y = value

    @property
    def bottom(self) -> float:
        """The y coordinate of the bottom edge of the viewable area."""
        return self._y + self.height

    @bottom.setter
    def bottom(self, value: float) -> None:
        self._y = value - self.height

    @property
    def x(self) -> float:
        """The x coordinate of the center of the viewable area."""
        return self._x + self.width / 2

    @x.setter
    def x(self, value: float) -> None:
        self._x = value - self.width / 2

    @property
    def y(self) -> float:
        """The y coordinate of the center of the viewable area."""
        return self._y + self.height / 2

    @y.setter
    def y(self, value: float) -> None:
        self._y = value - self.height / 2

    @property
    def center(self) -> tuple[float, float]:
        """The (x, y) coordinates of the center of the viewable area."""
        return self.x, self.y

    @center.setter
    def center(self, value: tuple[float, float] | Sequence[float]) -> None:
        self.x, self.y = value

    @property
    def topleft(self) -> tuple[float, float]:
        """The (x, y) coordinates of the top-left corner of the viewable area."""
        return self.left, self.top

    @topleft.setter
    def topleft(self, value: _Coordinate) -> None:
        self.left, self.top = value

    @property
    def topright(self) -> tuple[float, float]:
        """The (x, y) coordinates of the top-right corner of the viewable area."""
        return self.right, self.top

    @topright.setter
    def topright(self, value: _Coordinate) -> None:
        self.right, self.top = value

    @property
    def bottomleft(self) -> tuple[float, float]:
        """The (x, y) coordinates of the bottom-left corner of the viewable area."""
        return self.left, self.bottom

    @bottomleft.setter
    def bottomleft(self, value: _Coordinate) -> None:
        self.left, self.bottom = value

    @property
    def bottomright(self) -> tuple[float, float]:
        """The (x, y) coordinates of the bottom-right corner of the viewable area."""
        return self.right, self.bottom

    @bottomright.setter
    def bottomright(self, value: _Coordinate) -> None:
        self.right, self.bottom = value

    @property
    def width(self) -> int:
        """The width of the viewable area."""
        return self._surface.get_width()

    @property
    def height(self) -> int:
        """The height of the viewable area."""
        return self._surface.get_height()

    @property
    def size(self) -> tuple[int, int]:
        """The size of the viewable area, in the order (width, height)."""
        return self.width, self.height

    @property
    def mousex(self) -> float:
        """The x coordinate of the mouse cursor."""
        return pygame.mouse.get_pos()[0] + self._x

    @property
    def mousey(self) -> float:
        """The x coordinate of the mouse cursor."""
        return pygame.mouse.get_pos()[1] + self._y

    @property
    def mouse(self) -> tuple[float, float]:
        """The (x, y) coordinates of the mouse cursor."""
        pos = pygame.mouse.get_pos()
        return pos[0] + self._x, pos[1] + self._y

    @property
    def mouseclick(self) -> bool:
        """Whether any of the mouse buttons are being pressed."""
        return any(pygame.mouse.get_pressed())

    def __getattr__(self, name: str) -> NoReturn:
        # Fallback when attribute is not found
        raise AttributeError(f"There is no '{name}' in a Camera object")

    def __setattr__(self, name: str, value: Any) -> None:
        # Log when non-standard attributes are added
        super().__setattr__(name, value)
        if name not in ["_surface", "_x", "_y"] and name not in dir(self):
            sys.stderr.write(f'INFO: added "{name}" to camera\n')

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f'{self.width}x{self.height} Camera centered at {self.x},{self.y}'


class SpriteBox:
    """Intended to represent a sprite (i.e., an image that can be drawn as part of a larger view)
    and the box that contains it. Has various collision and movement methods built in.
    You can add as many other attributes as you want, by (e.g.) saying ``box.number_of_coins_found = 5``."""

    def __init__(self, x: float, y: float, image: str | Surface | None, color: _ColorValue | None,
                 w: float = None, h: float = None):
        """You should probably use the :py:meth:`SpriteBox.from_image`, :py:meth:`SpriteBox.from_text`,
        or :py:meth:`SpriteBox.from_color` functions instead of this."""
        self.x: float = x
        self.y: float = y
        self.speedx: float = 0.0
        self.speedy: float = 0.0
        self._key: _ImageKey | None
        self._image: Surface | None
        self._color: _ColorValue | None
        self._w: float
        self._h: float
        if image is not None:
            self._set_key(image, False, 0, 0, 0)
            if w is not None:
                if h is not None:
                    self.size = w, h
                else:
                    self.width = w
            elif h is not None:
                self.height = h
        elif color is not None:
            if w is None or h is None:
                raise ValueError("must supply size of color box")
            self._key = None
            self._image = None
            self._color = color
            self._w = w
            self._h = h

    @classmethod
    def from_image(cls, x: float, y: float, filename_or_url: str | Surface) -> SpriteBox:
        """Creates a SpriteBox object at the given location from the provided filename, URL, or image."""
        if isinstance(filename_or_url, Surface):
            _ImageCache.cache_surface(filename_or_url)
            image = filename_or_url
        else:
            image = _ImageCache.load_filename_or_url(filename_or_url)
        return cls(x, y, image, None)

    @classmethod
    def from_color(cls, x: float, y: float, color: _ColorValue, width: float, height: float) -> SpriteBox:
        """Creates a SpriteBox object at the given location with the given color, width, and height"""
        return cls(x, y, None, color, width, height)

    @classmethod
    def from_circle(cls, x: float, y: float, color: _ColorValue, radius: float, *args) -> SpriteBox:
        """Creates a SpriteBox object at the given location filled with a circle.
        `from_circle(x, y, color, radius, color2, radius2, color3, radius3, ...)` works too;
        the largest circle must come first."""
        img = Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(img, color, (radius, radius), radius)
        for i in range(1, len(args), 2):
            color = args[i - 1]
            pygame.draw.circle(img, color, (radius, radius), args[i])
        return cls(x, y, img, None)

    @classmethod
    def from_polygon(cls, x: float, y: float, color: _ColorValue, *pts: _Coordinate) -> SpriteBox:
        """Creates a SpriteBox of minimal size to store the given points.
        Note that it will be centered; adding the same offset to all points does not change the polygon."""
        x0 = min(x for x, y in pts)
        y0 = min(y for x, y in pts)
        w = max(x for x, y in pts) - x0
        h = max(y for x, y in pts) - y0
        img = Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.polygon(img, color, [(x - x0, y - y0) for x, y in pts])
        return cls(x, y, img, None)

    @classmethod
    def from_text(cls, x: float, y: float, text: str, fontsize: int, color: _ColorValue, *,
                  bold: bool = False, italic: bool = False) -> SpriteBox:
        """Creates a SpriteBox object at the given location with the given text as its content."""
        image = _ImageCache.render_text(text, fontsize, color, bold=bold, italic=italic)
        return cls(x, y, image, None)

    def _set_key(self, name: str | Surface, flip: bool, width: float, height: float, angle: float) -> None:
        """Updates the SpriteBox to display the specified image with the specified transformations."""
        if isinstance(name, Surface):
            _ImageCache.cache_surface(name)
            key = '__id__' + str(id(name))  # use id as key for Surface instead
        else:
            key = name
        assert isinstance(key, str)

        # round to nearest int, no need to render images that are within a pixel/degree of each other
        width = int(width + 0.5)
        height = int(height + 0.5)
        angle = ((int(angle) % 360) + 360) % 360  # angle in range [0, 360)

        unrot = _ImageCache.get_transform(key, flip, width, height)
        if width == 0 and height == 0:
            width = unrot.get_width()
            height = unrot.get_height()
        self._key = _ImageKey(key, flip, width, height, angle)
        self._image = _ImageCache.get_transform(*self._key)
        self._color = None
        self._w = self._image.get_width()
        self._h = self._image.get_height()

    @property
    def left(self) -> float:
        """The x coordinate of the left edge."""
        return self.x - self._w / 2

    @left.setter
    def left(self, value: float) -> None:
        self.x = value + self._w / 2

    @property
    def right(self) -> float:
        """The x coordinate of the right edge."""
        return self.x + self._w / 2

    @right.setter
    def right(self, value: float) -> None:
        self.x = value - self._w / 2

    @property
    def top(self) -> float:
        """The y coordinate of the top edge."""
        return self.y - self._h / 2

    @top.setter
    def top(self, value: float) -> None:
        self.y = value + self._h / 2

    @property
    def bottom(self) -> float:
        """The y coordinate of the bottom edge."""
        return self.y + self._h / 2

    @bottom.setter
    def bottom(self, value: float) -> None:
        self.y = value - self._h / 2

    @property
    def center(self) -> tuple[float, float]:
        """The (x, y) coordinates of the center."""
        return self.x, self.y

    @center.setter
    def center(self, value: tuple[float, float] | Sequence[float]) -> None:
        self.x, self.y = value

    @property
    def topleft(self) -> tuple[float, float]:
        """The (x, y) coordinates of the top-left corner."""
        return self.left, self.top

    @topleft.setter
    def topleft(self, value: _Coordinate) -> None:
        self.left, self.top = value

    @property
    def topright(self) -> tuple[float, float]:
        """The (x, y) coordinates of the top-right corner."""
        return self.right, self.top

    @topright.setter
    def topright(self, value: _Coordinate) -> None:
        self.right, self.top = value

    @property
    def bottomleft(self) -> tuple[float, float]:
        """The (x, y) coordinates of the bottom-left corner."""
        return self.left, self.bottom

    @bottomleft.setter
    def bottomleft(self, value: _Coordinate) -> None:
        self.left, self.bottom = value

    @property
    def bottomright(self) -> tuple[float, float]:
        """The (x, y) coordinates of the bottom-right corner."""
        return self.right, self.bottom

    @bottomright.setter
    def bottomright(self, value: _Coordinate) -> None:
        self.right, self.bottom = value

    @property
    def width(self) -> float:
        """The width of the box in pixels."""
        return self._w

    @width.setter
    def width(self, value: float) -> None:
        self.scale_by(value / self._w)

    @property
    def height(self) -> float:
        """The height of the box in pixels."""
        return self._h

    @height.setter
    def height(self, value: float) -> None:
        self.scale_by(value / self._h)

    @property
    def size(self) -> tuple[float, float]:
        """The size of the box in pixels in the order (width, height)."""
        return self.width, self.height

    @size.setter
    def size(self, value: tuple[float, float] | Sequence[float]) -> None:
        if self._image is not None and self._key is not None:
            key = self._key
            self._set_key(key[0], key[1], value[0], value[1], key[4])
        else:
            self._w, self._h = value

    @property
    def speed(self) -> tuple[float, float]:
        """The speed of the box in the order (speedx, speedy)."""
        return self.speedx, self.speedy

    @speed.setter
    def speed(self, value: tuple[float, float] | Sequence[float]) -> None:
        self.speedx, self.speedy = value

    @property
    def color(self) -> _ColorValue | None:
        """The color of the box."""
        return self._color

    @color.setter
    def color(self, value: _ColorValue) -> None:
        self._image = None
        self._key = None
        self._color = value

    @property
    def rect(self) -> pygame.Rect:
        """A :py:class:`~pygame.rect.Rect` providing the location and size of the box."""
        return pygame.Rect(self.topleft, self.size)

    @property
    def image(self) -> Surface | None:
        """A :py:class:`~pygame.surface.Surface` representing the current look of the box."""
        return self._image

    @image.setter
    def image(self, value: str | Surface) -> None:
        if self._key is not None:
            key = self._key
            self._set_key(value, *key[1:])
        else:
            self._set_key(value, False, 0, 0, 0)

    @property
    def xspeed(self) -> float:
        """Alias of :py:attr:`speedx`."""
        return self.speedx

    @xspeed.setter
    def xspeed(self, value: float) -> None:
        self.speedx = value

    @property
    def yspeed(self) -> float:
        """Alias of :py:attr:`speedy`."""
        return self.speedy

    @yspeed.setter
    def yspeed(self, value: float) -> None:
        self.speedy = value

    @property
    def mousehover(self) -> bool:
        """Whether the mouse cursor is hovering over this box."""
        return self.contains(*Camera.instance.mouse)

    @property
    def mouseclick(self) -> bool:
        """Whether this box is being clicked with any of the mouse buttons."""
        return self.mousehover and Camera.instance.mouseclick

    def overlap(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> list[float]:
        """``b1.overlap(b1)`` returns a list of 2 values such that ``self.move(result)`` will cause them to not overlap.
        Returns ``[0,0]`` if there is no overlap (i.e., if ``b1.touches(b2)`` returns False).
        ``b1.overlap(b2, 5)`` adds a 5-pixel padding to b1 before computing the overlap.
        ``b1.overlap(b2, 5, 10)`` adds a 5-pixel padding in x and a 10-pixel padding in y before computing the
        overlap."""
        if padding2 is None:
            padding2 = padding
        l = other.left - self.right - padding
        r = self.left - other.right - padding
        t = other.top - self.bottom - padding2
        b = self.top - other.bottom - padding2
        m = max(l, r, t, b)
        if m >= 0:
            return [0, 0]
        elif m == l:
            return [l, 0]
        elif m == r:
            return [-r, 0]
        elif m == t:
            return [0, t]
        else:
            return [0, -b]

    def touches(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> bool:
        """``b1.touches(b1)`` returns True if the two SpriteBoxes overlap, False if they do not.
        ``b1.touches(b2, 5)`` adds a 5-pixel padding to b1 before computing the touch.
        ``b1.touches(b2, 5, 10)`` adds a 5-pixel padding in x and a 10-pixel padding in y before computing the touch."""
        if padding2 is None:
            padding2 = padding
        l = other.left - self.right - padding
        r = self.left - other.right - padding
        t = other.top - self.bottom - padding2
        b = self.top - other.bottom - padding2
        return max(l, r, t, b) <= 0

    def bottom_touches(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> bool:
        """``b1.bottom_touches(b2)`` returns True if both ``b1.touches(b2)``
        and b1's bottom edge is the one causing the overlap."""
        if padding2 is None:
            padding2 = padding
        return self.overlap(other, padding + 1, padding2 + 1)[1] < 0

    def top_touches(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> bool:
        """``b1.top_touches(b2)`` returns True if both ``b1.touches(b2)``
        and b1's top edge is the one causing the overlap."""
        if padding2 is None:
            padding2 = padding
        return self.overlap(other, padding + 1, padding2 + 1)[1] > 0

    def left_touches(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> bool:
        """``b1.left_touches(b2)`` returns True if both ``b1.touches(b2)``
        and b1's left edge is the one causing the overlap."""
        if padding2 is None:
            padding2 = padding
        return self.overlap(other, padding + 1, padding2 + 1)[0] > 0

    def right_touches(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> bool:
        """``b1.right_touches(b2)`` returns True if both ``b1.touches(b2)``
        and b1's right edge is the one causing the overlap."""
        if padding2 is None:
            padding2 = padding
        return self.overlap(other, padding + 1, padding2 + 1)[0] < 0

    @functools.singledispatchmethod
    def contains(self, x: float, y: float) -> bool:
        """Checks if the given point is inside this SpriteBox's bounds or not.
        If only x given, assumed to be a point [x,y]."""
        return abs(x - self.x) * 2 < self._w and abs(y - self.y) * 2 < self._h

    @contains.register(tuple)
    @contains.register(Sequence)
    def _(self, coords: _Coordinate) -> bool:
        if len(coords) > 2:
            raise ValueError(f"Expected 2 coordinates, but got {len(coords)} instead")
        return self.contains(coords[0], coords[1])

    def move_to_stop_overlapping(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> None:
        """``b1.move_to_stop_overlapping(b2)`` makes the minimal change to b1's position necessary so that they no
        longer overlap. Afterwards, b1's speed will be set to 0."""
        o = self.overlap(other, padding, padding2)
        if o != [0, 0]:
            self.move(o)
            if o[0] * self.speedx < 0:
                self.speedx = 0
            if o[1] * self.speedy < 0:
                self.speedy = 0

    def move_both_to_stop_overlapping(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> None:
        """``b1.move_both_to_stop_overlapping(b2)`` changes both b1 and b2's positions so that they no longer overlap.
        Afterwards, both b1 and b2's speed will be set to their average speed."""
        o = self.overlap(other, padding, padding2)
        if o != [0, 0]:
            self.move(o[0] / 2, o[1] / 2)
            other.move(-o[0] / 2, -o[1] / 2)
            if o[0] != 0:
                self.speedx = (self.speedx + other.speedx) / 2
                other.speedx = self.speedx
            if o[1] != 0:
                self.speedy = (self.speedy + other.speedy) / 2
                other.speedy = self.speedy

    @functools.singledispatchmethod
    def move(self, x: float, y: float) -> None:
        """Change position by the given amount in x and y. If only x given, assumed to be a point [x,y]."""
        self.x += x
        self.y += y

    @move.register(tuple)
    @move.register(Sequence)
    def _(self, coords: _Coordinate) -> None:
        if len(coords) > 2:
            raise ValueError(f"Expected 2 coordinates, but got {len(coords)} instead")
        return self.move(coords[0], coords[1])

    def move_speed(self) -> None:
        """Change position by the current speed field of the SpriteBox object."""
        self.move(self.speedx, self.speedy)

    def full_size(self) -> None:
        """Change size of this SpriteBox to be the original size of the source image."""
        if self._key is None:
            return
        key = self._key
        self._set_key(key[0], key[1], 0, 0, key[4])

    def __getattr__(self, name: str) -> NoReturn:
        # Fallback when attribute is not found
        raise AttributeError(f"There is no '{name}' in a SpriteBox object")

    def __setattr__(self, name: str, value: Any) -> None:
        # Log when non-standard attributes are added
        super().__setattr__(name, value)
        if name not in ["x", "y", "speedx", "speedy", "_w", "_h", "_key", "_image", "_color"] and name not in dir(self):
            sys.stderr.write(f'INFO: added "{name}" to box\n')

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self._w}x{self._h} SpriteBox centered at {self.x},{self.y}"

    def copy_at(self, newx: float, newy: float) -> SpriteBox:
        """Make a new SpriteBox just like this one but at the given location instead of here."""
        return SpriteBox(newx, newy, self._image, self._color, self._w, self._h)

    def copy(self) -> SpriteBox:
        """Make a new SpriteBox just like this one and in the same location."""
        return self.copy_at(self.x, self.y)

    def scale_by(self, multiplier: float) -> None:
        """Change the size of this SpriteBox by the given factor.
        ``b1.scale_by(1)`` does nothing; ``b1.scale_by(0.4)`` makes b1 40% of its original width and height."""
        if self._key is None:
            self._w *= multiplier
            self._h *= multiplier
        else:
            key = self._key
            self._set_key(key[0], key[1], key[2] * multiplier, key[3] * multiplier, key[4])

    def flip(self) -> None:
        """Mirrors the SpriteBox left-to-right.
        Mirroring top-to-bottom can be accomplished by::

            b1.rotate(180)
            b1.flip()"""
        if self._key is None:
            return
        key = self._key
        self._set_key(key[0], not key[1], *key[2:])

    def rotate(self, angle: float) -> None:
        """Rotates the SpriteBox by the given angle (in degrees)."""
        if self._key is None:
            return
        key = self._key
        self._set_key(key[0], key[1], key[2], key[3], key[4] + angle)


class _ImageCache:
    """A cache to avoid loading images many times."""
    _known_images: dict[_ImageKey, Surface] = {}
    _known_text: dict[_TextKey, Surface] = {}

    @classmethod
    def cache_surface(cls, surface: Surface) -> None:
        """Caches a :py:class:`~Surface`."""
        sid = '__id__' + str(id(surface))
        key = _ImageKey(sid)
        if _ImageKey(sid) not in cls._known_images:
            cls._known_images[key] = surface
            cls._known_images[_ImageKey(sid, False, surface.get_width(), surface.get_height())] = surface

    @classmethod
    def get_transform(cls, key: str, flip: bool = False, w: int = 0, h: int = 0, angle: int = 0) -> Surface:
        """A method for loading images, caching them, and applying transformations to them."""
        # get the requested image by getting the base image and applying one transformation at a time recursively
        # already in cache
        if _ImageKey(key, flip, w, h, angle) in cls._known_images:
            ans = cls._known_images[_ImageKey(key, flip, w, h, angle)]
        # for rotation, get the flipped/scaled image then rotate
        elif angle != 0:
            base = _ImageCache.get_transform(key, flip, w, h)
            img = pygame.transform.rotozoom(base, angle, 1)
            cls._known_images[_ImageKey(key, flip, w, h, angle)] = img
            ans = img
        # for scaling, get the flipped image then scale
        elif w != 0 or h != 0:
            base = _ImageCache.get_transform(key, flip)
            img = pygame.transform.smoothscale(base, (w, h))
            cls._known_images[_ImageKey(key, flip, w, h, angle)] = img
            ans = img
        # for flipping, get the original image then flip
        elif flip:
            base = _ImageCache.get_transform(key)
            img = pygame.transform.flip(base, True, False)
            cls._known_images[_ImageKey(key, flip, w, h, angle)] = img
            ans = img
        # load the original image
        else:
            img = _ImageCache.load_filename_or_url(key)
            cls._known_images[_ImageKey(key, flip, w, h, angle)] = img
            ans = img

        # if requested at default size, also cache using the image's original width and height values
        if w == 0 and h == 0:
            if angle != 0:
                tmp = _ImageCache.get_transform(key, flip, w, h)
            else:
                tmp = ans
            cls._known_images[_ImageKey(key, flip, tmp.get_width(), tmp.get_height(), angle)] = ans

        return ans

    @classmethod
    def load_filename_or_url(cls, filename_or_url: str) -> Surface:
        """A method for loading an image from cache, then a file, then a URL. Caches the image that is loaded."""
        # check cache
        key = _ImageKey(filename_or_url)
        if key in cls._known_images:
            return cls._known_images[key]

        try:
            # check local file and add to cache if found
            if os.path.exists(filename_or_url):
                return cls._get_filename(filename_or_url)

            # check URL and add to cache if found
            else:
                return cls._get_url(filename_or_url)
        except OSError:
            raise ValueError(
                f'An error occurred while fetching image, are you sure the file/website name is "{filename_or_url}"?')

    @classmethod
    def _get_filename(cls, filename: str) -> Surface:
        """A method for loading images from files."""
        # load from file
        image = pygame.image.load(filename).convert_alpha()

        # add to cache under filename
        cls._known_images[_ImageKey(filename)] = image
        cls._known_images[_ImageKey(filename, False, image.get_width(), image.get_height())] = image

        # add to cache as surface
        cls.cache_surface(image)
        return image

    @classmethod
    def _get_url(cls, url: str) -> Surface:
        """A method for loading images from a URL by first saving them locally."""
        filename = os.path.basename(urllib.parse.urlparse(url).path)
        if not os.path.exists(filename):
            if '://' not in url:
                url = 'http://' + url
            urllib.request.urlretrieve(url, filename)

        # load from file and add to cache
        return cls._get_filename(filename)

    @classmethod
    def render_text(cls, text: str, fontsize: int, color: _ColorValue, *,
                    bold: bool = False, italic: bool = False) -> Surface:
        # check cache
        key = _TextKey(text, fontsize, color, bold, italic)
        if key in cls._known_text:
            return cls._known_text[key]

        # render text
        font = pygame.font.Font(None, fontsize)
        font.set_bold(bold)
        font.set_italic(italic)
        image = font.render(text, True, color)

        # add to text cache and surface cache
        cls._known_text[key] = image
        cls.cache_surface(image)
        return image


def load_sprite_sheet(filename_or_url: str, rows: int, columns: int) -> list[Surface]:
    """Loads a sprite sheet.
    Assumes the sheet has rows-by-columns evenly-spaced images and returns a list of those images."""
    sheet = _ImageCache.load_filename_or_url(filename_or_url)
    height = sheet.get_height() / rows
    width = sheet.get_width() / columns
    frames = []
    for row in range(rows):
        for col in range(columns):
            clip = pygame.Rect(col * width, row * height, width, height)
            frame = sheet.subsurface(clip)
            frames.append(frame)
    return frames


def timer_loop(fps: int, callback: Callable[[], Any], limit: int = None) -> bool:
    # noinspection PyMissingTypeHints,PyShadowingNames,PyUnresolvedReferences
    """Requests that pygame call the provided function `fps` times a second.

        :param fps: a number between 1 and 60
        :param callback: a function that accepts a set of keys pressed since the last tick
        :param limit: if given, will only run for that many frames and then return True
        :return: True if given limit and limit reached; False otherwise

        :example:

        >>> seconds = 0
        >>>
        >>> def tick(keys):
        >>>     seconds += 1/30
        >>>     if pygame.K_DOWN in keys:
        >>>         print('down arrow pressed')
        >>>     if not keys:
        >>>         print('no keys were pressed since the last tick')
        >>>     camera.draw(box)
        >>>     camera.display()
        >>>
        >>> gamebox.timer_loop(30, tick)
        """
    # Enforce maximum FPS of 60
    if fps > 60:
        fps = 60

    frames = 0
    pygame.time.set_timer(pygame.USEREVENT, int(1000 / fps))
    while not limit or frames < limit:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:  # closing the window or stop_loop()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                Camera.instance.keys.add(event.key)
        elif event.type == pygame.KEYUP and event.key in Camera.instance.keys:
            Camera.instance.keys.remove(event.key)
        elif event.type == pygame.USEREVENT:
            frames += 1
            pygame.event.clear(pygame.USEREVENT)
            callback()
    pygame.time.set_timer(pygame.USEREVENT, 0)
    return limit == frames


def freeze_loop() -> None:
    """Freezes the game and stops the timer.
    You cannot unfreeze the game, but you can still exit the game using the Esc key."""
    pygame.time.set_timer(pygame.USEREVENT, 0)


def stop_loop() -> None:
    """Completely quits the `timer_loop`, usually ending the program."""
    pygame.event.post(pygame.event.Event(pygame.QUIT))
