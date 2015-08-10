# -*- coding: utf-8 -*-

from plone import api

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from plone.testing import z2
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
import transaction

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Solgema.fullcalendar
        self.loadZCML(package=Solgema.fullcalendar)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Solgema.fullcalendar:default')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        folder_one = api.content.create(
            type='Folder',
            id='folder_one',
            container=portal,
        )

        event_one = api.content.create(
            type='Event',
            id='event_one',
            title='Event One',
            container=folder_one,
        )

        event_two = api.content.create(
            type='Event',
            id='event_two',
            title='Event Two',
            container=folder_one,
        )

        folder_two =  api.content.create(
            type='Folder',
            id='folder_two',
             container=folder_one,
        )
        
        collection_one = api.content.create(
            type='Collection',
            id='collection_one',
            title='Collection One',
            container=folder_two,
        )

        transaction.commit()


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Solgema.fullcalendar:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='Solgema.fullcalendar:Functional',
)

ROBOT_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="ROBOT_TESTING",
)
