#!/usr/bin/python3

#   Este programa baja videos de youtube
#   Copyright (C) 2022 Cristian Tocci
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   Contacto : toccicristian@hotmail.com / toccicristian@protonmail.ch

# TODO : chequear que en windows busque el 7-zip en os.environ['PROGRAMFILES']

licencias = dict()
licencias['gplv3'] = """    pitsydownloader.py  Copyright (C) 2022  Cristian Tocci
	This program comes with ABSOLUTELY NO WARRANTY; for details press 'w'.
	This is free software, and you are welcome to redistribute it
	under certain conditions; See COPYING.odt file for further details.
"""
licencias['gplv3logo'] = """
+----------------------------------------------------------------------------------------------------+
|oooooooo+~~~+~~~~~~+~~~~~+~~~~+~~~~~~+~~~~+~~~~~~+~~+~~~~+~~~~~+~~~~+~~~~~~++~~+~~+~~~~~~:  ::::::~+|
|oooooooo :::::::::::::::::::::::::::::::::::::::::::~::::::::::::::::::::::::::::::::. ~~~++ooooo+:.|
|ooooooo~::::::~:::::::::::::::::::::::::::::::::::::+::::::::::::::::::::::::~~.~:~:~+oooooooooooo:.|
|ooooooo :~:~~~~~~~~~~+~::: +~~~~~~~~~~~~~::++ :::::~+~:::::::::::::::::::~...~:::~ooooooooooooooo~.+|
|oooooo~~:~oo~~~~~~~~~oo~:~+oo ~~~~~~.ooo.~oo+~::::.+o ::::::::::::::::~  .~::::+oo+~:   +ooooooo::+o|
|oooooo::.+o+~::::::~+oo : oo~::::::::oo~:~oo~::::: oo~:::::::::::::: ~ ~::::.++~ ~:::::.+oooo+~ ~ooo|
|ooooo+~:~oo~:::::::::::::~oo::::::::+oo :+oo~:::::~oo+.::::::::::.:~ ~:::::: .:::::::~~oooo+:~ +oooo|
|ooooo::~+o+.:::::::::::: oo+~:::::: oo~~:oo~::::::~ooo~::::::::.~~.::::::::::::::::~~+oooooo+~::oooo|
|oooo+~::oo~:::~:~:~~::::~oo~       ~oo::+oo.::::::~ooo+~::::: ~~.:::::::::::::::: ~+oooooooooo~~oooo|
|oooo~::+oo :::~   +oo::.ooo~~~~~~~~~:.: oo+:::::::~oooo~:::~~+:::::::::::::::: ~+++~~~~oooooo+.~oooo|
|ooo+.: oo~:::::::.oo+.:~oo~::::::::::::~oo:::::::::oooo+~::++~::::::::::::::~   .::::::ooooo~.~ooooo|
|ooo~::~oo::::::::~oo~:~+o+~::::::::::: oo+~:::::::.+ooo~.~o+:::::::::::::::::::::::: +oooo+: +oooooo|
|ooo.: oo+.~~~~~~ +oo.::oo~::::::::::::~oo~~~~~~~:::+oo~ +oo ::::::::::::::::::::.:~ooooo+: ~oooooooo|
|oo~::.~~~~~~~~~~~~~ ::~+~.::::::::::::~+~~~~~~~~~:::o~ +ooo:::::::::::::::::: ~+oooooo~::~oooooooooo|
|o+ :~   ~::::::::::::.  ~::::: ..:::::::::::::::::::~ ~oooo~~::::::::::~. ~~+oooooo+~::+oooooooooooo|
|o~~:~~: ~ :~~. ~~.::~~~~. ::.~~~~::~:: :~~.~::~~ ::::.oooooo+~~::::~~~~ooooooooo+~::~+oooooooooooooo|
|o::~~~~:::~~~ ~~~.:: ::~.~:~.~~~: ~~~ :~~~: ~~~~~:::: oooooooooooooooooooooo++~::~+ooooooooooooooooo|
|+:::~::::::~~::::::::~~:::~::~:::::::::::~::::~:::::::~ooooooooooooooooo++~::~~+oooooooooooooooooooo|
|::::::::::::::::::::::::::::::::::::::::::::::::::::::: ~oooooooooo+~~~::~~+oooooooooooooooooooooooo|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:~~~~~:    ::::::::~~~ooooooooooooooooooooooooooooo|
+----------------------------------------------------------------------------------------------------+
"""
licencias['textow'] = """
	15. Disclaimer of Warranty.
	THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
	APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
	HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT
	WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT
	LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
	PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE
	OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU
	ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

	16. Limitation of Liability.
	IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
	WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
	CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR
	DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL
	DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM
	(INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED
	INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF
	THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER
	OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

	17. Interpretation of Sections 15 and 16.
	If the disclaimer of warranty and limitation of liability provided above
	cannot be given local legal effect according to their terms,
	reviewing courts shall apply local law that most closely approximates
	an absolute waiver of all civil liability in connection with the Program,
	unless a warranty or assumption of liability accompanies a copy of
	the Program in return for a fee.
	"""

