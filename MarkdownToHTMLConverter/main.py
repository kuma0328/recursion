import markdown
import sys

cmd = sys.argv[1]
if cmd == "markdown":
  input_path = sys.argv[2]
  output_path = sys.argv[3]
  with open(input_path, "r") as f:
    text = f.read()
  html = markdown.markdown(text)
  with open(output_path, "w") as f:
    f.write(html)
else:
  print("Unknown command")