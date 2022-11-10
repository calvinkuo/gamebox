"""A game where the player types 20 words as fast as possible."""

import random

from gamebox import *

fps = 60
words = [
    'along', 'being', 'dance', 'finch', 'floor',
    'frown', 'graze', 'heart', 'joker', 'knife',
    'quart', 'rivet', 'scrub', 'silky', 'slump',
    'super', 'troll', 'valor', 'xylem', 'zebra',
]
random.shuffle(words)
word_index = -1
keys_remaining = ' '
keys_already_typed = ''
current_key = ''
total_score = 0
round_score = 0
camera = Camera()

def tick():
    global words, word_index, keys_remaining, keys_already_typed, current_key, total_score, round_score

    # If all the words in the list have been used, reset and show game over screen
    if word_index >= len(words):
        random.shuffle(words)
        word_index = -1
        keys_remaining = 'Game Over '
        keys_already_typed = ''
        current_key = ''
        round_score = 0

    # All the letters in this word have been typed, so go to the next round
    if not current_key and not keys_remaining:
        # Go to the next word
        word_index += 1

        # Reset score if on game over screen, otherwise add this round's score
        if keys_already_typed == 'Game Over ':
            total_score = 0
        else:
            total_score += round_score

        # Set up next round if not at the end of the list
        if word_index < len(words):
            keys_remaining = words[word_index] + ' '
            keys_already_typed = ''
            round_score = 100

    # Decrement timer if not resetting it
    elif keys_remaining != ' ' and keys_remaining != '':
        if round_score > 0:
            round_score -= 30 / fps
        else:
            round_score = 0

    # Print score
    camera.clear('black')
    camera.draw(SpriteBox.from_text(200, 50, f'Score: {int(total_score):03d}', 40, 'white'))
    camera.draw(SpriteBox.from_text(600, 50, f'Timer: {int(round_score):02d}', 40, 'white'))

    # Print the current word
    if keys_remaining != '':
        # Measure the width of the whole word, and use it to center the remaining letters
        full_word = keys_already_typed + current_key + keys_remaining.rstrip()
        x = 400 - SpriteBox.from_text(0, 275, full_word, 160, 'white').width / 2

        # Draw each letter that has already been typed in blue
        for letter in keys_already_typed:
            b = SpriteBox.from_text(0, 275, letter, 160, 'blue')
            b.left = x
            camera.draw(b)
            x += b.width + 5

        # Draw the current letter in red
        if current_key:
            b = SpriteBox.from_text(0, 275, current_key, 160, 'red')
            b.left = x
            camera.draw(b)
            x += b.width + 5

        # Draw each letter that has not been typed yet in white
        for letter in keys_remaining:
            b = SpriteBox.from_text(0, 275, letter, 160, 'white')
            b.left = x
            camera.draw(b)
            x += b.width + 5

    # Tell player to hit space to start the game and after each word
    if keys_remaining == ' ':
        camera.draw(SpriteBox.from_text(400, 475, 'Press Space', 72, 'white'))
    elif keys_remaining == '':
        camera.draw(SpriteBox.from_text(400, 475, 'Press Space', 72, 'red'))

    # Need to let go of the key before moving on to the next key
    # Fast typers will actually hit the next key before lifting their finger from the previous key,
    # so this matters most for when the same key needs to be typed twice in a row
    if current_key and not Key(current_key).is_pressed():
        keys_already_typed += current_key
        current_key = ''
    if not current_key and keys_remaining and Key(keys_remaining[0]).is_pressed():
        current_key = keys_remaining[0]
        keys_remaining = keys_remaining[1:]

    camera.display()

timer_loop(fps, tick)
