from pathlib import Path


class FileWrapper:
    def read_file(self, file_path: Path) -> str:
        with open(file_path, "r") as f:
            file_contents = f.read()
        return file_contents

    def write_file(self, content: str, file_path: Path):
        with open(file_path, "w") as f:
            f.write(content)
