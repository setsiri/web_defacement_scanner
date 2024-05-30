import os
import sys
import tkinter as tk
from bs4 import BeautifulSoup, builder
from tkinter import filedialog
from tkinter import messagebox
import urllib.request
from urllib.parse import urlparse
from datetime import datetime

import csv
import requests
import time
import socket
from threading import Thread
from tkinter import ttk

#* golbal variable
running =False
stop = False
thread = None
keepHistory = True
Domain_URL = ""
"""
running fetch function
"""
def run():
    #*check if url is valid
    website_url_sub1 = URL_Entry.get()
    if not (website_url_sub1.startswith("https://") or website_url_sub1.startswith("http://")):
        website_url_sub1 =  "https://" +website_url_sub1
    if(URL_Entry.get() == "" or not is_valid_domain(urlparse(website_url_sub1).netloc)): 
        messagebox.showerror("URL not valid","URL not valid or domain not found.")
        return
    global Domain_URL
    Domain_URL = website_url_sub1
    #*clear the home screen
    title.place_forget()
    by.place_forget()
    internet_text.place_forget()
    Internet_Label.place_forget()
    URL_text.place_forget()
    URL_Entry.place_forget()
    Scan_limit_text.place_forget()
    Scan_Limit_Entry.place_forget()
    keyword.place_forget()
    text_frame.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    progress.set(0)
    
    #*show running screen
    result_title.place(x=150, y=10)
    result_Label.place(x=150, y=50)
    internet_text.place(x=150, y=85)
    Internet_Label.place(x=235, y=85)
    config_text.place(x=150, y=110)
    result_frame.place(x=60, y=170, width=600, height=250)
    progress_Time.place(x=450, y=110)
    button2.place(x=240, y=440)
    switch_frame.place(x=335, y=440)
    progressbar.place(x=60, y=145, width=600, height=20)
    config_text.config(text="URL : "+str(URL_Entry.get())+" | Scan limit :"+str(Scan_Limit_Entry.get()))

    #*start the thread and run the function
    rateLimit=  int(Scan_Limit_Entry.get()) if not (Scan_Limit_Entry.get() == 'No Limit' or Scan_Limit_Entry.get() == '') else 0
    global running,thread
    running = True
    thread = Thread(target=find_defacement,args=(website_url_sub1,"",rateLimit,))
    thread.start()

"""
return to home screen
"""
def back():
    global running,stop,keepHistory
    running = False
    stop = False
    keepHistory = True
    result_title.place_forget()
    result_Label.place_forget()
    internet_text.place_forget()
    Internet_Label.place_forget()
    config_text.place_forget()
    result_frame.place_forget()
    button2.place_forget()
    button5.place_forget()
    progress_Time.place_forget()
    button6.place_forget()
    progressbar.place_forget()
    
    title.place(x=225,y=10)
    by.place(x=285,y=40)
    internet_text.place(x=130,y=85)
    Internet_Label.place(x=225,y=85)
    URL_text.place(x=185,y=115)
    URL_Entry.place(x=225,y=115)
    Scan_limit_text.place(x=155, y=145)
    Scan_Limit_Entry.place(x=225, y=145)
    keyword.place(x=155,y=180)
    text_frame.place(x=225, y=180, width=150, height=275)
    button1.place(x=410,y=180)
    button2.place(x=410,y=215)
    button3.place(x=410,y=250)
    button4.place(x=410,y=430)
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.config(state=tk.DISABLED)
    
    """
    check if url is valid

    Returns:
        boolean: True if url is valid, False otherwise
    """
def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

"""
check if keyword.txt file exist if not create one.
Effect:
    -show mwssage box
"""
def open_file():
        try:
            with open('keyword.txt', 'r', encoding='utf-8') as file:
                content = file.read()
                text.delete(1.0, tk.END)
                text.insert(tk.END, content)
        except FileNotFoundError:
            open('keyword.txt', "x", encoding='utf-8')
            messagebox.showinfo("File not found","keyword.txt not found. created keyword.txt on this direction.")

"""
save keyword in home screen in to the keyword.txt file
Effect : keyword.txt will be created if not exist
"""
def save_file():
        content = text.get(1.0, tk.END)
        try:
            with open('keyword.txt', 'w', encoding='utf-8') as file:
                file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

#* ฟังก์ชั่นเพื่อตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
def check_internet_connection():
    try:
        # พยายามเชื่อมต่อไปยัง Google
        urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except:
        return False

