class SexprBuilder:
    def __init__(self, indent_size=2):
        self.lines = []
        self.level = 0
        self.indent_size = indent_size

    def write(self, line):
        self.lines.append(' ' * self.level * self.indent_size + line)

    def open(self, tag):
        self.write(f"({tag}")
        self.level += 1

    def close(self):
        self.level -= 1
        self.write(")")

    def render(self):
        return '\n'.join(self.lines)
