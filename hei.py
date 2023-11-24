class chi:
   def __init__(self):
      self._data = {}
      self._headers = {}
      self.headers(user_agent="hei/chi/ti/pi")
      self._json = {}
      self._args = {}
      self._method = None
      self._url = None
        
   def args(self, **kwargs):
      self._args = {
         name.replace("_", " "): value
         for name, value in kwargs.items()
      }
      return self

   def cookies(self, **kwargs):
      self.headers(cookie = "; ".join(
         f"{name}={value}" for name, value in kwargs.items())
      )
      return self

   def data(self, **kwargs):
      self._json.clear()
      self._data = { 
         name.replace("_", " "): value for name, value in kwargs.items() 
      }
      return self

   def get(self): 
      self._method = "GET"
      return self

   def head(self): 
      self._method = "HEAD"
      return self

   def headers(self, **kwargs):
      self._headers.update({
         name.replace("_", "-").title(): value for name, value in kwargs.items()
      })
      return self
 
   def json(self, **kwargs):
      self._data.clear()
      self._json = { 
         name.replace("_", " "): value for name, value in kwargs.items() 
      }
      return self.headers(content_type="application/json")
    
   def post(self): 
      self._method = "POST"
      return self

   def put(self): 
      self._method = "PUT"
      return self

   def send(self):
      if self._method in {"PUT", "POST"}:
         query = __import__("urllib.parse", fromlist=[""]).urlencode(self._args)
         self._url = f"""{self._url.rstrip("?")}?{query}"""
         self._args.clear()
        
      return __import__("urllib3").request(
         self._method,
         self._url,
         fields=self._data if self._method in {"PUT", "POST"} else self._args,
         headers=self._headers,
         json=self._json or None,
      )
    
   def url(self, url): 
      self._url = url
      return self
 
   def __repr__(self):
      return __import__("json").dumps(
         dict(
            url=self._url,
            method=self._method,
            headers=self._headers,
            args=self._args,
            data=self._data,
            json=self._json,
         ), 
         indent=3
      )
