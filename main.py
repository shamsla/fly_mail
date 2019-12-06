##########################################################

#              Programmer: ShAms LA
#              GitHub: https://github.com/shams-la
#              Email: contact.shams.in@gmail.com

##########################################################


from tkinter import *
from tkinter import ttk, messagebox
import re, funcs, threading, webbrowser, file_main, imagesdata, io, bug
from PIL import ImageTk, Image
from set_logo import setLogo
#################### Functions #############################
#############################################################
#############################################################
def makeShow(val):
    if val:
        if user_password.get() != "  Password":
            user_password.config(show = "\u2022")
    else:
        user_password.config(show = "")

def showHide(val):
    global color_check, sh_btn_check
    if not color_check:
        if val:
            show_btn.pack_forget()
            hide_btn.pack(side = LEFT, padx = (0, 15))
            makeShow(False)
            sh_btn_check = False
        else:
            hide_btn.pack_forget()
            show_btn.pack(side = LEFT, padx = (0, 15))
            makeShow(True)
            sh_btn_check = True
    else:
        if val:
            show_btn_l.pack_forget()
            hide_btn_l.pack(side = LEFT, padx = (0, 15))
            makeShow(False)
            sh_btn_check = False

        else:
            hide_btn_l.pack_forget()
            show_btn_l.pack(side = LEFT, padx = (0, 15))
            makeShow(True)
            sh_btn_check = True


def reset(e):
    root.focus_set()
    mess_label.pack_forget()

def checkMail(string):
    pattern = r"^[\w.-]+@[\w-]+\.[a-z]{2,8}$"
    if re.match(pattern, string):
        return True
    return False

def displayResult(string, val, width):
    if val:
        mess_label.config(text = string, background = success_color, width = width)
    else:
        mess_label.config(text = string, background = danger_color, width = width)
    mess_label.pack(ipady = 4)

def startThread(target, args, callback):
    global thread
    thread = threading.Thread(target = target, args = args)
    thread.start()
    main_frame.pack_forget()
    empty_menu = Menu(root)
    root.config(menu = empty_menu)
    bar_frame.place(relx = 0.5, rely = 0.5, y = -10, anchor = "center")
    pro_bar.start(15)
    root.after(20, lambda: checkThread(callback))


def checkThread(callback):
    global thread
    if thread.is_alive():
        root.after(20, lambda: checkThread(callback))
    else:
        pro_bar.stop()
        bar_frame.place_forget()
        root.config(menu = menu1)
        main_frame.pack(fill = "both", padx = 27)
        callback()

def makeForget(num):
    if num:
        login_btn.pack_forget()
        login_label.pack_forget()
        send_label.pack_forget()
        send_btn.pack_forget()
    else:
        login_btn_l.pack_forget()
        login_label_l.pack_forget()
        send_btn_l.pack_forget()
        send_label_l.pack_forget()

def send():
    global details

    email = rev_email.get()
    mess = text_area.get(1.0, END)
    subject = title.get()

    if not checkMail(email) or email in ("", "  Recievers's Email") or subject in ("", "  Title") or mess in ("\n", "  Message...\n"):
        root.focus_set()
        if not checkMail(email) or email in ("", "  Email"):
            rev_email.config(highlightthickness = 1)
        if subject in ("", "  Title"):
            title.config(highlightthickness = 1)
        if mess in ("\n", "  Message...\n"):
            text_area.config(highlightthickness = 1)

    else:
        startThread(funcs.sendMail, (details[0], details[1], email, mess, subject), afterSend)


def afterSend():
    global _hold_text, text_color, place_color, color_check, btn_check

    if funcs.GETBOOL != True:
        if funcs.GETBOOL == "SMTPAuthenticationError":
            displayResult("Allow lesssecureapps", False, 20)
        else:
            displayResult("ERR! Check Your Internet Connection", False, 32)
    else:
        displayResult("Email Sent Successfully.", True, 25)
        _hold_text = ("  Email", "  Password")
        user_email.config(foreground = text_color)
        user_password.config(foreground = text_color)
        for entry in ([rev_email, "  Login First."], [title, "  Title"]):
            entry[0].delete(0, END)
            focusOut(entry[0], entry[1])
        text_area.delete(1.0, END)
        focusOut(text_area, text = "  Message...", area = True)
        
        if not color_check:
            makeForget(num = False)
            login_label.pack_forget()
            login_btn.pack(side = RIGHT, anchor = "e")
            send_label.pack(anchor="w", pady=(20, 0))
            send_btn.pack_forget()
        else:
            makeForget(num = True)
            login_label_l.pack_forget()
            login_btn_l.pack(anchor = "e", side = RIGHT)
            send_label_l.pack(anchor="w", pady=(20, 0))
            send_btn_l.pack_forget()

        btn_check = True
        funcs.GETBOOL = False
    root.focus_set()


