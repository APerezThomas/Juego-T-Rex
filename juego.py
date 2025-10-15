import pygame
import random
import sys
import constantes as cons
import clases as cls
    

def superficie_animacion(superficie,velocidad_juego):
    #Genero la animacion de superfie con una axuliar para simular una animacion "circular"
    superficie.restar_x(velocidad_juego)
    if superficie.get_x_aux() < 0 - (cons.VENTANA_X/2):
        superficie.set_x_aux(cons.VENTANA_X)
    if superficie.get_x() < 0 - (cons.VENTANA_X/2):
        superficie.set_x(cons.VENTANA_X)
        
    superficie.dibujar_superficie_mov()

def agregar_obstaculos_a_lista( obstaculos, ventana, animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble):
    # Se generan de manera al azar los obstaculos con distintas caracteristicas
    num = random.randint(0,4)
    if num == 0:
        obstaculos.append(cls.Pajaro(ventana,cons.COMIENZO_OBSTACULO_X,
                                     cons.COMIENZO_PAJARO_ALTO_Y, animaciones_pajaro))
    elif num == 1:
        obstaculos.append(cls.Pajaro(ventana,cons.COMIENZO_OBSTACULO_X,
                                     cons.COMIENZO_PAJARO_BAJO_Y, animaciones_pajaro))
    elif num == 2:
        tipo_cactus_chico = random.choice(tipos_cactus_chicos)
        obstaculos.append(cls.Cactus(ventana,cons.COMIENZO_OBSTACULO_X,
                                     cons.COMIENZO_CACTUS_CHICO_Y,
                                     cons.ANCHO_CACTUS_CHICO,
                                     cons.ALTO_CACTUS_CHICO,
                                     cons.ANCHO_CACTUS_CHICO_HITBOX,
                                     cons.ALTO_CACTUS_CHICO_HITBOX,tipo_cactus_chico))
    elif num == 3:
        tipo_cactus_grande = random.choice(tipos_cactus_grandes)
        obstaculos.append(cls.Cactus(ventana,cons.COMIENZO_OBSTACULO_X,
                                     cons.COMIENZO_CACTUS_GRANDE_Y,
                                     cons.ANCHO_CACTUS_GRANDE,
                                     cons.ALTO_CACTUS_GRANDE,
                                     cons.ANCHO_CACTUS_GRANDE_HITBOX,
                                     cons.ALTO_CACTUS_GRANDE_HITBOX,tipo_cactus_grande))
    elif num == 4:
        tipo_cactus_grande_doble = random.choice(tipos_cactus_grandes_doble)
        obstaculos.append(cls.Cactus(ventana,cons.COMIENZO_OBSTACULO_X,
                                     cons.COMIENZO_CACTUS_GRANDE_DOBLE_Y,
                                     cons.ANCHO_CACTUS_GRANDE_DOBLE,
                                     cons.ALTO_CACTUS_GRANDE_DOBLE,
                                     cons.ANCHO_CACTUS_GRANDE_DOBLE_HITBOX,
                                     cons.ALTO_CACTUS_GRANDE_DOBLE_HITBOX,tipo_cactus_grande_doble))    

def cargar_pngs( animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble):

    # Cargo los png's del proyecto
    for i in  range(2):
        img = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//obstaculos//Pajaro_{i}.png")
        animaciones_pajaro.append(img)
    for i in range(2):
        img = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//obstaculos//Cactus_chico_{i}.png")
        tipos_cactus_chicos.append(img)
    for i in range(2):
        img = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//obstaculos//Cactus_grande_{i}.png")
        tipos_cactus_grandes.append(img)
    for i in range(1):
        img = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//obstaculos//Cactus_grande_doble_{i}.png")
        tipos_cactus_grandes_doble.append(img)
    
    aviso_go = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//escenario//Aviso_GO.png")
    boton_restart = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//escenario//Boton_restars.png")
    nube = pygame.image.load(f"C://Users//PC//Desktop//Practica//sprites//escenario//Nube.png")
    font = pygame.font.Font("C://Users//PC//Desktop//Practica//fuente//Pixels.ttf", cons.TAMAÑO_FUENTE_CONTADOR)

    return aviso_go, boton_restart, nube, font

