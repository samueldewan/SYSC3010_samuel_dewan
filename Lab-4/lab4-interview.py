from sense_hat import SenseHat

s = SenseHat()
s.low_light = True

letters = ["T", "T", "A", "A"]
next_letter = 0

def toggle_letter(event):
  if event is None or event.action == u"pressed":
    global next_letter
    s.show_letter(letters[next_letter], (255, 255, 255))
    next_letter = (next_letter + 1) % 4

# Show initial letter
toggle_letter(None)

s.stick.direction_up = toggle_letter
s.stick.direction_down = toggle_letter
s.stick.direction_left = toggle_letter
s.stick.direction_right = toggle_letter

while True:
  pass

