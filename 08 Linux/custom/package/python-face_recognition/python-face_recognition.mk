################################################################################
#
# python-face_recognition
#
################################################################################

PYTHON_FACE_RECOGNITION_VERSION = 1.2.2
PYTHON_FACE_RECOGNITION_SOURCE = face_recognition-$(PYTHON_FACE_RECOGNITION_VERSION).tar.gz
PYTHON_FACE_RECOGNITION_SITE = https://files.pythonhosted.org/packages/e1/da/b607fc6c80eb8e82487b1cb3cff445450d712eb0456f562790c7a761f781
PYTHON_FACE_RECOGNITION_SETUP_TYPE = setuptools
PYTHON_FACE_RECOGNITION_LICENSE = MIT
PYTHON_FACE_RECOGNITION_LICENSE_FILES = LICENSE

$(eval $(python-package))
