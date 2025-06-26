# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
import random
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import os  # Pour gérer les chemins de fichiers
import time  # Pour attendre un court instant
from selenium.webdriver.common.action_chains import ActionChains  # Pour utiliser les Actions de Selenium
import config as cfg
import test_LAB_CT_FONCTIONS_PAIEMENT as fonctionP

class TestPaiement:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    #test de paiement success
    
    def test_paie_success(self,driver):
        fonctionP.FonctionsUtilesPaiement.aller_url_clt(self,driver)
        listing_articles=fonctionP.FonctionsUtilesPaiement.verifier_article_suffisant_a_commander(self,driver)
     
        # Sélectionner et cliquer sur le premier article et qu'on arrive sur la bonne page
        article=0
        fonctionP.FonctionsUtilesPaiement.Selectionner_article(self,driver,listing_articles,article)
        fonctionP.FonctionsUtilesPaiement.ajouter_panier(self,driver)
        fonctionP.FonctionsUtilesPaiement.continuer_shopping(self,driver)
 
        # Localiser tous les articles pour un deuxième achat
        article=2
        listing_articles=fonctionP.FonctionsUtilesPaiement.verifier_article_suffisant_a_commander(self,driver)    
        fonctionP.FonctionsUtilesPaiement.Selectionner_article(self,driver,listing_articles,article)
        fonctionP.FonctionsUtilesPaiement.ajouter_panier(self,driver)    
        fonctionP.FonctionsUtilesPaiement.aller_panier(self,driver)
        fonctionP.FonctionsUtilesPaiement.entrer_donnees_checkout(self,driver)
        fonctionP.FonctionsUtilesPaiement.entrer_donnees_shipping(self,driver)
        fonctionP.FonctionsUtilesPaiement.payer_commande(self,driver,cfg.NUM_CART_SUCCESS)
        fonctionP.FonctionsUtilesPaiement.verifier_paiement_passe(self,driver)

    #test de paiement error
    def test_paie_error(self,driver):
        fonctionP.FonctionsUtilesPaiement.aller_url_clt(self,driver)
        listing_articles=fonctionP.FonctionsUtilesPaiement.verifier_article_suffisant_a_commander(self,driver)
        # Sélectionner et cliquer sur le premier article et qu'on arrive sur la bonne page
        article=0
        fonctionP.FonctionsUtilesPaiement.Selectionner_article(self,driver,listing_articles,article)
        fonctionP.FonctionsUtilesPaiement.ajouter_panier(self,driver)
        fonctionP.FonctionsUtilesPaiement.continuer_shopping(self,driver)
 
        # Localiser tous les articles pour un deuxième achat
        article=2
        listing_articles=fonctionP.FonctionsUtilesPaiement.verifier_article_suffisant_a_commander(self,driver)    
        fonctionP.FonctionsUtilesPaiement.Selectionner_article(self,driver,listing_articles,article)
        fonctionP.FonctionsUtilesPaiement.ajouter_panier(self,driver)    
        fonctionP.FonctionsUtilesPaiement.aller_panier(self,driver)
        fonctionP.FonctionsUtilesPaiement.entrer_donnees_checkout(self,driver)
        fonctionP.FonctionsUtilesPaiement.entrer_donnees_shipping(self,driver)
        fonctionP.FonctionsUtilesPaiement.payer_commande(self,driver,cfg.NUM_CART_ERROR)
        fonctionP.FonctionsUtilesPaiement.verifier_paiement_passe(self,driver)
        fonctionP.FonctionsUtilesPaiement.verifier_paiement_error(self,driver)

    
    
      