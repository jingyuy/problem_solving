class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.children = {}

    def addChild(self, value):
        if value not in self.children:
            self.children[value] = Node(value)
            return True
        else:
            return False

    def containsChild(self, value):
        return value in self.children

    def hasChildren(self):
        return len(self.children) > 0

    def addAndGetChild(self, value):
        if value not in self.children:
            self.children[value] = Node(value)
        return self.children[value]


class Matcher:
    def __init__(self, rules) -> None:
        self.root = Node("/")
        for rule in rules:
            rule = rule.replace("...", "$")
            prev = None
            for char in rule:
                if prev is None:
                    prev = self.root
                    assert char == "/"
                else:
                    current = prev.addAndGetChild(char)
                    prev = current

    def getScore(self, value, weight):
        if value == "*" or value == "$":
            return 0
        else:
            return 1 * weight

    def isChar(self, value):
        return value != "*" and value != "$" and value != "/"

    def match(self, root, path, weight=10000):
        if len(path) == 0:
            return (-1, "")
        if len(path) == 1 and root.value == path[0]:
            return (1, root.value)
        if root.value == "*":
            maxScore = 0
            subrule = ""
            for i in range(len(path)):
                if self.isChar(path[i]):
                    for child in root.children:
                        (score, r) = self.match(
                            root.children[child], path[i + 1 :], weight - 1
                        )
                        if score >= 0 and maxScore < score:
                            maxScore = score
                            subrule = r
                else:
                    break
            return (maxScore + self.getScore("*", weight), "*" + subrule)
        elif root.value == "$":
            maxScore = 0
            subrule = ""
            folderIndex = path.index("/") if "/" in path else len(path)
            while folderIndex < len(path):
                for child in root.children:
                    (score, r) = self.match(
                        root.children[child], path[folderIndex:], weight - 1
                    )
                    if score >= 0 and maxScore < score:
                        maxScore = score
                        subrule = r
                try:
                    folderIndex = folderIndex + 1 + path[folderIndex + 1 :].index("/")
                except ValueError:
                    break
            return (maxScore + self.getScore("$", weight), "..." + subrule)
        elif root.value == path[0]:
            if len(path) == 1:
                return (self.getScore(root.value), root.value)
            maxScore = 0
            subrule = ""
            for child in root.children:
                (score, r) = self.match(root.children[child], path[1:], weight - 1)
                if score >= 0 and maxScore < score:
                    maxScore = score
                    subrule = r
            return (maxScore + self.getScore(root.value, weight), path[0] + subrule)
        else:
            return (-1, "")


m = Matcher(["/*/t/b.html", "/a/*/b.html"])
print(m.match(m.root, "/a/t/b.html"))
m = Matcher(["/*/.../*.html", "/a/*/b.html"])
print(m.match(m.root, "/a/cab/b.html"))
m = Matcher(["/a/.../b.html", "/a/cab/.../b.html"])
print(m.match(m.root, "/a/cab/ba/ct/kt/b.html"))
