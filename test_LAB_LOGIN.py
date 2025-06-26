# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import config as cfg    
import Test_LAB_CT_FONCTIONS_LOGIN as fonctionL

class TestLogin:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    def login_success(self,driver):
        """Fonction réutilisable pour faire une connexion réussie"""
        fonctionL.FonctionUtilesLogin.ouvrir_url(self,driver)
        fonctionL.FonctionUtilesLogin.saisir_email(self,driver,cfg.VALID_EMAIL)
        fonctionL.FonctionUtilesLogin.saisir_mdp(self,driver,cfg.VALID_PASSWORD)
        fonctionL.FonctionUtilesLogin.cliquer_bouton_valider(self,driver)
        fonctionL.FonctionUtilesLogin.verifier_ouverture_ok(self,driver)

    def test_successful_login(self, driver):
        self.login_success(driver)

    def test_invalid_email(self, driver):
        # Test avec un email invalide
        fonctionL.FonctionUtilesLogin.ouvrir_url(self,driver)
        fonctionL.FonctionUtilesLogin.saisir_email(self,driver,cfg.INVALID_EMAIL)
        fonctionL.FonctionUtilesLogin.saisir_mdp(self,driver,cfg.VALID_PASSWORD)
        fonctionL.FonctionUtilesLogin.cliquer_bouton_valider(self,driver)
        fonctionL.FonctionUtilesLogin.verifier_message_nok(self,driver)
          
    def test_invalid_password(self, driver):
        # Test avec un mot de passe invalide
        fonctionL.FonctionUtilesLogin.ouvrir_url(self,driver)
        fonctionL.FonctionUtilesLogin.saisir_email(self,driver,cfg.VALID_EMAIL)
        fonctionL.FonctionUtilesLogin.saisir_mdp(self,driver,cfg.INVALID_PASSWORD)
        fonctionL.FonctionUtilesLogin.cliquer_bouton_valider(self,driver)
        fonctionL.FonctionUtilesLogin.verifier_message_nok(self,driver)
        