def mover_y_dibujar_nube( nubes, ventana, prox_spawn_x, distancia_min, distancia_max, nube_img, velocidad_juego):
    #recorro la lista de nubes
    for nube in nubes:
            nube.disminuir_x(velocidad_juego/10)
            nube.dibujar()
    #verico que haya pasado el margen de la pantalla final para eliminar el primero de la lista
    if nubes[0].get_x() < -100:
        nubes.pop(0)
    #verifico que el ultimo haya pasado una distancia alzar para agregar a la lista
    if nubes[-1].get_x() < prox_spawn_x:
            w_h_rand = random.randint(40,80)
            nubes.append(cls.Nube(ventana, cons.VENTANA_X, random.randint(50,200),w_h_rand,w_h_rand, nube_img))
            prox_spawn_x = random.randint(distancia_min, distancia_max) 

def mover_y_dibujar_obstaculos( obstaculos, dinosaurio, ventana, prox_spawn_x, distancia_min, distancia_max, animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble,velocidad_juego):
    
    colision = False     
    #recorro la lista de nubes
    for obstaculo in obstaculos:
            obstaculo.animacion()
            # Chequeo el tipo de clase del objeto
            # Aumento la velocidad en base al tipo de objeto
            if isinstance(obstaculo,cls.Cactus):
                obstaculo.disminuir_x(velocidad_juego)
            else:
                obstaculo.disminuir_x(velocidad_juego+1/2)
            obstaculo.dibujar()
            obstaculo.actualizar_hitbox()
            if dinosaurio.colision(obstaculo):
                print("\nSe detecto una colision con obstaculo!!\n")
                colision = True
    #verico que haya pasado el margen de la pantalla final para eliminar el primero de la lista
    if obstaculos[0].get_x() < -100:
        obstaculos.pop(0)
    #verifico que el ultimo haya pasado una distancia alzar para agregar a la lista
    if obstaculos[-1].get_x() < prox_spawn_x:
        agregar_obstaculos_a_lista(obstaculos, ventana, animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble)
        prox_spawn_x = random.randint(distancia_min, distancia_max) 
    return colision

def accion_de_saltar( dinosaurio, esta_saltando,velocidad_juego):
    # En base a la funcion de caida libre surge la siguiente funcion de salto:
    if esta_saltando :
        dinosaurio.disminuir_y_salto()
        dinosaurio.disminuir_velocidad_y()
        dinosaurio.dibujar_salto()
        if dinosaurio.get_velocidad_y() < -dinosaurio.get_altura_salto():
            esta_saltando = False
            dinosaurio.set_velocidad_y()
    else:
        dinosaurio.correr()
    return esta_saltando

def mostrar_hitbox( dinosaurio, obstaculos):
    dinosaurio.hitbox()
    for obstaculo in obstaculos:
        obstaculo.hitbox()


