"""A library file for simplifying pygame interaction.
You MUST place this file in the same directory as your game py files."""

# This code is the original work of Luther Tychonievich, who releases it into the public domain.
# As a courtesy, Luther would appreciate it if you acknowledged him in any work that benefited from this code.

from __future__ import annotations

import os.path
import sys
from typing import Any, Callable, Dict, Hashable, List, NoReturn, Sequence, Tuple, Union
from urllib.request import urlretrieve

import pygame

pygame.init()


__all__ = [
    'Camera',
    'SpriteBox',
    'load_sprite_sheet',
    'from_image',
    'from_color',
    'from_circle',
    'from_polygon',
    'from_text',
    'timer_loop',
    'pause',
    'unpause',
    'stop_loop',
    'keys_loop'
]

# Typing hints copied from pygame._common
_RgbaOutput = Tuple[int, int, int, int]
_ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], List[int], _RgbaOutput]
_Coordinate = Union[Tuple[float, float], Sequence[float]]  # pygame._common._Coordinate, but without pygame.math.Vector2

_Image = Union[pygame.surface.Surface, str]
_ImageKey = Union[_Image, Tuple[Union[pygame.surface.Surface, str], bool, int, int, int], Tuple[int, int, str]]
_Key = int

# Module-level private globals
_known_images: Dict[_ImageKey, pygame.surface.Surface] = {}  # a cache to avoid loading images many time
_timeron: bool = False
_timerfps: int = 0


