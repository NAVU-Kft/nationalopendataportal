import ckan.plugins.toolkit as toolkit

class ExcelController:
    def getRoutes(self):
        return [
            (u'/excelExport', u'excelExport', self.excelExport)            
        ]

    def excelExport(self):
        response = toolkit.get_action('hutemplate_export_excel')({}, {})
        return response