import random

class maze():
    #generiert eine 3 dimensionale tabelle/liste, wo x == int(dim_x), y == int(dim_y) und z == list([])
    def gen_cells(dim_x = 3, dim_y = 3):
        maze_cells = []
        empty_list = []
        for x in range(dim_x):
            y_cells = []
            for y in range(dim_y):
                y_cells.append(empty_list)
            maze_cells.append(y_cells)
        return maze_cells
    
    #legt die standart-werte für die dritte Dimension (z) fest
    #z enthält alle 4 Himmelsrichtungen pro Zelle, wo Norden == index(0), ..., Westen == index(3)
    #Was pro Index gespeichert wird ist, ob in diese Richtung der Rand liegt (d.h. index = False) oder ob dort eine andere Zelle liegt (index = None)
    def gen_possible_directions(cells):
            for x in range(len(cells)):
                for y in range(len(cells[0])):
                    directions = [None, None, None, None]
                    if x == 0:
                        directions[3] = False
                    elif x == len(cells)-1:
                        directions[1] = False
                    if y == 0:
                        directions[2] = False
                    elif y == len(cells[0])-1:
                        directions[0] = False
                    cells[x][y] = directions
            return cells

    #Hier wird das baumdiagramm generiert ()d.h. wo darf man später lang und wo liegen die Wände
    #Die Regeln für die generation finden sie in meinen Bewerbungsunterlagen
    def gen_connections(cells):
        #Diese funktion wählt eine neue Zelle aus falls das Programm aktuell fest steckt
        def find_next_cell(cells):
            for x in range(len(cells)):
                for y in range(len(cells[0])):
                    if True in cells[x][y]:
                        continue
                    dim_changer = [[0, 1], [1, 0],
                                [0, -1], [-1, 0]]
                    possible_connections = [[], [], []]
                    for index_dir in range(4):
                        if cells[x][y][index_dir] == None:
                            next_cell = [x, y]
                            for index_dim in range(2):
                                next_cell[index_dim] += dim_changer[index_dir][index_dim]
                            if True in cells[next_cell[0]][next_cell[1]]:
                                possible_connections[0].append(index_dir)
                                possible_connections[1].append(next_cell)
                    if len(possible_connections[0]) > 0:  
                        possible_connections[2].append(x)
                        possible_connections[2].append(y)           
                        return possible_connections
            return False
        current_cell = [random.randint(0, len(cells)-1), 
                        random.randint(0, len(cells[0])-1)]
        
        x = 5
        while x != 0:
            forced_connection = False
            directions = cells[current_cell[0]][current_cell[1]]
            #dim changer zeigt welche coordinaten sich bei einer Richtung verändern
            dim_changer = [[0, 1], [1, 0],
                           [0, -1], [-1, 0]]
            #Suche alle validen Richtungen und Zellen raus
            free_directions = [[], []]
            for index_dir in range(4):
                if directions[index_dir] == None:
                    next_cell = [current_cell[0], current_cell[1]]
                    for index_dim in range(2):
                        next_cell[index_dim] += dim_changer[index_dir][index_dim]
                    if True in cells[next_cell[0]][next_cell[1]]:
                        continue
                    free_directions[0].append(index_dir)
                    free_directions[1].append(next_cell)
            if len(free_directions[0]) == 0:
                free_directions = find_next_cell(cells)
                if free_directions == False:
                    x = 0
                    break
                current_cell = free_directions[2]
                forced_connection = True
            #Sucht sich die Richtung per Zufall aus
            random_index = random.randint(0, len(free_directions[0])-1)
            cells[current_cell[0]][current_cell[1]][free_directions[0][random_index]] = True
            #Spiegelt die Richtung der ersten Zelle auf die zweite 
            mirror_directions = [2, 3, 0, 1]
            if forced_connection == False:
                #Setzt neue Zelle auf zurzeitige Zelle
                #ändert die Richtung der neuen Zelle
                current_cell = free_directions[1][random_index]
                cells[current_cell[0]][current_cell[1]][mirror_directions[free_directions[0][random_index]]] = True
            else:
                forced_cell = free_directions[1][random_index]
                cells[forced_cell[0]][forced_cell[1]][mirror_directions[free_directions[0][random_index]]] = True
        return cells
        
    #Hier wird die 3 dimensionale Liste in Text umgewandelt
    #Erst werden die Wände und freie Wege generiert, während für die Ecken ein platzhalter (a) verwendet wird
    #Danach wird der Platzhalter (a) basierend auf umliegenden Wänden in eines der drei Symbole (1. - 2. ¦ 3. , 4. ')
    def convert_to_text(cells):
        buildingblocks = ["----", "    ", "¦", " ", "a", ",", "'"]
        maze_as_text = []
        #generiere standart labyrhint ohne ecken
        #ecken werden durch a ersetzt
        even_numbers = [0, 2, 4, 6, 8]
        max_x = len(cells)*2+1
        max_y = len(cells[0])*2+1
        for x in range(max_x):
            x_even = False
            if str(x)[-1] in str(even_numbers):
                x_even = True
            maze_as_text.append([])
            for y in range(max_y):
                y_even = False
                if str(y)[-1] in str(even_numbers):
                    y_even = True
                block = None
                if x_even and y_even:
                    block = buildingblocks[4]
                elif (not x_even) and (not y_even):
                    block = buildingblocks[1]
                elif x == 0:
                    block = buildingblocks[2]
                elif x == max_x-1:
                    block = buildingblocks[2]
                elif y == 0:
                    block = buildingblocks[0]
                elif y == max_y-1:
                    block = buildingblocks[0]
                elif x_even and (not y_even):
                    if cells[int(x/2-1)][int((y-1)/2)][1] == True:
                        block = buildingblocks[3]
                    else:
                        block = buildingblocks[2]
                elif (not x_even) and y_even:
                    if cells[int((x-1)/2)][int(y/2-1)][0] == True:
                        block = buildingblocks[1]
                    else:
                        block = buildingblocks[0]   
                maze_as_text[x].append(block)
        #labyrhint mit ecken       
        #ersetzt a durch ecken
        #finde umliegende vertikale Wände
        for x in range(max_x):
            for y in range(max_y):
                if maze_as_text[x][y] != "a":
                    continue
                vertical_walls = [False, False]
                if y < max_y-1:
                    if "¦" == maze_as_text[x][y+1]:
                        vertical_walls[0] = True
                if y > 0:
                    if "¦" == maze_as_text[x][y-1]:
                        vertical_walls[1] = True
                #ersetze a mit richtigem Symbol
                symbol = "-"
                if vertical_walls[0] and vertical_walls[1]:
                    symbol = buildingblocks[2]
                elif vertical_walls[0]:
                    symbol = buildingblocks[6]
                elif vertical_walls[1]:
                    symbol = buildingblocks[5]
                maze_as_text[x][y] = symbol
        return maze_as_text

    #Druckt das ganze Labyrinth in der richtigen reihenfolge    
    def print_maze(cells):
        #even_numbers = [0, 2, 4, 6, 8]
        #punkte = []
        #max_x = len(cells)
        #max_y = len(cells[0])
        #for index in range(2):
        #    searching = True
        #    while searching:
        #        rand_x = random.randint(1, max_x)
        #        rand_y = random.randint(1, max_y)
        #        if not (str(rand_x)[-1] in str(even_numbers)):
        #            if not (str(rand_y)[-1] in str(even_numbers)):
        #                searching = False
        #    punkte.append([rand_x, rand_y])
        #for i in range(2):
        #    cells[punkte[i][0]][punkte[i][1]] = " ++ "
        walls = []
        for y in range(len(cells[0])):
            line = ""
            for x in range(len(cells)):
                line += cells[-x-1][-y-1]
            walls.append(line)
        for wall in walls:
            print(wall)
            
    def generate(dim_x = 3, dim_y = 3):
        cells = maze.gen_cells(dim_x, dim_y)
        #print(cells)
        #print()
        cells_wdir = maze.gen_possible_directions(cells)
        #print(cells_wdir)
        #print()
        cells_wcon = maze.gen_connections(cells_wdir)
        #print(cells_wcon)
        #print()
        maze_as_text = maze.convert_to_text(cells_wcon)
        #print(maze_as_text)
        #print()
        maze.print_maze(maze_as_text)

maze.generate(10, 10)