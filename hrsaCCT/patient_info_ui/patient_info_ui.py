import json
import dearpygui.dearpygui as dpg

# DearPyGUI's Viewport Constants
VIEWPORT_WIDTH = 900
VIEWPORT_HEIGHT = 900  # 700

# GUI Element Tags
HRSA_CCT_TOOL: str = "HRSA_CCT_TOOL"

problem_num = 0
sdoh_problem_num = 0
medication_num = 0
allergy_num = 0
family_health_history_num = 0
patient_info = {}

patient_info_saved = False

problem_tab = None
sdoh_problem_tab = None
medication_tab = None
family_health_history_tab = None
allergy_tab = None

# GUI Element Tags
PIU_PATIENT_FIRST_NAME_INPUT_TEXT: str = "PIU_PATIENT_FIRST_NAME_INPUT_TEXT"
PIU_PATIENT_LAST_NAME_INPUT_TEXT: str = "PIU_PATIENT_LAST_NAME_INPUT_TEXT"
PIU_PATIENT_MIDDLE_NAME_INPUT_TEXT: str = "PIU_PATIENT_MIDDLE_NAME_INPUT_TEXT"
PIU_PATIENT_SUFFIX_INPUT_TEXT: str = "PIU_PATIENT_SUFFIX_INPUT_TEXT"
PIU_PATIENT_PREVIOUS_NAME_INPUT_TEXT: str = "PIU_PATIENT_PREVIOUS_NAME_INPUT_TEXT"
PIU_PATIENT_DATE_OF_BIRTH_INPUT_TEXT: str = "PIU_PATIENT_DATE_OF_BIRTH_INPUT_TEXT"
PIU_PATIENT_DATE_OF_DEATH_INPUT_TEXT: str = "PIU_PATIENT_DATE_OF_DEATH_INPUT_TEXT"
PIU_PATIENT_AGE_INPUT_TEXT: str = "PIU_PATIENT_AGE_INPUT_TEXT"
PIU_PATIENT_RACE_INPUT_TEXT: str = "PIU_PATIENT_RACE_INPUT_TEXT"
PIU_PATIENT_ETHNICITY_INPUT_TEXT: str = "PIU_PATIENT_ETHNICITY_INPUT_TEXT"
PIU_PATIENT_TRIBAL_AFFILIATION_INPUT_TEXT: str = "PIU_PATIENT_TRIBAL_AFFILIATION_INPUT_TEXT"
PIU_PATIENT_SEX_ASSIGNED_AT_BIRTH_INPUT_TEXT: str = "PIU_PATIENT_SEX_ASSIGNED_AT_BIRTH_INPUT_TEXT"
PIU_PATIENT_SEXUAL_ORIENTATION_INPUT_TEXT: str = "PIU_PATIENT_SEXUAL_ORIENTATION_INPUT_TEXT"
PIU_PATIENT_GENDER_IDENTITY_INPUT_TEXT: str = "PIU_PATIENT_GENDER_IDENTITY_INPUT_TEXT"
PIU_PATIENT_PREFERRED_LANGUAGE_INPUT_TEXT: str = "PIU_PATIENT_PREFERRED_LANGUAGE_INPUT_TEXT"
PIU_PATIENT_CURRENT_ADDRESS_INPUT_TEXT: str = "PIU_PATIENT_CURRENT_ADDRESS_INPUT_TEXT"
PIU_PATIENT_PREVIOUS_ADDRESS_INPUT_TEXT: str = "PIU_PATIENT_PREVIOUS_ADDRESS_INPUT_TEXT"
PIU_PATIENT_PHONE_NUMBER_INPUT_TEXT: str = "PIU_PATIENT_PHONE_NUMBER_INPUT_TEXT"
PIU_PATIENT_PHONE_NUMBER_TYPE_INPUT_TEXT: str = "PIU_PATIENT_PHONE_NUMBER_TYPE_INPUT_TEXT"
PIU_PATIENT_EMAIL_ADDRESS_INPUT_TEXT: str = "PIU_PATIENT_EMAIL_ADDRESS_INPUT_TEXT"
PIU_PATIENT_RELATED_PERSONS_NAME_INPUT_TEXT: str = "PIU_PATIENT_RELATED_PERSONS_NAME_INPUT_TEXT"
PIU_PATIENT_RELATED_PERSONS_RELATIONSHIP_INPUT_TEXT: str = "PIU_PATIENT_RELATED_PERSONS_RELATIONSHIP_INPUT_TEXT"
PIU_PATIENT_OCCUPATION_INPUT_TEXT: str = "PIU_PATIENT_OCCUPATION_INPUT_TEXT"
PIU_PATIENT_OCCUPATION_HISTORY_INPUT_TEXT: str = "PIU_PATIENT_OCCUPATION_HISTORY_INPUT_TEXT"
PIU_PATIENT_CHIEF_COMPLAINT_INPUT_TEXT: str = "PIU_PATIENT_CHIEF_COMPLAINT_INPUT_TEXT"
PIU_PATIENT_INSURANCE_INPUT_TEXT: str = "PIU_PATIENT_INSURANCE_INPUT_TEXT"


