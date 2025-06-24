# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import config as cfg    

class TestLogin:
    @pytest.fixture
    def driver(self):
        # Configuration du driver Chrome avant chaque test
        service = Service(ChromeDriverManager().install())  # Installation automatique du driver Chrome
        driver = webdriver.Chrome(service=service)  # Création d'une instance du navigateur Chrome
        driver.maximize_window()  # Maximisation de la fenêtre du navigateur
        yield driver  # Retourne le driver pour les tests
        driver.quit()  # Ferme le navigateur après les tests

    def login_success(self, driver):
        """Fonction réutilisable pour faire une connexion réussie"""
        driver.get(cfg.BASE_URL)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(cfg.VALID_EMAIL)

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(cfg.VALID_PASSWORD)

        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        sign_in_button.click()

        dashboard_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
        )
        assert dashboard_heading.text == "Dashboard"

    def test_successful_login(self, driver):
        self.login_success(driver)


    def test_invalid_email(self, driver):
        # Test avec un email invalide
        driver.get(cfg.BASE_URL)  # Navigation vers la page de connexion
        
        # Attente et remplissage de l'email invalide
        email_input = WebDriverWait(driver, 10).until(  # Attend jusqu'à 10 secondes
            EC.presence_of_element_located((By.NAME, "email"))  # Pour que l'élément email soit présent
        )
        email_input.send_keys(cfg.INVALID_EMAIL)  # Saisit l'email invalide
        
        # Remplissage du mot de passe valide
        password_input = driver.find_element(By.NAME, "password")  # Trouve le champ mot de passe
        password_input.send_keys(cfg.VALID_PASSWORD)  # Saisit le mot de passe valide
        
        # Clic sur le bouton de connexion
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  # Trouve le bouton
        sign_in_button.click()  # Clique sur le bouton
        
        # Vérification du message d'erreur
        error_message = WebDriverWait(driver, 10).until(  # Attend jusqu'à 10 secondes
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-critical"))  # Pour que le message d'erreur soit présent
        )
        assert error_message.text == "Invalid email or password"  # Vérifie le texte du message d'erreur

    def test_invalid_password(self, driver):
        # Test avec un mot de passe invalide
        driver.get(cfg.BASE_URL)  # Navigation vers la page de connexion
        
        # Attente et remplissage de l'email valide
        email_input = WebDriverWait(driver, 10).until(  # Attend jusqu'à 10 secondes
            EC.presence_of_element_located((By.NAME, "email"))  # Pour que l'élément email soit présent
        )
        email_input.send_keys(cfg.VALID_EMAIL)  # Saisit l'email valide
        
        # Remplissage du mot de passe invalide
        password_input = driver.find_element(By.NAME, "password")  # Trouve le champ mot de passe
        password_input.send_keys(cfg.INVALID_PASSWORD)  # Saisit le mot de passe invalide
        
        # Clic sur le bouton de connexion
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  # Trouve le bouton
        sign_in_button.click()  # Clique sur le bouton
        
        # Vérification du message d'erreur
        error_message = WebDriverWait(driver, 10).until(  # Attend jusqu'à 10 secondes
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-critical"))  # Pour que le message d'erreur soit présent
        )
        assert error_message.text == "Invalid email or password"  # Vérifie le texte du message d'erreur 
