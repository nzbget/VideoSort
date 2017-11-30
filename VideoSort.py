#!/usr/bin/env python
#
# VideoSort post-processing script for NZBGet.
#
# Copyright (C) 2013-2017 Andrey Prygunkov <hugbug@users.sourceforge.net>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the program.  If not, see <http://www.gnu.org/licenses/>.
#


##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                           ###

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
# Web-site: http://nzbget.net/VideoSort.
# License: GPLv3 (http://www.gnu.org/licenses/gpl.html).
# PP-Script Version: 8.0-testing.
#
# NOTE: This script requires Python 2.x to be installed on your system.

##############################################################################
### OPTIONS                                                                   ###

# Destination directory for movies.
#
# The option can be left empty to use global DestDir or CategoryX.DestDir
# as destination.
#MoviesDir=${DestDir}/movies

# Destination directory for seasoned TV shows.
#
# The option can be left empty to use global DestDir or CategoryX.DestDir
# as destination.
#SeriesDir=${DestDir}/series

# Destination directory for dated TV shows.
#
# The option can be left empty to use global DestDir or CategoryX.DestDir
# as destination.
#DatedDir=${DestDir}/tv

# Destination directory for other TV shows.
#
# The option can be left empty to use global DestDir or CategoryX.DestDir
# as destination.
#OtherTvDir=${DestDir}/tv

# List of TV categories.
#
# Comma separated list of categories for TV. VideoSort automatically
# distinguishes movies from series and dated TV shows. But it needs help
# to distinguish movies from other TV shows because they are named
# using same conventions. If a download has associated category listed in
# option <TvCategories>, VideoSort uses this information.
#
# Category names must match categories defined in NZBGet.
#TvCategories=tv

# File extensions for video files.
#
# Only files with these extensions are processed. Extensions must
# be separated with commas.
# Example=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso
#VideoExtensions=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso

# File extensions for satellite files.
#
# Move satellite files such as subtitles to the destination along with
# the files they are related to. Extensions must be separated with commas.
# Example=.srt,.nfo
#SatelliteExtensions=.srt,.sub

# Minimum video file size (Megabytes).
#
# Smaller files are ignored.
#MinSize=100

# Formatting rules for movies.
#
# Specifiers for movies:
# %t, %.t, %_t    - movie title with words separated with spaces, dots
#                   or underscores (case-adjusted);
# %tT, %t.T, %t_T - movie title (original letter case);
# %y              - year;
# %decade         - two-digits decade (90, 00, 10);
# %0decade        - four-digits decade (1990, 2000, 2010).
# %imdb           - IMDb ID;
# %cpimdb         - IMDb ID (formatted for CouchPotato);
#
# Common specifiers (for movies, series and dated tv shows):
# %dn              - original directory name (nzb-name);
# %^dn, %.dn, %_dn - directory name with words separated with spaces, dots
#                    or underscores (case-adjusted);
# %^dN, %.dN, %_dN - directory name with words separated with spaces, dots
#                    or underscores (original letter case);
# %fn              - original filename;
# %^fn, %.fn, %_fn - filename with words separated with spaces, dots
#                    or underscores (case-adjusted);
# %^fN, %.fN, %_fN - filename with words separated with spaces, dots
#                    or underscores (original letter case);
# %cat, %.cat, %_cat - category with words separated with spaces, dots
#                   or underscores (case-adjusted);
# %cAt, %.cAt, %_cAt - category (original letter case);
# %ext            - file extension;
# %Ext            - file extension (case-adjusted);
# %qf             - video format (HTDV, BluRay, WEB-DL);
# %qss            - screen size (720p, 1080i);
# %qvc            - video codec (x264);
# %qac            - audio codec (DTS);
# %qah            - audio channels (5.1);
# %qrg            - release group;
# {{text}}        - uppercase the text;
# {TEXT}          - lowercase the text.
#MoviesFormat=%t (%y)

# Formatting rules for seasoned TV shows.
#
# Specifiers:
# %sn, %s.n, %s_n - show name with words separated with spaces, dots
#                   or underscores (case-adjusted);
# %sN, %s.N, %s_N - show name (original letter case);
# %s              - season number (1, 2);
# %0s             - two-digits season number (01, 02);
# %e              - episode number (1, 2);
# %0e             - two-digits episode number (01, 02);
# %en, %e.n, %e_n - episode name (case-adjusted);
# %eN, %e.N, %e_N - episode name (original letter case);
# %y              - year;
# %decade         - two-digits decade (90, 00, 10);
# %0decade        - four-digits decade (1990, 2000, 2010).
#
# For a list of common specifiers see option <MoviesFormat>.
#SeriesFormat=%sn/Season %s/%sn - S%0sE%0e - %en

# Multiple Episodes (list, range).
#
# This option is used for seasoned TV shows when the video file includes multiple episodes. For example: the formatting
# string "S%0sE%0e", combined with "MultipleEpisode=list" and "EpisodeSeparator=E" will result in a file named
# "My.Show.S01E01E02E03". "MultipleEpisode=range" and "EpisodeSeparator=-E" will result in a file named
# "My.Show.S01E01-E03.mkv". The "range" option is useful to follow the TV episode naming conventions of popular media
# management software, such as Plex.
#
#MultipleEpisodes=range

