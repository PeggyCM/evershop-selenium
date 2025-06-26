# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import os  # Pour gérer les chemins de fichiers
import time  # Pour attendre un court instant
import config as cfg
import test_LAB_LOGIN as loginS
import Test_LAB_CT_FONTIONS_PDT as fonctionP
import Test_LAB_CT_FONCTIONS_CATEG as fonctionC

class TestModifPdt:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    # ✅ Test de modification de produit
    def test_modif_pdt(self,driver):
    # Connexion d'abord
        loginS.TestLogin.login_success(self,driver)

        fonctionP.FonctionUtilesPdt.aller_pdt(self,driver)
        fonctionC.FonctionUtilesCateg.chercher_element_dans_liste(self,driver,
            ".main-content-inner",".listing > tbody > tr > td > div > a",cfg.PRODUCT_NAME_MODIF)
        
        # Sélection de la catégorie pour modif
        fonctionP.FonctionUtilesPdt.cherche_categPdt_pour_modif(self,driver)
        # Sauvegarder les modifications
        fonctionC.FonctionUtilesCateg.sauver_categ_pdt(self,driver)
        # Vérifier que le toast indique que le produit a bien été sauvegardé
        fonctionC.FonctionUtilesCateg.verifier_toast(self,driver,"Product saved successfully!")