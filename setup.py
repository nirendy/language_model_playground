import setuptools

setuptools.setup(
    name="language_model_playground",
    version="0.1.0",
    author="nirendy",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
        'joblib',
        'tqdm',
        'sentencepiece',
        'transformers',
        'tokenizers',
        'pandas',
        'numpy',
        'matplotlib',
        'torch',
        'streamlit-tags',
        'sentencepiece'
    ],
)
