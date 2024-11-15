import sys


LEVEL_INDENT = 2
CREATE_COMMAND = "create"
DELETE_COMMAND = "delete"
MOVE_COMMAND = "move"
LIST_COMMAND = "list"
DONE_COMMAND = "done"
BASE_DIR_NAME = "root"

base_dir = (BASE_DIR_NAME, [])


def find_missing_path_element(path):
    """
    Navigates a path string and looks for the first element (nearest root) that doesn't
    exist in the current directory structure, if any

            Parameters:
                path (str): a directory path and name
            
            Returns:
                element (str): the path dir element that did not exist in the structure, 
                or empty string if the full path exists
    """
    path_elements = path.split("/")
    current_dir = base_dir

    for path_element in path_elements:
        subdir_match_found = False
        for subdir in current_dir[1]:
            if subdir[0] == path_element:
                subdir_match_found = True
                current_dir = subdir
                break
        if not subdir_match_found:
            return path_element
    
    return ""


def validate_create(tokens):
    """
    Validates the creation command. Validates correct number of arguments, 
    and verifies new directory doesn't already exist.

            Parameters:
                tokens (list): creation command line arguments
            
            Returns:
                is_valid (boolean): whether the command is determined valid or not
    """
    if len(tokens) != 1:
        print("Usage: CREATE dirname")
        return False
    
    if (
        tokens[0] == BASE_DIR_NAME 
        or tokens[0].startswith(BASE_DIR_NAME + "/") 
        or tokens[0].find("/" + BASE_DIR_NAME) != -1
    ):
        print(BASE_DIR_NAME, "is reserved for the base directory and cannot be created")
        return False

    if find_missing_path_element(tokens[0]) == "":
        print("Cannot create", tokens[0], "-", tokens[0], "already exists")
        return False
    
    return True


def validate_move(tokens):
    """
    Validates the move command. Validates correct number of arguments, 
    verifies that the directory to move exists, and verifies the new path and
    directory resulting does not already exist.

            Parameters:
                tokens (list): move command line arguments
            
            Returns:
                is_valid (boolean): whether the command is determined valid or not
    """
    if len(tokens) != 2:
        print("Usage: MOVE moving_dirname target_location_dirname")    
        return False
    
    if tokens[0] == BASE_DIR_NAME:
        print("Cannot move root directory")
        return False
    
    missing_path_element = find_missing_path_element(tokens[0])
    if missing_path_element != "":
        print("Cannot move", tokens[0], "to", tokens[1], "-", missing_path_element, "does not exist")
        return False

    if (
        tokens[1].startswith(BASE_DIR_NAME + "/")
        or tokens[1].find("/" + BASE_DIR_NAME) != -1
    ):
        print("Directory name", BASE_DIR_NAME, "is reserved for the base directory only")
        return False
    
    moving_dir_name = tokens[0].split("/")[-1]
    if tokens[1] == BASE_DIR_NAME:
        new_dir_name = moving_dir_name
    else:
        new_dir_name = tokens[1] + "/" + moving_dir_name
    
    if find_missing_path_element(new_dir_name) == "":
        print("Cannot move", tokens[0], "to", tokens[1], "- path", new_dir_name, "already exists")
        return False
    
    return True


def validate_delete(tokens):
    """
    Validates the delete command. Validates correct number of arguments, 
    and verifies target directory exists.

            Parameters:
                tokens (list): deletion command line arguments
            
            Returns:
                is_valid (boolean): whether the command is determined valid or not
    """
    if len(tokens) != 1:
        print("Usage: DELETE dirName")
        return False
    
    if tokens[0] == BASE_DIR_NAME:
        print("Cannot delete root directory")
        return False
    
    missing_path_element = find_missing_path_element(tokens[0])
    if missing_path_element != "":
        print("Cannot delete", tokens[0], "-", missing_path_element, "does not exist")
        return False
    
    return True    


def validate_list(tokens):
    """
    Validates the list command. Verifies no additional arguments present.

            Parameters:
                tokens (list): command line arguments
            
            Returns:
                is_valid (boolean): whether the command is determined valid or not
    """
    if len(tokens) != 0:
        print("Usage: LIST")
        return False
    return True


def create_dir(dir_name):
    """
    Creates a new directory. If passed directory path has multiple elements, will
    create all elements as necessary. Can also be used to simply locate a directory
    within the tree and return it

            Parameters:
                dir_name (str): the directory path and name
            
            Returns:
                current_dir (tuple): the newly created (or located) directory
    """
    path_elements = dir_name.split("/")
    current_dir = base_dir

    for path_element in path_elements:
        subdir_match_found = False
        for subdir in current_dir[1]:
            if subdir[0] == path_element:
                subdir_match_found = True
                current_dir = subdir
                break
        if not subdir_match_found:
            new_subdir = (path_element, [])
            current_dir[1].append(new_subdir)
            current_dir = new_subdir
    return current_dir

