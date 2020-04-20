import cv2
from pytesseract import image_to_string
import threading
from espeak import espeak
from textblob import TextBlob

class oculus:
    def __init__(self):
        self.voice = espeak
        self.voice.set_voice('en-us')
        self.voice.set_parameter(espeak.Parameter.Pitch,60)
        self.voice.set_parameter(espeak.Parameter.Rate, 160)
        self.voice.set_parameter(espeak.Parameter.Volume, 70)
        #self.face_cascade = cv2.CascadeClassifier('.model/haarcascade_frontalface_default.xml')
        #self.eye_cascade = cv2.CascadeClassifier('.model/haarcascade_eye.xml')

        #en-scottish
        #english_wmids
        #other/en-rp
        #english-north
        
    def language_detector(self, words):
        self.word_ocr = words
        self.word_ocr = TextBlob(self.word_ocr)
        language = self.word_ocr.detect_language()
        if language == 'sw':
            self.voice.set_voice('sw')
        else:
            self.voice.set_voice('en-us')

    def cleaner(self, textual):
        #===================cleaning the txt =============
        self.textual = textual
        self.textual = self.textual.lower()
        self.textual = self.textual.replace('=', ' ')
        self.textual = self.textual.replace('#', ' ')
        self.textual = self.textual.replace('/', ' ')

        #===================corecting spelling ===============
        self.textual_spell = TextBlob(self.textual).correct()
        return self.textual

    def remove_invalid_words(self, words):
        self.words = words
        self.words_list = self.words.split(' ')
        self.spaces = ' '
        self.clean_words  =  self.spaces
        for word in self.words_list:
            if 'a' in word or 'e' in word or 'i' in word or 'o' in word or 'u' in word:
                self.clean_words = self.clean_words+word+self.spaces
            else:
                continue
        return self.clean_words

    def body(self):
        self.windowname = 'Oculus Inc'
        cv2.namedWindow(self.windowname)
        self.cap = cv2.VideoCapture(0)

        #=========setting resolution=============
        self.cap.set(3, 1080)
        self.cap.set(4, 720)

        print('The resulution of the camera is {} x {}'.format(self.cap.get(3), self.cap.get(4)))

        #===========frame manipulation ============
        if self.cap.isOpened():
            self.ret, self.frame = self.cap.read()
        else:
            self.ret = False

        while self.ret:
            self.ret, self.frame = self.cap.read()
            self.frame_color = self.frame
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.frame = cv2.GaussianBlur(self.frame, (5, 5), 3)
            cv2.imshow(self.windowname, self.frame_color)
            if cv2.waitKey(1) == ord('a'):
                self.information = image_to_string(self.frame)
                if self.information:
                    self.information = str(self.cleaner(self.information))
                    self.information = str(self.remove_invalid_words(self.information))
                    #self.language_detector(self.information)
                    print(self.information)
                    self.voice.synth(self.information)
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()
        self.cap.release()
ai = oculus()
if __name__ == '__main__':
    ai.body()
