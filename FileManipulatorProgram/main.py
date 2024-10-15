import sys


cmd = sys.argv[1]

if cmd == "reverse":
  input_path = sys.argv[2]
  output_path = sys.argv[3]
  with open(input_path, "r") as f:
    data = f.read()
  with open(output_path, "w") as f:
    f.write(data[::-1])
elif cmd == "copy":
  input_path = sys.argv[2]
  output_path = sys.argv[3]
  with open(input_path, "r") as f:
    data = f.read()
  with open(output_path, "w") as f:
    f.write(data)
elif cmd == "duplicate-contents":
  input_path = sys.argv[2]
  loop_count = int(sys.argv[3])
  with open(input_path, "r") as f:
    data = f.read()
  with open(input_path, "a") as f:
    for i in range(loop_count):
      f.write(data)
elif cmd == "replace-string":
  input_path = sys.argv[2]
  needle = sys.argv[3]
  newString = sys.argv[4]
  with open(input_path, "r") as f:
    data = f.read()
  with open(input_path, "w") as f:
    f.write(data.replace(needle, newString))
else:
  print("Invalid command")