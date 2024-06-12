# Importações necessárias
import customtkinter as ctk
from tkinter import filedialog, ttk
import pandas as pd
from segundaTela import segundaTela
import funcoes
import re
from funcoes import Unidade
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from requests import get
import sys
from pathlib import Path
from os import path
# Verifica se estamos executando o código empacotado
if getattr(sys, 'frozen', False):
    # Se estivermos executando o código empacotado, os arquivos estão na mesma pasta que o executável
    base_path = sys._MEIPASS
else:
    # Se não estivermos executando o código empacotado, os arquivos estão na mesma pasta que o script Python
    base_path = Path(__file__).parent.absolute()

ctk.set_appearance_mode("dark")
icone = path.join(base_path,"Simula_Rapido_icon.ico")
# Configuração inicial da tela
TelaEscolher = ctk.CTk()
TelaEscolher.title("Simulador")
TelaEscolher.iconbitmap(icone)
TelaEscolher.geometry("600x480")
TelaEscolher.resizable(width=False, height=False)
dark = "#242424"

#criando um estilo para o app
style = ttk.Style()

style.theme_use("alt")

style.theme_create("new",parent="alt", settings={
    "Treeview": {
        "configure": {
            "background": "#2F2F2F",  # Cor de fundo do corpo
            "fieldbackground": "#2F2F2F",  # Cor de fundo para células
            "foreground": "white",  # Cor da fonte para o texto do corpo
            "font": ("Arial", 16),  # Fonte do corpo
            "rowheight": 23,
        
        
        },
        "map": {
            "background": [("selected", "darkblue")],  # Cor de fundo para itens selecionados
            "foreground": [("selected", "white")], # Cor da fonte para itens selecionados
        
        }
    },
    "Treeview.Heading": {
        "configure": {
            "background": "black",
            "foreground": "white",  # Cor da fonte do cabeçalho
            "font": ("Arial", 20, "bold"),  # Fonte do cabeçalho
            "padding": 10,
        }
    },
    #estilo da barra de rolagem
    "Vertical.TScrollbar":{
        "configure":{
            "background":"#2F2F2F", 
            "troughcolor":dark, 
            "arrowcolor":"#2F2F2F",
            "bordercolor": "#2F2F2F",
        }
    },
    "TNotebook": {
        "configure": {
            "tabmargins": [2, 5, 2, 0]
              } },
            
    "TNotebook.Tab": {
        "configure": {
            "padding": [5, 5],
            "font": ("Arial",12, "bold"), 
            },
    "map":{
         "background": [("selected", dark)],  # Cor de fundo para itens selecionados
         "foreground": [("selected", "white")], # Cor da fonte para itens selecionados
    }        
    }
})
style.theme_use("new")

#inicializando lista da planilha
planilha = []
dados = []
data_entrega = ""
data_lancamento = ""
valor_renda = 0

# frame no meu centro da tela
frameUnica = ctk.CTkFrame(TelaEscolher, width=500, height=400, fg_color="#2f2f2f", bg_color=dark)
frameUnica.pack(pady=40)

# Titulo no centro do frame
titulo_label_simulador = ctk.CTkLabel(frameUnica, text="Simulador", fg_color="#2f2f2f", bg_color=dark, text_color="#ffffff", font=("cabian", 30))
titulo_label_simulador.place(x=180, y=30)

# Campo inserir o arquivo
campoArquivo = ctk.CTkFrame(frameUnica, width=100, height=200, fg_color="#2f2f2f", bg_color=dark)
campoArquivo.place(x=50, y=140)

# Função para atualizar a lista de opções com base na entrada do usuário
def atualizar_lista(event):
    texto_digitado = pesquisaUnidade.get().lower()
    opcoes_filtradas = [opcao for opcao in unidades_filtradas if texto_digitado in opcao.lower()]
    unidades.configure(values=opcoes_filtradas)

# Definir o caminho desejado
    
diretorio = '//cyrela.com.int/SPO/REPASSE_SP/PPI/Teste_ProjetoSimulador'#Teste de Diretorio da rede TEMPORARIO   

