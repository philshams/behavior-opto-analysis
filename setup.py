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
            "process = opto_analysis.__process_data__:process_data",
            "analyze = opto_analysis.__analyze_data__:analyze_data",
            "track = opto_analysis.__track_data__:track_data"
        ]
    }

)