def login():
    global thread
    email = user_email.get()
    password = user_password.get()

    if not checkMail(email) or email in ("", "  Email") or password in ("", "  Password"):
        root.focus_set()
        if not checkMail(email) or email in ("", "  Email"):
            user_email.config(highlightthickness = 1)
        if password in ("", "  Password"):
            user_password.config(highlightthickness = 1)
    else:
        if details != None and email == details[0] and password == details[1]:
            funcs.GETBOOL = True
            afterLogin()
        else:
            startThread(funcs.login, (email, password), afterLogin)

def afterLogin():
    global _hold_text, place_color,color_check, btn_check, details

    if funcs.GETBOOL != True:
        if not funcs.GETBOOL:
            displayResult("Only [gmail,yahoo,outlook,hotmail] Acc Supported", False, 40)
        elif funcs.GETBOOL == "SMTPAuthenticationError":
            displayResult("Invalid Email OR Password", False, 22)
            if dont_show_var.get() == 0:
                gmailError()
        else:
            displayResult("ERR! Check Your Internet Connection", False, 30)
    else:
        displayResult("Successfully Loged In.", True, 20)
        details = [user_email.get(), user_password.get()]
        _hold_text = ("  Reciever's Email", "  Title", "  Message...")
        user_email.config(foreground = place_color)
        user_password.config(foreground = place_color)
        rev_email.delete(0, END)
        rev_email.insert(0, "  Reciever's Email")

        if not color_check:
            makeForget(num = False)
            login_btn.pack_forget()
            login_label.pack(anchor = "e", side = RIGHT)
            send_label.pack_forget()
            send_btn.pack(anchor="w", pady=(20, 0))
        else:
            makeForget(num = True)
            login_btn_l.pack_forget()
            login_label_l.pack(anchor = "e", side = RIGHT)
            send_label_l.pack_forget()
            send_btn_l.pack(anchor="w", pady=(20, 0))
        
        btn_check = False
        funcs.GETBOOL = False
    root.focus_set()

