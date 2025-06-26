import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg

class FonctionUtilesPdt:
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
    def remplir_sku(self,driver,sku,i):
        sku_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']")))
        sku_input.clear()
        sku_input.send_keys(f"{sku}{i:03d}")
    
    def remplir_price(self,driver,price):
        price_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='price'][placeholder='Price']")))
        price_input.clear()
        price_input.send_keys(price)

    def remplir_weight(self,driver,weight):
        weight_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='weight'][placeholder='Weight']")))
        weight_input.clear()
        weight_input.send_keys(weight)

    def remplir_categorie_pdt(self,driver,categ):
        # Attendre que la modale de la categorie soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))
        # Trouver la zone de recherche dans la modale
        search_input = driver.find_element(By.CSS_SELECTOR, ".modal-content input[placeholder='Search categories']")
        # Tape la catégorie à rechercher
        category_to_search = categ
        search_input.clear()
        search_input.send_keys(category_to_search)
        search_input.send_keys(Keys.RETURN)  # Tape Entrée

        # Attendre que la liste soit filtrée (présence d'au moins un résultat)
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content .grid.grid-cols-8")))

        # Récupérer toutes les lignes affichées après filtrage
        filtered_rows = driver.find_elements(By.CSS_SELECTOR, ".modal-content .grid.grid-cols-8")
    
        found = False
        for row in filtered_rows:
            try:
                # Construire le nom complet sans ">"
                spans = row.find_elements(By.CSS_SELECTOR, "h3 span")
                parts = [span.text.replace(">", "").strip() for span in spans if span.text.strip()]
                category_name = " / ".join(parts)
                print(f"[DEBUG] Trouvé dans filtre: '{category_name}'")
                if category_name == category_to_search:
                # Cliquer sur le bouton Select dans cette ligne
                    select_button = row.find_element(By.CSS_SELECTOR, "button.button.secondary")
                    select_button.click()
                    print(f"[INFO] Bouton 'Select' cliqué pour la catégorie '{category_name}'")
                    found = True
                    break
            except Exception as e:
                print(f"[ERROR] Ligne ignorée : {e}")
                continue
    
        assert found, f"Catégorie '{category_to_search}' non trouvée après recherche."


#----------------------------------------------------------------
#---------------------ALLER--------------------------------------
#----------------------------------------------------------------
    def aller_pdt(self,driver):
        """fonction pour cliquer sur menu products"""
        # Aller dans "products avec find elements de ul li dans css selector"
        pdt_link = driver.find_elements(By.CSS_SELECTOR,".item-group .nav-item")
        print("Elements trouvés:", len(pdt_link))  # Affiche le nombre d'éléments trouvés
       
        # Parcours des éléments pour trouver celui avec le texte correct
        for element in pdt_link:
         
            if "Products" in element.text:  # Compare le texte, en ignorant la casse
                element.click()  # Clique sur l'élément trouvé
                break  # Quitte la boucle une fois l'élément trouvé et cliqué
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Products" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    def aller_new_pdt(self,driver):
        """fonction pour cliquer sur menu new products"""
        # Aller dans "new products avec find elements de ul li dans css selector"
        pdt_link = driver.find_elements(By.CSS_SELECTOR,".item-group .nav-item")
        print("Elements trouvés:", len(pdt_link))  # Affiche le nombre d'éléments trouvés
       
        # Parcours des éléments pour trouver celui avec le texte correct
        for element in pdt_link:
         
            if "New Product" in element.text:  # Compare le texte, en ignorant la casse
                element.click()  # Clique sur l'élément trouvé
                break  # Quitte la boucle une fois l'élément trouvé et cliqué
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    def aller_new_pdt_par_pdt(self,driver):
        """fonction pour cliquer sur menu new product"""
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.primary")))
        driver.find_element(By.CSS_SELECTOR,"a.button.primary").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

