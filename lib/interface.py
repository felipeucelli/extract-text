import tkinter
from tkinter import filedialog
import easyocr
import _thread
import fitz


class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Extract Text')
        self.root.resizable(width=False, height=False)
        self.file_path = ''

        self.canvas = tkinter.Canvas(self.root, width=300, height=250)
        self.canvas.pack()

        self.label = tkinter.Label(self.root, font='Arial 15')
        self.canvas.create_window(150, 60, window=self.label)

        self.get_file = tkinter.Button(text='    Import File    ', font='Arial 15', command=self._get_file_path)
        self.canvas.create_window(150, 130, window=self.get_file)

        self.extract_file = tkinter.Button(self.root, text='    Extract File    ', font='Arial 15',
                                           command=self._extract)
        self.canvas.create_window(150, 180, window=self.extract_file)

    def _get_file_path(self):
        self.file_path = filedialog.askopenfilename(filetypes=(('PDF files', '*.pdf'),
                                                               ('Image files', '*.jpg *.png')))
        if self.file_path != '':
            self.label['text'] = 'File: ' + self.file_path.split('/')[len(self.file_path.split('/')) - 1]

    def _save_file(self, extracted_file):
        file_name = self.file_path.split('/')[len(self.file_path.split('/')) - 1]
        new_file_name = file_name.split('.')[0]
        save_file_path = filedialog.asksaveasfilename(defaultextension='txt',
                                                      initialfile=new_file_name,
                                                      filetypes=(('Text files', '*.txt'), ('All files', '*.*')))

        if save_file_path != '':
            with open(save_file_path, 'w') as save:
                save.writelines(extracted_file)

    def _disable_btn(self):
        self.get_file.configure(state=tkinter.DISABLED)
        self.extract_file.configure(state=tkinter.DISABLED)

    def _enable_btn(self):
        self.get_file.configure(state=tkinter.ACTIVE)
        self.extract_file.configure(state=tkinter.ACTIVE)

    def _thread_pdf(self, *args):
        self._disable_btn()
        with fitz.open(args[0]) as pdf:
            text = ''
            for page in pdf:
                text += page.getText()
        self._save_file(text)
        self._enable_btn()

    def _thread_image(self, *args):
        self._disable_btn()
        reader = easyocr.Reader(['pt'], verbose=False)
        result_file = reader.readtext(args[0], paragraph=False)
        text = ''
        for result in result_file:
            text += f'{result[1]}\n'
        self._save_file(text)
        self._enable_btn()

    def _extract_pdf(self, pdf_file):
        _thread.start_new_thread(self._thread_pdf, (pdf_file, 0))

    def _extract_image(self, image_file):
        _thread.start_new_thread(self._thread_image, (image_file, 0))

    def _extract(self):
        if self.file_path != '':
            file = self.file_path.split('/')[len(self.file_path.split('/')) - 1]
            if file.split('.')[1] == 'pdf':
                self._extract_pdf(self.file_path)
            if file.split('.')[1] == 'jpg' or file.split('.')[1] == 'png':
                self._extract_image(self.file_path)

    def start(self):
        self.root.mainloop()