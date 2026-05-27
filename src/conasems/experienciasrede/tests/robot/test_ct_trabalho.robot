# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s conasems.experienciasrede -t test_trabalho.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src conasems.experienciasrede.testing.CONASEMS_EXPERIENCIASREDE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/conasems/experienciasrede/tests/robot/test_trabalho.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Trabalho
  Given a logged-in site administrator
    and an add Trabalho form
   When I type 'My Trabalho' into the title field
    and I submit the form
   Then a Trabalho with the title 'My Trabalho' has been created

Scenario: As a site administrator I can view a Trabalho
  Given a logged-in site administrator
    and a Trabalho 'My Trabalho'
   When I go to the Trabalho view
   Then I can see the Trabalho title 'My Trabalho'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Trabalho form
  Go To  ${PLONE_URL}/++add++Trabalho

a Trabalho 'My Trabalho'
  Create content  type=Trabalho  id=my-trabalho  title=My Trabalho

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Trabalho view
  Go To  ${PLONE_URL}/my-trabalho
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Trabalho with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Trabalho title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
