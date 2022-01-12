#%%
# Necesario instalar en caso que no las tengan
# pip install pandas
# pip install selenium
# Cargando las librerias necesarias
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
#%%
# Variables necesarios
path_webdriver = "/home/cbpaguay/Downloads/chromedriver"
url = "https://alert.socialsalert.com"
user = "qa-sa@golden-companies.com"
passwd = "uzS+u3f)PG{LC25u"
list_usernames = list()
cadena = "https://4v4t4r5.socialsalert.com/tw/"
paises = {"ECU":"Ecuador",
          "ARG":"Argentina",
          "BRA":"Brazil",
          "DOM":"Dominican Republic"}
# Opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--disabe-extensions')
options.add_argument('--start-maximized')

#%%
# Funciones
def click_btn(element):
    WebDriverWait(driver,5)\
    .until(EC.element_to_be_clickable((By.XPATH,element)))\
    .click()
        
def input_txt(element,text):
    WebDriverWait(driver,5)\
    .until(EC.element_to_be_clickable((By.XPATH,element)))\
    .send_keys(text)

def scroll_in_element(element):
    driver.execute_script("arguments[0].scrollIntoView();",element)
#%%
# Inicializa el bot
driver = webdriver.Chrome(path_webdriver,chrome_options=options)

# Se dirige a la pagina 
driver.get(url)

# Ingreso usuario
input_user ='//*[@id="root"]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[2]/div[1]/input' 
input_txt(input_user,user)

# Ingreso contrasena
input_passwd = '//*[@id="root"]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[2]/div[2]/input' 
input_txt(input_passwd,passwd)

# clic en iniciar sesion
login = '//*[@id="root"]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[3]/button' 
click_btn(login)
#%%
# clic en consultas
query = '//*[@id="root"]/div/div[2]/div/div[2]/ul/li[6]/a'
click_btn(query)

# clic en ir a dashboard
dashboard = '/html/body/div[2]/div/div[3]/div[2]/div/div[5]/div/div/div/div/div/div/div/div[1]/div[3]/div[4]/div/div[5]/div/div/a[1]'
click_btn(dashboard)

# clic en Quien
who = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/ul/li[6]/a'
click_btn(who)

# clic en Influencers
influencers = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div[6]/div/ul/li[2]/a'
click_btn(influencers)

# clic en Red Social
socials = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[1]/div/div[4]/a/div/div'
click_btn(socials)

# clic en Twitter
twitter = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[1]/div/div[4]/div/div/button[2]'
click_btn(twitter)

# hacer un scroll hasta el footer
footer = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[2]/footer')
scroll_in_element(footer)

# clic en pais
pais = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[1]/div/div[8]/a/div'
click_btn(pais)

#### COMENZAR EL BUCLE DE PAISES

for k,v in paises.items():

    #%%
    # Escribe el pais
    input_pais = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[1]/div/div[8]/div/div/div[1]/input'
    driver.find_element_by_xpath(input_pais).clear()
    input_txt(input_pais,v)

    # clic en Ecuador
    btn_pais_selected = '/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[1]/div/div[8]/div/div/div[2]/button[2]'
    click_btn(btn_pais_selected)

    # Scroll a la página hasta el inicio
    btn_qa = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div[1]/nav/div/div[2]/div[2]/button')
    scroll_in_element(btn_qa)
    #%%
    try:
        # Ya que el listado se carga de forma dinamica en la pagina, se procede a recolectar 
        # los datos en 3 tiempos
        for i in range(3):

            # Esperando un tiempo a que carguen los elementos
            time.sleep(5)
            # Capturando los influencers
            elems = driver.find_elements(By.TAG_NAME,"img")
            for elem in elems:
                usuario_tw = elem.get_attribute("src") 
                if cadena in usuario_tw:
                    list_usernames.append(usuario_tw)


            # Hacer un scroll en el cuadro de influencers 
            influencers_box = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div[6]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div[44]/div/div/span/a/div')
            scroll_in_element(influencers_box)

            # Esperando un tiempo a que carguen los elementos
    except Exception as e:
        print(e)

    # Manipulando y exportando el listado descargado
    df = pd.DataFrame(list_usernames)
    df.drop_duplicates(inplace=True)
    list_usernames = list()
    df.rename(columns={0: 'username'},inplace=True)
    df.username = df.username.apply(lambda x: x.replace(cadena,""))
    df['paisCalf']= k
    path_salida = v + "_influencers.csv"
    df.to_csv(path_salida,index=False)

    # Scroll hasta el footer
    scroll_in_element(footer)

# Scroll hasta la cabecera
scroll_in_element(btn_qa)

# Clic en el boton QA
btn_qa = '/html/body/div[2]/div/div[3]/div[1]/nav/div/div[2]/div[2]/button'
click_btn(btn_qa)

# Clic en cerrar sesion
logout = '/html/body/div[2]/div/div[3]/div[1]/nav/div/div[2]/div[2]/div/a[4]'
click_btn(logout)

# cierra el navegador
driver.close()
