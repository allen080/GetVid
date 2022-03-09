#!C:\Python34\python.exe
import ctypes,os

admin = ctypes.windll.shell32.IsUserAnAdmin() # check if is admin

if not admin:
	ctypes.windll.shell32.ShellExecuteW(None, "runas", os.sys.executable, __file__, None, 1) # request admin privileges
	admin = ctypes.windll.shell32.IsUserAnAdmin()

if not admin: # if still not admin, close program
	os.sys.exit(1)

#if is admin, execute this:
try:
	if not os.path.isfile('ffmpeg.exe'):
		raise Exception('"ffmpeg.exe" not found.')
	if not os.path.isfile("getVid.exe"):
		raise Exception('"getVid.exe" not found.')

	os.popen('move ffmpeg.exe C:\\Windows\\System32 2> nul > nul').read()
	os.popen('move getVid.exe C:\\Windows\\System32 2> nul > nul').read()

	input('[*] Instalação concluida com sucesso! Feche essa janela ou aperte enter. ')

except Exception as er:
	input("Instalation error: %s"%er)
