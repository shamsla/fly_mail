from tkinter import *
from tkinter import ttk, scrolledtext
import threading, smtplib

# frame : main_frame of parent window (root)
# bar_frame : frame containing prog.bar
# bar : main prog.bar
# master : bug_win (bugReport window)
# root : parent window (Toplevel)
# terminator : Function (execute) after sendReport execution
# speed : prog.bar speed
# bugbool : (BOOLEAN) indicates the submission of report {True|False}

def inRaise(frame, bar_frame): # raise the bar_frame
    frame.pack_forget()
    bar_frame.pack()

def outRaise(frame, bar_frame): # hide the bar_frame
    bar_frame.pack_forget()
    frame.pack()

def startThread(master, name, title, message,root, frame, bar_frame, bar, terminator, speed): # starts the thread for progressbar and sendReport (function)
    global thread
    inRaise(frame, bar_frame) # bar_frame will raise
    thread = threading.Thread(target = sendReport, args = (master, name, title, message, terminator))
    thread.start() # thread starts here
    bar.start(speed) # prog.bar starts here with speed {default:20}
    root.after(20, lambda:checkThread(root, frame, bar_frame, bar)) # checkThread function call here
    
def checkThread(root, frame, bar_frame, bar): # terminate everything after the sendReport (function) execution.
    if thread.is_alive(): # checks: is the thread alive or not
        root.after(20, lambda:checkThread(root, frame, bar_frame, bar)) # recurssion after evrey 20ms
    else:
        bar.stop() # bar will stop here
        outRaise(frame, bar_frame) # responsible for terminating the bar_frame
        root.focus_set() # focus set to root (parent window)
    

def sendReport(master, name, title, message, terminator): # (main function) report send from here
    global bugbool # bug_win will be terminate when user click on send button
    master.destroy()
    try:
        connect = smtplib.SMTP("smtp.gmail.com", 587)
        connect.ehlo()
        connect.starttls()
        connect.login("Put Your Email Here ...", "Put Your Password Here ...")
        connect.sendmail("Put Your Email Here ...", "Put Your Email Here ...", (f"subject: B:Fly Mail-{name.capitalize()}\n\nFly Mail,\n\t{name.capitalize()}\n\tBug: {title.capitalize()}\n\n\t{message}"))
        connect.quit()
        bugbool = True
        if terminator != None: # terminator function calls from here
            terminator()
        master.destroy()
    except:
        bugbool = False
        if terminator != None:
            terminator()
        

def proceed(master, nEntry, tEntry, mEntry,root, frame, bar_frame, bar, terminator, speed): # evaluates the entries and proceed the startThread (function)
    name = nEntry.get()
    title = tEntry.get()
    message = mEntry.get(1.0, END)
    if len(name) == 0 or len(title) == 0 or len(message) == 1 or message == "** Please Write About Bug **\n" or name == "** Enter Name | Email **" or title == "** Enter Title **":
        if len(name) == 0:
            nEntry.insert(0, "** Enter Name | Email **")
        elif len(title) == 0:
            tEntry.insert(0, "** Enter Title **")
        elif len(message)  == 1:
            mEntry.insert(END, "** Please Write About Bug **")
    else:
        empty_menu = Menu(root)
        root.config(bg="#fafafa", menu = empty_menu) # for removing the menu from toplevel root window (main send main program window)
        root.update_idletasks()


        startThread(master, name, title, message,root, frame, bar_frame, bar, terminator, speed) # proceeds from here

def focusInB(entry, name): # when user get in focus
    if name != "messEntry":
        if entry.get() and entry.get() in ("** Enter Name | Email **", "** Enter Title **"):
            entry.delete(0, END)
    else:
        if entry.get(1.0,END) == "** Please Write About Bug **\n":
            entry.delete(1.0,END)