import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import platform
import time
import sys
import os
import shutil
import distro
import requests
import ffmpeg
import yt_dlp

ancho_barra_progresion = 550
default_dir = '~'
url_ffmpeg_git_essentials='https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z'
url_7z_installer='https://www.7-zip.org/a/7z2107-x64.exe'


class FormatoVideo:
	def __init__(self, tam=int(), ext=str(), formato=str(), acodec=str(), url=str()):
		if tam is None:
			tam = 0
		if ext is None:
			ext = ''
		if formato is None:
			formato = ''
		if url is None:
			url = ''
		self._tam = tam
		self._ext = ext
		self._formato = formato
		self._acodec = acodec
		self._url = url

	def get_tam(self, mb=False):
		if mb:
			return round(self._tam/1024/1024, 2)
		return self._tam

	def get_ext(self):
		return self._ext

	def get_formato(self):
		return self._formato

	def get_acodec(self):
		return self._acodec

	def get_url(self):
		return self._url

	def to_str(self, url_sz=None):
		u = self._url
		lj = 0
		if url_sz is not None and str(url_sz).isdigit() and int(url_sz) > 0:
			u = self.get_url()[:url_sz]+'[...]'
			lj = int(url_sz)+3
		return (
			(str(self.get_tam(mb=True))+' MB ').rjust(15)
			+ str(self.get_ext().ljust(8))
			+ str(self.get_formato().ljust(20))
			+ str(u.ljust(lj))
			)


continuar = False
def descarga_archivo(label_info,barra_p,url_origen=str(),url_destino=str(),nombre_descarga=str()):
	global continuar
	continuar = True
	chunksz = 1024*4
	url_destino=os.path.expanduser(os.path.normpath(url_destino))
	with open(url_destino,'wb') as ar_destino:
		agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-us,en;q=0.5', 'Sec-Fetch-Mode': 'navigate'}
		label_info.config(text='Conectando: Espera un cachito...')
		respuesta = requests.get(url_origen, stream=True, headers=agent)
		tam_total = respuesta.headers.get('content-length')
		if not continuar:
			return False
		if tam_total is None:
			ar_destino.write(respuesta.content)
		else:
			barra_p['value'] = 0
			dl = 0
			tam_total = int(tam_total)
			tam_totalmb = round(tam_total/1024/1024,2)
			for datos in respuesta.iter_content(chunk_size=chunksz):
				if not continuar:
					return False
				dl += len(datos)
				ar_destino.write(datos)
				dlmb = round(dl/1024/1024, 2)
				label_info.config(text='Descargando '+nombre_descarga+' ['+str(dlmb)+'/'+str(tam_totalmb)+']')
				barra_p.step(chunksz*100/tam_total)
			barra_p.step(100)
			label_info.config(text='Descarga finalizada')
	return True


