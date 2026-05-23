def center_menu(master, menu, event=None):
    if event:
        x = event.x_root - master.winfo_rootx()
        y = event.y_root - master.winfo_rooty()
        menu.place(x=x, y=y, anchor="center")
    else:
        menu.place(relx=0.5, rely=0.5, anchor="center")

    menu.lift()