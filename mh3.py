##Massey Hacks 7 - Arfaa Rashid
##commenting code? what's that?

from pygame import *
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename

screen = display.set_mode((1050,600))
screen.fill((255,255,255))

root = Tk()     
root.withdraw()

shlist = []

def op():       #select image of unlabeled sheet
    result = askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")])
    sheet = image.load(result)
    shlist.append(sheet)                #added to list so it can be accessed later
    screen.blit(sheet,(0,100))
    
step = 1

font.init()
style = font.SysFont("Times New Roman", 20)


def step2(r):
    notes = "FEDCBAGFEDC"
    interval = r[3]//8
    start = r[1]-interval
    for i in range(11):                 #lines and spaces from F5 to middle C
        find_note((start+i*interval),notes[i])

    export()
 

def find_note(y,note):      #uses average color in rectangle to determine whether/where the notes are on that line or space
    rx,ry = 36,28           #approx length and width of notehead.
    x = 150                 #where notes begin               
    black = False
    found = False
        
    while True:
        rect = (x,y,rx,ry)
        
        col = transform.average_color(screen,rect)
        if col[0] < 75 and col[1] < 75 and col[2] < 75:     #If the avg col is low, there's a lot of black, so a note is there
            if black == False:                              #so note only found once
                found = True
            else:
                found = False
            black = True
        else:
            black = False

        if found:
            draw_note(x,note)

        if x == 1049:       #end of screen
            break
        else:
            x += 1

        display.flip()


def draw_note(x,note):          #draw letter corresponding to note under staff
    pic = style.render(note, True, (0,0,0))
    screen.blit(pic,(x,400))
    return


def export():               #export labeled image
    image.save(screen,"notes1.jpg")
    time.wait(10)
    screen.fill((0,0,0))
    

def drag(r,dx,dy,omx,omy):
    mx,my = mouse.get_pos()
    nx,ny = omx-dx,omy-dy
    
    return Rect(nx,ny,r[2],r[3])

def resize(r,dx,dy,direc):

    x = r[0]
    y = r[1]
    ndx = r[2]
    ndy = r[3]
    
    if direc == "left":
        if ndx > 2:
            ndx -= 2
            
    elif direc == "right":
        if ndx + 2 < 1050:
            ndx += 2

    elif direc == "top":
        if ndy > 2:
            ndy -= 2

    elif direc == "bottom":
        if ndy + 2 < 600:
            ndy += 2

    return Rect(x,y,ndx,ndy)
        

r = Rect(10,10,100,20)              #Rect used to line up with staff to calculate where the lines and spaces are

left = Rect(465,50,40,40)           #buttons used to resize the Rect
right = Rect(545,50,40,40)
top = Rect(505,10,40,40)
bottom = Rect(505,90,40,40)
handles = [left,right,top,bottom]

button = Rect(940,30,80,30)         #proceed to next step
opbutton = Rect(940,70,80,30)

omx,omy = 0,0
running = True
while running:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            dx,dy = mx-r[0],my-r[1]
        if e.type == QUIT:
            running = False

    if step == 1:
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if len(shlist) >0:
            screen.blit(shlist[0],(0,0))
        else:
            screen.fill((255,255,255))

        if mb[0]:
            if handles[0].collidepoint(mx,my):
                r = resize(r,dx,dy,"left")
            elif handles[1].collidepoint(mx,my):
                r = resize(r,dx,dy,"right")
            elif handles[2].collidepoint(mx,my):
                r = resize(r,dx,dy,"top")
            elif handles[3].collidepoint(mx,my):
                r = resize(r,dx,dy,"bottom")
            elif r.collidepoint(mx,my):
                r = drag(r,dx,dy,omx,omy)

        draw.rect(screen,(255,0,0),r,3)

        for handle in handles:
            draw.rect(screen,(0,0,255),handle,2)

        plus_pic = style.render("+", True, (0,0,0))
        screen.blit(plus_pic,(560,60))
        screen.blit(plus_pic,(520,100))
        minus_pic = style.render("-", True, (0,0,0))
        screen.blit(minus_pic,(480,60))
        screen.blit(minus_pic,(520,20))

        info = style.render("Line up the box with the staff. Drag and use the +/-.", True, (0,0,0))
        screen.blit(info,(20,450))

        if button.collidepoint(mx,my):
            sz = 4
            if mb[0] and len(shlist)>0:
                step = 2
                screen.blit(shlist[0],(0,0))
                step2(r)   
        else:
            sz = 2
        draw.rect(screen,(0,255,0),button,sz)
        next_pic = style.render("Next", True, (0,0,0))
        screen.blit(next_pic,(945,35))

        if opbutton.collidepoint(mx,my) and len(shlist) == 0:
            sz2 = 4
            if mb[0] == 1:
                op()
        else:
            sz2 = 2
        draw.rect(screen, (0,255,0),opbutton,sz2)
        op_pic = style.render("Open", True, (0,0,0))
        screen.blit(op_pic,(945,75))

        omx,omy = mx,my

    display.flip()
quit()









