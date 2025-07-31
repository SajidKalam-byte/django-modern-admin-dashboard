from setuptools import setup, find_packages

# Read version from the package
def get_version():
    with open('dashboard/_version.py', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return '0.1.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-modern-admin-dashboard',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12.0',
    ],
    extras_require={
        'dev': [
            'pytest-django>=4.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'isort>=5.0.0',
        ],
    },
    description='A modern, responsive Django admin dashboard with widgets, charts, and REST API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='SajidKalam-byte',
    author_email='your-email@domain.com',  # Update with your email
    url='https://github.com/SajidKalam-byte/django-modern-admin-dashboard',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
)
