################################################################################
#
# libdlib
#
################################################################################

LIBDLIB_VERSION = 19.14
LIBDLIB_SOURCE = dlib-$(LIBDLIB_VERSION).tar.bz2
LIBDLIB_SITE = https://sourceforge.net/projects/dclib/files/dlib/v$(LIBDLIB_VERSION)
LIBDLIB_LICENSE = BSL-1.0
LIBDLIB_LICENSE_FILES = dlib/LICENSE.txt
LIBDLIB_INSTALL_STAGING = YES
LIBDLIB_DEPENDENCIES = giflib libjpeg libpng sqlite

define LIBDLIB_POST_INSTALL_TARGET_REMOVE_HEADERS
	rm -r $(TARGET_DIR)/usr/include/dlib
	rm -r $(TARGET_DIR)/usr/lib/cmake/dlib
endef

LIBDLIB_POST_INSTALL_TARGET_HOOKS += LIBDLIB_POST_INSTALL_TARGET_REMOVE_HEADERS

# gui support
ifndef BR2_PACKAGE_LIBDLIB_GUI_SUPPORT
  LIBDLIB_CONF_OPTS = -DDLIB_NO_GUI_SUPPORT_STR=ON
endif

$(eval $(cmake-package))
