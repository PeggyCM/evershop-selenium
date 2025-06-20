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

# Variables de configuration pour les tests
BASE_URL = "http://localhost:3000/admin/login"  # URL de la page de connexion
VALID_EMAIL = "admin@admin.com"  # Email valide pour la connexion
VALID_PASSWORD = "DB123456"  # Mot de passe valide pour la connexion

# Données du premier produit
PRODUCT_NAME = "Bonnet"
PRODUCT_CATEG_new= "Enfant / Accessoires"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()  # Toujours exécuté après le test, même en cas d'échec


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

# ✅ Test de modification de produit
def test_modif_pdt(driver):
    # Connexion d'abord
    login(driver)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a[href='http://localhost:3000/admin/products']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.page-heading-title")))
    assert "Products" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".main-content-inner"))) 
    
    # Trouver tous les produits dans la liste
    liste_pdt = driver.find_elements(By.CSS_SELECTOR, ".listing > tbody > tr > td > div > a")
                       
    for item in liste_pdt:
        if PRODUCT_NAME in item.text and item.text == PRODUCT_NAME:
            item.click()  # Cliquer sur l'élément correspondant
            break  # Sortir de la boucle une fois l'élément trouvé et cliqué

    # Modifier le formulaire 
    # Sélection de la catégorie
    wait = WebDriverWait(driver, 10)
    
    # Localise et clique sur le lien "Change" via un sélecteur CSS
    change_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "span.text-interactive > a")
    ))
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
        if category_name == PRODUCT_CATEG_new:
            # Cliquer sur le bouton "Select" associé à cette catégorie
            select_button = row.find_element(By.CSS_SELECTOR, "button.button.secondary")
            select_button.click()
            print(f"[INFO] Catégorie '{PRODUCT_CATEG_new}' sélectionnée.")
            found = True
            break

    # Vérifier si la catégorie a été trouvée
    assert found, f"Catégorie '{PRODUCT_CATEG_new}' non trouvée dans la modale."

    # Sauvegarder les modifications
    save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[type='button']"))
    )
    save_button.click()

    # Vérifier que le toast indique que le produit a bien été sauvegardé
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "Toastify__toast-body"), "Product saved successfully!"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "Product saved successfully!" in toast.text