#* ฟังก์ชั่นสำหรับอัพเดตสถานะการเชื่อมต่อ
def update_status():
    if check_internet_connection():
        Internet_Label.config(text="Connected", fg="green")
    else:
        Internet_Label.config(text="Disconnected", fg="red")
    # ตั้งค่าให้ฟังก์ชั่นนี้ถูกเรียกอีกครั้งใน 3 วินาที
    root.after(3000, update_status)

#* function that return the program directory
def get_program_directory():
    # หา path ของโฟลเดอร์ที่โปรแกรมนี้อยู่
    program_path = os.path.dirname(sys.argv[0])
    return program_path
#* fuction that open History folder
def open_History_folder(program_path):
    # ระบุ path ของโฟลเดอร์ที่ต้องการเปิด
    folder_path = program_path+r"\History"  # เปลี่ยนเป็น path ที่ต้องการเปิด

    # เปิดโฟลเดอร์ด้วยโปรแกรมเริ่มต้นของระบบ Windows
    os.startfile(folder_path)

#* function that open Result file when finish
def open_Result_file():
    global Domain_URL
    current_date = datetime.now().date()
    os.startfile(f".\\History\\{str(urlparse(Domain_URL).netloc)}-{current_date}.txt")

#* check is rate limit is number
def validate_entry(new_value):
    if new_value == "No Limit" or new_value == "":
        return True
    try:
        int(new_value)
        return True
    except ValueError:
        return False


def on_focus_in(event):
    if event.widget.get() == "No Limit":
        event.widget.delete(0, tk.END)

def on_focus_out(event):
    if event.widget.get() == "":
        event.widget.insert(0, "No Limit")

#* GUI
root = tk.Tk()
root.title("Open History Folder")
root.geometry('700x500+350+100')

bar = 0

title = tk.Label(root, text='Web Defacetion Scanner', font=('Arial', 16))
title.place(x=225,y=10)
by = tk.Label(root, text='by ITSC Intern 2024', font=('Arial', 10))
by.place(x=285,y=40)

internet_text = tk.Label(root, text="Internet Status :")
internet_text.place(x=130,y=85)
Internet_Label = tk.Label(root, text="Checking . . .")
Internet_Label.place(x=225, y=85)

URL_text = tk.Label(root, text="URL :")
URL_text.place(x=185,y=115)
URL_Entry = tk.Entry(root, width=45)
URL_Entry.place(x=225,y=115)

Scan_limit_text = tk.Label(root, text="Scan limit :")
Scan_limit_text.place(x=155, y=145)
validate_cmd = root.register(validate_entry)
Scan_Limit_Entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, '%P'), width=45)
Scan_Limit_Entry.insert(0, "No Limit")
Scan_Limit_Entry.bind("<FocusIn>", on_focus_in)
Scan_Limit_Entry.bind("<FocusOut>", on_focus_out)
Scan_Limit_Entry.place(x=225, y=145)


keyword = tk.Label(root, text="Keyword :")
keyword.place(x=155,y=180)
# Frame for Text Editor
text_frame = tk.Frame(root)
text_frame.place(x=225, y=180, width=150, height=275)
# Text Widget for displaying and editing the content
text = tk.Text(text_frame, wrap='word')
text.pack(fill=tk.BOTH, expand=True)

# Create three buttons
button1 = tk.Button(root, text="Save Keyword", command=save_file)
button1.place(x=410,y=180)
button2 = tk.Button(root, text="View History", command=lambda: open_History_folder(get_program_directory()))
button2.place(x=410,y=215)
button3 = tk.Button(root, text="Start Scan", command=run)
button3.place(x=410,y=250)
button4 = tk.Button(root, text="Exit Program", command=root.quit)
button4.place(x=410,y=430)


button5 = tk.Button(root, text="Back", command=back)
button5.place_forget()


result_title = tk.Label(root, text="Web Defacetion Scanner by ITSC Intern 2024")
result_title.place_forget()

result_Label = tk.Label(root, text="Scan processing", font=('Arial', 16))
result_Label.place_forget()

config_text = tk.Label(root,text="URL : "+str(URL_Entry.get())+" | Scan limit :"+str(Scan_Limit_Entry.get()))


result_frame = tk.Frame(root)
result_frame.place_forget()

result_text = tk.Text(result_frame, wrap='word')
result_text.pack(fill=tk.BOTH, expand=True)

