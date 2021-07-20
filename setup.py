import setuptools

setuptools.setup(
    name='opto-analysis',
    version='1.2',
    author='Philip Shamash',
    license='GNU General Public License',
    packages = ['opto_analysis'],
    package_dir={'opto_analysis': 'opto_analysis'},
    entry_points={
        "console_scripts": [
            "process = opto_analysis.run:process",
            "analyze = opto_analysis.run:analyze",
            "track = opto_analysis.run:track",
            "visualize = opto_analysis.run:visualize"       
        ]
    }

)