def chequeo_inicial():
	if str(platform.system()) == 'Windows':
		if not (os.path.isfile('ffmpeg.exe') and os.path.isfile('ffprobe.exe')):
			ventana_setup()
		if not (os.path.isfile('ffmpeg.exe') and os.path.isfile('ffprobe.exe')):
			print('No se pudo obtener ffmpeg.exe o ffprobe.exe')
			sys.exit(0)
	if str(platform.system()) == 'Linux':
		if not shutil.which('ffmpeg'):
			ventana_setup()
		if not shutil.which('ffmpeg'):
			print('No se pudo obtener o instalar el paquete ffmpeg')
			sys.exit(0)


def comando_boton_iniciar (v,boton,label_info,barra_p):
	boton.configure(text='CANCELAR',command=lambda :cancelar_descarga())
	threading.Thread(target=setup_inicial, args=(v,label_info,barra_p,)).start()
	return None


def setup_inicial(v,label_info,barra_p):
	recursos_dir = './recursos'
	recursos_dir=os.path.expanduser(os.path.normpath(recursos_dir))
	if str(platform.system()) == 'Windows':
		programfiles_var=os.environ['PROGRAMW6432']
		if not (os.path.isfile('ffmpeg.exe') and os.path.isfile('ffprobe.exe')):
			exe7z=os.path.join(os.path.join(programfiles_var,'7-Zip'),'7z.exe')
			if not os.path.isdir(recursos_dir):
					os.makedirs(recursos_dir,exist_ok=True)
			if not (os.path.isfile(exe7z)):
				if not (descarga_archivo(label_info,barra_p,url_7z_installer,os.path.join(recursos_dir,'7z.exe'),'7-zip')):
					v.destroy()
					return True
				label_info.config(text='Instalando 7-Zip')
				os.system('start /wait '+os.path.join(recursos_dir,' 7z.exe')+' /S')
			if not (descarga_archivo(label_info,barra_p,url_ffmpeg_git_essentials,
				os.path.join(recursos_dir,'ffmpeg_git_essentials.7z'),'encoder FFMPEG')):
				v.destroy()
				return True
			label_info.config(text='Extrayendo encoder...')
			com_extraer_ffmpeg='\"'+exe7z+'\"'+' e -y '+os.path.join(recursos_dir,'ffmpeg_git_essentials.7z')+' *.exe -r'
			os.system(com_extraer_ffmpeg)
		v.destroy()
		return True
	if str(platform.system()) == 'Linux':
		if not shutil.which('ffmpeg'):
			url_ffmpeg_linux={
			'trusty'  : 'http://launchpadlibrarian.net/153479180/ffmpeg_0.8.7-1ubuntu2_amd64.deb',
			'xenial'  : 'http://launchpadlibrarian.net/489338525/ffmpeg_2.8.17-0ubuntu0.1_amd64.deb',
			'bionic'  : 'http://launchpadlibrarian.net/489641527/ffmpeg_3.4.8-0ubuntu0.2_amd64.deb',
			'focal'   : 'http://launchpadlibrarian.net/489340659/ffmpeg_4.2.4-1ubuntu0.1_amd64.deb',
			'hirsute' : 'http://launchpadlibrarian.net/524395138/ffmpeg_4.3.2-0+deb11u1ubuntu1_amd64.deb',
			'impish'  : 'http://launchpadlibrarian.net/559380332/ffmpeg_4.4-6ubuntu5_amd64.deb',
			'jammy'   : 'http://launchpadlibrarian.net/590399276/ffmpeg_4.4.1-3ubuntu5_amd64.deb'
			}
			if not os.path.isdir(recursos_dir):
				os.makedirs(recursos_dir,exist_ok=True)
			if not((distro.os_release_info()['name'] == 'Ubuntu') and
					(distro.os_release_info()['version_codename'] in url_ffmpeg_linux)):
				print('version de OS no soportada')
				v.destroy()
				return True
			rel=distro.os_release_info()['version_codename']
			deb_nombre='ffmpeg_'+url_ffmpeg_linux[rel].split('ffmpeg_')[1]
			if not (descarga_archivo(label_info,barra_p,url_ffmpeg_linux[rel],
					os.path.join(recursos_dir,deb_nombre),'encoder FFMPEG')):
				print('inicializacion cancelada')
				v.destroy()
				return True
			label_info.config(text='Instalando encoder FFMPEG')
			com=['qapt-deb-installer',join(recursos_dir,deb_nombre)]
			subprocess.Popen(com, shell=True, stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT, universal_newlines=True)
		v.destroy()
		return True


