def parse_command(line: str) -> tuple[str | None, list[str]]:
    tokens = line.split()
    if not tokens:
        return None, []
    return tokens[0], tokens[1:]
