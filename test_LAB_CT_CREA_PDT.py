# Import des bibliothèques nécessaires pour les tests
import pytest  # Framework de test
import random
from selenium import webdriver  # Pour automatiser le navigateur
from selenium.webdriver.common.by import By  # Pour localiser les éléments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # Pour attendre les éléments
from selenium.webdriver.support import expected_conditions as EC  # Pour définir les conditions d'attente
from selenium.webdriver.chrome.service import Service  # Pour configurer le service Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Pour gérer automatiquement le driver Chrome
import os  # Pour gérer les chemins de fichiers
import time  # Pour attendre un court instant
from selenium.webdriver.common.action_chains import ActionChains  # Pour utiliser les Actions de Selenium

# Variables de configuration pour les tests
BASE_URL = "http://localhost:3000/admin/login"  # URL de la page de connexion
VALID_EMAIL = "admin@admin.com"  # Email valide pour la connexion
VALID_PASSWORD = "DB123456"  # Mot de passe valide pour la connexion

# Données du premier produit
PRODUCT_NAME = ["Pantalon","Robe","Salopette","Echarpe","Gant","Bonnet"]
PRODUCT_CATEG = ["Hommes / Vetements","Femme / Vetements","Enfant / Vetements","Hommes / Accessoires",
                 "Femme / Accessoires","Enfant / Vetements"]
PRODUCT_SKU = "sku"
PRODUCT_PRICE = "50"
PRODUCT_WEIGHT = "2"
PRODUCT_QTY = "20"
PRODUCT_URL_KEY = "url"
PRODUCT_IMAGE = "/home/combeau-mansour/Tools/EverShopDocker-TP/cintre.avif"  # Chemin absolu de la photo
NUM_ALEA = random.randint(1, 9999)
i = 0

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()  # Toujours exécuté après le test, même en cas d'échec

# Fixture avec login exécuté une seule fois pour le module
@pytest.fixture(scope="module")
def logged_in_driver(driver):
    login(driver)  # ← ta fonction de login est appelée ici une seule fois
    return driver

@pytest.fixture(scope="module")
def sku_doublon():
    return {"value": ""}

@pytest.fixture(scope="module")
def url_doublon():
    return {"value": ""}

# ✅ Test de connexion
def login(driver):
    driver.get(BASE_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")

    email_input.send_keys(VALID_EMAIL)
    password_input.send_keys(VALID_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
    dashboard_title = driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
    assert "Dashboard" in dashboard_title

# ✅ Test de création de produit vide
def test_crea_vide(logged_in_driver):
    driver = logged_in_driver
    # Cliquer sur "New products"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    "a[href='http://localhost:3000/admin/products/new']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
    assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    # Attente et clic sur le bouton Save
    save_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']")))
    save_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.pl025.text-critical")))
    assert "This field can not be empty" == driver.find_element(By.CSS_SELECTOR, "span.pl025.text-critical").text
    

# ✅ Test de création de produit
def test_crea_pdt(logged_in_driver):
    driver = logged_in_driver

    for i in range(3):
        # Aller dans "Products"
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='http://localhost:3000/admin/products']"))).click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Products" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

        # Cliquer sur "New products"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        "a[href='http://localhost:3000/admin/products/new']"))).click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

        # Remplir le formulaire pour le nouveau produit
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys(PRODUCT_NAME[i])
        driver.find_element(By.NAME, "url_key").send_keys(PRODUCT_URL_KEY + f"{PRODUCT_NAME[i]}{i:03d}")
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(PRODUCT_IMAGE)

        sku_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']")))
        sku_input.clear()
        sku_input.send_keys(f"{PRODUCT_SKU}{i:03d}")
    
        price_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='price'][placeholder='Price']")))
        price_input.clear()
        price_input.send_keys(PRODUCT_PRICE)
        
        weight_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='weight'][placeholder='Weight']")))
        weight_input.clear()
        weight_input.send_keys(PRODUCT_WEIGHT)

        # Sélection de la catégorie
        select_category_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.text-interactive")))
        select_category_link.click()

         # Attendre que la modale de la categorie soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Trouver la zone de recherche dans la modale
        search_input = driver.find_element(By.CSS_SELECTOR, ".modal-content input[placeholder='Search categories']")

        # Tape la catégorie à rechercher
        category_to_search = PRODUCT_CATEG[i]
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
        qty_input.send_keys(PRODUCT_QTY)

        # Attente et clic sur le bouton Save
        save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']")))
        save_button.click()
    
        
        # Attente de la confirmation de position sur page Editing
        # Attend que le titre devienne "Editing"
        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
        assert ("Editing "+PRODUCT_NAME[i]) == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
    

