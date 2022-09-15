#!/usr/bin/python3
import logging
import wget
import PyPDF2
import requests
from os.path import exists

_LOGGER = logging.getLogger(__name__)
url = "https://files.boltenergie.be/pricelists/var/" 


@pyscript_compile
def download_file(args): 
    if not exists(args[1]):
        try:
            response = wget.download(args[0], args[1])
        except Exception as e: 
            _LOGGER.error(e)

    pdffileobj=open(args[1],'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    pageobj=pdfreader.getPage(0)
    return pageobj.extractText()    



@service
def get_bolt_data(entity_id,subscription,residential,utility):

    pdffile = ""
    url = "https://files.boltenergie.be/pricelists/var/"  
    stop = True
    pdfNumber = 3
    text = ""

    if utility == "electricity":
        utility = "el"
    elif utility == "gas":
        utility = "ng"
    else:
        _LOGGER.error("no correct utility value")


    url = url + subscription + "_" + residential + "_" + utility + "_nl_"

    while stop:
        test_url = url + str(pdfNumber) + ".pdf"
        r = task.executor(requests.get, test_url)

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


    if utility == "el":
        head, sep, tail = text.partition('maandAbonnementskostincl. BTW c€')
    elif utility == "ng":
        head, sep, tail = text.partition('incl. BTWEnergiekostEnkelvoudigc €') 
    else:
        _LOGGER.error("error utility keuze")

    price,s,t=tail.partition('/kWh')
    price= price.replace(" ", "")
    price = float(price.replace(',', '.'))

    if utility == "ng":
        price = price/10.26
    
    
    domain, sep, tail = entity_id.partition('.')

    service.call(domain, "set_value", entity_id=entity_id, value=price)
