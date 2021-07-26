import tkinter
from tkinter import filedialog
import easyocr
import _thread
import fitz


def disable_btn():
    global get_file, extract_file
    get_file.configure(state=tkinter.DISABLED)
    extract_file.configure(state=tkinter.DISABLED)


def enable_btn():
    global get_file, extract_file
    get_file.configure(state=tkinter.ACTIVE)
    extract_file.configure(state=tkinter.ACTIVE)


def save_file(extracted_file):
    global file_path
    file_name = file_path.split('/')[len(file_path.split('/')) - 1]
    new_file_name = file_name.split('.')[0]
    save_file_path = filedialog.asksaveasfilename(defaultextension='txt',
                                                  initialfile=new_file_name,
                                                  filetypes=(('Text files', '*.txt'), ('All files', '*.*')))

    if save_file_path != '':
        with open(save_file_path, 'w') as save:
            save.writelines(extracted_file)
    else:
        pass


def thread_pdf(*args):
    disable_btn()
    with fitz.open(args[0]) as pdf:
        text = ''
        for page in pdf:
            text += page.getText()
    save_file(text)
    enable_btn()


def extract_pdf(pdf_file):
    _thread.start_new_thread(thread_pdf, (pdf_file, 0))


def thread_image(*args):
    disable_btn()
    reader = easyocr.Reader(['pt'], verbose=False)
    result_file = reader.readtext(args[0], paragraph=False)
    text = ''
    for result in result_file:
        text += f'{result[1]}\n'
    save_file(text)
    enable_btn()


def extract_image(image_file):
    _thread.start_new_thread(thread_image, (image_file, 0))


def extract():
    global file_path
    if file_path != '':
        file = file_path.split('/')[len(file_path.split('/')) - 1]
        if file.split('.')[1] == 'pdf':
            extract_pdf(file_path)
        if file.split('.')[1] == 'jpg' or file.split('.')[1] == 'png':
            extract_image(file_path)


def get_file_path():
    global file_path
    global label
    file_path = filedialog.askopenfilename(filetypes=(('PDF files', '*.pdf'),
                                                      ('Image files', '*.jpg *.png')))

    label['text'] = 'File: ' + file_path.split('/')[len(file_path.split('/')) - 1]


root = tkinter.Tk()
root.title('Extract Text')
root.resizable(width=False, height=False)
file_path = ''

canvas = tkinter.Canvas(root, width=300, height=250)
canvas.pack()

label = tkinter.Label(root, font='Arial 15')
canvas.create_window(150, 60, window=label)

get_file = tkinter.Button(text='    Import File    ', font='Arial 15', command=get_file_path)
canvas.create_window(150, 130, window=get_file)

extract_file = tkinter.Button(root, text='    Extract File    ', font='Arial 15', command=extract)
canvas.create_window(150, 180, window=extract_file)

root.mainloop()
