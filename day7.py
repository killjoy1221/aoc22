import abc
import os.path


class Node(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    @abc.abstractmethod
    def size(self) -> int:
        pass

    @classmethod
    def parse(cls, line: str):
        type_or_size, name = line.split()
        if type_or_size == "dir":
            return DirNode(name)
        else:
            return FileNode(name, int(type_or_size))


class DirNode(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: list[Node] = []

    def get_node(self, name: str):
        return next(c for c in self.children if c.name == name)

    def resolve(self, path: str):
        if path == "/":
            return root
        nodes = path.split("/")[1:]
        node = self
        for n in nodes:
            node = node.get_node(n)

            if not isinstance(node, DirNode):
                raise AssertionError("node was not a dir: " + str(node))
        return node

    def dirs(self):
        yield self
        for c in self.children:
            if isinstance(c, DirNode):
                yield from c.dirs()

    @property
    def size(self):
        return sum(c.size for c in self.children)


class FileNode(Node):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    @property
    def size(self):
        return self._size


root = DirNode("")


class Shell:
    def __init__(self):
        self.cwd = "/"

    def get_cwd_node(self):
        return root.resolve(self.cwd)

    def handle_cmd(self, cmd: str, args: list[str], result: list[str]):
        if cmd == "cd":
            (path,) = args
            self.cwd = os.path.normpath(os.path.join(self.cwd, path))
        elif cmd == "ls":
            node = self.get_cwd_node()
            node.children.extend(map(Node.parse, result))


def main(data: str):
    s = Shell()
    command = None
    args = []
    result = []
    for line in data.splitlines():
        if line.startswith("$ "):
            if command is not None:
                s.handle_cmd(command, args, result)
            command, *args = line.removeprefix("$ ").split()
            result = []
        else:
            result.append(line)
    if command is not None:
        s.handle_cmd(command, args, result)

    # part 1
    print("Part 1:", sum(d.size for d in root.dirs() if d.size < 100000))

    # part 2
    total_storage = 70_000_000
    required_storage = 30_000_000

    storage_used = root.size
    storage_free = total_storage - storage_used
    to_free = required_storage - storage_free

    print("Part 2:", min(c.size for c in root.dirs() if c.size > to_free))
