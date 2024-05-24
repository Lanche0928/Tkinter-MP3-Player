#importando as bibliotecas necessárias
from pygame import mixer
from tkinter import *
import tkinter.font as font
from  tkinter import filedialog
import os

#adiciona músicas na lista
def addSongs():
    #retorna um lista músicas selecionadas
    temp_song = filedialog.askopenfilenames(initialdir="C:/Users/Pichau/Desktop/Imagens/Musics/", title="Choose one or more songs", filetypes=(("mp3 Files","*.mp3"),))
    #faz uma iteração na lista, passando por cada item dela e retira o ".mp3" do nome do arquivo
    for s in temp_song:
        path = s 
        basename = os.path.basename(path)
        songs_list.insert(END, basename)

#exclui uma música da lista
def deleteSong():
    curr_song = songs_list.curselection()
    songs_list.delete(curr_song[0])

#variável global que registra o estado da "música pausado/tocando", para evitar conflitos
global paused
paused = False

#inicia uma música
def Play(not_paused):
    song = songs_list.get(ACTIVE)
    song = f"C:/Users/Pichau/Desktop/Imagens/Musics/{song}"
    mixer.music.load(song)
    mixer.music.play()
    
    global paused
    paused = not_paused
    if paused:
        mixer.music.unpause()
        paused= False

    global song_display
    path = song
    basename = os.path.basename(path)
    song_display.insert(0, basename)
    song_display.delete(1, 'end')

#pausa e despausa a música
def Pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        mixer.music.unpause()
        paused= False
    else:
        mixer.music.pause()
        paused= True

#encerra a música que está tocando no momento
def Stop():
    mixer.music.stop()
    songs_list.selection_clear(ACTIVE)

#volta para a música anterior
def Previous():
    previous_one = songs_list.curselection()
    previous_one = previous_one[0] - 1
    temp2 = songs_list.get(previous_one)
    temp2 = f'C:/Users/Pichau/Desktop/Imagens/Musics/{temp2}'
    mixer.music.load(temp2)
    mixer.music.play()
    songs_list.selection_clear(0,END)
    songs_list.activate(previous_one)
    songs_list.selection_set(previous_one)

    global paused
    paused = False

    global song_display
    path = temp2
    basename = os.path.basename(path)
    song_display.insert(0, basename)
    song_display.delete(1, 'end')

#pula para a música seguinte   
def Next():
    next_one = songs_list.curselection()
    next_one = next_one[0] + 1
    temp = songs_list.get(next_one)
    temp = f'C:/Users/Pichau/Desktop/Imagens/Musics/{temp}'
    mixer.music.load(temp)
    mixer.music.play()
    songs_list.selection_clear(0, END)
    songs_list.activate(next_one)
    songs_list.selection_set(next_one)

    global paused
    paused = False

    global song_display
    path = temp
    basename = os.path.basename(path)
    song_display.insert(0, basename)
    song_display.delete(1, 'end')

def Volume(vol):
    volume = int(vol)/100
    mixer.music.set_volume(volume)

#root da Janela
root = Tk()
root.title('LCH09XX Music Player')
#inicializa o mixer
mixer.init()

songs_list = Listbox(root, selectmode=SINGLE, bg='black', fg='green3',font=('arial',15), height=12, width=47, selectbackground='green1', selectforeground='black')
songs_list.grid(columnspan= 9)

defined_font = font.Font(family='Helvetica')

#um pequeno painel que mostra a música atual que está sendo tocada
global songs_display
song_display = Listbox(root, bg= 'black', fg='green3', font=('arial',15), height=1, width=47)
song_display.grid(rowspan= 1, columnspan=9)

#abaixo temos todos os botões de funcionalidades de um player: play, pause/resume, stop, previous, next e o controlador de volume
play_button = Button(root, text= '⏵', width=7, command=lambda: Play(paused))
play_button['font'] = defined_font
play_button.grid(row=2, column=1)

pause_button = Button(root, text='⏸', width=7, command=lambda: Pause(paused))
pause_button['font'] = defined_font
pause_button.grid(row=2, column=2)

stop_button = Button(root, text='⏹', width=7, command=Stop)
stop_button['font'] = defined_font
stop_button.grid(row=2, column=3)

previous_button = Button(root, text='⏮', width=7, command=Previous)
previous_button['font'] = defined_font
previous_button.grid(row=2, column=4)

next_button = Button(root, text='⏭', width=7, command=Next)
next_button['font'] = defined_font
next_button.grid(row=2, column= 5)

volume_scale = Scale(root, label='Vol.',from_=100, to= 0,command= Volume)
volume_scale.set(100)
volume_scale.grid(row=2, column=6)

#menu da janela
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Menu', menu=add_song_menu)
add_song_menu.add_command(label='Add songs', command= addSongs)
add_song_menu.add_command(label='Delete song', command= deleteSong)

mainloop()