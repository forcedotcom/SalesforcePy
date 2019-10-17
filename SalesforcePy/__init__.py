import warnings
from salesforce import name, client, LoginException

warnings.warn(
    'The SalesorcePy package has been deprecated in favor of salesfoce. '
    'Please update your imports as required as SalesforcePy will be '
    'removed in a future version.'
)
