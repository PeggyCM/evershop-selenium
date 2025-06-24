import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config as cfg
import test_lab_login as loginS
import Test_LAB_CT_FONCTIONS as fonction


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
            fonction.FonctionUtiles.aller_categ(self,driver)
            
            fonction.FonctionUtiles.aller_new_categ_par_categ(self,driver)
            
            # Remplir le formulaire pour la nouvelle catégorie
            fonction.FonctionUtiles.remplir_form_categ(self,driver,cfg.CATEGORY_NAME[i],cfg.FILE_PATH)
            driver.find_element(By.NAME, "url_key").send_keys(cfg.URL_KEY + cfg.CATEGORY_NAME[i])
          
            # Sauvegarder la catégorie
            fonction.FonctionUtiles.sauver_categ(self,driver)
            
            #test du toast
            fonction.FonctionUtiles.verifier_toast(self,driver)
            

            # Attend que le titre devienne "Editing" + nom_categ
            WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
            assert ("Editing "+ cfg.CATEGORY_NAME[i]) == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text   

    def test_create_sscategory(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)

        for i in range(3):
            j=0
            for j in range(3):
                fonction.FonctionUtiles.aller_categ(self,driver)
            
                fonction.FonctionUtiles.aller_new_categ_par_categ(self,driver)

                # Remplir le formulaire pour la nouvelle catégorie
                fonction.FonctionUtiles.remplir_form_categ(self,driver,cfg.CATEGORY_NAME[i],cfg.FILE_PATH)    
                driver.find_element(By.NAME, "url_key").send_keys(cfg.URL_KEY + cfg.CATEGORY_NAME[j] + cfg.SSCATEGORY_NAME[i])
            
                # Cliquer sur "Parent"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".text-interactive"))).click()

                #chercher un nom dans une liste
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".category-tree-container"))) 
            
                liste_parents = driver.find_elements(By.CSS_SELECTOR, ".category-tree > li > div > a")
                       
                for item in liste_parents:
                    if cfg.CATEGORY_NAME[j] in item.text:
                        item.click()  # Cliquer sur l'élément correspondant
                        break  # Sortir de la boucle une fois l'élément trouvé et cliqué


                # Sauvegarder la catégorie
                fonction.FonctionUtiles.sauver_categ(self,driver)

                #test du toast
                fonction.FonctionUtiles.verifier_toast(self,driver)
                
                # Attend que le titre devienne "Editing" + nom_categ
                WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
                assert ("Editing "+ cfg.CATEGORY_NAME[i]) == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text   
                