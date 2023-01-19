pyinstaller --onefile --windowed __main__.py
xcopy /y decent-lambda-354120-0d9c66891965.json .\dist\
xcopy /y .\patient_info_ui\patient_information_template.json .\dist\patient_info_ui\
xcopy /y .\dialogue_ui_config\dialogue_ui_config.json .\dist\dialogue_ui_config\
xcopy /y .\character_config\CharacterModelData.json .\dist\character_config\
xcopy /y dpg.ini .\dist\
xcopy /s /y inklecate_windows .\dist\inklecate_windows\
rename .\dist\__main__.exe HRSA_CCT.exe
