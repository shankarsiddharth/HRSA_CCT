import os
import pathlib
import platform
import shutil
import sys
import time
from datetime import datetime

import PyInstaller.__main__

from __v1 import hrsa_cct_constants as hcc
from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_version import app_version

# region startup
afs: AppFileSystem = AppFileSystem()
afsc: AppFileSystemConstants = AppFileSystemConstants()

# Get the current directory path
# Scripts folder path
current_folder_path = os.path.dirname(os.path.realpath(__file__))
# Project root folder path
project_folder_path = os.path.dirname(os.path.realpath(current_folder_path))

# Source folder path
SOURCE_FOLDER_NAME = "src"
src_folder_path = os.path.join(project_folder_path, SOURCE_FOLDER_NAME)
# endregion startup

# region build
BUILD_FOLDER_NAME = "build"
# Create build folder if it does not exist
build_folder_path = os.path.join(project_folder_path, BUILD_FOLDER_NAME)
build_folder = pathlib.Path(build_folder_path)
if not build_folder.exists():
    build_folder.mkdir()

# Get the version number
version_string: str = app_version.APP_VERSION_STRING

version_folder_path = os.path.join(build_folder_path, version_string)
version_folder = pathlib.Path(version_folder_path)
# Delete the version folder if it exists
if version_folder.exists():
    try:
        shutil.rmtree(version_folder_path)
    except PermissionError as e:
        print("PermissionError: " + str(e), file=sys.stderr)
        print('Application might be running in the background. If it is close it and try again.', file=sys.stderr)
        print("Background processes might be accessing this file/folder.", file=sys.stderr)
        print("If the adb process is running in the background, then kill it and try again.", file=sys.stderr)
        print("Make sure no other background processes/applications are accessing this file/folder.", file=sys.stderr)
        exit(1)
    except Exception as e:
        print("Exception: " + str(e), file=sys.stderr)
        exit(1)
# Create version folder if it does not exist
if not version_folder.exists():
    version_folder.mkdir()

# Create the Application Build folder
APPLICATION_NAME = "HRSACCT"
build_platform = platform.system()

if build_platform == "Windows":
    pass
elif build_platform == "Linux":
    sys.exit("Linux is not supported yet.")
elif build_platform == "Darwin":
    sys.exit("MacOS is not supported yet.")

# Application Executable File Name - Windows Only
application_executable_file_name = APPLICATION_NAME + ".exe"
app_build_version_folder_path = os.path.join(version_folder_path, APPLICATION_NAME)
app_build_version_folder = pathlib.Path(app_build_version_folder_path)
# Delete the Application Build folder if it exists
if app_build_version_folder.exists():
    shutil.rmtree(app_build_version_folder_path)
# Create Application Build folder if it does not exist
if not app_build_version_folder.exists():
    app_build_version_folder.mkdir()

# region _pyi_temp
PYINSTALLER_INTERMEDIATE_FOLDER_NAME = "_pyi_temp"
PYINSTALLER_WORKPATH_FOLDER_NAME = "_pyi_build"
PYINSTALLER_DIST_FOLDER_NAME = "_pyi_dist"
PYINSTALLER_SPEC_FOLDER_NAME = "_pyi_spec"

pyinstaller_temp_folder_path = os.path.join(project_folder_path, PYINSTALLER_INTERMEDIATE_FOLDER_NAME)
pyinstaller_temp_folder = pathlib.Path(pyinstaller_temp_folder_path)
# Delete the pyinstaller temp folder if it exists
if pyinstaller_temp_folder.exists():
    print("Deleting pyinstaller temp folder: " + pyinstaller_temp_folder_path)
    shutil.rmtree(pyinstaller_temp_folder_path)
# Create pyinstaller temp folder if it does not exist
if not pyinstaller_temp_folder.exists():
    print("Creating pyinstaller temp folder: " + pyinstaller_temp_folder_path)
    pyinstaller_temp_folder.mkdir()

# PyInstaller SPEC Folder Path
pyinstaller_spec_folder_path = os.path.join(project_folder_path, PYINSTALLER_INTERMEDIATE_FOLDER_NAME, PYINSTALLER_SPEC_FOLDER_NAME)
# PyInstaller Workpath / Build Folder Path
pyinstaller_workpath_folder_path = os.path.join(project_folder_path, PYINSTALLER_INTERMEDIATE_FOLDER_NAME, PYINSTALLER_WORKPATH_FOLDER_NAME)
# PyInstaller Dist Folder Path
pyinstaller_dist_folder_path = os.path.join(project_folder_path, PYINSTALLER_INTERMEDIATE_FOLDER_NAME, PYINSTALLER_DIST_FOLDER_NAME)
# endregion _pyi_temp