def makeDark():
    global color_check,text_color, place_color, _hold_text, btn_check, danger_color, success_color, pro_bar, sh_btn_check

    back_color = "#fafafa"
    entry_color = "#e3e3e3"
    placeholder = "#5f6368"
    text =  "#000000"

    if color_check:
        back_color = "#21252B"
        entry_color = "#323843"
        placeholder = "#ABB4C2"
        text = "#ffffff"

        makeForget(num = True)

        if btn_check:
            login_btn_l.pack_forget()
            send_label_l.pack_forget()
            login_btn.pack(side = RIGHT, anchor = "e")
            send_label.pack(anchor="w", pady=(20, 0))
        else:
            login_label.pack(anchor = "e", side = RIGHT)
            send_btn.pack(anchor="w", pady=(20, 0))
            login_label_l.pack_forget()
            send_btn_l.pack_forget()
        
        color_shift_d.pack_forget()
        color_shift_l.pack(anchor = "e", pady = (5, 0))
        main_logo_l.pack_forget()
        main_logo_d.pack()


        if sh_btn_check:
            show_btn_l.pack_forget()
            show_btn.pack(side = LEFT, padx = (0, 15))
        else:
            hide_btn_l.pack_forget()
            hide_btn.pack(side = LEFT, padx = (0, 15))

        danger_color = "#bd4339"
        success_color = "#21ad68"
        mess_label.config(foreground = "#ffffff")
        if mess_label["background"] == "#89f0bd":
            mess_label.config(background = success_color)
        elif mess_label["background"] == "#f78e86":
            mess_label.config(background = danger_color)
        
        wait_light.pack_forget()
        wait_dark.pack(pady = (0, 20))

        styler.configure("red.Horizontal.TProgressbar", troughcolor="#323843", bordercolor="#323843", background="#fafafa", lightcolor="#fafafa", darkcolor="#fafafa")

        pro_bar.pack_forget()
        pro_bar.pack(ipady = 3)

        color_check = False
        
        setColorMode("dark") # setting color to deafult color mode { check setColorMode() for more }
    else:
        makeForget(num = True)
        if btn_check:
            login_btn.pack_forget()
            send_label.pack_forget()
            login_btn_l.pack(anchor = "e", side = RIGHT)
            send_label_l.pack(anchor="w", pady=(20, 0))
        else:
            login_label.pack_forget()
            send_btn.pack_forget()
            login_label_l.pack(anchor = "e", side = RIGHT)
            send_btn_l.pack(anchor="w", pady=(20, 0))
        color_shift_l.pack_forget()
        color_shift_d.pack(anchor = "e", pady = (5, 0))
        main_logo_d.pack_forget()
        main_logo_l.pack()
        

        if sh_btn_check:
            show_btn.pack_forget()
            show_btn_l.pack(side = LEFT, padx = (0, 15))
        else:
            hide_btn.pack_forget()
            hide_btn_l.pack(side = LEFT, padx = (0, 15))

        danger_color = "#f78e86"
        success_color = "#89f0bd"
        mess_label.config(foreground = "#000000")
        if mess_label["background"] == "#21ad68":
            mess_label.config(background = success_color)
        elif mess_label["background"] == "#bd4339":
            mess_label.config(background = danger_color)

        wait_dark.pack_forget()
        wait_light.pack(pady = (0, 20))

        styler.configure("red.Horizontal.TProgressbar", troughcolor="#e3e3e3", bordercolor="#e3e3e3", background="#323843", lightcolor="#323843", darkcolor="#323843")

        pro_bar.pack_forget()
        pro_bar.pack(ipady = 3)       

        color_check = True

        setColorMode("light") # setting color to deafult color mode { check setColorMode() for more }


    root.configure(background = back_color)
    for i in (main_frame, u_left_frame, u_right_frame, top_frame, mid_frame, bot_frame, left_frame, right_frame, color_frame, lg_right_frame, lg_left_frame, login_frame_r, login_frame_l, bar_frame):
        i.config(background = back_color)
    for i in (user_email, user_password, rev_email, title, text_area):
        i.config(background = entry_color, foreground = placeholder, insertbackground = text)
    place_color = placeholder
    text_color = text
    entries = ({"  Reciever's Email": rev_email, "  Title": title, "  Email": user_email, "  Password": user_password})
    for key, val in entries.items():
        if key in _hold_text:
            val.delete(0, END)
            focusOut(val, key)
    if "  Message..." in _hold_text:
        text_area.delete(1.0, END)
        focusOut(text_area, text = "  Message...",area = True)
    root.focus_set()

def showBug():
    """
    Bug Open Here. (Report Bug)
    """

    bug.bug(root=root, main_frame=main_frame, win_width=550, win_height=380, logo = ImageTk.PhotoImage(getImage(imagesdata.cardLight()).resize((139, 28), Image.ANTIALIAS)), terminator=bugTerminator, wait_image=ImageTk.PhotoImage(getImage(imagesdata.waitLight()).resize((153, 13), Image.ANTIALIAS)), p_pad=160, p_length=230)

def bugTerminator():
    
    """
    After The Bug Report (after sending the report)
    """

    root_color = "#fafafa" if color_check else "#21252b"
    root.config(menu = menu1, bg=root_color) # getting old menu

    if bug.bugbool:
        displayResult("Thanks For Your Feedback.", True, 23)
    else:
        displayResult("Please Check Your Internet Connection", False, 31)        

def focusing(element, text, area = None):
    global _hold_text, text_color
    if text not in _hold_text:
        root.focus_set()
    else:
        element.config(highlightthickness = 0)
        if area:
            if element.get(1.0, END) == text+"\n":
                element.delete(1.0, END)
                element.config(foreground = text_color)
        else: 
            if element.get() == text:
                if element.get() == "  Password" and sh_btn_check == True:
                    element.config(show = "\u2022")
                element.delete(0,END)
                element.config(foreground = text_color)
                
    mess_label.pack_forget()