def generate_tag(key, sub_key, index=0):
    sub_key = sub_key.upper()
    if key == "patient_demographics":
        return "PIU_PATIENT_" + sub_key + "_INPUT_TEXT"
    elif key == "vital_signs" or key == "social_health_history":
        return "PIU_" + sub_key + "_INPUT_TEXT"
    elif key == "problems":
        return "PIU_PROBLEM_" + str(index) + "_" + sub_key + "_INPUT_TEXT"
    elif key == "sdoh_problems_health_concerns":
        return "PIU_SDOH_PROBLEM_" + str(index) + "_" + sub_key + "_INPUT_TEXT"
    elif key == "medications":
        return "PIU_MEDICATION_" + str(index) + "_NAME_INPUT_TEXT"
    elif key == "family_health_history":
        return "PIU_FAMILY_HEALTH_HISTORY_" + str(index) + "_INPUT_TEXT"
    elif key == "allergies_intolerances":
        return "PIU_ALLERGY_" + str(index) + "_" + sub_key + "_INPUT_TEXT"
    return ""


def load_patient_info(key, sub_dict):
    global problem_tab, sdoh_problem_tab, medication_tab, family_health_history_tab
    global patient_info
    global sdoh_problem_num, problem_num, medication_num, family_health_history_num, allergy_num
    if key == "problems":
        num = len(sub_dict["problems"])
        while num > problem_num:
            _callback_add_problem("", "", user_data=problem_tab)

        while problem_num > num:
            _callback_delete_problem("", "", user_data=problem_tab)

        index = 0
        # print("sub_dict => ", sub_dict[key])
        while index < num:
            item = sub_dict[key][index]
            dpg.set_value(generate_tag(
                "problems", "problem", index + 1), item["problem"])
            dpg.set_value(generate_tag(
                "problems", "date_of_diagnosis", index + 1), item["date_of_diagnosis"])
            dpg.set_value(generate_tag(
                "problems", "date_of_resolution", index + 1), item["date_of_resolution"])
            index += 1
        patient_info["problems"]["problems"] = patient_info["problems"]["problems"][:problem_num]

        num = len(sub_dict["sdoh_problems_health_concerns"])
        while num > sdoh_problem_num:
            _callback_add_sdoh_problem(
                "", "", user_data=sdoh_problem_tab)
        while sdoh_problem_num > num:
            _callback_delete_sdoh_problem(
                "", "", user_data=sdoh_problem_tab)
        index = 0
        while index < num:
            item = sub_dict["sdoh_problems_health_concerns"][index]
            dpg.set_value(generate_tag(
                "sdoh_problems_health_concerns", "problem", index + 1), item["problem"])
            dpg.set_value(generate_tag(
                "sdoh_problems_health_concerns", "date_of_diagnosis", index + 1), item["date_of_diagnosis"])
            dpg.set_value(generate_tag(
                "sdoh_problems_health_concerns", "date_of_resolution", index + 1), item["date_of_resolution"])
            index += 1
        patient_info["problems"]["sdoh_problems_health_concerns"] = patient_info[
            "problems"]["sdoh_problems_health_concerns"][
            :sdoh_problem_num]
    elif key == "medications":
        num = len(sub_dict["medications"])
        while num > medication_num:
            _callback_add_medication(
                "", "", user_data=medication_tab)
        while medication_num > num:
            _callback_delete_medication(
                "", "", user_data=medication_tab)
        index = 0
        while index < num:
            item = sub_dict["medications"][index]
            dpg.set_value(generate_tag(
                "medications", "", index + 1), item)
            index += 1
        patient_info["medications"]["medications"] = patient_info["medications"]["medications"][:medication_num]
    elif key == "family_health_history":
        num = len(sub_dict["family_health_history"])
        while num > family_health_history_num:
            _callback_add_family_health_history(
                "", "", user_data=family_health_history_tab)
        while family_health_history_num > num:
            _callback_delete_family_health_history(
                "", "", user_data=family_health_history_tab)
        index = 0
        while index < num:
            # print(sub_dict["family_health_history"])
            item = sub_dict["family_health_history"][index]
            dpg.set_value(generate_tag(
                "family_health_history", "", index + 1), item)
            index += 1
        patient_info["family_health_history"]["family_health_history"] = patient_info[
            "family_health_history"][
            "family_health_history"][
            :family_health_history_num]
    elif key == "allergies_intolerances":
        num = len(sub_dict["substances"])
        while num > allergy_num:
            _callback_add_allergy("", "", user_data=allergy_tab)
        while allergy_num > num:
            _callback_delete_allergy(
                "", "", user_data=allergy_tab)
        index = 0
        while index < num:
            item = sub_dict["substances"][index]
            # print(item)
            dpg.set_value(generate_tag(
                "allergies_intolerances", "substance_medication", index + 1), item["substance_medication"])
            dpg.set_value(generate_tag(
                "allergies_intolerances", "substance_drug_class", index + 1), item["substance_drug_class"])
            dpg.set_value(generate_tag(
                "allergies_intolerances", "substance_reaction", index + 1), item["reaction"])
            index += 1
        patient_info["allergies_intolerances"]["substances"] = patient_info["allergies_intolerances"]["substances"][
            :allergy_num]
    else:
        for sub_key in sub_dict:
            tag = generate_tag(key, sub_key)
            # print(tag)
            if tag != "":
                dpg.set_value(tag, sub_dict[sub_key])


