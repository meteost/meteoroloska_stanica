import pygame
from pygame.locals import *
import time
import datetime
import calendar
import pywapi
from icon_defs import *
from background_defs import *
from bme280 import *
from w1thermsensor import *
import Adafruit_DHT

sensor = W1ThermSensor()
DHT_SENSOR = Adafruit_DHT.DHT22

DHT_PIN = 16
import string

MAX_WIDTH = 800
MAX_HEIGHT = 600
HALF_WIDTH = MAX_WIDTH/2
THIRD_WIDTH = MAX_WIDTH/3
QUARTER_WIDTH = MAX_WIDTH/4
HALF_HEIGHT = MAX_HEIGHT/2
QUARTER_HEIGHT = MAX_HEIGHT/4
white = (255,255,255)
green = (0,255,0)
window = 'w' #pocetni je weather prikaz

#postavljanje prozora
pygame.init()

screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

pygame.display.set_caption("Weather")

icon = pygame.image.load('icon.jpeg')
pygame.display.set_icon(icon)

#program se pokrece
running = True

while running:
	for event in pygame.event.get():
		#izlazak iz programa
		if event.type == pygame.QUIT:
			running = False
			
		#mijenjanje prikaza
		if event.type == pygame.KEYDOWN:
			if event.key == K_s: #prikaz mjerenja senzora
				window = 's'
			elif event.key == K_w: #prikaz vremenske prognoze
				window = 'w'
			elif event.key == K_q: #izlazak iz programa
				running = False
			
	screen.fill((0, 0, 0))
	
	#dohvacanje podataka za odredeni grad
	result = pywapi.get_weather_from_weather_com('HRXX0019', units = 'metric')
	
	#pozadinska slika
	background_br = int(result['current_conditions']['icon'])
	background = pygame.image.load(bd + backgrounds[background_br]).convert_alpha()
	background = pygame.transform.scale(background, (800,600))
	screen.blit(background, (0, 0))
	
	#zaglavlje
	pygame.draw.rect(screen, (0, 0, 0), (0,0,MAX_WIDTH,MAX_HEIGHT/12), 0)
	
	#fonts
	font_big = pygame.font.SysFont( "freesans", MAX_HEIGHT/15, bold = 1)
	font_small = pygame.font.SysFont( "freesans", MAX_HEIGHT/30, bold = 1)
	
	#datum i vrijeme
	t1 = time.strftime("%b %d, %a", time.localtime())
	t2 = time.strftime("%H:%M", time.localtime())
	t3 = time.strftime("%S", time.localtime())
	
	rt1 = font_big.render(t1, True, white)
	(tx1,ty1) = rt1.get_size()
	rt2 = font_big.render(t2, True, white)
	(tx2, ty2) = rt2.get_size()
	rt3 = font_small.render(t3, True, white )
	(tx3, ty3) = rt3.get_size()
	
	screen.blit(rt1, (3, 3))
	screen.blit(rt2, (MAX_WIDTH-3-tx3-tx2, 3))
	screen.blit(rt3, (MAX_WIDTH-3-tx3, 3))

	#podnozje
	pygame.draw.rect(screen, (0, 0, 0), (0,MAX_HEIGHT - 25,MAX_WIDTH,MAX_HEIGHT), 0)
	
	#vremenska prognoza
	if window == 'w':
		#grad
		font_location = pygame.font.SysFont("freesans", MAX_HEIGHT/20, bold = 0)
		location = font_location.render(result['location']['name'], True, white)
		(lx, ly) = location.get_size()
		screen.blit(location, (HALF_WIDTH - lx/2, MAX_HEIGHT/12 - ly - 3))
		
		#fonts
		font_temp = pygame.font.SysFont("freesans", MAX_HEIGHT/5, bold = 1)
		font_cels = pygame.font.SysFont("freesans", MAX_HEIGHT/10, bold = 1)
		font_text = pygame.font.SysFont("freesans", MAX_HEIGHT/25, bold = 1)
		font_left = pygame.font.SysFont("freesans", MAX_HEIGHT/25, bold = 0)
		font_right = pygame.font.SysFont("freesans", MAX_HEIGHT/30, bold = 0)
		
		#podaci lijevo
		temp = font_temp.render(result['current_conditions']['temperature'], True, white)
		(tempx, tempy) = temp.get_size()
		cels = font_cels.render(unichr(0x2103), True, white)
		(celsx, celsy) = cels.get_size()
		text = font_text.render(result['current_conditions']['text'], True, white)
		(textx, texty) = text.get_size()
		feel = font_left.render("Feels like: " + result['current_conditions']['feels_like'] + unichr(0x2103), True, white)
		(feelx, feely) = feel.get_size()
		hl = font_left.render("High/Low: " + result['forecasts'][0]['high'] + "/" + result['forecasts'][0]['low'] + unichr(0x2103), True, white)
		(hlx, hly) = hl.get_size()
		hum = font_left.render("Humidity: " + result['current_conditions']['humidity'] + "%", True, white)
		(humx, humy) = hum.get_size()
		#podaci desno
		sunrise = font_right.render("Sunrise: " + result['forecasts'][0]['sunrise'], True, white)
		(sunrisex, sunrisey) = sunrise.get_size()
		sunset = font_right.render("Sunset: " + result['forecasts'][0]['sunset'], True, white)
		(sunsetx, sunsety) = sunrise.get_size()
		uv = font_right.render("UV: " + result['current_conditions']['uv']['text'], True, white)
		(uvx, uvy) = uv.get_size()
		moon = font_right.render("Moon phase: " + result['current_conditions']['moon_phase']['text'], True, white)
		(moonx, moony) = moon.get_size()
		wind = font_right.render("Wind: " + result['current_conditions']['wind']['text'], True, white)
		(windx, windy) = wind.get_size()
		rain = font_right.render("Chance of rain (day/night): " + result['forecasts'][0]['day']['chance_precip'] + 
		"/" + result['forecasts'][0]['night']['chance_precip'] + "%", True, white)
		(rainx, rainy) = rain.get_size()
	
		#ispis podataka lijevo
		screen.blit(temp, (QUARTER_WIDTH - tempx/2, QUARTER_HEIGHT - tempy + MAX_HEIGHT/12))
		screen.blit(cels, (QUARTER_WIDTH - tempx/2 + tempx, QUARTER_HEIGHT - tempy + MAX_HEIGHT/12))
		screen.blit(text, (QUARTER_WIDTH - textx/2, QUARTER_HEIGHT + 1.5*texty))
		screen.blit(feel, (QUARTER_WIDTH - feelx/2, QUARTER_HEIGHT + 2.5*texty))
		screen.blit(hl, (QUARTER_WIDTH - hlx/2, QUARTER_HEIGHT + 3.5*texty))
		screen.blit(hum, (QUARTER_WIDTH - humx/2, QUARTER_HEIGHT + 4.5*texty))
		#ispis podataka desno
		screen.blit(sunrise, (3*QUARTER_WIDTH - sunrisex/2, QUARTER_HEIGHT - 2*sunrisey))
		screen.blit(sunset, (3*QUARTER_WIDTH - sunsetx/2, QUARTER_HEIGHT - sunsety))
		screen.blit(uv, (3*QUARTER_WIDTH - uvx/2, QUARTER_HEIGHT))
		screen.blit(moon, (3*QUARTER_WIDTH - moonx/2, QUARTER_HEIGHT + moony))
		screen.blit(wind, (3*QUARTER_WIDTH - windx/2, QUARTER_HEIGHT + 2*windy))
		screen.blit(rain, (3*QUARTER_WIDTH - rainx/2, QUARTER_HEIGHT + 3*rainy))
		
		#fonts
		font_days = pygame.font.SysFont("freesans", MAX_HEIGHT/30, bold = 0)
		day_name = font_days.set_underline(True)
		font_numbers = pygame.font.SysFont("freesans", MAX_HEIGHT/30, bold = 0)
		
		#prvi dan
		day_name = font_days.render(result['forecasts'][1]['day_of_week'], True, white)
		(dnx, dny) = day_name.get_size()
		hl = font_numbers.render(result['forecasts'][1]['high'] + "/" + result['forecasts'][1]['low'] + 
		unichr(0x2103), True, white)
		(hlx, hly) = hl.get_size()
		humidity = font_numbers.render(result['forecasts'][1]['day']['humidity'] + "/" + 
		result['forecasts'][1]['night']['humidity'] + "%", True, white)
		(hx, hy) = humidity.get_size()
		icon_br = int(result['forecasts'][1]['day']['icon'])
		icon = pygame.image.load(sd + icons[icon_br]).convert_alpha()
		(ix, iy) = icon.get_size()
		
		screen.blit(day_name, (QUARTER_WIDTH/2 - 0.5*dnx, HALF_HEIGHT + dny))
		screen.blit(hl, (QUARTER_WIDTH/2 - 0.5*hlx, MAX_HEIGHT - 4*hly))
		screen.blit(humidity, (QUARTER_WIDTH/2 - 0.5*hx, MAX_HEIGHT - 3*hy))
		screen.blit(icon, (QUARTER_WIDTH/2 - 0.5*ix, HALF_HEIGHT + iy))
		
		#drugi dan
		day_name = font_days.render(result['forecasts'][2]['day_of_week'], True, white)
		(dnx, dny) = day_name.get_size()
		hl = font_numbers.render(result['forecasts'][2]['high'] + "/" + result['forecasts'][1]['low'] + 
		unichr(0x2103), True, white)
		(hlx, hly) = hl.get_size()
		humidity = font_numbers.render(result['forecasts'][2]['day']['humidity'] + "/" + 
		result['forecasts'][1]['night']['humidity'] + "%", True, white)
		(hx, hy) = humidity.get_size()
		icon_br = int(result['forecasts'][2]['day']['icon'])
		icon = pygame.image.load(sd + icons[icon_br]).convert_alpha()
		(ix, iy) = icon.get_size()
		
		screen.blit(day_name, (QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*dnx, HALF_HEIGHT + dny))
		screen.blit(hl, (QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*hlx, MAX_HEIGHT - 4*hly))
		screen.blit(humidity, (QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*hx, MAX_HEIGHT - 3*hy))
		screen.blit(icon, (QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*ix, HALF_HEIGHT + iy))
		
		#treci dan
		day_name = font_days.render(result['forecasts'][3]['day_of_week'], True, white)
		(dnx, dny) = day_name.get_size()
		hl = font_numbers.render(result['forecasts'][3]['high'] + "/" + result['forecasts'][1]['low'] + 
		unichr(0x2103), True, white)
		(hlx, hly) = hl.get_size()
		humidity = font_numbers.render(result['forecasts'][3]['day']['humidity'] + "/" + 
		result['forecasts'][1]['night']['humidity'] + "%", True, white)
		(hx, hy) = humidity.get_size()
		icon_br = int(result['forecasts'][3]['day']['icon'])
		icon = pygame.image.load(sd + icons[icon_br]).convert_alpha()
		(ix, iy) = icon.get_size()
		
		screen.blit(day_name, (HALF_WIDTH + QUARTER_WIDTH/2 - 0.5*dnx, HALF_HEIGHT + dny))
		screen.blit(hl, (HALF_WIDTH + QUARTER_WIDTH/2 - 0.5*hlx, MAX_HEIGHT - 4*hly))
		screen.blit(humidity, (HALF_WIDTH + QUARTER_WIDTH/2 - 0.5*hx, MAX_HEIGHT - 3*hy))
		screen.blit(icon, (HALF_WIDTH + QUARTER_WIDTH/2 - 0.5*ix, HALF_HEIGHT + iy))
		
		#cetvrti dan
		day_name = font_days.render(result['forecasts'][4]['day_of_week'], True, white)
		(dnx, dny) = day_name.get_size()
		hl = font_numbers.render(result['forecasts'][4]['high'] + "/" + result['forecasts'][1]['low'] + 
		unichr(0x2103), True, white)
		(hlx, hly) = hl.get_size()
		humidity = font_numbers.render(result['forecasts'][4]['day']['humidity'] + "/" + 
		result['forecasts'][1]['night']['humidity'] + "%", True, white)
		(hx, hy) = humidity.get_size()
		icon_br = int(result['forecasts'][4]['day']['icon'])
		icon = pygame.image.load(sd + icons[icon_br]).convert_alpha()
		(ix, iy) = icon.get_size()
		
		screen.blit(day_name, (3*QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*dnx, HALF_HEIGHT + dny))
		screen.blit(hl, (3*QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*hlx, MAX_HEIGHT - 4*hly))
		screen.blit(humidity, (3*QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*hx, MAX_HEIGHT - 3*hy))
		screen.blit(icon, (3*QUARTER_WIDTH + QUARTER_WIDTH/2 - 0.5*ix, HALF_HEIGHT + iy))
		
		#vrijeme zadnjeg azuriranja podataka
		font_update = pygame.font.SysFont( "freesans", MAX_HEIGHT/35, bold = 0)
	
		update = font_update.render("Last updated: " + result['current_conditions']['last_updated'], True, white)
		(update_x, update_y) = update.get_size()
	
		screen.blit(update, (MAX_WIDTH - update_x - 2, MAX_HEIGHT - update_y - 2))
		
		pygame.display.update()
		
	
	#mjerenja senzora
	if window == 's':
		#fonts
		font_sensors = pygame.font.SysFont("freesans", MAX_HEIGHT/20, bold = 0)
		font_sensors_br = pygame.font.SysFont("freesans", MAX_HEIGHT/15, bold = 1)
		
		#naslov
		sensors = font_sensors.render("Sensors", True, white)
		(sensorsx, sensorsy) = sensors.get_size()
		
		#DHT22
		humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
		
		#temperatura
		temp1_s = font_sensors.render("Temperature: ", True, white)
		(temp1_sx, temp1_sy) = temp1_s.get_size()
		temp1_sbr = font_sensors_br.render("%.1f\xb0C" % temperature, True, white)
		(temp1_sbrx, temp1_sbry) = temp1_sbr.get_size()
		#vlaga
		hum_s = font_sensors.render("Humidity: ", True, white)
		(hum_sx, hum_sy) = hum_s.get_size()
		hum_sbr = font_sensors_br.render("%.1f%%" % humidity, True, white)
		(hum_sbrx, hum_bry) = hum_sbr.get_size()
		
		#DS18B20
		temperature = sensor.get_temperature()
		
		#temperatura
		temp2_s = font_sensors.render("Temperature: ", True, white)
		(temp2_sx, temp2_sy) = temp2_s.get_size()
		temp2_sbr = font_sensors_br.render("%.1f\xb0C" % temperature, True, white)
		(temp2_sbrx, temp2_sbry) = temp2_sbr.get_size()
		
		#bme280
		temperature,pressure = readBME280All()
		
		#temperatura
		temp3_s = font_sensors.render("Temperature: ", True, white)
		(temp3_sx, temp3_sy) = temp3_s.get_size()
		temp3_sbr = font_sensors_br.render("%.1f\xb0C" % temperature, True, white)
		(temp3_sbrx, temp3_sbry) = temp3_sbr.get_size()
		#tlak zraka
		press_s = font_sensors.render("Pressure: ", True, white)
		(press_sx, press_sy) = press_s.get_size()
		press_sbr = font_sensors_br.render("%.1f Pa" % pressure, True, white)
		(press_sbrx, press_sbry) = press_sbr.get_size()
		
		#ispis naslova
		screen.blit(sensors, (HALF_WIDTH - sensorsx/2, MAX_HEIGHT/12 - sensorsy - 3))
		
		#ispis DHT22
		screen.blit(temp1_s, (20, QUARTER_HEIGHT - temp1_sy))
		screen.blit(temp1_sbr, (QUARTER_WIDTH, QUARTER_HEIGHT))
		screen.blit(hum_s, (3*QUARTER_WIDTH - hum_sx, QUARTER_HEIGHT - hum_sy))
		screen.blit(hum_sbr, (3*QUARTER_WIDTH, QUARTER_HEIGHT))
		
		#ispis DS18B20
		screen.blit(temp2_s, (20, HALF_HEIGHT - 0.5*temp2_sy))
		screen.blit(temp2_sbr, (20 + temp2_sx, HALF_HEIGHT + 0.5*temp2_sbry))
		
		#ispis bme280
		screen.blit(temp3_s, (20, 3*QUARTER_HEIGHT))
		screen.blit(temp3_sbr, (QUARTER_WIDTH, 3*QUARTER_HEIGHT + temp3_sbry))
		screen.blit(press_s, (3*QUARTER_WIDTH - press_sx, 3*QUARTER_HEIGHT))
		screen.blit(press_sbr, (MAX_WIDTH - press_sbrx - 20, 3*QUARTER_HEIGHT + press_sbry))
	
		pygame.display.update()
	
pygame.quit()
	
