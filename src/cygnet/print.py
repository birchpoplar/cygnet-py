from rich import print

def print_source_code(source):
    print("---SOURCE---")
    max_num_width = len(str(len(source)))
    line_num = 1
    for line in source:
        print(f"{line_num:>{max_num_width}}: {line}")
        line_num += 1

def print_token_list(tokens):
    print("---TOKENS---")
    prev_line_num = 0
    for token, value, line_num in tokens:
        if line_num == prev_line_num:
            print(f"  | {token.name} - {value}")
        else:
            print(f"{prev_line_num+1}: {token.name} - {value}")

        prev_line_num = line_num

def print_msg(type, message):
    print(f"[green][{type}][/green]: {message}")

def print_error(message):
    print(f"[red][ERROR][/red]: {message}")
