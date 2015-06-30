#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import ndb
import os
import cgi
import urllib
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname ('base.html'), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), extensions=['jinja2.ext.autoescape'], autoescape= True)



    

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))




#Creating modify page object by defining class. 
class ModifyPage(ndb.Model):
    #name=ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
  
    def get(self):
            
           
            comment=self.request.get_all("comment")
      

            #added this for triggering error
            error=self.request.get('error'," ")


            #Creating a key 
            commentbook_key = ndb.Key('MainPage', 'modify_page')

            #instantiates modify page object
            modify_page = ModifyPage(comment='')
            modify_query = ModifyPage.query(ancestor=commentbook_key).order(-ModifyPage.date)
           

            query=ModifyPage.query().order(ModifyPage.date)
            info_list = query.fetch()
            
            
            
            self.render("index-Stage4.html", comment=info_list, error=error)

        

        
    def post(self):

        #writes object to Google Datastore server

        #pull a reference object to ModifyPage object to pull the objects from Google Datastore. Queries all objects in database.Use fetch
        #to limit query to specified number.
        pull_posts=5
        query=ModifyPage.query()
        page_comments = query.fetch(pull_posts)

    

        comment=self.request.get('comment')     
                
            
        if comment:
                    modify_page = ModifyPage(comment=comment)
                    modify_page.content=self.request.get('comment')
                    modify_page.put()
                    import time
                    time.sleep(.1)
                    self.redirect('/')


        
        else:
                    self.redirect('/?error=Please fill out comment section!')

    






    
app = webapp2.WSGIApplication ([('/', MainPage), ],debug=True)
