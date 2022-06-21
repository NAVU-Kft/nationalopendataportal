import ckantoolkit as tk
import ckan.lib.helpers as helpers
from ckanext.hutemplate.model.blog_types import blog_t, get_blog_type_record
from ckanext.hutemplate.model.page_types import page_t

class FilteredBlogController:
    def getRoutes(self):
        return [
            (u'/news', u'news', self.news),
            (u'/news_admin/categories', u'newscategory_index', self.newscategory_index),
            (u'/news_admin/category/<category_name_or_id>', u'newscategory_show', self.newscategory_show),
            (u'/news/all', u'news_all', self.news_all),
            (u'/news/<page>', u'news_show', self.news_show),
            (u'/news/category/<category_name_or_id>', u'news_category', self.news_category)
        ]

    def news(self):
        return tk.render('hutemplate/news-cms.html')
        #return tk.render('hutemplate/news.html')

    def newscategory_index(self):
        return tk.render('ckanext_pages/newscategory_index.html')

    def newscategory_show(self, category_name_or_id):
        record = get_blog_type_record(category_name_or_id)
        
        if record is None:
            return self.newscategory_index()

        category_id = record['key']
        self.filter_blog_pages(category_id)
        tk.c.category = record
        
        return tk.render('ckanext_pages/newscategory_show.html')

    def news_all(self):
        self.filter_blog_pages(u'Hírek')
        return tk.render('ckanext_pages/news_all.html')

    def news_category(self, category_name_or_id):
        record = get_blog_type_record(category_name_or_id)
        if record is None:
            return self.news_all()

        category_id = record['key']
        self.filter_blog_pages(category_id)
        tk.c.category = record

        return tk.render('ckanext_pages/news_category.html')

    def news_show(self, page):
        tk.c.page_type = 'blog'
        if page.startswith('/'):
            page = page[1:]
        if not page:
            return self.news_all()
        _page = tk.get_action('ckanext_pages_show')(
            data_dict={'org_id': None,
                    'page': page}
        )
        if _page is None:
            return self.news_all()
        tk.c.page = _page
        
        return tk.render('ckanext_pages/news_show.html')

    def filter_blog_pages(self, category):
        data_dict = {'org_id': None, 'page_type': 'blog'}
        data_dict['order_publish_date'] = True
        
        blog_list = tk.get_action('ckanext_pages_list')(
            data_dict=data_dict
        )
        
        tk.c.pages_dict = []
        for blog in blog_list:
            if category and blog['blog_type'] != category:
                continue
            tk.c.pages_dict.append(blog)

        tk.c.page = helpers.Page(
            collection=tk.c.pages_dict,
            page=tk.request.params.get('page', 1),
            url=helpers.pager_url,
            items_per_page=21
        )