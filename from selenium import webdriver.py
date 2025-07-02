from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time,threading,logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

def create_chrome_driver()->webdriver.Chrome:
    options=Options()
    options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
def  monitor_and_close_window(driver: webdriver.Chrome):
    while True:
        try:
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
            close_button.click()
            time.sleep(1)
            
        except Exception:
            time.sleep(1)

def login(driver:webdriver.Chrome,account:str,password:str):
    driver.get("http://sit-admin2.tcg.com/")
    OperationName=WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//input[contains(@id, "operatorName")]'))
    )
    OperationName.send_keys(f"{account}")
    time.sleep(0.5)

    Password=WebDriverWait(driver,30).until(
        EC.visibility_of_element_located((By.XPATH, '//input[contains(@id, "password")]'))
    )
    Password.send_keys(f"{password}")
    time.sleep(0.5)

    switch_button=driver.find_element(By.XPATH, "//span[@class='ant-switch-inner']")
    switch_button.click()

    login_button=driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(1)
    logging.info("登入成功")

def promotion_page(driver):
    Promotion=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='ant-menu-title-content' and text()='活动红利']"))
    )
    Promotion.click()
    time.sleep(0.5)
    Manual_Promotion=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='ant-menu-title-content']//a[@title='手动活动红利']"))
    )
    Manual_Promotion.click()
    time.sleep(0.5)
    Manual_promo=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='tab' and text()='手动活动红利']"))
    )
    Manual_promo.click()
    time.sleep(1)

def promotion_bonus_1(driver):
    logging.info("開始測試case=====TCG-106897.010.060=====")
    start_time=time.time()
    try:
        Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
        Search.click()
    except TimeoutException:
        logging.error("加載過慢")
    end_time=time.time()
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename=f"screenshot{timestamp}.png"
    duration=end_time-start_time
    if duration > 1:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    logging.info("====== Case PASS ======")
    time.sleep(2)
    driver.save_screenshot(filename)


def promotion_bonus_2(driver,promotion_name:str):
    logging.info("開始測試case=====TCG-106897.010.061=====")
    promotion_name_input=WebDriverWait(driver, 20).until(

            EC.visibility_of_element_located((By.XPATH, "(//input[@id='promotionName'])[2]"))
    )
    promotion_name_input.send_keys(f"{promotion_name}")
    time.sleep(2)
    start_time=time.time()
    try:
        Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
        Search.click()
    except TimeoutException:
        logging.error("加載過慢")
    end_time=time.time()
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename=f"screenshot{timestamp}.png"
    duration=end_time-start_time
    if duration > 2:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    logging.info("====== Case PASS ======")
    time.sleep(2)
    driver.save_screenshot(filename)
def promotion_bonus_3(driver):  

    logging.info("開始測試case=====TCG-106897.010.062=====")
    promotion_name_input = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "(//input[@id='promotionName'])[2]"))
    )
    promotion_name_input.click() 
    promotion_name_input.send_keys(Keys.CONTROL + "a") 
    promotion_name_input.send_keys(Keys.BACKSPACE) 
    promotion_name_input.clear()
    driver.execute_script("""
    const input = arguments[0];
    const lastValue = input.value;

    input.value = '';

    const tracker = input._valueTracker;
    if (tracker) {
        tracker.setValue(lastValue);
    }

    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    """, promotion_name_input)
    time.sleep(1)

    Condition=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='ant-select-selection-item' and @title='开始']"))
    )
    Condition.click()

    ALL_button=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content']"))
    )
    ALL_button.click()
    time.sleep(1)

    start_time=time.time()
    try:
        Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid']"))
        )
        Search.click()
    except TimeoutException:
        logging.error("加載過慢")

    end_time=time.time()
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename=f"screenshot{timestamp}.png"
    duration=end_time-start_time
    if duration > 1:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    time.sleep(2)
    driver.save_screenshot(filename)
def promotion_bonus_4(driver):

    logging.info("開始測試case=====TCG-106897.010.063=====")
    Condition=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='ant-select-selection-item' and @title='全部']"))
    )
    Condition.click()
    time.sleep(2)
    Finish_button=WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content' and text()='结束']"))
    )
    Finish_button.click()
    time.sleep(2)
    start_time=time.time()
    try:
        Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
        Search.click()
    except TimeoutException:
        logging.error("加載過慢")
    end_time=time.time()
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename=f"screenshot{timestamp}.png"
    duration=end_time-start_time
    if duration > 1:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    time.sleep(1)

    driver.save_screenshot(filename)
