#VideoSort
Post-processing script for [NZBGet](http://nzbget.net).

This is a script for downloaded TV shows and movies. It uses scene-standard naming conventions to match TV shows and movies and rename/move/sort/organize them as you like.

## Example

Let's say the download folder has following files:

    [dir]	/home/user/downloads/Futurama.S07E18.The.Inhuman.Torch.XVID
    [file]	/home/user/downloads/Futurama.S07E18.The.Inhuman.Torch.XVID/F0718TIT.avi

VideoSort can rename the video-file and move it into another directory creating sub-directories when necessary:

    [dir]	/home/user/videos/Futurama
    [dir]	/home/user/videos/Futurama/Season 7
    [file]	/home/user/videos/Futurama/Season 7/Futurama - S07E18 - The Inhuman Torch.avi

The formatting rules for destination file name (and sub-directories) are definable via configuration options.

VideoSort can organize:
 - seasoned tv shows;
 - dated tv shows;
 - movies.

## Installation

 - Download the newest version from [releases page](https://github.com/nzbget/VideoSort/releases/latest).
 - Unpack into pp-scripts directory. Your pp-scripts directory now should have folder "videosort" with subfolder "lib" and file "VideoSort.py";
 - Open settings tab in NZBGet web-interface and define settings for VideoSort;
 - Save changes and restart NZBGet.

## Formatting string

### Movies

 - %t, %.t, %_t - movie title with words separated with spaces, dots or underscores (case-adjusted);
 - %tT, %t.T, %t_T - movie title (original letter case);
 - %y	- year;
 - %decade - two-digits decade (90, 00, 10);
 - %0decade - four-digits decade (1990, 2000, 2010);
 - %imdb - IMDb ID, requires DNZB-header "X-DNZB-MoreInfo", containing link to imdb.com;
 - %cpimdb - IMDb ID (formatted for CouchPotato), requires DNZB-header "X-DNZB-MoreInfo", containing link to imdb.com.
 
### Seasoned TV shows

 - %sn, %s.n, %s_n - show name with words separated with spaces, dots or underscores (case-adjusted);
 - %sN, %s.N, %s_N - show name (original letter case);
 - %s - season number (1, 2);
 - %0s - two-digits season number (01, 02);
 - %e - episode number (1, 2);
 - %0e - two-digits episode number (01, 02);
 - %en, %e.n, %e_n - episode name (case-adjusted);
 - %eN, %e.N, %e_N - episode name (original letter case);

### Dated TV shows

 - %sn, %s.n, %s_n - show name with words separated with spaces, dots or underscores (case-adjusted);
 - %sN, %s.N, %s_N - show name (original letter case);
 - %y	- year;
 - %decade - two-digits decade (90, 00, 10);
 - %0decade - four-digits decade (1990, 2000, 2010).
 - %m	- month (1-12);
 - %0m	- two-digits month (01-12);
 - %d	- day (1-31);
 - %0d	- two-digits day (01-31);

### General

These specifiers can be used with all three types of supported video files:

 - %dn - original directory name (nzb-name);
 - %fn - original filename;
 - %ext - file extension;
 - %Ext - file extension (case-adjusted);
 - %qf - video format (HTDV, BluRay, WEB-DL);
 - %qss - screen size (720p, 1080i);
 - %qvc - video codec (x264);
 - %qac - audio codec (DTS);
 - %qah - audio channels (5.1);
 - %qrg - release group;
 - {{text}} - uppercase the text;
 - {TEXT} - lowercase the text;

Credits
-------
The script relies on python library "guessit" (http://guessit.readthedocs.org) to extract information from file names and includes portions of code from "SABnzbd+" (http://sabnzbd.org).
