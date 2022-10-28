import pygame
import gamebox_compat_uni as gamebox


camera = gamebox.Camera(400, 400)

camera.x = 10

b = gamebox.from_text(40, 50, "It Works! (type \"0\")", 40, "red", italic=True, bold=False)
b.speedx = 3
b.left += 2
b.y = 100
b.move_speed()

camera.draw(b)
camera.display()

def tick():
    global b
    if gamebox.is_pressing('0'):
        b = gamebox.from_text(40, 50, "Type \"1\"", 40, "blue", italic=False, bold=False)
    elif gamebox.is_pressing('1'):
        b = gamebox.from_text(40, 50, "Type \"2\"", 40, "green", italic=True, bold=True)
    elif gamebox.is_pressing('2'):
        b = gamebox.from_text(40, 50, "Type \"3\"", 40, "white", italic=False, bold=True)
    elif gamebox.is_pressing('a'):
        gamebox.stop_loop()
    elif gamebox.keys:
        b.image = "https://www.python.org/static/img/python-logo.png"
    b.full_size()
    b.rotate(-5)
    b.center = camera.mouse
    b.bottom = camera.bottom
    camera.draw(b)
    camera.display()

gamebox.timer_loop(30, tick)
