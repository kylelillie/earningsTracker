#1. On Friday mornings (TODAY), go to http://web.tmxmoney.com/earnings_cal.php?market=All&date=2017-05-03
#2. Cycle through [TODAY-(1,5)],which will be variable Reporting_Date, or the Monday-Friday (probably need Datetime), 
#   by modifying the URL.
#3. On each cycle, look through the entire stock symbol list for a match on that page.
#4. If there's a match, go to this link, substituting ADI for the matched symbol. Eg/
#		http://web.tmxmoney.com/financials.php?qm_symbol=ADI:US&type=IncomeStatement&rtype=Q
#5. Pick out "Net Income" from the first column, also, get the header of that first column, because that 
#   tells you the reporting date. Eg, 2017-01 means January 31, 2017. Also look for where it says "Fiscal Year Ends in____"
#6. Pick out "Net Income" from the last column, because that lets you compare year to year.
#7. Produce a dataframe with this format:
#		Name,Reporting_Date,Current_Net_Income,Old_Net_Income,Link
#
#	Data Sources: 	Name,Link -> earnings_list.csv
#					Reporting_Date -> URL in step 2
#					Current_Net_Income,Old_Net_Income -> scrape from website in step 4.
#8. Using the dataframe, it should be feasible to generate a generic sentence about the data and send it
#   as an email.
#
#		{Name} - {quarter_n year} net {income/loss} of ${###}, {up/down} from last year's {income/loss} of ${###}. {link}

from datetime import date, datetime, timedelta
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import feedparser
import re

def marketwire():

	n = 0
	
	d=feedparser.parse("http://www.marketwire.com/rss/ern.xml") #Marketwire RSS feed
	for post in d.entries:
		try:
			if(post.category.find("TSX")==0):
				
				html = requests.get(post.link).text
				data = BeautifulSoup(html,"lxml")		
				
				extract = data.findAll('meta',{'content':True})
				
				if (str(extract[4]).find('ALBERTA')>0) or (str(extract[4]).find('AB')>0):
					print(extract[4])
					n+=1
				
					print (post.category,post.link)
					name = str(post.category)
					n = name.index(':')
					name = name[n+1:]
					table = data.findAll('table')
					df = pd.DataFrame()
					
					with open(name+'-'+datetime.today().strftime('%Y-%m-%d')+".html", "w") as file:
						file.write(str(table))
						
				# elif ((post.category.find("RBC")) or (post.category.find("TD"))):
				
					# n+=1
					
					# print (post.category,post.link)
					# name = str(post.category)
					# n = name.index(':')
					# name = name[n+1:]
					# table = data.findAll('table')
					# df = pd.DataFrame()
					
					# with open(name+'-'+datetime.today().strftime('%Y-%m-%d')+".html", "w") as file:
						# file.write(str(table))
				
				else: pass
		except:
			pass

def tsx():		
	#load the list of companies
	company_list = pd.read_csv("earnings_list.csv")	
		
	#set up the base link to seach for stock symbols
	base = "http://web.tmxmoney.com/earnings_cal.php?market=All&date="
	detail = "http://web.tmxmoney.com/financials.php?qm_symbol=ADI:US&type=IncomeStatement&rtype=Q"

	for n in range(0,7):

		date = (datetime.today()-timedelta(days=n)).strftime('%Y-%m-%d')
		link = base+date
		
		html = requests.get(link).text
		bs = BeautifulSoup(html,"lxml")
		print(link)
		
		#set up the link to find financials for valid symbols
		for symbol in company_list["symbol"]:
		
			detail_mod = detail.replace("symbol=ADI:US","symbol="+symbol)
			
			if (bs.find_all("a",text=symbol)):
				print(symbol)
				financials = requests.get(detail_mod).text
				bt = BeautifulSoup(financials,"lxml")
				
				with open("output_"+symbol+".html", "w") as file:
					file.write(str(bt))
			
		
marketwire()			

	
	