# Version 1 Folder Name
VERSION_1_FOLDER_NAME = "__v1"
# Application Start-up Script Name
application_start_up_script_name = "__main__v1__.py"

# Create options for pyinstaller
# Application Name Argument
app_name_args_string = "--name=" + APPLICATION_NAME
# Source Path Argument
src_path_args_string = "--path=" + src_folder_path
# Deprecated Source Path Argument
deprecated_src_path_args_string = "--path=" + os.path.join(src_folder_path, VERSION_1_FOLDER_NAME)
# Start-up script path - "*.py" file
main_script_path = os.path.join(src_folder_path, VERSION_1_FOLDER_NAME, application_start_up_script_name)
# Icon File Path for the Application
icon_path = afs.get_default_app_icon_large_file_path()
icon_args_string = "--icon=" + icon_path
# SPEC File Path
spec_file_args_string = "--specpath=" + pyinstaller_spec_folder_path
# Workpath / Build Folder Path
workpath_args_string = "--workpath=" + pyinstaller_workpath_folder_path
# Dist Folder Path
distpath_args_string = "--distpath=" + pyinstaller_dist_folder_path

print("Building Application using PyInstaller...")
try:
    PyInstaller.__main__.run(
        [
            main_script_path,
            "--onefile",
            "--windowed",
            app_name_args_string,
            src_path_args_string,
            deprecated_src_path_args_string,
            icon_args_string,
            spec_file_args_string,
            workpath_args_string,
            distpath_args_string
        ]
    )

except BaseException as e:
    print(e, file=sys.stderr)
    exit(1)
print("PyInstaller packaging completed.")
# endregion build

# region assets
# Copy the assets folder to the Application Build folder
print("Copying assets folder to the Application Build folder...")
build_assets_folder_path = os.path.join(app_build_version_folder_path, afsc.ASSETS_FOLDER_NAME)
build_assets_folder = pathlib.Path(build_assets_folder_path)
# Delete the assets folder if it exists
if build_assets_folder.exists():
    print("Deleting the existing assets folder...")
    shutil.rmtree(build_assets_folder_path)
# Copy the source assets folder to the distribution assets folder
project_assets_folder_path = os.path.join(project_folder_path, afsc.ASSETS_FOLDER_NAME)
project_assets_folder = pathlib.Path(project_assets_folder_path)
if not project_assets_folder.exists():
    print("Project assets folder does not exist", file=sys.stderr)
    exit(1)
shutil.copytree(project_assets_folder_path, build_assets_folder_path)
# endregion assets

# region bin
# Create a binary directory in the Application Build folder
print("Copying binaries to the Application Build folder...")
build_binary_folder_path = os.path.join(app_build_version_folder_path, afsc.BINARY_FOLDER_NAME)
build_binary_folder = pathlib.Path(build_binary_folder_path)
# Delete the binary folder if it exists
if build_binary_folder.exists():
    shutil.rmtree(build_binary_folder_path)
# # Create the binary folder if it does not exist
# if not build_binary_folder.exists():
#     build_binary_folder.mkdir()

# Copy inklecate and Inky Binaries to the Application Build folder
print("Copying inklecate and Inky binaries to the Application Build folder...")
project_binary_folder_path = os.path.join(project_folder_path, afsc.BINARY_FOLDER_NAME)
project_binary_folder = pathlib.Path(project_binary_folder_path)
if not project_binary_folder.exists():
    print("Project binary folder does not exist", file=sys.stderr)
    exit(1)
# TODO : Change this to copy inklecate and Inky binaries only for the current platform
shutil.copytree(project_binary_folder_path, build_binary_folder_path)

# PyInstaller created Executable File Path
temp_executable_file_path = os.path.join(pyinstaller_dist_folder_path, application_executable_file_name)
temp_executable_file = pathlib.Path(temp_executable_file_path)
if not temp_executable_file.exists():
    print("Executable file does not exist", file=sys.stderr)
    exit(1)
# Copy the executable file to the binary folder
print("Copying the executable file to the binary folder...")
build_binary_executable_file_path = os.path.join(build_binary_folder_path, application_executable_file_name)
shutil.copyfile(temp_executable_file_path, build_binary_executable_file_path)

if build_platform == "Windows":
    pass
elif build_platform == "Linux":
    sys.exit("Linux is not supported yet.")
elif build_platform == "Darwin":
    sys.exit("MacOS is not supported yet.")

