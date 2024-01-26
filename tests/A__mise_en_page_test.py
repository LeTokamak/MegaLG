from datetime import datetime
import os
import sys

os.chdir(f"{os.getcwd()}\\src")
sys.path.append(os.getcwd())

from A___mise_en_page import AjoutZerosAvant, de_dApostrophe, MeF_Prenom, MeF_Pseudo, mois, JSemaine, strDate, RGB_intHexa

import unittest

class TestMiseEnPage(unittest.TestCase):
    
    def test_AjoutZerosAvant(self):
        self.assertEqual(AjoutZerosAvant(   17, 5), '00017'   )
        self.assertEqual(AjoutZerosAvant(   17, 2), '17'      )
        self.assertEqual(AjoutZerosAvant(   17, 0), '17'      )
        self.assertEqual(AjoutZerosAvant(99.36, 5), '00099.36')
        self.assertEqual(AjoutZerosAvant(99.36, 2), '99.36'   )
        
    def test_d_apostrophe(self):
        self.assertEqual(de_dApostrophe("pin")          , "de pin"    )
        self.assertEqual(de_dApostrophe("alain")        , "d'alain"   )
        self.assertEqual(de_dApostrophe("haricot", True), "De haricot")
        
    def test_MeF_Prenom(self):  
        self.assertEqual(MeF_Prenom("   JeAn-cléMENt frANçoiS       "), "Jean-Clément François")
        self.assertEqual(MeF_Prenom("  toto  tata  titi  "), "Toto Tata Titi")
        
    def test_MeF_Pseudo(self):
        self.assertEqual(MeF_Pseudo("abcdef"), "Abcdef")
        self.assertEqual(MeF_Pseudo(" toto  tata  titi "), "Toto tata titi")
        
    def test_mois(self):
        self.assertEqual(mois( 1), "Janvier")
        self.assertEqual(mois( 2), "Février")
        self.assertEqual(mois(10), "Octobre")
    
    def test_JSemaine(self):
        self.assertEqual(JSemaine(0), "Lundi")
        self.assertEqual(JSemaine(1), "Mardi")
        self.assertEqual(JSemaine(4), "Vendredi")
        
    def test_strDate(self):
        date = datetime(2021, 11, 30)
        
        self.assertEqual(strDate(date, type_format = 0), "Mardi 30 Novembre 2021")
        self.assertEqual(strDate(date, type_format = 1), "Mardi 30 Novembre")
        self.assertEqual(strDate(date, type_format = 2), "Mar 30 Nov")
        self.assertEqual(strDate(date, type_format = 3), "30 Novembre 2021")
        self.assertEqual(strDate(date, type_format = 4), "30 Novembre")
        self.assertEqual(strDate(date, type_format = 5), "30/11")
    
    def test_RGB_intHexa(self):
        self.assertEqual(RGB_intHexa(255, 255, 255), 255*16**4 + 255*16**2 + 255 ) # "#ffffff"
        self.assertEqual(RGB_intHexa(  0,   0,   0), 0                           ) # "#000000"
        self.assertEqual(RGB_intHexa(  0,   0, 255), 255                         ) # "#0000ff"
        self.assertEqual(RGB_intHexa(  0, 255,   0), 255*16*16                   ) # "#00ff00"
        self.assertEqual(RGB_intHexa(255,   0,   0), 255*16*16*16*16             ) # "#ff0000"
        

if __name__ == '__main__':
    unittest.main()