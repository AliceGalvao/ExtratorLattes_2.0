# ExtratorLattes_2.0

Meio de contato para as infos (_ususario + senha + arquivo de confuguração_ da VPN e _usuario + senha_ para acesso à maquina):
infraestrutura.dtic@upe.br

Acessar o Putty:
- baixar a versão adequada em --> https://openvpn.net/connect-docs/connect-for-windows.html
- Configurar a VPN (com as infos fornecidas)
- Baixe o Putty --> https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- Configurar o Putty (com as infos fornecidas)
- Conectar a VPN
- Fazer login usando usuário:sistemas (existem outros) e colocar a senha

Para rodar o código dentro da máquina da UPE:
- Entrar no repositório (repositório atual sistemas/ExtratorLattes_2.0)
      Obs: usar o comando 'ls' se houver dificuldade para encontrar a pasta
- Ativar o amiente virtual
- para rodar 'python run app.py'
-> 'git checkout' par a ir para a branch escolhida
--> Lembrar de dar 'git pull' para garantir que o repositório está atualizado
---> É possível fazer alterações diretamente pelo put usando 'nano' (não recomendado)
----> Git push para enviar para esse repositório (provavelmente precisará de um token==senha para prosseguir) *

Comandos muito utilizados no Putty:
- venv/bin/activate (ativar a venv)
- lsof -i :8050 (quando a porta for 8050 para achar o processo que está rodando na porta) 
- kill -9 <PID> (matar o processo)
- ifconfig (encontrar os ips)
- nano <nome_do_arquivo> (para editar, deletar, escrever os arquivos diretamente)
- htop: mostra com detalhes todos os processos rodando na máquina, há também a possibilidade de interação
- ps: esse comando fornece um snapshot estático de todos os processos em execução, mostrando informações como PID, TTY, tempo de execução e nome do comando

* Do Putty para o GitHub:
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

Sobre o deploy:
- sudo suporte/extrator_lattes/deploy_old.sh
  Obs1: deve estar fora de 'suporte' use 'cd ..' e 'ls' para conseguir navegar entre as pastas
  Obs2: a senha é a mesma do usuario:sistemas
- systemctl daemon-reload
- sudo systemctl status dash_app.service (aepnas para verificar o status do serviço)

Para novos repositório e/ou atualizações:
- Para facilitar a adição do repositório na máquina: Deixar o rep público quando clonar do GitHub
- Deve ser atualizado anualmente para garantir que os anos de corte estejam atualizados e as medianas também
