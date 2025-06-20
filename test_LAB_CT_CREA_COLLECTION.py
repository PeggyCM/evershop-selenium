import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Définition des constantes
BASE_URL = "http://localhost:3000/admin/login"
VALID_EMAIL = "admin@admin.com"
VALID_PASSWORD = "DB123456"

# ✅ Fixture pour gérer le navigateur
@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
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

# ✅ Test de création de catégorie
def test_create_collection(driver):
    # Connexion d'abord
    login(driver)
    
    collection_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "a[href='http://localhost:3000/admin/collections']")))
    collection_link.click()
    
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
    (By.CSS_SELECTOR, "h1.page-heading-title"),"Collections"))
    assert "Collections" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
    
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
    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay.fadeIn"))
    )
    driver.find_element(By.CSS_SELECTOR,"button.button.primary").click()
  
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
    (By.CLASS_NAME, "Toastify__toast-body"),"Collection saved successfully!"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "Collection saved successfully!" in toast.text