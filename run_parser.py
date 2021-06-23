from get_category_links import get_category_products_links
from get_links import get_links
from get_content import get_content


def run_parser():
    get_links()
    get_category_products_links()
    get_content()

if __name__ == "__main__":
    run_parser()