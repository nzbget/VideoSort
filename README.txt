# VideoSort post-processing script for NZBGet.
#
# Copyright (C) 2013-2020 Andrey Prygunkov <hugbug@users.sourceforge.net>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with subliminal.  If not, see <http://www.gnu.org/licenses/>.
#

# Sort movies and tv shows.
#
# This is a script for downloaded TV shows and movies. It uses scene-standard
# naming conventions to match TV shows and movies and rename/move/sort/organize
# them as you like.
#
# The script relies on python library "guessit" (http://guessit.readthedocs.org)
# to extract information from file names and includes portions of code from
# "SABnzbd+" (http://sabnzbd.org).
#
# Info about pp-script:
# Author: Andrey Prygunkov (nzbget@gmail.com).
# Web-site: https://github.com/nzbget/VideoSort.
# PP-Script Version: see <VideoSort.py>.
