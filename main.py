import cv2
import numpy as np
import pyautogui
import re
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# type your email and password
LOGIN = "email@email.com"
PASSWORD = "password"

block_image = cv2.imread('Resources/blockButton.PNG')

# logowanie do strony
def login(login, password):
    # czekanie na zaladowanie okienka z ciasteczkami
    cookies_window_loaded = expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '[data-cookiebanner = "accept_button"]'))
    WebDriverWait(driver, 15).until(cookies_window_loaded)
    cookies_button = driver.find_element(By.CSS_SELECTOR, '[data-cookiebanner = "accept_button"]')
    # akceptacja ciasteczek
    cookies_button.click()

    print("logowanie...")
    # czekanie na zaladowanie formularza
    form_email_loaded = expected_conditions.presence_of_all_elements_located((By.ID, 'email'))
    form_password_loaded = expected_conditions.presence_of_all_elements_located((By.ID, 'pass'))
    form_loginbutton_loaded = expected_conditions.presence_of_all_elements_located((By.NAME, 'login'))
    WebDriverWait(driver, 10).until(form_email_loaded)
    WebDriverWait(driver, 10).until(form_password_loaded)
    WebDriverWait(driver, 10).until(form_loginbutton_loaded)

    login_form = driver.find_element(By.ID, 'email')
    password_form = driver.find_element(By.ID, 'pass')
    button_login_form = driver.find_element(By.NAME, 'login')
    login_form.click()
    # wprowadzenie danych
    login_form.send_keys(login)
    password_form.click()
    password_form.send_keys(password)
    button_login_form.click()
    print('Zalogowano')

# funkcja do klikania zaczepek
def clickPokes():
    pokes_loaded = expected_conditions.presence_of_all_elements_located((
        By.CSS_SELECTOR, '[aria-label = "Odpowiedz na zaczepkę"]'))
    try:
        WebDriverWait(driver, 15).until(pokes_loaded)
    except TimeoutException:
        print("Brak Zaczepek")
    pokesButtons = driver.find_elements(By.CSS_SELECTOR, '[aria-label = "Odpowiedz na zaczepkę"]')
    for button in pokesButtons:
        button.click()
        time.sleep(0.5)


def clickNotificationsButton():
    print("finding image block")
    time.sleep(8)
    w = block_image.shape[1]
    h = block_image.shape[0]
    center_w = w / 2
    center_h = h / 2

    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(img, block_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= .75:
        x = max_loc[0] + center_w
        y = max_loc[1] + center_h
        cv2.rectangle(img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)
        pyautogui.click(x, y)
        print("Zablokowano powiadomienia od fb")
    else:
        print("Brak okienka z powiadomieniami od fb")


# implementacja drivera do Chrome
driver = webdriver.Chrome('./chromedriver.exe')

# wyszukanie strony na Chrome
driver.get("https://facebook.com")
# logowanie
login(LOGIN, PASSWORD)

clickNotificationsButton()
time.sleep(3)
# przejscie na strone zaczepek
driver.get('https://www.facebook.com/pokes')
while True:
    clickPokes()