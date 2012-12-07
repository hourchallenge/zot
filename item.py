class Item:
    def __init__(self, item_dict={}):
        self.__dict__ = item_dict
        
    def __repr__(self):
        return repr(self.__dict__)
        
    def match(self, **kwargs):
        if not 'keywords' in kwargs: kwargs['keywords'] = []
        fields_to_search = {'title': 'title',
                            'pub': 'publicationTitle',
                            }
        result = []
        match_score = 0
        for field, to_search in fields_to_search.items():
            if not hasattr(self, to_search): continue
            search_terms = kwargs['keywords']
            if field in kwargs: field += kwargs[field]
            
            text_to_search = getattr(self, to_search).lower()
            search_terms = [term.lower() for term in search_terms]
            for search_term in search_terms:
                match_score += text_to_search.count(search_term)
        
        return match_score
        
        
    def bibliography(self):
        pass
        
    def citation(self):
        pass
        
    def full_text(self):
        pass
