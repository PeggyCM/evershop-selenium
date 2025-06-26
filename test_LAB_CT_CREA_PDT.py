# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
import random
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import os  # Pour gérer les chemins de fichiers
import time  # Pour attendre un court instant
from selenium.webdriver.common.action_chains import ActionChains  # Pour utiliser les Actions de Selenium
import test_LAB_LOGIN as loginS
import Test_LAB_CT_FONTIONS_PDT as fonctionP
import Test_LAB_CT_FONCTIONS_CATEG as fonctionC
import config as cfg


class TestCreaPdt:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    # ✅ Test de création de produit vide
    def test_crea_vide(self,driver):
        loginS.TestLogin.login_success(self,driver)
        # Cliquer sur "New products"
        fonctionP.FonctionUtilesPdt.aller_new_pdt(self,driver)
        fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
        fonctionP.FonctionUtilesPdt.verifier_champs_empty_pdt(self,driver)
        
     # ✅ Test de création de produit
    def test_crea_pdt(self,driver):
        loginS.TestLogin.login_success(self,driver)

        #creation de 3 produits en passant par products et new product
        for i in range(3):
            fonctionP.FonctionUtilesPdt.aller_pdt(self,driver)
            fonctionP.FonctionUtilesPdt.aller_new_pdt_par_pdt(self,driver)
            
            # Remplir le formulaire pour le nouveau produit
            fonctionC.FonctionUtilesCateg.remplir_nom_categ_pdt(self,driver,cfg.PRODUCT_NAME[i])
            driver.find_element(By.NAME, "url_key").send_keys(cfg.PRODUCT_URL_KEY + f"{cfg.PRODUCT_NAME[i]}{i:03d}")
            fonctionC.FonctionUtilesCateg.upload_photo_categ(self,driver,cfg.FILE_PATH)
            fonctionP.FonctionUtilesPdt.remplir_sku(self,driver,cfg.PRODUCT_SKU,i)
            fonctionP.FonctionUtilesPdt.remplir_price(self,driver,cfg.PRODUCT_PRICE)
            fonctionP.FonctionUtilesPdt.remplir_weight(self,driver,cfg.PRODUCT_WEIGHT)
            fonctionP.FonctionUtilesPdt.cliquer_lien_categ_new_pdt(self,driver)
            fonctionP.FonctionUtilesPdt.remplir_categorie_pdt(self,driver,cfg.PRODUCT_CATEG[i])
            fonctionP.FonctionUtilesPdt.cliquer_bouton_radio(self,driver)
            
            fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
            fonctionC.FonctionUtilesCateg.verifier_page_categ_pdt_apres_sauver(self,driver,cfg.PRODUCT_NAME[i])
            
# ✅ Test de création de produit    
    def test_crea_pdtN(self,driver):
        loginS.TestLogin.login_success(self,driver)

        for i in range(3,6,1):
            # Cliquer sur "New products"
            fonctionP.FonctionUtilesPdt.aller_new_pdt(self,driver)

            # Remplir le formulaire pour le nouveau produit
            fonctionC.FonctionUtilesCateg.remplir_nom_categ_pdt(self,driver,cfg.PRODUCT_NAME[i])
            driver.find_element(By.NAME, "url_key").send_keys(cfg.PRODUCT_URL_KEY + f"{cfg.PRODUCT_NAME[i]}{i:03d}")
            fonctionC.FonctionUtilesCateg.upload_photo_categ(self,driver,cfg.FILE_PATH)
            fonctionP.FonctionUtilesPdt.remplir_sku(self,driver,cfg.PRODUCT_SKU,i)
            fonctionP.FonctionUtilesPdt.remplir_price(self,driver,cfg.PRODUCT_PRICE)
            fonctionP.FonctionUtilesPdt.remplir_weight(self,driver,cfg.PRODUCT_WEIGHT)
            fonctionP.FonctionUtilesPdt.cliquer_lien_categ_new_pdt(self,driver)
            fonctionP.FonctionUtilesPdt.remplir_categorie_pdt(self,driver,cfg.PRODUCT_CATEG[i])
            fonctionP.FonctionUtilesPdt.cliquer_bouton_radio(self,driver)
            
            fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
            fonctionC.FonctionUtilesCateg.verifier_page_categ_pdt_apres_sauver(self,driver,cfg.PRODUCT_NAME[i])
            
    # ✅ Test de création de produit doublon
    def test_crea_doublon(self,driver):
        loginS.TestLogin.login_success(self,driver)
        # Cliquer sur "New products"
        fonctionP.FonctionUtilesPdt.aller_new_pdt(self,driver)
        #test de sku en doublon
        driver.find_element(By.NAME, "name").send_keys("X")
        driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").send_keys(cfg.sku_doublon)
        driver.find_element(By.CSS_SELECTOR, "input[name='price'][placeholder='Price']").send_keys(2)
        driver.find_element(By.CSS_SELECTOR, "input[name='weight'][placeholder='Weight']").send_keys(2)
        driver.find_element(By.CSS_SELECTOR, "input[name='qty'][placeholder='Quantity']").send_keys(2)
        driver.find_element(By.NAME, "url_key").send_keys("A")

        # Attente et clic sur le bouton Save
        fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
        fonctionC.FonctionUtilesCateg.verifier_toast(self,driver,cfg.msgSkuDoublon)
       
        # Attendre que le bouton de fermeture du toast soit cliquable
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Toastify__close-button"))).click()
        #test de url en doublon
        driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").clear()
        driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").send_keys("A")
        driver.find_element(By.NAME, "url_key").clear()
        driver.find_element(By.NAME, "url_key").send_keys(cfg.url_doublon)
        print("urlkey", cfg.url_doublon)
        time.sleep(5)
    
        # Attente et clic sur le bouton Save
        fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
        fonctionC.FonctionUtilesCateg.verifier_toast(self,driver,cfg.msgUrlDoublon)