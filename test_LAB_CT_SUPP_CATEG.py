import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config_login as cfg
import test_LAB_login as loginS
import Test_LAB_CT_FONCTIONS as fonction

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
        
        fonction.FonctionUtiles.aller_categ(self,driver)

        #coche le premier bouton radio de la liste des categories, le générique
        boutonRadio = driver.find_elements(By.CSS_SELECTOR, ".field-wrapper.radio-field")
        boutonRadio[0].click()
    
        delete_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.inline-flex a:nth-of-type(2)")))
        delete_button.click()
    
        fonction.FonctionUtiles.bouton_delete_modal(self,driver)


        final_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.flex.w-full.justify-center")))
        assert "There is no category to display" in final_message.text

