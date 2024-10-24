from enum import Enum, auto
import argparse
import os

class BUILD_SYSTEM(Enum):
    MAKEFILE = auto()
    CMAKE    = auto()
    GRADLE   = auto()
    MAX      = auto()

class DependencyMapper:
    """
    This class is intended to be given a root folder and file
        format (such as makefile or CMakeLists.txt or build.gradle)
        and it will then create a map of dependencies of libraries.
        It can be helpful for finding circular dependencies.
    """


    def __init__(self, project_root : str, build_file : str, build_system : BUILD_SYSTEM) -> None:
        """
        __init__ Initializes the class to setup for processing

        :param project_root: Root directory to search underneath recursively
        :param build_file: Full file name (such as CMakeLists.txt or build.gradle)
        :param build_system: The build system used
        :return: None
        """
        self.root = project_root
        self.file = build_file
        self.build_system = build_system
        self.filelist = list()
        # Each library will have a list of dependencies
        self.dependency_list = dict(list())

        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file == build_file:
                    print(os.path.join(root, file))
                    # Append the path to the file list
                    self.filelist.append(os.path.join(root, file))

        # for filename in os.listdir(root):
        #     file_path = os.path.join(folder_path, filename)
        #     if os.path.isfile(file_path):
        #         with open(file_path, 'r') as file:
        #             content = file.read()
        #             print(content)
        return

    def start(self) -> None:

        match self.build_system:
            case BUILD_SYSTEM.MAKEFILE:
                self.process_make()
            case BUILD_SYSTEM.CMAKE:
                self.process_cmake()
            case BUILD_SYSTEM.GRADLE:
                self.process_gradle()
            case _:
                print("Invalid build system")


        return

    def process_make(self) -> None:
        """
        Searches make files and calls the map function
        """
        print("Unimplemented")

        self.map()

    def process_cmake(self) -> None:
        """
        Searches cmake files and calls the map function
        """
        print("Unimplemented")

        self.map()

    def process_gradle(self) -> None:
        """
        Searches gradle files and calls the map function
        """
        # Used to track if we are reading dependencies
        found_dependencies = False

        for build_file in self.filelist:
            # Create entry for this lib
            if build_file not in self.dependency_list:
                self.dependency_list[build_file] = list()
            # Read through and pull out dependencies
            with open(build_file, 'r') as file:
                for line in file:
                    # if the line is a dependency line, read and add to the dependency list
                    if line.find("dependencies") >= 0:
                        # Start reading after this
                        found_dependencies = True
                        continue
                    if found_dependencies:
                        # Check for the end
                        if line.find("}") > 0:
                            found_dependencies = False
                            break
                        dependency = line.strip()
                        print(dependency)
                        self.dependency_list[build_file].append(dependency)

        self.map()

    def map(self):
        """
        Creates the map output of the dependencies
        """
        # Create a https://pypi.org/project/py2puml/ output file
        with open('output.puml', 'w') as file:
            # Start the document
            file.write('@startuml py2puml.domain\n')
            file.write('!pragma useIntermediatePackages false\n')

            # Classes
            print("Writing Classes")
            for f in self.filelist:
                class_file = 'class ' + f
                print(class_file)
                file.write(class_file + '{\n')
                file.write('}\n')

            # Relationships
            print("Writing Dependencies")
            print(self.dependency_list)
            for d in self.dependency_list:
                print(d)
                base = d
                # Loop the list of dependencies
                for i in d:
                    pass
                    # dep_str = d + ' --|> ' + i
                    # print(dep_str)
                    # file.write(dep_str+'\n')

            # Close UML
            file.write('@enduml\n')
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser("DependencyMapper")
    parser.add_argument("root", help="Path to root project folder or . for cwd", type=str)
    parser.add_argument("file", help="File name and extension for each type of build file (such as CMakeLists.txt)", type=str)
    parser.add_argument("build_system", help="1 Make, 2 CMake, 3 Gradle", type=int)
    args = parser.parse_args()

    # Convert . to CWD
    if args.root == '.':
        args.root = os.getcwd()

    # Create the class to map dependencies
    lm = DependencyMapper(args.root, args.file, BUILD_SYSTEM(args.build_system))
    # Run the mapper
    lm.start()