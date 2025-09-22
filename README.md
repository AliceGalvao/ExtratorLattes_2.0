# ExtratorLattes_2.0

Comandos muito utilizados no Putty:
. venv/bin/activate (ativar a venv)
lsof -i :8050 (quando a porta for 8050 para achar o processo que está rodando na porta) 
kill -9 <PID> (matar o processo)
ifconfig (encontrar os ips)
nano <nome_do_arquivo> (para editar, deletar, escrever os arquivos diretamente)

Do Putty para o GitHub:
  Passo 1: Gerar um token no GitHub
    - Vá para https://github.com/settings/tokens
    - Clique em "Tokens (classic)"
    - Clique em "Generate new token"
    - Dê um nome (ex: Git push token)
    - Selecione a validade
    - Marque a permissão repo
    - Clique em Generate token
    - Copie o token gerado. Você só verá ele uma vez.
  Passo 2: Usar o token como “senha” no terminal
    - Agora, quando o terminal pedir:
    - Username: seu nome de usuário do GitHub (AliceGalvao, por exemplo)
    -Password: cole o token gerado, não sua senha do GitHub

rodar o app:
python run app.py

