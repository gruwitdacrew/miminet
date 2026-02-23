from quiz.entity.entity import Section
from .base import BaseActionHandler, BaseResultSender
from flask import make_response, redirect, url_for
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.lineitem import LineItem

class SectionCreationHandler(BaseActionHandler):
    
    def _process(self):       
        return redirect(url_for("create_question_endpoint"))


class SectionSender(BaseResultSender[Section]):
    
    def _send(self, section: Section) -> bool:

        deep_link = self.message_launch.get_deep_link()

        line_item = LineItem()\
            .set_tag('score')\
            .set_score_maximum(section.max_score)

        resource = DeepLinkResource()\
            .set_title(section.name)\
            .set_url("http://127.0.0.1/lti/launch")\
            .set_lineitem(line_item)\
            .set_custom_params({"section_id": f"{section.id}"})
    
        return deep_link.output_response_form([resource])