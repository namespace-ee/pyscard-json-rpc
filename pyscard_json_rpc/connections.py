from collections import defaultdict
from typing import Dict, Tuple
from uuid import UUID

from smartcard.CardConnection import CardConnection

card_connections: Dict[Tuple[str, int], Dict[UUID, CardConnection]] = defaultdict(dict)
