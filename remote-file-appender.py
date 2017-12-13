#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sched
import sys
import time
import urllib

print 'Remote File Appender'

DOWNLOADS_DIR = 'downloads'

SCHED = sched.scheduler(time.time, time.sleep)
INTERVAL = 5

def run(sc):
    with open('urls.txt') as furls:
        urls = furls.readlines()

    # you may also want to remove whitespace characters like `\n` at the end of each line
    urls = [url.strip() for url in urls]

    # removing empty lines
    urls = filter(None, urls)

    print '--------------------------------------------------'
    print 'Monitored URLs: ', urls

    for url in urls:
        try:
            logname = url.rsplit('/', 1)[-1].strip()

            # Combine the name and the downloads directory to get the local filename
            filename = os.path.join(DOWNLOADS_DIR, logname)

            # Download the file if it does not exist
            if not os.path.isfile(filename):
                urllib.urlretrieve(url, filename)
                print filename, ' created'

            # Just add the new lines
            else:
                newloglines = urllib.urlopen(url).readlines()
                newloglines = [log.strip() for log in newloglines]

                with open(filename) as flog:
                    actualloglines = flog.readlines()
                actualloglines = [log.strip() for log in actualloglines]

                cont = 0
                with open(filename, 'a') as logfile:
                    for newlogline in newloglines:
                        if newlogline not in actualloglines:
                            logfile.write(newlogline + '\n')
                            cont += 1

                print filename, ' updated with ', cont, ' new lines'

        except:
            print 'Unexpected error: ', sys.exc_info()[0]

    print 'Job done, waiting ', INTERVAL, ' seconds'
    SCHED.enter(INTERVAL, 1, run, (sc,))


if __name__ == '__main__':
    SCHED.enter(1, 1, run, (SCHED,))
    SCHED.run()
