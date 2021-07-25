import tkinter
from tkinter import filedialog
import easyocr
import _thread
import fitz


def thread_pdf(*args):
    with fitz.open(args[0]) as pdf:
        text = ''
        for page in pdf:
            text += page.getText()
    print(text)


def extract_pdf(pdf_file):
    _thread.start_new_thread(thread_pdf, (pdf_file, 0))


def thread_extract(*args):
    reader = easyocr.Reader(['pt'])
    result_file = reader.readtext(args[0], paragraph=False)
    for result in result_file:
        print(f'{result[1]}')


def extract_image(image_file):
    _thread.start_new_thread(thread_extract, (image_file, 0))


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
root.title('Extract Text')
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