def _callback_load_patient_info_file(sender, app_data):
    global patient_info
    with open(app_data["file_path_name"]) as patient_info_json:
        patient_info = json.load(patient_info_json)

        for key in patient_info:
            # print(key, patient_info[key])
            load_patient_info(key, patient_info[key])


def _callback_save_patient_into_to_file(sender, app_data):
    global patient_info
    patient_info_json = json.dumps(patient_info, indent=4)

    with open(app_data["file_path_name"], "w") as outfile:
        outfile.write(patient_info_json)


def _callback_load_patient_info(sender, app_data, user_data):
    global patient_info_saved
    dpg.configure_item("PIU_OPEN_FILE_DIALOG", show=True)


def _callback_save_patient_info(sender, app_data, user_data):
    dpg.configure_item("PIU_SAVE_FILE_CONFIRM_WINDOW", show=False)
    dpg.show_item("PIU_SAVE_FILE_DIALOG")


def _callback_update_patient_demographics(sender, app_data, user_data):
    key = sender.replace("PIU_PATIENT_", "").replace(
        "_INPUT_TEXT", "").lower()
    patient_info["patient_demographics"][key] = app_data


def _call_update_problems(sender, app_data, user_data):
    index_key = sender.replace(
        "PIU_PROBLEM_", "").replace("_INPUT_TEXT", "")
    index = int(index_key.split("_")[0]) - 1
    key = index_key[2:].lower()
    patient_info["problems"]["problems"][index][key] = app_data


