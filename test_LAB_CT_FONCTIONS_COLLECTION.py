import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionUtilesCollection:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    def aller_collection(self,driver):
        """fonction pour cliquer sur menu collections"""
        # Aller dans "collections avec find elements de ul li dans css selector"
        collections_link = driver.find_elements(By.CSS_SELECTOR,".item-group .nav-item")
        
        # Parcours des éléments pour trouver celui avec le texte correct
        for element in collections_link:
         
            if "Collections" in element.text:  # Compare le texte, en ignorant la casse
                element.click()  # Clique sur l'élément trouvé
                break  # Quitte la boucle une fois l'élément trouvé et cliqué
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Collections" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    def choisir_collection_automne(self,driver):
        # On récupère tous les liens dans la table
        elements = driver.find_elements(By.CSS_SELECTOR, "table.listing a.font-semibold")

        # On parcourt les liens pour trouver celui avec le texte "Collection Automne"
        for el in elements:
            if el.text.strip() == "Collection Automne":
                el.click()  # On clique sur le lien trouvé
                break  # On sort de la boucle une fois cliqué

        
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, "h1.page-heading-title"),"Editing Collection Automne"))
        
        assert "Editing Collection Automne" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
  
    def ajouter_article_a_collection(self,driver):
        driver.find_element(By.CSS_SELECTOR, ".text-interactive").click()
        
        # Attendre que la modale de la categorie soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay.fadeIn")))
        modal = driver.find_element(By.CSS_SELECTOR, ".modal-overlay.fadeIn")
        # Récupérer tous les boutons "Select" dans la modale
        boutons_select = driver.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-8 > div > button")
        buttons = modal.find_elements(By.CSS_SELECTOR, "button.button.secondary")
    
        for i in range(3):
            boutons_select[i].click()
    
        # Trouve  "Close"
        modal.find_element(By.CSS_SELECTOR, "div.card-section.border-b.box-border > div.card-session-content.pt-lg > div.flex.justify-between.gap-8 > button.button.secondary").click()
        
        #time.sleep(1)
   
        # Attente explicite jusqu'à ce que la modale ait disparu
        WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay.fadeIn")))
        driver.find_element(By.CSS_SELECTOR,"button.button.primary").click()

    def verifier_collection_ok(self,driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "Toastify__toast-body"),"Collection saved successfully!"))
        toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
        assert "Collection saved successfully!" in toast.text 