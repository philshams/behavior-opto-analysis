import setuptools

setuptools.setup(
    name='opto-analysis',
    version='1.1',
    author='Philip Shamash',
    license='GNU General Public License',
    packages = ['opto_analysis'],
    package_dir={'opto_analysis': 'opto_analysis'},
    entry_points={
        "console_scripts": [
            "opto = opto_analysis.__run__:run"
        ]
    }

)