progress_Time = tk.Label(root, text="Estimate Time: ")
progress_Time.place_forget()

switch_frame = tk.Frame(root)
switch_frame.place_forget()

"""fuction that pause program from running
"""
def pausing():
    global running
    running = False
def stopping():
    global stop ,keepHistory
    pausing()
    if messagebox.askyesno("Confirmation", "Are you sure you want to stop?\nThis will end this process."):
        if not messagebox.askyesno("Confirmation","keep history of current processed?"): 
            keepHistory = False
        stop = True
    else: resuming()

"""function that resume program from pausing
"""
def resuming():
    global running
    running = True

switch_variable = tk.StringVar(value="resume")
pause_button = tk.Radiobutton(switch_frame, text="pause", variable=switch_variable,
                            indicatoron=False, value="pause", width=8,command=pausing)
resume_button = tk.Radiobutton(switch_frame, text="resume", variable=switch_variable,
                            indicatoron=False, value="resume", width=8,command =resuming)
stop_button = tk.Button(switch_frame,text="stop", command=stopping)
pause_button.pack(side="left")
resume_button.pack(side="left")
stop_button.pack(side="left")
button6 = tk.Button(root, text="View Result", command=open_Result_file)
button6.place_forget()

progress = tk.IntVar()
progressbar = ttk.Progressbar(root, variable=progress)

root.after(0, update_status)
root.after(0, open_file)

"""
write result on file in History depending on domain
Effect:
    -Create history folder if not exist
    -Create and write result file
"""
def write_result(Domain,url_found,founding,url_notfound,url_cannot_fetch):
    os.makedirs("./History", exist_ok=True)
    current_date = datetime.now().date()
    f = open(f"./History/{str(urlparse(Domain).netloc)}-{current_date}.txt", "w", encoding='utf-8')
    f.write(f"{str(datetime.now().time())}\n")
    f.write(f"summary: {len(url_found)+ len(url_notfound)+len(url_cannot_fetch) }\n")
    f.write(f"\n[Defacement detected {len(url_found)}]\n")
    if(not url_found): f.write("-\n")
    for i in range(len(url_found)):
        f.write(f"{url_found[i]}\n")
        f.write(f"found: {founding[i]}\n")

    f.write(f"[No defacement detected {len(url_notfound)}]\n")
    if(not url_notfound): f.write("-\n")
    for i in url_notfound:
        f.write(f"{i}\n")
    f.write(f"[Cannot fetch URL {len(url_cannot_fetch)}]\n")
    if(not url_cannot_fetch): f.write("-\n")
    for i in url_cannot_fetch:
        f.write(f"{i}\n")
    f.write("------------------------------------------------------------------")
    print("Finish")

"""
fetch website content from url 
Effect:
    print string in result_text
Parameters:
    url (string): website url
Returns:
    String: HTML content of the website
"""
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else: #! cannot access to website
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END,f"Failed to fetch website content. Status code: {response.status_code}, on the website {url}\n")
            result_text.see(tk.END)
            result_text.config(state=tk.DISABLED)
            

            return None
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END,f"Error fetching website content: on the website {url}\n", e)
        result_text.see(tk.END)
        result_text.config(state=tk.DISABLED)
        return None