# ✅ Test de création de produit
def test_crea_pdtN(logged_in_driver,sku_doublon,url_doublon):
    driver = logged_in_driver

    for i in range(3,6,1):
        # Cliquer sur "New products"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        "a[href='http://localhost:3000/admin/products/new']"))).click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
        assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

        # Remplir le formulaire pour le nouveau produit
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys(PRODUCT_NAME[i])
        url = PRODUCT_URL_KEY + f"{PRODUCT_NAME[i]}{i:03d}"
        driver.find_element(By.NAME, "url_key").send_keys(url)
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(PRODUCT_IMAGE)

        sku_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']")))
        sku_input.clear()
        sku = f"{PRODUCT_SKU}{i:03d}"
        sku_input.send_keys(sku)

        sku_doublon["value"] = sku
        url_doublon["value"] = url
    
        price_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='price'][placeholder='Price']")))
        price_input.clear()
        price_input.send_keys(PRODUCT_PRICE)
        
        weight_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='weight'][placeholder='Weight']")))
        weight_input.clear()
        weight_input.send_keys(PRODUCT_WEIGHT)

        # Sélection de la catégorie
        select_category_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.text-interactive")))
        select_category_link.click()

         # Attendre que la modale de la categorie soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Trouver la zone de recherche dans la modale
        search_input = driver.find_element(By.CSS_SELECTOR, ".modal-content input[placeholder='Search categories']")

        # Tape la catégorie à rechercher
        category_to_search = PRODUCT_CATEG[i]
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
        qty_input.send_keys(PRODUCT_QTY)

        # Attente et clic sur le bouton Save
        save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']")))
        save_button.click()
    
        
        # Attend que le titre devienne "Editing"
        WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1.page-heading-title"), "Editing"))
        assert "Editing "+PRODUCT_NAME[i] == driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
   
# ✅ Test de création de produit doublon
def test_crea_doublon(logged_in_driver,sku_doublon,url_doublon):
    driver = logged_in_driver
    sku = sku_doublon["value"]
    url = url_doublon["value"]
    # Cliquer sur "New products"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    "a[href='http://localhost:3000/admin/products/new']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title")))
    assert "Create a new product" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    driver.find_element(By.NAME, "name").send_keys("X")
    driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").send_keys(sku)
    driver.find_element(By.CSS_SELECTOR, "input[name='price'][placeholder='Price']").send_keys(2)
    driver.find_element(By.CSS_SELECTOR, "input[name='weight'][placeholder='Weight']").send_keys(2)
    driver.find_element(By.CSS_SELECTOR, "input[name='qty'][placeholder='Quantity']").send_keys(2)
    driver.find_element(By.NAME, "url_key").send_keys("A")

    # Attente et clic sur le bouton Save
    save_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']")))
    save_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "Toastify__toast-body"),"PRODUCT_SKU_UNIQUE"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "PRODUCT_SKU_UNIQUE" in toast.text
    # Attendre que le bouton de fermeture du toast soit cliquable
    close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Toastify__close-button")))

    # Cliquer sur la croix pour fermer le toast
    close_button.click()

    driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").clear()
    driver.find_element(By.CSS_SELECTOR, "input[name='sku'][placeholder='SKU']").send_keys("A")
    driver.find_element(By.NAME, "url_key").clear()
    driver.find_element(By.NAME, "url_key").send_keys(url)
    
    # Attente et clic sur le bouton Save
    save_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']")))
    save_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "Toastify__toast-body"),"PRODUCT_URL_KEY_UNIQUE"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "PRODUCT_URL_KEY_UNIQUE" in toast.text