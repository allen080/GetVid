Manual de uso do getVid.exe =)
criado por: Luan Fellipe (Allen08)

O getVid.exe � um programa CLI que foi criado com o intuito de facilitar na hora que fazer download de video ou audios de sites como Youtube, Facebook, Instagram, Twitter, Dailymotion e etc.

As op��es disponiveis nessa vers�o 1.4 do programa incluem:
- baixar varios videos apartir de suas urls
- baixar varios audios apartir de suas urls
- baixar um trecho de video ou audio especifico
- baixar playlists inteiras de video ou audio do youtube
* Bugs de reconhecer o Desktop do usu�rio corrigidos!

Instala��o:
se vc acabou de fazer o download do programa e extraiu o ".zip" dele, os proximos passos que vc tera que executar s�o:

1�) verifique se os arquivos "getVid.exe","Setup.exe" e "ffmpeg.exe" estao na pasta do programa, se nao estiverem, � provavel que vc n�o os baixou ou o seu antivirus/firewall bloqueou a cria��o deles.
se esse for o caso, tente permitir a cria��o deles no seu antivirus ou desative ele e baixe tudo novamente.
2�) Abra o "Setup.exe" que esta contido na pasta
3�) Coloque "Sim" quando perguntar se deseja que o programa use o acesso de administrador. esse acesso � apenas necessario para que se possa copiar os arquivos necessarios pra pasta System32 do Windows, que sera responsavel para poder usar o programa em qualquer diretorio no Cmd.
4�) Se aparecer a mensagem "A instala��o foi concluida com sucesso", tudo ocorreu bem e o programa esta pronto pra uso. Sen�o, � provavel que ou o acesso administrativo nao foi permitido, ou os arquivos "ffmpeg.exe" e "getVid.exe" n�o foram encontrados na pasta.

Uso:
para usar o programa, apenas abra um prompt de comando (Cmd) no windows e digite "getvid" (n importa se for com letra maiuscula ou n�o) obs: para abrir o cmd digite na area de pesquisa do windows "cmd" ou as teclas (Windows + R) e cmd.
Se a mensagem "the following arguments are required: url" aparecer no final, quer dizer que esta tudo pronto pra uso. 
Se a mensagem "'getVid' n�o � reconhecido como um comando interno..." aparecer, quer dizer que o programa n�o esta instalado na maquina e vc tera que baixar novamente.

para verificar as op��es do programa, digite: getvid -h ou getvid --help

segue abaixo informa��es sobre as op�oes de uso do programa:

-baixar videos .mp4:
  o padrao a ser usado � baixar os arquivos de video de um site atraves da url, lembrando que pode ser usado mais de uma url, ex:
	getvid https://www.youtube.com/watch?v=x91tRBU_H9Q https://www.youtube.com/watch?v=d3jhKXYM-CY

-baixar musicas .mp3:
  para baixar apenas o audio contido no video, use a op�ao "-only_audio" ou "--only_audio" antes ou dps das urls fornecidas, ex:
	getvid https://www.youtube.com/watch?v=d3jhKXYM-CY --only_audio

-escolher uma pasta especifica para os videos/audios:
  por padrao, o getVid.exe salva os arquivos na pasta de Desktop do usuario, porem � possivel especificar o diretorio com o "-o" ou "--output", ex:
	getvid https://www.youtube.com/watch?v=d3jhKXYM-CY -o c:\users\nome_de_usuario\videos 
  obs: as vezes pode ocorrer erros ao salvar o video por conta do nome da pasta que esta sendo salva, sendo assim tente com um outro diretorio com um nome comum e de preferencia sem acentos.

-escolher o nome do video/audio:
  por padrao, o getVid.exe salva os arquivos com o nome que esta no titulo do video no youtube (removendo os caracteres especiais se houver pois o Windows nao aceita), mas para especificar o nome pode ser usado a flag "-n" ou "--name", ex:
	getvid https://www.youtube.com/watch?v=d3jhKXYM-CY -n meu_video.mp4 (lembrando que a extensao do arquivo nao � necessaria)

-escolher apenas uma parte do audio ou video para ser baixado:
  tambem � possivel escolher uma parte especifica do video para baixar, sendo o inicio usando a flag "-b" ou "--begin" e o final com a flag "-e" ou "--end", sendo tambem possivel utilizar apenas uma delas (se apenas a "-b" foi especificada, ira baixar o video do tempo informado como inicial ate o final e se apenas a "-e" foi informada, vai baixar o video do come�o ate esse tempo especificado).
   OBS: o formato de tempo a ser utilizado deve ser (hh:mm:ss). exs:
	- getvid https://www.youtube.com/watch?v=d3jhKXYM-CY -b 1:25 -e 3:35
	- getvid https://www.youtube.com/watch?v=d3jhKXYM-CY -b 0:50
	- getvid https://www.youtube.com/watch?v=d3jhKXYM-CY --end 1:40
	- getvid https://www.youtube.com/watch?v=d3jhKXYM-CY -b 1 -e 3  (o video sera baixado do primeiro ao terceiro minuto)

-baixar uma playlist:
  � possivel tambem baixar uma playlist inteira com videos/audios do youtube, usando a op�ao "-p" ou "--playlist"
  OBS: quando a url da playlist for selecionada, � necessario utilizar aspas entre o come�o e o fim dela.
  OBS2: so � possivel baixar uma playlist por vez.
  ex:
	- getvid "https://www.youtube.com/watch?v=mxBauZxV9Us&list=PL84BF136B93C5B8EB" --playlist
	- getvid "https://www.youtube.com/watch?v=mxBauZxV9Us&list=PL84BF136B93C5B8EB" --playlist -b 0:50
	
 