def focusOut(element, text, area = None):
    global place_color
    if area:
        if element.get(1.0, END) == "\n":
            element.insert(END,text)
            element.config(foreground = place_color)
    else:
        if not element.get():
            if element == user_password:
                    element.config(show = "")
            element.insert(0,text)
            element.config(foreground = place_color)

def defaultColorMode():
    global color_check
    """ Sets the color mode (light | Drak)
        Stored in file.
        Everytime when program runs.
    """
    color_mode_name = file_main.getProp("user_color_mode")
    print(color_mode_name)
    if color_mode_name == 2:
        defaultColorMode()
    elif color_mode_name == "light":
        color_check = False
        makeDark()
    else:
        color_check = True
        makeDark()
    
def setColorMode(mode):
    """
        | store the color mode in managerud.dta file.
        | everytime when user toggle the color.
        |
        | Args:
        |   mode: (color mode) required for setting the color. [ mostly from makeDark() ]

    """
    output = file_main.writeProp("user_color_mode", mode)
    if not output:
        setColorMode(mode)


def setSelect(e):
    hold_int = dont_show_var.get()
    if hold_int == 1:
        get_res = file_main.writeProp("user_select_dont_show", False)
        if not get_res:
            file_main.writeProp("user_select_dont_show", False)
    else:
        get_res = file_main.writeProp("user_select_dont_show", True)
        if not get_res:
            file_main.writeProp("user_select_dont_show", True)

def getSelect():
    value = file_main.getProp("user_select_dont_show")
    if value == 2:
        value = file_main.getProp("user_select_dont_show")
    if value:
        return 1
    return 0


def makeNormal():
    global color_check
    dont_show.place_forget()
    disc_frame.pack_forget()
    main_frame.pack(fill = "both", padx = 24)
        
    root.maxsize(height=380, width=550)
    root.minsize(height=380, width=550)
    if color_check:
        root.config(bg = "#fafafa", menu = menu1)
    else:   
        root.config(bg = "#21252B", menu = menu1)
    root.withdraw()
    root.deiconify()

def allowGmail():
    webbrowser.open("https://myaccount.google.com/lesssecureapps")

def gmailError():
    main_frame.pack_forget()
    disc_frame.pack(fill = "both", padx = (0, 30), pady = (24, 0))
    dont_show.place(x = 10, y  = 400)
    empty = Menu(root)
    root.maxsize(height=430, width=560)
    root.minsize(height=430, width=560)
    root.config(bg = "#384150", menu = empty)

def insta():
    webbrowser.open("https://www.instagram.com/leme.shams/")

def twitter():
    webbrowser.open("https://twitter.com/shams_la")

def gitHub():
    webbrowser.open("https://github.com/shams-la")

def helpp():
    messagebox.showinfo(title='Help',message='Firstly, Login by putting your Email and Password.\n\n\tThen, Enter receiver\'s email.\n\tPut subject(Title of message) and message.\n\nThen click on SEND button.')

def ask():
    ans = messagebox.askyesno(title="Exit",message="Are You Sure?")
    if ans is True:
        quit()
def d_show():
    messagebox.showinfo(title="About",message="  FLY-MAIL\n\nVersion: 1.0\n- ShAms LA.\nEmail: contact.shams.in@gmail.com\nGitHub - https://github.com/shams-la")

def getImage(data):
    image = Image.open(io.BytesIO(bytearray(data)))
    return image

root = Tk()
root.title("Fly Mail")
root.geometry("550x350")
root.maxsize(height=380, width=550)
root.minsize(height=380, width=550)
root.configure(bg="#21252B")
setLogo(root)

_hold_text = ("  Email", "  Password")
place_color = "#ABB4C2"
text_color = "#ffffff"
danger_color = "#bd4339"
success_color = "#21ad68"
details = None
color_check = False
btn_check = True
sh_btn_check = True


styler = ttk.Style()
styler.theme_use("clam")
styler.configure("red.Horizontal.TProgressbar", troughcolor="#323843", bordercolor="#323843", background="#fafafa", lightcolor="#fafafa", darkcolor="#fafafa")
#################### Menu #############################
#############################################################
#############################################################


menu1 = Menu(root)
root.config(menu=menu1)

file_menu = Menu(menu1,tearoff=0)
menu1.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='Exit',command=ask)


