#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime, timedelta
import sys
from time import sleep

import meetup_api_client
import wikitools


class MeetBotPage(object):
    # Human-readable name for this MeetBotPage.
    name = None

    # A wikitools Wiki edit for the wiki to edit.
    wiki = None

    # A wikitools Page object for the page to be edited.
    page = None

    # Method that takes a list of Meetup Event objects and returns wikitext
    # for this page.
    def events_to_wikitext(self, events):
        raise NotImplementedError


class MeetBot(object):
    def __init__(self, meetup_api, meetup_group_urlname, *meetbot_pages):
        self.meetup = meetup_api
        self.meetup_group_urlname = meetup_group_urlname
        self.meetbot_pages = meetbot_pages

    @property
    def events(self):
        request = self.meetup.get_events(group_urlname=
                                         self.meetup_group_urlname)
        # TODO: error/throttle checking
        return request.results

    def run_once(self, verbose=False):
        events = self.events
        if verbose:
            print("Found {0} Meetup events".format(len(events)),
                  file=sys.stderr)
        
        for page in self.pages:
            if verbose:
                print("Updating [[{1}]] on {0}...".format(page.name,
                                                          page.page.title),
                      file=sys.stderr)
            wikitext = settings.events_to_wikitext(events)
            request = settings.page.edit(text=wikitext)
            # TODO: error checking

    def run(self, verbose=False):
        while True:
            try:
                self.run_once(verbose=verbose)
            except:
                pass # TODO: error handling
            sleep(3600) # TODO: sleep until on the hour