# Delete the project development files like readme, version files
print("Deleting the project development files like readme, version files...")
# region Windows Only
# Delete inklecate Readme File
DEFAULT_README_FILE_NAME = "README.md"
build_binary_inklecate_readme_file_path = os.path.join(build_binary_folder_path, afsc.BINARY_INKLECATE_FOLDER_NAME, afsc.WINDOWS_BINARY_FOLDER_NAME, DEFAULT_README_FILE_NAME)
build_binary_inklecate_readme_file = pathlib.Path(build_binary_inklecate_readme_file_path)
if not build_binary_inklecate_readme_file.exists():
    print("inklecate readme file does not exist in the build binary folder. Make sure the project binary folder has the readme file.", file=sys.stderr)
    inklecate_fp = os.path.join(project_binary_folder_path, afsc.BINARY_INKLECATE_FOLDER_NAME, afsc.WINDOWS_BINARY_FOLDER_NAME, DEFAULT_README_FILE_NAME)
    print("Please check the project readme file path: " + inklecate_fp, file=sys.stderr)
    exit(1)
os.remove(build_binary_inklecate_readme_file_path)
# Delete Inky Readme File
build_binary_inky_readme_file_path = os.path.join(build_binary_folder_path, afsc.BINARY_INKY_FOLDER_NAME, afsc.WINDOWS_BINARY_FOLDER_NAME, DEFAULT_README_FILE_NAME)
build_binary_inky_readme_file = pathlib.Path(build_binary_inky_readme_file_path)
if not build_binary_inky_readme_file.exists():
    print("Inky readme file does not exist in the build binary folder. Make sure the project binary folder has the readme file.", file=sys.stderr)
    inky_fp = os.path.join(project_binary_folder_path, afsc.BINARY_INKY_FOLDER_NAME, afsc.WINDOWS_BINARY_FOLDER_NAME, DEFAULT_README_FILE_NAME)
    print("Please check the project readme file path: " + inky_fp, file=sys.stderr)
    exit(1)
os.remove(build_binary_inky_readme_file_path)
# endregion Windows Only

# Delete inklecate Version File - All Platforms
print("Deleting inklecate version file...")
DEFAULT_INKLECATE_VERSION_FILE_NAME = "inklecate_version.txt"
inky_version_file_path = os.path.join(build_binary_folder_path, afsc.BINARY_INKLECATE_FOLDER_NAME, DEFAULT_INKLECATE_VERSION_FILE_NAME)
inky_version_file = pathlib.Path(inky_version_file_path)
if not inky_version_file.exists():
    print("Inklecate version file does not exist in the build binary folder. Make sure the project binary folder has the version file.", file=sys.stderr)
    inky_version_fp = os.path.join(project_binary_folder_path, afsc.BINARY_INKLECATE_FOLDER_NAME, DEFAULT_INKLECATE_VERSION_FILE_NAME)
    print("Please check the project version file path: " + inky_version_fp, file=sys.stderr)
    exit(1)
os.remove(inky_version_file_path)
# Delete Inky Version File - All Platforms
print("Deleting Inky version file...")
DEFAULT_INKY_VERSION_FILE_NAME = "Inky_version.txt"
inky_version_file_path = os.path.join(build_binary_folder_path, afsc.BINARY_INKY_FOLDER_NAME, DEFAULT_INKY_VERSION_FILE_NAME)
inky_version_file = pathlib.Path(inky_version_file_path)
if not inky_version_file.exists():
    print("Inky version file does not exist in the build binary folder. Make sure the project binary folder has the version file.", file=sys.stderr)
    inky_version_fp = os.path.join(project_binary_folder_path, afsc.BINARY_INKY_FOLDER_NAME, DEFAULT_INKY_VERSION_FILE_NAME)
    print("Please check the project version file path: " + inky_version_fp, file=sys.stderr)
    exit(1)
os.remove(inky_version_file_path)
# endregion bin

# region cctconfig
# Copy cctconfig defaults folder to the Application Builds folder
print("Copying cctconfig defaults folder to the Application Builds folder...")
build_cctconfig_folder_path = os.path.join(app_build_version_folder_path, hcc.CCT_CONFIG_FOLDER_NAME)
build_cctconfig_folder = pathlib.Path(build_cctconfig_folder_path)
# Delete the config defaults folder if it exists
if build_cctconfig_folder.exists():
    shutil.rmtree(build_cctconfig_folder_path)
# Create the cctconfig folder
build_cctconfig_folder.mkdir()
# Copy the project cctconfig - dpg config ini to the versioned build cctconfig - dpg config ini folder
build_dpg_config_file_path = os.path.join(build_cctconfig_folder_path, hcc.DPG_CONFIG_FILE_NAME)
build_dpg_config_file = pathlib.Path(build_dpg_config_file_path)
# Delete the dpg config ini file if it exists
if build_dpg_config_file.exists():
    os.remove(build_dpg_config_file_path)
