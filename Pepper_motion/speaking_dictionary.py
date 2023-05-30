sentence_generation={
    "express_excitement":"I am very excited to work with you",
    "express_enthusiasm_for_the_last_achieved_action":"We are doing a really good job!",
    "express_enthusiasm_for_the_next_future_work":"Continuing so we will build a beautiful tower",
    "chat":"behavior1",
    "say_to_not_distract":"Please do not get distracted",
    "say_to_pay_attention":"Please be careful not to make mistakes",
    "say_to_focus_on_future_work":"We need to focus so we can finish our task as well",
    "say_they_have_a_goal_to_achieve":"We have a job to do, we have to focus only on this",
    "chat_unsc":"behavior1",
    "say_no_matter_about_the_task":"Don't worry if you make a mistake, it can happen",
    "ask_if_human_need_help":"Do yo need any help?",
    "say_that_you_know_it_is_a_difficult_task":"I know it is hard work, I am so sorry",
    "say_to_not_matter_if_an_error_occur":"Do not worry about making mistakes, we will find a solution",
    "say_you_are_sorry_for_the_fatigue":"I am so sorry to tire you out",
    "say_the_human_he_is_doing_a_good_work":"You are working very well, keep it up",
    "say_that_you_would_perform_an_action_differently":"I would have behaved differently than you, surely I would have achieved better results",
    "say_the_human_should_work_better":"You could work better and be faster",
    "say_to_work_more_fast":"Hurry up or we will never finish",
    "speak_about_assembly_room":"behavior2",
    "speak_about_production_room":"behavior3",
    "ask_pick_the_block_voice":"behavior4",
    "ask_pick_the_block_tablet":"behavior5",
    "ask_assembly_block_voice_rude":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet_rude":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":"behavior10",
    "say_goodbye_assembly_room":"behavior10"
}

behavior1=["Make me a question in italian about ","Answer to * knowing that we are speaking about +"]
behavior2=["Hello my name is Pepper","Finally you arrived to help me","I have called you because I have to build a tower of block and I need your help","Now I will explain your task","Every time I bring you a block you will have to assemble it","Let's go to work"]
behavior3=["Hello my name is Pepper","Finally you arrived to help me","I have called you because I have to build a tower of block and I need your help","Now I will explain your task","Every time I ask to you you will bring me a block","The block must be of the specific color that I ask", "Let's go to work"]
behavior4=["Hand me a * block","Bring me a * block", "Now bring me a * block", "Get me again a * block"]
behavior6=["Pick this * block and put it to build the tower","Take now this * block and put it upon the green onyelloweprevious one","Take now this * block", "Pick now the * block and put it on the tower","Pick now this * block"]
behavior10=["We have finished to build the whole tower", "Your help has been fundamental", "Our collaboration has been successful", "The next time I need help I will ask you again","Goodbye and see you soon"]

sentence=["Rewrite in a "," way in "]

behaviors={
    "behavior1":behavior1,
    "behavior2":behavior2,
    "behavior3":behavior3,
    "behavior4":behavior4,
    "behavior5":behavior4,
    "behavior6":behavior6,
    "behavior7":behavior6,
    "behavior8":behavior6,
    "behavior9":behavior6,
    "behavior10":behavior10,
    "behavior11":behavior10,
}

modality={
    "Extrovert":"extrovert",
    "Introvert":"introvert",
    "Conscientious":"conscientous",
    "Unscrupulous":"distracted",
    "Agreeable":"agreeable",
    "Disagreeable":"disagreeable"
}