Dedupe
======

Dee-Doop, dee-doop, Deedoop.

Find duplicate songs, and (optionally) delete them.

Written by Brandon W Maister <quodlibetor@gmail.com>

Homepage: https://github.com/quodlibetor/dedupe

Let me know if you have any problems or feature requests. Note that
right now the program is *incredibly* alpha, it has basically no features.


Installation
------------

On Mac open Terminal.app, on Linux it's via your preferred terminal
emulator. On Windows, sorry, it *should* work but you're on your own
for installation since I don't have a windows box handy to create
installers.

It's recommended to install via pip_, as that will install mutagen_ for you, and without that nothing will work. So install pip and then do::

    $ pip install dedupe

or if you've already downloaded it::

    $ pip install ./dedupe/setup.py

.. _pip: http://pypi.python.org/packages/pip
.. _mutagen: http://code.google.com/mutagen

Usage
-----

This program is in an incredibly early state. It might kill your
children or set fire to your house. It hasn't done that to me, but I'm
kinda nice to it. You have been warned.

Once it's installed, pass it a list of one or more directories to scan
for duplicate songs. Dedupe will scan the directories, trying to read
metadata (artist, album, title, etc) from each song. Any songs that
match artist, album, title *exactly* are considered duplicates.

It will print out a list of errors, then a list of songs that are
duplicated, as well as the paths to all the duplicates. For example::

    $ dedupe music new_music
    "Could not handle 'path': 'reason'"
    "Could not handle 'another/path': 'reason'"
    ----------------------------------------------------------------
    Duplicates:
    Sample Artist - Sample Album - Sample Song:
        music/path/to/song.mp3
        new_music/another/path/to/a/song/in/a/weird/place.ogg
        new_music/this/guy/had/too/many/copies/of/this/song.flac

It will also write a file with the path to the lowest-bitrate versions
of the songs to a file called ``duplicates.m3u``, so for the above
``duplicates.m3u`` would look something like::

    music/path/to/song.mp3
    new_music/another/path/to/a/song/in/a/weird/place.ogg

You can edit duplicates.m3u (it's just a text file, you can open it with
textedit or gedit or any other text editor) however you want, for
example by removing paths to files that you want to keep, or anything
else.

You should also be able to import it into an audio player to see what
all the songs are, but I've never tried.

You can then run dedupe.py with the ``--kill-duplicates`` options, and
it will delete everything in the ``duplicates.m3u`` file::

    $ dedupe --kill-duplicates
    This will DELETE everything in duplicates.m3u.
    This is NOT UNDOABLE.
    Type 'y' if you are sure you want to continue: y
    $

If a directory is made completely empty by kill-duplicates command, it
will be deleted, too.

Known Formats and Caveats
~~~~~~~~~~~~~~~~~~~~~~~~~

Caveats
~~~~~~~

Since the algorithm works by comparing Artist/Album/Title, if there is
no artist or album tag there is nothing much I can do. I do use the
filename if there is no title tag, though.

I plan make it possible to compare using other fields, especially a
Artist/Title option might be nice for people who want to get rid of
duplicates caused by greatest hits collections and etc.

I have *absolutely no intention* of ever allowing dupe-finding by
file-content matching. There is no fast way to do it, and identical
songs encoded at different qualities or at the same quality by
different programs or versions of the same program would not
match. Since it would take hours per run, would be a bunch of extra
work for me, and it would *not work* I'm not doing it.

Known Formats
~~~~~~~~~~~~~

Basically everything supported by mutagen, this includes: ogg, mp3,
flac, APE, and many, many more.

Copying
-------

This program is licensed under the GNU GPL: copy it and give it to
your friends. If you make something fancy that is very heavily
dependent upon this code you should notify me of your changes and make
your source available to all users. See the file COPYING for the
legalese.

Big Scary License Block follows:


Copyright (C) 2010 Brandon W Maister quodlibetor@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
