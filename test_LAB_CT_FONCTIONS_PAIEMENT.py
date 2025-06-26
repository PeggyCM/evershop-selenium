import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionsUtilesPaiement:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    def aller_url_clt(self,driver):
        driver.get(cfg.URL_CLT)

    def verifier_article_suffisant_a_commander(self,driver):
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h3.mt-12")))

        # Localiser tous les articles
        listing_articles = driver.find_elements(By.CLASS_NAME, "listing-tem")
        
        # Vérifier qu'il y a au moins 3 articles
        assert len(listing_articles) >= 3, "Il n'y a pas au moins trois articles 'listing-tem' sur la page."
        return listing_articles

    def Selectionner_article(self,driver,listing,num_art):
        article = listing[num_art]
        lien_article= article.find_element(By.CSS_SELECTOR, ".product-thumbnail-listing")  # Trouver le lien <a> à l'intérieur
        nom_article = article.find_element(By.CSS_SELECTOR, ".product-name > a > span").text
        lien_article.click()
        #attendre le chargement de la page
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-single-name")))
        #vérifier qu'on est sur la page de l'article
        nom_article_page = driver.find_element(By.CSS_SELECTOR, ".product-single-name").text
        assert nom_article == nom_article_page

    def ajouter_panier(self,driver):
        #ajouter au panier
        driver.find_element(By.CSS_SELECTOR,".button.primary.outline").click()

    def continuer_shopping(self,driver):    
        #continuer le shopping
        driver.find_element(By.CSS_SELECTOR,".add-cart-popup-continue").click()
        driver.back()# retour arrière sur le site
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".editor__html")))            

    def aller_panier(self,driver):
        #aller au panier
        driver.find_element(By.CSS_SELECTOR,".add-cart-popup-button").click()
    
    def entrer_donnees_checkout(self,driver):
        #cliquer sur checkout
        driver.find_element(By.CSS_SELECTOR, "a.button.primary").click()
        #saisir le mail
        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(cfg.MAIL_CLT)
        
    def entrer_donnees_shipping(self,driver):    
        #cliquer sur shipping
        driver.find_element(By.CSS_SELECTOR, "div.form-submit-button.flex.border-t.border-divider.mt-4.pt-4 button.button.primary").click()
        #remplir les zones du client
        driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[full_name]']").send_keys(cfg.NOM_CLT)
        driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[telephone]']").send_keys(cfg.TEL_CLT)
        driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[address_1]']").send_keys(cfg.ADR_CLT)
        driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[city]']").send_keys(cfg.CITY_CLT)
        driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[postcode]']").send_keys(cfg.CP_CLT)

        # Trouver le menu déroulant par son ID
        select_element = driver.find_element(By.ID, "address[country]")
        # Attendre que le select soit visible
        select_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "address[country]")))
        # Créer l'objet Select
        ropdown = Select(select_element)
        # Sélectionner le pays par son texte visible
        Select(select_element).select_by_visible_text(cfg.country_name)

        # Trouver le menu déroulant des provinces
        select_element = driver.find_element(By.ID, "address[province]")
        # Attendre que le select soit visible
        select_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "address[province]")))
        # Créer l'objet Select
        dropdown = Select(select_element)
        # Sélectionner la province
        Select(select_element).select_by_visible_text(cfg.province_name)
    
    def payer_commande(self,driver,num_carte):
        #choisir la méthode de paiement
        labels = driver.find_elements(By.CSS_SELECTOR, "label[for^='method']")
        labels[1].click()  # Clique sur le 2ᵉ label radio visible
        #cliquer sur continue to paiement
        driver.find_element(By.CSS_SELECTOR,"button.button.primary > span").click()
        #clique bouton radio carte bancaire et attendre le chargement zones bancaires
        svg_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.flex.justify-start a svg.feather.feather-circle")))
        svg_button.click()
        #monter sur iframe banque
        driver.switch_to.frame(0)
    
        # Remplir les informations de la carte
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#Field-numberInput")))
        driver.find_element(By.CSS_SELECTOR,"#Field-numberInput").send_keys(num_carte)
        driver.find_element(By.CSS_SELECTOR,"#Field-expiryInput").send_keys(cfg.DAT_CART_SUCCESS)
        driver.find_element(By.CSS_SELECTOR,"#Field-cvcInput").send_keys(cfg.CVC_SUCCESS)
     
        driver.find_element(By.CSS_SELECTOR,"#Field-linkEmailInput").send_keys(cfg.MAIL_CLT)
        driver.find_element(By.CSS_SELECTOR,"#Field-linkMobilePhoneInput").send_keys(cfg.TEL_CLT)
        driver.find_element(By.CSS_SELECTOR,"#Field-linkLegalNameInput").send_keys(cfg.NOM_CLT)

        driver.switch_to.default_content()   
        # Cliquer sur le bouton pour soumettre le paiement
        driver.find_element(By.CSS_SELECTOR, ".form-submit-button > button > span").click()  

    def verifier_paiement_passe(self,driver):    
        #attente chargement du paiement
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".checkout-success-customer-info")))
 
    def verifier_paiement_error(self,driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "Toastify__toast-body"),"Payment failed"))
        toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
        assert "Payment failed" in toast.text
        