def _callback_add_problem(sender, app_data, user_data):
    global problem_num
    problem_num += 1
    # TODO
    # encapsulate into a struct
    problem = dict()
    problem["problem"] = ""
    problem["date_of_diagnosis"] = ""
    problem["date_of_resolution"] = ""
    dpg.add_text("Problem {0}: ".format(problem_num), tag="PIU_PROBLEM_{0}_LABEL_TEXT".format(problem_num),
                 parent=user_data, indent=20)
    dpg.add_input_text(tag="PIU_PROBLEM_{0}_PROBLEM_INPUT_TEXT".format(problem_num), label="Problem",
                       default_value="", parent=user_data, indent=20, callback=_call_update_problems)
    dpg.add_input_text(tag="PIU_PROBLEM_{0}_DATE_OF_DIAGNOSIS_INPUT_TEXT".format(problem_num),
                       label="Date of Diagnosis", default_value="", parent=user_data, indent=20,
                       callback=_call_update_problems)
    dpg.add_input_text(tag="PIU_PROBLEM_{0}_DATE_OF_RESOLUTION_INPUT_TEXT".format(problem_num),
                       label="Date of Resolution", default_value="", parent=user_data, indent=20,
                       callback=_call_update_problems)
    patient_info["problems"]["problems"].append(problem)


def _callback_delete_problem(sender, app_data, user_data):
    global problem_num
    if problem_num <= 0:
        return
    dpg.delete_item(
        "PIU_PROBLEM_{0}_LABEL_TEXT".format(problem_num))
    dpg.delete_item(
        "PIU_PROBLEM_{0}_PROBLEM_INPUT_TEXT".format(problem_num))
    dpg.delete_item(
        "PIU_PROBLEM_{0}_DATE_OF_DIAGNOSIS_INPUT_TEXT".format(problem_num))
    dpg.delete_item(
        "PIU_PROBLEM_{0}_DATE_OF_RESOLUTION_INPUT_TEXT".format(problem_num))
    problem_num -= 1
    patient_info["problems"]["problems"] = patient_info["problems"]["problems"][:problem_num]


def _callback_add_sdoh_problem(sender, app_data, user_data):
    global sdoh_problem_num
    sdoh_problem_num += 1
    # TODO
    # encapsulate into a struct
    problem = dict()
    problem["problem"] = ""
    problem["date_of_diagnosis"] = ""
    problem["date_of_resolution"] = ""

    dpg.add_text("Problem {0}: ".format(sdoh_problem_num),
                 tag="PIU_SDOH_PROBLEM_{0}_LABEL_TEXT".format(
                     sdoh_problem_num),
                 parent=user_data, indent=20)
    dpg.add_input_text(tag="PIU_SDOH_PROBLEM_{0}_PROBLEM_INPUT_TEXT".format(sdoh_problem_num), label="Problem",
                       default_value="", parent=user_data, indent=20, callback=_call_update_sdoh_problems)
    dpg.add_input_text(tag="PIU_SDOH_PROBLEM_{0}_DATE_OF_DIAGNOSIS_INPUT_TEXT".format(sdoh_problem_num),
                       label="Date of Diagnosis", default_value="", parent=user_data, indent=20,
                       callback=_call_update_sdoh_problems)
    dpg.add_input_text(tag="PIU_SDOH_PROBLEM_{0}_DATE_OF_RESOLUTION_INPUT_TEXT".format(sdoh_problem_num),
                       label="Date of Resolution", default_value="", parent=user_data, indent=20,
                       callback=_call_update_sdoh_problems)
    patient_info["problems"]["sdoh_problems_health_concerns"].append(
        problem)


def _callback_delete_sdoh_problem(sender, app_data, user_data):
    global sdoh_problem_num
    if sdoh_problem_num <= 0:
        return
    dpg.delete_item(
        "PIU_SDOH_PROBLEM_{0}_LABEL_TEXT".format(sdoh_problem_num))
    dpg.delete_item(
        "PIU_SDOH_PROBLEM_{0}_PROBLEM_INPUT_TEXT".format(sdoh_problem_num))
    dpg.delete_item(
        "PIU_SDOH_PROBLEM_{0}_DATE_OF_DIAGNOSIS_INPUT_TEXT".format(sdoh_problem_num))
    dpg.delete_item(
        "PIU_SDOH_PROBLEM_{0}_DATE_OF_RESOLUTION_INPUT_TEXT".format(sdoh_problem_num))
    sdoh_problem_num -= 1
    patient_info["problems"]["sdoh_problems_health_concerns"] = patient_info[
        "problems"]["sdoh_problems_health_concerns"][
        :sdoh_problem_num]