class Camera:
    """A camera defines what is visible.
    It has a width, height, full screen status, and can be moved.
    Moving a camera changes what is visible.
    You can add as many other attributes as you want, by (e.g.) saying ``camera.number_of_coins_found = 5``."""

    is_initialized = False

    def __init__(self, width: int, height: int, full_screen: bool = False) -> None:
        """Camera(pixelsWide, pixelsTall, False) makes a window; using True instead makes a full-screen display."""
        if Camera.is_initialized:
            raise RuntimeError("You can only have one Camera at a time")
        self._surface: pygame.surface.Surface
        if full_screen:
            self._surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self._surface = pygame.display.set_mode((width, height))
        self._x: float = 0.0
        self._y: float = 0.0
        Camera.is_initialized = True

    def move(self, x: float | _Coordinate, y: float = None) -> None:
        """``camera.move(3, -7)`` moves the screen's center to be 3 more pixels to the right and 7 more up."""
        if y is None:
            if len(x) > 2:
                raise ValueError(f"Expected 2 coordinates, but got {len(x)} instead")
            self.x += x[0]
            self.y += x[1]
        else:
            self.x += x
            self.y += y

    def draw(self, thing: SpriteBox | pygame.surface.Surface | str, *args) -> None:
        """* ``camera.draw(box)`` draws the provided SpriteBox object.
        * ``camera.draw(image, x, y)`` draws the provided image centered at the provided coordinates.
        * ``camera.draw("Hi", 12, "red", x, y)`` draws the text Hi in a red 12-point font at x,y."""
        if isinstance(thing, SpriteBox):
            if thing.color is not None:
                region = thing.rect.move(-self._x, -self._y)
                region = region.clip(self._surface.get_rect())
                self._surface.fill(thing.color, region)
            elif thing.image is not None:
                self._surface.blit(thing.image, [thing.left - self._x, thing.top - self._y])
        elif isinstance(thing, pygame.surface.Surface):
            try:
                if len(args) == 1:
                    x, y = args[0]
                else:
                    x, y = args[:2]
                self._surface.blit(thing, (x - thing.get_width() / 2, y - thing.get_height() / 2))
            except (IndexError, TypeError):
                raise TypeError("Wrong arguments; try .draw(surface, [x,y])")
        elif type(thing) is str:
            try:
                size = args[0]
                color = args[1]
                self.draw(pygame.font.Font(None, size).render(thing, True, color), *args[2:])
            except (IndexError, TypeError):
                raise TypeError("Wrong arguments; try .draw(text, fontSize, color, [x,y])")
        else:
            raise TypeError("I don't know how to draw a ", type(thing))

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
    def center(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the center of the viewable area."""
        return self.x, self.y

    @center.setter
    def center(self, value: Tuple[float, float] | Sequence[float]) -> None:
        self.x, self.y = value

    @property
    def topleft(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the top-left corner of the viewable area."""
        return self.left, self.top

    @topleft.setter
    def topleft(self, value: _Coordinate) -> None:
        self.left, self.top = value

    @property
    def topright(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the top-right corner of the viewable area."""
        return self.right, self.top

    @topright.setter
    def topright(self, value: _Coordinate) -> None:
        self.right, self.top = value

    @property
    def bottomleft(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the bottom-left corner of the viewable area."""
        return self.left, self.bottom

    @bottomleft.setter
    def bottomleft(self, value: _Coordinate) -> None:
        self.left, self.bottom = value

    @property
    def bottomright(self) -> Tuple[float, float]:
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
    def size(self) -> Tuple[int, int]:
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
    def mouse(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the mouse cursor."""
        return pygame.mouse.get_pos()[0] + self._x, pygame.mouse.get_pos()[1] + self._y

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
    and the box that contains it. Has various collision and movement methods built in."""

    def __init__(self, x: float, y: float, image: _Image | None, color: _ColorValue | None,
                 w: float = None, h: float = None):
        """You should probably use the from_image, from_text, or from_color method instead of this one"""
        self.x: float = x
        self.y: float = y
        self.speedx: float = 0.0
        self.speedy: float = 0.0
        self._key: Tuple[_Image, bool, int, int, int] | None
        self._image: pygame.surface.Surface | None
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

    def _set_key(self, name: _Image, flip: bool, width: float, height: float, angle: float) -> None:
        width = int(width + 0.5)
        height = int(height + 0.5)
        angle = ((int(angle) % 360) + 360) % 360
        unrot = _image(name, flip, width, height)
        if width == 0 and height == 0:
            width = unrot.get_width()
            height = unrot.get_height()
        self._key = (name, flip, width, height, angle)
        self._image = _image(*self._key)
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
    def center(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the center."""
        return self.x, self.y

    @center.setter
    def center(self, value: Tuple[float, float] | Sequence[float]) -> None:
        self.x, self.y = value

    @property
    def topleft(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the top-left corner."""
        return self.left, self.top

    @topleft.setter
    def topleft(self, value: _Coordinate) -> None:
        self.left, self.top = value

    @property
    def topright(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the top-right corner."""
        return self.right, self.top

    @topright.setter
    def topright(self, value: _Coordinate) -> None:
        self.right, self.top = value

    @property
    def bottomleft(self) -> Tuple[float, float]:
        """The (x, y) coordinates of the bottom-left corner."""
        return self.left, self.bottom

    @bottomleft.setter
    def bottomleft(self, value: _Coordinate) -> None:
        self.left, self.bottom = value

    @property
    def bottomright(self) -> Tuple[float, float]:
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
    def size(self) -> Tuple[float, float]:
        """The size of the box in pixels in the order (width, height)."""
        return self.width, self.height

    @size.setter
    def size(self, value: Tuple[float, float] | Sequence[float]) -> None:
        if self._image is not None and self._key is not None:
            key = self._key
            self._set_key(key[0], key[1], value[0], value[1], key[4])
        else:
            self._w, self._h = value

    @property
    def speed(self) -> Tuple[float, float]:
        """The speed of the box in the order (speedx, speedy)."""
        return self.speedx, self.speedy

    @speed.setter
    def speed(self, value: Tuple[float, float] | Sequence[float]) -> None:
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
        """A :py:class:`~pygame.Rect` providing the location and size of the box."""
        return pygame.Rect(self.topleft, self.size)

    @property
    def image(self) -> pygame.surface.Surface | None:
        """A :py:class:`~pygame.surface.Surface` representing the current look of the box."""
        return self._image

    @image.setter
    def image(self, value: _Image) -> None:
        if self._key is not None:
            key = self._key
            self._set_key(value, *key[1:])
        else:
            self._set_key(value, False, 0, 0, 0)

    @property
    def xspeed(self) -> float:
        """Alias of ``speedx``."""
        return self.speedx

    @xspeed.setter
    def xspeed(self, value: float) -> None:
        self.speedx = value

    @property
    def yspeed(self) -> float:
        """Alias of ``speedy``."""
        return self.speedy

    @yspeed.setter
    def yspeed(self, value: float) -> None:
        self.speedy = value

    def overlap(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> List[float]:
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

    def contains(self, x: float | _Coordinate, y: float = None) -> bool:
        """Checks if the given point is inside this SpriteBox's bounds or not."""
        if y is None:
            if len(x) > 2:
                raise ValueError(f"Expected 2 coordinates, but got {len(x)} instead")
            return self.contains(x[0], x[1])
        else:
            return abs(x - self.x) * 2 < self._w and abs(y - self.y) * 2 < self._h

    def move_to_stop_overlapping(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> None:
        """``b1.move_to_stop_overlapping(b2)`` makes the minimal change to b1's position necessary
        so that they no longer overlap"""
        o = self.overlap(other, padding, padding2)
        if o != [0, 0]:
            self.move(o)
            if o[0] * self.speedx < 0:
                self.speedx = 0
            if o[1] * self.speedy < 0:
                self.speedy = 0

    def move_both_to_stop_overlapping(self, other: SpriteBox, padding: float = 0, padding2: float = None) -> None:
        """``b1.move_both_to_stop_overlapping(b2)`` changes both b1 and b2's positions
        so that they no longer overlap"""
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

    def move(self, x: float | _Coordinate, y: float = None) -> None:
        """Change position by the given amount in x and y. If only x given, assumed to be a point [x,y]."""
        if y is None:
            if len(x) > 2:
                raise ValueError(f"Expected 2 coordinates, but got {len(x)} instead")
            self.x += x[0]
            self.y += x[1]
        else:
            self.x += x
            self.y += y

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
        return '%dx%d SpriteBox centered at %d,%d' % (self._w, self._h, self.x, self.y)

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

    def draw(self, surface: Camera | pygame.surface.Surface) -> None:
        """``b1.draw(camera)`` is the same as saying ``camera.draw(b1)``.
        ``b1.draw(image)`` draws a copy of b1 on the image provided."""
        if isinstance(surface, Camera):
            surface.draw(self)
        elif self._color is not None:
            surface.fill(self._color, self.rect)
        elif self._image is not None:
            surface.blit(self._image, self.topleft)

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


def _image(key: _Image, flip: bool = False, w: float = 0, h: float = 0, angle: float = 0) -> pygame.surface.Surface:
    """A method for loading images, caching them, and flipping them"""
    if not isinstance(key, Hashable):
        key = id(key)
    assert isinstance(key, str) or isinstance(key, int) or isinstance(key, pygame.surface.Surface)
    angle, w, h = int(angle), int(w), int(h)
    if (key, flip, w, h, angle) in _known_images:
        ans = _known_images[(key, flip, w, h, angle)]
    elif angle != 0:
        base = _image(key, flip, w, h)
        img = pygame.transform.rotozoom(base, angle, 1)
        _known_images[(key, flip, w, h, angle)] = img
        ans = img
    elif w != 0 or h != 0:
        base = _image(key, flip)
        img = pygame.transform.smoothscale(base, (w, h))
        _known_images[(key, flip, w, h, angle)] = img
        ans = img
    elif flip:
        base = _image(key)
        img = pygame.transform.flip(base, True, False)
        _known_images[(key, flip, w, h, angle)] = img
        ans = img
    else:
        img, _ = _get_image(key)
        _known_images[(key, flip, w, h, angle)] = img
        ans = img
    if w == 0 and h == 0:
        if angle != 0:
            tmp = _image(key, flip, w, h)
        else:
            tmp = ans
        _known_images[(key, flip, tmp.get_width(), tmp.get_height(), angle)] = ans
    return ans


def _image_from_url(url: str) -> Tuple[pygame.surface.Surface, str]:
    """A method for loading images from urls by first saving them locally."""
    filename = os.path.basename(url)
    if not os.path.exists(filename):
        if '://' not in url:
            url = 'http://' + url
        urlretrieve(url, filename)
    image, filename = _image_from_file(filename)
    return image, filename


def _image_from_file(filename: str) -> Tuple[pygame.surface.Surface, str]:
    """A method for loading images from files."""
    image = pygame.image.load(filename).convert_alpha()
    _known_images[filename] = image
    _known_images[(image.get_width(), image.get_height(), filename)] = image
    return image, filename


def _get_image(thing: _ImageKey) -> Tuple[pygame.surface.Surface, _ImageKey]:
    """a method for loading images from cache, then file, then url"""
    if thing in _known_images:
        return _known_images[thing], thing

    sid = '__id__' + str(id(thing))
    if sid in _known_images:
        return _known_images[sid], sid

    if isinstance(thing, str):
        if os.path.exists(thing):
            return _image_from_file(thing)
        return _image_from_url(thing)

    assert isinstance(thing, pygame.surface.Surface)
    _known_images[sid] = thing
    _known_images[(thing.get_width(), thing.get_height(), sid)] = thing
    return thing, sid


def load_sprite_sheet(url_or_filename: str, rows: int, columns: int) -> List[pygame.surface.Surface]:
    """Loads a sprite sheet.
    Assumes the sheet has rows-by-columns evenly-spaced images and returns a list of those images."""
    sheet, key = _get_image(url_or_filename)
    height = sheet.get_height() / rows
    width = sheet.get_width() / columns
    frames = []
    for row in range(rows):
        for col in range(columns):
            clip = pygame.Rect(col * width, row * height, width, height)
            frame = sheet.subsurface(clip)
            frames.append(frame)
    return frames


def from_image(x: float, y: float, filename_or_url: str | pygame.surface.Surface) -> SpriteBox:
    """Creates a SpriteBox object at the given location from the provided filename or url"""
    image, key = _get_image(filename_or_url)
    return SpriteBox(x, y, image, None)


def from_color(x: float, y: float, color: _ColorValue, width: float, height: float) -> SpriteBox:
    """Creates a SpriteBox object at the given location with the given color, width, and height"""
    return SpriteBox(x, y, None, color, width, height)


def from_circle(x: float, y: float, color: _ColorValue, radius: float, *args) -> SpriteBox:
    """Creates a SpriteBox object at the given location filled with a circle.
    from_circle(x,y,color,radius,color2,radius2,color3,radius3,...) works too; the largest circle must come first"""
    img = pygame.surface.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32)
    pygame.draw.circle(img, color, (radius, radius), radius)
    for i in range(1, len(args), 2):
        color = args[i - 1]
        pygame.draw.circle(img, color, (radius, radius), args[i])
    return SpriteBox(x, y, img, None)


def from_polygon(x: float, y: float, color: _ColorValue, *pts: _Coordinate) -> SpriteBox:
    """Creates a SpriteBox of minimal size to store the given points.
    Note that it will be centered; adding the same offset to all points does not change the polygon."""
    x0 = min(x for x, y in pts)
    y0 = min(y for x, y in pts)
    w = max(x for x, y in pts) - x0
    h = max(y for x, y in pts) - y0
    img = pygame.surface.Surface((w, h), pygame.SRCALPHA, 32)
    pygame.draw.polygon(img, color, [(x - x0, y - y0) for x, y in pts])
    return SpriteBox(x, y, img, None)


def from_text(x: float, y: float, text: str, fontsize: int, color: _ColorValue,
              bold: bool = False, italic: bool = False) -> SpriteBox:
    """Creates a SpriteBox object at the given location with the given text as its content"""
    # always use default font. Earlier versions allowed others, but this proved platform-dependent
    font = pygame.font.Font(None, fontsize)
    font.set_bold(bold)
    font.set_italic(italic)
    return from_image(x, y, font.render(text, True, color))


def timer_loop(fps: int, callback: Callable[[set[_Key]], Any], limit: int = None) -> bool:
    """Requests that pygame call the provided function fps times a second
    fps: a number between 1 and 60
    callback: a function that accepts a set of keys pressed since the last tick
    limit: if given, will only run for that many frames and then return True
    returns: True if given limit and limit reached; False otherwise::

        seconds = 0
        def tick(keys):
            seconds += 1/30
            if pygame.K_DOWN in keys:
                print 'down arrow pressed'
            if not keys:
                print 'no keys were pressed since the last tick'
            camera.draw(box)
            camera.display()

        gamebox.timer_loop(30, tick)"""
    global _timeron, _timerfps
    keys: set[_Key] = set([])
    if fps > 60:
        fps = 60
    _timerfps = fps
    _timeron = True
    frames = 0
    pygame.time.set_timer(pygame.USEREVENT, int(1000 / fps))
    while not limit or frames < limit:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                keys.add(event.key)
        elif event.type == pygame.KEYUP and event.key in keys:
            keys.remove(event.key)
        elif event.type == pygame.USEREVENT:
            frames += 1
            pygame.event.clear(pygame.USEREVENT)
            callback(keys)
    pygame.time.set_timer(pygame.USEREVENT, 0)
    _timeron = False
    return limit == frames


def pause() -> None:
    """Pauses the timer; an error if there is no timer to pause"""
    if not _timeron:
        raise RuntimeError("Cannot pause a timer before calling timer_loop(fps, callback)")
    pygame.time.set_timer(pygame.USEREVENT, 0)


def unpause() -> None:
    """Unpauses the timer; an error if there is no timer to unpause"""
    if not _timeron:
        raise RuntimeError("Cannot pause a timer before calling timer_loop(fps, callback)")
    pygame.time.set_timer(pygame.USEREVENT, int(1000 / _timerfps))


def stop_loop() -> None:
    """Completely quits one timer_loop or keys_loop, usually ending the program"""
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def keys_loop(callback: Callable[[List[_Key]], Any]) -> None:
    """Requests that pygame call the provided function each time a key is pressed
    callback: a function that accepts the key pressed::

        def onPress(key):
            if pygame.K_DOWN == key:
                print 'down arrow pressed'
            if pygame.K_a in keys:
                print 'A key pressed'
            camera.draw(box)
            camera.display()

        gamebox.keys_loop(onPress)
    """
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                callback([event.key])
        if event.type == pygame.MOUSEBUTTONDOWN:
            callback([])
