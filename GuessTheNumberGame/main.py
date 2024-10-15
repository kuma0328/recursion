import sys
import random

sys.stdout.buffer.write(b"Welcome to the number guessing game!\n")
sys.stdout.buffer.write(b"Please enter a small number\n")
sys.stdout.flush()
n = int(sys.stdin.readline())
sys.stdout.buffer.write(b"Please enter a large number\n")
sys.stdout.flush()
m = int(sys.stdin.readline())

guess_number = random.randint(n, m)
while True:
  sys.stdout.buffer.write(b"Guess the number: ")
  sys.stdout.flush()
  number = int(sys.stdin.readline())
  if number == guess_number:
    sys.stdout.buffer.write(b"Congratulations! You guessed the number!\n")
    break
  elif number < guess_number:
    sys.stdout.buffer.write(b"Try guessing a larger number\n")
  else:
    sys.stdout.buffer.write(b"Try guessing a smaller number\n")