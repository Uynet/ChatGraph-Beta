def onInput(node):
  import re

  def extract_queue_puts(text):
    pattern = r'\[queue\.put\([^)]*\)\]'
    matches = re.findall(pattern, text)
    return matches

  def process_text(text):
    puts = extract_queue_puts(text)
    print(puts)

  process_text(node.input)
onInput(node)