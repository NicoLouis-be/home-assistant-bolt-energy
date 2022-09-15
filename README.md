# home-assistant-bolt-energy

pyscript to automatic import the new variable tariff of "bolt energy"

prices are fetched from the online pdf file that bolt updates every month or quarter

https://www.boltenergie.be/nl/prijslijsten?gclid=CjwKCAjwvNaYBhA3EiwACgndgrxjotwoQZP0Ti93cKBVp68rRXoiFu2fvaXd7ikpT66PRsJXak7uDBoCUwIQAvD_BwE 

First install pyscript through hacs

I manual updated the configuration.yaml file
<pre><code>
pyscript:
  allow_all_imports: true
  hass_is_global: true
</pre></code>
  
dowload both files (requirement.txt and utilityprice.py) and place them in the "pyscript" folder under home assistant

create an automation to get the data periodically
<pre><code>
  service: pyscript.get_bolt_data
  data:
    entity_id: input_number.gas_rate
    subscription: bolt
    residential: res
    utility: gas
</code></pre>
    
</blockquote>
  
settings are:
 <ul>
  <li>entity_id: the entity where the value needs to be written to, i use input_number but can also be a sensor</li>
  <li>subscription: the contract you have "bolt" "online" or "go"</li>
  <li>residential: can be res (residential) or pro (profecional)</li>
  <li>utility: gas or electricity</li>
</ul>
    
# TODO
  variable for choosing which meter you have:
  <ul>
    <li>day</li>
    <li>day/night</li>
    <li>excl. night</li>
  </ul>
