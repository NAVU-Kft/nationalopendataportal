from ckan.lib.base import render

class StaticHutemplateController:
    def getRoutes(self):
        return [
            (u'/datarequest', u'datarequest', self.datarequest),
            (u'/knowledgebase', u'knowledgebase', self.knowledgebase),
            (u'/completedanalyzes', u'completedanalyzes', self.completedanalyzes),
            (u'/contact', u'contact', self.contact),
            (u'/faq', u'faq', self.faq),
            (u'/disclaimers', u'disclaimers', self.disclaimers),
            (u'/privacypolicy', u'privacypolicy', self.privacypolicy),
            (u'/imprint', u'imprint', self.imprint),
            (u'/purpose', u'purpose', self.purpose)
            
        ]

    def datarequest(self):
        return render('hutemplate/datarequest.html', extra_vars={})

    def knowledgebase(self):
        return render('hutemplate/knowledgebase.html', extra_vars={})

    def completedanalyzes(self):
        return render('hutemplate/completedanalyzes.html', extra_vars={})

    def contact(self):
        return render('hutemplate/contact.html', extra_vars={})

    def faq(self):
        return render('hutemplate/faq.html', extra_vars={})

    def disclaimers(self):
        return render('hutemplate/disclaimers.html', extra_vars={})

    def privacypolicy(self):
        return render('hutemplate/privacypolicy.html', extra_vars={})
    
    def imprint(self):
        return render('hutemplate/imprint.html', extra_vars={})

    def purpose(self):
        return render('hutemplate/purpose.html', extra_vars={})


