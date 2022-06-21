from .StaticHutemplateController import StaticHutemplateController
from .FilteredBlogController import FilteredBlogController
from .ExcelController import ExcelController


def registerRoutes(blueprint):
    # Add plugin url rules to Blueprint object
    rules = []

    rules += StaticHutemplateController().getRoutes()
    rules += FilteredBlogController().getRoutes()
    rules += ExcelController().getRoutes()

    for rule in rules:
        blueprint.add_url_rule(*rule)