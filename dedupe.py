#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import mutagen

VERSION = "0.1.1"

class NotASong(Exception):
    pass

class Song(object):
    """Create song info from audio file

    `Song.__init__` might raise NotASong()
    """

    tags = ('artist', 'album', 'title',
            'length', 'bitrate', 'type')

    def __init__(self, path):
        if not os.path.exists(path):
            print >>sys.stderr, "%s does not exist" % path

        self.path = path
        self.type = os.path.splitext(path)[1][1:]
        self.artist = self.album = self.title = None
        self.set_tags()

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u"{0.artist[0]} - {0.album[0]} - {0.title[0]}".format(self)

    def set_tags(self):
        try:
            song = mutagen.File(self.path, easy=True)
        except Exception:
            raise NotASong(self.path)

        if song is None:
            raise NotASong(self.path)

        for tag in Song.tags[:-1]: # skip type
            setattr(self, tag,
                    self._get_tag(song, tag))

    def get_tag(self, tag):
        try:
            return getattr(self, tag)
        except AttributeError:
            song = mutagen.File(self.path, easy=True)

            if song is None:
                raise NotASong()

            setattr(self, tag,
                    self._get_tag(song, tag))
            return getattr(self, tag)


    def _get_tag(self, song, tag):
        # try slightly harder than mutagen to get some things, and
        # maybe print a warning.
        try:
            return song[tag]
        except KeyError:
            if tag == 'bitrate':
                if self.type == 'flac':
                    return float('inf')
                return song.info.bitrate
            elif tag == 'length':
                return song.info.length
            elif tag in ('title', 'TIT2'):
                fname = os.path.basename(self.path)
                fname = os.path.splitext(fname)[0]
                print >>sys.stderr, "WARNING: {0} has no title,"\
                    " using '{1}' instead".format(self.path, fname)
                return [fname]
            else:
                raise

valid_exts = set(['.mp3', '.ogg', '.ogf', '.ogs', '.flac', '.ape', '.apev2',
                  '.mp4', '.m4a', '.wav', '.mus', ])
wtags = {"TIT2": 'title',
         "TALB": 'album',
         "TPE1": 'artist'}
def add_song(songs, dups, path):
    """Validate and add song at `path` to `songs` and possibly `dupes`
    """
    if not os.path.isfile(path):
        return

    try:
        song = Song(path)
    except NotASong:
        return
    except KeyError, e:
        comp, ext = os.path.splitext(path)
        if ext.lower() in valid_exts:
            global wtags
            e = str(e)[1:-1]
            print >>sys.stderr, "ERROR:   {0:6} tag not present, skipping:"\
                " '{1}' ".format(wtags.get(e,e),
                                 path,)
        return

    ss = str(song)
    if ss in songs:
        songs[ss].append(song)
        if ss in dups:
            dups[ss].append(song)
        else:
            # the items in songs are lists of songs
            dups[ss] = [song, songs[ss][0]]
    else:
        songs[ss] = [song]

def open_editor():
    from subprocess import Popen
    def which(program):
        def is_exe(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    # problem here is that 'open' in linux starts a program on a new
    # virtual terminal, but in OSX it's the equivalent of the various
    # gui-open funcs.
    #
    # Hopefully putting it at the end of this list will make the
    # problem go away.
    command = None
    for com in ('gnome-open', 'kde-open', 'xdg-open',
                'open',):
        if which(com):
            command = com
            break
    else:
        if sys.platform.startswith('win'):
            command = 'start' # I think?
    if command is None:
        exit('couldn\'t figure out how to open the duplicates file, '
             'sorry but you will have to do it yourself.')
    Popen('%s %s' % (command, os.path.realpath('duplicates.txt')),
                   shell=True)

def main(args):
    songs = {}
    dups = {}

    for root in args.root:
        for dirpath, dirs, fnames in os.walk(root):
            for f in fnames:
                add_song(songs, dups, os.path.join(dirpath, f))

    for dupstring, songlist in dups.iteritems():
        dups[dupstring] = sorted(songlist, key=lambda s: s.bitrate)


    print "\n"+("-"*70)+"\nDuplicates:"

    keys = sorted(dups.keys())
    with open("duplicates.txt", 'w') as fh:
        for key in keys:
            print key + ":"
            for i, song in enumerate(dups[key]):
                print "    " + song.path + ", bitrate:" + str(song.bitrate)
                if i > 0:
                    fh.write(song.path + "\n")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(action="store", dest="root", nargs="*",
                        help="The music folder to check")
    parser.add_argument("--kill-duplicates", action="store_true",
                        default=False,
                        help="kill all the paths in a file named "
                        "'duplicates.txt'")
    parser.add_argument("-e", "--edit-duplicates",
                        default=False, action="store_true",
                        help="Open duplicates.txt for editing."
                        "If this is passed in combination with some roots"
                        " to check, the editor will be opened immediately"
                        " after dedupe is finished checking them.")
    parser.add_argument("--logfile",
                        help="print warnings and errors to this file"
                        " instead of to your terminal screen.")

    return parser.parse_args()

def main():
    args = parse_args()
    args.root = [os.path.expanduser(root) for root in args.root]
    if args.root:
        orig_stderr = sys.stderr
        close_logfile = False
        if args.logfile is not None:
            sys.stderr = open(args.logfile, 'w')
            close_logfile= True

        try:
            main(args)
        except (EOFError, KeyboardInterrupt, SystemExit):
            print
        finally:
            if close_logfile:
                sys.stderr.close()
            sys.stderr = orig_stderr

    if args.edit_duplicates:
        open_editor()

    if args.kill_duplicates:
        confirm = raw_input("This will DELETE everything in duplicates.txt.\n"
                            "This is NOT UNDOABLE.\n"
                            "Type 'y' if you are sure you want to continue: ")
        if confirm =='y':
            for path in open("duplicates.txt"):
                os.unlink(path.rstrip())
                dirname = os.path.dirname(path)
                while os.listdir(dirname) == []:
                    os.unlink(dirname)
                    dirname = os.path.dirname(dirname)
        else:
            print "You didn't say y: exiting."


if __name__ == "__main__":
    main()
