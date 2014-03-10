__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'


class MetadataDatasetModel():

    id = ''
    url = ''
    url_fra = ''
    title = ''
    title_fra = ''
    notes = ''
    notes_fra = ''
    date_modified = ''
    data_series_name = ''
    data_series_name_fra = ''
    keywords = []
    keywords_fra = []
    spatial = ''
    presentation_from = ''
    digital_object_identifier = ''
    geographic_region = []
    data_series_issue_identification = ''
    presentation_form = ''
    browse_graphic_url = ''
    topic_category = []
    state = ''
    resources = []

    def __init__(self):
        self.resources.append(MetadataResourcesModel())


class MetadataResourcesModel():
    name = ''
    name_fra = ''
    url = ''
    format = ''

    def __init__(self, res_name='', res_name_fra='', res_url='', res_format=''):
        self.name = res_name
        self.name_fra = res_name_fra
        self.url = res_url
        self.format = res_format
