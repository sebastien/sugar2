# encoding: utf-8
# SEE: https://packaging.python.org/en/latest/distributing.html#id23
# SEE: https://pythonhosted.org/setuptools/setuptools.html
# --
# Create source distribution: python setup.py sdist
# Upload using twine: twine upload dist/*
# Upload using setup.py: setup.py sdist bdist_wheel upload
from distutils.core import setup

setup(
	name             = "sugar2",
	version          = "0.9.1",
	url              = "https://github.com/sebastien/sugar2",
	author           = 'Sébastien Pierre',
	author_email     = 'sebastien.pierre@gmail.com',
	license          = 'BSD',
	description      = "The Sugar programming language",
	keywords         = "programming language transpiler JavaScript",
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
	],
	package_dir = {"":"dist"},
	packages    = ["sugar2", "sugar2.grammar"],
	install_requires=["libparsing>=0.8.2","lambdafactory>=0.8.0"],
)

# EOF

