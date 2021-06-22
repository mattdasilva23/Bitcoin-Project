
# from doing the research, found that requests paired with json is the easiest way to deal with json content - could use urllib etc
import requests, json, html, time, threading, os
from prettytable import PrettyTable as pt

# function to return the value of a given currency
# e.g. if param 'c' is USD, searches the json content/dictionary for USD and returns that value
# the html.unescape converts the html entities within the json data to symbols, e.g. "&#36;" is the code for "$"
def getBTCPrice(c, d):
	return html.unescape(d["bpi"][c]["symbol"]) + str(format(round(d["bpi"][c]["rate_float"], 3), '.3f'))

# quit program
def quitProgram():
	print("Quitting Program...")
	os._exit(0) 

# print prices
def printPrices():

	t = threading.Timer(interval, printPrices)	# recursive call
	t.start()

	# firstly you want to retrieve the data from the url, then parse as json
	r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
	content = r.json()

	# the "content" variable is a dictionary, so we can index by using content["x"], e.g. for the time we use ["time"]["updateduk"] 
	# myTime = content["time"]["updateduk"]

	# concise way of getting currencies without copy and paste
	# this just so happens to work due to the way the json file is loaded, would be different in other situations
	currencies = ["USD", "GBP", "EUR"]			# add or remove fields here to determine what prices to print
	prices = {}
	for curr in currencies:
		prices["Bitcoin Price " + curr] = getBTCPrice(curr, content)

	# PrettyTable is used to print all values nicely (vertically)
	t = pt(["Currency", "Value"])				# create table with field values
	t.title = "Bitcoin Table"					# name of the table (will be at the top)
	# t.add_row(["Time Requested", myTime])		# add row - time requested (optional)
	for k, v in prices.items():
		t.add_row([k, v])						# add row - Bitcoin price, based on the amount of values in 'currencies' dictionary
	print(t)

# start of program
print("Bitcoin Interval Printer")
duration = int(input("Duration? (secs) "))
interval = int(input("Interval? (secs) "))
print("Running for " + str(duration) + " seconds\nWith an interval of " + str(interval) + " seconds")

stopProgram = threading.Timer(duration, quitProgram)
stopProgram.start()									# start timer countdown until program will exit
printPrices()										# call printPrices immediately (0 seconds), then do interval timer
# threading.Timer(interval, printPrices).start()	# call printPrices with a delay initially, then continue with interval timer normally

# ------------------------------------

# old way of printing table (horizontally)
# t2 = pt(["Bitcoin Price USD", "Bitcoin Price GBP", "Bitcoin Price EUR"])									# headers of the table
# t2.add_row([prices["Bitcoin Price USD"], prices["Bitcoin Price GBP"], prices["Bitcoin Price EUR"]])		# values
# print(t2)

# old code for reference
# btcUSD = html.unescape(content["bpi"]["USD"]["symbol"]) + str(round(content["bpi"]["USD"]["rate_float"], 2))	# technically could just type "$" for USD, but better coding practice to use data
# btcGBP = html.unescape(content["bpi"]["GBP"]["symbol"]) + str(round(content["bpi"]["GBP"]["rate_float"], 2))
# btcEUR = html.unescape(content["bpi"]["EUR"]["symbol"]) + str(round(content["bpi"]["EUR"]["rate_float"], 2))

# helpful resources
# https://www.json.org/json-en.html
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content
# https://www.educative.io/edpresso/what-is-the-difference-between-jsonloads-and-jsondumps
# https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds