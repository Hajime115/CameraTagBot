# -*- coding: utf-8 -*-
import os
import sys
import datetime
import random
import logging
import configparser
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def autolike():

    now = datetime.datetime.now()
    filePreFix=os.getcwd()

    # Configとログの読み込み
    INI_FILE = filePreFix + '/config/setting.ini'
    logging.basicConfig(filename=filePreFix + '/log/likeLog_{0:%Y%m%d}.log'.format(now),
                        level=logging.INFO, format='%(asctime)s %(message)s')

    config = configparser.ConfigParser()
    config.read(INI_FILE, 'UTF-8')
    sleepRandomMin = config.getint('System', 'sleepRandomMin')
    sleepRandomMax = config.getint('System', 'sleepRandomMax')

    # アクセス (ページの読み込み待ちは最大20秒)
    driver = webdriver.Chrome(config.get('System', 'webdriver'))
    driver.implicitly_wait(20)

    try:
        # ログイン
        driver.get(config.get('Element', 'loginURL'))
        sleep(random.randint(sleepRandomMin, sleepRandomMax))
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/"
                                     "div/article/div/div[1]/div/form/div[2]"
                                     "/div/label/input").send_keys(config.get('Account', 'id'))
        password = driver.find_element_by_name('password')
        password.send_keys(config.get('Account', 'pass'))
        password.send_keys(Keys.ENTER)
        sleep(random.randint(sleepRandomMin, sleepRandomMax))

        # ログイン情報の保存は後でを選択
        loginSaveElement = driver.find_elements_by_xpath(config.get('Element', 'loginSaveElement'))
        if len(loginSaveElement) > 0:
            loginSaveElement[0].click()

    	# お知らせをオンにするは後でを選択
        notificationOnElement = driver.find_elements_by_xpath(config.get('Element', 'notificationOnElement'))
        if len(notificationOnElement) > 0:
            notificationOnElement[0].click()

        # ポップアップの後でを選択
        popupElement = driver.find_elements_by_xpath(config.get('Element', 'popUpElement'))
        if len(popupElement) > 0:
            popupElement[0].click()

        # 設定ファイルのタグをランダムに検索
        sleep(random.randint(sleepRandomMin, sleepRandomMax))
        tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9', 'tag10']
        tag = config.get('Tags', tags[random.randint(0, 9)])
        tagUrl = 'https://www.instagram.com/explore/tags/' + tag
        driver.get(tagUrl)
        driver.find_element_by_xpath(config.get('Element', 'searchBarElement')).click()
        sleep(random.randint(sleepRandomMin, sleepRandomMax))

        # 一日の上限になるまでいいねしつづける
        likeCount = 0
        likeLimit = config.getint('System', 'dailyLikeLimit')
        goodThroughCount = config.getint('System', 'goodThroughCount')
        logging.info(u'いいね処理開始! タグは [ %s ]', tag)

        while likeLimit > likeCount:

            # いいね判定 既にいいねしていたらパス
            alreadyGood = driver.find_elements_by_css_selector(u'[aria-label=「いいね！」を取り消す]')
            if len(alreadyGood) == 0:
                # ユーザー情報取得
                userName = driver.find_element_by_xpath(
                    "/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a").text
                try:
                    userLikeCount = int(driver.find_element_by_xpath(
                        "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button/span").text)
                except:
                    userLikeCount = -1

                # いいねが設定値(goodThroughCount)以下の投稿にだけいいねする
                if goodThroughCount > userLikeCount:
                    driver.find_element_by_xpath(config.get('Element', 'goodHeartButton')).click()
                    likeCount += 1
                    logging.info(u'本日 %d回目の いいね! です。 %sの投稿に いいね! しました。', likeCount, userName)

            sleep(random.randint(sleepRandomMin, sleepRandomMax))
            driver.find_element_by_css_selector(config.get('Element', 'nextPhotoArrow')).click()
    except Exception as err:
        logging.exception(err)
    finally:
        logging.info(u'処理終了!')
        driver.quit()


if __name__ == '__main__':
    autolike()
