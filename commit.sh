#!/bin/bash
echo "Adicionando agente"
./ssh-add.sh
echo "Stash nas atualizações da maquina"
ssh  asdihtal@66.29.146.192 -p21098 ./portal.asdigitallab.com.br/stash.sh
echo "Iniciando push"
git add .
echo "Arquivos adicionados"
git commit -a -m "Push Automatizado"
echo "Iniciando o push"
git push --set-upstream origin master

# Iniciando Deploy
# sshpass -p 88077151asd ssh -o StrictHostKeyChecking=no ubuntu@132.226.166.224 "/home/ubuntu/friday/./deploy.sh"
# sshpass -p 88077151asd ssh ubuntu@132.226.166.224 "/home/ubuntu/./deploy.sh"
# ssh -o StrictHostKeyChecking=no ubuntu@132.226.166.224 "/home/ubuntu/./deploy.sh"
echo "Fim do script"