def _call_update_sdoh_problems(sender, app_data, user_data):
    index_key = sender.replace(
        "PIU_SDOH_PROBLEM_", "").replace("_INPUT_TEXT", "")
    index = int(index_key.split("_")[0]) - 1
    key = index_key[2:].lower()
    patient_info["problems"]["sdoh_problems_health_concerns"][index][key] = app_data


def _callback_add_medication(sender, app_data, user_data):
    global medication_num
    medication_num += 1
    dpg.add_input_text(tag="PIU_MEDICATION_{0}_NAME_INPUT_TEXT".format(medication_num),
                       label="Medication {0}".format(medication_num),
                       default_value="", parent=user_data, indent=20, callback=_callback_update_medications)
    patient_info["medications"]["medications"].append("")


def _callback_delete_medication(sender, app_data, user_data):
    global medication_num
    if medication_num <= 0:
        return
    dpg.delete_item(
        "PIU_MEDICATION_{0}_NAME_INPUT_TEXT".format(medication_num))
    medication_num -= 1
    patient_info["medications"]["medications"] = patient_info["medications"]["medications"][:medication_num]


def _callback_update_medications(sender, app_data, user_data):
    index = int(sender.replace("PIU_MEDICATION_", "").replace(
        "_NAME_INPUT_TEXT", "")) - 1
    patient_info["medications"]["medications"][index] = app_data


def _callback_update_allergy(sender, app_data, user_data):
    index_key = sender.replace(
        "PIU_ALLERGY_", "").replace("_INPUT_TEXT", "")
    index = int(index_key.split("_")[0]) - 1
    key = index_key[2:].lower()
    patient_info["allergies_intolerances"]["substances"][index][key] = app_data


def _callback_add_allergy(sender, app_data, user_data):
    global allergy_num
    allergy_num += 1
    dpg.add_text("Substance {0}: ".format(allergy_num),
                 tag="PIU_ALLERGY_{0}_LABEL_TEXT".format(
                     allergy_num),
                 parent=user_data, indent=20)
    dpg.add_input_text(tag="PIU_ALLERGY_{0}_SUBSTANCE_MEDICATION_INPUT_TEXT".format(allergy_num),
                       label="Substance Medication",
                       default_value="", parent=user_data, indent=20, callback=_callback_update_allergy)
    dpg.add_input_text(tag="PIU_ALLERGY_{0}_SUBSTANCE_DRUG_CLASS_INPUT_TEXT".format(allergy_num),
                       label="Substance Drug Class", default_value="", parent=user_data, indent=20,
                       callback=_callback_update_allergy)
    dpg.add_input_text(tag="PIU_ALLERGY_{0}_SUBSTANCE_REACTION_INPUT_TEXT".format(allergy_num),
                       label="Reaction", default_value="", parent=user_data, indent=20,
                       callback=_callback_update_allergy)
    allergy = dict()
    allergy["substance_medication"] = ""
    allergy["substance_drug_class"] = ""
    allergy["reaction"] = ""
    patient_info["allergies_intolerances"]["substances"].append(
        allergy)


def _callback_delete_allergy(sender, app_data, user_data):
    global allergy_num
    if allergy_num <= 0:
        return
    dpg.delete_item(
        "PIU_ALLERGY_{0}_LABEL_TEXT".format(allergy_num))
    dpg.delete_item(
        "PIU_ALLERGY_{0}_SUBSTANCE_MEDICATION_INPUT_TEXT".format(allergy_num))
    dpg.delete_item(
        "PIU_ALLERGY_{0}_SUBSTANCE_DRUG_CLASS_INPUT_TEXT".format(allergy_num))
    dpg.delete_item(
        "PIU_ALLERGY_{0}_SUBSTANCE_REACTION_INPUT_TEXT".format(allergy_num))
    allergy_num -= 1
    patient_info["allergies_intolerances"]["substances"] = patient_info["allergies_intolerances"]["substances"][
        :allergy_num]


def _callback_update_patient_vital_signs(sender, app_data, user_data):
    key = sender.replace("PIU_", "").replace(
        "_INPUT_TEXT", "").lower()
    patient_info["vital_signs"][key] = app_data


