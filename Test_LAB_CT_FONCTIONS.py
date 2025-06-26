import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionUtiles:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

    def aller_categ(self,driver):
        """fonction réutilisable pour menu categories"""
        # Aller dans "Categories avec find elements de ul li dans css selector"
        categories_link = driver.find_elements(By.CSS_SELECTOR,".item-group .nav-item")
        print("Elements trouvés:", len(categories_link))  # Affiche le nombre d'éléments trouvés
       
        # Parcours des éléments pour trouver celui avec le texte correct
        for element in categories_link:
         
            if "Categories" in element.text:  # Compare le texte, en ignorant la casse
                element.click()  # Clique sur l'élément trouvé
                break  # Quitte la boucle une fois l'élément trouvé et cliqué
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Categories" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    def remplir_form_categ(self,driver,nom,photo):
        # Remplir le formulaire pour la nouvelle catégorie
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys(nom)
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(photo)

    def sauver_categ(self,driver):
        # Sauvegarder la catégorie
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.primary[type='button']"))).click()


    def aller_new_categ_par_categ(self,driver):
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.primary")))
        driver.find_element(By.CSS_SELECTOR,"a.button.primary").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new category" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    def aller_pdt(self,driver):
        """fonction réutilisable pour menu products"""
        # Aller dans "products avec find elements de ul li dans css selector"
        pdt_link = driver.find_elements(By.CSS_SELECTOR,".item-group .nav-item")
               
        # Parcours des éléments pour trouver celui avec le texte correct
        for element in pdt_link:
            
            if "Products" in element.text:  # Compare le texte, en ignorant la casse
                element.click()  # Clique sur l'élément trouvé
                break  # Quitte la boucle une fois l'élément trouvé et cliqué
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Products" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text    

    def bouton_delete_modal(self,driver):
        """fonction réutilisable pour cliquer sur delete de la modale"""
        #Cliquer sur le bouton Delete dans la modale
        wait = WebDriverWait(driver, 10)
        # Vérification que la modale est visible
        modal_overlay = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-overlay")))

        # Identifier la modale à survoler
        modal_wrapper = driver.find_element(By.CLASS_NAME, "modal-wrapper")

        # Simuler le hover sur la modale pour retirer l'opacité
        action = ActionChains(driver)
        action.move_to_element(modal_wrapper).perform()

        # Attendre que le bouton "Delete" devienne cliquable après le hover
        modal_delete_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.critical span")))

        # Cliquer sur le bouton "Delete"
        modal_delete_button.click()

    def verifier_toast(self,driver):
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".Toastify__toast-body")))
        toast=driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
        assert "Category saved successfully!" in toast.text

   
        

        
        