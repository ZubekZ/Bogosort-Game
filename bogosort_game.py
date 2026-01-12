import pygame, sys, random
import os 

# Inicializa o pygame
pygame.init()

# Inicializa o mixer para sons
pygame.mixer.init() 

# Tela aumentada
LARGURA, ALTURA = 900, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("BogoSort Game")

# Paleta de Cores 8-Bit
PIXEL_FUNDO_ESCURO = (20, 0, 40)       
PIXEL_FUNDO_PRETO = (0, 0, 0)         
PIXEL_DESTAQUE = (255, 190, 0)      
PIXEL_TEXTO = (255, 245, 200)       
PIXEL_DESTAQUE_HOVER = (255, 230, 150) 
PIXEL_BOTAO = (50, 200, 120)        
PIXEL_BOTAO_HOVER = (120, 230, 150)  
PIXEL_BOTAO_SAIR = (255, 60, 60)       
PIXEL_BOTAO_SAIR_HOVER = (255, 120, 120) 
PIXEL_BOTAO_SOMBRA = (30, 120, 80)   
PIXEL_BOTAO_SAIR_SOMBRA = (180, 40, 40) 
PIXEL_DESTAQUE_SOMBRA = (180, 120, 0) 
PIXEL_NUMERO = (220, 0, 0)          
BRANCO = (255, 255, 255)
CINZA = (120, 120, 120) 

PIXEL_SLOT_BORDA = (200, 0, 0)      
PIXEL_SLOT_LUZ = (255, 50, 50)      
PIXEL_SLOT_FUNDO = (30, 30, 30)     

PIXEL_MOEDA_OURO = (255, 215, 0)
PIXEL_MOEDA_BORDA = (180, 150, 0)
PIXEL_MOEDA_DETALHE = (255, 230, 100)

PIXEL_CAIXA_FUNDO = (200, 0, 0)      
PIXEL_CAIXA_BORDA = (255, 190, 0)      
PIXEL_CAIXA_BORDA_HOVER = (255, 230, 150)
PIXEL_LETRA_FUNDO = (255, 255, 255)      
PIXEL_LETRA_COR = (0, 0, 0)          

# Carregando a fonte da pasta 'assets'
CAMINHO_FONTE = os.path.join("assets", "PressStart2P-Regular.ttf")
try:
    fonte_titulo_grande = pygame.font.Font(CAMINHO_FONTE, 60)
    fonte_titulo_pequeno = pygame.font.Font(CAMINHO_FONTE, 30)
    fonte_padrao = pygame.font.Font(CAMINHO_FONTE, 20)
    fonte_numeros = pygame.font.Font(CAMINHO_FONTE, 36) 
    fonte_interrogacao = pygame.font.Font(CAMINHO_FONTE, 50) 
    fonte_moeda_letra = pygame.font.Font(CAMINHO_FONTE, 16)
except FileNotFoundError:
    print(f"ERRO: Fonte '{CAMINHO_FONTE}' nao encontrada.")
    print("Usando fonte padrao.")
    # Fallback fonts
    fonte_titulo_grande = pygame.font.Font(None, 100)
    fonte_titulo_pequeno = pygame.font.Font(None, 50)
    fonte_padrao = pygame.font.Font(None, 36)
    fonte_numeros = pygame.font.Font(None, 60)
    fonte_interrogacao = pygame.font.Font(None, 70)
    fonte_moeda_letra = pygame.font.Font(None, 24)

# Carregando todos os efeitos sonoros
try:
    som_click = pygame.mixer.Sound(os.path.join("assets", "click.mp3"))
    som_start = pygame.mixer.Sound(os.path.join("assets", "Start.MP3"))
    som_vitoria = pygame.mixer.Sound(os.path.join("assets", "win.mp3"))
    som_derrota = pygame.mixer.Sound(os.path.join("assets", "Lost.MP3")) 
    som_shuffle_loop = pygame.mixer.Sound(os.path.join("assets", "shuffle.mp3")) 
except pygame.error as e:
    print(f"Erro ao carregar um ou mais efeitos sonoros da pasta 'assets': {e}")
    som_click, som_start, som_vitoria, som_derrota, som_shuffle_loop = None, None, None, None, None

