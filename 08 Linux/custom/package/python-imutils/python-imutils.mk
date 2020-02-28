################################################################################
#
# python-imutils
#
################################################################################

PYTHON_IMUTILS_VERSION = 0.4.6
PYTHON_IMUTILS_SOURCE = imutils-$(PYTHON_IMUTILS_VERSION).tar.gz
PYTHON_IMUTILS_SITE = https://files.pythonhosted.org/packages/15/ba/24272ac57159cf255959f9298b8e42f00528be90ce4ccd274b604ae5e32d
PYTHON_IMUTILS_SETUP_TYPE = distutils
PYTHON_IMUTILS_LICENSE = 

$(eval $(python-package))
