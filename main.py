import tkinter
from tkinter import filedialog


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

root.mainloop()
