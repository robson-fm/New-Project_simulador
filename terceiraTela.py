import customtkinter as ctk
import datetime
from tkinter import RIGHT,ttk
from CTkMessagebox import CTkMessagebox
import funcoes
from reportlab.platypus import Table, SimpleDocTemplate, Spacer, TableStyle, PageTemplate,Frame
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from numpy import array,delete,concatenate
from os import getlogin, path, system
from dateutil.relativedelta import relativedelta
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics import shapes
from reportlab.graphics.charts.textlabels import Label
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from requests import post

cm = 2.54
dark = "#242424"

# Variaval Global para com que ao clicar em gerar funcione
y_parcela = 70
datamensal = datetime.datetime.now()
dataanual = datetime.datetime(datamensal.year,12,1)
soma_parcelas = 0  # Inicializando a variável soma_parcelas
soma_parcelas_padrao = 0 
valor_alteravel = 0
valor_alteravel_padrao = 0
comparador = False
total_parcelas = 0

def terceiraTela(grandparent,parent,base_path,icone,lista_ato,valor_pro_soluto,parcela_bonus,renda,anual, valor_capacidade,
                 dados_unidade, valor_adim_premiada):
    global datamensal, dataanual, soma_parcelas,soma_parcelas_adicionais
    global soma_parcelas_padrao, y_parcela, dark, valor_alteravel, valor_alteravel_padrao
    global comparador, qtdParcelas, valoresParcelas, descParcelas, w , lista_cef, lista_cef_padrao
    global periodicidade, qtd_anual, soma_total_linear, qtd_parcelas_linear

    # Configuração inicial da tela
    ctk.set_appearance_mode("dark")
    telaInicial =  ctk.CTkToplevel(parent)
    parent.withdraw()
    telaInicial.title("Simulador")
    telaInicial.after(250, lambda: telaInicial.iconbitmap(icone))
    telaInicial.config(background=dark)
    telaInicial.geometry("1220x610")
    telaInicial.resizable(width=False, height=False)
    def on_closing():
        grandparent.destroy()

    telaInicial.protocol("WM_DELETE_WINDOW", on_closing)

    lista_parcela = []
    lista_cef = [["Parcela CEF", "Soma", "Porcentagem", "Index Parcela"]]
    lista_cef_padrao = [["Parcela CEF", "Soma", "Porcentagem", "Index Parcela"]]
    qtd_parcelas_linear = int(len(lista_ato)) + 1

    def enviar_erro_firebase(nome_func,erro):
        usuario = getlogin()
        dados = {
            "Usuario": usuario,
            "Data": datetime.datetime.now().strftime("%d/%m/%Y"),
            "Função": nome_func,
            "Empreendimento": str(dados_unidade.Empreendimento),
            "Erro": str(erro)
        }

        post("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Erros/.json",json=dados)


    
    # Configurando o estilo para o ttk.Notebook e ttk.Frame
    style = ttk.Style()
    style.configure("TNotebook", background="#2F2F2f")
    style.configure("TFrame", background=dark)
    # style.configure("TNotebook", width= "50", heigth="50" )

    def tooltip_treeview_padrao(event):
        textbox_tooltip_tb_padrao.delete("0.0","end")
        tree = event.widget
        if "!treeview" in str(tree):
            item = tree.identify_row(event.y)
            
            if tree.item(item,'values')!='':
                for item_lista in lista_cef_padrao:
                    if item in item_lista:
                        texto = f"Parcela CEF: {item_lista[0]}\nSoma: {item_lista[1]}\nPorcentagem: {item_lista[2]}"
                        break
                    else:
                        texto = ""
                
                if texto != "":
                    if event.y > 403:
                        posicao_y = 403
                    elif event.y < 60:
                        posicao_y = 60
                    else:
                        posicao_y = event.y
                    textbox_tooltip_tb_padrao.insert("0.0",text=texto)
                    textbox_tooltip_tb_padrao.place(x=180, y=posicao_y)
                else:
                    textbox_tooltip_tb_padrao.place_forget()
            else:
                textbox_tooltip_tb_padrao.place_forget()
        else:
            textbox_tooltip_tb_padrao.place_forget()

    def tooltip_treeview_linear(event):
        textbox_tooltip_tb_linear.delete("0.0","end")
        tree = event.widget
        if "!treeview" in str(tree):
            item = tree.identify_row(event.y)
            if tree.item(item,'values')!='':
                for item_lista in lista_cef:
                    if item in item_lista:
                        texto = f"Parcela CEF: {item_lista[0]}\nSoma: {item_lista[1]}\nPorcentagem: {item_lista[2]}"
                        break
                    else:
                        texto = ""
                
                if texto != "":
                    if event.y > 403:
                        posicao_y = 403
                    elif event.y < 60:
                        posicao_y = 60
                    else:
                        posicao_y = event.y
                    textbox_tooltip_tb_linear.insert("0.0",text=texto)
                    textbox_tooltip_tb_linear.place(x=515, y=posicao_y)
                else:
                    textbox_tooltip_tb_linear.place_forget()
            else:
                textbox_tooltip_tb_linear.place_forget()
        else:
            textbox_tooltip_tb_linear.place_forget()
    # Adicionando o CTkNotebook
    notebook = ttk.Notebook(telaInicial)
    notebook.place(x=20, y=20, width=1790, height=825)


    ####################################### Aba 1: Simulação Padrão #############################

    aba_simulacao_padrao = ttk.Frame(notebook)
    notebook.add(aba_simulacao_padrao, text="Tabela Padrão")  

    comparador = False
    qtd_anual = 0
    periodicidade = 0

    style = ttk.Style()

    style.layout('arrowless.Vertical.TScrollbar', 
            [('Vertical.Scrollbar.trough',
            {'children': [('Vertical.Scrollbar.thumb', 
                            {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])

    # Título
    titulo_label = ctk.CTkLabel(aba_simulacao_padrao, text="Tabela Padrão", fg_color=dark, 
                                font=("arial bold", 30), text_color="#ffffff")
    titulo_label.pack(pady=20, padx=5)


    # Container lado direito (Aba Simulação Padrão)
    frame_simulacao_padrao = ctk.CTkFrame(aba_simulacao_padrao, width=700, height=480, fg_color="#2F2F2F", bg_color=dark,
                                        border_width=0, corner_radius=30)
    frame_simulacao_padrao.place(x=400, y=60)

    #criando treeview das parcelas
    columns=('Descrição','Valor','Data')
    tabela_parcelas_padrao = ttk.Treeview(frame_simulacao_padrao,columns=columns, show='headings',height=26)
    
    #chamando função para organizar as colunas
    for col in columns:
        tabela_parcelas_padrao.heading(col, text=col, command=lambda _col=col: \
                    funcoes.treeview_ordenar_coluna(tabela_parcelas_padrao, _col, False))
        
    #declarando barra de rolagem
    vsb = ttk.Scrollbar(frame_simulacao_padrao,orient='vertical',command=tabela_parcelas_padrao.yview,style='arrowless.Vertical.TScrollbar')
    vsb.pack(side=RIGHT, fill="y")
    tabela_parcelas_padrao.configure(yscrollcommand=vsb.set)
    funcoes.configurar_treeview(tabela_parcelas_padrao,"Descrição",260)
    funcoes.configurar_treeview(tabela_parcelas_padrao,"Valor",200)
    funcoes.configurar_treeview(tabela_parcelas_padrao,"Data",140)
    tabela_parcelas_padrao.pack(fill="both")
    textbox_tooltip_tb_padrao = ctk.CTkTextbox(
        master=aba_simulacao_padrao,
        fg_color="#2F2F2F",
        text_color="#ffffff",
        font=("arial bold", 15),
        corner_radius=20,
        border_color="#34C7C8",
        border_width=1,
        width=220,
        height=95,
        activate_scrollbars=False
    )
    telaInicial.bind("<Motion>",tooltip_treeview_padrao)

    check_var = ctk.StringVar(value="on")
    legenda_aviso = ctk.CTkCheckBox(telaInicial, text="Soma Parcela maior que 30% da renda",variable=check_var, 
                                onvalue="on", offvalue="off",state=ctk.DISABLED,font=("arial bold", 10),
                                checkmark_color="yellow",fg_color="yellow",checkbox_height=15,
                                checkbox_width=12,text_color_disabled="#ffffff")
    
    legenda_limite = ctk.CTkCheckBox(telaInicial, text="Soma Parcela maior que 40% da renda",variable=check_var, 
                                onvalue="on", offvalue="off",state=ctk.DISABLED,font=("arial bold", 10),
                                checkmark_color="red",fg_color="red",checkbox_height=15,
                                checkbox_width=12,text_color_disabled="#ffffff")
    legenda_limite.place(x=628, y=538)

    def comparar_datas():
        global dataanual, datamensal
        data_comparar_anual = dataanual.strftime("%b/%Y")
        data_comparar_mensal = datamensal.strftime("%b/%Y")
        comparador_anual = funcoes.comparar_data(str(data_comparar_anual),dados_unidade.Data_Entrega, "Anual")
        comparador_mensal = funcoes.comparar_data(str(data_comparar_mensal),dados_unidade.Data_Entrega, "Mensal")

        if comparador_anual == True and comparador_mensal == True:
            return True
        return False

    def adicionar_parcela_padrao():
        global soma_parcelas_padrao, y_parcela, valor_alteravel_padrao,comparador, lista_cef_padrao
        global periodicidade, data_peri, total_parcelas
        try:
            valor_alteravel_padrao = pro_soluto
            lista_data_padrao = []
            lista_data_parcela_adimplencia = []
            valor_parcela_adim_premiada = 0
            soma_final = 0
            data_peri = datetime.datetime.now() + relativedelta(months=37)

            string_parcelas = str(dados_unidade.Qtd_divi_parcelas)
            string_porcentagem = str(dados_unidade.Qtd_percen_parcelas)
            porcetagem_anual = float(dados_unidade.Percen_anual)
            porcetagem_periodicidade = float(dados_unidade.Percen_peri)

            divi_parcelas = string_parcelas.split("|")
            divi_porcentagem = string_porcentagem.split("|")

            soma_valores = sum(float(valor) for valor in divi_parcelas)
            
            comparador = comparar_datas()
            if comparador == True:
                return CTkMessagebox(title="ALERTA", message="Parcela atingiu a data limite",
                            icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
            if valor_pro_soluto > 0:
                try:
                    desc_Parcelas =  "Mensal"
                    while comparador == False:
                        dataParcela = gerar_data(desc_Parcelas)
                        lista_data_padrao.append(dataParcela)
                        comparador = funcoes.comparar_data(dataParcela,dados_unidade.Data_Entrega,desc_Parcelas)
                    
                    lista_data_padrao.pop(-1)
                    
                    for i in range(len(lista_ato) - 1):
                        lista_data_padrao.pop(0)
                    
                    p = 25
                    q = 50
                    w = 0.2
                    v20 = (1 - w)/len(lista_data_padrao)

                    if dados_unidade.Check_adimplencia == "Sim":
                        qtd_adim_premiada = 0
                        lista_data_parcela_adimplencia = []
                        for x in range(len(lista_data_padrao)):
                            if x % 6 == 0 and x > 0:
                                qtd_adim_premiada +=1
                            
                        valor_parcela_adim_premiada = round(valor_adim_premiada/qtd_adim_premiada,2)

                        for y in range(qtd_adim_premiada):
                            data_parcela_adimplencia = lista_data_padrao[-1]
                            lista_data_padrao.pop(-1)
                            lista_data_parcela_adimplencia.append(data_parcela_adimplencia)
                        lista_data_parcela_adimplencia.reverse()


                    if porcetagem_periodicidade > 0:
                        soma_valores +=1

                    if qtd_anual > 0:
                        divisao_porcentagem_anual = porcetagem_anual/qtd_anual
                        resultado_anual = divisao_porcentagem_anual * valor_pro_soluto
                        soma_final_anual = resultado_anual - anual
                        soma_final += qtd_anual*anual
                        dif_mesais = round((soma_final_anual*qtd_anual)/soma_valores,2)
                    else:
                        dif_mesais = 0

                    if porcetagem_periodicidade > 0:
                        periodicidade = valor_pro_soluto*porcetagem_periodicidade + dif_mesais
                        soma_final += periodicidade
                        tabela_parcelas_padrao.insert("","end",values=("Periodicidade",funcoes.converter_real(periodicidade),
                                                                ENparaBR(data_peri.strftime("%b/%Y"))), tags = "ok")
                        soma_valores -= 1
            

                    if len(lista_data_padrao) == soma_valores:
                        
                        lista_parcela = []

                        count = 0
                        for val in divi_parcelas:
                            val_porcentagem = float(divi_porcentagem[count])/float(val)
                            valor_parcelas = valor_pro_soluto*val_porcentagem+dif_mesais
                            soma_final += valor_parcelas*float(val)
                            count+=1
                            for i in range(int(val)):
                                lista_parcela.append(valor_parcelas)

                        count_data = 0
                        for data in lista_data_padrao:
                            valorParcelas = float(lista_parcela[count_data])
                            soma_parcelas_padrao += valorParcelas
                            x = w * (float(valor_capacidade) * 0.85) + p + q
                            w = w + v20
                            parcela_cef = round(x,0)
                            soma_parcelas_cef = round(valorParcelas + parcela_cef,0)  
                            porcentagem_cef = soma_parcelas_cef/renda * 100
                            item = tabela_parcelas_padrao.insert("","end",values=(desc_Parcelas,funcoes.converter_real(valorParcelas),
                                                                    data), tags=(funcoes.treeview_tag(renda,soma_parcelas_cef,
                                                                                                    desc_Parcelas)))
                            
                            lista_cef_padrao.append([funcoes.converter_real(parcela_cef), 
                                            funcoes.converter_real(soma_parcelas_cef),
                                            f"{round(porcentagem_cef,2)}%",str(item)])  
                            tabela_parcelas_padrao.tag_configure("aviso", background="yellow", foreground="black")
                            tabela_parcelas_padrao.tag_configure("limite", background="red")
                            count_data += 1

                        for data in lista_data_parcela_adimplencia:
                            x = w * (float(valor_capacidade) * 0.85) + p + q
                            w = w + v20
                            parcela_cef = round(x,0)
                            soma_parcelas_cef = round(valor_parcela_adim_premiada + parcela_cef,0)
                            porcentagem_cef = soma_parcelas_cef/renda * 100
                            item = tabela_parcelas_padrao.insert("","end",values=("Adimplência Premiada",
                                                                        funcoes.converter_real(valor_parcela_adim_premiada),
                                                                        data), tags=(funcoes.treeview_tag(renda,soma_parcelas_cef,
                                                                                                    "Adimplência Premiada")))
                            lista_cef_padrao.append([funcoes.converter_real(parcela_cef), 
                                            funcoes.converter_real(soma_parcelas_cef),
                                            f"{round(porcentagem_cef,2)}%",str(item)]) 
                            tabela_parcelas_padrao.tag_configure("aviso", background="yellow", foreground="black")
                            tabela_parcelas_padrao.tag_configure("limite", background="red")

                            item = tabela_parcelas_linear.insert("","end",values=("Adimplência Premiada",
                                                                            funcoes.converter_real(valor_parcela_adim_premiada),
                                                                            data), tags=(funcoes.treeview_tag(renda,soma_parcelas_cef,
                                                                                                    "Adimplência Premiada")))
                            lista_cef.append([funcoes.converter_real(parcela_cef), 
                                            funcoes.converter_real(soma_parcelas_cef),
                                            f"{round(porcentagem_cef,2)}%",str(item)]) 
                            tabela_parcelas_linear.tag_configure("aviso", background="yellow", foreground="black")
                            tabela_parcelas_linear.tag_configure("limite", background="red")
                            total_parcelas -= 1     
                            StringVar_parcelas_faltantes.set(value=str(total_parcelas))               
                
                        valor_alteravel_padrao -= soma_parcelas_padrao

                        funcoes.treeview_ordenar_coluna(tabela_parcelas_padrao,"Descrição",False)

                        if round(valor_alteravel_padrao,2) >= 1000:
                            button_gera_pdf_padrao.configure(state= ctk.DISABLED)
                        else:
                            button_gera_pdf_padrao.configure(state= ctk.NORMAL)
                    else:
                        CTkMessagebox(title="ERRO", message="Divisão desigual ao valor total de parcelas possiveis",
                                icon="cancel",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")

                except ValueError:
                    CTkMessagebox(title="ALERTA", message="Por favor, insira números válidos para o número e valor da parcela.",
                                icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
        except Exception as e:
            enviar_erro_firebase("adicionar_parcela_padrao",e)
    # Botão Gerar pdf para a aba Tabela Padrão
    button_gera_pdf_padrao = ctk.CTkButton(aba_simulacao_padrao, text="Gerar PDF", bg_color=dark, fg_color="blue",
                                        font=("arial bold", 13), text_color="#ffffff", corner_radius=10,
                                        hover_color="#0066aa", width=120, height=30,command=lambda t="padrão": gerar_pdf(t))
    # Inicialmente escondido
    button_gera_pdf_padrao.place(x=1050, y=490)

    # Função para alternar elementos com base na aba selecionada
    def on_tab_changed(event):
        selecionar_aba_tabela = notebook.tab(notebook.select(), "text")
        
        if selecionar_aba_tabela == "Tabela Linear":
            # Mostrar elementos da Tabela Linear
            button_nova_proposta.place(x=20, y=50)
            botao_limpar.place(x=820, y=575)
            button_voltar.place(x=955, y=575)
            button_gera_pdf.place(x=1085, y=575)
            label_falta_pagar.place(x=315, y=575)
            entry_falta_pagar.place(x=408, y=575)
            label_soma_parcelas.place(x=543, y=575)
            entry_soma_parcelas.place(x=687, y=575)
            label_parcelas_faltantes.place(x=15, y=575)
            entry_parcelas_faltantes.place(x=230, y=575)
            legenda_aviso.place(x=725, y=538)
            legenda_limite.place(x=928, y=538)
            # Ocultar elementos específicos da Tabela Padrão (se houver)
        elif selecionar_aba_tabela == "Tabela Padrão":
            # Ocultar elementos da Tabela Linear
            button_nova_proposta.place(x=20, y=50)
            botao_limpar.place_forget()
            button_voltar.place(x=930, y=528.5)
            button_gera_pdf.place_forget()
            label_falta_pagar.place_forget()
            entry_falta_pagar.place_forget()
            label_soma_parcelas.place_forget()
            entry_soma_parcelas.place_forget()
            label_parcelas_faltantes.place_forget()
            entry_parcelas_faltantes.place_forget()
            legenda_aviso.place(x=425, y=538)
            legenda_limite.place(x=628, y=538)
            # Mostrar elementos específicos da Tabela Padrão (se houver)
            

    ####################################### Aba 2: Tabela Linear #######################################
    aba_tabela_linear = ttk.Frame(notebook)
    notebook.add(aba_tabela_linear, text="Tabela Linear")
 
    # Adicione todo o código relacionado à Tabela Linear aqui

    # lista_parcela = []
    # lista_cef = [["Parcela CEF", "Soma", "Porcentagem", "Index Parcela"]]
    soma_total_linear = 0

    comparador = False

    style = ttk.Style()

    style.layout('arrowless.Vertical.TScrollbar', 
            [('Vertical.Scrollbar.trough',
            {'children': [('Vertical.Scrollbar.thumb', 
                            {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])

    # Título
    titulo_label = ctk.CTkLabel(aba_tabela_linear, text="Tabela Linear", fg_color=dark, 
                                font=("arial bold", 30), text_color="#ffffff")
    titulo_label.pack(pady=20, padx=5)

    # Container lado esquerdo (Aba Tabela Linear)
    frame1_tabela_linear = ctk.CTkFrame(aba_tabela_linear, width=500, height=440, fg_color="#2F2F2F", bg_color=dark,
                                    border_width=0, corner_radius=30)
    frame1_tabela_linear.place(x=50, y=60)

    qtdParcelas = []
    valoresParcelas = []
    descParcelas = []
    opcao_desc = ["Mensal"]
    y_parcela = 70

    # Entry para digitar a quantidade parcelas
    labelParcelas = ctk.CTkLabel( frame1_tabela_linear, text="Parcelas", text_color="#ffffff", bg_color="#2F2F2F")
    labelParcelas.place(x=70, y=40)    
    labelValorParcelas = ctk.CTkLabel( frame1_tabela_linear, text="Valor da Parcela", text_color="#ffffff", bg_color="#2F2F2F")
    labelValorParcelas.place(x=160, y=40) 
    labelDescParcelas = ctk.CTkLabel( frame1_tabela_linear, text="Descrição", text_color="#ffffff", bg_color="#2F2F2F")
    labelDescParcelas.place(x=300, y=40) 

    #criando as primeiras parcelas e alimentando a lista das variaveis
    campos_iniciais = funcoes.parcelas_Novas(y_parcela, frame1_tabela_linear)
    qtdParcelas.append(campos_iniciais[0])
    valoresParcelas.append(campos_iniciais[1])
    descParcelas.append(campos_iniciais[2])

    # Container lado direito (Aba Tabela Linear)
    frame2_tabela_linear = ctk.CTkFrame(aba_tabela_linear, width=500, height=480, fg_color="#2F2F2F", bg_color=dark,
                                        border_width=0, corner_radius=30)
    frame2_tabela_linear.place(x=700, y=60)

    #criando treeview das parcelas
    columns=('Descrição','Valor','Data')
    tabela_parcelas_linear = ttk.Treeview(frame2_tabela_linear,columns=columns, show='headings',height=26)
    
    #chamando função para organizar as colunas
    for col in columns:
        tabela_parcelas_linear.heading(col, text=col, command=lambda _col=col: \
                    funcoes.treeview_ordenar_coluna(tabela_parcelas_linear, _col, False))
    #declarando barra de rolagem
    vsb = ttk.Scrollbar(frame2_tabela_linear,orient='vertical',command=tabela_parcelas_linear.yview,style='arrowless.Vertical.TScrollbar')
    vsb.pack(side=RIGHT, fill="y")
    tabela_parcelas_linear.configure(yscrollcommand=vsb.set)
    funcoes.configurar_treeview(tabela_parcelas_linear,"Descrição",260)
    funcoes.configurar_treeview(tabela_parcelas_linear,"Valor",200)
    funcoes.configurar_treeview(tabela_parcelas_linear,"Data",140)
    tabela_parcelas_linear.pack(fill="both")
    textbox_tooltip_tb_linear = ctk.CTkTextbox(
        master=aba_tabela_linear,
        fg_color="#2F2F2F",
        bg_color="#2F2F2F",
        text_color="#ffffff",
        font=("arial bold", 15),
        corner_radius=20,
        border_color="#34C7C8",
        border_width=1,
        width=220,
        height=95,
        activate_scrollbars=False,
        
    )
    tabela_parcelas_linear.bind("<Motion>",tooltip_treeview_linear)

    # Variável para a soma das parcelas
    soma_parcelas = 0
    soma_parcelas_adicionais = 0
    StringVar_prosoluto = ctk.StringVar(value=funcoes.converter_real(valor_pro_soluto))
    StringVar_soma_parcelas = ctk.StringVar(value=funcoes.converter_real(soma_parcelas))
    StringVar_parcelas_faltantes = ctk.StringVar(value=str(total_parcelas))  


    # Label para exibir a numero de parcelas faltantes
    label_parcelas_faltantes = ctk.CTkLabel(telaInicial, text="Número de Parcelas Faltantes: ",
                            font=("arial bold", 15),text_color="#ffffff", bg_color="#2F2F2F", corner_radius=20)

    entry_parcelas_faltantes = ctk.CTkEntry(telaInicial, textvariable=StringVar_parcelas_faltantes, fg_color="#2f2f2f", bg_color="#2f2f2f", 
                                    text_color="#ffffff", font=("arial bold", 15) ,border_color="#2F2F2F",width=50,
                                    state=ctk.DISABLED)

    # Label para exibir a soma total das parcelas
    label_falta_pagar = ctk.CTkLabel(telaInicial, text="Falta Pagar:",font=("arial bold", 15),
                                    text_color="#ffffff", bg_color="#2F2F2F", corner_radius=80)

    entry_falta_pagar = ctk.CTkEntry(telaInicial, textvariable=StringVar_prosoluto, fg_color="#2f2f2f", bg_color="#2f2f2f", 
                                    text_color="#ffffff", font=("arial bold", 15) ,border_color="#2F2F2F",width=115,
                                    state=ctk.DISABLED)

    # Label para exibir a soma total das parcelas
    label_soma_parcelas = ctk.CTkLabel(telaInicial, text="Soma das Parcelas:",font=("arial bold", 15),
                                    text_color="#ffffff", bg_color="#2F2F2F", corner_radius=80)

    entry_soma_parcelas = ctk.CTkEntry(telaInicial, textvariable=StringVar_soma_parcelas, fg_color="#2f2f2f", bg_color="#2f2f2f", 
                                    text_color="#ffffff", font=("arial bold", 15) ,border_color="#2F2F2F",width=100,
                                    state=ctk.DISABLED)

    # Variável para verificar se é a primeira vez que a função está sendo chamada
    datamensal = datetime.datetime.now()
    dataanual = datetime.datetime(datamensal.year,12,1)


    # Função para limpar dados
    def limpar_dados():
        global soma_parcelas, soma_parcelas_adicionais,datamensal, dataanual, y_parcela, lista_cef,soma_total_linear
        global lista_parcela, w, qtd_anual, lista_cef_padrao,qtd_parcelas_linear

        soma_parcelas = 0
        soma_parcelas_adicionais = 0
        soma_total_linear = 0
        datamensal = datetime.datetime.now()
        dataanual = datetime.datetime(datamensal.year, 12, 1)
        button_gera_pdf.configure(state=ctk.DISABLED)
        lista_parcela = []
        lista_cef = [["Parcela CEF", "Soma", "Porcentagem", "Index Parcela"]]
        lista_cef_padrao = [["Parcela CEF", "Soma", "Porcentagem", "Index Parcela"]]  
        qtd_parcelas_linear = int(len(lista_ato)) + 1
        w = 0.2
        
        # Destruir widgets adicionais, mantendo o 'ato' e 'bônus da parcela'
        if len(qtdParcelas) > 0:  # Assumindo que o primeiro conjunto de widgets é para o 'ato'
            for widgets in [qtdParcelas[1:], valoresParcelas[1:], descParcelas[1:]]:
                for widget in widgets:
                    widget.destroy()

            # Limpa as listas, mas mantém a primeira entrada
            del qtdParcelas[1:]
            del valoresParcelas[1:]
            del descParcelas[1:]

        # Resetar a posição y inicial para a criação das novas parcelas
        y_parcela = 70

        # Se a primeira entrada de parcela foi desabilitada, habilitá-la para limpeza
        if qtdParcelas:
            qtdParcelas[0].configure(state=ctk.NORMAL, text_color="#2F2F2F", fg_color="#fFfFfF")
            qtdParcelas[0].delete(0, ctk.END)

        if valoresParcelas:
            valoresParcelas[0].configure(state=ctk.NORMAL, text_color="#2F2F2F", fg_color="#fFfFfF")
            valoresParcelas[0].delete(0, ctk.END)
            
        if descParcelas:
            descParcelas[0].configure(state="readonly", text_color="#2F2F2F", fg_color="#fFfFfF")  # Se o combobox estiver desabilitado
            descParcelas[0].insert(0,"Mensal")  # Ou qualquer que seja o valor padrão

        # Limpa a tabela de parcelas, mantendo o 'ato' e 'bônus da parcela'
        for i in tabela_parcelas_linear.get_children():
            tabela_parcelas_linear.delete(i)

        for i in tabela_parcelas_padrao.get_children():
            tabela_parcelas_padrao.delete(i)

        # Atualiza o total de parcelas
        StringVar_prosoluto.set(funcoes.converter_real(pro_soluto))    
        StringVar_soma_parcelas.set(funcoes.converter_real(soma_parcelas))
       
        # Recriando as entradas iniciais para 'ato' e 'bônus da parcela'
        qtd_anual = 0
        parcelas_anuais()
        parcelas_iniciais_padrao()
        valoresparcelaCEF()
        adicionar_parcela_padrao()
        parcelas_iniciais()
       
    #função para gerar data com base na descrição
    def gerar_data(desc_Parcelas):
        global dataanual,datamensal
        if desc_Parcelas == "Mensal":
            ano = int(datamensal.strftime("%Y"))
            mes = int(datamensal.strftime("%m"))
            dataParcela = datamensal.strftime("%b/%Y")
            
            # laço se para caso o mês chegue em Dezembro(12), voltar para Janeiro(1) e ir para o próximo ano
            
            if mes >= 12:
                mes = 1
                ano += 1

            # caso negativo somente vai para o proximo mês
            else:
                mes += 1

            # inserindo novo valor de data para puxar o nome do mês
            datamensal = datetime.datetime(ano,mes,1)
        elif desc_Parcelas == "Anual":
            ano = int(dataanual.strftime("%Y"))
            dataParcela = dataanual.strftime("%b/%Y")
            ano +=1
            dataanual = datetime.datetime(ano,12,1)

        return ENparaBR(dataParcela) 
    
    def ENparaBR(texto):
        lista_EN = {1: 'Jan', 2: 'Feb', 3: 'Mar',  4: 'Apr',  5: 'May',  6: 'Jun',
              7: 'Jul',  8: 'Aug',  9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        lista_BR = {1: 'Jan',  2: 'Fev',  3: 'Mar',  4: 'Abr',  5: 'Mai',  6: 'Jun',
              7: 'Jul',  8: 'Ago',  9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        for mesnum, mes in lista_EN.items():
            if mes in texto:
                texto_subs = texto.replace(mes,lista_BR[mesnum])
                return texto_subs
    
    # função para inserir os valores na treeview a partir dos valores recebidos da tela anterio
    def parcelas_iniciais():
        global datamensal, pro_soluto, soma_parcelas
        datamensal = datetime.datetime.now()
        texto_ato = "Ato"
        count_ato = 0
        for ato in lista_ato:
            if count_ato == 1:
                texto_ato = "Parcela 30 Dias"
            elif count_ato == 2:
                texto_ato = "Parcela 60 Dias"
            
            dataAto = gerar_data("Mensal")
            tabela_parcelas_linear.insert("","end",values=(texto_ato,funcoes.converter_real(ato),dataAto), tags="ok")
            lista_cef.insert(1,["","","",""])
            count_ato += 1
        
        tabela_parcelas_linear.insert("","end",values=("Parcela Bônus",parcela_bonus,ENparaBR(dados_unidade.Data_Entrega)),
                            tags= "ok")
        tabela_parcelas_linear.insert("","end",values=("Periodicidade",funcoes.converter_real(periodicidade),
                                                            ENparaBR(data_peri.strftime("%b/%Y"))), tags = "ok")
        pro_soluto-= periodicidade
        soma_parcelas += periodicidade
        StringVar_prosoluto.set(funcoes.converter_real(pro_soluto))    
        StringVar_soma_parcelas.set(funcoes.converter_real(soma_parcelas))
        
        funcoes.treeview_ordenar_coluna(tabela_parcelas_linear,"Descrição",False)

    def parcelas_iniciais_padrao():
        texto_ato = "Ato"
        count_ato = 0
        for ato in lista_ato:
            if count_ato == 1:
                texto_ato = "Parcela 30 Dias"
            elif count_ato == 2:
                texto_ato = "Parcela 60 Dias"

            dataAto = gerar_data("Mensal")  
            tabela_parcelas_padrao.insert("","end",values=(texto_ato,funcoes.converter_real(ato),dataAto), tags="ok")
            lista_cef_padrao.append(["","","",""])
            count_ato += 1

        tabela_parcelas_padrao.insert("","end",values=("Parcela Bônus",parcela_bonus,ENparaBR(dados_unidade.Data_Entrega)),
                            tags= "ok")
           
    def parcelas_anuais():
        global pro_soluto, soma_parcelas, qtd_anual
        pro_soluto =  valor_pro_soluto
        if anual > 0:
            comparador_anual = comparar_datas()
            while comparador_anual == False:
                dataAnual = gerar_data("Anual")
                comparador_anual = funcoes.comparar_data(dataAnual,dados_unidade.Data_Entrega, "Anual")
                if comparador_anual == False:
                    tabela_parcelas_padrao.insert("","end",values=("Anual",funcoes.converter_real(anual),dataAnual), tags="ok")
                    tabela_parcelas_linear.insert("","end",values=("Anual",funcoes.converter_real(anual),dataAnual), tags="ok")
                    pro_soluto-=anual
                    soma_parcelas += anual
                    qtd_anual += 1
                    StringVar_prosoluto.set(funcoes.converter_real(pro_soluto))    
                    StringVar_soma_parcelas.set(funcoes.converter_real(soma_parcelas))

    # função para verificar se tanto as mensais quanto as anuais passaram da data permitida
    def comparar_datas():
        global dataanual, datamensal
        data_comparar_anual = dataanual.strftime("%b/%Y")
        data_comparar_mensal = datamensal.strftime("%b/%Y")
        comparador_anual = funcoes.comparar_data(str(data_comparar_anual),dados_unidade.Data_Entrega, "Anual")
        comparador_mensal = funcoes.comparar_data(str(data_comparar_mensal),dados_unidade.Data_Entrega, "Mensal")

        if comparador_anual == True and comparador_mensal == True:
            return True
        return False

    def valoresparcelaCEF():
        global v20,p,q,w, comparador, datamensal, total_parcelas
        lista_data = []
        while comparador == False:
            dataParcela = gerar_data("Mensal")
            lista_data.append(dataParcela)
            comparador = funcoes.comparar_data(dataParcela,dados_unidade.Data_Entrega,"Mensal")

        datamensal = datetime.datetime.now()
        gerar_data("Mensal")
        comparador == False

        p = 25
        q = 50
        w = 0.2
        v20 = (1 - w)/(len(lista_data)-1)

        total_parcelas = (len(lista_data)-1)
        StringVar_parcelas_faltantes.set(value=str(total_parcelas)) 
     
    # Função para adicionar parcelas ao Listbox no frame2 e atualizar a soma
    def adicionar_parcela():
        global soma_parcelas_adicionais, y_parcela, valor_alteravel,comparador, w
        global total_parcelas, soma_total_linear,qtd_parcelas_linear
        valor_alteravel = pro_soluto
        
        comparador = comparar_datas()
        if comparador == True:
            return CTkMessagebox(title="ALERTA", message="Parcela atingiu a data limite",
                        icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
        try:
            if valoresParcelas:
                valores = funcoes.parcelas_Anteriores(qtdParcelas,valoresParcelas,descParcelas)
                numeroParcelas = valores[0]
                valorParcelas = valores[1]
                desc_Parcelas = valores[2]

            y_parcela += 30
            novos_valores = funcoes.parcelas_Novas(y_parcela,frame1_tabela_linear)
            qtdParcelas.append(novos_valores[0])
            valoresParcelas.append(novos_valores[1])
            descParcelas.append(novos_valores[2])
            
            for i in range(numeroParcelas):
                dataParcela = gerar_data(desc_Parcelas)

                comparador = funcoes.comparar_data(dataParcela,dados_unidade.Data_Entrega,desc_Parcelas)
                if comparador == True:
                    CTkMessagebox(title="ALERTA", message="Parcela atingiu a data limite",
                        icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
                    break
                
                lista_parcela.append(funcoes.converter_real(valorParcelas))
                soma_parcelas_adicionais += valorParcelas
                x = w * (float(valor_capacidade) * 0.85) + p + q
                w = w + v20
                parcela_cef = round(x,0)
                soma_parcelas_cef = round(valorParcelas + parcela_cef,0)  
                porcentagem_cef = soma_parcelas_cef/renda * 100    
                item = tabela_parcelas_linear.insert("","end",values=(desc_Parcelas,funcoes.converter_real(valorParcelas),
                                                        dataParcela), tags=(funcoes.treeview_tag(renda,soma_parcelas_cef,desc_Parcelas)))
                lista_cef.insert(qtd_parcelas_linear,[funcoes.converter_real(parcela_cef), 
                                funcoes.converter_real(soma_parcelas_cef),
                                            f"{round(porcentagem_cef,2)}%",str(item)]) 
                tabela_parcelas_linear.tag_configure("aviso", background="yellow", foreground="black")
                tabela_parcelas_linear.tag_configure("limite", background="red")
                qtd_parcelas_linear += 1
          
            valor_alteravel -= soma_parcelas_adicionais
            soma_total_linear = soma_parcelas + soma_parcelas_adicionais
            StringVar_prosoluto.set(funcoes.converter_real(valor_alteravel))
            StringVar_soma_parcelas.set(funcoes.converter_real(soma_total_linear))

            # Atualização correta do número de parcelas faltantes
            total_parcelas -= numeroParcelas
            StringVar_parcelas_faltantes.set(str(total_parcelas))  
           
            if round(valor_alteravel,2) > 10 or round(valor_alteravel,2) < -10 or  (total_parcelas) > 3:
                button_gera_pdf.configure(state= ctk.DISABLED)
            else:
                button_gera_pdf.configure(state= ctk.NORMAL)

            funcoes.treeview_ordenar_coluna(tabela_parcelas_linear,"Descrição",False)
        except ValueError:
            CTkMessagebox(title="ALERTA", message="Por favor, insira números válidos para o número e valor da parcela.",
                        icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF")
            
    def inserir_resto_peri(resto):
        global periodicidade, valor_alteravel
        periodicidade += resto
        valor_alteravel -= resto
        total_parcelas = soma_total_linear
        total_parcelas += resto
    
        StringVar_prosoluto.set(funcoes.converter_real(valor_alteravel))
        StringVar_soma_parcelas.set(funcoes.converter_real(total_parcelas))
   
    def gerar_pdf(tipo):
        global lista_cef_padrao, lista_cef
        tabela_unida_padrao = []
        tabela_unida_linear = []
        styles = getSampleStyleSheet()
        GRID_STYLE = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT')])

        GRID_STYLE2 = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT')])
        
        STYLE_TITULO_TABELA = ParagraphStyle(
              name = 'TitleStyle',
              parent=styles['Heading1'],
              fontSize=25,
              color= 'black',
              alignment=1)
        
        style = styles["Normal"]

        # criando a lista tabela e colocando os valores iniciais
        try:
            tabela_padrao = []
            tag_tabela_padrao = []
            tabela_padrao.append(["Descrição", "Valor", "Data"])
            tag_tabela_padrao.append(["ok"])

            # inserindo valores e suas respectivas tags nas listas
            for child in tabela_parcelas_padrao.get_children():
                tabela_padrao.append(tabela_parcelas_padrao.item(child)["values"])
                tag_tabela_padrao.append(tabela_parcelas_padrao.item(child)["tags"])

            dif_tabelas_padrao =  len(tabela_padrao) - len(lista_cef_padrao)
            for i in range(dif_tabelas_padrao):
                lista_cef_padrao.append(["","","",""])
                
            lista_cef_padrao_pdf = delete(lista_cef_padrao,(3),axis=1)
        
            tabela_unida_padrao = concatenate((tabela_padrao,lista_cef_padrao_pdf),axis=1)

            t1 = Table(array(tabela_unida_padrao).tolist())

            if tipo == "linear":
                tabela_linear = []
                tag_tabela_linear = []
                tabela_linear.append(["Descrição", "Valor", "Data"])
                tag_tabela_linear.append(["ok"])

                for child in tabela_parcelas_linear.get_children():
                    valor = tabela_parcelas_linear.item(child)["values"]

                    localizar = valor[0].find("Periodicidade")

                    if localizar == 0:
                        if valor_alteravel != 0:
                            CTkMessagebox(title="Aviso", message="Valor restante inserido na parcela de periodicidade",
                            icon="warning", fg_color="#2F2F2F", text_color="#FFFFFF", title_color="#FFFFFF")
                            inserir_resto_peri(valor_alteravel)
                            tabela_parcelas_linear.item(child, values=("Periodicidade",funcoes.converter_real(periodicidade),
                                                                    ENparaBR(data_peri.strftime("%b/%Y"))), tags = "ok")

                    tabela_linear.append(tabela_parcelas_linear.item(child)["values"])
                    tag_tabela_linear.append(tabela_parcelas_linear.item(child)["tags"])

                dif_tabelas_linear =  len(tabela_linear) - len(lista_cef)
                for i in range(dif_tabelas_linear):
                    lista_cef.append(["","","",""])

                
                lista_cef_pdf = delete(lista_cef,(3),axis=1)

                tabela_unida_linear = concatenate((tabela_linear,lista_cef_pdf),axis=1)

            # criando uma table para o documento

            
                t2 = Table(array(tabela_unida_linear).tolist())
            
            index = 0

            d = shapes.Drawing(200, 100)

            # mark the origin of the label
            d.add(shapes.Circle(100,90,5, fillColor=colors.yellow))

            lab = Label()
            lab.setOrigin(100,90)
            lab.dx = 87
            lab.dy = 1
            lab.setText('Soma Parcela maior que 30% da renda')

            d.add(lab)

            d.add(shapes.Circle(300,90,5, fillColor=colors.red))

            lab = Label()
            lab.setOrigin(300,90)
            lab.dx = 87
            lab.dy = 1
            lab.setText('Soma Parcela maior que 40% da renda')

            d.add(lab)

            # laço for para colocar a cor na tabela do documento com base na tag da linha
            for row in range(len(tabela_padrao)):
                taglida = str(tag_tabela_padrao[index])
                if taglida == "['limite']":
                    GRID_STYLE.add('BACKGROUND', (0, row), (-1, row), colors.red)
                elif taglida == "['aviso']":
                    GRID_STYLE.add('BACKGROUND', (0, row), (-1, row), colors.yellow)
                index += 1
            
            if tipo == "linear":
                index = 0
                for row in range(len(tabela_linear)):
                    taglida = str(tag_tabela_linear[index])
                    if taglida == "['limite']":
                        GRID_STYLE2.add('BACKGROUND', (0, row), (-1, row), colors.red)
                    elif taglida == "['aviso']":
                        GRID_STYLE2.add('BACKGROUND', (0, row), (-1, row), colors.yellow)
                    index += 1
            element = []
            # definindo variáveis para texto no arquivo
            falta_text = label_falta_pagar.cget("text") + " "
            soma_text = label_soma_parcelas.cget("text") + " "
            usuario = getlogin()

            # inserindo dados da unidade no documento
            element.append(Spacer(10, 80))
            funcoes.inserir_elementos(element, style, "Vendedor(a): ", usuario.replace("."," "))
            funcoes.inserir_elementos(element, style, "Cliente: ", dados_unidade.Cliente)
            funcoes.inserir_elementos(element, style, "Empreendimento: ", dados_unidade.Empreendimento)
            funcoes.inserir_elementos(element, style, "Unidade: ", dados_unidade.Unidade)
            funcoes.inserir_elementos(element, style, "Renda do Cliente: ", funcoes.converter_real(renda))
            funcoes.inserir_elementos(element, style, "Capacidade de Pagto do Cliente: ", funcoes.converter_real(
                float(valor_capacidade)))
            funcoes.inserir_elementos(element, style, "Valor Financiado: ", dados_unidade.Financiamento)
            funcoes.inserir_elementos(element, style, "Porgentagem do Financiado: ", dados_unidade.Percen_finan)
            funcoes.inserir_elementos(element, style, "Valor FGTS: ", dados_unidade.FGTS)
            funcoes.inserir_elementos(element, style, "Valor Subsidio: ", dados_unidade.Subsidio)
            funcoes.inserir_elementos(element, style, "FGTS + Finan + Subsidio: ", dados_unidade.Financiamento_total)
            funcoes.inserir_elementos(element, style, "Valor de Avaliação: ", dados_unidade.Valor_Avaliacao)
            funcoes.inserir_elementos(element, style, "Valor com Desconto: ", dados_unidade.Valor_Desconto)
            funcoes.inserir_elementos(element, style, "Desconto Solicitado: ", dados_unidade.Desconto_solicitado)
            funcoes.inserir_elementos(element, style, "Porcentagem do Desconto Solicitado: ", dados_unidade.Percen_desconto)
            funcoes.inserir_elementos(element, style, "Pro Soluto: ", funcoes.converter_real(valor_pro_soluto))
            funcoes.inserir_elementos(element, style, "Porcentagem do Pro Soluto: ", dados_unidade.Percen_pro_soluto)
            funcoes.inserir_elementos(element, style, "Data de Entrega: ", dados_unidade.Data_Entrega)
            
            element.append(Spacer(1, 12))  # Adiciona um espaço entre a tabela e o título
            funcoes.inserir_elementos(element, STYLE_TITULO_TABELA, "Tabela Padrão", "")# titulo da tabela
            element.append(Spacer(1, 12)) 
            #Tabelas da tabela padrão e CEF
            t1.setStyle(GRID_STYLE)
            element.append(t1)
            element.append(Spacer(1, 12))
            element.append(d)
            element.append(Spacer(1, 12))

            if tipo == "linear":

                element.append(Spacer(1, 12))  # Adiciona um espaço entre a tabela e o título
                funcoes.inserir_elementos(element, STYLE_TITULO_TABELA, "Tabela Linear", "")# titulo da tabela
                #Tabelas da tabela linear e CEF

                element.append(Spacer(1, 12))
                t2.setStyle(GRID_STYLE2)
                element.append(t2)
                element.append(Spacer(1, 12))
                element.append(d)
                element.append(Spacer(1, 12))
                funcoes.inserir_elementos(element, style, falta_text, entry_falta_pagar.get())
                element.append(Spacer(1, 12))
                funcoes.inserir_elementos(element, style, soma_text, entry_soma_parcelas.get())
                element.append(Spacer(1, 12))
            # Texto Exclusivo para o Jurídico
            texto_jurídico = '''
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
                            irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.***'''

            texto_jurídico_2 = '''
                            ***Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
                            irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.***'''

            element.append(Spacer(1, 12))
            funcoes.inserir_elementos(element, style, "\n\n***ESTE TEXTO É RESERVADO PARA O TEXTO DO JURÍDICO: \n\n",
                                    texto_jurídico)

            element.append(Spacer(1, 12))
            funcoes.inserir_elementos(element, style, " ", texto_jurídico_2)

            # FAZENDO DOWNLOAD DO PDF PARA A PASTA DE DOWNLOAD DO USUÁRIO

            # Definindo o caminho da pasta de Downloads e o nome do arquivo
            download_path = path.join(path.expanduser('~'), 'Downloads')

            # definindo nome do arquivo como data e hora atual
            nome_arquivo = str(datetime.datetime.now().strftime("%Y_%b_%d__%H_%M_%S")) + ".pdf"
            pdf_path = path.join(download_path, nome_arquivo)

            # Criar documento com a Imagem de fundo
            doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=3 * cm,
                                    leftMargin=6.5 * cm, topMargin=2 * cm, bottomMargin=0,
                                    title="Relatório")
            

            # Carregar a imagem de fundo
            background_image = path.join(base_path,"logo_vivaz.png") 

            # Criar um template com uma imagem de fundo
            page_template = PageTemplate(id='background', frames=Frame(0, 0, A4[0], A4[1], id='normal'),
                                        onPage=lambda canvas, doc: canvas.drawImage(background_image, -10, 760, width=190, height=90))

            # Adicionar o template a todas as páginas do documento
            doc.addPageTemplates([page_template])

            # Construindo o documento PDF
            doc.build(element)

            # Exibindo mensagem de confirmação
            CTkMessagebox(title="PDF Gerado", message="Relatório em PDF gerado com sucesso na pasta de Downloads.",
                        icon="check", fg_color="#2F2F2F", text_color="#FFFFFF", title_color="#FFFFFF")

            # Abrindo o arquivo PDF
            system(f'start {pdf_path}')

            dados = {
            "Usuario": usuario,
            "Tipo": tipo,
            "Data": datetime.datetime.now().strftime("%d/%m/%Y"),
            "Enquadramento": str(dados_unidade.Enquadramento),
            "Empreendimento": str(dados_unidade.Empreendimento)
            }
    
            post("https://automacoesperform5-default-rtdb.firebaseio.com/SimuladorParcelas/Dados/.json",json=dados)
        except Exception as e:
            CTkMessagebox(title="ERRO", message=f"PDF não foi gerado por erro: {e}",
                        icon="cancel", fg_color="#2F2F2F", text_color="#FFFFFF", title_color="#FFFFFF")
            enviar_erro_firebase("gerar_pdf",e)
    # Botão para adicionar parcelas
    botao_adicionar = ctk.CTkButton( frame1_tabela_linear, text="Adicionar", command=adicionar_parcela, corner_radius=10,
                    font=("arial bold", 13),bg_color="#2F2F2F", fg_color="#1E2", hover_color="#2F2",width=120, height=30)
    botao_adicionar.place(x=360, y=380)

    # Botão para limpar dados
    botao_limpar = ctk.CTkButton(telaInicial, text="Limpar Dados", command=limpar_dados, corner_radius=10,
                        font=("arial bold", 13),bg_color=dark, fg_color="#ff7000", hover_color="#ff0000", width=120, height=30)
    
    # Botão para Voltar utilizada dando para tabela Padrão e para Linear
    button_voltar = ctk.CTkButton(telaInicial, text="Voltar", bg_color=dark, fg_color="red",
                            font=("arial bold", 13), text_color="#ffffff", corner_radius=10,  
                            hover_color="#bb0000", width=120, height=30, 
                            command=lambda: funcoes.voltar(parent, telaInicial))

    #Botão Gerar pdf
    button_gera_pdf = ctk.CTkButton(telaInicial, text="Gerar PDF", bg_color=dark, fg_color="blue", state=ctk.DISABLED,
                                font=("arial bold", 13), text_color="#ffffff", corner_radius= 10,  
                                hover_color="#0066aa", width=120, height=30, command=lambda t="linear": gerar_pdf(t))

    #Botão Nova Proposta
    button_nova_proposta = ctk.CTkButton(telaInicial, text="Nova Proposta", bg_color=dark, fg_color="#ffffff",
                                font=("arial bold", 13), text_color="#000000", corner_radius= 10,  
                                hover_color="gray", width=120, height=30, 
                                command = lambda: funcoes.voltar_tela_inicio(grandparent,parent, telaInicial))

    # Vinculando o evento de mudança de aba
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
    
    parcelas_anuais()
    parcelas_iniciais_padrao()
    valoresparcelaCEF()
    adicionar_parcela_padrao()
    parcelas_iniciais()

    # Inicialização da tela
    telaInicial.mainloop()