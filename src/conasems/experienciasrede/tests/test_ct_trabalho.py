# -*- coding: utf-8 -*-
from conasems.experienciasrede.content.trabalho import ITrabalho  # NOQA E501
from conasems.experienciasrede.testing import (  # noqa
    CONASEMS_EXPERIENCIASREDE_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TrabalhoIntegrationTest(unittest.TestCase):

    layer = CONASEMS_EXPERIENCIASREDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_trabalho_schema(self):
        fti = queryUtility(IDexterityFTI, name="Trabalho")
        schema = fti.lookupSchema()
        self.assertEqual(ITrabalho, schema)

    def test_ct_trabalho_fti(self):
        fti = queryUtility(IDexterityFTI, name="Trabalho")
        self.assertTrue(fti)

    def test_ct_trabalho_factory(self):
        fti = queryUtility(IDexterityFTI, name="Trabalho")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ITrabalho.providedBy(obj),
            "ITrabalho not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_trabalho_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="Trabalho",
            id="trabalho",
        )

        self.assertTrue(
            ITrabalho.providedBy(obj),
            "ITrabalho not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("trabalho", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("trabalho", parent.objectIds())

    def test_ct_trabalho_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Trabalho")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_trabalho_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Trabalho")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "trabalho_id",
            title="Trabalho container",
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type="Document",
            title="My Content",
        )
        self.assertTrue(obj, "Cannot add {0} to {1} container!".format(obj.id, fti.id))