follow = Menu(menu1,tearoff=0)
menu1.add_cascade(label='Follow',menu=follow)
follow.add_command(label = "Instagram", command = insta)
follow.add_command(label = "Twitter", command = twitter)
follow.add_command(label = "Github", command = gitHub)

help_menu = Menu(menu1, tearoff = 0)
menu1.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "How To", command = helpp)
help_menu.add_command(label = "Gmail Error", command = gmailError)
help_menu.add_command(label = "Report Bug", command = showBug)

menu1.add_command(label='About',command=d_show)
#################### Main Frame #############################



disc_frame = Frame(root, bg = "#384150")
# disc_frame.pack(fill = "both")

disc_img = ImageTk.PhotoImage(getImage(imagesdata.disc()).resize((354, 388), Image.ANTIALIAS))
right_arrow = ImageTk.PhotoImage(getImage(imagesdata.rightArrow()).resize((30, 26), Image.ANTIALIAS))
left_arrow = ImageTk.PhotoImage(getImage(imagesdata.leftArrow()).resize((24, 21), Image.ANTIALIAS))

Label(disc_frame, image = disc_img, borderwidth = 0, highlightthickness = 0).pack()
right_btn_a = Button(disc_frame, image = right_arrow, cursor = "hand2", borderwidth = 0, highlightthickness = 0, activebackground = "#14cadf", relief = "flat", command = allowGmail)
left_btn_a = Button(disc_frame, image = left_arrow, cursor = "hand2", borderwidth = 0, highlightthickness = 0, activebackground = "#323843", relief = "flat", command = makeNormal)

right_btn_a.place(x = 140, y = 275)
left_btn_a.place(x = 383, y = 63)

styler.configure("Red.TCheckbutton", background = "#384150", foreground = "#fafafa")

dont_show_var = IntVar()
dont_show = ttk.Checkbutton(root, text = "Don't Show Again", style = "Red.TCheckbutton", cursor = "hand2", takefocus = False, variable = dont_show_var, onvalue = 1, offvalue = 0)


#############################################################
#############################################################

bar_frame = Frame(root, background = "#21252B")
# bar_frame.place(relx = 0.5, rely = 0.5,y = -10, anchor = "center")

wait_img_d = ImageTk.PhotoImage(getImage(imagesdata.PleaseWait()).resize((153, 13), Image.ANTIALIAS))
wait_dark = Label(bar_frame, image = wait_img_d, borderwidth = 0, highlightthickness = 0)
wait_dark.pack(pady = (0, 20))

wait_img_l = ImageTk.PhotoImage(getImage(imagesdata.waitLight()).resize((153, 13), Image.ANTIALIAS))
wait_light = Label(bar_frame, image = wait_img_l, borderwidth = 0, highlightthickness = 0)


pro_bar = ttk.Progressbar(bar_frame, style = "red.Horizontal.TProgressbar", mode = "indeterminate", length = 230)
pro_bar.pack(ipady = 3)

main_frame = Frame(root, background="#21252B")
main_frame.pack(fill = "both", padx = 24)
#################### Frames #############################
#############################################################
#############################################################

color_frame = Frame(main_frame, bg = "#21252B")
color_frame.pack(fill = "both", pady = (30, 0))

top_frame = Frame(main_frame, background="#21252B")
top_frame.pack(fill="both", pady=(30, 0))

mid_frame = Frame(main_frame, background="#21252B")
mid_frame.pack(fill="both", pady=20)

bot_frame = Frame(main_frame, background="#21252B")
bot_frame.pack(fill="both")

#################### TOP-Frame #############################
############################################################

lg_left_frame = Frame(color_frame, background="#21252B")
lg_left_frame.pack(side = LEFT, fill = "both", padx = (10, 0))

lg_right_frame = Frame(color_frame, background="#21252B")
lg_right_frame.pack(anchor = "se", side = RIGHT, fill = "both")

#############################################################


