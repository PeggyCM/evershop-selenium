import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import test_LAB_LOGIN as loginS
import config as cfg
import test_LAB_CT_FONCTIONS_COLLECTION as fonctionC

class TestCreerCollectionPourPaiement:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec


    # ✅ Test de création de catégorie
    def test_create_collection(self,driver):
        # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)
        fonctionC.FonctionUtilesCollection.aller_collection(self,driver)
        fonctionC.FonctionUtilesCollection.choisir_collection_automne(self,driver)
        fonctionC.FonctionUtilesCollection.ajouter_article_a_collection(self,driver)
        fonctionC.FonctionUtilesCollection.verifier_collection_ok(self,driver)
        
  
    