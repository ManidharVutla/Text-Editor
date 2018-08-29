from Tkinter import *
from tkFileDialog import *
import os
from tkMessageBox import *
from tkFont import *
root=Tk()

title="Simple Text Editor!";
root.title(title)
root.geometry("1000x500")




file_name=None
show_line_number=IntVar()
show_line_number.set(1)



def get_line_numbers():
	output= ''
	if show_line_number.get():
		row,col=textpanel.index("end").split('.')
		for i in range(1,int(row)):
			output += str(i)+'\n'
		return output
def update_line_numbers(event=None):
	line_numbers=get_line_numbers()
	linenum.config(state='normal')
	linenum.delete('1.0','end')
	linenum.insert('1.0',line_numbers)
	linenum.config(state='disabled')

def on_content_changed(event=None):
	update_line_numbers()

#Function for Cut

def cut():
	textpanel.event_generate("<<Cut>>")
	on_content_changed()

#Functon for Copy

def copy():
	textpanel.event_generate("<<Copy>>")
	on_content_changed()

#Functon for Paste

def paste():
	textpanel.event_generate("<<Paste>>")
	on_content_changed()

#Function for Undo

def undo():
	textpanel.event_generate("<<Undo>>")
	on_content_changed()

#Function for Redo

def redo(event=None):
	textpanel.event_generate("<<Redo>>")
	on_content_changed()
	return 'break'

#Function for Select All

def select_All(event=None):
	textpanel.tag_add('sel','1.0','end')
	return 'break'


# Function for Open

def opening_file(event=None):
	file_open=askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
	if file_open:
		global file_name
		file_name= file_open
		root.title('{} - {}'.format(os.path.basename(file_name),title))
		textpanel.delete(1.0,END)
		with open(file_name) as _file:
			textpanel.insert(1.0,_file.read())
		on_content_changed()

# Function for Save
def save(event=None):
	global file_name
	if not file_name:
		saveas()
	else:
		write_file(file_name)
	return "break"

# Function for SaveAs

def saveas(event=None):
	file_open=asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
	if file_open:
		global file_name
		file_name=file_open
		write_file(file_name)
		root.title('{} - {}'.format(os.path.basename(file_name),title))
	return "break"


# Write_File

def write_file(file_name):
	try:
		content=textpanel.get(1.0,END)
		with open(file_name,'w') as the_file:
			the_file.write(content)
	except IOError:
		pass

def new_file(event=None):
	root.title("{} - {}".format("Untitled",title))
	global file_name
	file_name=None
	textpanel.delete(1.0,END)
	on_content_changed()

def about(event=None):
	showinfo(title="About Me!", message="A Simple text editor for minor content changes!")	




#--------------------------------------------------------- UI Part ---------------------------------------------------------------

#Menu Bar
menubar=Menu(root,background="#306EFF",foreground="#306EFF", activebackground="#306EFF", activeforeground="#306EFF")
root.config(menu=menubar)





submenu=Menu(menubar)

#File Menu

menubar.add_cascade(label="File",menu=submenu)
submenu.add_command(label="Grab Something New!",accelerator='New',command=new_file)
submenu.add_command(label="Wanna Open Something!",accelerator='Open',command=opening_file)
submenu.add_command(label="Better save your work!",accelerator='Save',command=save)
submenu.add_command(label="Don't search for SaveAs!",accelerator='SaveAs',command=saveas)
submenu.add_separator()
submenu.add_command(label="See You Soon! Bye!",accelerator='Exit',command=root.quit)

#Edit Menu

editmenu=Menu(menubar)

menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Made a mistake!",accelerator='Undo',command=undo)
editmenu.add_command(label="Redo the Undo!",accelerator='Redo',command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut Anything",accelerator='Cut',command=cut)
editmenu.add_command(label="Copy Something",accelerator='Copy',command=copy)
editmenu.add_command(label="Paste Somewhere",accelerator='Paste',command=paste)

# Help menu

helpmenu=Menu(menubar)

menubar.add_cascade(label="About",menu=helpmenu)
helpmenu.add_command(label="Wanna Know about Me!",command=about)

#Icons Panel

shortcutbar=Frame(root,height=30)
shortcutbar.pack(fill='x')

#Line number 

linenum=Text(root,width=3,takefocus=0,border=0,state='disabled',foreground="#306EFF",wrap='none')
linenum.config(font=("Times New Roman", 15,'bold'))
linenum.pack(side='left',fill='y')

#Text Panel

textpanel=Text(root,wrap='word',undo=1)
textpanel.config(font=("Times New Roman", 15))
textpanel.pack(expand='yes',fill='both')
textpanel.bind('<Control-y>',redo)
textpanel.bind('<Control-Y>',redo)
textpanel.bind('<Control-a>',select_All)
textpanel.bind('<Control-A>',select_All)
textpanel.bind('<Control-n>',new_file)
textpanel.bind('<Control-N>',new_file)
textpanel.bind('<Control-o>',opening_file)
textpanel.bind('<Control-O>',opening_file)
textpanel.bind('<Control-S>',save)
textpanel.bind('<Control-s>',save)
textpanel.bind('<Any-KeyPress>',on_content_changed)

#Scroll Bar

scrollbar=Scrollbar(textpanel)
textpanel.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=textpanel.yview)
scrollbar.pack(side='right',fill='y')


#Buttons on Shortcut bar
helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="New",border=0,foreground="#306EFF",background="white",command=new_file)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')


# Open Button

helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="Open",border=0,foreground="#306EFF",background="white",command=opening_file)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')


# Save Button

helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="Save",border=0,foreground="#306EFF",background="white",command=save)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')

# Undo Button


helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="Undo",border=0,foreground="#306EFF",background="white",command=undo)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')

# Redo Button 


helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="Redo",border=0,foreground="#306EFF",background="white",command=redo)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')

# Exit Button


helv36 = Font(weight='bold')
tool_bar=Button(shortcutbar,text="Exit",border=0,foreground="#306EFF",background="white",command=root.quit)
tool_bar['font'] = helv36

tool_bar.pack(expand='yes',fill='both',side='left')

# Status bar

status=Label(root,text="Developed By Manidhar Vutla",relief="sunken",anchor="s")
status.pack(side=BOTTOM,fill='x')

root.mainloop()
