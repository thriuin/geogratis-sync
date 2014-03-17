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
    presentation_form = ''
    digital_object_identifier = ''
    geographic_region = []
    data_series_issue_identification = ''
    data_series_issue_identification_fra = ''
    browse_graphic_url = ''
    topic_category = []
    subject = []
    state = ''
    resources = []

    def __init__(self):
        self.resources.append(MetadataResourcesModel())

    def equals(self, other):
        is_equal = True
        if self.id != other.id or \
            self.url != other.id or \
            self.url_fra != other.url_fra or \
            self.title != other.title or \
            self.title_fra != other.title_fra or \
            self.notes != other.notes or \
            self.notes_fra != other.notes_fra or \
            self.date_modified != other.date_modified or \
            self.data_series_name != other.data_series_name or \
            self.data_series_name_fra != other.data_series_name_fra or \
            self.spatial != other.spatial or \
            self.presentation_form != other.presentation_form or \
            self.digital_object_identifier != other.digital_object_identifier or \
            self.data_series_issue_identification != other.data_series_issue_identification or \
            self.data_series_issue_identification_fra != other.data_series_issue_identification_fra or \
            self.browse_graphic_url != other.browse_graphic_url or \
            self.state != other.state:
                is_equal = False
        else:
            if len(self.keywords) == len(other.keywords):
                if not compare_list(self.keywords, other.keywords):
                    is_equal = False
            else:
                is_equal = False

            if len(self.keywords_fra) == len(other.keywords_fra):
                if not compare_list(self.keywords_fra, other.keywords_fra):
                    is_equal = False
            else:
                is_equal = False

            if len(self.geographic_region) == len(other.geographic_region):
                if not compare_list(self.geographic_region, other.geographic_region):
                    is_equal = False
            else:
                is_equal = False

            if len(self.topic_category) == len(other.topic_category):
                if not compare_list(self.topic_category, other.topic_category):
                    is_equal = False
            else:
                is_equal = False

            if len(self.subject) == len(other.subject):
                if not compare_list(self.subject, other.subject):
                    is_equal = False
            else:
                is_equal = False

            if len(self.resources) == len(other.resources):
                for i in range(0, len(self.resources) - 1):
                    if not self.resources[i].equals(other.resources[i]):
                        is_equal = False
                        break
            else:
                is_equal = False

        return is_equal

    def compare(self, other):
        diff_list = []
        if self.id != other.id:
            diff_list.append(u"ID: \tSource [{0}], \tOther [{1}]".format(self.id, other.id))
        if self.url!= other.url:
            diff_list.append(u"URL: \tSource [{0}], \tOther [{1}]".format(self.url, other.url))
        if self.url_fra != other.url_fra:
            diff_list.append(u"URL (FR): \tSource [{0}], \tOther [{1}]".format(self.url_fra, other.url_fra))
        if self.title != other.title:
            diff_list.append(u"Title: \tSource [{0}], \tOther [{1}]".format(self.title, other.title))
        if self.title_fra != other.title_fra:
            diff_list.append(u"Title (FR): \tSource [{0}], \tOther [{1}]".format(self.title_fra, other.title_fra))
        if self.notes != other.notes:
            diff_list.append(u"Notes: \tSource [{0}], \tOther [{1}]".format(self.notes, other.notes))
        if self.notes_fra != other.notes_fra:
            diff_list.append(u"Notes (FR): \tSource [{0}], \tOther [{1}]".format(self.notes_fra, other.notes_fra))
        if self.date_modified != other.date_modified:
            diff_list.append(u"Date: \tSource [{0}], \tOther [{1}]".format(self.date_modified, other.date_modified))
        if self.data_series_name != other.data_series_name:
            diff_list.append(u"DSN: \tSource [{0}], \tOther [{1}]".format(self.data_series_name,
                                                                         other.data_series_name))
        if self.data_series_name_fra != other.data_series_name_fra:
            diff_list.append(u"DSN (FR): \tSource [{0}], \tOther [{1}]".format(self.data_series_name_fra,
                                                                              other.data_series_name_fra))
        if self.spatial != other.spatial:
            diff_list.append(u"Spatial: \tSource [{0}], \tOther [{1}]".format(self.spatial, other.spatial))
        if self.presentation_form != other.presentation_form:
            diff_list.append(u"PForm: \tSource [{0}], \tOther [{1}]".format(self.presentation_form,
                                                                           other.presentation_form))
        if self.digital_object_identifier != other.digital_object_identifier:
            diff_list.append(u"DOI: \tSource [{0}], \tOther [{1}]".format(self.digital_object_identifier,
                                                                         other.digital_object_identifier))
        if self.data_series_issue_identification != other.data_series_issue_identification:
            diff_list.append(u"DSII: \tSource [{0}], \tOther [{1}]".format(self.data_series_issue_identification,
                                                                          other.data_series_issue_identification))
        if self.data_series_issue_identification_fra != other.data_series_issue_identification_fra :
            diff_list.append(u"DSII (FR): \tSource [{0}], \tOther [{1}]".format(
                self.data_series_issue_identification_fra, other.data_series_issue_identification_fra))
        if self.browse_graphic_url != other.browse_graphic_url:
            diff_list.append(u"Graphic: \tSource [{0}], \tOther [{1}]".format(self.browse_graphic_url,
                                                                             other.browse_graphic_url))
        if self.state != other.state:
            diff_list.append(u"State: \tSource [{0}], \tOther [{1}]".format(self.state, other.state))
            
        if len(self.keywords) != len(other.keywords):
            diff_list.append(u"Keywords: \tCount {0}, \tCount Other {1}".format(len(self.keywords),
                                                                                          len(other.keywords)))
        if len(self.keywords_fra) != len(other.keywords_fra):
            diff_list.append(u"Keywords (FR): \tCount {0}, \tCount Other {1}".format(len(self.keywords_fra),
                                                                                          len(other.keywords_fra)))
        if len(self.geographic_region) != len(other.geographic_region):
            diff_list.append(u"Regions: \tCount {0}, \tCount Other {1}".format(len(self.geographic_region),
                                                                                          len(other.geographic_region)))
        if len(self.topic_category) != len(other.topic_category):
            diff_list.append(u"Topics: \tCount {0}, \tCount Other {1}".format(len(self.topic_category),
                                                                                          len(other.topic_category)))
        if len(self.subject) != len(other.subject):
            diff_list.append(u"Subjects: \tCount {0}, \tCount Other {1}".format(len(self.subject),
                                                                                          len(other.subject)))
        if len(self.resources) != len(other.resources):
            diff_list.append(u"Resources: \tCount {0}, \tCount Other {1}".format(len(self.resources),
                                                                                          len(other.resources)))
        return diff_list


