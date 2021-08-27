import math
from typing import List

import requests
from dataclasses import dataclass

BASE_URL = 'https://huggingface.co/models-json'
_PAGE_SIZE = 30


@dataclass
class DownloadableModel:
    model_name: str
    task: str
    downloads: int


class DownloadableModels:
    @staticmethod
    def download_model_page(page_i: int) -> List[DownloadableModel]:
        params = f'?sort=downloads&p={page_i}'
        response = requests.get(BASE_URL + params)
        return [
            DownloadableModel(model['model']['modelId'], model['model']['pipeline_tag'], model['model']['downloads'])
            for model in response.json()['modelsWithAuthorObj']
        ]

    @classmethod
    def download_top_k_models(cls, k: int) -> "DownloadableModels":
        models = []
        for i in range(math.ceil(k / _PAGE_SIZE)):
            models += cls.download_model_page(i)

        return cls(models)

    def __init__(self, models: List[DownloadableModel]):
        self.models = models
