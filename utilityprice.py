#!/usr/bin/python3
import logging
import wget
import PyPDF2
import requests
from os.path import exists

_LOGGER = logging.getLogger(__name__)

# @pyscript_compile: run this function without pyscript restrictions
@pyscript_compile
def download_file(args):
    """
    function download the file from the given URL
    return extracted text in the pdf 
    variable:
        args 0: url
        args 1: file name
    """ 
    url = args[0]
    file = args[1]

    # check if file already exist
    # if yes -> don't download again
    if not exists(file):
        try:
            response = wget.download(url, file)
        except Exception as e: 
            _LOGGER.error(e)

    # open and extract text
    pdffileobj=open(file,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    pageobj=pdfreader.getPage(0)
    return pageobj.extractText()    


# @service: run this as a service to call it in an automation
@service
def get_bolt_data(entity_id,subscription,residential,utility):

    url = "https://files.boltenergie.be/pricelists/var/" 
    text = ""
    pdffile = "" 
    stop = True
    pdfNumber = 3   # 1 and 2 didn't exist so start from 3

    if utility == "electricity":
        utility = "el"
    elif utility == "gas":
        utility = "ng"
    else:
        _LOGGER.error("no correct utility value")


    url = url + subscription + "_" + residential + "_" + utility + "_nl_"

    # run untill 404 code
    while stop:
        test_url = url + str(pdfNumber) + ".pdf"
        r = task.executor(requests.get, test_url)

        # if 404 code then take previous number and create link+filename
        if r.status_code == 404:
            pdfNumber -= 1
              
            if utility == "el":
                pdffile = "elek_" + str(pdfNumber) + ".pdf"
            elif utility == "ng":
                pdffile = "gas_" + str(pdfNumber) + ".pdf"

            data = [url + str(pdfNumber) + ".pdf", pdffile]
            text = task.executor(download_file, data)

            stop = False
            break
        else:
            pdfNumber += 1    


    # split the text up 
    # head text before number
    # sep text itself where we did the search on
    # tail: the number and all text behind (this is what we need)
    if utility == "el":
        head, sep, tail = text.partition('maandAbonnementskostincl. BTW c€')
    elif utility == "ng":
        head, sep, tail = text.partition('incl. BTWEnergiekostEnkelvoudigc €') 
    else:
        _LOGGER.error("error utility keuze")

    # split the text up 
    # head the number (this is what we need)
    # sep text itself where we did the search on
    # tail: all text behind
    price,s,t=tail.partition('/kWh')

    # delete spaces
    price= price.replace(" ", "")

    # change , to .
    price = float(price.replace(',', '.'))

    # if gas convert kwh to m³
    if utility == "ng":
        price = price/10.26
    
    # get the domain of the given entity
    domain, sep, tail = entity_id.partition('.')

    # change the value if the entity
    service.call(domain, "set_value", entity_id=entity_id, value=price)
