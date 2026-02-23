from quiz.entity.entity import QuizSession, SessionQuestion
from .base import BaseActionHandler, BaseResultSender
from flask import redirect, session, url_for
from datetime import datetime
from pylti1p3.grade import Grade

class SectionRetrievalHandler(BaseActionHandler):

    def _process(self):
        custom = self.launch_data.get("https://purl.imsglobal.org/spec/lti/claim/custom")
        
        section_id = custom.get('section_id')

        return redirect(url_for('get_section_endpoint', section=section_id))
    

class QuizSessionSender(BaseResultSender[SessionQuestion]):
    
    def _send(self, session_question: SessionQuestion) -> bool:
        if not self.message_launch.has_ags(): raise Exception("LTI launch doesn't have AGS permissions")
        
        sub = self.launch_data.get('sub')
        timestamp = datetime.now().isoformat() + 'Z'
        
        grades = self.message_launch.get_ags()
        
        grade = Grade() \
            .set_user_id(sub) \
            .set_timestamp(timestamp) \
            .set_activity_progress("Completed") \
            .set_grading_progress("Pending") \
            .set_extra_claims({"quiz_session_id": f"{session_question.quiz_session_id}"})
        
        return grades.put_grade(grade)


class QuizSessionScoreSender(BaseResultSender[SessionQuestion]):
    
    def _send(self, session_question: SessionQuestion) -> bool:
        if not self.message_launch.has_ags(): raise Exception("LTI launch doesn't have AGS permissions")
        
        sub = self.launch_data.get('sub')
        timestamp = datetime.now().isoformat() + 'Z'
        
        grades = self.message_launch.get_ags()
        
        grade = Grade() \
            .set_user_id(sub) \
            .set_timestamp(timestamp) \
            .set_activity_progress("Completed") \
            .set_grading_progress("FullyGraded") \
            .set_score_given(session_question.score) \
            .set_extra_claims({"quiz_session_id": f"{session_question.quiz_session_id}"})
        
        return grades.put_grade(grade)
