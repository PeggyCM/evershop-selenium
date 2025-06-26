import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config as cfg
import test_LAB_LOGIN as loginS
import Test_LAB_CT_FONCTIONS_CATEG as fonction


class TestModifCateg:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    # ✅ Test de modification de catégorie
    def test_modif_category(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)

        fonction.FonctionUtilesCateg.aller_categ(self,driver)

        #chercher un nom de parent dans la liste
        fonction.FonctionUtilesCateg.chercher_element_dans_liste(self,driver,
            ".main-content-inner",".listing > tbody > tr > td > div > a",cfg.CATEGORY_NAME_old)

        # Modifier le nom de la categorie
        fonction.FonctionUtilesCateg.remplir_nom_categ_pdt(self,driver,cfg.CATEGORY_NAME_new)
    
        # Sauvegarder la catégorie
        fonction.FonctionUtilesCateg.sauver_categ_pdt(self,driver)

        #test du toast
        message = "Category saved successfully!"
        fonction.FonctionUtilesCateg.verifier_toast(self,driver,message)
        
        # Attend que le titre devienne "Editing" + nom_categ
        fonction.FonctionUtilesCateg.verifier_page_categ_pdt_apres_sauver(self,driver,cfg.CATEGORY_NAME_new) 