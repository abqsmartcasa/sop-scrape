from setuptools import setup

setup(
    name="sopscrape",
    version="1.0",
    description="utility to scrape SOP PDF",
    url="http://github.com/apdforward/sop-scrape",
    author="Russ Biggs",
    author_email="russbiggs@gmail.com",
    license="Apache 2.0",
    packages=["sopscrape"],
    install_requires=["pdfminer-six", "chardet"],
    zip_safe=False,
)
