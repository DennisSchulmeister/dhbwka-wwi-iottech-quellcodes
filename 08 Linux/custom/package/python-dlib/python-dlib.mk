################################################################################
#
# python-dlib
#
################################################################################

PYTHON_DLIB_VERSION = 19.14
PYTHON_DLIB_SOURCE = dlib-$(PYTHON_DLIB_VERSION).tar.bz2
PYTHON_DLIB_SITE = https://sourceforge.net/projects/dclib/files/dlib/v$(PYTHON_DLIB_VERSION)
PYTHON_DLIB_LICENSE = BSL-1.0
PYTHON_DLIB_LICENSE_FILES = dlib/LICENSE.txt
PYTHON_DLIB_SUBDIR = tools/python
PYTHON_DLIB_INSTALL_STAGING = YES

PYTHON_DLIB_DEPENDENCIES += python3 giflib libjpeg libpng sqlite

# Don't use host-python to compile the bindings
PYTHON_DLIB_CONF_OPTS += -DPYTHON_INCLUDE_DIR=$(TARGET_DIR)/usr/include/python$(PYTHON3_VERSION_MAJOR)m
PYTHON_DLIB_CONF_OPTS += -DPYTHON_EXECUTABLE=$(TARGET_DIR)/usr/bin/python$(PYTHON3_VERSION_MAJOR)
PYTHON_DLIB_CONF_OPTS += -DPYTHON_LIBRARY=$(TARGET_DIR)/usr/lib/python$(PYTHON3_VERSION_MAJOR)

## Bypass python detection completely, as it still searches in
## /lib on the host for ld-linux-ARCH.so.3
#PYTHON_DLIB_CONF_OPTS += -DPYTHONLIBS_FOUND=TRUE
#PYTHON_DLIB_CONF_OPTS += -DPYTHON_MODULE_EXTENSION=.so
#
## Find Python.h when #included in the source

define PYTHON_DLIB_POST_INSTALL_TARGET_REMOVE_HEADERS
	rm -r $(TARGET_DIR)/usr/include/dlib
	rm -r $(TARGET_DIR)/usr/lib/cmake/dlib
endef

PYTHON_DLIB_POST_INSTALL_TARGET_HOOKS += PYTHON_DLIB_POST_INSTALL_TARGET_REMOVE_HEADERS

# gui support
ifndef BR2_PACKAGE_PYTHON_DLIB_GUI_SUPPORT
  PYTHON_DLIB_CONF_OPTS += -DDLIB_NO_GUI_SUPPORT_STR=ON
endif

$(eval $(cmake-package))
