import pygame
import pymunk
import random

#inicializamos o pygame
pygame.init()

#definimos o número de pixels que nosso "mapa" vai ter
mapa = pygame.display.set_mode((1000,600))

#definimos na objeto "tempo" que vai delimitar o tempo que as coisas acontecem
tempo = pygame.time.Clock()

#criamos um espaço de simulação da física usando o Pymunk
espaco = pymunk.Space()

#taxa de quadros atualizados por segundo
fps = 120

#definiremos os limites das paredes no espaço do pong
PEx = 50
PDx = 950
topo = 25
base = 575
Mx = 500
My = 300



#criaremos a bola do pong
class Bola():
    def __init__(self):
        #definimos que a bola será um corpo que o Pymunk vai interpetrar
        self.body = pymunk.Body()
        #definimos as posições iniciais da bola
        self.body.position = Mx, My
        #definimos a velocidade da bola
        self.body.velocity = 400, -300
        #definimos uma "forma" para o corpo, para que possa interagir com demais obj.
        self.shape = pymunk.Circle(self.body, 8)
        #definimos a densidade do corpo
        self.shape.density = 1
        #definimos a elasticidade do corpo (que será 1) para que as colisões sejam
        #perfeitamente elásticas
        self.shape.elasticity = 1
        #adicionamos a nossa bola no espaço
        espaco.add(self.body, self.shape)
        #determinamos um tipo de colisão para o formato da bola
        self.shape.collision_type = 1

    #definiremos o desenho do nosso objeto BOLA
    def desenho(self):
        x, y = self.body.position
        pygame.draw.circle(mapa, (255,255,255), (int(x), int(y)), 8)

    #definimos que quando o jogo for reiniciar, a bola volte a posição e velocidade inicias
    def reiniciar(self, X,Y,Z):
        self.body.position = Mx, My
        self.body.velocity = 400*random.choice([-1, 1]), -300*random.choice([-1, 1])
        return False

#definiremos o comportamento das paredes no jogo
class parede():
    #colocaremos dois pontos p1 e p2, pois temos 4 paredes e cada uma vai ter
    #um ponto 1 e ponto 2 diferentes.
    def __init__(self, p1, p2, collision_number = None):
        #definimos que as paredes serão corpos estáticos
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        #definimos a forma da parede
        self.shape = pymunk.Segment(self.body, p1, p2, 10)
        self.shape.elasticity = 1
        espaco.add(self.body, self.shape)
        if collision_number:
            self.shape.collision_type = collision_number
    def desenho(self):
        pygame.draw.line(mapa, (255,255,255), self.shape.a, self.shape.b,10)

#definiremos o comportamento dos jogadores
class jogador():
    #x é apenas a posição em x que o jogador vai ficar
    def __init__(self, x):
        #o corpo será "estático" em relação a não adiquir o momento linear da bola
        #mas queremos que se mova em y, então usamos o tipo de corpo "KINEMATIC"
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, My
        self.shape = pymunk.Segment(self.body, [0, -40], [0, 40], 10)
        self.shape.elasticity = 1
        espaco.add(self.body, self.shape)

    #Evitar que o corpo ultrapasse as paredes superiores e inferiores
    def sair(self):
        #A função local_to_world converte as coordenas para a biblioteca
        #A indexação [1] indica que o que queremos é apenas o eixo y
        p1_y = self.body.local_to_world(self.shape.a)[1]
        p2_y = self.body.local_to_world(self.shape.b)[1]

        if p1_y < topo:
            self.body.position = (self.body.position[0], topo + 40)
        if p2_y > base:
            self.body.position = (self.body.position[0], base - 40)

    def desenho(self):
        #p1 e p2 são os pontos a e b de coordenadas vistas acima, que definem a altura
        #do desenho do jogador. Queremos que essas posições sejam em relação ao "mundo"
        #que é o mapa, então precisamos definir de forma mais específica aqui
        p1 = self.body.local_to_world(self.shape.a) 
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(mapa, (255, 255, 255), p1, p2, 10)
    #Define as velocidades iniciais do jogador
    def movimento(self, para_cima = True):
        if para_cima:
            self.body.velocity = 0, -600
        else:
            self.body.velocity = 0, 600

    def parada(self):
        self.body.velocity = 0, 0
#criaremos uma função jogo, que é o nosso jogo :)
def jogo():
    #definimos nosso objeto Bola() no jogo
    bola = Bola()

    #definimos as quatro paredes
    parede_esquerda =  parede([PEx, topo], [PEx, base], 2)
    parede_direita = parede([PDx, topo], [PDx, base], 2)
    parede_topo = parede([PEx, topo], [PDx, topo], 3)
    parede_base = parede([PEx, base], [PDx, base], 3)

    #definiremos jogador 1 e 2
    jogador1 = jogador(PEx + 50)
    jogador2 = jogador(PDx - 50)

    #collision handler basicamente diz pra simulação o que fazer quando dois objetos
    #colidem
    ponto = espaco.add_collision_handler(1,2)
    ponto.begin = bola.reiniciar
    #se um evento do tipo "QUIT"(no nosso caso) fechar a janela do jogo), o jogo vai
    # fechar e a função vai retornar o loop.
    while True:
        for click in pygame.event.get():
            if click.type == pygame.QUIT:
                return

            #define uma ação para caso uma tecla for pressionada
        teclas = pygame.key.get_pressed()
        if not  jogador2.sair():
            #tecla SETINHA PRA CIMA faz mover para cima
            if teclas[pygame.K_UP]:
                jogador2.movimento()
            #tecla SETINHA PRA BAIXO faz mover para baixo
            elif teclas [pygame.K_DOWN]:
                jogador2.movimento(False)
            else:
                jogador2.parada()

        if not jogador1.sair():
            if teclas[pygame.K_w]:
            #tecla W faz mover para cima
                jogador1.movimento()
            #tecla S faz mover para baixo
            elif teclas [pygame.K_s]:
                jogador1.movimento(False)
            else:
                jogador1.parada()

        #define cor do mapa
        mapa.fill((0,0,0))
        #definimos o objeto bola agora com seu desenho circular
        bola.desenho()

        #definiremos as paredes agora com seu desenho
        parede_esquerda.desenho()
        parede_direita.desenho()
        parede_topo.desenho()
        parede_base.desenho()

        #definiremos os jogadores com seus devidos desenhos
        jogador1.desenho()
        jogador2.desenho()

        pygame.draw.line(mapa,(255,255,255), [Mx, topo], [Mx, base], 5)
        pygame.draw.circle(mapa, (255,255,255), [Mx, My],10)

        # atualiza a tela durante esse loop para cada frame atualizado
        pygame.display.update()

        # define o fps máximo do jogo
        tempo.tick(fps)

        #definimos que o espaço de simulação do Pymunk será atualizado em 40 fps
        espaco.step(1/fps)

jogo()
pygame.quit()