def get_formatos(video):
	formatos = list()
	for f in video['formats']:
		sz = 0
		if 'filesize' in f.keys() and f['filesize'] is not None:
			sz = int(f['filesize'])
		formatos.append(FormatoVideo(tam=sz, ext=str(f['ext']), formato=str(
			f['format']).split(' - ')[1], acodec=str(f['acodec']), url=str(f['url'])))
	return formatos


def get_videos(url):
	ytdl = yt_dlp.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
	with ytdl:
		busq=url
		if not url.startswith('https://www.youtube.com/watch?v='):
			busq='ytsearch:{'+busq+'}'
		resultado = ytdl.extract_info((busq), download=False)
	v = list()
	if 'entries' not in resultado:
		v.append(resultado)
		return v
	for entrada in resultado['entries']:
		v.append(entrada)
	return v


def acorta_texto(texto=str(), longitud=int()):
	if longitud is None:
		longitud = 30
	if texto is None:
		return '...'
	if len(texto) < longitud:
		return texto
	return texto[:longitud]+'...'


def directory_browser(titulo=str(), defaultdir=str()):
	if not titulo:
		titulo = 'Seleccione directorio destino...'
	directorio = filedialog.askdirectory(title=titulo)
	if not directorio:
		directorio = defaultdir
	return os.path.expanduser(os.path.normpath(directorio))


def examinar(entry_url):
	head_url = os.path.expanduser(os.path.normpath(default_dir))
	directorio_seleccionado = directory_browser(
		'Seleccione directorio destino...', entry_url.get())
	entry_url.delete(0, tk.END)
	if not directorio_seleccionado:
		directorio_seleccionado = head_url
	entry_url.insert(tk.END, directorio_seleccionado)
	return None


# ######################################################################### INTERACCIONES DEL MOUSE
def copiapega_menu(event, menu):
	try:
		menu.tk_popup(event.x_root, event.y_root)
	finally:
		menu.grab_release()


def copiar_al_portapapeles(ventana_principal, entrada):
	if entrada.select_present():
		texto = entrada.selection_get()
		ventana_principal.clipboard_clear()
		ventana_principal.clipboard_append(texto)


def cortar_al_portapapeles(ventana_principal, entrada):
	if entrada.select_present():
		texto_copiado = entrada.selection_get()
		ventana_principal.clipboard_clear()
		ventana_principal.clipboard_append(texto_copiado)
		textofinal = entrada.get().replace(entrada.selection_get(), '')
		selstartpos = entrada.index(tk.INSERT)-len(entrada.selection_get())
		entrada.delete(0, tk.END)
		entrada.insert(0, textofinal)
		entrada.icursor(selstartpos)
		return None


def pegar_del_portapapeles(ventana_principal, entrada):
	portapapeles = ventana_principal.clipboard_get()
	if entrada.select_present():
		textofinal = entrada.get().replace(entrada.selection_get(), portapapeles)
		selstartpos = entrada.index(tk.INSERT)-len(entrada.selection_get())
		entrada.delete(0, tk.END)
		entrada.insert(0, textofinal)
		entrada.icursor(selstartpos+len(portapapeles))
		return None
	entrada.insert(entrada.index(tk.INSERT), portapapeles)
	return None


def copiapega_menu_destruye(menu, event=None):
	menu.unpost()
# ################################################################# FIN DE INTERACCIONES DEL MOUSE


def cancelar_descarga():
	global continuar
	continuar = False
	return None


def reset_ui_info(barra_progresion, progresion_info, label_estado_descarga, statmsg=str()):
	if statmsg == None:
		statmsg = '-'
	progresion_info.config(text='inactiva')
	barra_progresion.step(0)
	label_estado_descarga.config(text=statmsg)
	return None


def obtiene_duracion_medio(url=str()):
	return time.strftime('%H:%M:%S', time.gmtime(round(int(float(ffmpeg.probe(url)['format']['duration'])))))


