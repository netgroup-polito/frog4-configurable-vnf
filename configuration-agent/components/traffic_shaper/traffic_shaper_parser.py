from components.traffic_shaper.traffic_shaper_model import TrafficShaper

class TrafficShaperParser():

    def parse_configuration(self, json_configuration):
        return json_configuration['configuration']

    def parse_interface_to_control(self, json_configuration):

        interface_name = json_configuration['interface_to_control']
        return interface_name

    def parse_traffic_shaper_configuration(self, json_configuration):

        download_limit = None
        if 'download_limit' in json_configuration:
            download_limit = json_configuration['download_limit']

        upload_limit = None
        if 'upload_limit' in json_configuration:
            upload_limit = json_configuration['upload_limit']

        return TrafficShaper(download_limit=download_limit,
                             upload_limit=upload_limit)

    def get_traffic_shaper_dict(self, traffic_shaper):

        traffic_shaper_dict = {}

        traffic_shaper_dict['interface_to_control'] = traffic_shaper.interface_name

        if traffic_shaper.download_limit is not None:
            traffic_shaper_dict['download_limit'] = traffic_shaper.download_limit

        if traffic_shaper.upload_limit is not None:
            traffic_shaper_dict['upload_limit'] = traffic_shaper.upload_limit

        return traffic_shaper_dict