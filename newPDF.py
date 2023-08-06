import PyPDF2
import PySimpleGUI as sg


def menu():  # Janela 1
    sg.theme('Dark Blue 3')
    layout = [[sg.Text('Arquivos de entrada')],
              [sg.Input(), sg.FilesBrowse(key='-ENTRADA1-', file_types=(('Text Files', '*.pdf'),))],
              [sg.Text('Informe a partir de qual página deseja dividir o arquivo')],
              [sg.InputText(key='split_at_page')],
              [sg.Button('Dividir arquivos'), sg.Button('Cancelar')]]
    return sg.Window('Divisor de arquivos PDF', layout=layout, finalize=True,)


def sucesso():  # Janela 2
    sg.theme('DarkGreen')
    layout = [[sg.Text('Divisão realizada com sucesso !')],
              [sg.Button('Voltar'), sg.Button('Cancelar')]]
    return sg.Window('SUCESSO', layout=layout, size=(300, 100), finalize=True)

janela1, janela2 = menu(), None
while True:
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break
    if window == janela1 and event == 'Cancelar':
        break
    if window == janela2 and event == 'Voltar':
        janela2.close()
        janela1 = menu()
    if window == janela2 and event == 'Cancelar':
        break
    if window == janela2 and event == sg.WINDOW_CLOSED:
        break
    if window == janela1 and event == 'Dividir arquivos' and values['-ENTRADA1-'] != '' and values['split_at_page'] != '':
        lista = values['-ENTRADA1-'].split(';')
        split_at_page = int(values['split_at_page'])
        for x in lista:
            with open(x, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                output1 = PyPDF2.PdfWriter()
                output2 = PyPDF2.PdfWriter()
                for i in range(num_pages):
                    page = reader.pages[i]
                    if i < split_at_page:
                        output1.add_page(page)
                    else:
                        output2.add_page(page)
                with open(x + '-ILP.pdf', 'wb') as f:
                    output1.write(f)
                with open(x + '-BANCO.pdf', 'wb') as f:
                    output2.write(f)
            janela1.close()
            janela2 = sucesso()