"""
    This fuction will create keyword.txt if not exist and ignore running 
    if keyword.txt already exist it will use keyword from keyword.txt each line
    to find defacement on HTML content from url and create file to keep history
    Effect:
        -print string in result_text
        -create keyword.txt if not exist
        -read keyword from keyword.txt
    Parameters:
        url (string): website url
        url_main_sub (string): path url of the website DEFAULT: ''
        rateLimit (int): number of request per second
"""
def find_defacement(url,url_main_sub,rateLimit=3):
    #* Check HTML content variable
    found =[]
    paths = ['']
    url_found =[]
    founding=[]
    url_notfound =[]
    url_cannot_fetch = []
    #* Passive scan variable
    fetched =set()
    fetch_domain = url.strip()
    sub_fetch_domain = urlparse(url).path
    isNotFinish = True
    paths = [fetch_domain]
    limit =1
    estimate_time=0
    
    root.update()
    
    try:
        #*if keyword.txt not exits create one
        open('keyword.txt', "x")
        print('keyword.txt does not exits.\nNow it was created please write keyword in file')
        return
    except FileExistsError:
        while(isNotFinish and (limit <= rateLimit or rateLimit==0)):
            #*User click pause
            while not running:
                time.sleep(0.1)
                if stop : break
            if stop : break
            result_text.update()
            #*Progress bar
            progressbar.step(bar+(99.9/float(Scan_Limit_Entry.get()) if not (Scan_Limit_Entry.get() == 'No Limit' or Scan_Limit_Entry.get() == '') else 0))
            progress_Time.config(text=f"Estimate time: {round(estimate_time, 2)} sec")
            start_time = time.time()
            #*check is it still has url in paths
            if len(paths) ==  0: break
            else : fetch_url = paths.pop(0)
            found =[]
            website_content = fetch_website_content(fetch_url)
            fetched.add(fetch_url)
            if(website_content == None ): 
                url_cannot_fetch.append(fetch_url)
                end_time = time.time()
                elapsed_time = end_time - start_time
                estimate_time -= elapsed_time
                limit+=1
                continue
            try:
                soup = BeautifulSoup(website_content, 'html.parser')
            except builder.ParserRejectedMarkup:
                continue
            links = soup.find_all('a', href=True)
            with open('keyword.txt','r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                #*get keyword from keyword.txt for each line
                for keyword in csv_reader:
                    if len(keyword)==0 : continue
                    if soup.find(string=lambda text: text and keyword[0].strip() in text):
                        found.append(keyword[0].strip())
                if(found) :
                    result_text.config(state=tk.NORMAL)
                    result_text.insert(tk.END,f"Defacement detected on the website: {fetch_url}\n")
                    result_text.insert(tk.END,f'summary keyword that were found : {found}\n')
                    url_found.append(fetch_url)
                    founding.append(found)
                    result_text.see(tk.END)
                    result_text.config(state=tk.DISABLED)
                else : 
                    result_text.config(state=tk.NORMAL)
                    result_text.insert(tk.END,f"No defacement detected on the website: {fetch_url}\n")
                    url_notfound.append(fetch_url)
                    result_text.see(tk.END)
                    result_text.config(state=tk.DISABLED)
            for link in links:
                path = link['href']
                path =path.strip()
                
                if(path == None) : continue
                if (len(path) > 1):
                    if (path.startswith(sub_fetch_domain) and not sub_fetch_domain=="" and not sub_fetch_domain=="/"):
                        sub_path =path
                        sub_path = sub_path[len(sub_fetch_domain):]
                        path = url+sub_path
                    elif(path.startswith('?')):
                        path = url+'/'+path
                    elif(path.startswith(url)):
                        path = path
                    elif(path.startswith('/')):
                        path = url+path
                    # elif(path.startswith('.')): #!unfinish
                    #     temp_url= fetch_url
                    #     period_count = len(path) - len(path.lstrip('.'))
                    #     temp_url= temp_url.split('/')
                    #     parts=path.lstrip('.').split('/')
                    #     if period_count == 1:
                    #         temp_url = temp_url[:-period_count]
                    #     elif period_count == 2:
                    #         temp_url = url.rstrip(sub_fetch_domain).split('/')
                    #     if parts:
                    #         temp_url.append(parts[-1])
                    #     path = '/'.join(temp_url)
                    elif ('.php' in path) and not (('https://' in path) or ('http://' in path)):
                        path = url+'/'+path
                    else :continue
                    if not (path.endswith('.pdf') or path.endswith('.jpg') or path.endswith('.png')or 
                            path.endswith('.mp4') or path.endswith('.mp3') or path.endswith('.jpeg')or
                            path.endswith('.jpg') or path.endswith('.doc') or path.endswith('.xlsx')or
                            path.endswith('.jfif') or path.endswith('.JPG')):
                        if  ((path not in paths)and( path not in fetched)):
                            paths.append(path)
            limit += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            estimate_time = elapsed_time*len(paths) if len(paths)<limit or rateLimit==0 else elapsed_time*(rateLimit-limit+1)
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END,f"Finish")
        result_text.see(tk.END)
        result_text.config(state=tk.DISABLED)
        progress_Time.config(text="Finish")
        progress.set(99.9)
        messagebox.showinfo("Alert", "Process Finish")
        if keepHistory :write_result(url,url_found,founding,url_notfound,url_cannot_fetch)
    
    switch_frame.place_forget()
    button5.place(x=425, y=440)
    button6.place(x=335, y=440)


root.mainloop()