# Separator for multi episodes.
#
# The option is used for seasoned TV shows when video file includes
# multiple episodes, e. g. "My.Show.S01E02-03.mkv". The option defines
# a character (or a string) which must be insterted between episode
# numbers. For example, if "EpisodeSeparator=E", the specifier "%0e"
# will expand to "02E03". Giving formatting string "%sN - S%0sE%0e" the
# resulting filename will be "My Show - S01E02E03.mkv".
#EpisodeSeparator=E

# Treat year following title as part of title (yes, no).
#
# For seasoned TV shows: if year in the file name goes directly after
# show name, it will be added to show name. This may be necessary for
# media players like XBMC, Boxee or Plex (or anyone using TheTVDB) to
# properly index TV show.
#SeriesYear=yes

# Formatting rules for dated TV shows.
#
# Specifiers:
# %sn, %s.n, %s_n - show name with words separated with spaces, dots
#                   or underscores (case-adjusted);
# %sN, %s.N, %s_N - show name (original letter case);
# %y              - year;
# %decade         - two-digits decade (90, 00, 10);
# %0decade        - four-digits decade (1990, 2000, 2010).
# %m              - month (1-12);
# %0m              - two-digits month (01-12);
# %d              - day (1-31);
# %0d              - two-digits day (01-31).
#
# For a list of common specifiers see option <MoviesFormat>.
#DatedFormat=%sn/%sn - %y-%0m-%0d

# Formatting rules for other TV shows.
#
# All specifiers are same as in option <MoviesFormat>.
#OtherTvFormat=%t

# List of words to keep in lower case.
#
# This option has effect on "case-adjusted"-specifiers.
#LowerWords=the,of,and,at,vs,a,an,but,nor,for,on,so,yet

# List of words to keep in upper case.
#
# This option has effect on "case-adjusted"-specifiers.
#UpperWords=III,II,IV

# Use information from Direct-NZB headers (yes, no).
#
# NZB-sites may provide extended information about videos,
# which is usually more confident than the information extracted
# from file names.
#DNZBHeaders=yes

# Use name of nzb-file instead of name of video file (yes, no).
#
# Good indexer nzb-sites do renaming and cleanup of nzb-file
# names making them a better choice to extract name information
# than the original video file names.
#
# NOTE: If download contains more than one video file suitable
# for renaming (having correct extension and bigger than <MinSize>)
# this option is ignored and the names of video files are always used.
#PreferNZBName=no

# Overwrite files at destination (yes, no).
#
# If not active the files are still moved into destination but
# unique suffixes are added at the end of file names, e.g. My.Show.(2).mkv.
#Overwrite=no

# Delete download directory after renaming (yes, no).
#
# If after successful sorting all remaining files in the download directory
# are smaller than "MinSize" the directory with all files is removed. If no
# files could be processed, the directory remains untouched.
#Cleanup=yes

# Preview mode (yes, no).
#
# When active no changes to file system are made but the destination
# file names are logged. Useful to test formating rules; to restart
# the script use "Post-Process-Again" on history tab in NZBGet web-interface.
#Preview=no

# Print more logging messages (yes, no).
#
# For debugging or if you need to report a bug.
#Verbose=no

### NZBGET POST-PROCESSING SCRIPT                                           ###
##############################################################################

import sys
from os.path import dirname
sys.path.insert(0, dirname(__file__) + '/lib')

import os
import traceback
import re
import shutil
import guessit
import difflib

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_NONE=95
POSTPROCESS_ERROR=94

# Check if the script is called from nzbget 11.0 or later
if not 'NZBOP_SCRIPTDIR' in os.environ:
    print('*** NZBGet post-processing script ***')
    print('This script is supposed to be called from nzbget (11.0 or later).')
    sys.exit(POSTPROCESS_ERROR)

# Check if directory still exist (for post-process again)
if not os.path.exists(os.environ['NZBPP_DIRECTORY']):
    print('[INFO] Destination directory %s doesn\'t exist, exiting' % os.environ['NZBPP_DIRECTORY'])
    sys.exit(POSTPROCESS_NONE)

# Check par and unpack status for errors
if os.environ['NZBPP_PARSTATUS'] == '1' or os.environ['NZBPP_PARSTATUS'] == '4' or os.environ['NZBPP_UNPACKSTATUS'] == '1':
    print('[WARNING] Download of "%s" has failed, exiting' % (os.environ['NZBPP_NZBNAME']))
    sys.exit(POSTPROCESS_NONE)

# Check if all required script config options are present in config file
required_options = ('NZBPO_MoviesDir', 'NZBPO_SeriesDir', 'NZBPO_DatedDir',
    'NZBPO_OtherTvDir', 'NZBPO_VideoExtensions', 'NZBPO_SatelliteExtensions', 'NZBPO_MinSize',
    'NZBPO_MoviesFormat', 'NZBPO_SeriesFormat', 'NZBPO_OtherTvFormat', 'NZBPO_DatedFormat',
    'NZBPO_EpisodeSeparator', 'NZBPO_Overwrite', 'NZBPO_Cleanup', 'NZBPO_LowerWords', 'NZBPO_UpperWords',
    'NZBPO_TvCategories', 'NZBPO_Preview', 'NZBPO_Verbose')
for optname in required_options:
    if (not optname.upper() in os.environ):
        print('[ERROR] Option %s is missing in configuration file. Please check script settings' % optname[6:])
        sys.exit(POSTPROCESS_ERROR)