def bind_check(driver):
    Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
    Search.click()
    time.sleep(1)
    start_time=time.time()
    try:
        Bind_button=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '绑定')]"))
        )
        Bind_button.click()
    except TimeoutException:
        logging.error("加載過慢")
        
    end_time=time.time()
    duration=end_time-start_time
    if duration > 1:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    time.sleep(2)
    try:
        close_btn=WebDriverWait(driver, ).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'ant-btn') and .//span[text()='取 消']]"))
            )
        close_btn.click()
        WebDriverWait(driver, 5).until(EC.invisibility_of_element(close_btn))
    except TimeoutException:
        logging.warning("關閉")
        time.sleep(2)
def update(driver):
    Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
    Search.click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.XPATH, '//button[@aria-label="Close"]'))
    )
    
    start_time=time.time()
    update_button=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "(//button[@type='button']//span[text()='编辑'])[1]"))
        )
    update_button.click()
    WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@class='ant-col ant-form-item-label css-fazdi2']//b"),
        "形容（前端可见）"
    ))
    end_time=time.time()
    
    screenshot_function(driver)
    duration=end_time-start_time
    if duration > 3:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    
    ActionFunction(driver)
    

def check(driver):
    Search=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='ant-btn css-fazdi2 ant-btn-primary ant-btn-color-primary ant-btn-variant-solid' ]"))
        )
    Search.click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.XPATH, '//button[@aria-label="Close"]'))
    )
    start_time=time.time()
    check_btn=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@type='button']//span[text()='查看']"))
        )
    check_btn.click()
    
    loaded=WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@class='ant-col ant-form-item-label css-fazdi2']//b"),
        "形容（前端可见）"
    ))
    if not loaded:
        logging.error("沒等到文字")
        return

    end_time=time.time()
    time.sleep(5)
    screenshot_function(driver)
    duration=end_time-start_time
    if duration > 3:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    ActionFunction(driver)
    

def copy(driver):
    WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.XPATH, '//button[@aria-label="Close"]'))
    )
    start_time=time.time()
    copy_button=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@type='button']//span[text()='复制']"))
        )
    copy_button.click()
    WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element((By.XPATH, "//div[@class='ant-modal-title']//b[text()='创建手动活动红利']"))  
    )
    WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@class='ant-col ant-form-item-label css-fazdi2']//b"),
        "形容（前端可见）"
    ))

    end_time=time.time()
    time.sleep(5)
    screenshot_function(driver)
    duration=end_time-start_time
    if duration > 3:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    ActionFunction(driver)

def create(driver):
    WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.XPATH, '//button[@aria-label="Close"]'))
    )
    start_time=time.time()
    create_button=WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "(//button[@type='button' and .//span[contains(@class, 'ant-btn-icon')] and .//span[text()='新增']])[3]"))
        )
    create_button.click()
    WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@class='ant-col ant-form-item-label css-fazdi2']//b"),
        "形容（前端可见）"
    ))
    end_time=time.time()
    time.sleep(5)
    screenshot_function(driver)
    duration=end_time-start_time
    if duration > 3:
        logging.warning(f"⚠️ Loading 過久: {duration:.2f} 秒")
    else:
        logging.info(f"✅ Loading 正常: {duration:.2f} 秒")
    ActionFunction(driver)

def screenshot_function(driver):
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename=f"screenshot{timestamp}.png"
    driver.save_screenshot(filename)
def ActionFunction(driver):
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    actions.move_by_offset(0, 0).click().perform()
    actions.reset_actions()
if __name__=='__main__':

    driver=create_chrome_driver()
    account="carrine03"
    password="Test@1234"
    promotion_name="ddd1111111"

    try:
        monitor_thread=threading.Thread(target=monitor_and_close_window,args=(driver,),daemon=True)
        monitor_thread.start()
        login(driver,account=account,password=password)
        promotion_page(driver)
        #promotion_bonus_1(driver)
        #promotion_bonus_2(driver,promotion_name)
        #promotion_bonus_3(driver)
        #promotion_bonus_4(driver)
        #update(driver)
        #time.sleep(1)
        check(driver)
        time.sleep(1)
        copy(driver)
        time.sleep(1)
        create(driver)
        #for _ in range(10):
         #   bind_check(driver)
        
    finally:
        input("Press Enter to close the browser...")
        driver.quit()