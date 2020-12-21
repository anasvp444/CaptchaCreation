# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 10:57:55 2020

@author: User
"""
import wx
import wx.xrc

import cv2


import os, random
import cv2, argparse
import numpy as np


backgroundlist = os.listdir('background')


def image_augmentation(img, type2=False):

    w, h, _ = img.shape
    pts1 = np.float32([[0, 0], [0, w], [h, 0], [h, w]])

    begin, end = 30, 90
    pts2 = np.float32([[random.randint(begin, end), random.randint(begin, end)],
                       [random.randint(begin, end), w - random.randint(begin, end)],
                       [h - random.randint(begin, end), random.randint(begin, end)],
                       [h - random.randint(begin, end), w - random.randint(begin, end)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)

    img = cv2.warpPerspective(img, M, (h, w))

    # Brightness
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = .4 + np.random.uniform()
    img[:, :, 2] = img[:, :, 2] * random_bright
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    # Blur
    blur_value = random.randint(0,4) * 2 + 1
    img = cv2.blur(img,(blur_value, blur_value))
    if type2:
        return img[130:280, 180:600, :]
    return img[130:280, 120:660, :]


class ImageGenerator:
    def __init__(self, ):

        # Plate
        self.plate = cv2.imread("plate.jpg")

        # loading Number
        file_path = "num/"
        file_list = os.listdir(file_path)
        self.Number = list()
        self.number_list = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)

            self.Number.append(img_path)
            self.number_list.append(file)



    def createPlate(self,givenYear):
                #char = self.Char1
                number = self.Number

                Plate = cv2.resize(self.plate, (520, 110))
                b_width ,b_height = 800, 400

                rand_int = random.randint(0, len(backgroundlist))
                background = cv2.imread('background/'+backgroundlist[rand_int])

                

                label = ""
                # row -> y , col -> x
                row, col = 13, 155  # row + 83, col + 56

                givenYeararray = [int(i) for i in str(givenYear)]

                # number 4
                rand_int = givenYeararray[0]#random.randint(0, 9)
                label += self.number_list[rand_int]
                numImg = cv2.imread(number[rand_int]+'/'+str(random.randint(0, 24))+'.jpg')
                h,w,_= numImg.shape
                Plate[row:row + h, col:col + w, :] = numImg
                col += w

                # number 5
                rand_int = givenYeararray[1]#random.randint(0, 9)
                label += self.number_list[rand_int]
                numImg = cv2.imread(number[rand_int]+'/'+str(random.randint(0, 24))+'.jpg')
                h,w,_= numImg.shape
                Plate[row:row + h, col:col + w, :] = numImg
                col += w

                # number 6
                rand_int = givenYeararray[2]#random.randint(0, 9)
                label += self.number_list[rand_int]
                numImg = cv2.imread(number[rand_int]+'/'+str(random.randint(0, 24))+'.jpg')
                h,w,_= numImg.shape
                Plate[row:row + h, col:col + w, :] = numImg
                col += w

                # number 7
                rand_int = givenYeararray[3]#random.randint(0, 9)
                label += self.number_list[rand_int]
                numImg = cv2.imread(number[rand_int]+'/'+str(random.randint(0, 24))+'.jpg')
                h,w,_= numImg.shape
                Plate[row:row + h, col:col + w, :] = numImg
                col += w


                s_width, s_height = int((400-110)/2), int((800-520)/2)
                background[s_width:110 + s_width, s_height:520 + s_height, :] = Plate
                background = image_augmentation(background)
                return cv2.resize(background,(270,75))    
        
    def Type_1(self, givenYearList):
        page = cv2.imread('page.jpg')
        plate= self.createPlate(givenYearList[0])

        x= 300
        y = 300
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate
        
        plate = self.createPlate(givenYearList[1])
        x= 600
        y = 300
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate

        plate = self.createPlate(givenYearList[2])
        x= 300
        y = 400
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate

        plate = self.createPlate(givenYearList[3])
        x= 600
        y = 400
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate

        plate = self.createPlate(givenYearList[4])
        x= 300
        y = 500
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate

        plate = self.createPlate(givenYearList[5])
        x= 600
        y = 500
        page [y:y+plate.shape[0],x:x+plate.shape[1]] = plate       
        cv2.imwrite('out.jpg',page)

    
def GenerateYearList(year = 2000):
    
    yearlist = []
    youngYear =2005 
    for i in range(3):
        rand = random.randint(1, 8)  if i%2 == 0 else -random.randint(1, 5) #exclude 0
        yearlist.append(youngYear + rand)
    
    year = year - random.randint(5, 25)
    for i in range(3):
        rand = random.randint(1, 5)  if i%2 == 0 else -random.randint(1, 5) #exclude 0
        yearlist.append(year + rand)
    return  yearlist
   
def GenerateCaptchaDB(givenYear):
    yearlist = GenerateYearList(year = givenYear)
    random.shuffle(yearlist)
    return (yearlist)


class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"What is your age?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.ALIGN_CENTER, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY,wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_bitmap1, 0, wx.ALL, 5 )

		self.SetSizer( bSizer1 )
		self.Layout()
		self.bSizer1 = bSizer1
		self.Centre( wx.BOTH )
		self.Show(True)
		self.m_button1.Bind(wx.EVT_BUTTON, self.createCaptcha)
	def createCaptcha(self, event):
            try:
                age = int(self.m_textCtrl1.GetValue())
                if age > 100 or age < 5:
                    raise Exception("Sorry, age incorrect")
                year = 2020 - age
                A = ImageGenerator()
                A.Type_1(givenYearList = GenerateCaptchaDB(year)  )
                img = wx.Image('out.jpg', wx.BITMAP_TYPE_ANY)
                self.m_bitmap1.SetBitmap(wx.Bitmap(img))
                self.SetSizer( self.bSizer1 )
                self.Layout()
            except:
                print('put correct age')
        
        
	
	def __del__( self ):
		pass


def main():

    ex = wx.App()
    MyFrame(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