#----------------------------------------------------------------    
#----------------------CLIQUER-----------------------------------
#----------------------------------------------------------------
    def bouton_lien_delete(self,driver):
        """fonction réutilisable pour cliquer sur delete de la modale"""
        delete_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.inline-flex a:nth-of-type(4)")))
        delete_button.click()

         

    def cliquer_lien_categ_new_pdt(self,driver):
        # Cliquer sur le lien de la catégorie pour la création d'un pdt
        select_category_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.text-interactive")))
        select_category_link.click()

    def cliquer_bouton_radio(self,driver):
        # Sélection des options radio
        # Status: Enabled
        status_enabled = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='status1'] span.pl-4")))
        status_enabled.click()
      
        # Visibility: Visible
        visibility_visible = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='visibility1'] span.pl-4")))
        visibility_visible.click()
        
        # Manage stock: Yes
        manage_stock_yes = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='manage_stock1'] span.pl-4")))
        manage_stock_yes.click()
        
        # Stock availability: Yes
        stock_availability_yes = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='stock_availability1'] span.pl-4")))
        stock_availability_yes.click()
        
        qty_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='qty'][placeholder='Quantity']")))
        qty_input.clear()
        qty_input.send_keys(cfg.PRODUCT_QTY)
#---------------------------------------------------------------- 
#---------------------RECHERCHER--------------------------------- 
#---------------------------------------------------------------- 
    def cherche_categPdt_pour_modif(self,driver):
        wait = WebDriverWait(driver, 10)
    
        # Localise et clique sur le lien "Change" via un sélecteur CSS
        change_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "span.text-interactive > a")))
        change_link.click()

        # Attendre que la modale des catégories soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Récupérer toutes les lignes des catégories dans la modale
        category_rows = driver.find_elements(By.CSS_SELECTOR, ".modal-content .grid.grid-cols-8")

        # Chercher la catégorie spécifiée dans `PRODUCT_CATEG_new`
        found = False
        for row in category_rows:
            # Extraire les catégories du `<h3>` dans chaque ligne
            spans = row.find_elements(By.CSS_SELECTOR, "h3 span")
        
            # Nettoyage du texte extrait pour enlever les espaces supplémentaires et les caractères spéciaux
            category_name = " / ".join([span.text.strip().replace(">", "").strip() for span in spans if span.text.strip()])
        
            print(f"[DEBUG] Catégorie trouvée : '{category_name}'")

            # Comparaison avec PRODUCT_CATEG_new après nettoyage
            if category_name == cfg.PRODUCT_CATEG_MODIF:
                # Cliquer sur le bouton "Select" associé à cette catégorie
                select_button = row.find_element(By.CSS_SELECTOR, "button.button.secondary")
                select_button.click()
                print(f"[INFO] Catégorie '{cfg.PRODUCT_CATEG_MODIF}' sélectionnée.")
                found = True
                break
 
        # Vérifier si la catégorie a été trouvée
        assert found, f"Catégorie '{cfg.PRODUCT_CATEG_MODIF}' non trouvée dans la modale."

#---------------------------------------------------------------- 
#------------------------VERIFIER-------------------------------- 
#----------------------------------------------------------------         

    def verifier_toast(self,driver,message):
        """fonction pour verifier les toast success d'enregistrement categorie"""
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".Toastify__toast-body")))
        toast=driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
        assert message in toast.text

    def verifier_page_categ_apres_sauver(self,driver,nom):
        """fonction pour verifier l'affichage de la categ apres enregistrement"""
        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
        assert ("Editing "+ nom) == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text   
        
    def verifier_table_pdt_vide(self,driver):
        """fonction pour verifier que la table des pdt est vide"""
        final_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.flex.w-full.justify-center")))
        assert "There is no product to display" in final_message.text    

    def verifier_champs_empty_pdt(self,driver):
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "span.pl025.text-critical")))
        assert "This field can not be empty" == driver.find_element(
            By.CSS_SELECTOR, "span.pl025.text-critical").text



    