from modules.GameEnums import CellType

def convert_digit_to_cell_type(char):
        try:
            char = int(char)
            if char in range(26):
                return CellType(char)
        except ValueError:
            pass
        return None

def convert_line_to_strings(line):
    string_values = []
    for char in line.strip():
        cell_type = convert_digit_to_cell_type(char)
        if cell_type is not None:
            string_values.append(str(cell_type))
        else:
            print(f"Invalid digit: {char}")
    return string_values

def update_map():
    """
    This is called to write the map.txt file to the map.csv file in a way that is loadable by GameBoard
    """
    with open('levels\\beginner\\map.txt', 'r') as file:
                with open('levels\\beginner\\map.csv', 'w') as f:
                    for line in file:
                        string_list = convert_line_to_strings(line)
                        string_str = ','.join(string_list) + '\n'
                        f.write(string_str)