from dataclasses import dataclass
from typing import List
from typing import Optional

import requests

HUGGINGFACE_BASE_URL = 'https://huggingface.co/'
_PAGE_SIZE = 30


@dataclass
class DownloadableModel:
    model_name: str
    downloads: int
    author: Optional[str]


class DownloadableModelsState:
    @staticmethod
    def download_model_page(
            page_i: Optional[int] = None,
            search: Optional[str] = None,
            other: Optional[str] = None,
    ) -> List[DownloadableModel]:
        def_params = 'models-json?sort=downloads&library=pytorch'
        if page_i is not None:
            def_params += f"&p={page_i}"
        if search:
            def_params += f"&search={search}"
        if other is not None:
            def_params += f"&other={other}"

        response = requests.get(HUGGINGFACE_BASE_URL + def_params)
        return [
            DownloadableModel(
                model_name=model['model']['modelId'],
                # task=model['model'].get('pipeline_tag', None),
                downloads=model['model']['downloads'],
                author=model['model'].get('author', None)
            )
            for model in response.json()['modelsWithAuthorObj']
        ]

    def __init__(self, models: List[DownloadableModel]):
        self.models = models
