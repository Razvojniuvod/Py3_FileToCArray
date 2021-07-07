#-------------------------------------------------------------------------------
# Name:         file_to_carray.py
# Purpose:      Providing a portable way to add a file to a C program.
#
# Author:       Razvojniuvod
#
# Created:      26.04.2020
# Copyright:    (c) Razvojniuvod 2020
# Licence:      MIT
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog as tkFileDialog
from tkinter.scrolledtext import ScrolledText as tkScrolledText
from tkinter import messagebox as tkMessageBox

from pathlib import Path

class C_Array_TextParser:
    def generateHeader(self, FILEPATH:str, DEFINED_HEADER:str="", VARIABLE_MODIFIER:str="", ARRAY_NAME:str="") -> str:
        """
        Loads the file defined in argument FILEPATH and generates a string
        representation of a C/C++ array with size parameter.
        The generated string is returned upon completion.
        """
        with open(FILEPATH, "rb") as file_pointer:
            CACHED_FILE = file_pointer.read()   #   Copy the content of the whole file.
            FILE_SIZE   = len(CACHED_FILE)      #   Get the size of the file in bytes.

        FILEPATH_PARENT  = Path(FILEPATH).parent   #   Input files absolute filepath, excluding the file and its extension itself.
        FILENAME         = Path(FILEPATH).stem     #   Input files name without its extension.
        FILE_EXTENSION   = Path(FILEPATH).suffix   #   Input files extension.

        ARRAY_NAME       = ARRAY_NAME if len(ARRAY_NAME) > 0 else FILENAME.replace(' ', '_').upper()
        if DEFINED_HEADER == "":
            DEFINED_HEADER = f"{ARRAY_NAME}_{FILE_EXTENSION.replace('.', '').upper()}_FILE"

        if VARIABLE_MODIFIER == "":
            CONSTANT_TYPE = "const unsigned char"
        else:
            CONSTANT_TYPE = f"const {VARIABLE_MODIFIER} unsigned char"

        GENERATED_HEADER_FILE_CODE = (
            f"#ifndef {DEFINED_HEADER}\n"
            f"#define {DEFINED_HEADER}\n"
            f"\n"
            f"// The array size is in bytes.\n"
            f"const {self.__autoDefine_C_Type(FILE_SIZE)} {ARRAY_NAME}_SIZE = {FILE_SIZE};\n"
            f"\n"
            f"{self.__generate_C_Array(ARRAY_NAME, CACHED_FILE, CONSTANT_TYPE)}\n"
            f"#endif"
        )

        return GENERATED_HEADER_FILE_CODE


    def __autoDefine_C_Type(self, VALUE:int, IS_SIGNED:bool = False) -> str:
        """
        Based on the minimum number of bits needed
        by a integer, decide what C data type would be
        suitable to use for that integers value.

        Supported C types:
            - signed char (8 bit, 1 byte)
            - unsigned char (8 bit, 1 byte)
            - signed short (16 bit, 2 byte)
            - unsigned short (16 bit, 2 byte)
            - signed long (32 bit, 4 byte)
            - unsigned long (32 bit, 4 byte)
            - signed long long (64 bit, 8 byte)
            - unsigned long long (64 bit, 8 byte)
        """
        BIT_LENGTH = VALUE.bit_length()
        c_type = "signed" if IS_SIGNED else "unsigned"

        if BIT_LENGTH <= 8:
            c_type += " char"
        elif BIT_LENGTH <= 16:
            c_type += " short"
        elif BIT_LENGTH <= 32:
            c_type += " long"
        elif BIT_LENGTH <= 64:
            c_type += " long long"
        else:
            raise ValueError(f"The value {VALUE} is to big to be set to any C type currently supported in this function!")

        return c_type

    def __generate_C_Array(self, NAME:str, ITERABLE, C_TYPE:str="int", ALTERNATIVE_LENGTH:str="", ELEMENTS_PER_ROW:int = 8) -> str:
        """
        Create a string representation of a one-dimensional C array.
        The elements are printed as decimals.

        If argument ALTERNATIVE_LENGTH (incase if you want to define the arrays size with a #define type of constant)
        is not used, get the length of the array-like object (list, tuple, bytes, ect...) and define
        with it the number of elements the C array will contain.
        """
        if ALTERNATIVE_LENGTH == "":
            c_array_string = f"{C_TYPE} {NAME}[{len(ITERABLE)}] = {{\n"
        else:
            c_array_string = f"{C_TYPE} {NAME}[{ALTERNATIVE_LENGTH}] = {{\n"

        elements_inserted = 0
        ARRAY_END = len(ITERABLE) - 1

        for element in ITERABLE:
            if elements_inserted == ARRAY_END:
                if (elements_inserted % ELEMENTS_PER_ROW) == 0:
                    c_array_string += f"\t0x{element:02X}\n"
                else:
                    c_array_string += f"0x{element:02X}\n"

            elif (elements_inserted % ELEMENTS_PER_ROW) == 0:
                c_array_string += f"\t0x{element:02X}, "
            elif (elements_inserted % ELEMENTS_PER_ROW) == ELEMENTS_PER_ROW - 1:
                c_array_string += f"0x{element:02X},\n"
            else:
                c_array_string += f"0x{element:02X}, "

            elements_inserted += 1

        c_array_string += "};"
        return c_array_string

