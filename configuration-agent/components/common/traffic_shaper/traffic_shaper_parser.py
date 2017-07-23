from components.common.traffic_shaper.traffic_shaper_model import TrafficShaper

class TrafficShaperParser():

    def parse_interface_to_control(self, json_configuration):

        interface_id = json_configuration['interface_to_control']
        return interface_id

    def parse_traffic_shaper_configuration(self, json_configuration):

        download_limit = None
        if 'download_limit' in json_configuration:
            download_limit = json_configuration['download_limit']

        upload_limit = None
        if 'upload_limit' in json_configuration:
            upload_limit = json_configuration['upload_limit']

        return TrafficShaper(download_limit=download_limit,
                             upload_limit=upload_limit)