continuar = False


def convertir_medio(barra_progresion, progresion_info, label_estado_descarga, url_in=str(), url_out=str(), soloaudio=False):
	if url_in is None or url_out is None:
		return False
	global continuar
	continuar = True
	duracion = ''
	duracion = obtiene_duracion_medio(url_in)
	url_in = os.path.expanduser(os.path.normpath(url_in))
	url_out = os.path.expanduser(os.path.normpath(url_out))
	com=['ffmpeg','-i',url_in]
	if url_out.endswith(('.mp3','.ogg')) or (soloaudio and url_out.endswith('.mp4')):
		com.append('-vn')
	if url_out.endswith('.ogg'):
		com.append('-acodec')
		com.append('libvorbis')
	com.append('-y')
	com.append(url_out)
	proceso = subprocess.Popen(com, shell=True, stdout=subprocess.PIPE,
							   stderr=subprocess.STDOUT, universal_newlines=True)
	for linea in proceso.stdout:
		if not continuar:
			proceso.kill()
			reset_ui_info(barra_progresion, progresion_info, label_estado_descarga,
							statmsg='CONVERSION CANCELADA :' + acorta_texto(str(url_out), 25))
			return None
		if 'size=' in linea and 'time=' in linea:
			tam = linea.split('size=')[1].lstrip().split(' ')[0]
			dur = linea.split('time=')[1].split(' ')[0]
			label_estado_descarga.config(
				text='CONVIRTIENDO :'+str(tam)+' -> '+str(dur)+'/'+str(duracion))
	label_estado_descarga.config(
		text='TERMINADA CONVERSION:'+acorta_texto(str(url_out), 25))
	return True


continuar = False


def bajar_video(video, formato, entry_destino, barra_progresion, progresion_info, label_estado_descarga):
	global continuar
	continuar = True
	chunksz = 1024*4
	destino_url = os.path.join(entry_destino.get(), video['title']+'-'
							+ formato.get_formato().replace(' ', '-').replace('(', '-').rstrip(')')+'.'+formato.get_ext())
	with open(destino_url, 'wb') as ar_destino:
		agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-us,en;q=0.5', 'Sec-Fetch-Mode': 'navigate'}
		respuesta = requests.get(formato.get_url(), stream=True, headers=agent)
		tam_total = respuesta.headers.get('content-length')
		if tam_total is None:
			ar_destino.write(respuesta.content)
		else:
			barra_progresion['value'] = 0
			label_estado_descarga.config(
				text='Descargando :'+acorta_texto(str(video['title']), 40))
			dl = 0
			tam_total = int(tam_total)
			tam_totalmb = round(tam_total/1024/1024, 2)
			for datos in respuesta.iter_content(chunk_size=chunksz):
				if not continuar:
					reset_ui_info(barra_progresion, progresion_info, label_estado_descarga,
					statmsg='CANCELADA :' + acorta_texto(str(video['title']), 39))
					return None
				dl += len(datos)
				ar_destino.write(datos)
				terminado = int(ancho_barra_progresion*dl/tam_total)
				dlmb = round(dl/1024/1024, 2)
				barra_progresion.step(chunksz*100/tam_total)
				progresion_info.config(text='['+str(dlmb)+'/'+str(tam_totalmb)+'] MB')
			barra_progresion.step(100)
			label_estado_descarga.config(
				text='TERMINADA :'+acorta_texto(str(video['title']), 40))
			progresion_info.config(text='inactiva')
	return destino_url


def selecciona_formato_preferido(video, soloaudio=False, calidad=('(480p)', '(720p)'), ext=['webm', 'mp4']):
	formatos = get_formatos(video)
	f_temp = False
	if soloaudio:
		for formato in formatos[::-1]:
			if formato.get_formato().startswith('audio only'):
				if not f_temp:
					f_temp = formato
				if formato.get_tam() > f_temp.get_tam():
					f_temp = formato
		return f_temp
	for formato in formatos:
		if formato.get_formato().endswith(calidad) and (formato.get_ext() in ext) and formato.get_acodec() != 'none':
			return formato
	for formato in formatos[::-1]:
		if not formato.get_formato().startswith('audio only') and formato.get_acodec() != 'none':
			return formato
	for formato in formatos[::-1]:
		if not formato.get_formato().startswith('audio only'):
			return formato
	return False


