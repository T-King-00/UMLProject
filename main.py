
import os
os.system("pip install -r requirements.txt")

import plantUML,helperFunctions
import spacy

x=helperFunctions.getSentencesFromFile("university.txt")
print(x)


"""
fileName="classtest11"
plantUml1=plantUML.ClassModel(fileName)
plantUml1.addClass("Person")
plantUml1.addClass("Student")
plantUml1.addClass("Doctor")
plantUml1.addGeneralizationRelation("Student","Person")
plantUml1.addGeneralizationRelation("Doctor","Person")
plantUml1.addMorFtoClass("Person","username")
plantUml1.addMorFtoClass("Person","Password",'-')
plantUml1.addMorFtoClass("Student","GPA",'-')
plantUml1.addMorFtoClass("Doctor","Salary",'-')
plantUml1.addAssociationRelation("Student","Doctor")
plantUml1.addClass("Course")
plantUml1.addAssoClass("Student","Doctor","Course")
plantUml1.closeFile()

os.system("python -m plantuml "+ fileName )"""