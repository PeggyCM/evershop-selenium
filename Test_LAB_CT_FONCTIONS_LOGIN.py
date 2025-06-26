import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionUtilesLogin:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

#---------------------------------------------------------------- 
#------------------------ALLER----------------------------------- 
#---------------------------------------------------------------- 
    def ouvrir_url(self,driver):
        """fonction pour ouvrir l'URL"""
        driver.get(cfg.BASE_URL)

#---------------------------------------------------------------- 
#------------------------REMPLIR--------------------------------- 
#---------------------------------------------------------------- 
    def saisir_email(self,driver,email):
        """fonction pour saisir l'email de la connexion"""
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys(email)

    def saisir_mdp(self,driver,mdp):   
        """fonction pour saisir le mot de passe"""
        driver.find_element(By.NAME, "password").clear() 
        driver.find_element(By.NAME, "password").send_keys(mdp)

#---------------------------------------------------------------- 
#------------------------CLIQUER--------------------------------- 
#---------------------------------------------------------------- 
    def cliquer_bouton_valider(self,driver):
        """fonction pour cliquer sur la validation"""
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        sign_in_button.click()

#---------------------------------------------------------------- 
#------------------------VERIFIER-------------------------------- 
#---------------------------------------------------------------- 
    def verifier_ouverture_ok(self,driver):
        """fonction pour verifier arrivée sur bonne page"""
        dashboard_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
        assert dashboard_heading.text == "Dashboard"

    def verifier_message_nok(self,driver):
        """fonction réutilisable pour menu products"""
        error_message = WebDriverWait(driver, 10).until(  
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-critical")))
        assert error_message.text == "Invalid email or password"  # Vérifie le texte du message d'erreur

    