################################################################################
#
# python-picamera
#
################################################################################

# Hack, der die Prüfung ausschaltet, ob das aktuelle System ein Pi ist,
# was unser Linux-Buildsystem natürlich nicht ist. :-) Funktioniert nur,
# weil diese Umgebungsvariable in der setup.py abgefragt wird.
READTHEDOCS = True
export READTHEDOCS

PYTHON_PICAMERA_VERSION = 1.13
PYTHON_PICAMERA_SOURCE = picamera-$(PYTHON_PICAMERA_VERSION).tar.gz
PYTHON_PICAMERA_SITE = https://files.pythonhosted.org/packages/79/c4/80afe871d82ab1d5c9d8f0c0258228a8a0ed96db07a78ef17e7fba12fda8
PYTHON_PICAMERA_SETUP_TYPE = setuptools
PYTHON_PICAMERA_LICENSE = BSD
PYTHON_PICAMERA_LICENSE_FILES = LICENSE.txt

$(eval $(python-package))
