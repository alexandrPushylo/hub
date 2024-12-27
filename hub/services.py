from typing import Type

from django.template.defaultfilters import title

from hub.models import Rent, ColdWater, HotWater, Electricity
import hub.utilites as U


from logger import getLogger
log = getLogger(__name__)