# Init script config options
nzb_name=os.environ['NZBPP_NZBNAME']
download_dir=os.environ['NZBPP_DIRECTORY']
movies_format=os.environ['NZBPO_MOVIESFORMAT']
series_format=os.environ['NZBPO_SERIESFORMAT']
dated_format=os.environ['NZBPO_DATEDFORMAT']
othertv_format=os.environ['NZBPO_OTHERTVFORMAT']
multiple_episodes=os.environ['NZBPO_MULTIPLEEPISODES']
episode_separator=os.environ['NZBPO_EPISODESEPARATOR']
movies_dir=os.environ['NZBPO_MOVIESDIR']
series_dir=os.environ['NZBPO_SERIESDIR']
dated_dir=os.environ['NZBPO_DATEDDIR']
othertv_dir=os.environ['NZBPO_OTHERTVDIR']
video_extensions=os.environ['NZBPO_VIDEOEXTENSIONS'].replace(' ', '').lower().split(',')
satellite_extensions=os.environ['NZBPO_SATELLITEEXTENSIONS'].replace(' ', '').lower().split(',')
min_size=int(os.environ['NZBPO_MINSIZE'])
min_size <<= 20
overwrite=os.environ['NZBPO_OVERWRITE'] == 'yes'
cleanup=os.environ['NZBPO_CLEANUP'] == 'yes'
preview=os.environ['NZBPO_PREVIEW'] == 'yes'
verbose=os.environ['NZBPO_VERBOSE'] == 'yes'
satellites=len(satellite_extensions)>0
lower_words=os.environ['NZBPO_LOWERWORDS'].replace(' ', '').split(',')
upper_words=os.environ['NZBPO_UPPERWORDS'].replace(' ', '').split(',')
series_year=os.environ.get('NZBPO_SERIESYEAR', 'yes') == 'yes'

tv_categories=os.environ['NZBPO_TVCATEGORIES'].lower().split(',')
category=os.environ.get('NZBPP_CATEGORY', '')
force_tv=category.lower() in tv_categories

dnzb_headers=os.environ.get('NZBPO_DNZBHEADERS', 'yes') == 'yes'
dnzb_proper_name=os.environ.get('NZBPR__DNZB_PROPERNAME', '')
dnzb_episode_name=os.environ.get('NZBPR__DNZB_EPISODENAME', '')
dnzb_movie_year=os.environ.get('NZBPR__DNZB_MOVIEYEAR', '')
dnzb_more_info=os.environ.get('NZBPR__DNZB_MOREINFO', '')
prefer_nzb_name=os.environ.get('NZBPO_PREFERNZBNAME', '') == 'yes'
use_nzb_name=False

# NZBPO_DNZBHEADERS must also be enabled
deep_scan = dnzb_headers
# difflib match threshold. Anything below is not considered a match
deep_scan_ratio = 0.60

if preview:
    print('[WARNING] *** PREVIEW MODE ON - NO CHANGES TO FILE SYSTEM ***')

if verbose and force_tv:
    print('[INFO] Forcing TV sorting (category: %s)' % category)

# List of moved files (source path)
moved_src_files = []

# List of moved files (destination path)
moved_dst_files = []

# Separator character used between file name and opening brace
# for duplicate files such as "My Movie (2).mkv"
dupe_separator = ' '

def guess_dupe_separator(format):
    """ Find out a char most suitable as dupe_separator
    """
    global dupe_separator

    dupe_separator = ' '
    format_fname = os.path.basename(format)

    for x in ('%.t', '%s.n', '%s.N'):
        if (format_fname.find(x) > -1):
            dupe_separator = '.'
            return

    for x in ('%_t', '%s_n', '%s_N'):
        if (format_fname.find(x) > -1):
            dupe_separator = '_'
            return

def unique_name(new):
    """ Adds unique numeric suffix to destination file name to avoid overwriting
        such as "filename.(2).ext", "filename.(3).ext", etc.
        If existing file was created by the script it is renamed to "filename.(1).ext".
    """
    fname, fext = os.path.splitext(new)
    suffix_num = 2
    while True:
        new_name = fname + dupe_separator + '(' + str(suffix_num) + ')' + fext
        if not os.path.exists(new_name) and new_name not in moved_dst_files:
            break
        suffix_num += 1
    return new_name

def optimized_move(old, new):
    try:
        os.rename(old, new)
    except OSError as ex:
        print('[DETAIL] Rename failed ({}), performing copy: {}'.format(ex, new))
        shutil.copyfile(old, new)
        os.remove(old)

def rename(old, new):
    """ Moves the file to its sorted location.
        It creates any necessary directories to place the new file and moves it.
    """
    if os.path.exists(new) or new in moved_dst_files:
        if overwrite and new not in moved_dst_files:
            os.remove(new)
            optimized_move(old, new)
            print('[INFO] Overwrote: %s' % new)
        else:
            # rename to filename.(2).ext, filename.(3).ext, etc.
            new = unique_name(new)
            rename(old, new)
    else:
        if not preview:
            if not os.path.exists(os.path.dirname(new)):
                os.makedirs(os.path.dirname(new))
            optimized_move(old, new)
        print('[INFO] Moved: %s' % new)
    moved_src_files.append(old)
    moved_dst_files.append(new)
    return new

