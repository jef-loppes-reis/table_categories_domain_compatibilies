from time import sleep

from httpx import Client, Response, ReadTimeout, ReadError
from ecomm import MLInterface
from rich.progress import Progress
from rich import print as rprint
from pandas import DataFrame, json_normalize, concat


class CategoriesDomain:

    def __init__(self) -> None:
        self.__base_url: str = 'https://api.mercadolibre.com'
        self.__endpoint: str = '/catalog/dumps/domains/MLB/compatibilities'

    def get_categories_domain(self) -> Response:
        with Client() as client:
            __num_tentativas: int = 0
            while True:
                if __num_tentativas > 10:
                    raise ValueError('Numero de tentativas exedido !')
                try:
                    __res: Response = client.get(
                        url=self.__base_url + self.__endpoint
                    )
                    return __res
                except ReadTimeout:
                    sleep(10)
                    continue
                except ReadError:
                    sleep(10)
                    continue

    def main(self):
        __categories: list[dict] = self.get_categories_domain().json()

        table: DataFrame = DataFrame()
        with Progress() as progress:
            task = progress.add_task(
                description='[green]Criando tabela...:',
                total=len(__categories)
            )
            for x in __categories:
                cat_domain: dict = x
                table_temp: DataFrame = json_normalize(cat_domain)
                table_temp['categories_id'] = cat_domain.get(
                    'compatibilities')[0].get('categories')[0].get('id')
                table_temp['compat_required'] = cat_domain.get(
                    'compatibilities')[0].get('categories')[0].get('required')
                table: DataFrame = concat([table, table_temp])
                # Atualiza a barra de progresso
                progress.update(task, advance=len(__categories))

        table: DataFrame = table.reset_index(drop=True).copy()
        return table

if __name__ == '__main__':
    cats_domain: CategoriesDomain = CategoriesDomain()
    df = cats_domain.main()
