"""
1. 크롤링을 위해 크롤링할 사이트의 페이지의 HTML 구조 분석 필요
2. 크롤링할 데이터가 어떤 태그에 포함되어 있는지 확인
3. 크롤링한 데이터를 CSV 파일로 저장 (행, 열 정렬하여)
"""

"""
코드 설명
setup_driver 함수:
Chrome 드라이버를 초기화하고 헤드리스(백그라운드) 모드로 실행.
webdriver-manager를 사용해 드라이버를 자동으로 관리.

crawl_titles 함수:
주어진 URL에 접속하고 h1 태그를 크롤링.
텍스트가 비어 있지 않은 제목만 추출.
추출된 데이터를 출력하고, CSV 파일로 저장.

save_to_csv 함수:
크롤링한 데이터를 지정된 CSV 파일에 저장.
첫 줄은 "Title" 헤더로 작성.

__main__:
크롤링할 URL과 저장할 CSV 파일 경로를 지정.
crawl_titles를 호출하여 크롤링 수행.


이 코드로 할 수 있는 것
Selenium을 사용하여 웹 페이지의 h1 태그를 추출.
데이터를 CSV 파일로 저장.
자동으로 Chrome 드라이버 관리.
"""
import requests
from urllib.robotparser import RobotFileParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    """
    브라우저 드라이버 설정 및 초기화.
    `webdriver-manager`를 사용하여 Chrome 드라이버를 자동으로 다운로드 및 관리.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 브라우저 창 숨기기 (필요시 주석 처리)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def can_crawl(url):
    """
    주어진 URL이 크롤링 가능한지 robots.txt 파일을 통해 확인.
    
    Args:
        url (str): 확인할 웹 페이지 URL.
    
    Returns:
        bool: 크롤링 가능 여부.
    """
    parsed_url = requests.utils.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    
    return rp.can_fetch("*", url)

def crawl_titles(url, output_file):
    """
    웹 페이지에서 제목 데이터를 크롤링하고 CSV 파일에 저장.
    
    Args:
        url (str): 크롤링할 웹 페이지 URL.
        output_file (str): 결과를 저장할 CSV 파일 경로.
    """
    driver = setup_driver()  # 드라이버 설정 및 초기화
    try:
        # URL 접속
        driver.get(url)
        time.sleep(10)  # 페이지 로드 10초 대기
        
        # h1, h2, p 태그 추출
        titles = driver.find_elements(By.TAG_NAME, 'h1')
        subtitles = driver.find_elements(By.TAG_NAME, 'h2')
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        
        extracted_titles = [title.text.strip() for title in titles if title.text.strip()]
        extracted_subtitles = [subtitle.text.strip() for subtitle in subtitles if subtitle.text.strip()]
        extracted_paragraphs = [paragraph.text.strip() for paragraph in paragraphs if paragraph.text.strip()]
        
        if not extracted_titles and not extracted_subtitles and not extracted_paragraphs:
            print("No important content found. The HTML structure might have changed.")
        else:
            print("Extracted Content:")
            for i, title in enumerate(extracted_titles, start=1):
                print(f"Title {i}: {title}")
            for i, subtitle in enumerate(extracted_subtitles, start=1):
                print(f"Subtitle {i}: {subtitle}")
            for i, paragraph in enumerate(extracted_paragraphs, start=1):
                print(f"Paragraph {i}: {paragraph}")
        
        # 데이터 저장
        save_to_csv(output_file, extracted_titles + extracted_subtitles + extracted_paragraphs)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # 드라이버 종료

def save_to_csv(file_path, data):
    """
    데이터를 CSV 파일로 저장.
    
    Args:
        file_path (str): 저장할 CSV 파일 경로.
        data (list): 저장할 데이터 리스트.
    """
    try:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Title'])  # 헤더 작성
            for row in data:
                writer.writerow([row])
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Failed to save data: {e}")

if __name__ == "__main__":
    # 크롤링할 URL과 저장할 파일 경로 설정
    target_url = "https://www.google.com/search?q=google&oq=google&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg8MgYIAhBFGEEyBggDEEUYPDIGCAQQRRhBMgYIBRBFGEHSAQk0MDg0ajBqMTWoAgCwAgA&sourceid=chrome&ie=UTF-8"  # 크롤링할 웹 페이지 URL
    output_csv = "C:/Users/rlawjdgns213/Desktop/crawled.csv"  # 저장할 CSV 파일 경로
    
    crawl_titles(target_url, output_csv)  # 크롤링 수행