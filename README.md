# Py3_FileToCArray description
Providing a portable way to add a file to a C program, by generating a byte array from the needed file, so it can be simply included into the C source code.

Its as a GUI program, so if you have trouble using the terminal/command-line, this could provide you some relief.
It is very simple to use, and will auto-fill the needed text entries, once you selected your file.

Other then that, i hope my program proves helpful.

# What are the requirements for running your program?
The source code is coded in the programming language Python 3, so you will require its intepreter (support from Python 3.6 and onwards) to use this utility.
Also, you must have the newest version of the GUI library Tkinter installed.

# How do you run the program?
Simply double-click on it, and you should see the programs window popup.
If you want to run it from the terminal/command-line, just type
for Unix-line and similar "python3 file_to_carray.py",
or in Windows having the default installation of the intepreter "python file_to_carray.py" .

# How do i use it to create the C array from my file?
1.          Run the program.

1.          Enter the filepath of your file to the text entry of "Input filepath:" by 
            manually copying it to it, or just select it from the file explorer by
            clicking the button "Select file".

1.          If you require a different name for your include guard, change it
            by clicking on the text entry of "Define header", and modify its text.
            If you want the default name for the include guard, just leave it,
            or in the case of a mistake, clicking on the button "Preset header define" .
            
            If you require a different name for your generated C array, change it
            by clicking on the text entry of "C/C++ Array name:", and modify its text.
            If you want the default name for the C array, just leave it,
            or in the case of a mistake, clicking on the button "Preset array name" .          
            
            If you require a variable modifier to be used for your array and size constant,
            write it on the text entry of "Variable modifier".
            You will usually need to do this, if developing code for embedded systems,
            incase if your compiler of choice doesn't put the C array on 
            the flash memory of the microcontroller (like in the case of Atmel microcontrollers,
            for which the compiler required "PROGMEM" to be defined as a variable modifier).
                      
1.          Optionally preview the generated C array by clicking the button "Preview generated code", to
            see if everything is as it should be.
            
            If you done that or want to get to it, just click the button "Generate code and save it",
            and save your generated code to the folder, in which you will need it.
