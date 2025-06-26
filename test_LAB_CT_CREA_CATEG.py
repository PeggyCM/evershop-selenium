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


class TestCreaCateg:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    # ✅ Test de création de catégorie
    def test_create_category(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)

        for i in range(3):
            fonction.FonctionUtilesCateg.aller_categ(self,driver)
            
            fonction.FonctionUtilesCateg.aller_new_categ_par_categ(self,driver)
            
            # Remplir le formulaire pour la nouvelle catégorie
            fonction.FonctionUtilesCateg.remplir_nom_categ_pdt(self,driver,cfg.CATEGORY_NAME[i])
            fonction.FonctionUtilesCateg.upload_photo_categ(self,driver,cfg.FILE_PATH)
            driver.find_element(By.NAME, "url_key").send_keys(cfg.URL_KEY + cfg.CATEGORY_NAME[i])
          
            # Sauvegarder la catégorie
            fonction.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
            
            #test du toast
            message = "Category saved successfully!"
            fonction.FonctionUtilesCateg.verifier_toast(self,driver,message)
            

            # Attend que le titre devienne "Editing" + nom_categ
            fonction.FonctionUtilesCateg.verifier_page_categ_pdt_apres_sauver(self,driver,cfg.CATEGORY_NAME[i])  

    def test_create_sscategory(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)

        for i in range(3):
            j=0
            for j in range(3):
                fonction.FonctionUtilesCateg.aller_categ(self,driver)
            
                fonction.FonctionUtilesCateg.aller_new_categ_par_categ(self,driver)

                # Remplir le formulaire pour la nouvelle catégorie
                fonction.FonctionUtilesCateg.remplir_nom_categ_pdt(self,driver,cfg.SSCATEGORY_NAME[i])
                fonction.FonctionUtilesCateg.upload_photo_categ(self,driver,cfg.FILE_PATH)   
                driver.find_element(By.NAME, "url_key").send_keys(cfg.URL_KEY + cfg.CATEGORY_NAME[j] + cfg.SSCATEGORY_NAME[i])
            
                # Cliquer sur le lien "Parent"
                fonction.FonctionUtilesCateg.cliquer_lien_parent(self,driver)

                #chercher un nom de parent dans la liste
                fonction.FonctionUtilesCateg.chercher_element_dans_liste(self,driver,
                    ".category-tree-container",".category-tree > li > div > a",cfg.CATEGORY_NAME[j])
               
                # Sauvegarder la catégorie
                fonction.FonctionUtilesCateg.sauver_categ_pdt(self,driver)

                #test du toast
                message = "Category saved successfully!"
                fonction.FonctionUtilesCateg.verifier_toast(self,driver,message)
                
                # Attend que le titre devienne "Editing" + nom_categ
                fonction.FonctionUtilesCateg.verifier_page_categ_pdt_apres_sauver(self,driver,cfg.SSCATEGORY_NAME[i])
                