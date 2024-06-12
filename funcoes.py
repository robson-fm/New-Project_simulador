from customtkinter import DISABLED, NORMAL, CTkEntry
from pandas import to_datetime
from pathlib import Path
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from reportlab.platypus import Paragraph
from tkinter import NO

dark = "#242424"

#funções base
#função para deixar valor em formato real
def converter_real(valor):
    valor_em_real = f"R$ {valor:,.2f}"
    valor_em_real = valor_em_real.replace(".","*")
    valor_em_real = valor_em_real.replace(",",".")
    valor_em_real = valor_em_real.replace("*",",")

    return valor_em_real

def converter_valor_numerico(valor):
    valor_numerico = valor
    valor_numerico = valor_numerico.replace(".","*")
    valor_numerico = valor_numerico.replace(",",".")
    valor_numerico = valor_numerico.replace("*",",")

    return valor_numerico

#função para pegar a ultima parte do texto substituindo uma parte e eviando o texto em maiusculo
def caminho_em_string_maiuscula(texto):
    novo_texto = Path(texto).stem
    novo_texto = novo_texto.replace("_"," ")

    return novo_texto.upper()

#funções ctk
#função para configurar entry pre desabilitada
def configurar_entry(entry, texto):
    entry.configure(state=NORMAL)
    entry.delete(0, "end")
    entry.insert(0,texto)
    entry.configure(state=DISABLED)

#função para configurar a coluna da treeview
def configurar_treeview(treeview,coluna,tamanho):
    treeview.column(coluna,minwidth=0,width=tamanho,anchor="center",stretch=NO)
    treeview.heading(coluna, text=coluna)

#funções parcelas
#função para criar parcelas novas
def parcelas_Novas(y,frame):
    novaparcelas = CTkEntry(frame, bg_color="#2F2F2f",fg_color="#ffffff",text_color="#000000", placeholder_text="Qtd", width=60, height=10)
    novaparcelas.place(x=70, y=y)

    novavalor_da_parcela = CTkEntry(frame, bg_color="#2F2F2f",fg_color="#ffffff",text_color="#000000", height=10, width=110, placeholder_text="R$")
    novavalor_da_parcela.place(x=160, y=y)

    novadesc_da_parcela = CTkEntry(frame, bg_color="#2F2F2f",fg_color="#ffffff",text_color="#000000", height=10, width=110)
    novadesc_da_parcela.insert(0,"Mensal")
    novadesc_da_parcela.configure(state=DISABLED)
    novadesc_da_parcela.place(x=300, y=y)

    return novaparcelas, novavalor_da_parcela, novadesc_da_parcela

#função para pegar os valores dos campos de parcelas antigos e desabilitar eles
def parcelas_Anteriores(qtdParcelas,valoresParcelas,descParcelas):
    qtdparcelaAnterior = qtdParcelas[-1]
    parcelaAnterior = valoresParcelas[-1]
    descparcelaAnterior = descParcelas[-1]
    
    numeroParcelas = int(qtdparcelaAnterior.get())
    valorParcelas = float(converter_valor_numerico(parcelaAnterior.get()))
    desc_Parcelas = str(descparcelaAnterior.get())

    qtdparcelaAnterior.configure(state=DISABLED,text_color="#ffffff", fg_color="#2F2F2F")
    parcelaAnterior.configure(state=DISABLED,text_color="#ffffff", fg_color="#2F2F2F")
    descparcelaAnterior.configure(state=DISABLED,text_color="#ffffff", fg_color="#2F2F2F")

    return numeroParcelas,valorParcelas,desc_Parcelas

def converter_ordem(descricao):
    ordem = {'ato':1,'parcela 30 dias':2,'parcela 60 dias':3,'mensal':4, 
             'adimplência premiada':5,'periodicidade':6,'anual':7, 'parcela bônus':8}

    for ordem_str, ordem_num in ordem.items():
         if ordem_str in descricao.lower():
             return ordem_num


