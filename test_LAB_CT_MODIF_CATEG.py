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
CATEGORY_NAME_old = "Homme"
CATEGORY_NAME_new = "Hommes" 

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

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "h1.page-heading-title")))
    dashboard_title = driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
    assert "Dashboard" in dashboard_title

# ✅ Test de modification de catégorie
def test_modif_category(driver):
    # Connexion d'abord
    login(driver)

    # Aller dans "Categories"
    categories_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "a[href='http://localhost:3000/admin/categories']")))
    categories_link.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "h1.page-heading-title")))
    assert "Categories" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, ".main-content-inner"))) 
            
    liste_categ = driver.find_elements(By.CSS_SELECTOR, ".listing > tbody > tr > td > div > a")
                       
    for item in liste_categ:
        if CATEGORY_NAME_old in item.text and item.text == CATEGORY_NAME_old:
            item.click()  # Cliquer sur l'élément correspondant
            break  # Sortir de la boucle une fois l'élément trouvé et cliqué

    # Modifier le formulaire 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
    
    inputAModif = driver.find_element(By.NAME, "name").clear()
    inputAModif = driver.find_element(By.NAME, "name").send_keys(CATEGORY_NAME_new)
    
    # Sauvegarder la catégorie
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button.primary[type='button']"))).click()

    #test du toast
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "Toastify__toast-body"),"Category saved successfully!"))
    toast = driver.find_element(By.CLASS_NAME, "Toastify__toast-body")
    assert "Category saved successfully!" in toast.text
