import tkinter
from tkinter import filedialog


def extract_pdf(pdf_file):
    import fitz

    with fitz.open(pdf_file) as pdf:
        texto = ''
        for pagina in pdf:
            texto += pagina.getText()

    print(texto)


def extract_image(image_file):
    import easyocr

    reader = easyocr.Reader(['pt'])

    resultados = reader.readtext(image_file, paragraph=False)

    for resultado in resultados:
        print(f'{resultado[1]}')


def extract():
    global file_path
    if file_path != '':
        file = file_path.split('/')[len(file_path.split('/')) - 1]

        if file.split('.')[1] == 'pdf':
            extract_pdf(file_path)
        if file.split('.')[1] == 'jpg':
            extract_image(file_path)


def get_file_path():
    global file_path
    global label
    file_path = filedialog.askopenfilename(filetypes=(('PDF files', '*.pdf'),
                                                      ('Image files', '*.jpg'),
                                                      ('All files', '*.*')))

    label['text'] = 'File: ' + file_path.split('/')[len(file_path.split('/')) - 1]


root = tkinter.Tk()
file_path = ''

canvas = tkinter.Canvas(root, width=300, height=250)
canvas.pack()

label = tkinter.Label(root, font='Arial 20')
canvas.create_window(150, 60, window=label)

get_file = tkinter.Button(text='    Import File    ', font='Arial 15', command=get_file_path)
canvas.create_window(150, 130, window=get_file)

extract_file = tkinter.Button(root, text='    Extract File    ', font='Arial 15', command=extract)
canvas.create_window(150, 180, window=extract_file)

root.mainloop()