def move_satellites(videofile, dest):
    """ Moves satellite files such as subtitles that are associated with base
        and stored in root to the correct dest.
    """
    if verbose:
        print('Move satellites for %s' % videofile)

    root = os.path.dirname(videofile)
    destbasenm = os.path.splitext(dest)[0]
    base = os.path.basename(os.path.splitext(videofile)[0])
    for (dirpath, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            fbase, fext = os.path.splitext(filename)
            fextlo = fext.lower()
            fpath = os.path.join(dirpath, filename)

            if fextlo in satellite_extensions:
                # Handle subtitles and nfo files
                subpart = ''
                # We support GuessIt supported subtitle extensions
                if fextlo[1:] in guessit.patterns.extension.subtitle_exts:
                    guess = guessit.guess_file_info(filename, info=['filename'])
                    if guess and 'subtitleLanguage' in guess:
                        fbase = fbase[:fbase.rfind('.')]
                        # Use alpha2 subtitle language from GuessIt (en, es, de, etc.)
                        subpart = '.' + guess['subtitleLanguage'][0].alpha2
                    if verbose:
                        if subpart != '':
                            print('Satellite: %s is a subtitle [%s]' % (filename, guess['subtitleLanguage'][0]))
                        else:
                            # English (or undetermined)
                            print('Satellite: %s is a subtitle' % filename)
                elif (fbase.lower() != base.lower()) and fextlo == '.nfo':
                    # Aggressive match attempt
                    if deep_scan:
                        guess = deep_scan_nfo(fpath)
                        if guess is not None:
                            # Guess details are not important, just that there was a match
                            fbase = base
                if fbase.lower() == base.lower():
                    old = fpath
                    new = destbasenm + subpart + fext
                    if verbose:
                        print('Satellite: %s' % os.path.basename(new))
                    rename(old, new)


def deep_scan_nfo(filename, ratio=deep_scan_ratio):
    if verbose:
        print('Deep scanning satellite: %s (ratio=%.2f)' % (filename, ratio))
    best_guess = None
    best_ratio = 0.00
    try:
        nfo = open(filename)
        # Convert file content into iterable words
        for word in ''.join([item for item in nfo.readlines()]).split():
            try:
                guess = guessit.guess_file_info(word + '.nfo', info=['filename'])
                # Series = TV, Title = Movie
                if any(item in guess for item in ('title')):
                    # Compare word against NZB name
                    diff = difflib.SequenceMatcher(None, word, nzb_name)
                    # Evaluate ratio against threshold and previous matches
                    if verbose:
                        print('Tested: %s (ratio=%.2f)' % (word, diff.ratio()))
                    if diff.ratio() >= ratio and diff.ratio() > best_ratio:
                        if verbose:
                            print('Possible match found: %s (ratio=%.2f)' % (word, diff.ratio()))
                        best_guess = guess
                        best_ratio = diff.ratio()
            except UnicodeDecodeError:
                # Ignore non-unicode words (common in nfo "artwork")
                pass
        nfo.close()
    except IOError as e:
        print('[ERROR] %s' % str(e))
    return best_guess


def cleanup_download_dir():
    """ Remove the download directory if it (or any subfodler) does not contain "important" files
        (important = size >= min_size)
    """
    if verbose:
        print('Cleanup')

    # Check if there are any big files remaining
    for root, dirs, files in os.walk(download_dir):
        for filename in files:
            path = os.path.join(root, filename)
            # Check minimum file size
            if os.path.getsize(path) >= min_size and (not preview or path not in moved_src_files):
                print('[WARNING] Skipping clean up due to large files remaining in the directory')
                return

    # Now delete all files with nice logging
    for root, dirs, files in os.walk(download_dir):
        for filename in files:
            path = os.path.join(root, filename)
            if not preview or path not in moved_src_files:
                if not preview:
                    os.remove(path)
                print('[INFO] Deleted: %s' % path)
    if not preview:
        shutil.rmtree(download_dir)
    print('[INFO] Deleted: %s' % download_dir)

STRIP_AFTER = ('_', '.', '-')

# * From SABnzbd+ (with modifications) *

REPLACE_AFTER = {
    '()': '',
    '..': '.',
    '__': '_',
    '  ': ' ',
    '//': '/',
    ' - - ': ' - ',
    '--': '-'
}

def path_subst(path, mapping):
    """ Replace the sort sting elements by real values.
        Non-elements are copied literally.
        path = the sort string
        mapping = array of tuples that maps all elements to their values
    """
    newpath = []
    plen = len(path)
    n = 0
    while n < plen:
        result = path[n]
        if result == '%':
            for key, value in mapping:
                if path.startswith(key, n):
                    n += len(key)-1
                    result = value
                    break
        newpath.append(result)
        n += 1
    return ''.join(newpath)

def get_titles(name, titleing=False):
    '''
    The title will be the part before the match
    Clean it up and title() it

    ''.title() isn't very good under python so this contains
    a lot of little hacks to make it better and for more control
    '''

    #make valid filename
    title = re.sub('[\"\:\?\*\\\/\<\>\|]', ' ', name)

    if titleing:
        title = titler(title) # title the show name so it is in a consistant letter case

        #title applied uppercase to 's Python bug?
        title = title.replace("'S", "'s")

        # Make sure some words such as 'and' or 'of' stay lowercased.
        for x in lower_words:
            xtitled = titler(x)
            title = replace_word(title, xtitled, x)

        # Make sure some words such as 'III' or 'IV' stay uppercased.
        for x in upper_words:
            xtitled = titler(x)
            title = replace_word(title, xtitled, x)

        # Make sure the first letter of the title is always uppercase
        if title:
            title = titler(title[0]) + title[1:]

    # The title with spaces replaced by dots
    dots = title.replace(" - ", "-").replace(' ','.').replace('_','.')
    dots = dots.replace('(', '.').replace(')','.').replace('..','.').rstrip('.')

    # The title with spaces replaced by underscores
    underscores = title.replace(' ','_').replace('.','_').replace('__','_').rstrip('_')

    return title, dots, underscores

def titler(p):
    """ title() replacement
        Python's title() fails with Latin-1, so use Unicode detour.
    """
    if isinstance(p, unicode):
        return p.title()
    elif gUTF:
        try:
            return p.decode('utf-8').title().encode('utf-8')
        except:
            return p.decode('latin-1', 'replace').title().encode('latin-1', 'replace')
    else:
        return p.decode('latin-1', 'replace').title().encode('latin-1', 'replace')

def replace_word(input, one, two):
    ''' Regex replace on just words '''
    regex = re.compile(r'\W(%s)(\W|$)' % one, re.I)
    matches = regex.findall(input)
    if matches:
        for m in matches:
            input = input.replace(one, two)
    return input

def get_decades(year):
    """ Return 4 digit and 2 digit decades given 'year'
    """
    if year:
        try:
            decade = year[2:3]+'0'
            decade2 = year[:3]+'0'
        except:
            decade = ''
            decade2 = ''
    else:
        decade = ''
        decade2 = ''
    return decade, decade2

_RE_LOWERCASE = re.compile(r'{([^{]*)}')
def to_lowercase(path):
    ''' Lowercases any characters enclosed in {} '''
    while True:
        m = _RE_LOWERCASE.search(path)
        if not m:
            break
        path = path[:m.start()] + m.group(1).lower() + path[m.end():]

    # just incase
    path = path.replace('{', '')
    path = path.replace('}', '')
    return path

_RE_UPPERCASE = re.compile(r'{{([^{]*)}}')
def to_uppercase(path):
    ''' Lowercases any characters enclosed in {{}} '''
    while True:
        m = _RE_UPPERCASE.search(path)
        if not m:
            break
        path = path[:m.start()] + m.group(1).upper() + path[m.end():]
    return path

def strip_folders(path):
    """ Return 'path' without leading and trailing strip-characters in each element
    """
    f = path.strip('/').split('/')

    # For path beginning with a slash, insert empty element to prevent loss
    if len(path.strip()) > 0 and path.strip()[0] in '/\\':
        f.insert(0, '')

    def strip_all(x):
        """ Strip all leading/trailing underscores and hyphens
            also dots for Windows
        """
        old_name = ''
        while old_name != x:
            old_name = x
            for strip_char in STRIP_AFTER:
                x = x.strip().strip(strip_char)

        return x

    return os.path.normpath('/'.join([strip_all(x) for x in f]))

gUTF = False
try:
    if sys.platform == 'darwin':
        gUTF = True
    else:
        gUTF = locale.getdefaultlocale()[1].lower().find('utf') >= 0
except:
    # Incorrect locale implementation, assume the worst
    gUTF = False

# END * From SABnzbd+ * END

def add_common_mapping(old_filename, guess, mapping):

    # Original dir name, file name and extension
    original_dirname = os.path.basename(download_dir)
    original_fname, original_fext = os.path.splitext(os.path.split(os.path.basename(old_filename))[1])
    original_category = os.environ.get('NZBPP_CATEGORY', '')

    # Directory name
    title_name = original_dirname.replace("-", " ").replace('.',' ').replace('_',' ')
    fname_tname, fname_tname_two, fname_tname_three = get_titles(title_name, True)
    fname_name, fname_name_two, fname_name_three = get_titles(title_name, False)
    mapping.append(('%dn', original_dirname))
    mapping.append(('%^dn', fname_tname))
    mapping.append(('%.dn', fname_tname_two))
    mapping.append(('%_dn', fname_tname_three))
    mapping.append(('%^dN', fname_name))
    mapping.append(('%.dN', fname_name_two))
    mapping.append(('%_dN', fname_name_three))

    # File name
    title_name = original_fname.replace("-", " ").replace('.',' ').replace('_',' ')
    fname_tname, fname_tname_two, fname_tname_three = get_titles(title_name, True)
    fname_name, fname_name_two, fname_name_three = get_titles(title_name, False)
    mapping.append(('%fn', original_fname))
    mapping.append(('%^fn', fname_tname))
    mapping.append(('%.fn', fname_tname_two))
    mapping.append(('%_fn', fname_tname_three))
    mapping.append(('%^fN', fname_name))
    mapping.append(('%.fN', fname_name_two))
    mapping.append(('%_fN', fname_name_three))

    # File extension
    mapping.append(('%ext', original_fext))
    mapping.append(('%EXT', original_fext.upper()))
    mapping.append(('%Ext', original_fext.title()))

    # Category
    category_tname, category_tname_two, category_tname_three = get_titles(original_category, True)
    category_name, category_name_two, category_name_three = get_titles(original_category, False)
    mapping.append(('%cat', category_tname))
    mapping.append(('%.cat', category_tname_two))
    mapping.append(('%_cat', category_tname_three))
    mapping.append(('%cAt', category_name))
    mapping.append(('%.cAt', category_name_two))
    mapping.append(('%_cAt', category_name_three))

    # Video information
    mapping.append(('%qf', guess.get('format', '')))
    mapping.append(('%qss', guess.get('screen_size', '')))
    mapping.append(('%qvc', guess.get('video_codec', '')))
    mapping.append(('%qac', guess.get('audio_codec', '')))
    mapping.append(('%qah', guess.get('audio_channels', '')))
    mapping.append(('%qrg', guess.get('release_group', '')))

def add_series_mapping(guess, mapping):

    # Show name
    series = guess.get('title', '')
    show_tname, show_tname_two, show_tname_three = get_titles(series, True)
    show_name, show_name_two, show_name_three = get_titles(series, False)
    mapping.append(('%sn', show_tname))
    mapping.append(('%s.n', show_tname_two))
    mapping.append(('%s_n', show_tname_three))
    mapping.append(('%sN', show_name))
    mapping.append(('%s.N', show_name_two))
    mapping.append(('%s_N', show_name_three))

    # season number
    season_num = str(guess.get('season', ''))
    mapping.append(('%s', season_num))
    mapping.append(('%0s', season_num.rjust(2,'0')))

    # episode names
    title = guess.get('episode_title')
    if title:
        ep_tname, ep_tname_two, ep_tname_three = get_titles(title, True)
        ep_name, ep_name_two, ep_name_three = get_titles(title, False)
        mapping.append(('%en', ep_tname))
        mapping.append(('%e.n', ep_tname_two))
        mapping.append(('%e_n', ep_tname_three))
        mapping.append(('%eN', ep_name))
        mapping.append(('%e.N', ep_name_two))
        mapping.append(('%e_N', ep_name_three))
    else:
        mapping.append(('%en', ''))
        mapping.append(('%e.n', ''))
        mapping.append(('%e_n', ''))
        mapping.append(('%eN', ''))
        mapping.append(('%e.N', ''))
        mapping.append(('%e_N', ''))

    # episode number
    if not isinstance(guess.get('episode'), list):
        episode_num = str(guess.get('episode', ''))
        mapping.append(('%e', episode_num))
        mapping.append(('%0e', episode_num.rjust(2,'0')))
    else:
        # multi episodes
        episodes = [str(item) for item in guess.get('episode')]
        episode_num_all = ''
        episode_num_just = ''
        if multiple_episodes == 'range':
            episode_num_all = episodes[0] + episode_separator + episodes[-1]
            episode_num_just = episodes[0].rjust(2, '0') + episode_separator + episodes[-1].rjust(2, '0')
        else:   # if multiple_episodes == 'list':
            for episode_num in episodes:
                ep_prefix = episode_separator if episode_num_all <> '' else ''
                episode_num_all += ep_prefix + episode_num
                episode_num_just += ep_prefix + episode_num.rjust(2,'0')

        mapping.append(('%e', episode_num_all))
        mapping.append(('%0e', episode_num_just))

    # year
    year = str(guess.get('year', ''))
    mapping.append(('%y', year))

    # decades
    decade, decade_two = get_decades(year)
    mapping.append(('%decade', decade))
    mapping.append(('%0decade', decade_two))


def add_movies_mapping(guess, mapping):

    # title
    name = guess.get('title', '')
    ttitle, ttitle_two, ttitle_three = get_titles(name, True)
    title, title_two, title_three = get_titles(name, True)
    mapping.append(('%title', title))
    mapping.append(('%.title', title_two))
    mapping.append(('%_title', title_three))

    # title (short forms)
    mapping.append(('%t', title))
    mapping.append(('%.t', title_two))
    mapping.append(('%_t', title_three))

    mapping.append(('%sn', title))
    mapping.append(('%s.n', title_two))
    mapping.append(('%s_n', title_three))

    mapping.append(('%sN', ttitle))
    mapping.append(('%s.N', ttitle_two))
    mapping.append(('%s_N', ttitle_three))

    # year
    year = str(guess.get('year', ''))
    mapping.append(('%y', year))

    # decades
    decade, decade_two = get_decades(year)
    mapping.append(('%decade', decade))
    mapping.append(('%0decade', decade_two))

    # imdb
    mapping.append(('%imdb', guess.get('imdb', '')))
    mapping.append(('%cpimdb', guess.get('cpimdb', '')))

def add_dated_mapping(guess, mapping):

    # title
    name = guess.get('title', '')
    ttitle, ttitle_two, ttitle_three = get_titles(name, True)
    title, title_two, title_three = get_titles(name, True)
    mapping.append(('%title', title))
    mapping.append(('%.title', title_two))
    mapping.append(('%_title', title_three))

    # title (short forms)
    mapping.append(('%t', title))
    mapping.append(('%.t', title_two))
    mapping.append(('%_t', title_three))

    mapping.append(('%sn', title))
    mapping.append(('%s.n', title_two))
    mapping.append(('%s_n', title_three))

    mapping.append(('%sN', ttitle))
    mapping.append(('%s.N', ttitle_two))
    mapping.append(('%s_N', ttitle_three))

    # Guessit doesn't provide episode names for dated tv shows
    mapping.append(('%desc', ''))
    mapping.append(('%.desc', ''))
    mapping.append(('%_desc', ''))

    # date
    date = guess.get('date')

    # year
    year = str(date.year)
    mapping.append(('%year', year))
    mapping.append(('%y', year))

    # decades
    decade, decade_two = get_decades(year)
    mapping.append(('%decade', decade))
    mapping.append(('%0decade', decade_two))

    # month
    month = str(date.month)
    mapping.append(('%m', month))
    mapping.append(('%0m', month.rjust(2, '0')))

    # day
    day = str(date.day)
    mapping.append(('%d', day))
    mapping.append(('%0d', day.rjust(2, '0')))

def os_path_split(path):
    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if newpath == path:
            if path: parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts

def deobfuscate_path(filename):
    start = os.path.dirname(download_dir)
    new_name = filename[len(start)+1:]
    if verbose:
        print('stripped filename: %s' % new_name)

    parts = os_path_split(new_name)
    if verbose:
        print(parts)

    part_removed = 0
    for x in range(0, len(parts)-1):
        fn = parts[x]
        if fn.find('.')==-1 and fn.find('_')==-1 and fn.find(' ')==-1:
            print('Detected obfuscated directory name %s, removing from guess path' % fn)
            parts[x] = None
            part_removed += 1

    fn = os.path.splitext(parts[len(parts)-1])[0]
    if fn.find('.')==-1 and fn.find('_')==-1 and fn.find(' ')==-1:
        print('Detected obfuscated filename %s, removing from guess path' % os.path.basename(filename))
        parts[len(parts)-1] = '-' + os.path.splitext(filename)[1]
        part_removed += 1

    if part_removed < len(parts):
        new_name = ''
        for x in range(0, len(parts)):
            if parts[x] != None:
                new_name = os.path.join(new_name, parts[x])
    else:
        print("All file path parts are obfuscated, using obfuscated NZB-Name")
        new_name = os.path.basename(download_dir) + os.path.splitext(filename)[1]

    return new_name

def remove_year(title):
    """ Removes year from series name (if exist) """
    m = re.compile('..*(\((19|20)\d\d\))').search(title)
    if not m:
        m = re.compile('..*((19|20)\d\d)').search(title)
    if m:
        if verbose:
            print('Removing year from series name')
        title = title.replace(m.group(1), '').strip()
    return title

def apply_dnzb_headers(guess):
    """ Applies DNZB headers (if exist) """

    dnzb_used = False
    if dnzb_proper_name != '':
        dnzb_used = True
        if verbose:
            print('Using DNZB-ProperName')
        if guess['vtype'] == 'series':
            proper_name = dnzb_proper_name
            if not series_year:
                proper_name = remove_year(proper_name)
            guess['title'] = proper_name
        else:
            guess['title'] = dnzb_proper_name

    if dnzb_episode_name != '' and guess['vtype'] == 'series':
        dnzb_used = True
        if verbose:
            print('Using DNZB-EpisodeName')
        guess['episode_title'] = dnzb_episode_name

    if dnzb_movie_year != '':
        dnzb_used = True
        if verbose:
            print('Using DNZB-MovieYear')
        guess['year'] = dnzb_movie_year

    if dnzb_more_info != '':
        dnzb_used = True
        if verbose:
            print('Using DNZB-MoreInfo')
        if guess['type'] == 'movie':
            regex = re.compile(r'^http://www.imdb.com/title/(tt[0-9]+)/$', re.IGNORECASE)
            matches = regex.match(dnzb_more_info)
            if matches:
                guess['imdb'] = matches.group(1)
                guess['cpimdb'] = 'cp(' + guess['imdb'] + ')'

    if verbose and dnzb_used:
        print(guess)

def guess_info(filename):
    """ Parses the filename using guessit-library """

    if use_nzb_name:
        if verbose:
            print("Using NZB-Name")
        guessfilename = os.path.basename(download_dir) + os.path.splitext(filename)[1]
    else:
        guessfilename = deobfuscate_path(filename)

    # workaround for titles starting with numbers (which guessit has problems with) (part 1)
    path, tmp_filename = os.path.split(guessfilename)
    pad_start_digits = tmp_filename[0].isdigit()
    if pad_start_digits:
        guessfilename = os.path.join(path, 'T' + tmp_filename)

    if verbose:
        print('Guessing: %s' % guessfilename)

    guess = guessit.api.guessit(unicode(guessfilename), {'allowed_languages': [], 'allowed_countries': []})

    if verbose:
        print(guess)

    # workaround for titles starting with numbers (part 2)
    if pad_start_digits:
        guess['title'] = guess['title'][1:]
        if guess['title'] == '':
            guess['title'] = os.path.splitext(os.path.basename(guessfilename))[0][1:]
            if verbose:
                print('use filename as title for recovery')

    # fix some strange guessit guessing:
    # if guessit doesn't find a year in the file name it thinks it is episode,
    # but we prefer it to be handled as movie instead
    if guess.get('type') == 'episode' and guess.get('episode', '') == '':
        guess['type'] = 'movie'
        guess['year'] = '1900'
        if verbose:
            print('episode without episode-number is a movie')

    # treat parts as episodes ("Part.2" or "Part.II")
    if guess.get('type') == 'movie' and guess.get('part') != None:
        guess['type'] = 'episode'
        guess['episode'] = guess.get('part')
        if verbose:
            print('treat parts as episodes')

    # add season number if not present
    if guess['type'] == 'episode' and (guess.get('season') == None):
        guess['season'] = 1
        if verbose:
            print('force season 1')

    # detect if year is part of series name
    if guess['type'] == 'episode':
        if series_year:
            if guess.get('year') != None and guess.get('title') != None and \
                    guess.get('season') != guess.get('year') and \
                    guess['title'] == remove_year(guess['title']):
                guess['title'] += ' ' + str(guess['year'])
                if verbose:
                    print('year is part of title')
        else:
            guess['title'] = remove_year(guess['title'])

    if guess['type'] == 'movie':
        date = guess.get('date')
        if date:
            guess['vtype'] = 'dated'
        elif force_tv:
            guess['vtype'] = 'othertv'
        else:
            guess['vtype'] = 'movie'
    elif guess['type'] == 'episode':
        guess['vtype'] = 'series'
    else:
        guess['vtype'] = guess['type']

    if dnzb_headers:
        apply_dnzb_headers(guess)

    if verbose:
        print('Type: %s' % guess['vtype'])

    if verbose:
        print(guess)

    return guess

def construct_path(filename):
    """ Parses the filename and generates new name for renaming """

    if verbose:
        print("filename: %s" % filename)

    guess = guess_info(filename)
    type = guess.get('vtype')
    mapping = []
    add_common_mapping(filename, guess, mapping)

    if type == 'movie':
        dest_dir = movies_dir
        format = movies_format
        add_movies_mapping(guess, mapping)
    elif type == 'series':
        dest_dir = series_dir
        format = series_format
        add_series_mapping(guess, mapping)
    elif type == 'dated':
        dest_dir = dated_dir
        format = dated_format
        add_dated_mapping(guess, mapping)
    elif type == 'othertv':
        dest_dir = othertv_dir
        format = othertv_format
        add_movies_mapping(guess, mapping)
    else:
        if verbose:
            print('Could not determine video type for %s' % filename)
        return None

    if dest_dir == '':
        dest_dir = os.path.dirname(download_dir)

    # Find out a char most suitable as dupe_separator
    guess_dupe_separator(format)

    # Add extension specifier if the format string doesn't end with it
    if format.rstrip('}')[-5:] != '.%ext':
        format += '.%ext'

    sorter = format.replace('\\', '/')

    if verbose:
        print('format: %s' % sorter)

    # Replace elements
    path = path_subst(sorter, mapping)

    if verbose:
        print('path after subst: %s' % path)

    # Cleanup file name
    old_path = ''
    while old_path != path:
        old_path = path
        for key, name in REPLACE_AFTER.iteritems():
            path = path.replace(key, name)

    path = path.replace('%up', '..')

    # Uppercase all characters encased in {{}}
    path = to_uppercase(path)

    # Lowercase all characters encased in {}
    path = to_lowercase(path)

    # Strip any extra strippable characters around foldernames and filename
    path, ext = os.path.splitext(path)
    path = strip_folders(path)
    path = path + ext

    path = os.path.normpath(path)

    if verbose:
        print('path after cleanup: %s' % path)

    new_path = os.path.join(dest_dir, path)

    if verbose:
        print('destination path: %s' % new_path)

    if filename.upper() == new_path.upper():
        if verbose:
            print('Destination path equals filename  - return None')
        return None

    return new_path

# Flag indicating that anything was moved. Cleanup possible.
files_moved = False

# Flag indicating any error. Cleanup is disabled.
errors = False

# Process all the files in download_dir and its subdirectories
video_files = []

for root, dirs, files in os.walk(download_dir):
    for old_filename in files:
        try:
            old_path = os.path.join(root, old_filename)

            # Check extension
            ext = os.path.splitext(old_filename)[1].lower()
            if ext not in video_extensions: continue

            # Check minimum file size
            if os.path.getsize(old_path) < min_size:
                print('[INFO] Skipping small: %s' % old_filename)
                continue

            # This is our video file, we should process it
            video_files.append(old_path)

        except Exception as e:
            errors = True
            print('[ERROR] Failed: %s' % old_filename)
            print('[ERROR] %s' % e)
            traceback.print_exc()

use_nzb_name = prefer_nzb_name and len(video_files) == 1

for old_path in video_files:
    try:
        new_path = construct_path(old_path)

        # Move video file
        if new_path:
            new_path = rename(old_path, new_path)
            files_moved = True

            # Move satellite files
            if satellites:
                move_satellites(old_path, new_path)

    except Exception as e:
        errors = True
        print('[ERROR] Failed: %s' % old_filename)
        print('[ERROR] %s' % e)
        traceback.print_exc()

# Inform NZBGet about new destination path
finaldir = ''
uniquedirs = []
for filename in moved_dst_files:
    dir = os.path.dirname(filename)
    if dir not in uniquedirs:
        uniquedirs.append(dir)
        finaldir += '|' if finaldir != '' else ''
        finaldir += dir

if finaldir != '':
    print('[NZB] FINALDIR=%s' % finaldir)

# Cleanup if:
# 1) files were moved AND
# 2) no errors happen AND
# 3) all remaining files are smaller than <MinSize>
if cleanup and files_moved and not errors:
    cleanup_download_dir()

# Returing status to NZBGet
if errors:
    sys.exit(POSTPROCESS_ERROR)
elif files_moved:
    sys.exit(POSTPROCESS_SUCCESS)
else:
    sys.exit(POSTPROCESS_NONE)
