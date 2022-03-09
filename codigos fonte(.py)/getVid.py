from youtube_dl import YoutubeDL
import argparse
import datetime
import os
import sys
from unicodedata import normalize
from getpass import getuser
from time import sleep

# lista de argumentos:
parser = argparse.ArgumentParser(description="Download Videos and Audios from url =D")
parser.add_argument('url',help="Urls to download",nargs="+",type=str)
parser.add_argument('-n','--name',help="Name of the video to be saved(default: video title from url)",type=str)
parser.add_argument('-o','--output',help="Path to be saved(default: Desktop)",type=str)
parser.add_argument('-only_audio','--only_audio',help="Download only audio(.mp3)",action='store_true')
parser.add_argument('-r','--remove_audio',help="Download video without the audio",action='store_true')
parser.add_argument('-b','--begin_time',help="Inicial time to video(default: 00) ex: 0:30",type=str)
parser.add_argument('-e','--end_time',help="End time to video(default: video size) ex: 2:10",type=str)
parser.add_argument('-p','--playlist',help="Download a playlist insted of a video on Youtube (use \"\" on url)",action='store_true')

if len(sys.argv)<2:
	parser.print_help()
	sys.exit(1)

args = parser.parse_args() # objeto com os argumentos

rename = (lambda title,new_name: os.rename(os.path.abspath('.')+'\\'+title, new_name)) # funcao de renomear arquivos

temp = sys.stdout # cria uma copia do arquivo de saida (Stdout)
def print_output(mode): #  elimina a saida padrão ou a seta
	global temp

	if mode:
		sys.stdout.close()
		sys.stdout = temp
	else:
		sys.stdout = open('nul','w')

temp_er = sys.stderr # cria uma copia do arquivo de erro (Stderr)
def print_error(mode): # elimina o erro padrão ou o seta
	global temp_er

	if mode:
		sys.stderr.close()
		sys.stderr = temp_er
	else:
		sys.stderr = open('nul','w')

def convert_time(minutes=0,seconds=0): # converte o tempo fornecido para o padrão "hh:mm:ss"
	time = str(datetime.timedelta(minutes=minutes,seconds=seconds))
	return time

def remove_audio(name):
	temp_name = 'temp_'+name
	print("[*] removing audio...")
	try:
		r = os.system('ffmpeg -y -i "%s" -vcodec copy -an "%s" 2> nul > nul'%(name,temp_name))
		if r!=0:
			raise Exception('"ffmpeg.exe" not found or with wrong parameters')

		if os.path.isfile(temp_name):
			os.remove(name)
			rename(temp_name,name)

	except Exception as er:
		print('[!] remove_audio error: %s'%er)

def cut_video(name,begin,end):  # corta o video/audio na parte especificada
	try:
		print("[*] cutting the video...")
		r = os.system("ffmpeg -y -i \"%s\" -ss %s -to %s \"%s\" 2> nul > nul"%(name,begin,end,'final_'+name))
		if r!=0:
			raise Exception('"ffmpeg" not found or with wrong parameters')

		os.remove(name)
		rename('final_'+name,name)

	except Exception as er:
		print("[!] cut video error: %s"%er)

def convert_video(video_name,new_name): # converte o video para um com outro nome e extensao
	resp = os.system('ffmpeg -y -i \"%s\" \"%s\" 2> nul > nul'%(video_name,new_name))
	if resp!=0:
		print("[!] error on video converting")
	else:
		os.remove(video_name)

def download_video(yld_opts,mode=1): # baixa o video em .mp4
	global title,url

	try:
		print("[*] starting download: %s..."%title)
	
		print_output(False)
		print_error(False) 
		with YoutubeDL(yld_opts) as video: # começa o download de fato do arquivo 
			video.download([url])
		print_output(True)
		print_error(True)
		
		
		webm = yld_opts['outtmpl']+".webm"
		mp4 = yld_opts['outtmpl']+".mp4"
		mp3 = yld_opts['outtmpl']+".mp3"
		other_name = name = [file for file in os.popen('dir /b /od').read().rstrip().split('\n') if file.startswith(yld_opts['outtmpl'])][0] # arquivo com o nome original que for achado no diretorio

		if os.path.isfile(webm) and mode==1: # se o arquivo for do formato .webm, converte para um video em .mp4
			print("[*] converting to mp4...")
			r = os.system("ffmpeg -y -i %s %s 2> nul > nul"%(webm,mp4))
			if r==0:
				os.remove(webm) # remove o arquivo .webm se a conversao for um sucesso
				return mp4
			else:
				return webm # se nao retorna o arquivo .webm

		elif mode==2 and os.path.isfile(mp3): # se o download do .mp3 for um sucesso, retorna o o nome do .mp3
			return mp3 

		else:
			return other_name # se nao retorna o nome do arquivo com a extensao final

	except KeyboardInterrupt:
		pass
	except Exception as er:
		print("[!] Download error: %s"%er)

# comeco do programa

special_c = ('\\','/','|','<','>','*',':','“','?','"')

if args.output: # verifica se um diretorio foi especificado
	if os.path.isdir(args.output): # se ele for um diretorio valido, muda para ele
		os.chdir(args.output)
	else: # se nao exibe o erro
		print("error: \"%s\" not found or not a directory"%args.output)
		sys.exit(1)
else: # se n for especificado o diretorio, o diretorio muda pra area de trabalho
	os.chdir(os.path.expanduser("~")+"\\Desktop")

print("\n[*] trying to find video(s) on Website...")
urls = args.url