project_dpg_config_ini_file_path = os.path.join(project_folder_path, hcc.CCT_CONFIG_FOLDER_NAME, hcc.DPG_CONFIG_FILE_NAME)
project_dpg_config_ini_file = pathlib.Path(project_dpg_config_ini_file_path)
if not project_dpg_config_ini_file.exists():
    print("Project cctconfig - dpg config ini file does not exist", file=sys.stderr)
    exit(1)
shutil.copyfile(project_dpg_config_ini_file_path, build_dpg_config_file_path)
# endregion cctconfig

# region data
# Copy project data folder to the Application Build folder
print("Copying project data folder to the Application Build folder...")
build_data_folder_path = os.path.join(app_build_version_folder_path, afsc.DATA_FOLDER_NAME)
build_data_folder = pathlib.Path(build_data_folder_path)
# Delete the data defaults folder if it exists
if build_data_folder.exists():
    print("Deleting the data defaults folder...")
    shutil.rmtree(build_data_folder_path)
# Copy the project data folder to the distribution/build data folder
project_data_folder_path = os.path.join(project_folder_path, afsc.DATA_FOLDER_NAME)
project_data_folder = pathlib.Path(project_data_folder_path)
if not project_data_folder.exists():
    print("Project data defaults folder does not exist", file=sys.stderr)
    exit(1)
shutil.copytree(project_data_folder_path, build_data_folder_path)
# endregion data

# region HRSAData
# Copy project HRSAData folder to the Application Build folder
print("Copying project HRSAData folder to the Application Build folder...")
build_HRSAData_folder_path = os.path.join(app_build_version_folder_path, afsc.HRSA_DATA_WORKSPACE_FOLDER_NAME)
build_HRSAData_folder = pathlib.Path(build_HRSAData_folder_path)
# Delete the HRSAData defaults folder if it exists
if build_HRSAData_folder.exists():
    print("Deleting the existing HRSAData folder...")
    shutil.rmtree(build_HRSAData_folder_path)
# Copy the project HRSAData folder to the distribution/build HRSAData folder
project_HRSAData_folder_path = os.path.join(project_folder_path, afsc.HRSA_DATA_WORKSPACE_FOLDER_NAME)
project_HRSAData_folder = pathlib.Path(project_HRSAData_folder_path)
if not project_HRSAData_folder.exists():
    print("ERROR: Project HRSAData folder does not exist.", file=sys.stderr)
    print("Please check the project HRSAData folder path: " + project_HRSAData_folder_path, file=sys.stderr)
    print("If the project HRSAData folder does not exist, please create it and copy the HRSAData files to it.", file=sys.stderr)
    print("The HRSAData files are located in the Unity HRSA project root folder.", file=sys.stderr)
    exit(1)
shutil.copytree(project_HRSAData_folder_path, build_HRSAData_folder_path)
# endregion HRSAData

# region license
PROJECT_LICENSE_FILE_NAME = "LICENSE.md"
# Copy the license file to the Application Build folder
print("Copying the license file to the Application Build folder...")
build_license_file_path = os.path.join(app_build_version_folder_path, PROJECT_LICENSE_FILE_NAME)
project_license_file_path = os.path.join(project_folder_path, PROJECT_LICENSE_FILE_NAME)
shutil.copy(project_license_file_path, build_license_file_path)
# endregion license

# region version
# Create Build Version File
print("Creating Build Version File...")
BUILD_VERSION_FILE_NAME = "version"
build_version_file_path = os.path.join(app_build_version_folder_path, BUILD_VERSION_FILE_NAME)
build_version_file = pathlib.Path(build_version_file_path)
# Delete the build version file if it exists
if build_version_file.exists():
    os.remove(build_version_file_path)
# Create the build version file
with open(build_version_file_path, "w") as version_file:
    current_date_time = datetime.now()
    date_time_string = current_date_time.strftime("Built on %B, %d, %Y (%A) at %I:%M:%S %p")
    time_zone_string = time.strftime("%Z", time.localtime())
    version_file_string = version_string + " - " + date_time_string + " " + time_zone_string
    version_file.write(version_file_string)
# endregion version

# region zip
# Create a zip file of the Application Build folder
print("Creating a zip file of the Application Build folder...")
print("This operation may take some time...")
zip_file_path = os.path.join(version_folder_path, APPLICATION_NAME + ".zip")
# Delete the zip file if it exists
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
# Create the zip file
shutil.make_archive(app_build_version_folder_path, "zip", app_build_version_folder_path)
print("Zip File Created")

print("====================================================================================================")
print(version_string + " Build Completed Successfully")
print("Build Folder: " + app_build_version_folder_path)
print("Zip File: " + zip_file_path)
print("====================================================================================================")
# endregion zip