def bug(root,main_frame, win_width, win_height, wait_image, logo = None, terminator = None, p_pad = 0, p_speed = 20, p_length = 200): # child window

    '''
Required:
    root (root window), main_frame (already packed frame), win_width, win_height

    ** win_width &_height (for aligning window in center)

important:
    terminator (function which  be execute after email sending (or mail not sent)), p_pad

other:
    logo (function), p_font_size, p_speed, p_length

*** Must Use bug.bugbool Variable In Your Terminator Function.
    '''

    bug_win = Toplevel(root)
    bug_win.title("Report Bug")
    bug_win.grab_set()
    bug_win.focus_set()

    bug_win.geometry(f"625x510+{(bug_win.winfo_screenwidth()//2)-(win_width//2)+(win_width-500)//2}+{(bug_win.winfo_screenheight()//2)-((win_height//2)+(win_height//15))+((win_height//4)//2)-3}")

    bug_win.minsize(width=500, height=420)
    bug_win.maxsize(width=500, height=420)
    bug_win.update_idletasks()

    bug_win.geometry(f"625x510+{(bug_win.winfo_screenwidth()//2)-(win_width//2)+(win_width-500)//2}+{(bug_win.winfo_screenheight()//2)-((win_height//2)+(win_height//15))+((win_height//4)//2)}")

    ######################## Frames ##########################
    ###########################################################
    ###########################################################
    ###########################################################

    bar_frame = Frame(root) # new bar creates from here
    Label(bar_frame, image = wait_image, borderwidth = 0, highlightthickness = 0).pack(pady = (p_pad,5))
    bar = ttk.Progressbar(bar_frame, style="red.Horizontal.TProgressbar", length = p_length, mode = "indeterminate")
    bar.pack(ipady=3, pady = (5, 0)) # prog.bar generates here

    top_frame = Frame(bug_win)
    top_frame.pack(pady = (20,0))

    bot_frame = Frame(bug_win)
    bot_frame.pack(pady = (25,0))

    ######################## T Frame ##########################
    ###########################################################
    ###########################################################
    ###########################################################

    Label(top_frame, image = logo, bg="#fafafa").pack()
    
    ######################## B Frame ##########################
    ###########################################################
    ###########################################################
    ###########################################################

    t_bot_frame = Frame(bot_frame)
    t_bot_frame.pack()

    m_bot_frame = Frame(bot_frame)
    m_bot_frame.pack(pady = (20,0))

    b_bot_frame = Frame(bot_frame)
    b_bot_frame.pack(pady = (20,0), anchor = "e")

    ######################## SUB Frames ##########################
    ###########################################################
    ###########################################################
    ###########################################################

    lt_bot_frame = Frame(t_bot_frame)
    lt_bot_frame.grid(row=1, column = 1, padx = (0,7))

    rt_bot_frame = Frame(t_bot_frame)
    rt_bot_frame.grid(row=1, column = 2, padx = (7,0))

    Label(lt_bot_frame, text = "NAME | EMAIL", bg="#fafafa").pack(anchor = "w", pady = (0, 2))
    name_e = Entry(lt_bot_frame, width=23)
    name_e.pack(ipady = 5)

    Label(rt_bot_frame, text = "ENTER TITLE", bg="#fafafa").pack(anchor = "w", pady = (0, 2))
    title_e = Entry(rt_bot_frame, width=23)
    title_e.pack(ipady = 5)
    
    Label(m_bot_frame, text = "WRITE ABOUT BUG", bg="#fafafa").pack(anchor = "w",padx = (16, 0), pady = (0, 2))
    message_e = scrolledtext.ScrolledText(m_bot_frame, width = 47, height = 8)
    message_e.pack(padx = (16, 0), ipadx = 5)

    for entry in (name_e, title_e, message_e):
        entry.config(background = "#e3e3e3", foreground = "#000000",highlightbackground = "#DB4437", highlightthickness = 0, font = ("Calibri", 13), relief = "flat", insertbackground = "#000000", insertwidth = "1")

    send_btn = ttk.Button(b_bot_frame, cursor = "hand2", text = "SEND", width = 15, command = lambda: proceed(bug_win, name_e, title_e, message_e,root, main_frame, bar_frame, bar, terminator, p_speed)) # proceed function call from here
    send_btn.pack(ipady = 5, padx = (0, 16))

    for frame in (bug_win, top_frame, bot_frame, rt_bot_frame, lt_bot_frame, b_bot_frame, bar_frame, m_bot_frame, t_bot_frame):
        frame.config(bg="#fafafa")

    message_e.bind("<FocusIn>", lambda x: focusInB(message_e, "messEntry"))
    name_e.bind("<FocusIn>", lambda x: focusInB(name_e, "name"))
    title_e.bind("<FocusIn>", lambda x: focusInB(title_e, "title"))
    
    bug_win.mainloop()
