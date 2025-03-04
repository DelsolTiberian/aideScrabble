from tkinter import *
from tkinter import ttk
from tkinter.font import *
from tkinter.messagebox import showerror
from string import ascii_uppercase



def verifieWord(userLetters):
    """
       Renvoie un dictionnaire avec tout les mots possibles d'écrire avec les lettres disponibles et la lettre qu'il manquerait
       Entree: chaine de caractère
       Sortie:
    """
    lWords=open("refMots.txt","r").read().split()
    validWords={}
    for word in lWords:
        userLetters=doubleLetter(userLetters)
        missedLetter=''
        i=1
        #rajoute des points au mot si l'utilisateur possède des joker
        if "*" in userLetters:

            i+=userLetters["*"]
        #Parcours chaque mots pour savoir si le mot est valide
        for letter in word:
            if letter in userLetters and userLetters[letter]>0:
                i+=1
                userLetters[letter]-=1
            else:
                missedLetter=letter
        #vérifie le nombre de points du mots
        if i >=len(word):
            validWords[word]=missedLetter
    return(validWords)



def doubleLetter(uLetters):
    """
       Regarde si l'utilisateur a des lettres doubles
       Entree: chaine de caractère
       Sortie: Dictionnaire avecles lettres et leur nombres d'apparitions dans la chaine de caractère
    """
    dicLetters={}
    for l in uLetters:
        if l not in dicLetters:
            dicLetters[l]=1
        else:
            dicLetters[l]+=1
    return(dicLetters)



def wordPoint(lWords, uLetter):
    """
       Renvoie un dictionnaire associant les mots et leur nombres de points
       Entree: lWords: mots valides
               haveJoker: nombre de joker de l'utilisateur
       Sortie:dictionnaire associant mots et nombres de points
    """
    letterPoints={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':10,'L':1,'M':2,'N':1,'O':1,'P':3,'Q':8,'R':1,'S':1,'T':1,'U':1,'V':4,'W':10,'X':10,'Y':10,'Z':10}
    wordPoints={}
    for word in lWords:
        wordPoints[word]=0
        if len(word)>=7:
            wordPoints[word]+=50
        for l in word:
            if l in uLetter or l==lWords[word]:
                wordPoints[word]+=letterPoints[l]

    return(wordPoints)



def tri(dict):
    """
       Entree: tableau
       Sortie: tableau trié
    """
    triedTab=[]
    for word in dict:
        triedTab.append(word)
    #tri insertion adapté pour comparer avec les valeurs du dictionnaire
    for i in range(1, len(triedTab)):
        k = triedTab[i]
        j = i-1
        while j >= 0 and dict[k] > dict[triedTab[j]] :
                triedTab[j + 1] = triedTab[j]
                j -= 1
        triedTab[j + 1] = k
    return(triedTab)




def main(letter):
    """
       Crée la liste des mots valides, de leurs points et leurs lettres manquantes
       Entrée: chaîne de caractères contenant 7 lettres
    """
    validWordsMissedLetter=verifieWord(letter)
    validWordsValue=wordPoint(validWordsMissedLetter, letter)
    validWordsTried=tri(validWordsValue)

    #Affichage console
    i=0
    print("Mots possibles:")
    for word in validWordsTried:
        i+=1
        if validWordsMissedLetter[word] != '':
            print(f"{word} (+{validWordsMissedLetter[word]})     {validWordsValue[word]} pts\n")
        else:
            print(f"{word} (lettre au choix)     {validWordsValue[word]} pts\n")

    #Affichage fenetre
    i=0
    content=''
    for word in validWordsTried:
        i+=1
        if validWordsMissedLetter[word] != '':
            content+=f"{word} (+{validWordsMissedLetter[word]})     {validWordsValue[word]} pts\n"
        else:
            content+=f"{word} (lettre au choix)     {validWordsValue[word]} pts\n"
    wordsList.config(text=content)




def init():
    """
       Appelle la fonction principale en lui donnant les lettres rentrées par l'utilisateur en guise d'arguments
    """
    letter=entryLetters.get()
    letter=letter.replace(" ", "").upper()
    #vérifie si tous les caractères sont valides
    alphabet=list(ascii_uppercase)
    alphabet.append('*')
    i=True
    for l in letter:
        if l not in alphabet:
            i=False
            break
    if len(letter)==7 and i==1:
        main(letter)
    #Gère les erreurs, de saisie ou de nombre de lettres
    elif i!=1:
        showerror("Erreur de saisie", "Votre saisie est invalide, seul les caractères alphabétique et le * pour le joker sont acceptés")
    else:
        showerror("Erreur de saisie", "Il vous faut saisir 7 lettres")


#Crée la fenêtre
app=Tk()
app.title("Aide au scrabble")
app.minsize(800, 600)


#Creation des widgets
fontStyle= Font(family='Times New Roman', size=35, weight="bold")
labelOrder = Label(app, text="Veuillez entrer vos lettres :", font=fontStyle, justify="center")
entryLetters = Entry(app)
wordsListFrame= LabelFrame(app, text='Liste des mots utilisables', height=500,width=500)
wordsList = Label(wordsListFrame, text="")
scrollBar=Scrollbar(wordsListFrame,orient="vertical")


#creation du boutton pour soumettre nos lettres
submitButton = Button(app, text="Continuer", command=init)
labelOrder.pack()
entryLetters.pack()
submitButton.pack()
wordsListFrame.pack()
wordsList.pack()
scrollBar.pack(side="right",fill="y")

#affiche la fenêtre
app.mainloop()