# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import conasems.experienciasrede


class ConasemsExperienciasredeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=conasems.experienciasrede)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "conasems.experienciasrede:default")


CONASEMS_EXPERIENCIASREDE_FIXTURE = ConasemsExperienciasredeLayer()


CONASEMS_EXPERIENCIASREDE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONASEMS_EXPERIENCIASREDE_FIXTURE,),
    name="ConasemsExperienciasredeLayer:IntegrationTesting",
)


CONASEMS_EXPERIENCIASREDE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONASEMS_EXPERIENCIASREDE_FIXTURE,),
    name="ConasemsExperienciasredeLayer:FunctionalTesting",
)
