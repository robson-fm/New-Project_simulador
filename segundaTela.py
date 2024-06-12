import customtkinter as ctk
import funcoes
from terceiraTela import terceiraTela
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PIL import Image
from os import path

valor_prosoluto = 0
valor_parcela_bonus = 0

def segundaTela(parent,base_path,icone,valor_unidade,valor_unidade_desconto, renda_familiar,dados_unidade, StringVar_credito):
    global ato, valor_prosoluto,valor_parcela_bonus,anual, desconto_solicitado, valor_adim_premiada
    dark = "#242424"
    #configuração da tela
    segundaTela = ctk.CTkToplevel(parent)
    parent.withdraw()
    segundaTela.geometry = ("1200x600")
    segundaTela.title("Simulador")
    segundaTela.after(250, lambda: segundaTela.iconbitmap(icone))
    segundaTela.config(background=dark)
    segundaTela.resizable(width=False, height=False)

    def on_closing():
        parent.destroy()

    segundaTela.protocol("WM_DELETE_WINDOW", on_closing)
    ato = 0
    anual = 0
    porcetagem_pro_soluto = 0.15
    valor_adim_premiada = 0

    check_var = ctk.StringVar(value="off")
    def habilitar():
    #caixa_selecao.toggle()
        if check_var.get() == "on":
            entry_valor_anual.configure(state=ctk.NORMAL, fg_color="#ffffff", text_color="black")
            entry_valor_anual.focus()
        else:
            entry_valor_anual.configure(state=ctk.DISABLED, fg_color= "#2F2F2F", text_color="#ffffff")
            StringVar_anual.set(0)

    def tooltip_entry(entry, mensagem):
        tooltip_entry = CTkToolTip(entry, delay=0.2, border_width=1, border_color= "#34C7C8", message = mensagem)

    # Título central da tela
    titulo_label = ctk.CTkLabel(segundaTela, text="Informe os Valores", fg_color=dark, 
                                font=("arial bold", 30), text_color="#ffffff")
    titulo_label.pack(pady=20, padx=5)

    #Frame do centro da tela
    frameCentral = ctk.CTkFrame(segundaTela, fg_color="#2F2F2F", bg_color=dark,
                        border_width=0, corner_radius=30,  width=900, height=425)
    frameCentral.pack(pady=20, padx= 60)

    #Nome Completo
    label_nome = ctk.CTkLabel(frameCentral, text="Nome do Comprador*",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_nome.place(x= 35, y=30)

    entry_nome = ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_nome.place(x= 35, y=60)

    #Renda Familiar (Renda Bruta)
    StringVar_valor_renda_familiar = ctk.StringVar(value=funcoes.converter_real(renda_familiar))

    label_renda_familiar = ctk.CTkLabel(frameCentral, text="Renda Familiar (Renda Bruta)",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_renda_familiar.place(x= 253, y=30)

    entry_renda_familiar = ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", text_color="#ffffff",fg_color="#2F2F2F",
                                         textvariable=StringVar_valor_renda_familiar, font=("arial bold", 15),
                                         width=190, state=ctk.DISABLED)
    entry_renda_familiar.place(x= 253, y=60)

    #Valor Capacidade Pagto Mensal
    label_valor_capacidade = ctk.CTkLabel(frameCentral, text="Valor Capac. Pagto Mensal*",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_valor_capacidade.place(x= 471, y=30)

    entry_valor_capacidade = ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_valor_capacidade.place(x= 471, y=60)

    #Ato
    label_ato = ctk.CTkLabel(frameCentral, text="Ato*",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_ato.place(x= 35, y=270)

    entry_ato = ctk.CTkEntry(frameCentral, bg_color= "#2f2f2f", fg_color="#ffffff", text_color="black", width=190)
    entry_ato.place(x= 35, y=300)

    delta = relativedelta(datetime.now(),datetime.strptime(dados_unidade.Data_Lancamento,'%b/%Y'))

    if delta.months < 2 and delta.months >= 0:
        label_ato30 = ctk.CTkLabel(frameCentral, text="Parcela 30 Dias*",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
        label_ato30.place(x= 253, y=270)

        entry_ato30 = ctk.CTkEntry(frameCentral, bg_color= "#2f2f2f", fg_color="#ffffff", text_color="black", width=190)
        entry_ato30.place(x= 253, y=300)
        
        if delta.months == 0:
            label_ato60 = ctk.CTkLabel(frameCentral, text="Parcela 60 Dias*",fg_color="#2F2F2F", 
                                        font=("arial bold", 15), text_color="#ffffff")
            label_ato60.place(x= 471, y=270)

            entry_ato60 = ctk.CTkEntry(frameCentral, bg_color= "#2f2f2f", fg_color="#ffffff", text_color="black", width=190)
            entry_ato60.place(x= 471, y=300)

    tooltip_entry(entry_ato, "Mínimo de Ato: R$ 500,00")
    

    if StringVar_credito.get() == "MCMV":
        porcentagem_financiamento = 0.8
    elif StringVar_credito.get() == "SBPE / PRICE":
         porcentagem_financiamento = 0.8    
    elif StringVar_credito.get() == "SBPE / SAC":
        porcentagem_financiamento = 0.9

    #ENTRADA DE DADOS label e entry Segunda linha
    limite_financiamento = valor_unidade * porcentagem_financiamento
    #Total Financiado
    label_total_financiado = ctk.CTkLabel(frameCentral, text="Total Financiado",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_total_financiado.place(x= 35, y=110)

    entry_total_financiado = ctk.CTkEntry(frameCentral, placeholder_text=funcoes.converter_real(limite_financiamento),
                                          bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_total_financiado.place(x= 35, y=140)

    tooltip_financiamento = CTkToolTip(entry_total_financiado, delay=0.2,  border_width=1, border_color= "#34C7C8", justify='left', message = f"Porcentagem atual: 0%\nPorcentagem máxima: {porcentagem_financiamento*100}%\nMáximo de financiamento: {funcoes.converter_real(limite_financiamento)}")

    #Valor FGTS
    label_valor_fgts = ctk.CTkLabel(frameCentral, text="Valor FGTS",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_valor_fgts.place(x= 253, y=110)

    entry_valor_fgts = ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_valor_fgts.place(x= 253, y=140)

    #Subsidio(desconto)
    label_subsidio = ctk.CTkLabel(frameCentral, text="Subsidio (Desconto)",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_subsidio.place(x= 471, y=110)

    entry_subsidio= ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_subsidio.place(x= 471, y=140)

    #Desconto solicitado
    label_desconto_solicitado = ctk.CTkLabel(frameCentral, text="Desconto Solicitado",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_desconto_solicitado.place(x= 471, y=190)

    entry_desconto_solicitado = ctk.CTkEntry(frameCentral, bg_color= "#2F2F2F", fg_color="#ffffff", text_color="black", width=190)
    entry_desconto_solicitado.place(x= 471, y=220)

    tooltip_desconto = CTkToolTip(entry_desconto_solicitado, delay=0.2, border_width=1, border_color= "#34C7C8", justify='left', message = f"Porcentagem Atual: 0%\nPorcentagem máxima: 3%\nValor máximo de desconto: {funcoes.converter_real(valor_unidade_desconto * 0.03)}")

    #SAÍDA DE DADOS label e entry Terceira linha
    StringVar_valor_avaliacao = ctk.StringVar(value=funcoes.converter_real(valor_unidade))

    #Valor da Avaliação
    label_valor_avaliacao= ctk.CTkLabel(frameCentral, text="Valor da Avaliação",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_valor_avaliacao.place(x= 35, y=190)

    entry_valor_avaliacao = ctk.CTkEntry(frameCentral, textvariable=StringVar_valor_avaliacao, bg_color= "#2F2F2F",  
                                         fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_valor_avaliacao.place(x= 35, y=220)


    StringVar_valor_com_desconto = ctk.StringVar(value=funcoes.converter_real(valor_unidade_desconto))
    #Total (Valor do Desconto)
    label_valor_desconto = ctk.CTkLabel(frameCentral, text="Valor de Compra e Venda",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_valor_desconto.place(x= 253, y=190)

    entry_valor_desconto = ctk.CTkEntry(frameCentral, textvariable=StringVar_valor_com_desconto, bg_color= "#2F2F2F",  
                                        fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_valor_desconto.place(x= 253, y=220)

    StringVar_financiamento = ctk.StringVar(value=funcoes.converter_real(0))

    #Valor total Financiamento
    label_valor_financiamento = ctk.CTkLabel(frameCentral, text="Valor total Financiamento",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_valor_financiamento.place(x= 689, y=30)

    entry_valor_financiamento= ctk.CTkEntry(frameCentral, textvariable=StringVar_financiamento, bg_color= "#2F2F2F",  
                                            fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_valor_financiamento.place(x= 689, y=60)

    StringVar_prosoluto = ctk.StringVar(value=funcoes.converter_real(valor_unidade_desconto))

    #Pro Soluto
    label_prosoluto = ctk.CTkLabel(frameCentral, text="Pro Soluto",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_prosoluto.place(x= 689, y=190)

    entry_prosoluto= ctk.CTkEntry(frameCentral, textvariable=StringVar_prosoluto, bg_color= "#2F2F2F", 
                                  fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_prosoluto.place(x= 689, y=220)
    
    valor_prosoluto = valor_unidade_desconto
    limite_prosoluto = valor_unidade_desconto * porcetagem_pro_soluto
    Stringvar_limite_prosoluto = ctk.StringVar(value=funcoes.converter_real(limite_prosoluto))
    tooltip_prosoluto = CTkToolTip(entry_prosoluto, delay=0.2, border_width=1, border_color= "#34C7C8", justify='left', message = f"Porcentagem: {round((valor_prosoluto/valor_unidade_desconto)*100,2)}%\nPorcentagem máxima: 15%\nLimite do Pro Soluto: {Stringvar_limite_prosoluto.get()}")

    StringVar_adim_premiada = ctk.StringVar(value="")
    if dados_unidade.Check_adimplencia == "Sim":
        valor_adim_premiada = round(valor_unidade_desconto * 0.01,2)
        StringVar_adim_premiada.set(value=funcoes.converter_real(valor_adim_premiada))
        label_adimplecia = ctk.CTkLabel(frameCentral, text="Adimplencia Premiada",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
        label_adimplecia.place(x= 689, y=270)

        entry_adimplencia = ctk.CTkEntry(frameCentral, textvariable=StringVar_adim_premiada, bg_color= "#2F2F2F", 
                                    fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
        entry_adimplencia.place(x= 689, y=300)

        valor_prosoluto -= valor_adim_premiada

        StringVar_prosoluto.set(funcoes.converter_real(valor_prosoluto))


    #SAÍDA DE DADOS e botões Voltar/Avançar label e entry Quarta linha

    StringVar_parcela_bonus = ctk.StringVar(value=funcoes.converter_real(valor_unidade - valor_unidade_desconto))
    
    #Parcela Bonus
    label_parcela_bonus = ctk.CTkLabel(frameCentral, text="Parcela Bônus",fg_color="#2F2F2F", 
                                font=("arial bold", 15), text_color="#ffffff")
    label_parcela_bonus.place(x= 689, y=110)

    entry_parcela_bonus= ctk.CTkEntry(frameCentral, textvariable= StringVar_parcela_bonus, bg_color= "#2F2F2F", 
                                      fg_color="#2F2F2F", state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_parcela_bonus.place(x= 689, y=140)

    StringVar_anual = ctk.StringVar(value=0)
    check_anual = ctk.CTkCheckBox(frameCentral, text="Anual:",variable=check_var, onvalue="on", offvalue="off",command=habilitar, text_color="#ffffff")
    check_anual.place(x=35, y=380)

    entry_valor_anual = ctk.CTkEntry(frameCentral,textvariable=StringVar_anual,bg_color= "#2F2F2F", fg_color="#2F2F2F", 
                                     state=ctk.DISABLED, text_color="#ffffff", width=190)
    entry_valor_anual.place(x=110, y=380)

    limite_anual = round(renda_familiar * 0.8,-2)

    tooltip_entry(entry_valor_anual,f"Anual máxima: {funcoes.converter_real(limite_anual)}")

    
    def verifica_limites(financiamento,valor_a_pagar, lista_ato,lista_ato_entry,desconto_solicitado):
        global anual
        anual = float(funcoes.converter_valor_numerico(entry_valor_anual.get()))
        valor_capacidade = float(funcoes.converter_valor_numerico(entry_valor_capacidade.get()))
        nome_comprador = entry_nome.get()
        count_ato = 0
        porcentagem_financiamento_atual = round((financiamento/valor_unidade)*100,2)
        porcetagem_pro_soluto_atual = round((valor_prosoluto/valor_a_pagar)*100,2)
        porcentagem_desconto_solicitado = round((desconto_solicitado/(desconto_solicitado + valor_a_pagar))*100,2)
        check = True

        if nome_comprador == "":
            entry_nome.configure(border_color="red")
            check = False
        else:
            entry_nome.configure(border_color="#979DA2")

        if 0 > valor_capacidade:
            entry_valor_capacidade.configure(border_color="red")
            check = False
        else:
            entry_valor_capacidade.configure(border_color="#979DA2")

        if financiamento > limite_financiamento or financiamento < 0:
            entry_total_financiado.configure(border_color="red")
            check = False
        else:
            entry_total_financiado.configure(border_color="#979DA2")

        for ato in lista_ato:
            if 500 > ato:
                lista_ato_entry[count_ato].configure(border_color="red")
                check = False
            else:
                lista_ato_entry[count_ato].configure(border_color="#979DA2")
            count_ato += 1

        if porcentagem_desconto_solicitado > 3:
            entry_desconto_solicitado.configure(border_color="red")
            check = False
        else:
            entry_desconto_solicitado.configure(border_color="#979DA2")

        if porcetagem_pro_soluto_atual > porcetagem_pro_soluto*100 or valor_prosoluto < 0:
            entry_prosoluto.configure(border_color="red")
            check = False
        else:
            entry_prosoluto.configure(border_color="#979DA2")

        if anual > limite_anual:
            entry_valor_anual.configure(border_color="red")
            check = False
        else:
            entry_valor_anual.configure(border_color="#979DA2")

        limite_prosoluto = valor_a_pagar * porcetagem_pro_soluto
        Stringvar_limite_prosoluto = ctk.StringVar(value=funcoes.converter_real(limite_prosoluto))
        tooltip_financiamento.configure(message=f"Porcentagem atual: {porcentagem_financiamento_atual}%\nPorcentagem máxima: {porcentagem_financiamento*100}%\nMáximo de financiamento: {funcoes.converter_real(limite_financiamento)}")
        tooltip_desconto.configure(message=f"Porcentagem: {porcentagem_desconto_solicitado}%\nPorcentagem máxima: 3%\nValor máximo de desconto: {funcoes.converter_real(valor_unidade_desconto * 0.03)}")
        tooltip_prosoluto.configure(message= f"Porcentagem: {porcetagem_pro_soluto_atual}%\nPorcentagem máxima: 15%\nLimite do Pro Soluto: {Stringvar_limite_prosoluto.get()}")

        dados_unidade.Percen_finan = str(porcentagem_financiamento_atual) + "%"
        dados_unidade.Percen_pro_soluto = str(porcetagem_pro_soluto_atual)  + "%"
        dados_unidade.Percen_desconto = str(porcentagem_desconto_solicitado) + "%"

        return check

    # função pra campos serem iniciados com 0
    def valores_com_zero():
        entry_valor_capacidade.insert(0,0)
        entry_ato.insert(0,0)
        entry_total_financiado.insert(0,0)
        entry_valor_fgts.insert(0,0)
        entry_subsidio.insert(0,0)
        entry_desconto_solicitado.insert(0,0)

        if delta.months < 2 and delta.months >= 0:
            entry_ato30.insert(0,0)

            if delta.months == 0:
                entry_ato60.insert(0,0)

    #função para o botão verificar, realiza os calculos utilizando os valores prenchidos pelo usuario
    def verificar_valores():
        global valor_prosoluto,valor_parcela_bonus, desconto_solicitado,ato, valor_adim_premiada
        try:
            ato30 = 0
            ato60 = 0
            lista_ato = []
            lista_ato_entry = []
            ato = float(funcoes.converter_valor_numerico(entry_ato.get()))
            financiamento = float(funcoes.converter_valor_numerico(entry_total_financiado.get()))
            fgts= float(funcoes.converter_valor_numerico(entry_valor_fgts.get()))
            subsidio= float(funcoes.converter_valor_numerico(entry_subsidio.get()))
            desconto_solicitado= float(funcoes.converter_valor_numerico(entry_desconto_solicitado.get()))

            lista_ato.append(ato)
            lista_ato_entry.append(entry_ato)

            if delta.months < 2 and delta.months >= 0:
                ato30 = float(funcoes.converter_valor_numerico(entry_ato30.get()))
                lista_ato.append(ato30)
                lista_ato_entry.append(entry_ato30)

                if delta.months == 0:
                    ato60 = float(funcoes.converter_valor_numerico(entry_ato60.get()))
                    lista_ato.append(ato60)
                    lista_ato_entry.append(entry_ato60)
        
            valor_total_financiamento = financiamento + fgts + subsidio
            valor_a_pagar = valor_unidade_desconto - desconto_solicitado
            valor_parcela_bonus = valor_unidade - valor_a_pagar

            valores_a_subtrair = ato + ato30 + ato60 + valor_total_financiamento

            if valores_a_subtrair >= valor_a_pagar:
                valor_prosoluto = 0
                valor_adim_premiada = 0

            else:
                valor_prosoluto = valor_a_pagar - valores_a_subtrair
                
                if dados_unidade.Check_adimplencia == "Sim":
                    valor_adim_premiada = round(valor_a_pagar * 0.01,2)
                    valor_prosoluto -= valor_adim_premiada

            # atualizando campos para mostrar novos valores ao usuario
            StringVar_valor_com_desconto.set(funcoes.converter_real(valor_a_pagar))
            StringVar_financiamento.set(funcoes.converter_real(valor_total_financiamento))
            StringVar_prosoluto.set(funcoes.converter_real(valor_prosoluto))
            StringVar_adim_premiada.set(funcoes.converter_real(valor_adim_premiada))
            StringVar_parcela_bonus.set(funcoes.converter_real(valor_parcela_bonus))

            check = verifica_limites(financiamento, valor_a_pagar, lista_ato,lista_ato_entry, desconto_solicitado)
            #inserindo o total de financiamento como dado da unidade
            dados_unidade.Valor_Desconto = StringVar_valor_com_desconto.get()
            dados_unidade.Financiamento = funcoes.converter_real(financiamento)
            dados_unidade.FGTS = funcoes.converter_real(fgts)
            dados_unidade.Subsidio = funcoes.converter_real(subsidio)
            dados_unidade.Financiamento_total = StringVar_financiamento.get()
            dados_unidade.Desconto_solicitado = funcoes.converter_real(desconto_solicitado)
            dados_unidade.Cliente = entry_nome.get()

            if check == True:
                button_avancar.configure(state=ctk.NORMAL)
                terceiraTela(parent,segundaTela,base_path,icone,lista_ato,valor_prosoluto,entry_parcela_bonus.get(), 
                            renda_familiar,anual, funcoes.converter_valor_numerico(entry_valor_capacidade.get()),dados_unidade, valor_adim_premiada)
            else:
                CTkMessagebox(title="ALERTA", message="Preencha os valores corretamente",
                            icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF",
                            option_1="OK")
        except ValueError:
            CTkMessagebox(title="ALERTA", message="Por favor, insira valores validos",
                        icon="warning",fg_color="#2F2F2F",text_color="#FFFFFF",title_color="#FFFFFF") 
    valores_com_zero()

    #Botão Voltar 
    button_voltar = ctk.CTkButton(frameCentral, text="Voltar", bg_color="#2f2f2f", fg_color="red",
                                font=("arial bold", 13), text_color="#ffffff", corner_radius= 10,  
                                hover_color="#bb0000", width=120, height=30, command=lambda:funcoes.voltar(parent,segundaTela))
    button_voltar.place(x=640, y= 370)

    #Botão Avançar
    button_avancar = ctk.CTkButton(frameCentral, text="Avançar", bg_color="#2f2f2f",  fg_color="green", 
                                font=("arial bold", 13), text_color="#ffffff", corner_radius=10, 
                                hover_color="#1E2", width=120, height=30, #state=ctk.DISABLED,
                                command=verificar_valores)
    button_avancar.place(x=770, y= 370)

    segundaTela.mainloop()