from random import randint as rnt
from time import sleep

#...

#Die Äußere Klasse, welche alle Methoden und untergeordneten Klassen enthält
class Maze:
    def create_instance(cls, *values):
        return cls(*values)

    class Options:
        class Size:
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

            @staticmethod
            def standard():
                return Maze.create_instance(Maze.Options.Size, 5, 5)

        class Start_End:
            class Waypoint:
                def __init__(self, name: str, x: int = None, y: int = None):
                    self.name = name
                    self.x = x
                    self.y = y

            def __init__(self, generate: bool, inside:bool, waypoint1: Waypoint, waypoint2: Waypoint):
                self.generate = generate
                self.inside = inside
                self.waypoint1 = waypoint1
                self.waypoint2 = waypoint2

            @staticmethod
            def standard():
                waypoint1 = Maze.Options.Start_End.Waypoint("A")
                waypoint2 = Maze.Options.Start_End.Waypoint("B")
                return Maze.create_instance(Maze.Options.Start_End, True, True, waypoint1, waypoint2)

        class Convert:
            class Blocks:
                class Corners:
                    def __init__(self, up, right, down, left):
                        self.up = up
                        self.right = right
                        self.down = down
                        self.left = left

                    @staticmethod
                    def standard():
                        return Maze.create_instance(Maze.Options.Convert.Blocks.Corners, "'", "-", ",", "-")

                def __init__(self, wall: str, floor: str, corners: Corners):
                    self.wall = wall
                    self.floor = floor
                    self.corners = corners

                @staticmethod
                def standard():
                    corners = Maze.Options.Convert.Blocks.Corners.standard()
                    return Maze.create_instance(Maze.Options.Convert.Blocks, "|", "--", corners)

            def __init__(self, generate: bool, blocks: Blocks):
                self.generate = generate
                self.blocks = blocks

            @staticmethod
            def standard():
                blocks = Maze.Options.Convert.Blocks.standard()
                return Maze.create_instance(Maze.Options.Convert, True, blocks)

        def __init__(self, size: Size, start_end: Start_End, convert: Convert):
            self.size = size
            self.start_end = start_end
            self.convert = convert

        @staticmethod
        def standard():
            size = Maze.Options.Size.standard()
            start_end = Maze.Options.Start_End.standard()
            convert = Maze.Options.Convert.standard()
            return Maze.create_instance(Maze.Options, size, start_end, convert)

    class Build:
        class Structure:
            class Base:
                class Cell:
                    def __init__(self, x: int, y: int, max_x = None, max_y = None):
                        self.x = x
                        self.y = y
                        self.up = None if y != 1 or max_y == None else False
                        self.right = None if x != max_x else False
                        self.down = None if y != max_y else False
                        self.left = None if x != 1 or max_x == None else False

                    def __str__(self):
                        return f"--Cell--\nx/y = {self.x}|{self.y}\ndirections:{self.up, self.right, self.down, self.left}"

                    @staticmethod
                    def generate(x, y, max_x, max_y):
                        return Maze.create_instance(Maze.Build.Structure.Base.Cell, x, y, max_x, max_y)

                class Row:
                    def __init__(self, row: list["Maze.Build.Structure.Row.generate"]):
                        self.row = row

                    def __str__(self):
                        row = self.row
                        return f"Cells in row: {len(row)}"

                    @staticmethod
                    def generate(size_options: "Maze.Options.Size", current_y) -> list["Maze.Build.Structure.Cell"]:
                        if not isinstance(size_options, Maze.Options.Size):
                            raise TypeError(f"")
                        max_x, max_y = size_options.x, size_options.y 
                        row = []
                        for x in range(max_x):
                            x += 1
                            row.append(Maze.create_instance(Maze.Build.Structure.Base.Cell, x, current_y, max_x, max_y))
                        return Maze.create_instance(Maze.Build.Structure.Base.Row, row)

                def generate(size_options: "Maze.Options.Size"):
                    if not isinstance(size_options, Maze.Options.Size):
                        raise TypeError(f"")
                    max_y = size_options.y
                    base = []
                    for y in range(max_y):
                        y += 1
                        base.append(Maze.Build.Structure.Base.Row.generate(size_options, y))
                    return base
        
            class Path:
                def generate():
                    ...

            def __init__(self, base: "Maze.Build.Structure.Base.generate", path: list["Maze.Build.Structure.Path"]):
                    self.base = base
                    self.path = path

            @staticmethod
            def generate(size_options: "Maze.options.Size", start_end_options):
                #1. Generate Base
                base = Maze.Build.Structure.Base.generate(size_options)
                #2. Generate Paths
                return Maze.create_instance(Maze.Build.Structure, base, base)

        class Convert:
            @staticmethod
            def generate(options, structure):
                ...
                return "This the convert"

        #add other pecification
        def __init__(self, structure: Structure, structure_text: Convert = None, solution = None, solution_text = None):
            self.structure = structure
            self.structure_text = structure_text
            self.solution = solution
            self.solution_text = solution_text

        @staticmethod
        def generate(options: "Maze.Options"):
            structure = Maze.Build.Structure.generate(options.size, options.start_end)
            structure_text = Maze.Build.Convert.generate(options.convert, structure)
            solution = None
            solution_text = None
            return Maze.create_instance(Maze.Build, structure, structure_text, solution, solution_text)

    class Info:
        @staticmethod
        def generate():
            return "Info:"

    #Enthält alle Daten zur Instanz der Klasse Maze() 
    def __init__(self, options: Options, build: Build, info: Info):
        self.options = options
        self.build = build
        self.info = info

    @staticmethod
    def generate(options: "Maze.Options"):
        build = Maze.Build.generate(options)
        info = Maze.Info.generate()
        return Maze.create_instance(Maze, options, build, info)

options = Maze.Options.standard()
my_maze = Maze.generate(options)
base = my_maze.build.structure.base
print(base,"\n")
for row in base:
    print(row)
    for cell in row.row:
        print(cell)