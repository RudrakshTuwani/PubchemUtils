def extract_id_type(soup):
	""" Takes a BS4 object of a puchem page as input and returns the Pubchem ID type and Pubchem ID Value """
    pubhcem_uid_type = soup.find_all('meta', {'name':'pubchem_uid_type'})[0]['content']
    pubhcem_uid_value = soup.find_all('meta', {'name':'pubchem_uid_value'})[0]['content']
    return pubhcem_uid_type +':'+ pubhcem_uid_value



def get_pubchem(cas):
	""" Extract the mappings to pubchem ids of a given CAS number """

	# Get the search page.
    url = 'https://www.ncbi.nlm.nih.gov/pccompound?term="{}"'.format(cas)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    # In case the search page redirects, extract pubchem id type and value.
    try: 
        return [extract_id_type(soup)]
    
    # Otherwise, get all the returned links and extract pubchem id type and value..
    except IndexError: 
        
        # If only exact results are returned.
        if (not 'Quoted phrase not found' in r.text) and (not 'Did you mean: ' in r.text):
            pubmed_results = [pr.find_all('p', {"class":"title"})[0] for pr in soup.find_all('div', {"class":"rprt"})]
            links = [pr.find_all('a')[0]['href'] for pr in pubmed_results]
            pubchem_ids = list()
            for link in links:
                r = requests.get(link)
                soup = BeautifulSoup(r.text, "lxml")
                pubchem_ids.append(extract_id_type(soup))
            return pubchem_ids
        # No results found.
        else:
            return []
