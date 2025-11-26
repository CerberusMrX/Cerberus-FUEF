from setuptools import setup, find_packages

setup(
    name="cerberus-fuef",
    version="1.0.0",
    description="Cerberus File Upload Exploitation Framework",
    author="Sudeepa Wanigarathna",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4",
        "rich",
        "urllib3"
    ],
    entry_points={
        "console_scripts": [
            "cerberus-fuef=cerberus_fuef.main:main",
        ],
    },
    python_requires=">=3.10",
)
