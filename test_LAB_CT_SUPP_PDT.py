import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "h1.page-heading-title")))
    dashboard_title = driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
    assert "Dashboard" in dashboard_title

# ✅ Test de suppression de catégorie
def test_supp_pdt(driver):
    # Connexion d'abord
    login(driver)

    # Aller dans "Categories"
    pdt_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "a[href='http://localhost:3000/admin/products']")))
    pdt_link.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "h1.page-heading-title")))
    assert "Products" in driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text

   
    # Vérifier si le message "There is no product to display" est visible
    no_pdt_message = driver.find_elements(By.CSS_SELECTOR, "div.flex.w-full.justify-center")
    if no_pdt_message and no_pdt_message[0].is_displayed():
        if "There is no product to display" in no_pdt_message[0].text:
            pytest.skip("Aucun produit à afficher, test arrêté.")

    #coche le premier bouton radio de la liste des categories, le générique
    boutonRadio = driver.find_elements(By.CSS_SELECTOR, ".field-wrapper.radio-field")
    boutonRadio[0].click()
    
    delete_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "div.inline-flex a:nth-of-type(4)")))
    delete_button.click()
    
    # Localiser la modale
    modal_wrapper = driver.find_element(By.CLASS_NAME, "modal-wrapper")

    # Simuler un hover sur la modale pour retirer l'opacité (sans JavaScript)
    action = ActionChains(driver)
    action.move_to_element(modal_wrapper).perform()

    # Attendre que le bouton "Delete" devienne cliquable
    modal_delete_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.critical span"))
    )

    # Cliquer sur le bouton "Delete"
    modal_delete_button.click()


    final_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "div.flex.w-full.justify-center")))
    assert "There is no product to display" in final_message.text

