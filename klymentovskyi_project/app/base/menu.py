from flask import url_for
from . import base_blueprint

__menu__ = []
__separator__ = "__separator__"

class MenuItem:
    def __init__(self, name: str, endpoint: str, visibility_lambda = None) -> None:
        self.name = name
        self.endpoint = endpoint
        self.visibility_lambda = visibility_lambda

    @property
    def url(self):
        return url_for(self.endpoint)

    @property
    def visible(self):
        return not self.visibility_lambda or self.visibility_lambda()

def separator():
    return __separator__

@base_blueprint.app_context_processor
def inject_menu():
    return dict(menu=__menu__.__iter__(), menu_separator=__separator__)

def add_items(*items: list):
    __menu__.extend(items)

def add_separator():
    __menu__.append(__separator__)
