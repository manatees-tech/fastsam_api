from setuptools import setup

REQUIREMENTS = [
    i.strip() for i in open("requirements-fastsam.txt").readlines()
]

setup(
    name="fastsam",
    version="0.1.1",
    install_requires=REQUIREMENTS,
    packages=["fastsam", "fastsam_tools", "ultralytics"],
    package_dir={
        "fastsam": "fastsam",
        "fastsam_tools": "utils",
        "ultralytics": "ultralytics"
    },
    url="https://github.com/manatees-tech/fastsam_api"
)
