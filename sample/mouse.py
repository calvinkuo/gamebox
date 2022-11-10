"""A game where the player clicks on as many moving boxes as they can in 30 seconds."""

import random

from gamebox import *


fps = 60
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
camera = Camera()
box = SpriteBox.from_color(random.randrange(50, 750), random.randrange(50, 550), random.choice(colors), 100, 100)
box.speedx = random.uniform(-10, 10) * 60 / fps
box.speedy = random.randrange(-10, 10) * 60 / fps
score = 0
timer = 30 * fps  # 30 seconds at 60 fps

def randomize_box():
    # Pick a new position that isn't too close to the cursor
    x, y = random.randrange(50, 750), random.randrange(50, 550)
    while -100 < x - camera.mousex < 100 or -100 < y - camera.mousey < 100:
        x, y = random.randrange(50, 750), random.randrange(50, 550)

    # Pick a new color that's different
    new_color = random.choice(colors)
    while new_color == box.color:
        new_color = random.choice(colors)

    # Update box
    box.x = x
    box.y = y
    box.speedx = random.randrange(-10, 10) * 60 / fps
    box.speedy = random.randrange(-10, 10) * 60 / fps
    box.color = new_color

def tick():
    global box, score, timer

    if timer > 0:
        # Move box if clicked
        if box.mouseclick:
            score += 1  # Increment score
            randomize_box()

        # Move box and bounce off walls
        if timer > 0:
            box.move_speed()
            if box.top < 0 or box.bottom > camera.height:
                box.yspeed = -box.yspeed
            if box.left < 0 or box.right > camera.width:
                box.xspeed = -box.xspeed
    elif timer < -3 * fps:
        # Reset game on any click after three seconds
        if camera.mouseclick:
            timer = 5 * fps
            score = 0
            randomize_box()

    # Draw everything
    camera.clear('black')
    camera.draw(box)
    camera.draw(SpriteBox.from_text(200, 50, f'Score: {score}', 40, 'white'))
    camera.draw(SpriteBox.from_text(600, 50, f'Timer: {max(timer, 0) / fps:.1f}', 40, 'white'))

    # Check timer for game over condition
    timer -= 1
    if timer <= 0:
        camera.draw(SpriteBox.from_text(400, 300, 'Game Over', 80, 'white'))
    if timer < -3 * fps:
        camera.draw(SpriteBox.from_text(400, 400, 'Click anywhere to restart', 40, 'white'))

    camera.display()

timer_loop(fps, tick)
