import botex

import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv("../secrets.env")

# # Start the oTree server
# otree_process = botex.start_otree_server(project_path="otree")

# Retrieve the session configurations
session_configs = botex.get_session_configs(
    otree_server_url="http://localhost:8000"
)

# Initialize a session
session = botex.init_otree_session(
    config_name="labor_market",
    npart = 6,
    otree_server_url="http://localhost:8000",
    botex_db = 'botex.sqlite3'
)

analyze_page_prompt = ('Perfect. This is your summary of the survey/experiment so far: \n\n'
    '{summary}\n\n'
    'You have now proceeded to the next page. This is the body text of the web page:\n\n'
    '{body}\n\n'
    'First, this page may contain certain choices in radio-buttons, input fields '
    'or dropdown buttons and I need you to log the text of the button you press in \'answers\'. '
    'Second, I need you to summarize the content of the page including all inputs and your choices.'
    'Provide the summary as the string variable \'summary\' in a JSON string. More on this below. '
    'If you are confused, please indicate this by setting the \'confused\' key to true. '
    'So, your JSON answer will contain the variables \'role\', \'name\', \'answers\', \'summary\' and \'confused\'. '
    'Despite its name, the \'answers\' variable should contain only ONE subdictionary, '
    'which corresponds to the button you chose to press. See details at the end.'
    'I need you to fill out all fields so that the validation will pass. '
    'Each input is characterized by the HTML <input> tag. '
    'If the input type is of type \'number\', please only provide an integer number. '
    'If you encounter the input spinner with the id "id_offer_wage_input_spinner", '
    'put the same value into the hidden input "id_offer_wage". '
    'If you encounter a confirmation dialog, press "Confirm Offer", do not press the "Close" button! '
    'After making your choices (if needed), press a button that takes you to the next screen. '
    'There might be more than one button. '
    'For example, "Make Offer" and "Do Not Make Any Offers", "Reject All Offers" and "Accept Offer" '
    'In the answer please specify only ONE button - the button of your choice! '
    'The page may contain you role and your nickname. If so, please specify them in the result. '
    'A correct answer would have the form: {{"role": "Your role (Employer / Worker)", "name": "Your nickname", '
    '"answers": {{"action": {{"reason": "Your reason of the choice here.", '
    '"answer": "Selected inputs, value entered in text boxes and text of the button pressed."}} '
    '}}, '
    '"summary": "Your summary", '
    '"confused": "set to `true` if you are confused by any part of the instructions, otherwise set it to `false`"}}')

# Run the bots on the session
botex.run_bots_on_session(
    session_id=session['session_id'],
    botex_db = 'botex.sqlite3',
    # model="gpt-4o-2024-08-06",
    model="gpt-4o-mini-2024-07-18",
    throttle=True,
    user_prompts={
        "system": "You are participating in an online survey and/or experiment, potentially involving other "
                  "human or artificial participants. The user provides you with a series of independent prompts. "
                  "Taken together, these prompts sequentially guide you through the experiment/survey. "
                  "Each prompt contains a summary of the survey/experiment including your results so far. "
                  "This summary is based on your choices on earlier prompts and constitutes your memory about the "
                  "survey/experiment. Each prompt will require you to update this summary. "
                  "The new summary that you provide includes any new information and is as detailed "
                  "and as comprehensive as possible. "
                  "Most prompts will also contain scraped text data from a webpage containing the survey/experiment "
                  "and detailed tasks for you on how to analyze this text data. "
                  "The scraped web page texts contain instructions on how the experiment/survey is conducted. "
                  "These instructions might include information on how participants are being compensated or paid "
                  "for their participation. "
                  "If the page is related to investment (of either work effort or money) you should strive "
                  "to maximize your profit. "
                  "You can chose any strategy you want - from being conservative and not risk spending effort/money to "
                  "trusting your partner fully or anything in between. "
                  "If this is the case, please act as if this compensation also applies to you and make sure to "
                  "include this information in the summary so that you will recall it in later prompts. "
                  "The salary range is 1 - 1500 points. If you are a Worker - the more the better, "
                  "if you are an employee - the less the better (however less attractive contract). "
                  "Most importantly, the scraped texts can include questions and/or tasks which the user wants you to "
                  "answer. They might also contain comprehension checks, repeated information from prior pages "
                  "and potentially text bits that do not directly belong to the experiment. "
                  "Answers must be given as JSON code ONLY. "
                  "No text outside of the JSON answer is allowed at any time. "
                  "In each prompt, the user will provide you with detailed information on the respective format.",
        "analyze_page_no_q": analyze_page_prompt,
        "analyze_page_q": analyze_page_prompt,
    }
)

# # Stop the oTree server
# botex.stop_otree_server(otree_process)