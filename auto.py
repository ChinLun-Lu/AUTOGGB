from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#開啟GeoGebra，用driver開啟特定網頁
geogebra_classic = "https://www.geogebra.org/classic"
driver = webdriver.Chrome(executable_path="/Users/chinlun/Downloads/chromedriver")
driver.get(geogebra_classic)



#等待
time.sleep(5)

#關閉瀏覽器
driver.close()