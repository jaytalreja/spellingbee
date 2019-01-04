from os import system 
import time
import datetime
import random
import subprocess
f=open('2019SpellitList.csv')
words = f.read()
words= words.split('\n')
words = [word for word in words if len(word)> 1 and word[0] != '%']
fw=open('remember_words.csv','w')
fw.write('Spelling Practice on : %s'%datetime.datetime.now())
fw.write('\n')
def sayWord(word):
  speech="osascript -e 'say \""+word+"\"'"
  system(speech)

def chooseWord(upperBound): 
  #word=words[random.randint(0,len(words)-1)]
  word=words[random.randint(0,upperBound)]
  return word

def showDialog(word):
  sayWord(word)
  command = "osascript -e 'Tell application \"System Events\" to display dialog \""+word+"\" buttons {\"Repeat\",\"Remember\",\"Next\"}'"
  #system(command)
  p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  p_status = p.wait()
  return output


def chooseAndSayWord(upperBound,word):
  if not word:
  	word = chooseWord(upperBound)
  output = showDialog(word)
  if "Repeat" in output:
    sayWord("Repeating the word")
    chooseAndSayWord(upperBound,word)
  if "Remember" in output:
    fw.write(word)
    fw.write('\n')

if __name__=="__main__":
   for i in xrange(50):
     chooseAndSayWord(250,"")
     #time.sleep(1)
