import constantes as cons
import pygame
import sys
import random

#Clase personaje
class Personaje:
    def __init__(self, ventana, comienzo_x, comienzo_y, velocidad_salto, altura_salto, hit_w_1,hit_h_1,hit_w_2,hit_h_2):
        self.x=comienzo_x
        self.y=comienzo_y
        self.ventana = ventana
        self.quieto_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (11).png"),(cons.ANCHO_DINOSAURIO,cons.ALTO_DINOSAURIO))
        self.colision_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (7).png"),(cons.ANCHO_DINOSAURIO,cons.ALTO_DINOSAURIO))
        self.salto_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (9).png"),(cons.ANCHO_DINOSAURIO,cons.ALTO_DINOSAURIO))
        self.der_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (9).png"),(cons.ANCHO_DINOSAURIO,cons.ALTO_DINOSAURIO))
        self.izq_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (8).png"),(cons.ANCHO_DINOSAURIO,cons.ALTO_DINOSAURIO))
        self.agachar_izq_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (6).png"),(cons.ANCHO_DINOSAURIO_AGACHADO,cons.ALTO_DINOSAURIO_AGACHADO))
        self.agachar_der_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//dinosaurio//Adobe Express - file (5).png"),(cons.ANCHO_DINOSAURIO_AGACHADO,cons.ALTO_DINOSAURIO_AGACHADO))
        self.dinosaurio_rect = self.quieto_surface.get_rect(center=(comienzo_x,comienzo_y))
        self.velocidad_y = velocidad_salto
        self.altura_salto= altura_salto
        self.tiempo_act = pygame.time.get_ticks()
        self.frame = 0
        self.agachado = False

        # (x, y, ancho, alto)
        self.hitbox1 = pygame.Rect(0,0, hit_w_1, hit_h_1)  
        self.hitbox1.center = (self.x+12,self.y-16)
        self.hitbox2 = pygame.Rect(0,0, hit_w_2, hit_h_2)  
        self.hitbox2.center = (self.x-1,self.y+14)
    
    def modificar_agachado(self,estado):
        self.agachado = estado
    
    def agacharse(self):
        self.hitbox1.center = (self.x+12,self.y+12)
        self.hitbox2.center = (self.x-1,self.y+12)
        self.agachado = True
    
    def chocar(self):
        self.dinosaurio_rect= self.colision_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.colision_surface,self.dinosaurio_rect)

    def dibujar_salto(self):
        self.hitbox1.center = (self.x+12,self.y-16)
        self.hitbox2.center = (self.x-1,self.y+14)
        self.dinosaurio_rect= self.salto_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.salto_surface,self.dinosaurio_rect)

    def dibujar_quieto(self):
        self.dinosaurio_rect= self.quieto_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.quieto_surface,self.dinosaurio_rect)
    
    def correr(self):
        cooldown_animacion = 100
        if self.frame == 0:
            if self.agachado:
                self.dinosaurio_rect= self.agachar_der_surface.get_rect(center=(self.x,self.y))
                self.ventana.blit(self.agachar_der_surface,self.dinosaurio_rect)
            else:
                self.dinosaurio_rect= self.der_surface.get_rect(center=(self.x,self.y))
                self.ventana.blit(self.der_surface,self.dinosaurio_rect)
                self.hitbox1.center = (self.x+12,self.y-16)
                self.hitbox2.center = (self.x-5,self.y+14)
        else:
            if self.agachado:
                self.dinosaurio_rect= self.agachar_izq_surface.get_rect(center=(self.x,self.y))
                self.ventana.blit(self.agachar_izq_surface,self.dinosaurio_rect)
            else:
                self.dinosaurio_rect= self.izq_surface.get_rect(center=(self.x,self.y))
                self.ventana.blit(self.izq_surface,self.dinosaurio_rect)
                self.hitbox1.center = (self.x+12,self.y-16)
                self.hitbox2.center = (self.x-5,self.y+14)
        
        if pygame.time.get_ticks() - self.tiempo_act >= cooldown_animacion:
            self.frame = self.frame + 1
            self.tiempo_act = pygame.time.get_ticks()
        if self.frame >= cons.CANT_FRAME_CORRER:
            self.frame = 0
    
    def hitbox(self):
        pygame.draw.rect(self.ventana, (255,0,0), self.hitbox1, width=3)
        pygame.draw.rect(self.ventana, (255,0,0), self.hitbox2, width=3)

    def cambiar_estado_salto(self,estado):
        self.estado=estado

    def disminuir_y(self, y):
        self.y -= y
    
    def disminuir_y_salto(self):
        self.y -= self.velocidad_y

    def disminuir_velocidad_y(self):
        self.velocidad_y-= cons.GRAVEDAD_Y

    def get_velocidad_y(self):
        return self.velocidad_y
    
    def set_velocidad_y(self):
     self.velocidad_y = cons.ALTURA_SALTO

    def get_altura_salto(self):
        return self.altura_salto
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def colision(self, obstaculo):
        return self.hitbox1.colliderect(obstaculo.hitbox1) or self.hitbox2.colliderect(obstaculo.hitbox1)



