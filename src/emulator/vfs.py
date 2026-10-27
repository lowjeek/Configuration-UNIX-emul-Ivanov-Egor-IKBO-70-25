import base64
import binascii
import posixpath
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


class VfsError(ValueError):
    pass


@dataclass
class VfsNode:
    name: str
    kind: str
    children: dict[str, "VfsNode"] = field(default_factory=dict)
    content: bytes = b""


def _check_name(name: str | None) -> str:
    if not name or name in {".", ".."} or "/" in name:
        raise VfsError(f"Некорректное имя в VFS: {name}")
    return name


def _parse_file(element: ET.Element, name: str) -> VfsNode:
    if list(element):
        raise VfsError(f"Файл содержит вложенные элементы: {name}")
    encoding = element.get("encoding", "text")
    text = element.text or ""
    if encoding == "text":
        content = text.encode("utf-8")
    elif encoding == "base64":
        try:
            content = base64.b64decode(text.strip(), validate=True)
        except (binascii.Error, ValueError) as error:
            raise VfsError(f"Неверный base64: {name}") from error
    else:
        raise VfsError(f"Неизвестная кодировка: {encoding}")
    return VfsNode(name=name, kind="file", content=content)


def _parse_node(element: ET.Element) -> VfsNode:
    name = _check_name(element.get("name"))
    if element.tag == "file":
        return _parse_file(element, name)
    if element.tag != "dir":
        raise VfsError(f"Неизвестный XML-тег: {element.tag}")
    node = VfsNode(name=name, kind="dir")
    for child in element:
        entry = _parse_node(child)
        if entry.name in node.children:
            raise VfsError(f"Повторяющееся имя: {entry.name}")
        node.children[entry.name] = entry
    return node


class VirtualFileSystem:
    def __init__(self, root: VfsNode) -> None:
        self.root = root

    @classmethod
    def from_xml(cls, path: str) -> "VirtualFileSystem":
        try:
            tree = ET.parse(path)
        except ET.ParseError as error:
            raise VfsError(f"Неверный формат XML: {error}") from error
        root_xml = tree.getroot()
        if root_xml.tag != "filesystem":
            raise VfsError("Корневой тег должен быть filesystem")
        root = VfsNode(name="/", kind="dir")
        for element in root_xml:
            node = _parse_node(element)
            if node.name in root.children:
                raise VfsError(f"Повторяющееся имя: {node.name}")
            root.children[node.name] = node
        return cls(root)

    @staticmethod
    def normalize(path: str, cwd: str = "/") -> str:
        if path.startswith("/"):
            return posixpath.normpath(path)
        return posixpath.normpath(posixpath.join(cwd, path))

    def get_node(self, path: str, cwd: str = "/") -> VfsNode:
        normalized = self.normalize(path, cwd)
        node = self.root
        if normalized == "/":
            return node
        for part in normalized.strip("/").split("/"):
            if node.kind != "dir":
                raise VfsError(f"Не каталог: {part}")
            if part not in node.children:
                raise VfsError(f"Нет такого файла или каталога: {path}")
            node = node.children[part]
        return node

    def list_directory(self, path: str, cwd: str = "/") -> str:
        node = self.get_node(path, cwd)
        if node.kind == "file":
            return node.name
        return "  ".join(sorted(node.children))

    def change_directory(self, path: str, cwd: str = "/") -> str:
        node = self.get_node(path, cwd)
        if node.kind != "dir":
            raise VfsError(f"Это не каталог: {path}")
        return self.normalize(path, cwd)
