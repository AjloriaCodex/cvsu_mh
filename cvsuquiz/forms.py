from django import forms
from .models import AnswerEasyCspear

class QuizForm(forms.Form):
    CHOICES_Q1 = [
        ('1', 'A. The branch of mechanics that studies the motion of a body or a system of bodies without consideration given to its mass or the forces acting on it.'),
        ('2', 'B. The branch of mechanics that is concerned with the effects of forces on the motion of a body or system of bodies, especially of forces that do not originate within the system itself.'),
        ('3', 'C. The study of the motion of a body or a system of bodies with consideration given to its mass or the forces acting on it.'),
        ('4', 'D. If the forces acting upon an object are balanced, then the acceleration of that object will be 0 m/s/s.'),
    ]
    CHOICES_Q2 = [
        ('1', 'A. Competence.'),
        ('2', 'B. Relatedness.'),
        ('3', 'C. Autonomy.'),
        ('4', 'D. Intrinsic Motivation.'),
    ]
    CHOICES_Q3 = [
        ('1', 'A. Ergogenic aids alone are sufficient to improve athletic performance, with no need for nutritional support.'),
        ('2', 'B. Proper nutrition supports exercise recovery, but ergogenic aids can provide a significant boost in endurance, strength, and recovery beyond what nutrition alone can offer.'),
        ('3', 'C. Proper nutrition and hydration are the most important factors for athletic performance, and ergogenic aids are only useful for professional athletes in extreme conditions.'),
        ('4', 'D.  Ergogenic aids and proper nutrition complement each other; both can improve performance, but should be tailored to the individuals sport, body composition, and energy requirements.'),
    ]
    
    answer_q1 = forms.ChoiceField(
        choices=CHOICES_Q1,
        widget=forms.RadioSelect,
        label="Whats is the definiton of Kinematics?"
    )

    answer_q2 = forms.ChoiceField(
        choices=CHOICES_Q2,
        widget=forms.RadioSelect,
        label="Which of the following constructs within the Self-Determination Theory (SDT) is primarily focused on the psychological need for autonomy and the desire to make choices that align with one's interests and values?"
    )
    answer_q3 = forms.ChoiceField(
        choices=CHOICES_Q3,
        widget=forms.RadioSelect,
        label=" Which of the following statements best describes the role of ergogenic aids and proper nutrition in enhancing athletic performance?"
    )