def _callback_add_family_health_history(sender, app_data, user_data):
    global family_health_history_num
    family_health_history_num += 1
    patient_info["family_health_history"]["family_health_history"].append(
        "")
    dpg.add_input_text(tag="PIU_FAMILY_HEALTH_HISTORY_{0}_INPUT_TEXT".format(family_health_history_num),
                       label="",
                       default_value="", parent=user_data, indent=20, callback=_callback_update_family_health_history)


def _callback_delete_family_health_history(sender, app_data, user_data):
    global family_health_history_num
    if family_health_history_num <= 0:
        return
    dpg.delete_item("PIU_FAMILY_HEALTH_HISTORY_{0}_INPUT_TEXT".format(
        family_health_history_num))
    family_health_history_num -= 1
    patient_info["family_health_history"]["family_health_history"] = patient_info[
        "family_health_history"][
        "family_health_history"][
        :family_health_history_num]


def _callback_update_social_health_history(sender, app_data, user_data):
    key = sender.replace("PIU_", "").replace(
        "_INPUT_TEXT", "").lower()
    patient_info["social_health_history"][key] = app_data


def _callback_update_family_health_history(sender, app_data, user_data):
    index = int(sender.replace(
        "PIU_FAMILY_HEALTH_HISTORY_", "").replace("_INPUT_TEXT", "")) - 1
    patient_info["family_health_history"]["family_health_history"][index] = app_data


