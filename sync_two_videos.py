from tkinter import *
from PIL import Image, ImageTk
import cv2

######### PUT THE VIDEO PATHS HERE #########
f1 = 'data/home_toycar/c2_1.mp4'
f2 =  'data/home_toycar/c2_2.mp4'

count1 = 0 # initialise the start frame where we want to cut 
count2 = 0

#### Create Video Object ####
vo1 = cv2.VideoCapture(f1)
vo2 = cv2.VideoCapture(f2)
end1 = int(vo1.get(cv2.CAP_PROP_FRAME_COUNT))
end2 = int(vo2.get(cv2.CAP_PROP_FRAME_COUNT))

#### Tk GUI Config ####
root = Tk()

root.geometry("1000x500")

# Image will be entry of label
label1 = Label(root)
label1.grid(row=0,column=0)
label2 = Label(root)
label2.grid(row=0,column=1)

# Frame Counter
counttext1 = Label(root, text="frame: 0")
counttext1.grid(row=2,column=0)
counttext2 = Label(root, text="frame: 0")
counttext2.grid(row=2,column=1)

# Function for processing a NEW frame given a counter position in video
def next_frame(vo, label, count, counttext, max):
    print(vo.get(cv2.CAP_PROP_POS_FRAMES))
    vo.set(cv2.CAP_PROP_POS_FRAMES, count)
    
    cv2img = cv2.cvtColor(vo.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2img)
    
    # w, h = resize(img)
    # print()
    img = img.resize((400, 200))

    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)    

    counttext.config(text= f'frame {count} /{max}')

    root.update()
    root.update_idletasks()

##### Process Next Frames #####
# For video 1
def next_frame1():
    global count1
    count1 += 1
    if count1 > end1:
        count1 = end1
    next_frame(vo1, label1, count1, counttext1, end1)
def next_frame11():
    global count1
    count1 += 10
    if count1 > end1:
        count1 = end1
    next_frame(vo1, label1, count1, counttext1, end1)
def next_frame111():
    global count1
    count1 += 100
    if count1 > end1:
        count1 = end1
    next_frame(vo1, label1, count1, counttext1, end1)

# For video 2
def next_frame2():
    global count2
    count2 += 1
    if count2 > end2:
        count2 = end2
        
    next_frame(vo2, label2, count2, counttext2, end2)
def next_frame22():
    global count2
    count2 += 10
    if count2 > end2:
        count2 = end2
        
    next_frame(vo2, label2, count2, counttext2, end2)
def next_frame222():
    global count2
    count2 += 100
    if count2 > end2:
        count2 = end2
        
    next_frame(vo2, label2, count2, counttext2, end2)

##### Process Last Frames #####
# For video 1
def back_frame1():
    global count1
    count1 -= 1
    if count1 < 0:
        count1 = 0
    next_frame(vo1, label1, count1, counttext1, end1)
def back_frame11():
    global count1
    count1 -= 10
    if count1 < 0:
        count1 = 0
    next_frame(vo1, label1, count1, counttext1, end1)
def back_frame111():
    global count1
    count1 -= 100
    if count1 < 0:
        count1 = 0
    next_frame(vo1, label1, count1, counttext1, end1)

# For video 2
def back_frame2():
    global count2
    count2 -= 1
    if count2 < 0:
        count2 = 0
    next_frame(vo2, label2, count2, counttext2, end2)
def back_frame22():
    global count2
    count2 -= 10
    if count2 < 0:
        count2 = 0
    next_frame(vo2, label2, count2, counttext2, end2)
def back_frame222():
    global count2
    count2 -= 100
    if count2 < 0:
        count2 = 0
    next_frame(vo2, label2, count2, counttext2, end2)

#### Create Buttons for next and last frames ####
# Next and Last Buttons for Left video frame
frame1 = Frame(root)
frame1.grid(row=1,column=0)
next1 = Button(frame1, text ="+1", command=next_frame1)
next11 = Button(frame1, text ="+10", command=next_frame11)
next111 = Button(frame1, text ="+100", command=next_frame111)

back1 = Button(frame1, text ="-1", command=back_frame1)
back11 = Button(frame1, text ="-10", command=back_frame11)
back111 = Button(frame1, text ="-100", command=back_frame111)

next111.pack(side=RIGHT)
next11.pack(side=RIGHT)
next1.pack(side=RIGHT)
back1.pack(side=RIGHT)
back11.pack(side=RIGHT)
back111.pack(side=RIGHT)

# Next and Last Buttons for Left video frame
frame2 = Frame(root)
frame2.grid(row=1,column=1)
next2 = Button(frame2, text ="+1", command=next_frame2)
next22 = Button(frame2, text ="+10", command=next_frame22)
next222 = Button(frame2, text ="+100", command=next_frame222)

back2 = Button(frame2, text ="-1", command=back_frame2)
back22 = Button(frame2, text ="-10", command=back_frame22)
back222 = Button(frame2, text ="-100", command=back_frame222)

next222.pack(side=RIGHT)
next22.pack(side=RIGHT)
next2.pack(side=RIGHT)
back2.pack(side=RIGHT)
back22.pack(side=RIGHT)
back222.pack(side=RIGHT)



#### Save Start Cut ####
def cut_start1():
    global count1
    print(vo1.get(cv2.CAP_PROP_FPS))
def cut_end1():
    global count1
    print(count1)

def cut_start2():
    global count2
    print(vo1.get(cv2.CAP_PROP_FPS))


def cut_end2():
    global count2
    print(count2)

# Create Widget for this
frame1_ = Frame(root)
frame1_.grid(row=3,column=0)
cstart1 = Button(frame1_, text ="cut start", command=cut_start1)
cend1 = Button(frame1_, text ="cut end", command=cut_end1)
cend1.pack(side=RIGHT)
cstart1.pack(side=RIGHT)

frame2_ = Frame(root)
frame2_.grid(row=3,column=1)
cstart2 = Button(frame2_, text ="cut start", command=cut_start2)
cend2 = Button(frame2_, text ="cut end", command=cut_end2)
cend2.pack(side=RIGHT)
cstart2.pack(side=RIGHT)

#### Save End Cut ####


def resize(img, target_width=500):
    w, h = img.size
    factor = float(target_width/w)
    height = int(h*factor)
    return target_width, height

def initialise():
    cv2img1 = cv2.cvtColor(vo1.read()[1], cv2.COLOR_BGR2RGB)
    img1 = Image.fromarray(cv2img1)
    
    cv2img2 = cv2.cvtColor(vo2.read()[1], cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(cv2img2)

    img1 = img1.resize((400, 200))
    img2 = img2.resize((400, 200))
    

    imgtk1 = ImageTk.PhotoImage(image=img1)
    imgtk2 = ImageTk.PhotoImage(image=img2)

    label1.imgtk = imgtk1
    label1.configure(image=imgtk1)
    label2.imgtk = imgtk2
    label2.configure(image=imgtk2)


# Run Main TK App
initialise()
root.mainloop()

# vo1.set(cv2.CAP_PROP_FRAME_COUNT, 100)
# ret, frame = cap.read()
# cv2.imwrite("path_where_to_save_image", frame)