# Carregando e tocando a MÚSICA DE FUNDO
try:
    musica_fundo = os.path.join("assets", "Money - 8 Bit Universe.mp3")
    pygame.mixer.music.load(musica_fundo)
    pygame.mixer.music.set_volume(0.4) 
    pygame.mixer.music.play(-1) 
except pygame.error as e:
    print(f"Erro ao carregar musica de fundo: {e}")

# Carregando imagem de fundo INTERNA
fundo_cassino_interno = None
try:
    fundo_img_original = pygame.image.load(os.path.join("assets", "fundo.png")).convert()
    fundo_cassino_interno = pygame.transform.scale(fundo_img_original, (LARGURA - 90, ALTURA - 90)) 
except pygame.error as e:
    print(f"Erro ao carregar imagem de fundo 'fundo.png': {e}")
    print("O fundo interno será uma cor sólida.")

# Gerenciador de canais para sons
canal_efeito_giro = pygame.mixer.Channel(0)

def tocar_som(som, loop=0, channel=None):
    if som:
        if channel:
            channel.play(som, loop)
        else:
            som.play(loop)

# Estados do jogo e variáveis de animação
estado = "menu"
dificuldade = 5
vetor = []
tentativas = 0
rects = {} 
animando = False
novo_vetor = []
tempo_inicio_animacao = 0
duracao_base_giro = 1500 
tempo_paragem_rolo = 300 
tempos_paragem_rolos = [] 

# Fundo com moedas "pixel"
moedas = []
for _ in range(100):
    x = random.randint(0, LARGURA)
    y = random.randint(0, ALTURA)
    tamanho = random.choice([8, 12, 16])
    velocidade = random.uniform(0.5, 1.5)
    moedas.append([x, y, tamanho, velocidade])

