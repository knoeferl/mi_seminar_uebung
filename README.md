# mi_seminar_uebung

# Übungen Action Regognition

Michael Knöferl

Michael.Knoeferl@sutdent.fhws.de

## Installation

Für diese Übung sollte keine Installation auf eurem System notwendig sein.

Ihr könnte Sie über Google Colab ausführen. 

Hierzu wird jedoch ein Google Konto benötigt.

Falls ihr dies nicht habt und keines anlegen wollt könntet ihr die Übung auch auf einem Linux System durchführen.
Da hier aber mehrere Schritte nötig sind, führe ich dies hier nicht auf. Ihr könnt euch dann gerne an mich wenden und ich helfe euch bei der Installation.

Die Daten liegen auf Github:
https://github.com/knoeferl/mi_seminar_uebung

Öffnet die Datei:

https://github.com/knoeferl/mi_seminar_uebung

Hier findet ihr einen Link der das Dokument in Google Colab öffnet.
https://colab.research.google.com/github/knoeferl/mi_seminar_uebung/blob/main/uebung_Aktivtaetserkennung.ipynb

Ihr könnt euch eine Instanz mit GPU holen und die Übung durchführen.

Beim ersten ausführen kommt eine Warnung, dass das Dokument auf die Google Drive Daten zugreifen kann.

Links könnt ihr auf ein Inhaltverzeichnis zugreifen um zu den einzelnen Übungen zu gelangen.

Die Stellen an dennen ihr Code einfügen sollt sind mit Kommentaren gekennzeichnet.


## Übungen

### Aufgabe 1: Schreibe ein LSTM

Im durch Kommentare gekennzeichneten Bereich schreibe ein Aufruf für die LSTM Funktion von Pytorch.

Doku LSTM: https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html

Ihr könnte hier mit der Anzahl der Hiddenlayer Spielen und sehen wie sich die Resultate verändern.
Die Anzahl der Hiddenlayer muss bei der Linear Funktion als erster Parameter mit hinein geben werden.

Doku LINEAR: https://pytorch.org/docs/stable/generated/torch.nn.Linear.html

### Aufgabe 2: LSTM laufen lassen
Hier könnt ihr die Anzahl der Epochen verändern und in den nachfolgenden Cellen betrachten wie sich die Resultate verändern.

### Aufgabe 3: Features berechnen

#### a) schreibe die Funktion calc_angle welche die Winkelveränderung zwischen zwei Bildern zurück gibt

#### b) schreibe die Funktion calc_euclidan welche den Euklisichen Abstand zwischen zwei Punkten zurück gibt

### Aufgabe 4: Ändere den Regulierungsparameter C und betrachte wie sich die Resultate verändern

Doku SVM: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

## Erwähnungen
Übungen basieren auf diesem Artikel https://blog.etereo.io/detecting-poses-with-openpose-in-google-colab-d591dc8d8609, diesem Repo https://github.com/shah-deven/Action-Classification-using-CNN-and-LSTM
und den Pytorch Beispielen zu LSTM und den Scikit-learn Beispielen zu SVM die es auf den offiziellen Seiten zu finden sind.

