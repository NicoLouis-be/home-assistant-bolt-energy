# home-assistant-bolt-energy
pyscript to automatic import the variable new tariff of bolt energy
prices are fetched from the online pdf file that bolt updates every month or quarter
https://www.boltenergie.be/nl/prijslijsten?gclid=CjwKCAjwvNaYBhA3EiwACgndgrxjotwoQZP0Ti93cKBVp68rRXoiFu2fvaXd7ikpT66PRsJXak7uDBoCUwIQAvD_BwE 

First install pyscript through hacs

I manual updated the configuration.yaml file
pyscript:
  allow_all_imports: true
  hass_is_global: true
  
dowload both files (requirement.txt and utilityprice.py) and place them in the "pyscript" folder under home assistant

create an automation to get the data periodically
  service: pyscript.get_bolt_data
  data:
    entity_id: input_number.gas_rate
    subscription: bolt
    residential: res
    utility: gas
  
  
  settings are:
    entity_id: the entity where the value needs to be written to, i use input_number but can also be a sensor
    subscription: the contract you have "bolt" "online" or "go"
    residential: can be res (residential) or pro (profecional)
    utility: gas or electricity
    
