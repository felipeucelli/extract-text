# -*- coding: utf-8 -*-

# @autor: Felipe Ucelli
# @github: github.com/felipeucelli

# Built-in
import tkinter
from tkinter import filedialog
import _thread

import easyocr
import fitz


class Interface:
    def __init__(self):
        # Basic tkinter interface settings
        self.root = tkinter.Tk()
        self.root.title('Extract Text')
        self.root.resizable(width=False, height=False)

        self.file_path = ''

        self.canvas = tkinter.Canvas(self.root, width=300, height=250)
        self.canvas.pack()

        self.label_file = tkinter.Label(self.root, font='Arial 15')
        self.canvas.create_window(150, 60, window=self.label_file)

        self.label_status = tkinter.Label(self.root, font='Arial 15', fg='green')
        self.canvas.create_window(150, 230, window=self.label_status)

        self.get_file = tkinter.Button(text='    Import File    ', font='Arial 15', command=self._get_file_path)
        self.canvas.create_window(150, 130, window=self.get_file)

        self.extract_file = tkinter.Button(self.root, text='    Extract File    ', font='Arial 15',
                                           command=self._extract)
        self.canvas.create_window(150, 180, window=self.extract_file)

        self.extract_file.configure(state=tkinter.DISABLED)

    def _get_file_path(self):
        """
        Get the directory of the file to be extracted
        :return: File directory
        """
        self.file_path = filedialog.askopenfilename(filetypes=(('PDF Files', '*.pdf'),
                                                               ('Image Files', '*.jpg *.jpeg *.png')))
        if self.file_path != '':
            self.label_file['text'] = 'File: ' + self.file_path.split('/')[len(self.file_path.split('/')) - 1]
            self.extract_file.configure(state=tkinter.ACTIVE)
        else:
            self.label_file['text'] = ''
            self.extract_file.configure(state=tkinter.DISABLED)

    def _save_file(self, extracted_file):
        """
        Save the extracted file in the selected directory
        :param extracted_file:
        :return:
        """
        file_name = self.file_path.split('/')[len(self.file_path.split('/')) - 1]
        file_extension = file_name.split('.')[len(file_name.split('.')) - 1]
        new_file_name = file_name.replace(f'.{file_extension}', '')
        save_file_path = filedialog.asksaveasfilename(defaultextension='txt',
                                                      initialfile=new_file_name,
                                                      filetypes=(('Text files', '*.txt'), ('All files', '*.*')))

        if save_file_path != '':
            with open(save_file_path, 'w') as save:
                save.writelines(extracted_file)

    def _disable_btn(self):
        """
        Disables the import file and extract file buttons and writes a message to the screen during extraction
        :return:
        """
        self.get_file.configure(state=tkinter.DISABLED)
        self.extract_file.configure(state=tkinter.DISABLED)
        self.label_status['text'] = 'Extracting, please wait.'

    def _enable_btn(self):
        """
        Activates the import file and extract file buttons and clears the message after extraction
        :return:
        """
        self.get_file.configure(state=tkinter.ACTIVE)
        self.extract_file.configure(state=tkinter.ACTIVE)
        self.label_status['text'] = ''

    def _thread_pdf(self, *args):
        """
        Extract .pdf files
        :param args: Receive the file to be extracted
        :return:
        """
        self._disable_btn()
        with fitz.open(args[0]) as pdf:
            text = ''
            for page in pdf:
                text += page.getText()
        self.label_status['text'] = 'Extraction Finished.'
        self._save_file(text)
        self._enable_btn()

    def _thread_image(self, *args):
        """
        Extract image files
        :param args: Receive the file to be extracted
        :return:
        """
        self._disable_btn()
        reader = easyocr.Reader(['pt'], verbose=False)
        result_file = reader.readtext(args[0], paragraph=False)
        text = ''
        for result in result_file:
            text += f'{result[1]}\n'
        self.label_status['text'] = 'Extraction Finished.'
        self._save_file(text)
        self._enable_btn()

    def _extract_pdf(self, pdf_file):
        """
        Start a new thread for extracting .pdf files
        :param pdf_file: Receive the file to be extracted
        :return:
        """
        _thread.start_new_thread(self._thread_pdf, (pdf_file, 0))

    def _extract_image(self, image_file):
        """
        Starts a new thread for extracting image files
        :param image_file: Receive the file to be extracted
        :return:
        """
        _thread.start_new_thread(self._thread_image, (image_file, 0))

    def _extract(self):
        """
        Valid and call the function matches the format of the file to be extracted
        :return:
        """
        if self.file_path != '':
            file = self.file_path.split('/')[len(self.file_path.split('/')) - 1]
            file_extension = file.split('.')[len(file.split('.')) - 1]
            if file_extension == 'pdf':
                self._extract_pdf(self.file_path)
            if file_extension == 'jpg' or file_extension == 'jpeg' or file_extension == 'png':
                self._extract_image(self.file_path)

    def start(self):
        """
        Start tkinter interface
        :return:
        """
        self.root.mainloop()
