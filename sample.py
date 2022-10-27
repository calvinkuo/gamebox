import pygame
import gamebox


camera = gamebox.Camera(400, 400)

camera.x = 10

b = gamebox.from_text(40, 50, "It Works! (type \"0\")", 40, "red", italic=True, bold=False)
b.speedx = 3
b.left += 2
b.y = 100
b.move_speed()

camera.draw(b)
camera.display()

def tick(keys):
    global b
    if keys:
        if pygame.K_0 in keys:
            b = gamebox.from_text(40, 50, "Type \"1\"", 40, "blue", italic=False, bold=False)
        elif pygame.K_1 in keys:
            b = gamebox.from_text(40, 50, "Type \"2\"", 40, "green", italic=True, bold=True)
        elif pygame.K_2 in keys:
            b = gamebox.from_text(40, 50, "Type \"3\"", 40, "white", italic=False, bold=True)
        elif pygame.K_a in keys:
            gamebox.stop_loop()
        elif keys:
            b.image = "https://www.python.org/static/img/python-logo.png"
        b.full_size()
    b.rotate(-5)
    b.center = camera.mouse
    b.bottom = camera.bottom
    camera.draw(b)
    camera.display()

gamebox.timer_loop(30, tick)