# Função para abrir e ler o arquivo Excel
def abrir_arquivo():
    
    acesso = get("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Acesso/SimuladorParcelas_V0.json").json()
    if not acesso:
        msg = CTkMessagebox(title="Atualização!", message="O aplicativo foi atualizado! Favor remover esta versão e instalar a nova.",
                          icon="cancel",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
        if msg.get() == "OK" or not msg.get() == "OK":

            sys.exit(0)

    global escolherArquivo, opcoes_unidades, planilha,dados, data_entrega, data_lancamento, diretorio
    # Abre uma caixa de diálogo para selecionar um arquivo
    escolherArquivo = filedialog.askopenfilename(initialdir=diretorio)
    # Verificar se o arquivo selecionado está dentro do caminho desejado
    if escolherArquivo.startswith(diretorio):
        #pega o ultimo sufixo do caminho do documento substitui o "_" e coloca os caracteres em maiusculo
        nome_arquivo = funcoes.caminho_em_string_maiuscula(escolherArquivo)

        #chama a função para configurar a entry e inputar o valor
        funcoes.configurar_entry(entry_nome_arquivo,nome_arquivo)

        # Leitura do arquivo Excel
        pd.set_option('display.max_rows', None)
        planilha = pd.read_excel(escolherArquivo, sheet_name="Planilha1")

        dados = pd.read_excel(escolherArquivo, sheet_name="Planilha2")
        data_entrega = dados.iloc[0,0]
        data_lancamento = dados.iloc[0,1]

        #definido as unidades do empreendimento
        opcoes_unidades = planilha["Torre e Unidade"]

        #colocando as opções da unidade com base no empreendimento escolhido
        unidades.configure(values=opcoes_unidades)

        #habilitando proximas informações a serem colocadas e desabilitando a ja preenchida
        entry_renda.configure(state=ctk.NORMAL, placeholder_text="Renda familiar", text_color="black")
        entry_renda.focus()
        button_continuar.configure(state=ctk.NORMAL)
        ButtonArquivo.configure(state=ctk.DISABLED)
        # Aqui você pode fazer o que precisa com o arquivo selecionado
    else:
        # Se o arquivo não estiver no caminho desejado, mostrar uma mensagem de aviso na tela
        CTkMessagebox(title="AVISO", message="Caminho do arquivo incorreto",
                          icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF") 




# Função de enquadramento atualizada para filtrar as unidades
categoria = ''
def enquadramento():
    global categoria, unidades_filtradas, valor_renda
    HIS1 = float(get("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Enquadramentos/HIS1.json").json())
    HIS2 = float(get("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Enquadramentos/HIS2.json").json())
    HMP = float(get("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Enquadramentos/HMP.json").json())
    try:
        valor_renda = float(funcoes.converter_valor_numerico(entry_renda.get()))
    except ValueError:
        valor_renda = 0
        CTkMessagebox(title="ALERTA", message="Insira um valor de renda válido",
                          icon="cancel",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
    if valor_renda != 0:    
        try:
            # Determina a categoria de renda do usuário
            if valor_renda <= HIS1:
                categoria = "HIS1"
            elif HIS1 < valor_renda <= HIS2:
                categoria = "HIS2"
            elif HIS2 < valor_renda <= HMP:
                categoria = "HMP"
            else:  # Renda acima de HMP, considerado R2V
                categoria = "R2V"

            # Define as categorias permitidas com base na categoria de renda do usuário
            if categoria == "HIS1":
                categorias_permitidas = ["HIS1", "HIS-1", "HIS 1", "HIS2", "HIS-2"," HIS 2", "HMP", "R2V"]
            elif categoria == "HIS2":
                categorias_permitidas = ["HIS2", "HIS-2", "HIS 2", "HMP", "R2V"]
            elif categoria == "HMP":
                categorias_permitidas = ["HMP", "R2V"]
            elif categoria == "R2V":
                categorias_permitidas = ["R2V"]  # R2V não pode adquirir HIS1

            # Cria um padrão regex para identificar as categorias permitidas
            categoria_pattern = "|".join(categorias_permitidas)

            # Filtra as unidades baseado no texto digitado e nas categorias permitidas
            texto_digitado = pesquisaUnidade.get().lower()
            unidades_filtradas = [unidade for unidade in opcoes_unidades if texto_digitado in unidade.lower() and re.search(categoria_pattern, unidade, re.IGNORECASE)]
            unidades.configure(values=unidades_filtradas)

            #habilitando proximas informações a serem colocadas e desabilitando a ja preenchida
            unidades.configure(state=ctk.NORMAL)
            pesquisaUnidade.configure(state=ctk.NORMAL, placeholder_text="Filtro")
            entry_renda.configure(state=ctk.DISABLED)
            button_continuar.configure(state= ctk.DISABLED)
            tooltip_unidades.configure(message= f"Categoria de Renda: {categoria}")

        except ValueError:
            CTkMessagebox(title="ALERTA", message="Por favor, selecione uma unidade valida.",
                            icon="cancel",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")

#função para reniciar a primeira tela            
def refazer_dados():
    global categoria
    funcoes.configurar_entry(entry_nome_arquivo,"")
    ButtonArquivo.configure(state=ctk.NORMAL)
    funcoes.configurar_entry(entry_renda,"")
    button_continuar.configure(state=ctk.DISABLED)
    funcoes.configurar_entry(pesquisaUnidade,"")
    selecao_var.set("Selecione")
    unidades.configure(state=ctk.DISABLED,fg_color= dark, text_color = 'white')
    button_gerar.configure(state=ctk.DISABLED)
    categoria = ""
    tooltip_unidades.configure(message= f"Categoria de Renda: {categoria}")

#Posições dos elementos Label e Entry

# titulo da label para escolher o arquivo
labelEscolher = ctk.CTkLabel(frameUnica, text="Nome do Arquivo", fg_color="#2f2f2f", bg_color=dark, text_color="#ffffff", font=("cabian", 15))
labelEscolher.place(x= 40, y=90)

# mostrar o nome do arquivo
entry_nome_arquivo = ctk.CTkEntry(frameUnica,placeholder_text="Nome do arquivo",fg_color="#2f2f2f", bg_color="#2f2f2f", text_color="#ffffff",
                        font=("arial bold", 15) ,border_color="#ffffff",width=420,state=ctk.DISABLED)
entry_nome_arquivo.place(x= 40, y=120 )  

#botão para selecionar o arquivo
ButtonArquivo = ctk.CTkButton(frameUnica, text="Inserir Arquivo",command=abrir_arquivo , corner_radius=10, text_color="#ffffff",
                                bg_color="#2F2F2F", fg_color="green", hover_color="#1E2", width=110, height=20)
ButtonArquivo.place(x=40, y=160) 

   
#Digite Renda
label_renda= ctk.CTkLabel(frameUnica, text="Renda",fg_color="#2F2F2F", 
                            font=("arial bold", 15), text_color="#ffffff")
label_renda.place(x=40, y=210) 
# place(x= 40, y=80)

entry_renda = ctk.CTkEntry(frameUnica, bg_color= "#2F2F2F", fg_color="#ffffff", state=ctk.DISABLED)
entry_renda.place(x=90, y=210)

button_continuar = ctk.CTkButton(frameUnica, text="Continuar",corner_radius=10, text_color="#ffffff",
                                    bg_color="#2F2F2F", fg_color="green", hover_color="#1E2", width=80, height=30,
                                    state=ctk.DISABLED)
button_continuar.place(x=240, y=210)
button_continuar.configure(command=enquadramento) # Atualiza o botão continuar para usar a função enquadramento corretamente


#Label Selecione a Unidade
labelSelecionar = ctk.CTkLabel(frameUnica, text="Selecione a Unidade",fg_color="#2f2f2f", bg_color="#2f2f2f", text_color="#ffffff",
                                font=("cabian", 15))
labelSelecionar.place(x= 40, y=260)

#Caixa de selecão
selecao_var = ctk.StringVar(value="Selecione")#aqui vai aparecer o nome no campo para não ficar vazio
StringVar_credito = ctk.StringVar(value="MCMV")

#Função da caixa de seleção 
empreendimento = ""
def selecionarUnidade(escolha):
    global valor_unidade, valor_unidade_desconto, empreendimento
    opcoes_unidades
    cont = -1
    #laço for para identificar linha escolhida la planilha
    try:
        for valor in opcoes_unidades:
            cont += 1
            if escolha == valor:
                break
        #declarando variaveis dos valores da unidade escolhida
        valor_unidade =  float(planilha.iloc[cont,-2])
        valor_unidade_desconto = float(planilha.iloc[cont,-1])
        Qtd_divi_parcelas = dados.iloc[0,2]
        Qtd_percen_parcelas = dados.iloc[0,3]
        Percen_anual = dados.iloc[0,4]
        Percen_peri = dados.iloc[0,5]
        Check_adimplencia = dados.iloc[0,6]

        #inserindo os primeiros valores da unidade
        empreendimento = Unidade(entry_nome_arquivo.get(),selecao_var.get(),
                                funcoes.converter_real(valor_unidade_desconto),
                                funcoes.converter_real(valor_unidade),0,0,0,0,0,
                                data_entrega, data_lancamento,Qtd_divi_parcelas,Qtd_percen_parcelas,
                                Percen_anual,Percen_peri, Check_adimplencia,"",categoria,
                                "","","")
        # verificando se a unidade é do enquadramento do cliente ou superior
        if categoria in escolha or (categoria[0:3]+"-"+categoria[3]) in escolha or (categoria[0:3]+" "+categoria[3]) in escolha:
            unidades.configure(fg_color= 'green', text_color = 'white')
        else:
            unidades.configure(fg_color= 'red', text_color = 'black')

        #hanilitando botão para ir para proxima tela
        button_gerar.configure(state=ctk.NORMAL)
    except ValueError:
            button_gerar.configure(state=ctk.DISABLED)
            CTkMessagebox(title="ALERTA", message="Por favor, selecione uma unidade valida.",
                        icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")


# caixa de seleção para escolher as unidades
unidades =ctk.CTkOptionMenu(frameUnica,
                    bg_color="#2f2f2f",
                    values=[""],
                    command=selecionarUnidade,
                    variable=selecao_var,
                    width=130, height=30, corner_radius=10,
                    fg_color=dark, button_color="green", button_hover_color="#1E2",
                    dropdown_text_color="white", dropdown_fg_color="#2f2f2f",dropdown_font=("arial bold", 15),
                    dropdown_hover_color="green", state=ctk.DISABLED)

unidades.place(x = 40 ,y=320)

tooltip_unidades = CTkToolTip(unidades, delay = 0.2, message = f"Categoria de Renda: {categoria}")

# caixa de seleção para selecionar a linha de credito escolhida pelo cliente
linha_credito = ctk.CTkOptionMenu(frameUnica, 
                    bg_color="#2f2f2f",
                    values=["MCMV", "SBPE / PRICE","SBPE / SAC"],
                    variable=StringVar_credito,
                    width=130, height=30, corner_radius=10,
                    fg_color=dark, button_color="green", button_hover_color="#1E2",
                    dropdown_text_color="white", dropdown_fg_color="#2f2f2f",dropdown_font=("arial bold", 15),
                    dropdown_hover_color="green")
linha_credito.place(x = 40,y=354)

# Pesquisa de unidade
pesquisaUnidade = ctk.CTkEntry(frameUnica, placeholder_text="Filtro", fg_color="#2f2f2f", bg_color="#2f2f2f", 
                               text_color="#ffffff",state=ctk.DISABLED,
                                font=("arial bold", 15), border_color="#ffffff")
pesquisaUnidade.place(x=40, y=285)
pesquisaUnidade.bind('<KeyRelease>', atualizar_lista)


#Botão refazer
button_refazer = ctk.CTkButton(frameUnica, text="Refazer",corner_radius=10, text_color="#ffffff",
                                    bg_color="#2F2F2F", fg_color="red", hover_color="#5D0000", width=80, height=30,
                                    command=refazer_dados)
button_refazer.place(x=280, y=355)

#Botão gerar
button_gerar = ctk.CTkButton(frameUnica, text="Gerar",corner_radius=10, text_color="#ffffff",state=ctk.DISABLED,
                                    bg_color="#2F2F2F", fg_color="green", hover_color="#1E2", width=80, height=30,
                                    command=lambda:segundaTela(TelaEscolher,base_path,icone,valor_unidade,valor_unidade_desconto, valor_renda,
                                                               empreendimento, StringVar_credito))
button_gerar.place(x=380, y=355)

TelaEscolher.mainloop()