def compare_list(source, other):
    list_equal = True
    for i in range(0, len(source.keywords) - 1):
        if source.keywords[i] != other.keywords[i]:
            is_equal = False
            break
    return list_equal


class MetadataResourcesModel():
    name = ''
    name_fra = ''
    url = ''
    format = ''
    resource_type = ''
    size = 0
    language = ''

    def __init__(self, res_name='', res_name_fra='', res_url='', res_format='', res_type='file', res_size=0,
                 res_language='eng; CAN | fra; CAN'):
        """

        :type res_format: str
        """
        self.name = res_name
        self.name_fra = res_name_fra
        self.url = res_url
        self.format = res_format
        self.resource_type = res_type
        self.size = res_size
        self.language = res_language

    def equals(self, other):

        if self.name != other.name or \
            self.name_fra != other.name_fra or \
            self.url != other.url or \
            self.format != other.format or \
            self.resource_type != other.resource_type or \
            self.size != other.size or \
            self.language != other.language:
            return False
        else:
            return True

    def compare(self, other):

        diff_list = []
        if self.name != other.name:
            diff_list.append(u"Name: \tSource [{0}], \tOther [{1}]".format(self.name, other.name))
        if self.name_fra != other.name_fra:
            diff_list.append(u"Name (FR): \tSource [{0}], \tOther [{1}]".format(self.name_fra, other.name_fra))
        if self.url != other.url:
            diff_list.append(u"URL: \tSource [{0}], \tOther [{1}]".format(self.url, other.url))
        if self.format != other.format:
            diff_list.append(u"Form: \tSource [{0}], \tOther [{1}]".format(self.format, other.format))
        if self.resource_type != other.resource_type:
            diff_list.append(u"Type: \tSource [{0}], \tOther [{1}]".format(self.resource_type, other.resource_type))
        if self.size != other.size:
            diff_list.append(u"Size: \tSource [{0}], \tOther [{1}]".format(self.size, other.size))
        if self.language != other.language:
            diff_list.append(u"Language: \tSource [{0}], \tOther [{1}]".format(self.language, other.language))
        return diff_list