def _init_patient_info_ui():
    global problem_tab
    with dpg.collapsing_header(label="Patient Info UI", default_open=True):
        # TODO: UI Creation

        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_load_patient_info_file, tag="PIU_OPEN_FILE_DIALOG", modal=True):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))

        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_save_patient_into_to_file, tag="PIU_SAVE_FILE_DIALOG", modal=True):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))

        # with dpg.window(height=100, width=350, label="Warning", modal=True, show=False,
        #                 tag="PIU_SAVE_FILE_CONFIRM_WINDOW", no_title_bar=True,
        #                 pos=[int(VIEWPORT_WIDTH / 2 - 175), int(VIEWPORT_HEIGHT / 2 - 50)], no_move=True):
        #     dpg.add_text(
        #         "Current patient information has not be saved.\nDo you want to save it firstly?")
        #     with dpg.group(horizontal=True):
        #         dpg.add_button(label="OK", width=75, pos=[50, 50],
        #                        callback=_callback_save_patient_info)
        #         dpg.add_button(label="Cancel", width=75, pos=[350 - 50 - 75, 50],
        #                        callback=lambda: dpg.configure_item("PIU_SAVE_FILE_CONFIRM_WINDOW", show=False))

        with dpg.group(horizontal=True):
            create_new_patient_info = dpg.add_button(
                label="Create Patient Information", indent=20)
            load_exist_patient_info = dpg.add_button(
                label="Load Patient Information", callback=_callback_load_patient_info)
        # with dpg.collapsing_header(label="Create Patient Information", default_open=False):

        # stupid code

        with dpg.collapsing_header(label="Patient Demographics", default_open=True, indent=20):
            dpg.add_input_text(tag=PIU_PATIENT_FIRST_NAME_INPUT_TEXT, label="First Name",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_LAST_NAME_INPUT_TEXT, label="Last Name",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_MIDDLE_NAME_INPUT_TEXT, label="Middle Name",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_SUFFIX_INPUT_TEXT, label="Suffix",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_PREVIOUS_NAME_INPUT_TEXT, label="Previous Name",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_DATE_OF_BIRTH_INPUT_TEXT, label="Date of Birth",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_DATE_OF_DEATH_INPUT_TEXT, label="Date of Death",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_AGE_INPUT_TEXT, label="Age",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_RACE_INPUT_TEXT, label="Race",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_ETHNICITY_INPUT_TEXT, label="Ethnicity",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_TRIBAL_AFFILIATION_INPUT_TEXT, label="Tribal Affiliation",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_SEX_ASSIGNED_AT_BIRTH_INPUT_TEXT, label="Sex Assigned at Birth",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_SEXUAL_ORIENTATION_INPUT_TEXT, label="Sexual Orientation",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_GENDER_IDENTITY_INPUT_TEXT, label="Gender Identity",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_PREFERRED_LANGUAGE_INPUT_TEXT, label="Preferred Language",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_CURRENT_ADDRESS_INPUT_TEXT, label="Current Address",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_PREVIOUS_ADDRESS_INPUT_TEXT, label="Previous Address",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_PHONE_NUMBER_INPUT_TEXT, label="Phone Number",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_PHONE_NUMBER_TYPE_INPUT_TEXT, label="Phone Number Type",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_EMAIL_ADDRESS_INPUT_TEXT, label="Email Address",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_RELATED_PERSONS_NAME_INPUT_TEXT, label="Related Persons Name",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_RELATED_PERSONS_RELATIONSHIP_INPUT_TEXT,
                               label="Related Persons Relationship",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_OCCUPATION_INPUT_TEXT, label="Occupation",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_OCCUPATION_HISTORY_INPUT_TEXT, label="Occupation History",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_CHIEF_COMPLAINT_INPUT_TEXT, label="Chief Complaint",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)
            dpg.add_input_text(tag=PIU_PATIENT_INSURANCE_INPUT_TEXT, label="Insurance",
                               default_value="", indent=20, callback=_callback_update_patient_demographics)

            # print(patient_info["problems"]["problems"])

        with dpg.collapsing_header(tag="PIU_PROBLEM_TAB", label="Problems", default_open=False,
                                   indent=20) as problem_tab:
            with dpg.group(horizontal=True):
                button_add_problem = dpg.add_button(
                    label="Add Problem", indent=20)
                button_delete_problem = dpg.add_button(
                    label="Delete Problem")
            dpg.configure_item(
                button_add_problem, user_data=problem_tab, callback=_callback_add_problem)
            dpg.configure_item(
                button_delete_problem, user_data=problem_tab, callback=_callback_delete_problem)

        with dpg.collapsing_header(tag="PIU_SDOH_PROBLEMS_TAB", label="SDOH Problems Health Concerns",
                                   default_open=False, indent=20) as sdoh_problem_tab:
            with dpg.group(horizontal=True):
                button_add_sdoh_problem = dpg.add_button(
                    label="Add Problem", indent=20)
                button_delete_sdoh_problem = dpg.add_button(
                    label="Delete Problem")
            dpg.configure_item(
                button_add_sdoh_problem, user_data=sdoh_problem_tab, callback=_callback_add_sdoh_problem)
            dpg.configure_item(
                button_delete_sdoh_problem, user_data=sdoh_problem_tab, callback=_callback_delete_sdoh_problem)

        with dpg.collapsing_header(label="Medications", default_open=False, indent=20) as medication_tab:
            with dpg.group(horizontal=True):
                button_add_medication = dpg.add_button(
                    label="Add Medication", indent=20)
                button_delete_medication = dpg.add_button(
                    label="Delete Medication")
            dpg.configure_item(
                button_add_medication, user_data=medication_tab, callback=_callback_add_medication)
            dpg.configure_item(
                button_delete_medication, user_data=medication_tab, callback=_callback_delete_medication)

        with dpg.collapsing_header(label="Allergies Intolerances", default_open=False, indent=20) as allergy_tab:
            with dpg.group(horizontal=True):
                button_add_allergy = dpg.add_button(
                    label="Add Allergy", indent=20)
                button_delete_allergy = dpg.add_button(
                    label="Delete Allergy")
            dpg.configure_item(
                button_add_allergy, user_data=allergy_tab, callback=_callback_add_allergy)
            dpg.configure_item(
                button_delete_allergy, user_data=allergy_tab, callback=_callback_delete_allergy)

        with dpg.collapsing_header(label="Vital Signs", default_open=False, indent=20) as vital_sign_tab:
            dpg.add_input_text(tag="PIU_SYSTOLIC_BLOOD_PRESSURE_INPUT_TEXT", label="Systolic Blood Pressure",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_DIASTOLIC_BLOOD_PRESSURE_INPUT_TEXT", label="Diastolic Blood_pressure",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_HEART_RATE_INPUT_TEXT", label="Heart Rate",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_RESPIRATORY_RATE_INPUT_TEXT", label="Respiratory Rate",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_BODY_TEMPERATURE_INPUT_TEXT", label="Body Temperature",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_BODY_HEIGHT_INPUT_TEXT", label="Body Height",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_BODY_WEIGHT_INPUT_TEXT", label="Body Weight",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_PULSE_OXIMETRY_INPUT_TEXT", label="Pulse Oximetry",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_INHALED_OXYGEN_CONCENTRATION_INPUT_TEXT", label="Inhaled Oxygen Concentration",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_BMI_PERCENTILE_2_TO_20_YEARS_INPUT_TEXT", label="BMI Percentile 2 to 20 years",
                               default_value="", indent=20, callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_WEIGHT_FOR_LENGTH_PERCENTILE_BIRTH_36_MONTHS_INPUT_TEXT",
                               label="Weight for Length Percentile birth 36 months", default_value="", indent=20,
                               callback=_callback_update_patient_vital_signs)
            dpg.add_input_text(tag="PIU_HEAD_OCCIPITAL_FRONTAL_CIRCUMFERENCE_PERCENTILE_BIRTH_36_MONTHS_INPUT_TEXT",
                               label="Head Occipital frontal circumference percentile birth 36 months",
                               default_value="", indent=20,
                               callback=_callback_update_patient_vital_signs)

        with dpg.collapsing_header(label="Family Health History", default_open=False,
                                   indent=20) as family_health_history_tab:
            with dpg.group(horizontal=True):
                button_add_family_health_history = dpg.add_button(
                    label="Add", indent=20)
                button_delete_family_health_history = dpg.add_button(
                    label="Delete")
            dpg.configure_item(button_add_family_health_history,
                               user_data=family_health_history_tab, callback=_callback_add_family_health_history)
            dpg.configure_item(button_delete_family_health_history,
                               user_data=family_health_history_tab, callback=_callback_delete_family_health_history)

            # social_health_history
        with dpg.collapsing_header(label="Social Health History", default_open=False,
                                   indent=20) as social_health_history:
            dpg.add_input_text(tag="PIU_SOCIAL_HISTORY_OBSERVATION_INPUT_TEXT", label="Social History Observation",
                               default_value="", indent=20, callback=_callback_update_social_health_history)
            dpg.add_input_text(tag="PIU_ALCOHOL_USE_INPUT_TEXT", label="Alcohol Use",
                               default_value="", indent=20, callback=_callback_update_social_health_history)
            dpg.add_input_text(tag="PIU_DRUG_USE_INPUT_TEXT",
                               label="Drug Use", default_value="", indent=20)
            dpg.add_input_text(tag="PIU_SEXUAL_ACTIVITY_INPUT_TEXT", label="Sexual Activity",
                               default_value="", indent=20, callback=_callback_update_social_health_history)
            dpg.add_input_text(tag="PIU_REFUGEE_STATUS_INPUT_TEXT", label="Refugee Status",
                               default_value="", indent=20, callback=_callback_update_social_health_history)
            dpg.add_input_text(tag="PIU_CONGREGATE_LIVING_INPUT_TEXT", label="Congregate Living",
                               default_value="", indent=20, callback=_callback_update_social_health_history)

        def _callback_export_patient_info(sender, app_data, user_data):
            dpg.show_item("PIU_SAVE_FILE_DIALOG")

        dpg.add_button(label="Export", indent=20,
                       callback=_callback_export_patient_info)


def main() -> None:
    global patient_info
    global problem_tab, sdoh_problem_tab, medication_tab, allergy_tab, family_health_history_tab
    with open('patient_information_template.json') as patient_info_json:
        patient_info = json.load(patient_info_json)

    dpg.create_context()
    dpg.configure_app(manual_callback_management=True)
    dpg.create_viewport(title='HRSA Content Creation Tool',
                        width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)

    with dpg.window(label="HRSA CCT", tag=HRSA_CCT_TOOL, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT):
        _init_patient_info_ui()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(HRSA_CCT_TOOL, True)
    # dpg.start_dearpygui()

    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()  # retrieves and clears queue
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
