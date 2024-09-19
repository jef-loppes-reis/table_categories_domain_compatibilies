from ecomm import Postgres
from pandas import DataFrame

from categories_domain import CategoriesDomain


cats_domain: CategoriesDomain = CategoriesDomain()
df_categories: DataFrame = cats_domain.main()
df_categories.loc[:, 'compatibilities'] = df_categories.loc[
    :, 'compatibilities'].apply(str)

with Postgres() as db:
    db.insert(
        df=df_categories.astype(
            {
            'domain_id': 'str',
            'main': 'bool',
            'compatibilities': 'str',
            'categories_id': 'str',
            'compat_required': 'bool'
        }
        ),
        table='ml_cat_compatibilities'
    )
