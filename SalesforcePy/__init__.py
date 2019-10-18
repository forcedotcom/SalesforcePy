import warnings

# the following lines are intended to provide backwards compatibility and should be removed once the SalesforcePy
# package has been removed
import salesforce
from salesforce import name, client, LoginException  # noqa: F401

sfdc = salesforce.sfdc
chatter = salesforce.chatter
commons = salesforce.commons
jobs = salesforce.jobs
wave = salesforce.wave

warnings.warn(
    'The SalesorcePy package has been deprecated in favor of salesforce. '
    'Please update your imports as required as SalesforcePy will be '
    'removed in a future version.'
)
