from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

class TeslaParser:
	"""
		Class provide parsing www.tesla.com,
		get information about used models with price that less than MAX_PRICE
		and create messages
	"""
	BASE_URL = "https://www.tesla.com/used"
	PHANTOMJS_PATH = r".\phantomjs.exe"
	vehicles = []
	
	def __init__(self, MAX_PRICE):
		self.MAX_PRICE = MAX_PRICE
	
	def getVehicles(self):
		"""
		This method create list of vehicles with price less than MAX_PRICE
		"""
		self.vehicles = []
		soup = self.getPageSource()
		div = soup.find('div', class_='react-container')
		for vehicle in div.find_all('div', class_='vehicle-inner'):
			price = vehicle.find('p', class_='price').text
			if float(price[1:].replace(',', ''))<= self.MAX_PRICE:
				self.vehicles.append({
					"model_name": vehicle.find('div', class_='model-name').text,
					"battery_capacity": vehicle.find('p', class_='battery-capacity').text,
					"price": price,
					"mileage": vehicle.find('p', class_='mileage').text,
					"link": "https://www.tesla.com" + vehicle.find('a', class_='vehicle-link')["href"]
				})
		return self.vehicles
		
	def getPageSource(self):
		"""
		Method that return Soup type object 
		"""
		try:
			browser = webdriver.PhantomJS(self.PHANTOMJS_PATH)
		except Exception:
			print("phantomjs problem")
		browser.get(self.BASE_URL)
		soup = BeautifulSoup(browser.page_source, "html.parser")
		return soup
	
	def createMessage(self):
		"""
		This method create message. Type of messages is MIMEText
		"""
		self.getVehicles()
		if self.vehicles == []:
			return []
		text = "Hi, there! It looks like there is a great offer for you.\n"
		for vehicle in self.vehicles:
			text_part = """
Model name: {0}
Battery capacity: {1}
Price: {2}
Mileage: {3}
Link: {4}
________________________________
			""".format(vehicle["model_name"], vehicle["battery_capacity"],
					   vehicle["price"], vehicle["mileage"], vehicle["link"])
			text = text + text_part
		msg = MIMEText(text)
		msg['Subject'] = "Your new offers"
		print("Message created")
		return msg
		
def sendmail(msg, sender_email, sender_password, recipient_email):
	smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
	try:		
		smtpObj.starttls()
		smtpObj.login(sender_email, sender_password)
		smtpObj.sendmail(sender_email, recipient_email, msg.as_string())
		print("Notification message sent!")
	except Exception:
		print("Somthing bad with sending email")
	finally:
		smtpObj.quit()
		
def main():
	sender_email = "sender@gmail.com"
	sender_password = "password"
	recipient_email = "recipient@gmail.com."
	max_price = 36000
	
	while True:
		try:
			with open(r".\settings.txt", "r") as f:
				data = [line.rstrip("\n") for line in f]
			sender_email = data[0]
			sender_password = data[1]
			recipient_email = data[2]
			max_price = float(data[3].replace(" ", ""))
		except Exception:
			print("Something bad with reading from setting file")
		
		print(sender_email)
		print(recipient_email)
		print(max_price)
		
		try:
			teslaParser = TeslaParser(max_price)
			msg = teslaParser.createMessage()
		except Exception:
			print("Can`t load data from site. May be there is no internet connection")
		try:
			if msg != []:
				sendmail(msg, sender_email, sender_password, recipient_email)
			else:
				print("There are no offers")
		except:
			pass
		time.sleep(900)
		

if __name__ == "__main__":
	main()