#função para ordenar coluna
def treeview_ordenar_coluna(tv, col, reverse):
    if col == 'Data':
        l = [(tv.set(k, col), k) for k in tv.get_children('')]

        #ordena coluna com base no padrão de data
        l = sorted(l,reverse=reverse, key=lambda x: to_datetime(BRparaEN(x[0]), format='%b/%Y'))
    elif col == "Descrição":
        l = [(converter_ordem(tv.set(k, col)), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
    else:
        l = [(tv.set(k, col), k) for k in tv.get_children('')] 

        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

#Função voltar

def voltar(telaAnterior, telaAtual):
    # Exibe a caixa de diálogo de confirmação
    msg = CTkMessagebox(title="ALERTA", message="Essa ação vai apagar o progresso feito, tem certeza?",
                          icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF",
                          option_1="Não", option_2="Sim")
    resposta = msg.get()
    # Se o usuário clicar em 'Sim', continue com a operação de voltar
    if resposta == "Sim":
        telaAnterior.deiconify()  # Restaura a tela anterior
        telaAtual.destroy()  # Fecha a tela atual
        
def voltar_tela_inicio(primeiraTela,telaAnterior, telaAtual):
    # Exibe a caixa de diálogo de confirmação
    msg = CTkMessagebox(title="ALERTA", message="Essa ação vai apagar o progresso feito, tem certeza?",
                          icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF",
                          option_1="Não", option_2="Sim")
    resposta = msg.get()
    # Se o usuário clicar em 'Sim', continue com a operação de voltar

    if resposta == "Sim":
        primeiraTela.deiconify()  # Restaura a tela inicial
        telaAnterior.destroy()  # Fecha a tela anterior
        telaAtual.destroy()  # Fecha a tela atual

def fechar_main(telaInicial):
    telaInicial.destroy()

# classe para guardar as informações da unidade
class Unidade:
    def __init__(self,Empreendimento,Unidade,Valor_Desconto,Valor_Avaliacao,Financiamento, FGTS, Subsidio,
                 Financiamento_total,Desconto_solicitado,Data_Entrega, Data_Lancamento,Qtd_divi_parcelas,
                 Qtd_percen_parcelas,Percen_anual,Percen_peri,Check_adimplencia, Cliente, Enquadramento,
                 Percen_pro_soluto,Percen_finan, Percen_desconto):
        self.Empreendimento = Empreendimento
        self.Unidade = Unidade
        self.Valor_Desconto = Valor_Desconto
        self.Valor_Avaliacao = Valor_Avaliacao
        self.Financiamento = Financiamento
        self.FGTS = FGTS
        self.Subsidio = Subsidio
        self.Financiamento_total = Financiamento_total
        self.Desconto_solicitado = Desconto_solicitado
        self.Data_Entrega = Data_Entrega.strftime('%b/%Y')
        self.Data_Lancamento = Data_Lancamento.strftime('%b/%Y')
        self.Qtd_divi_parcelas = Qtd_divi_parcelas
        self.Qtd_percen_parcelas = Qtd_percen_parcelas
        self.Percen_anual = Percen_anual
        self.Percen_peri = Percen_peri
        self.Check_adimplencia = Check_adimplencia
        self.Cliente = Cliente
        self.Enquadramento = Enquadramento
        self.Percen_pro_soluto = Percen_pro_soluto
        self.Percen_finan = Percen_finan
        self.Percen_desconto = Percen_desconto

# função para criar paragrafo para o pdf
def inserir_elementos(self,style,texto,info):
    valor = texto + info
    p_valor = Paragraph(valor,style)
    self.append(p_valor)

# função que compara as datas
def comparar_data(dataparcela,dataentrega,descricao):
    dataparcela = datetime.strptime(BRparaEN(dataparcela),'%b/%Y')
    dataentrega = datetime.strptime(BRparaEN(dataentrega),'%b/%Y')

    if descricao == "Anual":
        if dataparcela >= dataentrega:
            return True
    elif descricao == "Mensal":
        if dataparcela > dataentrega:
            return True
    return False

def BRparaEN(texto):
        lista_EN = {1: 'Jan', 2: 'Feb', 3: 'Mar',  4: 'Apr',  5: 'May',  6: 'Jun',
              7: 'Jul',  8: 'Aug',  9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        lista_BR = {1: 'Jan',  2: 'Fev',  3: 'Mar',  4: 'Abr',  5: 'Mai',  6: 'Jun',
              7: 'Jul',  8: 'Ago',  9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        for mesnum, mes in lista_BR.items():
            if mes in texto:
                texto_subs = texto.replace(mes,lista_EN[mesnum])
                return texto_subs
        return texto

# função para definir a tag da parcela colocada
def treeview_tag(renda,valor_parcela,descricao):
    renda = float(renda)
    porcentagem_aviso = 30/100 * renda
    porcentagem_limite = 40/100 * renda
    if descricao != "Anual":
        if valor_parcela > porcentagem_limite:
            return "limite"
        elif valor_parcela > porcentagem_aviso:
            return "aviso"
    return "ok"
    
