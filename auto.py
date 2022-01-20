from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

#開啟GeoGebra，用driver開啟特定網頁
geogebra_classic_home = "https://www.geogebra.org/classic"
driver = webdriver.Chrome(executable_path="/Users/chinlun/Downloads/AUTOGGB/chromedriver")
driver.get(geogebra_classic_home)

### GeoGebra自動繪圖區 ###

#等待
sleep(5)

#關閉瀏覽器
driver.close()