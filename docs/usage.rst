========
Usage
========

To use Payzone Python package in a project::

	import payzone
	client = payzone.PayZoneClient("username", "password") # Please get in touch with www.payzone.ma if you don't have the necessary credentials
	response = client.transaction.prepare(**{
		'customerIP': "41.41.41.41",
		'orderID': 666,
		'amount': 15000, # 150 DH
		'shippingType': "Virtual",
		'paymentType': "CreditCard",
		'ctrlRedirectURL': "https://www.my_website.com/mycallback_uri"
	})
	

``response`` will be a dict containing the following elements : 

* ``customerToken`` 
* ``code``
* ``message``
* ``merchantToken``
	
	
1. You might want to store this information in a database.
2. Right after you should redirect the user to the following url::

	url = client.transaction.get_dopay_url(response['customerToken'])
	
	
---------------
 Transaction status
---------------

In order to check a transaction status you should do the following::

	client.transaction.status(merchant_token)
	# the client being a PayZone instance