class AutoCounter:
    def __init__(self, count_preset = 0, increment_by = 1):
        """
        Counter class, with which one can automate
        parts of code, which rely on incrementing
        sequences of values being input.
        """
        self.__count = count_preset
        self.__increment = increment_by

    def presetCount(self, count_preset):
        """
        Sets the count of this object to
        the value of count_preset and returns
        the previous count.
        """
        previous_count = self.__count
        self.__count = count_preset
        return previous_count

    def incrementCount(self):
        """
        Increments the count by the among
        set initially in this object.
        """
        current_count = self.__count
        self.__count += self.__increment
        return current_count

    def getCount(self):
        """
        Returns the current count of this object.
        """
        return self.__count



class tkDataEntry:
    def __init__(self, parent_frame, label = "DataEntry:", preset_text = "", on_row = 0, with_width = 30, with_padding = 5, sticks_to = tk.E):
        """
        Structure class for a selection of tkinter GUI widgets.

        This one combines a Label (first column) and Entry (second column)
        in a grid, based on the parent widget (Frame of Tk) for
        easier creation of having a known entry input, in which it is
        shown to the GUI user what type of data is expected.

        The Label is always on column 0, while the Entry is on column 1.
        """
        self.__data_label = tk.Label(parent_frame, text = label)
        self.__data_entry = tk.Entry(parent_frame, text = preset_text, width = with_width)
        self.__data_label.grid(row = on_row, column = 0, padx = with_padding, pady = with_padding, sticky = sticks_to)
        self.__data_entry.grid(row = on_row, column = 1, padx = with_padding, pady = with_padding, sticky = sticks_to)

    def getLabelText(self) -> str:
        """
        Returns the displayed text of the Label widget.
        """
        return self.__data_label["text"]

    def setEntryText(self, new_text=""):
        """
        Sets the text programmatically in the Entry widget.
        """
        self.__data_entry.delete(0, tk.END)
        self.__data_entry.insert(0, new_text)

    def getEntryText(self) -> str:
        """
        Returns the entered text in the Entry widget.
        """
        return self.__data_entry.get()

    def __str__(self):
        return (
            f"Label text: \"{self.__data_label['text']}\",\n"
            f"Entry text: \"{self.__data_entry.get()}\""
        )


class MainWindow(tk.Frame):
    def __init__(self, parent):
        """
        The GUI structure is defined in __init__.
        """
        super().__init__(parent)

        self.__code_preview_window = None
        self.__code_generator   = C_Array_TextParser()
        self.__row_counter      = AutoCounter()

        self.__input_filepath   = tkDataEntry(self, "Input filepath:", on_row = self.__row_counter.getCount())
        self.__browse_files     = tk.Button(self, text="Select file", bd = 4, command = self.__setInputFilepath)
        self.__browse_files.grid(row = self.__row_counter.incrementCount(), column = 3, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.__defined_header       = tkDataEntry(self, "Define header:", on_row = self.__row_counter.getCount())
        self.__preset_header_define = tk.Button(self, text="Preset header define", bd = 4, command = self.__presetHeaderDefine)
        self.__preset_header_define.grid(row = self.__row_counter.incrementCount(), column = 3, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.__array_name           = tkDataEntry(self, "C/C++ Array name:", on_row = self.__row_counter.getCount())
        self.__preset_array_name    = tk.Button(self, text="Preset array name", bd = 4, command = self.__presetArrayName)
        self.__preset_array_name.grid(row = self.__row_counter.incrementCount(), column = 3, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.__variable_modifier    = tkDataEntry(self, "Variable modifier:", on_row = self.__row_counter.getCount())
        self.__preview_code         = tk.Button(self, text="Preview generated code", bd = 4, command = self.__previewGeneratedCode)
        self.__preview_code.grid(row = self.__row_counter.incrementCount(), column = 3, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.__save_code = tk.Button(self, text="Generate code and save it", bd = 4, command = self.__generateAndSaveHeader)
        self.__save_code.grid(row = self.__row_counter.incrementCount(), columnspan = 4, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.pack()

    def __setInputFilepath(self):
        """
        Sets the filepath using a file dialog, or check a already entered
        absolute filepath if it was manually entered by the GUI user.

        TODO:
            Should display dialog box asking the GUI user whenever
            they want to check the current filename or overwrite it.

            Could also be done by dynamically checking what is being written in
            the entry box and trying to check if its a legal filepath.

            Might aswell just do two buttons with seperate functions (best choice).
        """


        input_filepath = tkFileDialog.askopenfilename(title="Select a file")
        self.__input_filepath.setEntryText(input_filepath)
        self.__presetHeaderDefine()
        self.__presetArrayName()

    def __presetHeaderDefine(self):
        """
        Sets the C macro name of the header,
        to prevent repeated loading of the header,
        in case it is included multiple times.

        The name is set based on the files name defined
        in the filepath of self.__defined_header with
        spaces being replaces by underscored, with the
        filename being included to the end. A additional
        underscore is added at the beginning.

        Example:
            File = example text.txt
            File name = example text
            File extension = txt

            Result = _EXAMPLE_TEXT_TXT_FILE
        """
        FILEPATH = self.__input_filepath.getEntryText()

        if len(FILEPATH) == 0:
            return

        FILENAME        = Path(FILEPATH).stem
        FILE_EXTENSION  = Path(FILEPATH).suffix
        HEADER_DEFINE   = f"_{FILENAME.replace(' ', '_').upper()}_{FILE_EXTENSION.replace('.', '').upper()}_FILE"

        self.__defined_header.setEntryText(HEADER_DEFINE)

    def __presetArrayName(self):
        """
        Sets the C arrays name of the header,
        which will contain the binary data of the defined file.

        The name is set based on the files name defined
        in the filepath of self.__defined_header with
        spaces being replaces by underscored.

        Example:
            File = example text.txt
            File name = example

            Result = EXAMPLE_TEXT
        """
        FILEPATH = self.__input_filepath.getEntryText()

        if len(FILEPATH) == 0:
            return

        FILENAME    = Path(FILEPATH).stem
        ARRAY_NAME  = FILENAME.replace(' ', '_').upper()

        self.__array_name.setEntryText(ARRAY_NAME)

    def __previewGeneratedCode(self):
        """
        Creates a dialog window containing a preview of
        the generated C/C++ header.

        If its already displayed, it will automatically close the
        current dialog window and open a new one.
        """
        try:
            generated_header_file = self.__code_generator.generateHeader(
                self.__input_filepath.getEntryText(),
                self.__defined_header.getEntryText(),
                self.__variable_modifier.getEntryText(),
                self.__array_name.getEntryText()
            )
        except OSError:
            tkMessageBox.showerror("Filepath invalid", (
                f"The entered filepath cannot be used due to being incorrectly entered, "
                f"file not existing or not having permission to read it.\n\n"
                f"To select a file using the file dialog, clear whatever is written in "
                f"the textbox of \"{self.__input_filepath.getLabelText()}\" and\n"
                f"click again on the button \"{self.__browse_files['text']}\"."
            ))
            return

        if self.__code_preview_window != None:
            self.__code_preview_window.destroy()

        self.__code_preview_window = tk.Toplevel()
        self.__code_preview_window.title("Generated code preview")
        self.__code_preview_window.protocol("WM_DELETE_WINDOW", self.__removeDialogWindow)

        text_field = tkScrolledText(self.__code_preview_window)
        text_field["font"] = ("arial", "12")

        text_field.insert(tk.END, generated_header_file)
        text_field.pack(expand = True, fill = tk.BOTH)

    def __removeDialogWindow(self):
        """
        Closes the code preview dialog window,
        and sets its variable to None to indicate,
        that there is no more dialog window shown
        to the GUI user.
        """
        self.__code_preview_window.destroy()
        self.__code_preview_window = None

    def __generateAndSaveHeader(self):
        """
        Creates a file dialog for where the header file
        should be save.

        First, the header files code is generated from the
        defined input filename. If errors occur while trying to
        open the file, display a error dialog and get out of the method.

        Once the code is generated, the GUI user is present with the option of
        where to save the file. By default, the file extension is
        .h, with different ones being selectable (currenty .txt and by users choice).
        """
        try:
            generated_header_file = self.__code_generator.generateHeader(
                self.__input_filepath.getEntryText(),
                self.__defined_header.getEntryText(),
                self.__variable_modifier.getEntryText(),
                self.__array_name.getEntryText()
            )
        except OSError:
            tkMessageBox.showerror("Filepath invalid", (
                f"The entered filepath cannot be used due to being incorrectly entered, "
                f"file not existing or not having permission to read it.\n\n"
                f"To select a file using the file dialog, clear whatever is written in "
                f"the textbox of \"{self.__input_filepath.getLabelText()}\" and\n"
                f"click again on the button \"{self.__browse_files['text']}\"."
            ))
            return

        FILEPATH = self.__input_filepath.getEntryText()
        FILENAME = Path(FILEPATH).stem

        destination = tkFileDialog.asksaveasfile(
            defaultextension = "*.h",
            filetypes = [
                ("Header file", "*.h"),
                ("Text file", "*.txt"),
                ("Any file", "*.*")
            ]
        )
        if destination == None:
            return

        destination.write(generated_header_file)
        destination.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File -> C/C++ array")
    root.resizable(False, False)

    MainWindow(root)

    root.mainloop()