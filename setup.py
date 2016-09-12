from setuptools import setup, find_packages


version = __import__('presence').__version__

setup(
  name = 'django-presence',
  packages=find_packages(),
  include_package_data=True,
  version = version,
  description = 'User presence widget for Django using Centrifugo',
  author = 'synw',
  author_email = 'synwe@yahoo.com',
  url = 'https://github.com/synw/django-presence', 
  download_url = 'https://github.com/synw/django-presence/releases/tag/'+version,
  keywords = ['django', 'websockets'], 
  classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
  install_requires=[
        'django-instant',
    ],
  zip_safe=False
)
