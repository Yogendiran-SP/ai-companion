from pywinauto import Desktop

def extract_cwd(terminal_buffer: str) -> str | None:
    cwd = None

    for line in terminal_buffer.splitlines():
        line = line.strip()

        if line.endswith(">") and ":\\" in line:
            cwd = line[:-1]

    return cwd


def get_terminal_cwd() -> str | None:
    terminal = Desktop(backend="uia").window(
        title_re=".*Command Prompt.*"
    )

    texts = terminal.descendants(control_type="Text")

    for text in texts:
        cwd = extract_cwd(text.window_text())

        if cwd:
            return cwd
        
    return None

# For Debugging
print(get_terminal_cwd())