def obtiene_lista_videos(entry_url, label_estado_descarga):
	try:
		s = ''
		label_estado_descarga.config(text='Buscando video...')
		videos = get_videos(entry_url.get().split('&')[0])
		if len(videos) > 1:
			s = 's'
		label_estado_descarga.config(
			text=str(len(videos))+' Video'+s+' Encontrado'+s)
	except yt_dlp.utils.DownloadError:
		label_estado_descarga.config(text='Video no encontrado')
		return None
	return videos


def gestion_de_bajada(convertir_opcion_seleccionada, entry_url, entry_destino,
					  barra_progresion, progresion_info, label_estado_descarga, soloaudio=False, convertir=False):
	#if not entry_url.get().startswith('https://www.youtube.com/watch?v='):
	#	return None
	lista_videos = obtiene_lista_videos(entry_url, label_estado_descarga)
	if lista_videos is None:
		return None
	video = lista_videos[0]
	formato_preferido = selecciona_formato_preferido(
		video=video, soloaudio=soloaudio)
	try:
		url_archivo_bajado = bajar_video(
			video, formato_preferido, entry_destino, barra_progresion, progresion_info, label_estado_descarga)
	except (ConnectionError) as e:
		reset_ui_info(barra_progresion, progresion_info,
					  label_estado_descarga, statmsg='ERROR EN DESCARGA : REINTENTAR?')
	if convertir:
		convertir_medio(barra_progresion, progresion_info, label_estado_descarga,
				 url_archivo_bajado, str(url_archivo_bajado)+str(convertir_opcion_seleccionada), soloaudio)
	return None


def comando_boton_bajar(convertir_opcion_seleccionada, convertir_var, soloaudio_var, entry_url, entry_destino,
						barra_progresion, progresion_info, label_estado_descarga):
	soloaudio = False
	if soloaudio_var == 1:
		soloaudio = True
	convertir = False
	if convertir_var == 1:
		convertir = True
	threading.Thread(target=gestion_de_bajada, args=(convertir_opcion_seleccionada, entry_url,
												  entry_destino, barra_progresion, progresion_info,
												  label_estado_descarga, soloaudio, convertir,)).start()
	return None


def ventana_setup():
	v_min_w = 400
	v_min_h = 130
	v = tk.Tk()
	v.title('Configuracion inicial')
	v.geometry(str(v_min_w)+'x'+str(v_min_h))
	v.resizable(width=False,height=False)
	label_info=tk.Label(v,text='Primero necesitaremos descargar 7z y ffmpeg. Pulse <INICIAR>')
	barra_p = ttk.Progressbar(v, length=280, mode='determinate')
	boton_iniciar = tk.Button(text='<INICIAR>',
		command= lambda : comando_boton_iniciar(v,boton_iniciar,label_info,barra_p))

	label_info.pack(side=tk.TOP,pady=(5,0))
	barra_p.pack(side=tk.TOP,pady=(15,0))
	boton_iniciar.pack(side=tk.TOP,pady=(15,0))
	v.mainloop()



def show_w(ventana_principal, textow):
	ventana_w = tk.Toplevel(ventana_principal)
	ventana_w.title('This program comes with ABSOLUTELY NO WARRANTY')
	ventana_w.geometry('800x600')
	tk.Label(ventana_w, text=textow).pack()
	ventana_w.focus_set()
	ventana_w.bind('<Escape>', lambda event: ventana_w.destroy())


def ayuda(ventana_principal):
	texto_ayuda = """
		Pitsy Downloader
		-----------------------------------------------------
		F1 : Esta ayuda.
		Enter : Descarga el video/audio de la url ingresada.
		Esc : Cierra la aplicación / Cierra esta ventana
		"""
	ventana_ayuda = tk.Toplevel(ventana_principal)
	ventana_ayuda.title(' Atajos y ayuda')
	tk.Label(ventana_ayuda, text=texto_ayuda, justify='left').pack(
		side=tk.LEFT, padx=(0, 30), pady=(10, 10))
	ventana_ayuda.focus_set()
	ventana_ayuda.bind('<Escape>', lambda event: ventana_ayuda.destroy())


