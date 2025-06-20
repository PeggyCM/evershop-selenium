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

# Données du paiement


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(URL)
    yield driver
    driver.quit()  # Toujours exécuté après le test, même en cas d'échec

#connexion au site
URL = "http://localhost:3000"
MAIL_CLT = "toto@mail.com"
NOM_CLT = "TOTO"
TEL_CLT = "0202020202"
ADR_CLT = "XXXXXXXXXX"
CITY_CLT = "LYON"
CP_CLT = "69000"
country_name = "France"
province_name = "Auvergne-Rhone-Alpes"
NUM_CART_SUCCESS = "4242424242424242"
NUM_CART_ERROR = "4000000000009995"
DAT_CART_SUCCESS = "04/26"
DAT_CART_ERROR = "04/26"
CVC_SUCCESS = "242"
CVC_ERROR = "242"

#test de paiement success
def test_paie_success(driver):
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".editor__html")))

    # Localiser tous les articles
    listing_articles = driver.find_elements(By.CLASS_NAME, "listing-tem")

    # Vérifier qu'il y a au moins deux articles
    assert len(listing_articles) >= 3, "Il n'y a pas au moins trois articles 'listing-tem' sur la page."

    # Sélectionner et cliquer sur le premier article
    article = listing_articles[0]
    lien_article= article.find_element(By.CSS_SELECTOR, ".product-thumbnail-listing")  # Trouver le lien <a> à l'intérieur
    nom_article = article.find_element(By.CSS_SELECTOR, ".product-name > a > span").text
    lien_article.click()
    
    #attendre le chargement de la page
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-single-name")))
    #vérifier qu'on est sur la page de l'article
    nom_article_page = driver.find_element(By.CSS_SELECTOR, ".product-single-name").text
    print("article de la page ",nom_article_page)          
    assert nom_article == nom_article_page
    #ajouter au panier
    driver.find_element(By.CSS_SELECTOR,".button.primary.outline").click()
    #continuer le shopping
    driver.find_element(By.CSS_SELECTOR,".add-cart-popup-continue").click()
    driver.back()# retour arrière sur le site
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".editor__html")))
 
    # Localiser tous les articles pour un deuxième achat
    listing_articles = driver.find_elements(By.CLASS_NAME, "listing-tem")

    # Vérifier qu'il y a au moins deux articles
    assert len(listing_articles) >= 3, "Il n'y a pas au moins 3 articles 'listing-tem' sur la page."

    # Sélectionner et cliquer sur le premier article
    article = listing_articles[2]
    lien_article= article.find_element(By.CSS_SELECTOR, ".product-thumbnail-listing")  # Trouver le lien <a> à l'intérieur
    nom_article = article.find_element(By.CSS_SELECTOR, ".product-name > a > span").text
    lien_article.click()
    
    #attendre le chargement de la page de l'article
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-single-name")))
    #vérifier qu'on est sur la bonne page
    nom_article_page = driver.find_element(By.CSS_SELECTOR, ".product-single-name").text
    print("article de la page ",nom_article_page)          
    assert nom_article == nom_article_page
    #Ajouter au panier
    driver.find_element(By.CSS_SELECTOR,".button.primary.outline").click()
    #aller au panier
    driver.find_element(By.CSS_SELECTOR,".add-cart-popup-button").click()
    #cliquer sur checkout
    driver.find_element(By.CSS_SELECTOR, "a.button.primary").click()
    #saisir le mail
    driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(MAIL_CLT)
    #cliquer sur shipping
    driver.find_element(By.CSS_SELECTOR, "div.form-submit-button.flex.border-t.border-divider.mt-4.pt-4 button.button.primary").click()
    #remplir les zones du client
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[full_name]']").send_keys(NOM_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[telephone]']").send_keys(TEL_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[address_1]']").send_keys(ADR_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[city]']").send_keys(CITY_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[postcode]']").send_keys(CP_CLT)
    # Trouver le menu déroulant par son ID
    select_element = driver.find_element(By.ID, "address[country]")

    # Attendre que le select soit visible
    select_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "address[country]")))

    # Créer l'objet Select
    ropdown = Select(select_element)

    # Sélectionner le pays par son texte visible
    Select(select_element).select_by_visible_text(country_name)

    # Trouver le menu déroulant des provinces
    select_element = driver.find_element(By.ID, "address[province]")

    
    # Attendre que le select soit visible
    select_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "address[province]")))
    # Créer l'objet Select
    dropdown = Select(select_element)

    # Sélectionner la province
    Select(select_element).select_by_visible_text(province_name)
    #choisir la méthode de paiement
    labels = driver.find_elements(By.CSS_SELECTOR, "label[for^='method']")
    labels[1].click()  # Clique sur le 2ᵉ label radio visible
    #cliquer sur continue to paiement
    driver.find_element(By.CSS_SELECTOR,"button.button.primary > span").click()
    #clique bouton radio carte bancaire et attendre le chargement zones bancaires
    svg_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flex.justify-start a svg.feather.feather-circle"))
    )
    svg_button.click()
    #monter sur iframe banque
    driver.switch_to.frame(0)
    
    # Remplir les informations de la carte
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#Field-numberInput")))
   
    
    driver.find_element(By.CSS_SELECTOR,"#Field-numberInput").send_keys(NUM_CART_SUCCESS)
    driver.find_element(By.CSS_SELECTOR,"#Field-expiryInput").send_keys(DAT_CART_SUCCESS)
    driver.find_element(By.CSS_SELECTOR,"#Field-cvcInput").send_keys(CVC_SUCCESS)
     
    driver.find_element(By.CSS_SELECTOR,"#Field-linkEmailInput").send_keys(MAIL_CLT)
    driver.find_element(By.CSS_SELECTOR,"#Field-linkMobilePhoneInput").send_keys(TEL_CLT)
    driver.find_element(By.CSS_SELECTOR,"#Field-linkLegalNameInput").send_keys(NOM_CLT)

    driver.switch_to.default_content()   
    # Cliquer sur le bouton pour soumettre le paiement
    driver.find_element(By.CSS_SELECTOR, ".form-submit-button > button > span").click()  

    #attente chargement du paiement
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".checkout-success-customer-info")))
    
