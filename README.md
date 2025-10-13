# ExtratorLattes_2.0

Meio de contato para as infos:
infraestrutura.dtic@upe.br

Acessar o Putty:
- baixar a versão adequada em --> https://openvpn.net/connect-docs/connect-for-windows.html
- Configurar a VPN (com as infos fornecidas) e se mantenha conectado
- Baixe o Putty --> https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- Configurar o Putty (com as infos fornecidas)
- Fazer login usuário:sistemas (existem outros) e colocar a senha
- Entrar no repositório
- Ativar o amiente virtual
- rodar app.py

Comandos muito utilizados no Putty:
- venv/bin/activate (ativar a venv)
- lsof -i :8050 (quando a porta for 8050 para achar o processo que está rodando na porta) 
- kill -9 <PID> (matar o processo)
- ifconfig (encontrar os ips)
- nano <nome_do_arquivo> (para editar, deletar, escrever os arquivos diretamente)

Do Putty para o GitHub:
- Passo 1: Gerar um token no GitHub
    - Vá para https://github.com/settings/tokens
    - Clique em "Tokens (classic)"
    - Clique em "Generate new token"
    - Dê um nome (ex: Git push token)
    - Selecione a validade
    - Marque a permissão repo
    - Clique em Generate token
    - Copie o token gerado. Você só verá ele uma vez.
- Passo 2: Usar o token como “senha” no terminal
    - Agora, quando o terminal pedir:
    - Username: seu nome de usuário do GitHub (AliceGalvao, por exemplo)
    -Password: cole o token gerado, não sua senha do GitHub

rodar o app:
python run app.py

Sobre o deploy:
- sudo suporte/extrator_lattes/deploy_old.sh
- sudo systemctl status dash_app.service
- systemctl daemon-reload
OBS:
Para facilitar a adição do repositório na máquina: Deixar o rep público quando clonar do GitHub