def juego():

    global dinosaurio
    ventana = pygame.display.set_mode((cons.VENTANA_X,cons.VENTANA_Y))
    pygame.display.set_caption("Sin Internet")
    puntaje = 0 

    run = True
    esta_saltando = False
    estado_hitbox = False
    hay_colision = False
    comienzo_juego = False
    
    #Carga de imagenes o sprites
    animaciones_pajaro = []
    tipos_cactus_chicos = []
    tipos_cactus_grandes = []
    tipos_cactus_grandes_doble = []
    nubes = []
    aviso_go, boton_restart,nube_img,font = cargar_pngs(animaciones_pajaro, tipos_cactus_chicos,
                                                        tipos_cactus_grandes, tipos_cactus_grandes_doble)
    
   
    
    # Inicializacion de listas que contienen objetos que se mostraran en pantalla
    obstaculos = []
    agregar_obstaculos_a_lista(obstaculos, ventana, animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble)
    w_h_rand = random.randint(40,80)
    nubes.append(cls.Nube(ventana, random.randint(50,cons.VENTANA_X), random.randint(50,200),w_h_rand,w_h_rand, nube_img))
    
    #Control del frame-rate
    relog = pygame.time.Clock()

    #Inicializacion de objetos
    dinosaurio = cls.Personaje(ventana,cons.COMIENZO_X,cons.COMIENZO_Y,
                               cons.VELOCIDAD_Y, cons.ALTURA_SALTO,
                               cons.ANCHO_DINOSAURIO_HITBOX_SUP,cons.ALTO_DINOSAURIO_HITBOX_SUP,
                               cons.ANCHO_DINOSAURIO_HITBOX_INF,cons.ALTO_DINOSAURIO_HITBOX_INF)
    superficie = cls.Superficie(ventana,cons.COMIENZO_SUPERFICE_X,cons.COMIENZO_SUPERFICE_Y)

    aviso_go = cls.Aviso(ventana, (cons.VENTANA_X/2)-25, 100, aviso_go)
    boton_restart = cls.Boton_Restart(ventana, (cons.VENTANA_X/2)-20, 200, boton_restart)
    distancia_min = cons.COMIENZO_OBSTACULO_X - 600
    distancia_max = cons.COMIENZO_OBSTACULO_X -300
    prox_spawn_x = random.randint(distancia_min, distancia_max)
    
    #inicalizacion de variables para el aumento de la velocidad del juego
    velocidad_juego = 3        
    tiempo_ultimo_incremento = pygame.time.get_ticks()
 

    while run:
        relog.tick(cons.FPS)

        #Aumento de la velocidad del juego cada cierto tiempo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_incremento > cons.INTERVALO_INCREMENTO and velocidad_juego < 15:
            velocidad_juego += cons.INCREMENTO_VELOCIDAD
            tiempo_ultimo_incremento = tiempo_actual

        #Verifica si hubo colision sigue el juego o no
        if hay_colision and not comienzo_juego:
            aviso_go.dibujar()
            dinosaurio.chocar()
            boton_restart.dibujar()
            pygame.display.update()
            texto_puntaje = font.render(f"{int(puntaje):08}", True, (50, 50, 50))
            ventana.blit(texto_puntaje, (cons.POSICION_CONTADOR_X, cons.POSICION_CONTADOR_Y))

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_restart.boton_rect.collidepoint(event.pos):
                        
                        # si se hace click en el boton restart

                        dinosaurio = cls.Personaje(ventana,cons.COMIENZO_X,cons.COMIENZO_Y,
                                                    cons.VELOCIDAD_Y, cons.ALTURA_SALTO,
                                                    cons.ANCHO_DINOSAURIO_HITBOX_SUP,cons.ALTO_DINOSAURIO_HITBOX_SUP,
                                                    cons.ANCHO_DINOSAURIO_HITBOX_INF,cons.ALTO_DINOSAURIO_HITBOX_INF)
                        obstaculos = []
                        agregar_obstaculos_a_lista(obstaculos, ventana, animaciones_pajaro, tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble)
                        nubes = []
                        w_h_rand = random.randint(40,80)
                        nubes.append(cls.Nube(ventana, cons.VENTANA_X, random.randint(50,200),w_h_rand,w_h_rand, nube_img))
                        esta_saltando = False
                        hay_colision = False
                        estado_hitbox = False
                        #inicalizacion de variables para el aumento de la velocidad del juego
                        velocidad_juego =3         
                        tiempo_ultimo_incremento = pygame.time.get_ticks()
                        puntaje = 0
            continue
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    estado_hitbox = not estado_hitbox

        ventana.fill((255,255,255))

        keys_pressed = pygame.key.get_pressed()

        #accion de saltar
        if keys_pressed[pygame.K_UP]:  
            esta_saltando = True
        
         #accion de agacharse
        if keys_pressed[pygame.K_DOWN]:  
            dinosaurio.agacharse()
        else:
            dinosaurio.modificar_agachado(False)            
        
        # Mover las nubes y dibujarlas
        mover_y_dibujar_nube(nubes, ventana, prox_spawn_x, distancia_min, distancia_max, nube_img,velocidad_juego)

        #accion de saltar
        esta_saltando=accion_de_saltar(dinosaurio, esta_saltando,velocidad_juego)

        # Mover los obstaculos y dibujarlos
        hay_colision = mover_y_dibujar_obstaculos(obstaculos, dinosaurio, ventana, prox_spawn_x,
                                          distancia_min, distancia_max, animaciones_pajaro, 
                                          tipos_cactus_chicos, tipos_cactus_grandes, tipos_cactus_grandes_doble,velocidad_juego) 
        if not hay_colision:
            #sumar puntaje y mostrar contador
            puntaje += 0.1 * (velocidad_juego / 10)
            texto_puntaje = font.render(f"{int(puntaje):08}", True, (50, 50, 50))
            ventana.blit(texto_puntaje, (cons.POSICION_CONTADOR_X, cons.POSICION_CONTADOR_Y))
        else:
            print(f"Veliciadad alcanzada: {velocidad_juego}\n Puntaje alcanzado:{int(puntaje)}")

        # Mostrar hitbox de los objetos y dibujarlo
        mostrar_hitbox(dinosaurio, obstaculos) if estado_hitbox else None
            
        # Mostrar superficie y moverla
        superficie_animacion(superficie,velocidad_juego)      
        
        pygame.display.update()


#MAIN
if __name__ == '__main__':
    pygame.init()
    juego()
    pygame.quit()
    exit()