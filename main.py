from tkinter import ttk
from tkinter import *
import tkinter as tktools
import threading as Thread
import time
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import base64
import requests

bgcolor = '#F1E8E3'

root = Tk(screenName='ChatAI', className='phytosense')
root['background'] = bgcolor
root.geometry("1000x750")
root.columnconfigure(0, weight=1)
root.iconbitmap(r"C:\Users\User\Desktop\Sunway_Competition\logo.ico")

frame_one_style = ttk.Style()
frame_one_style.configure('Frame1.TFrame', background='#F1E8E3')


templist = []
def process_img():
    mic_button.configure(state=tktools.DISABLED)
    a = askopenfile()
    try:
        templist.append(a.name)
    except:
        mic_button.configure(state=tktools.NORMAL)
        return

    img_name.configure(text=f'{a.name} ')
    dir_stuff.configure(text=f'Encoding: {a.encoding}\nAccess mode: read-only')
    mic_button.configure(state=tktools.NORMAL)
    det_button.configure(state=tktools.NORMAL)

def scan():
    det_button.configure(state=tktools.DISABLED)
    mic_button.configure(state=tktools.DISABLED)

    dir = templist[0]
    img_list = []
    with open(dir, 'rb') as file:
        base64_pic = base64.b64encode(file.read()).decode('ascii')
        img_list.append(base64_pic)
    
    params = {
		'images': img_list
	}

    headers = {
		'Content-Type': 'application/json',
        "Api-Key" : 'sW3pB5PKYIytIh0y5GCxWRNFY6q2ZNh1P88WSvJOSXv0EsgMxW'
	}

    response = requests.post('https://api.plant.id/v2/health_assessment', json=params, headers=headers).json()
    rate = round(response["health_assessment"]["is_healthy_probability"]*100, 2)
    if rate >= 70:

        text_one = f'\n\nHealth Rating: {rate}% [Healthy]\nImage: {dir}'
    else:
        text_one = f'\n\nHealth Rating: {rate}% [Unhealthy]\nImage: {dir}'
    list_temp = []
    full_list = response["health_assessment"]["diseases"]
    for item in full_list:

        string = f'{full_list.index(item)+1}. Name: {item["name"]} | Probability: {round(item["probability"]*100, 2)}%'
        list_temp.append(string)
    disease_list = '\n'.join(list_temp)
    text_two = f"\n\nPossible diseases: \n{disease_list}"
    final_res = text_one + text_two
    mic_button.configure(state=tktools.NORMAL)
    img_name.configure(text='          [Null]          ')
    dir_stuff.configure(text='[Null]')

    log = tktools.Toplevel(root)
    log.title = 'Phytosense Diagnostics'
    log['background'] = bgcolor
    log.geometry("800x750")
    
    log_frame = ttk.Frame(log, style='Frame1.TFrame', padding=20)
    log_frame.grid()
    
    ttk.Label(log_frame, text=final_res, font=("Tw Cen MT", 16), background=bgcolor).grid(column=0, row=0)




master_page = ttk.Frame(root, style='Frame1.TFrame', padding=10)
master_page.grid()

main_page = ttk.Frame(master_page, style='Frame1.TFrame', padding=10)
main_page.grid(column=0, row=0)

action_center = ttk.Frame(master_page, style = 'Frame1.TFrame', padding=10)
action_center.grid(column=0, row=1)

action_center.columnconfigure(0, weight=3)
action_center.columnconfigure(0, weight=1)


click_btn= PhotoImage(file=r'C:\Users\User\Desktop\Sunway_Competition\Button_test.png')

plant_img = ImageTk.PhotoImage(Image.open(r"C:\Users\User\Desktop\Sunway_Competition\phytosense_banner.png").resize((700, 350)))
scan_button_image = ImageTk.PhotoImage(Image.open(r"C:\Users\User\Desktop\Sunway_Competition\Scan_Normal.png").resize((150, 33)))

ttk.Label(main_page, image=plant_img).grid(column=0, row=1)

ttk.Label(action_center, text='Choose image:', font=("Tw Cen MT", 20), background=bgcolor).grid(column=0, row=0, sticky=tktools.E)

img_name = ttk.Label(action_center, text='          [Null]          ', font=("Tw Cen MT", 20), background=bgcolor)
img_name.grid(column=1, row=0)

ttk.Label(action_center, text='Image information: ', font=("Tw Cen MT", 20), background=bgcolor).grid(column=0, row=1, sticky=tktools.NW)

dir_stuff = ttk.Label(action_center, text='[Null]', font=("Tw Cen MT", 20), background=bgcolor)
dir_stuff.grid(column=1, row=1)

mic_button = ttk.Button(action_center, text='Browse', command=lambda: process_img())
mic_button.grid(column=2, row=0, sticky = tktools.E)

frame_one_style.configure('TButton', font=('Tw Cen MT', 20), background=bgcolor, foreground='#000000')
frame_one_style.map('TButton', background=[('active', bgcolor)])
det_button = ttk.Button(action_center, command=lambda: scan(), text = 'Scan', state=tktools.DISABLED)
det_button.grid(column=2, row=2)


try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()