logo_img_d = ImageTk.PhotoImage(getImage(imagesdata.cardDark()).resize((153, 31), Image.ANTIALIAS))
logo_img_l = ImageTk.PhotoImage(getImage(imagesdata.cardLight()).resize((153, 31), Image.ANTIALIAS))
main_logo_d = Label(lg_left_frame, image = logo_img_d, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat")
main_logo_d.pack()
main_logo_l = Label(lg_left_frame, image = logo_img_l, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat")

#############################################################
#############################################################



dark_img = ImageTk.PhotoImage(getImage(imagesdata.dark()).resize((42, 23), Image.ANTIALIAS))
light_img = ImageTk.PhotoImage(getImage(imagesdata.light()).resize((42, 22), Image.ANTIALIAS))
color_shift_l = Button(lg_right_frame, image = light_img, cursor = "hand2", borderwidth = 0, highlightthickness = 0, activebackground = "#21252B", relief = "flat", command = makeDark)
color_shift_l.pack(anchor = "se", pady = (5, 0))

color_shift_d = Button(lg_right_frame, image = dark_img, cursor = "hand2", borderwidth = 0, highlightthickness = 0, activebackground = "#fafafa", relief = "flat", command = makeDark)
#################### TOP-Frame #############################
#############################################################
#############################################################

u_left_frame = Frame(top_frame, bg = "#21252B")
u_left_frame.pack(side = LEFT, fill = "both",padx=(0, 10))

u_right_frame = Frame(top_frame, bg = "#21252B")
u_right_frame.pack(side = RIGHT, fill = "both",padx=(10, 0))

user_email = Entry(u_left_frame)
user_email.pack(ipady=6)
user_email.insert(0, "  Email")

user_password = Entry(u_right_frame)
user_password.pack(ipady=6)
user_password.insert(0, "  Password")

#################### MID-Frame #############################
#############################################################

login_frame_l = Frame(mid_frame, bg = "#21252B")
login_frame_l.pack(side = LEFT, fill = "both")

login_frame_r = Frame(mid_frame, bg = "#21252B")
login_frame_r.pack(side = RIGHT, fill = "both")

#############################################################

lg_img_d = ImageTk.PhotoImage(getImage(imagesdata.loginD()).resize((84, 35), Image.ANTIALIAS))
lg_img = ImageTk.PhotoImage(getImage(imagesdata.login()).resize((84, 33), Image.ANTIALIAS))
lg_img_l = ImageTk.PhotoImage(getImage(imagesdata.loginLight()).resize((84, 35), Image.ANTIALIAS))
lg_img_ld = ImageTk.PhotoImage(getImage(imagesdata.loginLightD()).resize((84, 35), Image.ANTIALIAS))

login_btn = Button(login_frame_r, image = lg_img, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", command = login)
login_btn.pack(side = RIGHT, anchor = "e")
login_label = Label(login_frame_r, image = lg_img_d, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat")

login_btn_l = Button(login_frame_r, image = lg_img_l, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", command = login)
login_label_l = Label(login_frame_r, image = lg_img_ld, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat")

show_img = ImageTk.PhotoImage(getImage(imagesdata.show()).resize((27, 20), Image.ANTIALIAS))
hide_img = ImageTk.PhotoImage(getImage(imagesdata.hide()).resize((27, 20), Image.ANTIALIAS))
show_img_l = ImageTk.PhotoImage(getImage(imagesdata.showLight()).resize((27, 20), Image.ANTIALIAS))
hide_img_l = ImageTk.PhotoImage(getImage(imagesdata.hideLight()).resize((27, 20), Image.ANTIALIAS))


show_btn = Button(login_frame_r, image = show_img,  borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", activebackground = "#21252B", command = lambda: showHide(True))
show_btn.pack(side = LEFT, padx = (0, 15))

hide_btn = Button(login_frame_r, image = hide_img, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", activebackground = "#21252B", command = lambda: showHide(False))

show_btn_l = Button(login_frame_r, image = show_img_l, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", activebackground = "#fafafa", command = lambda: showHide(True))

hide_btn_l = Button(login_frame_r, image = hide_img_l, borderwidth = 0, cursor = "hand2", highlightthickness = 0, relief = "flat", activebackground = "#fafafa", command = lambda: showHide(False))


mess_label = Label(login_frame_l, text = "", foreground = "#ffffff", font = ("Calibri", 13), background = "#21ad68", width = 30)
#################### BOT-Frame #############################
#############################################################
#############################################################

left_frame = Frame(bot_frame, background="#21252B")
right_frame = Frame(bot_frame, background="#21252B")
left_frame.pack(side=LEFT, fill="both", padx = (0, 10))
right_frame.pack(side=RIGHT, fill="both", padx = (10, 0))

#################### LEFT-Frame #############################
#############################################################
#############################################################

rev_email = Entry(left_frame)
rev_email.pack(ipady=6)
rev_email.insert(0, "  Login First.")

title = Entry(left_frame)
title.pack(ipady=6, pady=(20, 0))
title.insert(0, "  Title")

send_img_d = ImageTk.PhotoImage(getImage(imagesdata.sendD()).resize((91, 35), Image.ANTIALIAS))
send_img = ImageTk.PhotoImage(getImage(imagesdata.send()).resize((91, 33), Image.ANTIALIAS))
send_img_l = ImageTk.PhotoImage(getImage(imagesdata.sendLight()).resize((91, 35), Image.ANTIALIAS))
send_img_ld = ImageTk.PhotoImage(getImage(imagesdata.sendLightD()).resize((91, 35), Image.ANTIALIAS))

send_btn = Button(left_frame,image = send_img,borderwidth = 0, cursor = "hand2", relief = "flat", command = send, highlightthickness = 0)
send_label = Label(left_frame,image = send_img_d,borderwidth = 0, cursor = "hand2", relief = "flat", highlightthickness = 0)
send_label.pack(anchor="w", pady=(20, 0))

send_btn_l = Button(left_frame,image = send_img_l,borderwidth = 0, cursor = "hand2", relief = "flat", command = send, highlightthickness = 0)
send_label_l = Label(left_frame,image = send_img_ld,borderwidth = 0, cursor = "hand2", relief = "flat", highlightthickness = 0)
#################### RIGHT-Frame #############################
#############################################################
#############################################################

text_area = Text(right_frame, height = 7)
text_area.pack()
text_area.insert(END, "  Message...")

#################### Entries Config #########################
#############################################################
#############################################################

for entry in (user_email, user_password, rev_email, title, text_area):
    entry.config(background = "#323843", foreground = place_color,highlightbackground = "#DB4437", highlightthickness = 0, font = ("Calibri", 13), relief = "flat", width = 26, insertbackground = "#ffffff", insertwidth = "1")


user_email.bind("<FocusIn>", lambda x: focusing(user_email, "  Email"))
user_password.bind("<FocusIn>", lambda x: focusing(user_password, "  Password"))
rev_email.bind("<FocusIn>", lambda x: focusing(rev_email, "  Reciever's Email"))
title.bind("<FocusIn>", lambda x: focusing(title, "  Title"))

user_email.bind("<FocusOut>", lambda x: focusOut(user_email, "  Email"))
user_password.bind("<FocusOut>", lambda x: focusOut(user_password, "  Password"))
rev_email.bind("<FocusOut>", lambda x: focusOut(rev_email, "  Reciever's Email"))
title.bind("<FocusOut>", lambda x: focusOut(title, "  Title"))

text_area.bind("<FocusIn>", lambda x: focusing(text_area, "  Message...", area = True))
text_area.bind("<FocusOut>", lambda x: focusOut(text_area, "  Message...", area = True))

top_frame.bind("<Button-1>", reset)
bot_frame.bind("<Button-1>", reset)
left_frame.bind("<Button-1>", reset)
mid_frame.bind("<Button-1>", reset)
right_frame.bind("<Button-1>", reset)
main_frame.bind("<Button-1>", reset)
color_frame.bind("<Button-1>", reset)
lg_left_frame.bind("<Button-1>", reset)
lg_right_frame.bind("<Button-1>", reset)
login_frame_l.bind("<Button-1>", reset)
login_frame_r.bind("<Button-1>", reset)
u_left_frame.bind("<Button-1>", reset)
u_right_frame.bind("<Button-1>", reset)

send_label.bind("<Button-1>", reset)
send_label_l.bind("<Button-1>", reset)
login_label.bind("<Button-1>", reset)
login_label_l.bind("<Button-1>", reset)

main_logo_d.bind("<Button-1>", reset)
main_logo_l.bind("<Button-1>", reset)

dont_show.bind("<Button-1>", setSelect)


dont_show_var.set(getSelect())

root.withdraw()
root.deiconify()
defaultColorMode()
root.mainloop()
