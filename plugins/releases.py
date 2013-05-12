#!/usr/bin/python -tt
##
# Copyright (C) 2013 by Kernel.org
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import os
import time, datetime
import re

from git import Repo

from pelican import signals, utils

from feedgenerator import Rss201rev2Feed
import json

# Pelican plugin API
def register():
    signals.article_generator_init.connect(kernel_releases_init)
    signals.article_generate_context.connect(fetch_kernel_releases)

def kernel_releases_init(gen):
    gen.releases_instance = KernelReleases(gen)

def fetch_kernel_releases(gen, metadata):
    gen.context['current_releases'] = gen.releases_instance.current_releases
    gen.context['latest_release']   = gen.releases_instance.latest_release

class KernelReleases():

    def __init__(self, generator):
        self.release_tracker = '/var/lib/mirror/release-tracker.json'

        self.rss_path = os.path.join(generator.output_path, 'feeds', 'kdist.xml')
        self.finger_path = os.path.join(generator.output_path, 'finger_banner')
        self.json_path = os.path.join(generator.output_path, 'releases.json')

        settings = generator.settings

        GIT_MAINLINE = settings.get('GIT_MAINLINE')
        GIT_STABLE   = settings.get('GIT_STABLE')
        GIT_NEXT     = settings.get('GIT_NEXT')

        LONGTERM_KERNELS = settings.get('LONGTERM_KERNELS')
        EOL_KERNELS      = settings.get('EOL_KERNELS')

        self.pub_mount = settings.get('PUB_MOUNT')

        repo = Repo(GIT_MAINLINE)
        tagrefs = self.get_tagref_list(repo)

        rc_reg = re.compile('v.*-rc\d+$')
        mainline_rc = self.find_latest_matching(tagrefs, rc_reg)
        rel_reg = re.compile('v[^-]*\d+$')
        mainline_rel = self.find_latest_matching(tagrefs, rel_reg)

        # if mainline_rel is newer than mainline_rc, ignore mainline_rc
        if mainline_rc[1] < mainline_rel[1]:
            mainline_rc = None

        # Move on to the linux-stable repo
        repo = Repo(GIT_STABLE)
        # ignore any tags older than 12 months
        cutoff = time.time() - 31536000

        tagrefs = self.get_tagref_list(repo, cutoff)

        # find all tags matching vX.X.X
        rel_reg = re.compile('v\d+\.\d+\.\d+$')
        matched = []
        for tagref in tagrefs:
            if rel_reg.match(tagref.name):
                matched.append(tagref)

        stable = []
        seen = []

        for tagref in matched:
            # does it match a longterm release?
            ignore = False
            for ver in LONGTERM_KERNELS:
                if tagref.name.find(ver) > 0:
                    # this is a long-term release, ignore
                    ignore = True
                    continue
            if ignore:
                continue

            # Drop the final \.\d+ and find the latest matching
            components = tagref.name.split('.')
            regex = re.compile('^' + '\\.'.join(components[:-1]))

            if regex in seen:
                continue

            stable.append(self.find_latest_matching(matched, regex))
            seen.append(regex)

        stable = sorted(stable, key=lambda tagged: tagged[0].split('.')[1], reverse=True)

        releases = []

        if mainline_rc is not None:
            releases.append(self.make_release_line(mainline_rc, 'mainline'))

        # look at the last stable and see if mainline_rel fits into it
        latest_stable = stable.pop(0)

        if latest_stable[0].find(mainline_rel[0]) != 0:
            releases.append(self.make_release_line(mainline_rel, 'mainline'))
            latest = self.make_release_line(mainline_rel, 'latest')
        else:
            latest = self.make_release_line(latest_stable, 'latest')
            # if latest stable is newer than latest mainline, but there are no
            # -rc kernels, list the latest mainline in the releases table anyway.
            if mainline_rc is None:
                releases.append(self.make_release_line(mainline_rel, 'mainline'))


        releases.append(self.make_release_line(latest_stable, 'stable'))

        # add other stable kernels and mark EOL accordingly
        eolcount = 0
        for rel in stable:
            iseol = False
            for eolrel in EOL_KERNELS:
                if rel[0].find(eolrel) >= 0:
                    iseol = True
                    eolcount += 1
                    break

            # limit the number of EOL kernels to 2.
            if not iseol or (iseol and eolcount <= 2):
                releases.append(self.make_release_line(rel, 'stable', iseol))

        # find latest long-term releases
        for rel in LONGTERM_KERNELS:
            components = rel.split('.')
            regex = re.compile('^v' + '\\.'.join(components) + '\\.\\d+$')
            found = self.find_latest_matching(tagrefs, regex)
            if found is not None:
                releases.append(self.make_release_line(found, 'longterm'))

        # now find latest tag in linux-next
        repo = Repo(GIT_NEXT)
        tagrefs = self.get_tagref_list(repo, cutoff)

        regex = re.compile('^next-')
        rel = self.find_latest_matching(tagrefs, regex)
        releases.append(self.make_release_line(rel, 'linux-next'))

        self.current_releases = releases
        self.latest_release   = latest

        self.generate_rss_feed()
        self.generate_finger_banner()
        self.generate_releases_json()
        self.check_release_tracker()

    def check_release_tracker(self):
        # Load known releases from the release tracker file
        known_old = None
        known_new = []

        if os.path.exists(self.release_tracker):
            try:
                fh = open(self.release_tracker, 'r')
                known_old = json.load(fh)
                fh.close()
            except:
                # it's better to not announce something than to spam
                # people needlessly.
                pass

        for chunks in self.current_releases:
            release = chunks[1]
            if known_old is None or release in known_old:
                # Don't announce this release. Add to known_new and move on
                known_new.append(release)
            else:
                # This appears to be a new release.
                if chunks[5] is None or chunks[6] is None or chunks[7] is None:
                    # Don't announce anything that doesn't have source, patch or sign.
                    continue
                self.send_release_email(chunks)
                known_new.append(release)

        fh = open(self.release_tracker, 'w')
        json.dump(known_new, fh, indent=4)
        fh.close()

    def send_release_email(self, chunks):
        (label, release, iseol, timestamp, isodate, source, sign, patch, incr, changelog, gitweb) = chunks
        if iseol:
            eol = ' (EOL)'
        else:
            eol = ''

        import smtplib
        from email.mime.text import MIMEText
        from email.Utils import COMMASPACE, formatdate, make_msgid

        body = ( "Linux kernel version %s%s has been released. It is available from:\r\n" % (release, eol)
               + "\r\n"
               + "Patch:          https://www.kernel.org/%s\r\n" % patch
               + "Full source:    https://www.kernel.org/%s\r\n" % source
               + "PGP Signature:  https://www.kernel.org/%s\r\n" % sign
               + "\r\n"
               + "-----------------------------------------------------------------------------\r\n"
               + "This is an automatically generated message. To unsubscribe from this list,\r\n"
               + "please send a message to majordomo@vger.kernel.org containing the line:\r\n"
               + "\r\n"
               + "\tunsubscribe linux-kernel-announce <your_email_address>\r\n"
               + "\r\n"
               + "... where <your_email_address> is the email address you used to subscribe\r\n"
               + "to this list.\r\n"
               + "-----------------------------------------------------------------------------\r\n"
               + "\r\n"
               + "You can view the summary of the changes at the following URL:\r\n"
               + "https://www.kernel.org/diff/diffview.cgi?file=/%s\r\n" % patch)

        msg = MIMEText(body)
        msg['Subject'] = "Linux kernel %s released" % release
        msg['From'] = 'Linux Kernel Distribution System <kdist@linux.kernel.org>'
        msg['To'] = 'linux-kernel-announce@vger.kernel.org'
        msg['Bcc'] = 'ftpadmin@kernel.org'
        msg['Date'] = formatdate(localtime=True)
        msg['Message-Id'] = make_msgid('kdist.linux.kernel.org')
        msg['X-Linux-Kernel-Version'] = release
        msg['X-Linux-Kernel-Patch-URL'] = "https://www.kernel.org/%s" % patch
        msg['X-Linux-Kernel-Full-URL'] = "https://www.kernel.org/%s" % source

        s = smtplib.SMTP('mail.kernel.org')
        s.sendmail('kdist@linux.kernel.org', ['linux-kernel-announce@vger.kernel.org', 'ftpadmin@kernel.org'], msg.as_string())
        s.quit()

    def generate_releases_json(self):
        # Put release info into a .json file for easy import and parse
        out = {'releases': []}
        for (label, release, iseol, timestamp, isodate, source, sign, patch, incr, changelog, gitweb) in self.current_releases:
            if source:
                source = 'https://www.kernel.org/%s' % source
            if sign:
                sign = 'https://www.kernel.org/%s' % sign
            if patch:
                patch = 'https://www.kernel.org/%s' % patch
            if incr:
                incr = 'https://www.kernel.org/%s' % incr
            if changelog:
                changelog = 'https://www.kernel.org/%s' % changelog

            relhash = {
                'moniker': label,
                'version': release,
                'iseol':   iseol,
                'released': {
                    'timestamp': timestamp,
                    'isodate':   isodate,
                },
                'source': source,
                'pgp': sign,
                'patch': {
                    'full': patch,
                    'incremental': incr,
                },
                'changelog': changelog,
                'gitweb': gitweb
            }

            out['releases'].append(relhash)

        out['latest_stable'] = {
            'version': self.latest_release[1],
        }

        fh = open(self.json_path, 'w')
        json.dump(out, fh, indent=4)
        fh.close()


    def generate_finger_banner(self):
        # Just a bit of legacy silliness
        contents = ''
        for chunks in self.current_releases:
            label   = chunks[0]
            release = chunks[1]
            iseol   = chunks[2]

            if label == 'mainline':
                line = ' 3'
            elif label == 'linux-next':
                line = ''
            else:
                bits = release.split('.')
                bits.pop(-1)
                line = ' ' + '.'.join(bits)

            if iseol:
                eol = ' (EOL)'
            else:
                eol = ''

            leftside = 'The latest %s%s version of the Linux kernel is:' % (label, line)
            contents += '{0:<61} {1}{2}\n'.format(leftside, release, eol)

        fp = open(self.finger_path, 'w')
        fp.write(contents)
        fp.close()

    def generate_rss_feed(self):

        feed = Rss201rev2Feed(
                title='Latest Linux Kernel Versions',
                link='http://www.kernel.org',
                feed_url='http://www.kernel.org/feeds/kdist.xml',
                description='Latest Linux Kernel Versions',
                creator='FTP Admin <ftpadmin@kernel.org>'
                )
        for (label, release, iseol, timestamp, isodate, source, sign, patch, incr, changelog, gitweb) in self.current_releases:
            if iseol:
                eol = ' (EOL)'
            else:
                eol = ''

            contents = '''
            <table>
                <tr><th align="right">Version:</th><td><strong>%s%s</strong> (%s)</td></tr>
                <tr><th align="right">Released:</th><td>%s</td></tr>
            ''' % (release, eol, label, isodate)

            if source:
                contents += '''
                <tr><th align="right">Source:</th><td><a href="https://www.kernel.org/%s">linux-%s.tar.xz</a></td></tr>''' % (source, release)

            if sign:
                contents += '''
                <tr><th align="right">PGP Signature:</th><td><a href="https://www.kernel.org/%s">linux-%s.tar.sign</a></td></tr>''' % (sign, release)

            if patch:
                contents += '''
                <tr><th align="right">Patch:</th><td><a href="https://www.kernel.org/%s">patch-%s.xz</a>''' % (patch, release)
                if incr:
                    contents += ''' (<a href="https://www.kernel.org/%s">Incremental</a>)''' % incr
                contents += '''</td></tr>'''

            if changelog:
                contents += '''
                <tr><th align="right">ChangeLog:</th><td><a href="https://www.kernel.org/%s">ChangeLog-%s</a></td></tr>''' % (changelog, release)

            contents += '''
            </table>'''

            feed.add_item(
                title='%s: %s' % (release, label),
                link='http://www.kernel.org/',
                unique_id='kernel.org,%s,%s,%s' % (label, release, isodate),
                description=contents,
                pubdate=datetime.datetime.fromtimestamp(timestamp)
            )

        # We really should be generating after site is done,
        # but I'm too lazy to figure out the plugin hooks for that
        utils.mkdir_p(os.path.dirname(self.rss_path))

        fp = open(self.rss_path, 'w')
        feed.write(fp, 'utf-8')
        fp.close()

    def make_release_line(self, rel, label, iseol=False):
        # drop the leading 'v':
        if rel[0][0] == 'v':
            release = rel[0][1:]
        else:
            release = rel[0]

        timestamp = rel[1]
        isodate   = time.strftime('%Y-%m-%d', time.gmtime(rel[1]))

        # some magic here to calculate where the source is
        urlpath = 'pub/linux/kernel'

        if release.find('3.') == 0:
            # This is version 3.x, so will be in /v3.x/
            urlpath += '/v3.x'

            if release.find('-rc') > 0:
                # This is a testing kernel, so will be in /testing/
                urlpath += '/testing'

        elif release.find('2.6') == 0:
            # We're hardcoding ourselves here, but this will rarely change
            urlpath += '/v2.6/longterm'

            if release.find('2.6.32') == 0:
                urlpath += '/v2.6.32'
            else:
                urlpath += '/v2.6.34'
        else:
            # Next-kernels are too unpredictable to bother
            urlpath = None

        source    = None
        sign      = None
        patch     = None
        incr      = None
        changelog = None
        gitweb    = None

        if urlpath is not None:
            source = '%s/linux-%s.tar.xz' % (urlpath, release)
            sign   = '%s/linux-%s.tar.sign' % (urlpath, release)
            patch  = '%s/patch-%s.xz' % (urlpath, release)

            if label.find('stable') == 0 or label.find('longterm') == 0:
                changelog = '%s/ChangeLog-%s' % (urlpath, release)
                gitweb    = 'https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/log/?id=refs/tags/v%s' % release
                # incr patches are named incr/3.5.(X-1)-(X).xz, which we calculate here
                try:
                    bits = release.split('.')
                    lastbit = int(bits.pop(-1))
                    if lastbit > 1:
                        prevbit = str(lastbit - 1)
                        bits.append(prevbit)
                        prevrel = '.'.join(bits)
                        incr = '%s/incr/patch-%s-%s.xz' % (urlpath, prevrel, lastbit)
                except ValueError:
                    incr = None

            elif label.find('mainline') == 0:
                gitweb = 'https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/log/?id=refs/tags/v%s' % release

        if label.find('linux-next') == 0:
            gitweb = 'https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/log/?id=refs/tags/%s' % release

        # Verify that source, patch, changelog and incremental patch exist
        if source and not os.path.exists('%s/%s' % (self.pub_mount, source)):
            source = None
        if patch and not os.path.exists('%s/%s' % (self.pub_mount, patch)):
            patch = None
        if changelog and not os.path.exists('%s/%s' % (self.pub_mount, changelog)):
            changelog = None
        if incr and not os.path.exists('%s/%s' % (self.pub_mount, incr)):
            incr = None

        # This needs to be refactored into a hash. In my defense,
        # it started with 3 entries.
        return (label, release, iseol, timestamp, isodate, source, sign, patch, incr, changelog, gitweb)

    def get_tagref_list(self, repo, cutoff=None):
        tagrefs = []
        for tagref in repo.tags:
            try:
                tdate = tagref.tag.tagged_date
            except:
                # Some of the tags break git-python due to not having an associated
                # commit. Work around this limitation by ignoring those tags.
                continue

            # Is it too old?
            if cutoff is not None and tdate < cutoff:
                continue

            tagrefs.append(tagref)

        return tagrefs

    def find_latest_matching(self, tagrefs, regex):
        current = None

        for tagref in tagrefs:
            tdate = tagref.tag.tagged_date

            # Does it match the regex?
            if not regex.match(tagref.name):
                continue

            # is it older than current?
            if current is None or current.tag.tagged_date < tdate:
                current = tagref

        if current is None:
            return None

        return (current.name, current.tag.tagged_date)

