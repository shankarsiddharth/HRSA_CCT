->transition1

=== transition1 ===
YOU: "Hello, Doctor." #Audio_1 #Player
MEDICAL STUDENT: "Hello, Doctor." #Audio_2 #MedicalStudent
YOU: "Let's begin" #Audio_3 #Player
MEDICAL STUDENT: "The patient is in the other room." #Audio_4 #MedicalStudent
MEDICAL STUDENT: "The patient does not feel well." #Audio_5 #MedicalStudent
MEDICAL STUDENT: "The patient is also sad." #Audio_6 #MedicalStudent
-> intervention1

=== intervention1 ===
MEDICAL STUDENT: "I'm going to ask you a question." #Audio_7 #MedicalStudent

*[A.	This is the first option. `This is where the feedback about this option is added. `MedicalStudent `Emotion `CORRECT] 
YOU:	"This is the first option." #Audio_8 #Player
-> transition2

*[B.	This is the second option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the second option." #Audio_9 #Player
-> transition2

*[C.	This is the third option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the third option." #Audio_10 #Player
-> transition2

*[D.	This is the fourth option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the fourth option." #Audio_11 #Player
-> transition2

=== transition2 ===
YOU: "I react to the response selected." #Audio_12 #Player

MEDICAL STUDENT: "Thank you. That was a good reaction." #Audio_13 #MedicalStudent

-> intervention2

=== intervention2 ===
MEDICAL STUDENT: "I'm going to ask you a second question." #Audio_14 #MedicalStudent

*[A.	This is the first option. `This is where the feedback about this option is added. `MedicalStudent `Emotion `CORRECT] 
YOU:	"This is the first option." #Audio_15 #Player
-> transition3

*[B.	This is the second option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the second option." #Audio_16 #Player
-> transition3

*[C.	This is the third option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the third option." #Audio_17 #Player
-> transition3

*[D.	This is the fourth option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the fourth option." #Audio_18 #Player
-> transition3

=== transition3 ===
YOU: "I am reacting to the response selected." #Audio_19 #Player

-> intervention3

=== intervention3 ===
MEDICAL STUDENT: "This is my third question for you." #Audio_20 #MedicalStudent

*[A.	This is the first option. `This is where the feedback about this option is added. `MedicalStudent `Emotion `CORRECT] 
YOU:	"This is the first option." #Audio_21 #Player
-> transition4

*[B.	This is the second option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the second option." #Audio_22 #Player
-> transition4

*[C.	This is the third option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the third option." #Audio_23 #Player
-> transition4

*[D.	This is the fourth option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the fourth option." #Audio_24 #Player
-> transition4

=== transition4 ===
YOU: "I will now react to the response selected." #Audio_25 #Player

-> intervention4

=== intervention4 ===
MEDICAL STUDENT: "This is the fourth and final question I have."#Audio_26 #MedicalStudent

*[A.	This is the first option. `This is where the feedback about this option is added. `MedicalStudent `Emotion `CORRECT] 
YOU:	"This is the first option." #Audio_27 #Player
-> endsection

*[B.	This is the second option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the second option." #Audio_28 #Player
-> endsection

*[C.	This is the third option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the third option." #Audio_29 #Player
-> endsection

*[D.	This is the fourth option. `This is where the feedback about this option is added. `MedicalStudent `Emotion] 
YOU:	"This is the fourth option." #Audio_30 #Player
-> endsection

=== endsection ===
You: "This is the end of this section." #Audio_31 #Player
Medical Student: "The next room will have you talking to the patient." #Audio_32 #MedicalStudent
You: "Great." #Audio_33 #Player
->END
