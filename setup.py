import os
from setuptools import setup, find_packages


def get_requirements():
    """
    必要なパッケージをrequirements.txtから取得する
    """
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8") as file:
        return file.read().splitlines()


setup(
    name="pyrmj",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "pyrmj": ["data/GL-MahjongTile.base64"],
    },
    install_requires=get_requirements(),
)