def muestra_ventana():
	ventana_principal_min_ancho = 700
	ventana_principal_min_alto = 300
	ventana_principal = tk.Tk()
	ventana_principal.title('Pitsy Downloader')
	ventana_principal.geometry(
		str(ventana_principal_min_ancho)+'x'+str(ventana_principal_min_alto))
	ventana_principal.resizable(width=False, height=False)

	marco_info = tk.Frame(ventana_principal)
	label_info = tk.Label(marco_info, text='F1:Ayuda')
	boton_w = tk.Button(marco_info, text='Acerca de...')

	marco_bajar = tk.Frame(ventana_principal, width=str(
		ventana_principal_min_ancho-20), height='100')
	marco_url_bajar = tk.Frame(marco_bajar, width=str(
		ventana_principal_min_ancho-100), height='100')
	label_url_bajar = tk.Label(marco_url_bajar, text='URL:', width=5)
	entry_url_bajar = tk.Entry(marco_url_bajar, width=str(
		int(ventana_principal_min_ancho/9)))
	menu_rmb_entry_url_bajar = tk.Menu(entry_url_bajar, tearoff=0)

	marco_boton_bajar = tk.Frame(marco_bajar, width='100', height='100')
	boton_bajar = tk.Button(marco_boton_bajar, text='BAJAR')

	marco_opciones = tk.Frame(ventana_principal, width=str(
		ventana_principal_min_ancho-20), height='100')
	marco_casillas = tk.Frame(marco_opciones, width=str(
		ventana_principal_min_ancho-100), height='100')
	soloaudio_var = tk.IntVar()
	soloaudio_checkbox = tk.Checkbutton(
		marco_casillas, text='Solo Audio', variable=soloaudio_var)
	convertir_var = tk.IntVar()
	convertir_checkbox = tk.Checkbutton(
		marco_casillas, text='Convertir:', variable=convertir_var)
	convertir_opcion_seleccionada = tk.StringVar(marco_casillas)
	convertir_opcion_seleccionada.set('.ogg')
	opciones = ['.ogg', '.mp3', '.mp4']
	convertir_dropdown = tk.OptionMenu(
		marco_casillas, convertir_opcion_seleccionada, *opciones)
	marco_boton_cancelar = tk.Frame(marco_opciones, width='100', height='100')
	boton_cancelar = tk.Button(marco_boton_cancelar, text='CANCELAR')

	marco_destino = tk.Frame(ventana_principal, width=str(
		ventana_principal_min_ancho-20), height='100')
	marco_destino_url = tk.Frame(marco_destino, width=str(
		ventana_principal_min_ancho-100), height='100')
	label_destino_url = tk.Label(marco_destino_url, text='Destino:', width=9)
	entry_destino_url = tk.Entry(marco_destino_url, width=str(
		int(ventana_principal_min_ancho/9)))
	marco_destino_boton_examinar = tk.Frame(
		marco_destino, width='100', height='100')
	boton_examinar = tk.Button(marco_destino_boton_examinar, text='Examinar...')

	marco_barra_progresion = tk.Frame(ventana_principal, width=str(
		ventana_principal_min_ancho-20), height='100')
	marco_barra_progresion_barra = tk.Frame(
		marco_barra_progresion, width=str(ventana_principal_min_ancho-100))
	label_estado_descarga = tk.Label(
		marco_barra_progresion_barra, width='50', text='-')
	barra_progresion = ttk.Progressbar(
		marco_barra_progresion_barra, length=ancho_barra_progresion, mode='determinate')
	marco_barra_progresion_info = tk.Frame(
		marco_barra_progresion, width='100', height='100')
	label_barra_progresion_info = tk.Label(
		marco_barra_progresion_info, text='[inactiva]')

	boton_w.config(command=lambda: show_w(ventana_principal, licencias['textow']))
	ventana_principal.bind('<F1>', lambda event: ayuda(ventana_principal))
	ventana_principal.bind('<Escape>', lambda event: ventana_principal.destroy())
	boton_bajar.config(command=lambda: comando_boton_bajar(convertir_opcion_seleccionada.get(), convertir_var.get(), soloaudio_var.get(),
														entry_url_bajar, entry_destino_url, barra_progresion, label_barra_progresion_info, label_estado_descarga))
	entry_url_bajar.bind('<Return>', lambda x: comando_boton_bajar(convertir_opcion_seleccionada.get(), convertir_var.get(), soloaudio_var.get(),
																entry_url_bajar, entry_destino_url, barra_progresion, label_barra_progresion_info, label_estado_descarga))
	boton_cancelar.config(command=lambda: cancelar_descarga())
	boton_examinar.config(command=lambda: examinar(entry_destino_url))
	menu_rmb_entry_url_bajar.add_command(
		label='Copiar - Ctrl+c', command=lambda: copiar_al_portapapeles(ventana_principal, entry_url_bajar))
	menu_rmb_entry_url_bajar.add_command(
		label='Cortar - Ctrl+x', command=lambda: cortar_al_portapapeles(ventana_principal, entry_url_bajar))
	menu_rmb_entry_url_bajar.add_command(
		label='Pegar - Ctrl+v', command=lambda: pegar_del_portapapeles(ventana_principal, entry_url_bajar))
	menu_rmb_entry_url_bajar.bind('<FocusOut>', lambda event: copiapega_menu_destruye(
		menu_rmb_entry_url_bajar, event=None))
	entry_url_bajar.bind(
		'<Button-3>', lambda event: copiapega_menu(event, menu_rmb_entry_url_bajar))
	entry_url_bajar.bind(
		'<Button-2>', lambda event: pegar_del_portapapeles(ventana_principal, entry_url_bajar))

	marco_info.pack(side='top', fill='x')
	label_info.pack(side=tk.LEFT, padx=(10, 10))
	boton_w.pack(side=tk.LEFT, padx=(10, 10))

	marco_bajar.pack(side='top', fill='x')
	marco_url_bajar.pack(side='left', anchor=tk.W)
	label_url_bajar.pack(side='top', padx=(5, 0), anchor=tk.W)
	entry_url_bajar.pack(side='top', padx=(10, 10))
	entry_url_bajar.focus()
	marco_boton_bajar.pack(side='right')
	boton_bajar.pack(side='top', padx=(10, 10), pady=(25, 10))

	marco_opciones.pack(side='top', fill='x')
	marco_casillas.pack(side='left', anchor=tk.W)
	soloaudio_checkbox.pack(side='left', padx=(5, 5), anchor=tk.W)
	convertir_checkbox.pack(side='left', padx=(5, 5), anchor=tk.W)
	convertir_dropdown.pack(side='left', padx=(5, 5), anchor=tk.W)
	marco_boton_cancelar.pack(side='right')
	boton_cancelar.pack(side='top', padx=(10, 10), pady=(0, 10))

	marco_destino.pack(side='top', fill='x')
	marco_destino_url.pack(side='left', anchor=tk.W)
	label_destino_url.pack(side='top', padx=(5, 0), anchor=tk.W)
	entry_destino_url.pack(side='top', padx=(10, 10))
	entry_destino_url.insert(0, os.path.expanduser(os.path.normpath(default_dir)))
	marco_destino_boton_examinar.pack(side='right')
	boton_examinar.pack(side='top', padx=(10, 10), pady=(25, 10))

	marco_barra_progresion.pack(side='top', fill='x')
	marco_barra_progresion_barra.pack(side='left', padx=(10, 10), pady=(15, 15))
	label_estado_descarga.pack(side='top')
	barra_progresion.pack(side='left', padx=(0, 0), pady=(10, 10))
	marco_barra_progresion_info.pack(side='left', fill='x')
	label_barra_progresion_info.pack(side='left', padx=(0, 0), pady=(25, 10))

	ventana_principal.mainloop()


chequeo_inicial()

muestra_ventana()