#test de paiement success
def test_paie_error(driver):
    driver.get(URL)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".editor__html")))

    # Localiser tous les articles
    listing_articles = driver.find_elements(By.CLASS_NAME, "listing-tem")

    # Vérifier qu'il y a au moins deux articles
    assert len(listing_articles) >= 3, "Il n'y a pas au moins trois articles 'listing-tem' sur la page."

    # Sélectionner et cliquer sur le premier article
    article = listing_articles[0]
    lien_article= article.find_element(By.CSS_SELECTOR, ".product-thumbnail-listing")  # Trouver le lien <a> à l'intérieur
    nom_article = article.find_element(By.CSS_SELECTOR, ".product-name > a > span").text
    lien_article.click()
    
    #attendre le chargement de la page
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-single-name")))
    #vérifier qu'on est sur la page de l'article
    nom_article_page = driver.find_element(By.CSS_SELECTOR, ".product-single-name").text
    print("article de la page ",nom_article_page)          
    assert nom_article == nom_article_page
    #ajouter au panier
    driver.find_element(By.CSS_SELECTOR,".button.primary.outline").click()
    #continuer le shopping
    driver.find_element(By.CSS_SELECTOR,".add-cart-popup-continue").click()
    driver.back()# retour arrière sur le site
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".editor__html")))
 
    # Localiser tous les articles pour un deuxième achat
    listing_articles = driver.find_elements(By.CLASS_NAME, "listing-tem")

    # Vérifier qu'il y a au moins deux articles
    assert len(listing_articles) >= 3, "Il n'y a pas au moins 3 articles 'listing-tem' sur la page."

    # Sélectionner et cliquer sur le premier article
    article = listing_articles[2]
    lien_article= article.find_element(By.CSS_SELECTOR, ".product-thumbnail-listing")  # Trouver le lien <a> à l'intérieur
    nom_article = article.find_element(By.CSS_SELECTOR, ".product-name > a > span").text
    lien_article.click()
    
    #attendre le chargement de la page de l'article
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-single-name")))
    #vérifier qu'on est sur la bonne page
    nom_article_page = driver.find_element(By.CSS_SELECTOR, ".product-single-name").text
    print("article de la page ",nom_article_page)          
    assert nom_article == nom_article_page
    #Ajouter au panier
    driver.find_element(By.CSS_SELECTOR,".button.primary.outline").click()
    #aller au panier
    driver.find_element(By.CSS_SELECTOR,".add-cart-popup-button").click()
    #cliquer sur checkout
    driver.find_element(By.CSS_SELECTOR, "a.button.primary").click()
    #saisir le mail
    driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(MAIL_CLT)
    #cliquer sur shipping
    driver.find_element(By.CSS_SELECTOR, "div.form-submit-button.flex.border-t.border-divider.mt-4.pt-4 button.button.primary").click()
    #remplir les zones du client
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[full_name]']").send_keys(NOM_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[telephone]']").send_keys(TEL_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[address_1]']").send_keys(ADR_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[city]']").send_keys(CITY_CLT)
    driver.find_element(By.CSS_SELECTOR, "div.form-field-container input[name='address[postcode]']").send_keys(CP_CLT)
    # Trouver le menu déroulant par son ID
    select_element = driver.find_element(By.ID, "address[country]")

    # Attendre que le select soit visible
    select_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "address[country]")))

    # Créer l'objet Select
    ropdown = Select(select_element)

    # Sélectionner le pays par son texte visible
    Select(select_element).select_by_visible_text(country_name)

    # Trouver le menu déroulant des provinces
    select_element = driver.find_element(By.ID, "address[province]")

    
    # Attendre que le select soit visible
    select_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "address[province]")))
    # Créer l'objet Select
    dropdown = Select(select_element)

    # Sélectionner la province
    Select(select_element).select_by_visible_text(province_name)
    #choisir la méthode de paiement
    labels = driver.find_elements(By.CSS_SELECTOR, "label[for^='method']")
    labels[1].click()  # Clique sur le 2ᵉ label radio visible
    #cliquer sur continue to paiement
    driver.find_element(By.CSS_SELECTOR,"button.button.primary > span").click()
    #clique bouton radio carte bancaire et attendre le chargement zones bancaires
    svg_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flex.justify-start a svg.feather.feather-circle"))
    )
    svg_button.click()
    #monter sur iframe banque
    driver.switch_to.frame(0)
    
    # Remplir les informations de la carte
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#Field-numberInput")))
   
    
    driver.find_element(By.CSS_SELECTOR,"#Field-numberInput").send_keys(NUM_CART_ERROR)
    driver.find_element(By.CSS_SELECTOR,"#Field-expiryInput").send_keys(DAT_CART_SUCCESS)
    driver.find_element(By.CSS_SELECTOR,"#Field-cvcInput").send_keys(CVC_SUCCESS)
     
    driver.find_element(By.CSS_SELECTOR,"#Field-linkEmailInput").send_keys(MAIL_CLT)
    driver.find_element(By.CSS_SELECTOR,"#Field-linkMobilePhoneInput").send_keys(TEL_CLT)
    driver.find_element(By.CSS_SELECTOR,"#Field-linkLegalNameInput").send_keys(NOM_CLT)

    driver.switch_to.default_content()   
    # Cliquer sur le bouton pour soumettre le paiement
    driver.find_element(By.CSS_SELECTOR, ".form-submit-button > button > span").click()  

    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "Toastify__toast-body"),"Payment failed"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "Payment failed" in toast.text
    
      