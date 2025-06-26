import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionUtilesCateg:
    # ✅ Fixture pour gérer le navigateur
    @pytest.fixture(scope="function")
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        yield driver
        driver.quit()  # Toujours exécuté après le test, même en cas d'échec

#----------------------------------------------------------------
#---------------------REMPLIR------------------------------------
#----------------------------------------------------------------
    def remplir_nom_categ_pdt(self,driver,nom):
        """fonction pour remplir le nom categorie"""
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").clear()
        driver.find_element(By.NAME, "name").send_keys(nom)

    def upload_photo_categ(self,driver,photo):   
        """fonction pour télécharger la photo d'une categorie""" 
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(photo)

#----------------------------------------------------------------
#---------------------ALLER--------------------------------------
#----------------------------------------------------------------
    def aller_categ(self,driver):
        """fonction pour cliquer sur menu categories"""
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

    def aller_new_categ_par_categ(self,driver):
        """fonction pour cliquer sur menu new category"""
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.primary")))
        driver.find_element(By.CSS_SELECTOR,"a.button.primary").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new category" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

#----------------------------------------------------------------    
#----------------------CLIQUER-----------------------------------
#----------------------------------------------------------------
    def sauver_categ_pdt(self,driver):
        """fonction pour sauver la categorie"""
        # Sauvegarder la catégorie
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.primary[type='button']"))).click()

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

    def cliquer_lien_parent(self,driver):
        """fonction pour cliquer sur le lien parent d'une categorie"""
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".text-interactive"))).click()     

    def cliquer_lien_delete_categ(self,driver):
        """fonction pour cliquer sur le lien delete des categories"""
        delete_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.inline-flex a:nth-of-type(2)")))
        delete_button.click()         

    def cocher_bouton_radio_categ(self,driver,position):
        """fonction pour cocher un bouton radio dans la liste des categ"""
        boutonRadio = driver.find_elements(By.CSS_SELECTOR, ".field-wrapper.radio-field")
        boutonRadio[position].click()        


#---------------------------------------------------------------- 
#---------------------RECHERCHER--------------------------------- 
#---------------------------------------------------------------- 
    def chercher_element_dans_liste(self,driver,zone,element,occurrence):
        """fonction pour chercher un element à cliquer dans une liste"""
        #attendre que tous les elements apparaissent dans une zone
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, zone))) 
        #mettre tous les elements identiques dans une liste    
        liste = driver.find_elements(By.CSS_SELECTOR, element)

        #regarder dans cette liste si on trouve l'occurrence                       
        for item in liste:
            if occurrence == item.text:
                item.click()  # Cliquer sur l'occurrence correspondante
                break  # Sortir de la boucle une fois l'occurrence trouvée et cliquée


#---------------------------------------------------------------- 
#------------------------VERIFIER-------------------------------- 
#----------------------------------------------------------------         

    def verifier_toast(self,driver,message):
        """fonction pour verifier les toast success d'enregistrement categorie"""
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".Toastify__toast-body")))
        toast=driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
        assert message in toast.text

    def verifier_page_categ_pdt_apres_sauver(self,driver,nom):
        """fonction pour verifier l'affichage de la categ apres enregistrement"""
        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
        assert ("Editing "+ nom) == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text   
        
    def verifier_table_categ_pdt_vide(self,driver):
        """fonction pour verifier que la table des categ est vide"""
        final_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.flex.w-full.justify-center")))
        assert "There is no category to display" in final_message.text    



    