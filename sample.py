from gamebox import *


camera = Camera(400, 400)

camera.x = 10

b = SpriteBox.from_text(40, 50, "It Works! (type \"0\")", 40, "red", italic=True, bold=False)
b.speedx = 3
b.left += 2
b.y = 100
b.move_speed()

camera.draw(b)
camera.display()

def tick():
    global b
    if Key.is_any_pressed():
        if Key.K_0.is_pressed():
            b = SpriteBox.from_text(40, 50, "Type \"1\"", 40, "blue", italic=False, bold=False)
        elif Key.K_1.is_pressed():
            b = SpriteBox.from_text(40, 50, "Type \"2\"", 40, "green", italic=True, bold=True)
        elif Key.K_2.is_pressed():
            b = SpriteBox.from_text(40, 50, "Type \"3\"", 40, "white", italic=False, bold=True)
        elif Key.K_a.is_pressed():
            stop_loop()
        else:
            b.image = "https://www.python.org/static/img/python-logo.png"
        b.full_size()
    b.rotate(-5)
    b.center = camera.mouse
    b.bottom = camera.bottom
    camera.draw(b)
    camera.display()

timer_loop(30, tick)
