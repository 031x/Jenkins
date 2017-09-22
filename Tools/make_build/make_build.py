import sys,os
import argparse
import re
import glob

# add keil path to python system path
keil_path = r'D:\Keil_v5\UV4'
sys.path.append(keil_path)

# define Build object
class BuildObj:
    def __init__(self):
        self.prj_path = ""
        self.build_mode = ""
        self.print_filter_str = ""
        self.is_use_local_git_code = False
        self.is_not_allow_exit_changed_files = False
        self.is_not_clean_when_build = False
    # define print class function
    def __str__(self):
        str = "\n--------------------------------------------------------------------------\n"
        str += "* project filename: " + self.prj_path+ "\n"
        str += "* build mode: " + self.build_mode + "\n"
        str += "* build output filter string: " + self.filter_str + "\n"
        str += "* is use local git code: %r" % self.is_use_local_git_code + "\n"
        str += "* is not allow exit change files: %r" % self.is_not_allow_exit_changed_files + "\n"
        str += "* is not clean when build: %r" % self.is_not_clean_when_build + "\n"
        str += "--------------------------------------------------------------------------\n"
        return str

    def __repr__(self):
        return str(self)
# create new build object class
build_obj = BuildObj()

# print error function
def exit_p(str):
    print("Error: "+str)
    exit(-1)

# add argparse for build
parser = argparse.ArgumentParser(description="Build your program command")
parser.add_argument('-pd','--prj_dir', help="Build program dirction")
parser.add_argument('-bm','--build_mode', default= "Debug", help="Build program mode: d/D/debug/Debug/r/R/release/Release/ut/UT/unittest/UnitTest,default as Debug")
parser.add_argument('-l','--local',  action = 'store_true',help="not update to last version, make firmware with current local version")
parser.add_argument('-n','--not_changed',action = 'store_true',help="not allow changed files when make firmware")
parser.add_argument('-nc','--not_clear',action = 'store_true',help="not clear when build")
parser.add_argument('-fs','--filter_string',default="Error",help="build output filter string, default as Error")
args = parser.parse_args()

if args.build_mode == "Debug" or args.build_mode == "debug" or args.build_mode == "D" or args.build_mode == "d" :
    build_obj.build_mode = "Debug"
elif args.build_mode == "Release" or args.build_mode == "release" or args.build_mode == "R" or args.build_mode == "r" :
    build_obj.build_mode = "Release"
elif args.build_mode == "UnitTest" or args.build_mode == "unittest" or args.build_mode == "UT" or args.build_mode == "ut":
    build_obj.build_mode = "UnitTest"
else:
    build_obj.build_mode = "Debug"

if args.filter_string:
    build_obj.filter_str = args.filter_string
else:
    build_obj.filter_str = ""

if args.local:
    build_obj.is_use_local_git_code = True
else:
    build_obj.is_use_local_git_code = False
if args.not_changed:
    build_obj.is_not_allow_exit_changed_files = True
else:
    build_obj.is_not_allow_exit_changed_files = False
if args.not_clear:
    build_obj.is_not_clean_when_build = True
else:
    build_obj.is_not_clean_when_build = False

# define print output information with filter
def print_output_file_by_filter(regex, output_file):
    if os.path.exists(output_file):
        for line in open(output_file):
            matchObj = re.search(regex, line, re.M | re.I)
            if matchObj:
                print(line)
    else:
        exit_p("%s does not exist" % output_file)

# define print output information
def print_output_file(output_file):
    if os.path.exists(output_file):
        for line in open(output_file):
            print(line)
    else:
        exit_p("%s does not exist" % output_file)

# check project path is exist
if os.path.exists(args.prj_dir):
    os.chdir(args.prj_dir)
else:
    exit_p("project dirction: %s does not exist" % args.project_dir)

# find a project with *uvproj format
for file_name in glob.glob("*.uvproj"):
    # print(file_name)
    prj_name = file_name
if os.path.exists(prj_name):
    build_obj.prj_path = os.path.abspath(prj_name)
    build_output_filename = build_obj.build_mode + "_Build_Output.txt"
    # print build config information
    print(build_obj)

    build_command = "UV4.exe -r %s -o %s -t %s" % (prj_name, build_output_filename, build_obj.build_mode)
    print(build_command+"\n")
    os.system(build_command)
    if build_obj.filter_str:
        print_output_file_by_filter(build_obj.filter_str, build_output_filename)
    else:
        print_output_file(build_output_filename)
else:
    exit_p("do not find project")

