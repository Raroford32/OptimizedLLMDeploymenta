import re

def sanitize_input(input_text):
    # Remove any potentially harmful characters or sequences
    return re.sub(r'[^\w\s\-\.,;:!?()]', '', input_text)

def format_cpp_code(code):
    # Basic formatting for C++ code (this is a simple example, consider using a proper formatter)
    lines = code.split('\n')
    formatted_lines = []
    indent = 0
    for line in lines:
        line = line.strip()
        if line.endswith('{'):
            formatted_lines.append('    ' * indent + line)
            indent += 1
        elif line.startswith('}'):
            indent -= 1
            formatted_lines.append('    ' * indent + line)
        else:
            formatted_lines.append('    ' * indent + line)
    return '\n'.join(formatted_lines)
