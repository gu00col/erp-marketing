#!/usr/bin/expect
spawn ssh-add
expect "Enter passphrase for /home/luisoliveira/.ssh/id_rsa"
send "88077151asd\n";
expect eof
