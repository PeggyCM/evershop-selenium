import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg
import test_LAB_LOGIN as loginS
import Test_LAB_CT_FONCTIONS_CATEG as fonction

class TestSupprCateg:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    # ✅ Test de suppression de catégorie
    def test_supp_category(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)
        
        fonction.FonctionUtilesCateg.aller_categ(self,driver)

        #je choisis de supprimer toute les catégories
        ligne_Asupprimer = 0

        #coche le bouton radio correspondant dans la liste des categories
        fonction.FonctionUtilesCateg.cocher_bouton_radio_categ(self,driver,ligne_Asupprimer)
    
        fonction.FonctionUtilesCateg.cliquer_lien_delete_categ(self,driver)
    
        fonction.FonctionUtilesCateg.bouton_delete_modal(self,driver)
        fonction.FonctionUtilesCateg.verifier_table_categ_pdt_vide(self,driver)

        

