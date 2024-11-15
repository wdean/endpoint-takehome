directories.py - script to implement endpoint coding assignment


USAGE:
    
    python directories.py [filename]

    directories has two modes of execution. If provided a filename argument, it will attempt to open the file and 
    run the command lines contained within. If no filename argument is give, it will prompt for the user to type in
    commands and read commands from stdin input until recieving the command "DONE".


IMPLEMENTATION NOTES:

    Commands are not case sensitive, but directory names are.

    Directory name "root" is reserved for the base root directory. This program will not allow the creation of any other
    directory in the tree named "root". It will interpret CREATE or MOVE target directories that start with "root/" as 
    attempts to create a new "root" directory under the base directory and will disallow it. The "root" directory name's
    only legal use is as the standalone target directory name of the MOVE command to move subdirectories directly under
    the base, I.E. "MOVE some/directory/tree root".

    The CREATE command will build the entire directory tree structure specified as necessary. For example, if base
    directory is currently empty, the command "CREATE foods/fruit/apple" will create the subdirectory "foods" under
    the base directory, then the directory "fruit" under "foods", and finally the directory "apple" under fruit. 
    Similarly, the MOVE command will build the specified target directory structure in similar fashion as necessary.

    The DELETE command will remove the entire subdirectory tree beneath the target directory.