if args.playlist: # se for escolhido baixar uma playlist ao inves de um video.
	try:
		if(len(urls)>1): # se for colocado mais de uma playlist pra baixar, entra no erro
			raise Exception('Supports only one playlist at a time')

		playlist = urls[0]
		base_url_videos = "https://www.youtube.com/watch?v="

		print_output(False)
		print_error(False)
		videos_info = YoutubeDL({}).extract_info(playlist,download=False,process=False) # informaçoes padroes sobre a playlist de videos
		videos_info_content = list(videos_info['entries']) # conteudo das informaçoes com as urls e os diretorios
		print_output(True)
		print_error(True)

		cont_videos = len(videos_info_content) # quantidade de videos da playlist
		playlist_title = videos_info['title']
		urls = [base_url_videos+videos_info_content[cont]['url'] for cont in range(cont_videos) if videos_info_content[cont]['title']!='[Private video]'] # lista com todas as urls da playlist tirando os videos privados

		print('[*] downloading playlist -> %s\n'%playlist_title)
	except Exception as er:
		print("Playlist error: %s"%er)
		sys.exit(1)

name_cont = 1
for url in urls:
	try:
		#video = YouTube(url) # cria a instancia do objeto do video
		url=url.rstrip('/')
		
		if 'list=' in url.lower():
			raise Exception("to download a playlist requires the option \"-p\"")

		print_output(False)
		print_error(False)
		video_info = YoutubeDL({}).extract_info(url,download=False)
		print_output(True)
		print_error(True)

		title = normalize('NFKD',video_info['title']).encode("ASCII",'ignore').decode('ASCII') # remove os caracteres invalidos do titulo do youtube

		s='' # remove todos os caracteres invalidos do titulo
		for i in title:
			if i not in special_c:
				s+=i
		title = s

	except Exception as er:
		if str(er).startswith('regex pattern'): # verifica se o erro foi por nao achar o video
			print('[!] video error: "%s" video not found on Youtube'%url)
			continue

		else:
			print("[!] creating object error: %s"%er)
			continue

	if args.name: # se foi especificado um nome pro video sera colocado, se n o nome sera o titulo
		name = args.name
	else:
		name = title

	if args.only_audio: # coloca o .mp3 ou .mp4 no video
		name = name.rstrip('.mp3')
		name+='.mp3'
	else:
		name = name.rstrip('.mp4')
		name+='.mp4'

	if args.name and len(urls)>1 or args.playlist:
		if args.only_audio:
			name = name[:name.index('.mp3')]+str(name_cont)+'.mp3'
		else:
			name = name[:name.index('.mp4')]+str(name_cont)+'.mp4'
		name_cont+=1

	exit_p = False # variavel para verificar se deseja nao sobrescrever o arquivo e continuar baixando as proximas urls
	if os.path.isfile(name): # verifica se ja existe um arquivo com o msm nome no diretorio atual
		while 1:
			exist = input('[!] o arquivo \'%s\' ja existe, deseja sobrescreve-lo?(s=sim/n=nao): '%name).lower()
			if exist.startswith('n'):
				exit_p = True 
				break
			elif exist.startswith('s') or exist.startswith('y'):
				os.remove(name)
				break
			print('invalido, digite "s" ou "n"')
				
	if exit_p: # se nao desejar sobrescrever, continua a baixar as outras
		print()
		continue 
		
	# download o video
	if args.only_audio: # se foi mandado baixar apenas o audio
		yld_opts = {'outtmpl':name,'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'195'}],'quiet':True}
		name_download = download_video(yld_opts,mode=2)

	else: # baixar o video completo
		yld_opts = {'outtmpl':name[:-4],'audioformat':"mp3",'quiet':True}
		name_download = download_video(yld_opts)

	if name_download!=name:
		convert_video(name_download,name)

	if args.remove_audio:
		remove_audio(name)

	file_path = os.getcwd()+'\\'+name # caminho completo do arquivo
	
	try:
		video_time = os.popen('ffmpeg -i "%s" 2> duration&type duration|find "Duration"& del duration'%name).read().strip().split()[1].split('.')[0][1:]
	except:
		video_time = ''

	try: # faz a verificaçao do tempo dos videos
		if args.begin_time:  # verifica se um tempo inicial foi especificado
			if ':' not in args.begin_time:
				begin = convert_time(int(args.begin_time))
			else:
				t = args.begin_time.split(':')
				begin = convert_time(int(t[0]),int(t[1]))
		else:
			begin = convert_time() # se n for especificado o tempo sera "00:00:00"

		if args.end_time: # verifica se o tempo final foi especificado
			if ':' not in args.end_time:
				end = convert_time(int(args.end_time))
			else:
				t = args.end_time.split(':')
				end = convert_time(int(t[0]),int(t[1]))
		else:
			end = convert_time()

			if video_time!='': # verifica se o tempo do video foi encontrado
				end = video_time # se n foi especificado o tempo final sera o tempo do video
		
		if begin>end: # se o tempo fornecido for maior q o tempo fornecido do video
			raise Exception('begin time is bigger than the final time!')

		elif video_time!='':
			if begin>video_time or end>video_time: # se o tempo inicial ou final for maior q o tempo total do video baixado
					raise Exception('selected time is bigger than the video length')

	except Exception as er:
		print('[!] time error: %s'%er)
		continue

	try:
		if begin!="0:00:00" or end!=video_time: #verifica se precisa cortar uma parte do video
			cut_video(name,begin,end)

		print("[*] saved in -> %s"%file_path)
		print("[*] download finished\n")

	except Exception as er:
		print("After download error: %s"%er)