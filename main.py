from random import randint as rnt
from math import ceil as up
from math import floor as flo

#NOTE Dazu gekommen sind einmal die Klasse Solve (maze.Solve) mit der funktion hand_on_wall(). Dazu sind die funktionen solve (maze.solve()) und gen_waypoints (maze.gen_waypoints())
#Zudem wird das Labyrinth nicht mehr gespiegelt gedruckt (z. 390)

class maze():
    #Diese Klasse enthält (in Zukunft) mehrere Algorithmen mit denen das Labyrinth gelöst werden kann
    class Solve():
        #Hand_on_wall ist eine Methode, bei der man immer an einer Wand entlang geht, bist man am Ende ankommt
        #Diese Methode klappt allerdings nur wenn es sich um ein perfektes labyrinth (immer nur ein möglicher weg von A nach B) handelt!
        def hand_on_wall(cells, waypoints, start_with = 0):
            #Die funktion search() geht stück für stück durch das labyrinth, bis es zum Ziel gelangt. Bleibt er stecken, bewegt er sich wieder zurück bis zu einer Kreuzung
            def search(solution, finished = False):
                #Der Code bewegt sich von Zelle zu Zelle. Die Startzelle ist in diesem Falle der erste Wert von Solutions (als der Punkt A)
                cc_coords = solution[-2][0]
                cc_dirs = solution[-2][1]
                #Hier ist eine Fortbeweguns-matrix
                #Sie wird verwendet um sich von einer Zelle zur anderen zu bewegen
                dirs_matrix = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                #Hier ist eine Matrix, welche Himmelsrichtungen (0, 1, 2, 3) in gegenüberliegende Richtungen ändert -> z.B. index 0 -> 2, index 2 -> 0, ...
                dir_matrix = [2, 3, 0, 1]
                #Schaut ob man sich von dieser Zelle aus fortbewegen kann, d.h. "Ist ein True wert in den Richtungen der Zelle?"
                #falls ja:
                if True in cc_dirs:
                    #sucht systematisch den ersten True wert der Zelle und bewegt sich in diese Richtung
                    for i in range(4):
                        if cc_dirs[i] == True:
                            #print(solution)
                            #Damit unser Code und wir wissen, wo wir bereits waren, wird jeder True Wert, wo wir uns lang begeben, zu str("") geändert -> z.B. index 0, richtungen (True, True, False, False) -> ("", True, False, False) ->
                            #                                                                                                                                                      ^^^^^^                        ^^^^
                            solution[-2][1][i] = ""
                            #print(solution)
                            #Hier werden mithilfe der Fortbewebungsmatrix die Koordinaten der nächsten Zelle berechnet
                            #Zudem holen wir uns die Richtungen der nächsten Zelle und setzen den True Wert, wo wir hergekommen sind, ebenfalls auf ""
                            nc_coords = [cc_coords[0] + dirs_matrix[i][0], cc_coords[1] + dirs_matrix[i][1]]
                            nc_dirs = cells[nc_coords[0]][nc_coords[1]]
                            nc_dirs[dir_matrix[i]] = ""
                            #Dieser Code sagt dass die Lösung gefunden wurde
                            #Der True wert sagt dem Code dass er aufhören soll weiter zu suchen
                            if nc_coords == solution[-1]:
                                #raise ValueError("Found solution")
                                return solution, True
                            #print(cc_coords)
                            #print(dirs_matrix[i])
                            #print(next_cell_coords)
                            #Die Zelle zu der wir uns bewegt haben wird in Solutions hinzugefügt
                            solution.insert(-1, [nc_coords, nc_dirs])
                            #print(solution)
                            #Nun starten wir die funktion innerhalb der funktion erneut, mit einer erweiterten solution variable
                            solution, finished = search(solution, finished)
                            #Dieser Code stoppt die Anwendung wenn der Richtige Weg gefunden wurde, d.h. Es wurde vorher True zurückgegeben
                            if finished == True:
                                return solution, finished
                            #Falls der Weg aber noch nicht gefunden wurde, wird der Wert "", also wo wir lang gegangen sind, auf False geändert
                            #Wieso wir flasche Wege bzw. Richtungen nicht auf "" lassen, liegt daran, dass wir sonst später Probleme haben, den richtigen weg in zeichen zu ändern.
                            else:
                                for s in range(len(solution)-1):
                                    if solution[s][0][0] == cc_coords[0] and solution[s][0][1] == cc_coords[1]:
                                        solution[s][1][i] == False
                    solution.pop(-2)
                #falls nein
                #Ist kein True Wert in dieser Zelle vorhanden, wird sie von dem Code komplett entfernt und von der Vorherigen Zelle wird der Wert "" ebenfalls auf False geändert
                #Dadurch vermeiden wir später Probleme bei flaschen Wegen und dem Konvertieren zu Text
                else:
                    #Entfernt falsche Zelle
                    solution.pop(-2)
                    #Ändert den "" Wert auf False
                    for i in range(4):
                        if solution[-2][1][i] == "":
                            solution[-2][1][i] = False
                #gibt die Solution (Lösung) zum Labyrinth zurück
                return solution, False
            #Der code hier bereitet die Daten für die search() vor
            start = waypoints[start_with]
            start_dirs = cells[start[0]][start[1]]
            end = waypoints[-start_with-1]     
            #Der startwert (A) und Endwert (B) werden in einer Varaible namens solution gespeichert
            solution = [[start, start_dirs], end]

            #hier wird search aufgerufen
            solution, x = search(solution)
            #print(solution)
            return solution
        
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
    
    #legt die standart-werte fÃ¼r die dritte Dimension (z) fest
    #z enthÃ¤lt alle 4 Himmelsrichtungen pro Zelle, wo Norden == index(0), ..., Westen == index(3)
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

    #Hier wird das baumdiagramm generiert ()d.h. wo darf man spÃ¤ter lang und wo liegen die WÃ¤nde
    #Die Regeln fÃ¼r die generation finden sie in meinen Bewerbungsunterlagen
    def gen_connections(cells):
        #Diese funktion wÃ¤hlt eine neue Zelle aus falls das Programm aktuell fest steckt
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
        current_cell = [rnt(0, len(cells)-1), 
                        rnt(0, len(cells[0])-1)]
        
        x = 5
        while x != 0:
            forced_connection = False
            directions = cells[current_cell[0]][current_cell[1]]
            #dim changer zeigt welche coordinaten sich bei einer Richtung verÃ¤ndern
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
            random_index = rnt(0, len(free_directions[0])-1)
            cells[current_cell[0]][current_cell[1]][free_directions[0][random_index]] = True
            #Spiegelt die Richtung der ersten Zelle auf die zweite 
            mirror_directions = [2, 3, 0, 1]
            if forced_connection == False:
                #Setzt neue Zelle auf zurzeitige Zelle
                #Ã¤ndert die Richtung der neuen Zelle
                current_cell = free_directions[1][random_index]
                cells[current_cell[0]][current_cell[1]][mirror_directions[free_directions[0][random_index]]] = True
            else:
                forced_cell = free_directions[1][random_index]
                cells[forced_cell[0]][forced_cell[1]][mirror_directions[free_directions[0][random_index]]] = True
        return cells

    def gen_waypoints(cells, gen_waypoints):
        random_waypoint = lambda x, y: [rnt(0, max_x-1), rnt(0, max_y-1)]
        def possible_coords(cells, waypoint1, locked, optional):
            locked_coords = []
            for i in range(2):
                locked_coords.append([waypoint1[i]-locked[i], waypoint1[i]+locked[i]])
            optional_coords = []
            for i in range(2):
                optional_coords.append([waypoint1[i]-optional[i], waypoint1[i]+optional[i]])
            #print("-- important --")
            #print("locked", locked_coords)
            #print("optio", optional_coords)

            coords = []
            for x in range(len(cells)):
                for y in range(len(cells[0])):
                    #print(f"x: {x}, y: {y}")
                    #print(f"x > {locked_coords[0][0]}")
                    if x >= locked_coords[0][0] and x <= locked_coords[0][1]:
                        #print(f"x is between {locked_coords[0][0]}, x ,{locked_coords[0][1]}")
                        if y >= locked_coords[1][0] and y <= locked_coords[1][1]:
                            #print(f"y is between {locked_coords[1][0]}, y ,{locked_coords[1][1]}")
                            continue
                    chance = 2
                    if x >= optional_coords[0][0] and x <= optional_coords[0][1]:
                        if x >= optional_coords[0][0] and x <= optional_coords[0][1]:
                            chance = 1
                    for i in range(chance):
                        coords.append([x, y])
            return coords

        distance = lambda x, y, divider, func: [func(x/divider), func(y/divider)]
        if type(gen_waypoints) == int:
            waypoint_option = [1]
            if gen_waypoints in waypoint_option:
                print("Accepted waypoint value")
                max_x, max_y = len(cells), len(cells[0])
                waypoints = [random_waypoint(max_x, max_y)]
                #print(waypoints)
                lock_distance = distance(max_x, max_y, 3, flo)
                #print("lock", lock_distance)
                optional_distance = distance(max_x, max_y, 2, up)
                #print("opt", optional_distance)
                #print(lock_distance, optional_distance)

                coords2 = possible_coords(cells, waypoints[0], lock_distance, optional_distance)
                waypoint2 = coords2[rnt(0, len(coords2)-1)]
                waypoints.append(waypoint2)
                return waypoints
            else:
                raise ValueError(f"gen_waypoints value ({gen_waypoints}) can only be False or one of the following values {waypoint_option}")
        else:
            return None

    #Hier wird die 3 dimensionale Liste in Text umgewandelt
    #Erst werden die WÃ¤nde und freie Wege generiert, wÃ¤hrend fÃ¼r die Ecken ein platzhalter (a) verwendet wird
    #Danach wird der Platzhalter (a) basierend auf umliegenden WÃ¤nden in eines der drei Symbole (1. - 2. Â¦ 3. , 4. ')
    def convert_to_text(cells, waypoints):
        buildingblocks = ["----", "    ", "Â¦", " ", "a", ",", "'"]
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
                #print(maze_as_text)   
                maze_as_text[x].append(block)
        #print(maze_as_text)
        #labyrhint mit ecken       
        #ersetzt a durch ecken
        #finde umliegende vertikale WÃ¤nde
        for x in range(max_x):
            for y in range(max_y):
                if maze_as_text[x][y] != "a":
                    continue
                vertical_walls = [False, False]
                if y < max_y-1:
                    if "Â¦" == maze_as_text[x][y+1]:
                        vertical_walls[0] = True
                if y > 0:
                    if "Â¦" == maze_as_text[x][y-1]:
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
        #print(maze_as_text)
        if type(waypoints) == list:
            #print(waypoints)
            points = ["A", "B"]
            for i in range(2):
                maze_as_text[waypoints[i][0]*2+1][waypoints[i][1]*2+1] = f" {points[i]}  "
        return maze_as_text

    #Dieser Code startet den Lösungsprozess des Labyrinths
    #Die Variable start_with erlaubt den nutzer zu wählen ob der Algorithmus von A nach B (starts_with = 0) sucht oder von B nach A (starts_with = 1)
    def solve(cells, waypoints, maze_text, show_answer = True, start_with = 0):
        #blocks = ["â", "â", "â", "â"]
        #blocks_clock = ["â±", "â¬ ", "â¬", "â°"]
        #blocks_c_clock = ["â¬", "â² ", "â³", "â¬"]

        #Prüft ob der Nutzer eine Lösung zum Labyrinth will oder nicht
        if show_answer == True:
            #Eine weitere Matrix, welche zwei Richtungsangaben in Zeichen umwandelt
            #Diese Zeichen hier sind die unterschiedlichen Pfeile, werden aber im Code anderes dargestellt
            block_matrix = [
                ["", "â³", "â", "â² "],
                ["â¬", "", "â¬", "â"],
                ["â", "â±", "", "â°"],
                ["â¬", "â", "â¬ ", ""]
                ]
            #Eine weitere Matrix welche Himmelsrictungen (0, 1, 2, 3) in gegenüberliegende Richtungen umwandelt
            dir_matrix = [2, 3, 0, 1]
            print(block_matrix)
            #Fürt den Algorithmus hand_on_wall aus (maze.Solve.hand_on_wall())
            solution = maze.Solve.hand_on_wall(cells, waypoints, start_with)
            print(solution)

            #Nachdem der richtige Weg generiert wurde, wird die Variable maze_text bearbeitet, welche den Konvertierten Text des Labyrinths enthält
            #Der Code sucht die Zellen vom Lösungsweg raus und nutzt die block_matrix um die Richtungen in Zeichen umzuwandeln, welche dann an der richtigen stelle eingesetzt werden
            for i in range(len(solution)-1):
                if i == 0:
                    for j in range(4):
                        if solution[0][1][j] == "":
                            start = dir_matrix[j]
                            break
                else:
                    for j in range(4):
                        if j == start:
                            continue
                        elif solution[i][1][j] == "":
                            end = j
                            break
                    print(i,"st", start, "till", end)
                    print("-->", solution[i][1])
                    coords = solution[i][0]
                    x, y = coords[0], coords[1]
                    block = block_matrix[start][end]
                    space = " "
                    if len(block) == 1:
                        space = "  "
                    maze_text[int(x*2+1)][y*2+1] = f"{space}{block} "

                    start = dir_matrix[end]
        return maze_text

    #Druckt das ganze Labyrinth in der richtigen reihenfolge    
    def print_maze(cells):
        #even_numbers = [0, 2, 4, 6, 8]
        #punkte = []
        #max_x = len(cells)
        #max_y = len(cells[0])
        #for index in range(2):
        #    searching = True
        #    while searching:
        #        rand_x = rnt(1, max_x)
        #        rand_y = rnt(1, max_y)
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
                line += cells[x][-y-1] #hier war ein bug -> cells[-x-1][-y-1], dies dreht aber den x Wert in einen negativen index um, obwohl der code das x von vorne nach hinten drucken sollte
            walls.append(line)
        for wall in walls:
            print(wall)
            
    def generate(dim_x = 3, dim_y = 3, waypoint_type = False, show_answer = False):
        if waypoint_type == False and show_answer != False:
            raise ValueError(f"Cant show answer if no waypoints are available!")
        cells = maze.gen_cells(dim_x, dim_y)
        print(cells)
        print()
        cells_wdir = maze.gen_possible_directions(cells)
        print(cells_wdir)
        print()
        cells_wcon = maze.gen_connections(cells_wdir)
        print(cells_wcon)
        print()

        waypoints = maze.gen_waypoints(cells_wcon, waypoint_type)
        print(waypoints)
        print()

        maze_as_text = maze.convert_to_text(cells_wcon, waypoints)
        print(maze_as_text)

        maze_as_text = maze.solve(cells_wcon, waypoints, maze_as_text, show_answer, 0)

        #1. Deffiniere 2 ZuffÃ¤llig generierte Koordinaten (Start) und (Ziel)
        #2. Zeige in den beiden Koordinaten einen Marker fÃ¼r Start (A) und Ziel (B) an
        #3. Erstelle einen suchalgorythmuss der einen weg vom Start zum Ziel sucht
        #4. zeige den weg mittels Folgender Zeichen an
        #print("ââââ")
        #5. zeige in den "ecken" folgende Pfeile an:
        #print("â±â¬ â¬â°")
        #print("â¬â² â³â¬")
        maze.print_maze(maze_as_text)

maze.generate(4, 4, 1, True)
print()