class Superficie:
    def __init__(self,ventana,x,y):
        self.x = x
        self.y = y
        self.x_aux = x+2*(cons.VENTANA_X/2)
        self.y_aux = y
        self.ventana = ventana

        self.vista_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//escenario//Chromium_T-Rex-horizon.png"),(cons.LARGO_SUPERFICIE,cons.ANCHO_SUPERFICIE))
        self.vista_aux_surface = pygame.transform.scale(pygame.image.load("C://Users//PC//Desktop//Practica//sprites//escenario//Chromium_T-Rex-horizon.png"),(cons.LARGO_SUPERFICIE,cons.ANCHO_SUPERFICIE))
        self.superficie_rect = self.vista_surface.get_rect(center=(self.x,self.y))
    
    def dibujar_superficie_mov(self):
        self.superficie_rect= self.vista_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.vista_surface,self.superficie_rect)

        self.superficie_rect= self.vista_aux_surface.get_rect(center=(self.x_aux,self.y_aux))
        self.ventana.blit(self.vista_aux_surface,self.superficie_rect)
        
    def set_x(self,x):
        self.x = cons.VENTANA_X + (cons.VENTANA_X/2)
        
    def set_x_aux(self,x):
        self.x_aux = cons.VENTANA_X + (cons.VENTANA_X/2)

    def restar_x(self, le):
        self.x -= le
        self.x_aux -=le

    def get_x(self):
        return self.x
    
    def get_x_aux(self):
        return self.x_aux
    

#Clases para los obstaculos
class Obstaculo:
    def __init__(self,ventana, x, y, animaciones):
        self.x = x
        self.y = y
        self.ventana = ventana
        self.animaciones = animaciones
        self.tiempo_act = pygame.time.get_ticks()
        self.frame = 0
        if isinstance(animaciones, list):
            self.animaciones = animaciones
            self.img = animaciones[self.frame]
        else:
            self.animaciones = [animaciones]
            self.img = animaciones
        
    def hitbox(self):
        pass

    def animacion(self):
        pass

    def dibujar(self):
        pass
    
    def actualizar_hitbox(self):
        pass

    def disminuir_x (self, x):
        self.x -= x
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y   
    
class Pajaro(Obstaculo):
    def __init__(self,ventana, x, y, animaciones):
        super().__init__(ventana,x, y, animaciones)
        self.pajaro_surface = pygame.transform.scale(self.animaciones[self.frame],(48,60))
        self.hitbox1 = pygame.Rect(0,0, 30, 35) 
        self.hitbox1.center = (self.x, self.y)
    
    def animacion(self):
        cooldown_animacion = 100
        self.img = self.animaciones[self.frame]
        if pygame.time.get_ticks() - self.tiempo_act >= cooldown_animacion:
            self.frame= self.frame +1 
            self.tiempo_act= pygame.time.get_ticks()
        if self.frame >= len(self.animaciones):
            self.frame = 0
    
    def dibujar(self):
        self.pajaro_surface = pygame.transform.scale(self.img,(48,60))
        self.vuelo_rect= self.pajaro_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.pajaro_surface,self.vuelo_rect)

    def hitbox(self):
       self.hitbox1.center = (self.x,self.y)
       pygame.draw.rect(self.ventana, (0,255,0), self.hitbox1, width=3)
    
    def actualizar_hitbox(self):
        self.hitbox1.center = (self.x, self.y)
        

class Cactus(Obstaculo):
    def __init__(self,ventana, x, y,c_w,c_hi,hi_w,hi_h, img):
        super().__init__(ventana,x, y, img)
        self.cactus_surface = pygame.transform.scale(img, (c_w, c_hi))
        self.hitbox1 = pygame.Rect(0,0, hi_w,hi_h) 
        self.hitbox1.center = (self.x, self.y)
        self.img = img
        self.c_w = c_w
        self.c_hi = c_hi
    
    def dibujar(self):
        self.cactus_surface = pygame.transform.scale(self.img,(self.c_w,self.c_hi))
        self.quieto_rect= self.cactus_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.cactus_surface,self.quieto_rect)
    
    def hitbox(self):
       self.hitbox1.center = (self.x,self.y)
       pygame.draw.rect(self.ventana, (0,0,255), self.hitbox1, width=3)
    
    def actualizar_hitbox(self):
        self.hitbox1.center = (self.x, self.y)
    

#clases para los elementos decorativos (nubes, aviso)
class Decorativo: 
    def __init__(self,ventana, x, y):
        self.x = x
        self.y = y
        self.ventana = ventana

    def dibujar(self):
        pass
    def disminuir_x (self, x):
        self.x -= x
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    
class Nube(Decorativo):
    def __init__(self,ventana, x, y,w,h, img):
        super().__init__(ventana,x, y)
        self.nube_surface = pygame.transform.scale(img,(w,h))
        self.nube_rect = self.nube_surface.get_rect(center=(x,y))
        self.img = img
        self.w = w
        self.h = h
    
    def dibujar(self):
        self.nube_surface = pygame.transform.scale(self.img,(self.w,self.h))
        self.nube_rect= self.nube_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.nube_surface,self.nube_rect)


class Aviso(Decorativo):
    def __init__(self,ventana, x, y, img):
        super().__init__(ventana,x, y)
        self.aviso_surface = pygame.transform.scale(img,(200,40))
        self.aviso_rect = self.aviso_surface.get_rect(center=(x,y))
        self.img = img
    
    def dibujar(self):
        self.aviso_surface = pygame.transform.scale(self.img,(200,40))
        self.aviso_rect= self.aviso_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.aviso_surface,self.aviso_rect)
    




# clases para los botones
class Boton:
    def __init__(self,ventana, x, y):
        self.x = x
        self.y = y
        self.ventana = ventana
    
    def dibujar(self):
        pass
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

class Boton_Restart(Boton):
    def __init__(self,ventana, x, y, img):
        super().__init__(ventana,x, y)
        self.boton_surface = pygame.transform.scale(img,(50,50))
        self.boton_rect = self.boton_surface.get_rect(center=(x,y))
        self.img = img
    def dibujar(self):
        self.boton_surface = pygame.transform.scale(self.img,(50,50))
        self.boton_rect= self.boton_surface.get_rect(center=(self.x,self.y))
        self.ventana.blit(self.boton_surface,self.boton_rect)