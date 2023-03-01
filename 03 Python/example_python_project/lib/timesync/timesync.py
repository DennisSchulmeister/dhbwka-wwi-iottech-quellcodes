
import pytz
import ntplib
from datetime import datetime,timezone

class TimeSyncService():


    def get_iso_timestamp_local(self) -> str:
        return datetime.now().astimezone().isoformat(timespec='milliseconds')

    def get_epoc_timestamp_from_iso(self, iso_timestamp) -> float:
        return datetime.fromisoformat(iso_timestamp).timestamp()

    def get_ntp_timestamp(self) -> str:
        client = ntplib.NTPClient()
        response = client.request('ptbtime1.ptb.de') # Request an die Physikalisch Technische Bundesanstalt (PTB) in Braunschweig
        response_timestamp = response.tx_time # Zeitstempel unformatiert als float

        timestamp_utc_from_ntp = datetime.fromtimestamp(response_timestamp, timezone.utc).isoformat(timespec='milliseconds') # UTC
        timestamp_zulu = timestamp_utc_from_ntp[:-6] + 'Z' # ZULU
        timestamp_local = datetime.fromtimestamp(response_timestamp, pytz.timezone('Europe/Berlin')).isoformat(timespec='milliseconds') # +2 Stunden Offset
        print(f'UTC: {timestamp_utc_from_ntp}\nZulu: {timestamp_zulu}\nLocal: {timestamp_local}')
        return timestamp_local
