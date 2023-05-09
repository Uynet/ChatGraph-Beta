def onInput(self):
    import ast
    import queue
    if not hasattr(self, "my_queue"):
        self.my_queue = queue.Queue()

    def countTask(node , q):
        s = q.qsize()
        name = "Queue "
        text = ""
        for i in range(s):
            text += "("
        text += "0"
        node.set("label",name + text)

    inputText = self.input
    commands = ast.literal_eval(inputText)
    for command in commands:
        if command.startswith("queue.put("):
            data = command.split("(")[1].split(")")[0]
            self.my_queue.put(data)
            countTask(self, self.my_queue)
        elif command == "queue.pop()":
            if not self.my_queue.empty():
                print(self.my_queue.get())
            else:
                print("Queue is empty")
            countTask(self, self.my_queue)
        else:
            print(f"Invalid command: {command}")
onInput(node)