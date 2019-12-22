from os import system 
import sys
import time
import datetime
import random
import subprocess
#f=open('2019SpellitList.csv')
f=open('SixthGrade.txt')
words = f.read()
words= words.split('\n')
words = [word for word in words if len(word)> 1 and word[0] != '%']
words = words[84:]
fw=open('remember_words.csv','a+')
fw.write('*************************************************\n')
fw.write('Spelling Practice on : %s'%datetime.datetime.now())
fw.write('\n')
correctWords=[]
incorrectWords = []
INDEX=0
def sayWord(word):
  speech="osascript -e 'say \""+word+"\"'"
  system(speech)

def chooseWord(upperBound): 
  #word=words[random.randint(0,len(words)-1)]
  word=words[upperBound]
  #word=words[random.randint(0,upperBound)]
  #word=words[random.randint(389,425)]

  return word.strip()

def showDialog(word,showWord=False):
  sayWord(word)
  if showWord:
    command = "osascript -e 'Tell application \"System Events\" to display dialog \""+word+"\" buttons {\"Next\"} default button \"Next\"'"
  else:
    command = "osascript -e 'Tell application \"System Events\" to display dialog \"Spell the word correctly\" default answer \"\" buttons {\"Repeat\",\"Check\",\"Show\"} default button \"Check\"'"  
    #system(command)
  p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  p_status = p.wait()
  return output


def chooseAndSayWord(idx,word,correctWords,incorrectWords):
  word=chooseWord(idx)
  #if not word:
  #  word = chooseWord(upperBound)
  output = showDialog(word)
  if "Repeat" in output:
     sayWord("Repeating the word")
     chooseAndSayWord(idx,word,correctWords,incorrectWords)
  if "Show" in output:
     incorrectWords.append(word)
     sayWord('%s is spelled as follows'%word)
     for char in word:
        sayWord(char)
     sayWord(word)
     fw.write(word)
     fw.write('\n')
     showDialog(word,showWord=True)
  if "Check" in output and word.upper() not in output.upper():
     #incorrectWords.append(word)
     #fw.write(word)
     #fw.write('\n')
     sayWord("Incorrect spelling, please try again")
     chooseAndSayWord(idx,word,correctWords,incorrectWords)
  if "Check" in output and word.upper() in output.upper():
     correctWords.append(word)

if __name__=="__main__":
   import sys
   args=sys.argv
   #sayWord(args[1]) 
   #sys.exit(0)
   sayWord("Anya is a good girl. Aggi is a good boy.")
   totalWordsToChoose=int(args[1])
   for i in xrange(totalWordsToChoose):
     chooseAndSayWord(i,"",correctWords,incorrectWords)
   percentCorrect=round(float(len(correctWords))/float(totalWordsToChoose)*100)
   percentCorrect=int(percentCorrect)
   sayWord('You spelled %s words correctly out of %s attempted with %s correct percent'%(len(correctWords),totalWordsToChoose,percentCorrect))
   percentCorrect=len(correctWords)/totalWordsToChoose*100
   if percentCorrect <= 50:
     sayWord('Keep practicing to improve your score')
   elif percentCorrect > 50 and percentCorrect <=75:
     sayWord('You can do better')
   elif percentCorrect > 75 and percentCorrect <=90:
     sayWord('Good job. Way to go.')
   elif percentCorrect > 90 and percentCorrect <=99:
     sayWord('Stupendous')
   elif percentCorrect == 100:
     sayWord('Congratulations ! You got it all correct. Yipee')
     
      
   if incorrectWords:
     sayWord('I will repeate the incorrect words again')
     for word in incorrectWords:
       sayWord(word)
       for char in word:
          sayWord(char)
       sayWord(word)
       time.sleep(2)
     
