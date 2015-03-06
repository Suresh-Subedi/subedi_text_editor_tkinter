#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
from tkinter import PhotoImage, messagebox, mainloop, Toplevel, Tk, Text, Menu, IntVar, StringVar, TclError, SEL_FIRST, SEL_LAST, SEL, INSERT, END, NONE, WORD, TOP, RAISED, SUNKEN, HORIZONTAL, E, W, N, S, X, BOTTOM, BOTH, LEFT
from tkinter.ttk import Entry, Frame, LabelFrame, Radiobutton, Scrollbar, Button, Label, Checkbutton, Combobox
from tkinter.filedialog import askopenfile

TITLE = "Subedi Text Editor"
top = Tk()
if "nt" == os.name:
    top.wm_iconbitmap(bitmap = "Notepad.ico") #top.wm_iconbitmap("Notepad.ico")
else:
    try:
        img = PhotoImage(file='notepad.gif')
        root.tk.call('wm', 'iconphoto', root._w, img)
    except:
        pass   
filename = None
key_word = ""

frame = Frame(top, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

# text widget
editor = Text(frame, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)
editor.focus_set()
editor.grid(row=0, column=0, sticky=N+S+E+W)
editor.config( wrap = WORD, # use word wrapping
               undo = True, # Tk 8.4 
               width = 64 )
xscrollbar.config(command=editor.xview)
yscrollbar.config(command=editor.yview)
class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
statusbar = StatusBar(frame)
statusbar.grid(row=2, column=1, columnspan=2, sticky=E+W)
frame.pack(side=BOTTOM, fill=BOTH, expand=1)

def set_title(local_filename = None):
    if local_filename == None:
        top.wm_title("Untitled" + " - " + TITLE)
    else:
        top.wm_title(os.path.basename(local_filename) + " - " + TITLE)
set_title(filename)

# toolbar commands
def br(event=None):
    editor.insert(INSERT, "<br />")
def ins_br():
    try:
        editor.delete(SEL)
    except:
        print('exception in function: ins_br')
    br()
    return 'break'
def indent(event=None):
    index = editor.index(INSERT).split(".")
    line_no = int(index[0])
    line_text = editor.get("%d.%d" % (line_no, 0),  "%d.end" % (line_no))
    text_only = line_text.lstrip(" ")
    no_of_spaces = len(line_text) - len(text_only)
    spaces = "\n" + " " * no_of_spaces
    editor.insert(INSERT, spaces)
    return 'break'
def indent_and_br(event=None):
    ins_br()
    indent()
    return 'break'
def enter_key():
    if ins_br_var.get() == 1 and indent_var.get() == 1:
        editor.bind('<Return>', indent_and_br)
    elif ins_br_var.get() == 1 and indent_var.get() == 0:
        editor.bind('<Return>', br)
    elif ins_br_var.get() == 0 and indent_var.get() == 1:
        editor.bind('<Return>', indent)
    else:
        editor.unbind('<Return>')
def h(event=None):
    try:
        editor.insert(SEL_FIRST, "<" + heading_var.get() + ">")
        editor.insert(SEL_LAST, "</" + heading_var.get() + ">")
    except TclError:
        #print("TclError")
        editor.insert(INSERT, "<" + heading_var.get() + "></" + heading_var.get() + ">")
        editor.mark_set("insert","%s-5c" % INSERT)
    editor.focus()
'''def lists(event=None):
    try:
        begin = editor.index(SEL_FIRST).split(".")
        end = editor.index(SEL_LAST).split(".")
        line = int(end[0]) - int(begin[0]) + 1
        counter = 1
        ins = editor.index(INSERT)
        editor.mark_set("cursor", SEL_FIRST)
        editor.insert("%s.%s" % (begin[0], begin[1]), "<" + list_var.get() + ">")
        indent()
        while line > 0:
            line_begin = str( int(begin[0]) + counter ) + "." + begin[1]
            line_end = str( int(begin[0]) + counter ) + ".end"
            editor.insert(line_begin, "   <li>")
            editor.insert(line_end, "</li>")
            counter = counter + 1
            line = line - 1
        editor.mark_set("cursor", str(int(end[0]) + 1) + ".end")
        editor.insert("cursor", "\n")
        editor.insert("cursor", " "*int(begin[1]) + "</" + list_var.get() + ">")
        
        editor.tag_delete(SEL)
        editor.tag_add(SEL, "", "%s+%dc" % (INSERT, 2 ))
    except:
        editor.insert(INSERT, "<" + list_var.get() + ">")
        indent()
        editor.insert(INSERT, "   <li></li>")
        indent()
        editor.mark_set("insert","%s-%dc" % (INSERT, 3))
        editor.insert(INSERT, "</" + list_var.get() + ">")
        editor.mark_set("insert","%s-%dl" % (INSERT, 1 ))
        editor.mark_set("insert","%s+%dc" % (INSERT, 2 ))
    editor.focus()'''
def lists(event=None):
    try:
        begin = editor.index(SEL_FIRST).split(".")
        end = editor.index(SEL_LAST).split(".")
        line = int(end[0]) - int(begin[0]) + 1
        counter = 1
        editor.insert("%s.%s" % (begin[0], begin[1]), "<" + list_var.get() + ">")
        indent()
        while line > 0:
            line_begin = str( int(begin[0]) + counter ) + "." + begin[1]
            line_end = str( int(begin[0]) + counter ) + ".end"
            editor.insert(line_begin, "   <li>")
            editor.insert(line_end, "</li>")
            counter = counter + 1
            line = line - 1
        editor.insert(str(int(end[0]) + 1) + ".end", "\n" + " "*int(begin[1]) + "</" + list_var.get() + ">")
        #editor.tag_config(SEL, "%s" % (str(begin[0]) + "." + str(begin[1])), "%s" % (str(end[0]) + "." + str(end[1])))
    except:
        print('ex')
    editor.focus()
def tag(event=None):
    try:
        editor.insert(SEL_FIRST, "<" + tag_var.get() + ">")
        editor.insert(SEL_LAST, "</" + tag_var.get() + ">")
    except TclError:
        print("TclError")
        editor.insert(INSERT, "<" + tag_var.get() + "></" + tag_var.get() + ">")
        editor.mark_set("insert","%s-%dc" % (INSERT, len(tag_var.get())+3 ))
    editor.focus()
def fn():
    print(editor.edit_modified())
# toolbar
toolbar = Frame(top, relief=RAISED)
toolbar.pack(side=TOP, fill=X)
ins_br_var = IntVar()
ins_br_cbox = Checkbutton(toolbar, text="ins_br", variable=ins_br_var, command=enter_key)
ins_br_cbox.pack(side=LEFT, padx=2, pady=2)
indent_var = IntVar()
indent_cbox = Checkbutton(toolbar, text="indent", variable=indent_var, command=enter_key)
indent_cbox.pack(side=LEFT, padx=2, pady=2)
lbButton = Button(toolbar, text="br", width=0, command=br)
lbButton.pack(side=LEFT, padx=2, pady=2)
heading_var = StringVar(toolbar)
heading_var.set("h1") # default value
heading = Combobox(toolbar, textvariable=heading_var, values=('h1', 'h2', 'h3', 'h4', 'h5', 'h6'), width=3, state='readonly')
heading.bind("<<ComboboxSelected>>", h)
heading.pack(side=LEFT, padx=2, pady=2)
list_var = StringVar(toolbar)
list_var.set("ul") # default value
list_cb = Combobox(toolbar, textvariable=list_var, values=('ol', 'ul'), width=5, state = 'readonly')
list_cb.bind("<<ComboboxSelected>>", lists)
list_cb.pack(side=LEFT, padx=2, pady=2)
tag_var = StringVar(toolbar)
tag_var.set("html") # default value
tag_cb = Combobox(toolbar, textvariable=tag_var, values=('html', 'title', 'body', 'head', 'p', 'ul', 'ol', 'li'), width=5, state = 'readonly')
tag_cb.bind("<<ComboboxSelected>>", tag)
tag_cb.pack(side=LEFT, padx=2, pady=2)
modButton = Button(toolbar, text="mod", width=0, command=lists)
modButton.pack(side=LEFT, padx=2, pady=2)
def rect_sel_end(event=None, delete=0):
    try:
        start_index = editor.index("sel.first").split(".")
        end_index = editor.index("sel.last").split(".")
        start_line = int(start_index[0])
        start_char = int(start_index[1])
        end_line = int(end_index[0])
        end_char = int(end_index[1])
        text = ""
        counter = 0
        no_of_lines = end_line - start_line + 1
        while no_of_lines > 0:
            start_rect_sel = str(start_line + counter) + "." + str(start_char)
            end_rect_sel = str(start_line + counter) + "." + str(end_char)
            if delete == 1:
                editor.delete(start_rect_sel, end_rect_sel)
            else:
                text = text + editor.get( start_rect_sel, end_rect_sel ) + "\n"
            counter = counter + 1
            no_of_lines = no_of_lines - 1
        return text
    except TclError:
        editor.tag_delete("selection")
        editor.mark_set("insert", INSERT)
        
def rect_sel_begin(event=None):
    editor.bind("<ButtonRelease-1>", rect_sel_end)
    editor.tag_delete("selection")
    try:
        start_index = editor.index("sel.first").split(".")
        end_index = editor.index("sel.last").split(".")
        start_line = int(start_index[0])
        start_char = int(start_index[1])
        end_line = int(end_index[0])
        end_char = int(end_index[1])
        counter = 0
        no_of_lines = end_line - start_line + 1
        while no_of_lines > 0:
            start_line_char = str(start_line + counter) + "." + str(start_char)
            end_line_char = str(start_line + counter) + "." + str(end_char)
            editor.tag_add("selection", start_line_char, end_line_char)
            no_of_lines = no_of_lines - 1
            counter = counter + 1
        editor.tag_config("selection", background="blue", foreground="black")
    except TclError:
        editor.mark_set("insert", INSERT)
def rectangular_selection():
    if rs.get() == 1:
        editor.config(selectbackground="white", inactiveselectbackground="white", selectforeground="black")#make normal selection invisible 
        editor.bind("<B1-Motion>", rect_sel_begin)
    elif rs.get() == 0:
        editor.unbind("<B1-Motion>")
        editor.unbind("<ButtonRelease-1>")
        editor.config(selectbackground="blue", inactiveselectbackground="gray", selectforeground="black")
    
rs = IntVar()
rs_cbox = Checkbutton(toolbar, text="rect_sel", variable=rs, command=rectangular_selection)
rs_cbox.pack(side=LEFT, padx=2, pady=2)

#micro functions
def save_if_modified():
    print("save_if_modified() editor.edit_modified()", editor.edit_modified())
    if editor.edit_modified():
        from tkinter.messagebox import askyesnocancel     
        response = askyesnocancel(TITLE, "This document has been modified. Do you want to save changes?") #cancel = none, no = false, yes = true
        print("Response: ", response)
        if response:
            cancelled = save()
            print("Cancelled: ", response)
            if cancelled == 1:
                return None
            elif cancelled == 0:
                return response
        else:
            return response
    else:
        return 0
def save(): #local_filename = filename):
    local_filename = filename
    if local_filename:
        cancelled = save_as(local_filename)
    else:
        cancelled = save_as()
    return cancelled
def save_as(local_filename=None):
    if local_filename == None:        
        from tkinter.filedialog import asksaveasfilename
        local_filename = asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt', 
    try:
        with open(local_filename, 'wb') as f:
                text = editor.get(1.0, END)
                f.write(bytes(text, 'UTF-8'))
                #f.write("\n") # normalize trailing whitespace
                editor.edit_modified(False)
                set_title(local_filename)
                return 0
    except FileNotFoundError:
        print('FileNotFoundError')
        return 1
def close():
    response = save_if_modified()
    if response != None: #None = Cancel save before new/open/quit confirmation, True = Save and quit, False = Quit without saving
        top.destroy() #sys.exit(0)
#file menu functions
def file_new(event = None):
    response = save_if_modified()
    if response != None:
        editor.delete(1.0, END)
        editor.edit_modified(False)
        global filename
        filename = None
        set_title()
        editor.edit_reset() 
def file_open(event = None, local_filename = None):
    response = save_if_modified()
    if response != None:
        # Returns the opened file
        if local_filename == None:
            from tkinter.filedialog import askopenfilename
            local_filename = askopenfilename()
        if local_filename != None  and local_filename != '':
            with open(local_filename, 'rb') as f:
                fileContents = f.read()# Get all the text from file.           
            # Set current text to file contents
            editor.delete(1.0, END)
            editor.insert(1.0, fileContents)
            editor.edit_modified(False)
            set_title(local_filename)
        global filename
        filename = local_filename
        return 'break'
if len(sys.argv) > 1:
    filename = sys.argv[1]
    file_open(local_filename = filename)
def file_save(event = None):
    save()
def file_save_as(event = None):
    save_as()
def file_quit(event = None):
    close() #sys.exit(0)
#edit menu functions
def edit_copy(event=None):
    print('rs.get()=', rs.get())
    if rs.get() == 1:
        editor.clipboard_clear()
        clipped_text = rect_sel_end()
        print('clipped_text=', clipped_text)
        editor.clipboard_append(clipped_text)
    else:
        try:
            editor.clipboard_clear()
            clipped_text = editor.get("sel.first", "sel.last")
            editor.clipboard_append(clipped_text)
        except TclError:
            pass
    return 'break'
def edit_cut(event=None):
    edit_copy()
    edit_delete()
def edit_paste(event=None):
    try:
        clipped_text = editor.selection_get(selection='CLIPBOARD')
        editor.insert('insert', clipped_text)
    except:
        pass
    return 'break'
def edit_delete(event=None):
    if rs.get() == 1:
        clipped_text = rect_sel_end()
        if clipped_text != None:
            rect_sel_end(delete=1)
            return 'break'
def edit_select_all(event = None):
    editor.tag_add(SEL, "1.0", END)
    editor.mark_set(INSERT, "1.0")
    editor.see(INSERT)
    return 'break'
def edit_find(event=None):
    try:
        editor.tag_delete("search")
    except:
        pass
    self = Toplevel(top)
    self.searchlabel = Label(self, text="Find what:")
    self.searchlabel.pack()
    self.key_word_entry = Entry(self, text="Find something...")
    self.key_word_entry.pack()
    self.matchcasevar = IntVar()
    self.matchcasevar.set(1)
    self.matchcase = Checkbutton(self, text="Match case", variable=self.matchcasevar)
    self.matchcase.pack()
    self.searcharea = StringVar()
    self.searcharea.set("all")
    self.group = LabelFrame(self, text="Direction", padx=5, pady=5)
    self.group.pack(padx=1, pady=3, anchor=W)
    Radiobutton(self.group, text="Up", variable=self.searcharea, value="up").pack(anchor=W)
    Radiobutton(self.group, text="Down", variable=self.searcharea, value="down").pack(anchor=W)
    Radiobutton(self.group, text="All", variable=self.searcharea, value="all").pack(anchor=W)
    self.key_word_entry.focus()
    def get_parameters(reply):
        key_word = self.key_word_entry.get()
        if self.searcharea.get() == "up":
            self.search_from = "1.0"
            self.search_until = INSERT
        elif self.searcharea.get() == "down":
            self.search_from = INSERT
            self.search_until = END
        elif self.searcharea.get() == "all":
            self.search_from = "1.0"
            self.search_until = END
        self.case_sensitive = self.matchcasevar.get()
        if reply == 1:
            answer = [key_word, self.search_from, self.search_until, self.case_sensitive]
            return answer
    get_parameters(reply=0)
    def findnextcmd(top=top, self=self, event=None):
        try:
            editor.tag_delete("current_word")
        except:
            pass
        answer = get_parameters(reply=1)
        key_word = answer[0]
        search_from = answer[1]
        search_until = answer[2]
        case_sensitive = answer[3]
        while True:
            start_kw = editor.search(key_word, search_from, stopindex=search_until, nocase=case_sensitive)
            if start_kw == "" or start_kw == None:
                try:
                    start_kw = editor.search(key_word, answer[1], stopindex=search_until, nocase=case_sensitive)    
                    editor.tag_configure("current_word", background="sea green")
                    editor.tag_add("current_word", start_kw, "%s + %sc"%(start_kw, len(key_word)))        
                    editor.see("%s + %sc"%(start_kw, len(key_word)))
                except:
                    pass
                break
            editor.tag_configure("search", background="green")
            editor.tag_add("search", start_kw, "%s + %sc"%(start_kw, len(key_word)))
            search_from = "%s + %sc "%(start_kw, len(key_word))
    self.findnext = Button(self, text="Find Next", command=findnextcmd)
    self.findnext.pack(anchor=W)
    self.bind("<Return>", findnextcmd)
    def cancelcmd(self=self):
        self.unbind("<Return>")
        editor.focus()
        self.destroy()
    self.cancel = Button(self, text="Cancel", command=cancelcmd)
    self.cancel.pack(anchor=W)
def edit_goto(event=None):
    from tkinter.simpledialog import askinteger
    line = askinteger('Goto', 'Enter line number:')
    editor.update()
    editor.focus()
    if line is not None:
        maxindex = editor.index(END+'-1c')
        maxline  = int(maxindex.split('.')[0])
        if line > 0 and line <= maxline:
            editor.mark_set(INSERT, '%d.0' % line)      # goto line
            editor.tag_remove(SEL, '1.0', END)          # delete selects
            editor.tag_add(SEL, INSERT, 'insert + 1l')  # select line
            editor.text.see(INSERT)                          # scroll to line
        else:
            from tkinter.messagebox import showerror
            showerror('PyEdit', 'Bad line number')
#other functions
def hello():
    messagebox.showinfo("Ok!")
    
#instead of closing the window, execute a function
top.protocol("WM_DELETE_WINDOW", close) 

#create a top level menu
menubar = Menu(top)
#Menu item File
filemenu = Menu(menubar, tearoff=0)# tearoff = 0 => can't be seperated from window
filemenu.add_command(label="New", underline=1, command=file_new, accelerator="Ctrl+N")
filemenu.add_command(label="Open...", underline=1, command=file_open, accelerator="Ctrl+O")
filemenu.add_command(label="Save", underline=1, command=file_save, accelerator="Ctrl+S")
filemenu.add_command(label="Save As...", underline=5, command=file_save_as, accelerator="Ctrl+Alt+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", underline=2, command=file_quit, accelerator="Alt+F4")
menubar.add_cascade(label="File", underline=0, menu=filemenu)
#Menu item Edit
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", underline=0, command=editor.edit_undo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", underline=0, command=editor.edit_redo, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut", underline=2, command=edit_cut, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", underline=0, command=edit_copy, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", underline=0, command=edit_paste, accelerator="Ctrl+V")
editmenu.add_command(label="Delete", underline=2, command=edit_delete, accelerator="Del")
editmenu.add_separator()
editmenu.add_command(label="Find...", underline=0, command=edit_find, accelerator="Ctrl+F")
editmenu.add_command(label="Find Next", underline=6, command=hello, accelerator="F3")
editmenu.add_command(label="Replace...", underline=0, command=hello, accelerator="Ctrl+H")
editmenu.add_command(label="Go To...", underline=0, command=edit_goto, accelerator="Ctrl+G")
editmenu.add_checkbutton(label="Toggle insert linebreak", variable=ins_br, command=enter_key)
editmenu.add_separator()
editmenu.add_command(label="Select All", command=edit_select_all, accelerator="Ctrl+A")
editmenu.add_command(label="Time/Date", command=hello, accelerator="F5")
menubar.add_cascade(label="Edit", underline=0, menu=editmenu)
#Menu item Format
formatmenu = Menu(menubar, tearoff=0)
formatmenu.add_command(label="Word Wrap", command=hello)
formatmenu.add_command(label="Font...", command=hello)
menubar.add_cascade(label="Format", underline=1, menu=formatmenu)
#Menu item View
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Status Bar", command=hello)
menubar.add_cascade(label="View", underline=0, menu=viewmenu)
#Menu item Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Manual", command=hello)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", underline=0, menu=helpmenu)
# display the menu
top.config(menu=menubar)
# create keyboard shortcuts for functions
editor.bind("<Control-n>", file_new)
editor.bind("<Control-o>", file_open)
editor.bind("<Control-s>", file_save)
editor.bind("<Control-Shift-s>", file_save_as)
editor.bind("<Control-q>", file_quit)
editor.bind("<Control-N>", file_new)
editor.bind("<Control-O>", file_open)
editor.bind("<Control-S>", file_save)
editor.bind("<Control-Shift-S>", file_save_as)
editor.bind("<Control-Q>", file_quit)
editor.bind("<Control-a>", edit_select_all)
editor.bind("<Control-A>", edit_select_all)
editor.bind("<Control-f>", edit_find)
editor.bind("<Control-F>", edit_find)
editor.bind("<Control-C>", edit_copy)
editor.bind("<Control-c>", edit_copy)
editor.bind("<Control-V>", edit_paste)
editor.bind("<Control-v>", edit_paste)
editor.bind("<Control-X>", edit_cut)
editor.bind("<Control-x>", edit_cut)
editor.bind("<BackSpace>", edit_delete)
editor.bind("<Delete>", edit_delete)
editor.bind("<Control-G>", edit_goto)
editor.bind("<Control-g>", edit_goto)
#h1 -h6 shortcuts
editor.bind("<Control-1>", h)
editor.bind("<Control-2>", h)
editor.bind("<Control-3>", h)
editor.bind("<Control-4>", h)
editor.bind("<Control-5>", h)
editor.bind("<Control-6>", h)
editor.bind("<Control-b>", h)
editor.bind("<Control-B>", h)
editor.bind("<Control-i>", h)
editor.bind("<Control-I>", h)
editor.bind("<Control-u>", h)
editor.bind("<Control-U>", h)
#context menu
cmenu = Menu(top, tearoff=0)
cmenu.add_command(label="Undo", command=editor.edit_undo)
cmenu.add_separator()
cmenu.add_command(label="Cut", command=edit_cut)
cmenu.add_command(label="Copy", command=edit_copy)
cmenu.add_command(label="Paste", command=edit_paste)
cmenu.add_command(label="Delete", command=edit_delete)
cmenu.add_separator()
cmenu.add_command(label="Select all", command=edit_select_all)
cmenu.add_separator()
cmenu.add_command(label="Exit", command=file_quit)
def context_menu(event):
    cmenu.post(event.x_root, event.y_root)
editor.bind("<Button-3>", context_menu)



mainloop()