def delete_dir(dir_name):
    """Deletes a directory from the directory tree, and returns the deleted directory. 
    Any subdirectory tree underneath the target directory will also be deleted.

            Parameters:
                dir_name (str): the target directory path and name
            
            Returns:
                deleted_dir (tuple): the deleted directory
    """
    path_elements = dir_name.split("/")
    current_dir = base_dir

    for path_element in path_elements[:-1]:
        for subdir in current_dir[1]:
            if subdir[0] == path_element:
                current_dir = subdir
                break
    
    subdirs = current_dir[1]
    for i in range(len(subdirs)):
        subdir_name = subdirs[i][0]
        if path_elements[-1] == subdir_name:
            deleted_dir = subdirs[i]
            del subdirs[i:i+1]
            break
    return deleted_dir


def move_dir(move_dir_name, target_dir_name):
    """
    Moves an existing directory. If target directory path has elements not existing, will
    create new element directories as necessary

            Parameters:
                move_dir_name (str): the directory path and name of the directory to be moved
                target_dir_name (str): the target location directpry to move the subject directory under
    """
    if target_dir_name == BASE_DIR_NAME:
        target_dir = base_dir
    else:
        target_dir = create_dir(target_dir_name)

    move_dir = delete_dir(move_dir_name)
    target_dir[1].append(move_dir)


def list(dir=base_dir, depth=0):
    """
    Prints listing of directories to stdout. Each directory is followed by its subdirectories.
    Directories are indented from their parent and alphabetized amongst their siblings

            Parameters:
                dir (tuple): the directory to list, base_dir by default
                depth (int): the current depth of the directory relative to the root directory 
                             passed in the initial call (or base_dir by default) 
    """
    for subdir in sorted(dir[1]):
        print((" " * depth * LEVEL_INDENT) + subdir[0])
        list(subdir, depth + 1)


validators = {
    CREATE_COMMAND : validate_create, 
    MOVE_COMMAND : validate_move,
    DELETE_COMMAND : validate_delete,
    LIST_COMMAND: validate_list
}


processors = {
    CREATE_COMMAND :create_dir, 
    MOVE_COMMAND: move_dir,
    DELETE_COMMAND: delete_dir,
    LIST_COMMAND: list
}


def process_input_line(input_line):
    """
    Splits a command line input into its command and argument tokens, then looks up and executes
    valdation and processing functions for the command as necessary

            Parameters:
                input_line (str): one line of input from command line or file
    """
    print(input_line)
    tokens = input_line.split()
    command = tokens[0].lower()
    if command not in validators:
        if command == DONE_COMMAND:
            print("If you are finished, enter 'DONE' without further text arguments")
        else:
            print(command, "is not a recognized command. Supported commands are 'CREATE', 'MOVE', 'DELETE', or 'LIST'")
        return
    
    validator = validators[command]
    if validator(tokens[1:]):
        processor = processors[command]
        processor(*tokens[1:])


def process_from_stdin():
    """
    Presents a command line interface for entering commands through stdin and passes 
    commands to process_input_line

    """
    print("Enter your commands. Type 'DONE' when finished.")
    while True:
        print("Command: ", end="")
        input_line = input().strip()
        if input_line.lower() == DONE_COMMAND:
            return
        
        process_input_line(input_line)


def process_from_file(file_name):
    """
    Attempts to open a file, read the commands contained within and pass them to
    process_input_line

            Parameters:
                file_name: name of file to open and read from. Can be a relative or absolute path
    """
    try:
        with open(file_name, errors="strict") as file:
            lines = file.read().strip().split("\n")
    except FileNotFoundError:
        print("File", file_name, "was not found")
        return
    except Exception:
        print("Error attempting to open and read text from file ", file_name)
  
    for line in lines:
        line = line.strip()
        if line.lower().startswith(DONE_COMMAND):
            continue
        process_input_line(line)
    

if __name__ == "__main__":
    """
    If filename argument is present in python command, attempt to read and process
    command from file. Otherwise present a command line interface for entering commands
    via stdin
    """
    if len(sys.argv) > 2:
        print("Usage: python directories.py [datafile]")
        exit()
    
    if len(sys.argv) == 2:
        data_file_name = sys.argv[1]
        process_from_file(data_file_name)
    else:
        process_from_stdin()
    
