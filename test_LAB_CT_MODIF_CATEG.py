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

        fonction.FonctionUtiles.aller_categ(self,driver)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".main-content-inner"))) 
            
        liste_categ = driver.find_elements(By.CSS_SELECTOR, ".listing > tbody > tr > td > div > a")
                       
        for item in liste_categ:
            if cfg.CATEGORY_NAME_old in item.text and item.text == cfg.CATEGORY_NAME_old:
                item.click()  # Cliquer sur l'élément correspondant
                break  # Sortir de la boucle une fois l'élément trouvé et cliqué

        # Modifier le formulaire 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
    
        inputAModif = driver.find_element(By.NAME, "name").clear()
        inputAModif = driver.find_element(By.NAME, "name").send_keys(cfg.CATEGORY_NAME_new)
    
        # Sauvegarder la catégorie
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.primary[type='button']"))).click()

        #test du toast
        toast=fonction.FonctionUtiles.verifier_toast(self,driver)
        assert "Category saved successfully!" in toast.text