def desenhar_fundo_moedas(cor_fundo):
    tela.fill(cor_fundo)
    for moeda in moedas:
        moeda[1] += moeda[3] 
        if moeda[1] > ALTURA:
            moeda[1] = -moeda[2] 
            moeda[0] = random.randint(0, LARGURA) 
        
        x, y, tamanho, _ = moeda
        pygame.draw.circle(tela, PIXEL_MOEDA_BORDA, (int(x), int(y)), tamanho // 2, 1)
        pygame.draw.circle(tela, PIXEL_MOEDA_OURO, (int(x), int(y)), tamanho // 2 - 1)
        brilho_size = max(1, tamanho // 4)
        pygame.draw.rect(tela, PIXEL_MOEDA_DETALHE, (int(x) - tamanho // 4, int(y) - tamanho // 4, brilho_size, brilho_size))

# Função para botões 8-bit SIMPLES (3D shadow)
def desenhar_botao_pixel_simples(texto, rect, cor_principal, cor_sombra, fonte, cor_texto=PIXEL_FUNDO_PRETO):
    pygame.draw.rect(tela, cor_sombra, (rect.x + 4, rect.y + 4, rect.width, rect.height))
    pygame.draw.rect(tela, cor_principal, rect)
    label = fonte.render(texto, True, cor_texto)
    tela.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

# Função para SUBTÍTULOS ESTÁTICOS "Encaixotados"
def desenhar_elemento_encaixotado(texto, rect, fonte, cor_borda, cor_fundo, cor_caixa, cor_letra):
    pygame.draw.rect(tela, cor_borda, rect, 3)
    pygame.draw.rect(tela, cor_fundo, (rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6))
    texto = texto.upper()
    num_letras = len(texto)
    if num_letras == 0: return
    espacamento_letra = 2
    padding_interno = 10
    largura_disponivel = rect.width - (padding_interno * 2)
    largura_caixa_letra = (largura_disponivel - (espacamento_letra * (num_letras - 1))) // num_letras
    altura_caixa_letra = rect.height - (padding_interno * 2)
    largura_total_letras = (largura_caixa_letra * num_letras) + (espacamento_letra * (num_letras - 1))
    x_inicial = rect.x + (rect.width - largura_total_letras) // 2
    y_inicial = rect.y + padding_interno

    for i, char in enumerate(texto):
        if char == ' ': continue
        caixa_letra_x = x_inicial + i * (largura_caixa_letra + espacamento_letra)
        pygame.draw.rect(tela, cor_caixa, (caixa_letra_x, y_inicial, largura_caixa_letra, altura_caixa_letra))
        label = fonte.render(char, True, cor_letra)
        label_x = caixa_letra_x + (largura_caixa_letra - label.get_width()) // 2
        label_y = y_inicial + (altura_caixa_letra - label.get_height()) // 2
        tela.blit(label, (label_x, label_y))

# Moldura 8-bit com detalhes de moedas
def desenhar_moeda_simples(surface, x, y, tamanho, cor_principal, cor_borda, cor_detalhe, simbolo="$"):
    pygame.draw.circle(surface, cor_borda, (x, y), tamanho // 2, 1)
    pygame.draw.circle(surface, cor_principal, (x, y), tamanho // 2 - 1)
    label_simbolo = fonte_moeda_letra.render(simbolo, True, cor_detalhe)
    surface.blit(label_simbolo, (x - label_simbolo.get_width()//2, y - label_simbolo.get_height()//2))

def desenhar_moldura():
    pygame.draw.rect(tela, PIXEL_DESTAQUE, (40, 40, LARGURA-80, ALTURA-80), 5)
    
    if fundo_cassino_interno:
        tela.blit(fundo_cassino_interno, (45, 45))
    else:
        pygame.draw.rect(tela, PIXEL_FUNDO_PRETO, (45, 45, LARGURA-90, ALTURA-90))
    
    pygame.draw.rect(tela, PIXEL_DESTAQUE_SOMBRA, (45, ALTURA-45, LARGURA-90, 5))
    pygame.draw.rect(tela, PIXEL_DESTAQUE_SOMBRA, (LARGURA-45, 45, 5, ALTURA-90))

    tamanho_moeda_moldura = 18
    offset_moeda = 20
    desenhar_moeda_simples(tela, 40 + offset_moeda, 40 + offset_moeda, tamanho_moeda_moldura, PIXEL_DESTAQUE, PIXEL_DESTAQUE_SOMBRA, PIXEL_MOEDA_DETALHE, "$")
    desenhar_moeda_simples(tela, LARGURA - 40 - offset_moeda, 40 + offset_moeda, tamanho_moeda_moldura, PIXEL_DESTAQUE, PIXEL_DESTAQUE_SOMBRA, PIXEL_MOEDA_DETALHE, "$")
    desenhar_moeda_simples(tela, 40 + offset_moeda, ALTURA - 40 - offset_moeda, tamanho_moeda_moldura, PIXEL_DESTAQUE, PIXEL_DESTAQUE_SOMBRA, PIXEL_MOEDA_DETALHE, "$")
    desenhar_moeda_simples(tela, LARGURA - 40 - offset_moeda, ALTURA - 40 - offset_moeda, tamanho_moeda_moldura, PIXEL_DESTAQUE, PIXEL_DESTAQUE_SOMBRA, PIXEL_MOEDA_DETALHE, "$")

    coroa_x = LARGURA // 2
    coroa_y = 40 + 5 
    pygame.draw.rect(tela, PIXEL_DESTAQUE, (coroa_x - 10, coroa_y, 20, 10))
    pygame.draw.polygon(tela, PIXEL_DESTAQUE, [(coroa_x - 15, coroa_y + 10), (coroa_x - 5, coroa_y), (coroa_x, coroa_y + 10), (coroa_x + 5, coroa_y), (coroa_x + 15, coroa_y + 10)])
    pygame.draw.rect(tela, PIXEL_DESTAQUE_SOMBRA, (coroa_x - 10, coroa_y + 4, 20, 6))

# Função para desenhar o título principal
def desenhar_titulo_pixel(texto_principal, texto_secundario, y_pos, hover_effect=False):
    largura_texto_principal = fonte_titulo_grande.render(texto_principal, True, PIXEL_DESTAQUE).get_width()
    min_width, max_width = 300, LARGURA - 160
    
    letreiro_width = max(min_width, largura_texto_principal + 80)
    letreiro_width = min(letreiro_width, max_width)
    
    letreiro_height = 110 
    letreiro_rect = pygame.Rect(LARGURA//2 - letreiro_width//2, y_pos - 10, letreiro_width, letreiro_height)
    
    pygame.draw.rect(tela, PIXEL_DESTAQUE_SOMBRA, (letreiro_rect.x+6, letreiro_rect.y+6, letreiro_rect.width, letreiro_rect.height))
    pygame.draw.rect(tela, PIXEL_DESTAQUE, letreiro_rect)
    pygame.draw.rect(tela, PIXEL_FUNDO_PRETO, (letreiro_rect.x+5, letreiro_rect.y+5, letreiro_rect.width-10, letreiro_rect.height-10))

    label_principal = fonte_titulo_grande.render(texto_principal, True, PIXEL_DESTAQUE)
    
    if texto_secundario:
        tela.blit(label_principal, (letreiro_rect.centerx - label_principal.get_width()//2, letreiro_rect.y + 10))
        label_secundario = fonte_titulo_pequeno.render(texto_secundario, True, PIXEL_TEXTO)
        tela.blit(label_secundario, (letreiro_rect.centerx - label_secundario.get_width()//2, letreiro_rect.y + 75)) 
    else:
        tela.blit(label_principal, (letreiro_rect.centerx - label_principal.get_width()//2, letreiro_rect.centery - label_principal.get_height()//2))

    if hover_effect: luz_cor = PIXEL_DESTAQUE_HOVER 
    else: luz_cor = PIXEL_DESTAQUE
    agora = pygame.time.get_ticks()
    if (agora // 200) % 2 == 0: cor_luz = PIXEL_DESTAQUE_HOVER 
    else: cor_luz = PIXEL_DESTAQUE
    passo_luz = 10
    for x in range(letreiro_rect.left, letreiro_rect.right, passo_luz):
        if (x // passo_luz) % 2 == 0:
            pygame.draw.rect(tela, cor_luz, (x, letreiro_rect.top, 5, 5))
            pygame.draw.rect(tela, cor_luz, (x, letreiro_rect.bottom - 5, 5, 5))
    for y in range(letreiro_rect.top, letreiro_rect.bottom, passo_luz):
        if (y // passo_luz) % 2 == 0:
            pygame.draw.rect(tela, cor_luz, (letreiro_rect.left, y, 5, 5))
            pygame.draw.rect(tela, cor_luz, (letreiro_rect.right - 5, y, 5, 5))

# Telas de menu
def desenhar_menu(mouse_pos):
    desenhar_fundo_moedas(PIXEL_FUNDO_ESCURO)
    desenhar_moldura()
    
    desenhar_titulo_pixel("BOGOSORT", "GAME", 120, True) 

    rect_jogar = pygame.Rect(LARGURA//2 - 150, 290, 300, 60)
    rect_tutorial = pygame.Rect(LARGURA//2 - 150, 380, 300, 60)
    rect_sair = pygame.Rect(LARGURA//2 - 150, 470, 300, 60)

    cor_jogar = PIXEL_BOTAO_HOVER if rect_jogar.collidepoint(mouse_pos) else PIXEL_BOTAO
    desenhar_botao_pixel_simples("Jogar", rect_jogar, cor_jogar, PIXEL_BOTAO_SOMBRA, fonte_padrao)

    cor_tut = PIXEL_BOTAO_HOVER if rect_tutorial.collidepoint(mouse_pos) else PIXEL_BOTAO
    desenhar_botao_pixel_simples("Tutorial", rect_tutorial, cor_tut, PIXEL_BOTAO_SOMBRA, fonte_padrao)
    
    cor_sair = PIXEL_BOTAO_SAIR_HOVER if rect_sair.collidepoint(mouse_pos) else PIXEL_BOTAO_SAIR
    desenhar_botao_pixel_simples("Sair", rect_sair, cor_sair, PIXEL_BOTAO_SAIR_SOMBRA, fonte_padrao, PIXEL_TEXTO)
    
    return {"jogar": rect_jogar, "tutorial": rect_tutorial, "sair": rect_sair}

def desenhar_tutorial(mouse_pos):
    desenhar_fundo_moedas(PIXEL_FUNDO_ESCURO)
    desenhar_moldura()
    
    desenhar_titulo_pixel("COMO JOGAR", "", 120) 

    # ### NOVO: Painel semitransparente para o texto ###
    painel_largura = 700
    painel_altura = 300 # Altura ajustada para o texto
    painel_x = (LARGURA - painel_largura) // 2
    painel_y = 260 # Posição Y ajustada
    
    # Cria uma superfície com suporte a transparência (SRCALPHA)
    painel_fundo = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)
    
    # Preenche a superfície com cinza semitransparente (Alpha 150)
    painel_fundo.fill((50, 50, 50, 150)) 
    
    # Desenha o painel na tela principal
    tela.blit(painel_fundo, (painel_x, painel_y))
    # #######################################################

    explicacao = [
        "O BogoSort e um algoritmo",
        "100% aleatorio!",
        "",
        "O jogo simula um caca-niquel:",
        "os numeros sao embaralhados",
        "ate ficarem em ordem.",
        "",
        "- Clique em 'Embaralhar'.",
        "- Quanto menos tentativas, melhor!",
        "",
    ]
    y_inicio_texto = 280 
    for i, linha in enumerate(explicacao):
        texto = fonte_padrao.render(linha, True, PIXEL_TEXTO) 
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y_inicio_texto + i * 30)) 
        
    rect_voltar = pygame.Rect(LARGURA//2 - 100, 580, 200, 60) 
    
    cor_voltar = PIXEL_BOTAO_HOVER if rect_voltar.collidepoint(mouse_pos) else PIXEL_BOTAO
    desenhar_botao_pixel_simples("Voltar", rect_voltar, cor_voltar, PIXEL_BOTAO_SOMBRA, fonte_padrao)
    
    return {"voltar": rect_voltar}

def desenhar_dificuldade(mouse_pos):
    desenhar_fundo_moedas(PIXEL_FUNDO_ESCURO)
    desenhar_moldura()
    
    desenhar_titulo_pixel("DIFICULDADE", "", 120) 

    rect_facil = pygame.Rect(LARGURA//2 - 200, 270, 400, 60)
    rect_medio = pygame.Rect(LARGURA//2 - 200, 360, 400, 60)
    rect_dificil = pygame.Rect(LARGURA//2 - 200, 450, 400, 60)
    rect_voltar = pygame.Rect(LARGURA//2 - 100, 540, 200, 50)

    cor_facil = PIXEL_DESTAQUE_HOVER if rect_facil.collidepoint(mouse_pos) else PIXEL_DESTAQUE
    desenhar_botao_pixel_simples("Facil (3 numeros)", rect_facil, cor_facil, PIXEL_DESTAQUE_SOMBRA, fonte_padrao)
    
    cor_medio = PIXEL_DESTAQUE_HOVER if rect_medio.collidepoint(mouse_pos) else PIXEL_DESTAQUE
    desenhar_botao_pixel_simples("Medio (5 numeros)", rect_medio, cor_medio, PIXEL_DESTAQUE_SOMBRA, fonte_padrao)
    
    cor_dificil = PIXEL_DESTAQUE_HOVER if rect_dificil.collidepoint(mouse_pos) else PIXEL_DESTAQUE
    desenhar_botao_pixel_simples("Dificil (7 numeros)", rect_dificil, cor_dificil, PIXEL_DESTAQUE_SOMBRA, fonte_padrao)

    cor_voltar = PIXEL_BOTAO_SAIR_HOVER if rect_voltar.collidepoint(mouse_pos) else PIXEL_BOTAO_SAIR
    desenhar_botao_pixel_simples("Voltar", rect_voltar, cor_voltar, PIXEL_BOTAO_SAIR_SOMBRA, fonte_padrao, PIXEL_TEXTO)

    return {"facil": rect_facil, "medio": rect_medio, "dificil": rect_dificil, "voltar": rect_voltar}

def desenhar_texto_contornado_pixel(surface, texto, fonte, cor_texto, cor_contorno, x, y):
    texto_sombra = fonte.render(texto, True, cor_contorno)
    surface.blit(texto_sombra, (x + 2, y + 2)) 
    texto_principal = fonte.render(texto, True, cor_texto)
    surface.blit(texto_principal, (x, y))

def desenhar_jogo(vetor_atual, tentativas_count, esta_animando, dificuldade, mouse_pos):
    global animando, vetor, estado
    
    desenhar_fundo_moedas(PIXEL_FUNDO_PRETO)
    desenhar_moldura()

    # Subtítulos Estáticos
    rect_titulo_jogo = pygame.Rect(LARGURA//2 - 100, 80, 200, 40)
    desenhar_elemento_encaixotado("JOGO", rect_titulo_jogo, fonte_padrao, PIXEL_CAIXA_BORDA, PIXEL_CAIXA_FUNDO, PIXEL_LETRA_FUNDO, PIXEL_LETRA_COR)
    
    rect_titulo_tentativas = pygame.Rect(LARGURA//2 - 200, 130, 400, 40)
    desenhar_elemento_encaixotado(f"Tentativas: {tentativas_count}", rect_titulo_tentativas, fonte_padrao, PIXEL_CAIXA_BORDA, PIXEL_CAIXA_FUNDO, PIXEL_LETRA_FUNDO, PIXEL_LETRA_COR)

    # --- Desenho da Máquina de Slot ---
    slot_width, slot_height, slot_spacing = 90, 90, 15
    if dificuldade == 7:
        slot_width, slot_spacing = 80, 10
    
    total_slots_width = dificuldade * slot_width + (dificuldade - 1) * slot_spacing
    maquina_width = total_slots_width + 60
    max_maquina_width = LARGURA - 100
    maquina_width = min(maquina_width, max_maquina_width)
    
    maquina_x = (LARGURA - maquina_width) // 2 
    maquina_y = 220
    maquina_height = slot_height + 60
    rect_maquina = pygame.Rect(maquina_x, maquina_y, maquina_width, maquina_height)

    # Borda da máquina
    pygame.draw.rect(tela, PIXEL_SLOT_BORDA, rect_maquina, 8) 
    pygame.draw.rect(tela, PIXEL_SLOT_FUNDO, (rect_maquina.x + 8, rect_maquina.y + 8, rect_maquina.width - 16, rect_maquina.height - 16))

    # Luzes piscando
    agora_ms = pygame.time.get_ticks()
    if (agora_ms // 150) % 2 == 0: luz_cor = PIXEL_SLOT_LUZ
    else: luz_cor = PIXEL_SLOT_BORDA 
    luz_passo = 15
    for x in range(rect_maquina.left, rect_maquina.right, luz_passo):
        pygame.draw.rect(tela, luz_cor, (x, rect_maquina.top, 5, 5))
        pygame.draw.rect(tela, luz_cor, (x, rect_maquina.bottom - 5, 5, 5))
    for y in range(rect_maquina.top, rect_maquina.bottom, luz_passo):
        if (y // luz_passo) % 2 == 0:
            pygame.draw.rect(tela, luz_cor, (rect_maquina.left, y, 5, 5))
            pygame.draw.rect(tela, luz_cor, (rect_maquina.right - 5, y, 5, 5))
    
    # --- Desenho dos Slots e Números ---
    slot_inicial_x = rect_maquina.x + (rect_maquina.width - total_slots_width) // 2
    slot_y = rect_maquina.y + (rect_maquina.height - slot_height) // 2
    agora = pygame.time.get_ticks()
    
    if esta_animando and tempos_paragem_rolos and agora >= tempos_paragem_rolos[-1]:
        animando = False
        vetor[:] = novo_vetor 
        if vetor == sorted(vetor):
            estado = "vitoria" 
            tocar_som(som_vitoria)
            if canal_efeito_giro.get_busy(): canal_efeito_giro.stop() 
            return {"embaralhar": pygame.Rect(0,0,0,0), "voltar": pygame.Rect(0,0,0,0)} 
        else:
            if canal_efeito_giro.get_busy(): canal_efeito_giro.stop()

    for i in range(dificuldade):
        rect_slot_interior = pygame.Rect(slot_inicial_x + i * (slot_width + slot_spacing), slot_y, slot_width, slot_height)
        pygame.draw.rect(tela, PIXEL_DESTAQUE, rect_slot_interior, 3) 
        pygame.draw.rect(tela, BRANCO, (rect_slot_interior.x + 3, rect_slot_interior.y + 3, rect_slot_interior.width - 6, rect_slot_interior.height - 6))
        try:
            rolo_surf = tela.subsurface(rect_slot_interior.x + 3, rect_slot_interior.y + 3, rect_slot_interior.width - 6, rect_slot_interior.height - 6)
            rolo_surf.fill(BRANCO) 
        except ValueError:
            continue 
        
        numero_final = vetor_atual[i]
        
        if esta_animando and tempos_paragem_rolos and agora < tempos_paragem_rolos[i]:
            text_to_display = "?"
            current_font = fonte_interrogacao
            text_color = PIXEL_NUMERO
            y_offset_animation = (agora * 3) % (rolo_surf.get_height() * 2) - rolo_surf.get_height()
            
            for j in range(-1, 2): 
                y_pos_text = (rolo_surf.get_height() // 2 - current_font.size(text_to_display)[1] // 2) + y_offset_animation + j * rolo_surf.get_height()
                desenhar_texto_contornado_pixel(
                    rolo_surf, text_to_display, current_font, text_color, PIXEL_FUNDO_PRETO,
                    rolo_surf.get_width() // 2 - current_font.size(text_to_display)[0] // 2, 
                    y_pos_text
                )
        else: 
            if esta_animando: 
                if novo_vetor and i < len(novo_vetor):
                    numero_final = novo_vetor[i]
                else:
                    numero_final = vetor_atual[i] 
            else:
                 numero_final = vetor_atual[i]
            desenhar_texto_contornado_pixel(
                rolo_surf, str(numero_final), fonte_numeros, PIXEL_NUMERO, PIXEL_FUNDO_PRETO,
                rolo_surf.get_width() // 2 - fonte_numeros.size(str(numero_final))[0] // 2,
                rolo_surf.get_height() // 2 - fonte_numeros.size(str(numero_final))[1] // 2
            )

    # --- Desenho dos Botões ---
    if esta_animando:
        label_botao = "Rodando..."
        cor_botao_embaralhar = CINZA
    else:
        label_botao = "Embaralhar"
        cor_botao_embaralhar = PIXEL_BOTAO

    rect_embaralhar = pygame.Rect(LARGURA//2 - 130, 520, 260, 60) 
    rect_voltar = pygame.Rect(LARGURA//2 - 130, 595, 260, 50) 
    
    if not esta_animando:
        cor_emb = PIXEL_BOTAO_HOVER if rect_embaralhar.collidepoint(mouse_pos) else PIXEL_BOTAO
        desenhar_botao_pixel_simples(label_botao, rect_embaralhar, cor_emb, PIXEL_BOTAO_SOMBRA, fonte_padrao)
    else:
        pygame.draw.rect(tela, CINZA, rect_embaralhar)
        label = fonte_padrao.render(label_botao, True, PIXEL_FUNDO_PRETO)
        tela.blit(label, (rect_embaralhar.centerx - label.get_width()//2, rect_embaralhar.centery - label.get_height()//2))

    cor_volt = PIXEL_BOTAO_SAIR_HOVER if rect_voltar.collidepoint(mouse_pos) else PIXEL_BOTAO_SAIR
    desenhar_botao_pixel_simples("Desistir", rect_voltar, cor_volt, PIXEL_BOTAO_SAIR_SOMBRA, fonte_padrao, PIXEL_TEXTO)

    return {"embaralhar": rect_embaralhar, "voltar": rect_voltar}


def desenhar_vitoria(tentativas_count, mouse_pos):
    desenhar_fundo_moedas(PIXEL_FUNDO_ESCURO)
    desenhar_moldura()
    
    desenhar_titulo_pixel("VOCE VENCEU", "PARABENS", 250) 

    rect_titulo_tentativas = pygame.Rect(LARGURA//2 - 200, 380, 400, 40)
    desenhar_elemento_encaixotado(f"Tentativas: {tentativas_count}", rect_titulo_tentativas, fonte_padrao, PIXEL_CAIXA_BORDA, PIXEL_CAIXA_FUNDO, PIXEL_LETRA_FUNDO, PIXEL_LETRA_COR)

    rect_reiniciar = pygame.Rect(LARGURA//2 - 150, 480, 300, 60)
    
    cor_reiniciar = PIXEL_DESTAQUE_HOVER if rect_reiniciar.collidepoint(mouse_pos) else PIXEL_DESTAQUE 
    desenhar_botao_pixel_simples("Voltar ao menu", rect_reiniciar, cor_reiniciar, PIXEL_DESTAQUE_SOMBRA, fonte_padrao)
    
    return {"voltar": rect_reiniciar}


# Loop principal
clock = pygame.time.Clock() 
while True:
    mouse_pos_frame = pygame.mouse.get_pos()
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos 
            
            if estado == "menu":
                if rects.get("jogar") and rects["jogar"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    estado = "dificuldade"
                elif rects.get("tutorial") and rects["tutorial"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    estado = "tutorial"
                elif rects.get("sair") and rects["sair"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    pygame.quit()
                    sys.exit()

            elif estado == "tutorial":
                if rects.get("voltar") and rects["voltar"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    pygame.mixer.music.unpause()
                    estado = "menu"

            elif estado == "dificuldade":
                nova_dificuldade = 0
                if rects.get("facil") and rects["facil"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    nova_dificuldade = 3
                elif rects.get("medio") and rects["medio"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    nova_dificuldade = 5
                elif rects.get("dificil") and rects["dificil"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    nova_dificuldade = 7
                elif rects.get("voltar") and rects["voltar"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    estado = "menu"

                if nova_dificuldade > 0:
                    dificuldade = nova_dificuldade
                    vetor = list(range(1, dificuldade + 1))
                    random.shuffle(vetor)
                    tentativas = 0
                    estado = "jogo"
                    tempos_paragem_rolos = [] 
                    if canal_efeito_giro.get_busy():
                        canal_efeito_giro.stop()
                    pygame.mixer.music.pause()

            elif estado == "jogo" and not animando: 
                if rects.get("embaralhar") and rects["embaralhar"].collidepoint(mouse_pos):
                    animando = True
                    tentativas += 1
                    novo_vetor = list(range(1, dificuldade + 1))
                    random.shuffle(novo_vetor)
                    
                    tempos_paragem_rolos = []
                    tempo_inicio_animacao = pygame.time.get_ticks()
                    for i in range(dificuldade):
                        paragem = tempo_inicio_animacao + duracao_base_giro + (i * tempo_paragem_rolo)
                        tempos_paragem_rolos.append(paragem)
                    
                    tocar_som(som_start) 
                    tocar_som(som_shuffle_loop, loop=-1, channel=canal_efeito_giro) 
                    
                elif rects.get("voltar") and rects["voltar"].collidepoint(mouse_pos):
                    tocar_som(som_derrota) 
                    estado = "menu" 
                    animando = False 
                    if canal_efeito_giro.get_busy():
                        canal_efeito_giro.stop()
                    pygame.mixer.music.unpause()

            elif estado == "vitoria":
                if rects.get("voltar") and rects["voltar"].collidepoint(mouse_pos):
                    tocar_som(som_click) 
                    pygame.mixer.music.unpause()
                    estado = "menu"

    # Renderização
    if estado == "menu":
        rects = desenhar_menu(mouse_pos_frame)
    elif estado == "tutorial":
        rects = desenhar_tutorial(mouse_pos_frame)
    elif estado == "dificuldade":
        rects = desenhar_dificuldade(mouse_pos_frame)
    elif estado == "jogo":
        rects = desenhar_jogo(vetor, tentativas, animando, dificuldade, mouse_pos_frame)
    elif estado == "vitoria":
        rects = desenhar_vitoria(tentativas, mouse_pos_frame)

    pygame.display.flip()
    clock.tick(60)