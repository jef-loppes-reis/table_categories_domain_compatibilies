from ecomm import Postgres
from pandas import DataFrame


with Postgres() as db:
    with open('./data/sql/query.sql', 'r', encoding='utf-8') as fp_query:
        with open('./data/exceptions.txt', 'r', encoding='utf-8') as fp_exceptions:
            exceptions: tuple[str] = tuple(set(fp_exceptions.read().split('\n')))
        df: DataFrame = db.query(fp_query.read() % str(exceptions))

df.to_excel('categories_domain_compatibilities.xlsx')
