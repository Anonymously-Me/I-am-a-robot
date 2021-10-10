from selenium.webdriver.common.action_chains import ActionChains
from random import randint
from time import sleep
from wget import download
from pydub import AudioSegment
import speech_recognition as sr
import os


class Docaptcha:

	def __init__(self, driver, xpath) -> None:
		self.driver = driver
		self.xpath = xpath
	
	def solve(self):
		action = ActionChains(self.driver)
		size = {'width': self.driver.execute_script('return document.body.clientWidth'), 'height': self.driver.execute_script('return document.body.clientHeight')}
		print(f"size: {size}")
		x, y = 0, 0
		for i in range(randint(5, 10)):
			randx = randint(-1 * (x - 1), size['width'] - (x + 1))
			randy = randint(-1 * (y - 1), size['height'] - (y + 1))
			x += randx
			y += randy
			action.move_by_offset(randx, randy)
			action.pause(0.5)
		action.move_to_element(self.driver.find_element_by_xpath(self.xpath))
		action.pause(1)
		action.perform()
		self.driver.find_element_by_xpath(self.xpath).click()
		sleep(1)
		action.move_to_element(self.driver.find_element_by_xpath(self.xpath))
		self.driver.switch_to.frame(self.driver.find_element_by_css_selector('iframe[title="recaptcha challenge"]'))
		sleep(1)
		action1 = ActionChains(self.driver)
		action1.move_to_element(self.driver.find_element_by_id('recaptcha-help-button'))
		action1.pause(0.5)
		action1.move_to_element(self.driver.find_element_by_id('recaptcha-audio-button'))
		
		action1.perform()
		sleep(1)
		self.driver.find_element_by_id('recaptcha-audio-button').click()
		sleep(1)
		while True:
			try:
				audio_btn = self.driver.find_element_by_class_name('rc-audiochallenge-tdownload-link')
			except:
				return
			link = audio_btn.get_attribute('href')
			if os.path.exists('audio.mp3'):
				os.remove('audio.mp3')
				download(link, 'audio.mp3')
			else:
				download(link, 'audio.mp3')
			s = AudioSegment.from_mp3('audio.mp3')
			s.export('audio.wav', format='wav')
			r = sr.Recognizer()
			with sr.AudioFile('audio.wav') as source:
				audio = r.record(source)
			try:
				text = r.recognize_google(audio)
				self.driver.find_element_by_id('audio-response').send_keys(text)
				sleep(3)
				action2 = ActionChains(self.driver)
				action2.move_to_element(self.driver.find_element_by_id('recaptcha-reload-button'))
				action2.move_to_element(self.driver.find_element_by_id('recaptcha-verify-button'))
				action2.perform()
				sleep(5)
				self.driver.find_element_by_id('recaptcha-verify-button').click()
			except sr.UnknownValueError:
				print(" Could not understand audio")
			except sr.RequestError as e:
				print("Error: {0}".format(e))
			if os.path.exists('audio.mp3'):
				os.remove('audio.mp3')
			if os.path.exists('audio.wav'):
				os.remove('audio.wav')
