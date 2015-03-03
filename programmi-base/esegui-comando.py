#!/usr/bin/python
# -*- coding: utf-8 -*-
# gd 20140728

import subprocess
output = subprocess.check_output(['ls', '-l'])
# i parametri vengono passati come lista di stringhe
print('Have %d bytes in output' % len(output))
print(output)


#--------------------------------------------------------------
#se il comando ha molte opzioni usare il comando shlex.split che le divide
import shlex
command_line = '/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"'
args = shlex.split(command_line)
print(args)
p = subprocess.Popen(args) # Success! e continua lo script senza aspettare che il comando finisca
#p = subprocess.call(args) # Aspetta che il comando finisca e poi continua lo script




