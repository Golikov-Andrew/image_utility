import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter.filedialog import askdirectory
from PIL import Image
import pathlib

root = tk.Tk()
root.title('Image Utility')

CHOOSE_SRC_IMG_FOLDER = "Choose Source Image Folder"
CHOOSE_DEST_IMG_FOLDER = "Choose Destination Image Folder"

canvas = tk.Canvas(root, width=800, height=350)
canvas.pack()

choosen_image_dir_var = tk.StringVar(canvas)
choosen_image_dir_var.set(CHOOSE_SRC_IMG_FOLDER)
lbl_image_dir = tk.Label(canvas, textvariable=choosen_image_dir_var).place(x=50, y=110)

choosen_dest_image_dir_var = tk.StringVar(canvas)
choosen_dest_image_dir_var.set(CHOOSE_DEST_IMG_FOLDER)
lbl_dest_image_dir = tk.Label(canvas, textvariable=choosen_dest_image_dir_var).place(x=50, y=200)


def func():
    if is_update_image.get() == 1:
        btn_choose_dest_image_folder['state'] = 'normal'
    else:
        btn_choose_dest_image_folder['state'] = 'disable'


is_update_image = tk.IntVar()
lbl_update_static_data_images = tk.Checkbutton(canvas, text="Move target images to destination folder ?",
                                               variable=is_update_image, command=func).place(x=50, y=145)


def log(filename, msg):
    print(msg)
    with open(filename, 'a') as lf:
        lf.write(msg + '\n')


def get_list_of_non_square_images():
    src_dir = choosen_image_dir_var.get()
    if src_dir == CHOOSE_SRC_IMG_FOLDER:
        status_label_var.set(f'{CHOOSE_SRC_IMG_FOLDER}!')
        return
    dest_dir = None
    if is_update_image.get() == 1:
        if choosen_dest_image_dir_var.get() == CHOOSE_DEST_IMG_FOLDER:
            status_label_var.set(f'FAIL: {CHOOSE_DEST_IMG_FOLDER} or uncheck this parameter')
            return
        else:
            dest_dir = choosen_dest_image_dir_var.get()
    filenames = os.listdir(src_dir)
    total = len(filenames)
    cnt = 0
    new_report_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + f'__target_images.txt'
    new_log_name = new_report_name.replace('.txt', '.log')

    with open(os.path.join('.', new_report_name), 'w') as f:
        for filename in filenames:
            cnt += 1
            src_path = os.path.join(src_dir, filename)
            if os.path.isdir(src_path):
                log(new_log_name, f'There is folder:\t{src_path}')
                continue
            sfx = pathlib.Path(src_path).suffix
            if sfx not in ('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG'):
                log(new_log_name, f'There is no image:\t{src_path}')
                continue
            im = Image.open(src_path)

            print(filename, im.width, im.height)
            if im.width != im.height:
                f.write(f'{filename.split(".")[0]}\n')
                if is_update_image.get() == 1:
                    dest_path = os.path.join(dest_dir, filename)
                    im.close()
                    shutil.move(src_path, dest_path)
            status_label_var.set(f'{cnt}/{total}')
            root.update_idletasks()
    print(f'DONE! New report file: ./{new_report_name}')
    status_label_var.set(f'DONE! New report file: ./{new_report_name}')


def choose_image_dir():
    dirname = askdirectory()
    print('src image dir:', dirname)
    if dirname:
        choosen_image_dir_var.set(dirname)


def choose_dest_image_dir():
    dirname = askdirectory()
    print('dest image dir:', dirname)
    if dirname:
        choosen_dest_image_dir_var.set(dirname)


btn_choose_source_image_folder = tk.Button(text=CHOOSE_SRC_IMG_FOLDER, command=choose_image_dir,
                                           bg='brown', fg='white')
btn_choose_source_image_folder.place(x=50, y=80)

btn_choose_dest_image_folder = tk.Button(text=CHOOSE_DEST_IMG_FOLDER, command=choose_dest_image_dir,
                                         bg='brown', fg='white')
btn_choose_dest_image_folder.place(x=50, y=170)
btn_choose_dest_image_folder['state'] = 'disable'

btn_run_func = tk.Button(text='Get List of non Square Images',
                         command=get_list_of_non_square_images, bg='brown', fg='white')
btn_run_func.place(x=50, y=240)

status_label_var = tk.StringVar(canvas)
status_label_var.set('')
status_label = tk.Label(canvas, textvariable=status_label_var).place(x=50, y=270)

root.mainloop()
