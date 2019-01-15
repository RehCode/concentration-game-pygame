import random
import pygame, sys, time

# inicia pygame y el clock
pygame.init()
fpsClock = pygame.time.Clock()
# Set the width and height of the screen [width,height]
size_screen = [485, 390]
windowSurfaceObj = pygame.display.set_mode(size_screen)
pygame.display.set_caption("Concentration")

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

# Define las variables
NUMBER_OF_TILES = 20
TILES_PER_ROW = 5
picked_tiles = []
# Genera los pares de cartas
tiles = [x for x in range(NUMBER_OF_TILES//2)] * 2

# Carga las imagenes
tile_size = [91, 91]
tiles_img_obj = []
for i in range(11):
    nombre_archivo_imagen = "{0}.png".format(i)
    imagen_obj = pygame.image.load(nombre_archivo_imagen).convert()
    tiles_img_obj.append(imagen_obj)

def genera_coords_tiles(tiles):
    # Genera la lista de cartas con sus coordenadas e imagen
    tiles = tiles
    gap_size = 5
    coords_tiles = []
    # Suffle de cartas
    random.shuffle(tiles)
    for i in range(NUMBER_OF_TILES):
        tile_img_x = gap_size+(tile_size[0]+gap_size) * (i%TILES_PER_ROW)
        tile_img_y = gap_size+(tile_size[1]+gap_size) * (int(i/TILES_PER_ROW))
        tile_img = 10 # numero de la imagen para dibujar 10 => signo ?
        tile_num = tiles[i] # numero interior de la tarjeta
        coords_tiles.append([tile_img_x, tile_img_y, tile_img, tile_num])
    return coords_tiles

def dibuja_tiles():
    windowSurfaceObj.fill(white)
    for tile in coords_tiles:
        windowSurfaceObj.blit(tiles_img_obj[tile[2]], (tile[0], tile[1]))
    pygame.display.update()


def verifica_click():
    global coords_tiles

    pos = pygame.mouse.get_pos()
    
    for tile in coords_tiles:
        bool_x = (pos[0] >= tile[0] and pos[0] <= tile[0]+91)
        bool_y = (pos[1] >= tile[1] and pos[1] <= tile[1]+91)
        if bool_x and bool_y:
            # muestra la tarjeta en click
            index = coords_tiles.index(tile)
            coords_tiles[index][2] = tile[3]
            dibuja_tiles()

            revisa_picked(tile)


def revisa_picked(tomada):
    global picked_tiles
    global coords_tiles

    if not tomada in picked_tiles:
        picked_tiles.append(tomada)

    if len(picked_tiles) >= 2:
        # si son iguales son borradas de la lista de coordenadas
        if picked_tiles[0][3] == picked_tiles[1][3]:
            # Son iguales"
            coords_tiles.remove(picked_tiles[0])
            coords_tiles.remove(picked_tiles[1])
            picked_tiles = []

        # si no son iguales se voltean y genera nueva lista para tomar
        else:
            # No son iguales
            picked_index_1 = coords_tiles.index(picked_tiles[0])
            picked_index_2 = coords_tiles.index(picked_tiles[1])
            pygame.time.wait(1000)
            # reset
            coords_tiles[picked_index_1][2] = 10
            coords_tiles[picked_index_2][2] = 10
            picked_tiles = []


# genera una lista con las coordenadas y elementos de las tarjetas
coords_tiles = genera_coords_tiles(tiles)

#Loop until the user clicks the close button.
done=False

# -------- Main Program Loop -----------
while done==False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            verifica_click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_r:
                # pygame.time.wait(1000)
                coords_tiles = genera_coords_tiles(tiles)
                dibuja_tiles


    if coords_tiles == []:
        coords_tiles = genera_coords_tiles(tiles)

    dibuja_tiles()
    

    # Limit to 20 frames per second
    fpsClock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()