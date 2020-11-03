
import sys
import os
import re

def cetmodules_20_patcher(*args):
    os.system("$HOME/migrate")

def fixrootlib(x):
    part = x.group(1)
    for lib in ("GenVector", "Core", "Imt", "RIO", "Net", "Hist", "Graf", "Graf3d", "Gpad", "ROOTVecOps", "Tree", "TreePlayer", "Rint", "Postscript", "Matrix", "Physics", "MathCore", "Thread", "MultiProc", "ROOTDataFrame"):
         if lib.lower() == part.lower():
              return 'ROOT::%s' % lib
    return 'ROOT::%s' % part.lower().capitalize()
        
def cetmodules_dir_patcher(dir, proj, vers, debug=False):
    for rt, drs, fnames in os.walk(dir):
        if "CMakeLists.txt" in fnames:
            cetmodules_file_patcher(rt + "/CMakeLists.txt", rt == dir, proj, vers, debug)
        for fname in fnames:
            if fname.endswith(".cmake"):
                cetmodules_file_patcher("%s/%s" % (rt, fname), rt == dir, proj, vers)

cmake_cet_ver_re = re.compile(r"ENV\{CETBUILDTOOLS_VERSION\}")
cmake_min_re = re.compile(r"cmake_minimum_required\s*\(\s*[VERSION ]*(\d*\.\d*).*\)")
cmake_project_re = re.compile(r"project\(\s*(\S*)(.*)\)")
cmake_ups_boost_re  = re.compile(r"find_ups_boost\(.*\)")
cmake_ups_root_re  = re.compile(r"find_ups_root\(.*\)")
cmake_find_ups_re  = re.compile(r"find_ups_product\(\s*(\S*).*\)")
cmake_find_cetbuild_re = re.compile(r"find_package\s*\(\s*(cetbuildtools.*)\)")
cmake_find_lib_paths_re = re.compile("cet_find_library\((.*) PATHS ENV.*NO_DEFAULT_PATH")
boost_re = re.compile(r"\$\{BOOST_(\w*)_LIBRARY\}")
root_re = re.compile(r"\$\{ROOT_(\w*)_LIBRARY\}")
tbb_re = re.compile(r"\$\{TBB}")
dir_re = re.compile(r"\$\{\([A-Z_]\)_DIR\}")
drop_re = re.compile(r"(_cet_check\()|(include\(UseCPack\))|(add_subdirectory\(\s*ups\s*\))|(cet_have_qual\()|(check_ups_version\()")
cmake_config_re = re.compile(r"cet_cmake_config\(")
cmake_inc_cme_re = re.compile(r"include\(CetCMakeEnv\)")
cmake_inc_ad_re = re.compile(r"include\(ArtDictionary\)")
cmake_eld_re = re.compile(r"export_library_dependencies\((.*)\)",re.IGNORECASE)
comment_re = re.compile(r"^\s*\#")

def fake_check_ups_version(line, fout):
    p0 = line.find("PRODUCT_MATCHES_VAR ") + 20
    p1 = line.find(")")
    fout.write("set( %s True )\n" % line[p0:p1] )

def cetmodules_file_patcher(fname, toplevel=True, proj='foo', vers='1.0', debug=False):
    sys.stderr.write("Patching file '%s'\n" % fname)
    fin = open(fname,"r")
    fout = open(fname+".new", "w")
    need_cmake_min = toplevel
    need_project = toplevel

    drop_til_close = False
    saw_cmake_config = False
    saw_cetmodules = False
    saw_cmakeenv_include = False
    saw_canvas_root_io = False

    for line in fin:

        if debug:
             sys.stderr.write("line: %s" % line)

        # don't be fooled by commented out lines..
        if comment_re.match(line):
            fout.write(line)
            continue

        line = line.rstrip()

        # ugly special cases
        # larpandoracontent has an if/else for if we have
        # cetmodules...
        if line == "else()" and proj.find("pandora")> 1:
            if toplevel and not saw_cmake_config:
                if not saw_cetmodules:
                    fout.write("find_package(cetmodules)\n")
                    saw_cetmodules = True
                if not saw_cmakeenv_include:
                    fout.write("include(CetCMakeEnv)\n")
                    saw_cmakeenv_include = True
                fout.write("cet_cmake_config()\n")
                saw_cmake_config = True
 
        # art_root_io has wierdness in simple_plugin(SamplingInput...
        if (line == 'simple_plugin(SamplingInput "source"' and
                     fname.find('art_root_io/CMakeLists.txt')>=0):
             line = 'simple_plugin(SamplingInput LIBRARY'

        if line.find("include(cetmodules") > 0:
            saw_cetmodules = True

        if drop_til_close:
            if line.find(")") > 0:
                drop_til_close = False
            if line.find("PRODUCT_MATCHES_VAR") > 0:
                fake_check_ups_version(line, fout)
            continue
        line = dir_re.sub(lambda x:'${%s_DIR}' % x.group(1).lower(), line)
        line = boost_re.sub(lambda x:'Boost::%s' % x.group(1).lower(), line)
        line = root_re.sub(fixrootlib, line)
        line = tbb_re.sub('TBB:tbb', line)
        # fool cetbuildtools version checks
        line = cmake_cet_ver_re.sub("CMAKE_CACHE_MAJOR_VERSION",line)

        if fname.find("Modules/CMakeLists.txt") >= 0  and line.find("DESTINATION ${product}/${version}/Modules") >= 0:
            fout.write("  DESTINATION Modules\n")
            continue

        mat = cmake_inc_ad_re.search(line)
        if mat and not saw_canvas_root_io:
            if debug:
                 sys.stderr.write("inc_ad without canvas_root_io\n")
            fout.write("find_package(canvas_root_io)\n")
            fout.write(line + "\n")
            continue

        # this found in larpandoracontent
        # https://cmake.org/cmake/help/v3.0/policy/CMP0033.html
        mat = cmake_eld_re.search(line)
        if mat:
            if mat.group(1):
                arg = "%s FILE %s" % (proj, mat.group(1))
            else:
                arg = proj
            fout.write("install(EXPORT libdeps {0})\n".format(arg))
            continue
            
        mat = cmake_find_cetbuild_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("cetbuild\n")
            sys.stderr.write("fixing cetbuild in: %s\n" % line)
            fout.write("find_package(cetmodules)\n")
            saw_cetmodules = True
            continue

        mat = cmake_inc_cme_re.search(line)
        if mat:
            if debug:
                sys.stderr.write("cetbuild_re\n")
            if not saw_cetmodules:
                fout.write("find_package(cetmodules)\n")
                saw_cetmodules = True
            saw_cmakeenv_include = True
            fout.write(line + "\n")
            continue

        # if its any other random cet_xxx command, make sure we have
        # included the parts...
        if line.find("cet_") > 0:
            if not saw_cetmodules:
                fout.write("find_package(cetmodules)\n")
                saw_cetmodules = True
            if not saw_cmakeenv_include:
                fout.write("include(CetCMakeEnv)\n")
                saw_cmakeenv_include = True

        mat = cmake_config_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("config_re\n")
            saw_cmake_config = True


        mat = drop_re.search(line)
        if mat: 
            if debug:
                 sys.stderr.write("drop_re\n")
            if line.find(")") < 0:
                drop_til_close = True
            if line.find("PRODUCT_MATCHES_VAR") > 0:
                fake_check_ups_version(line, fout)
            continue

        mat = cmake_min_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("min_re\n")
            if proj.find("pandora") > 0:
                fout.write(line + "\n")
                fout.write("cmake_policy(SET CMP0048 NEW)\n")
            else:
                fout.write( "cmake_minimum_required(VERSION %s)\n" % str(max(float(mat.group(1)), 3.11)))
            need_cmake_min = False
            continue
        
        mat = cmake_find_lib_paths_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("find_lib_paths_re\n")
            fout.write("cet_find_library(%s)\n" % mat.group(1).replace("_ups",""))
            continue

        mat = cmake_project_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("project_re\n")
            if mat.group(2).find("VERSION") >= 0:
                fout.write( line + "\n" )
            else:
                fout.write( "project(%s VERSION %s LANGUAGES CXX C)\n" % (mat.group(1),vers))
            fout.write("#some need this for install_fhicl(), install_gdml()\nset(fcl_dir job)\nset(gdml_dir gdml)\n")
            need_project = False
            continue

        mat = cmake_ups_root_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("ups_root_re\n")
            if need_cmake_min:
               fout.write("cmake_minimum_required(VERSION 3.11)\n")
               need_cmake_min = False
            if need_project:
               fout.write("project( %s VERSION %s LANGUAGES CXX )\n" % (proj,vers))
               need_project = False
              
            fout.write("set(ROOT_CONFIG_DEBUG TRUE)\n")
            fout.write("find_package(ROOT COMPONENTS Core GenVector Gpad Graf Graf3d Hist Imt MathCore Matrix MultiProc Net Physics Postscript Rint RIO ROOTDataFrame ROOTDataFrame ROOTVecOps Thread Tree TreePlayer)\n")
            continue

        mat = cmake_ups_boost_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("ups_boost_re\n")
            if need_cmake_min:
               fout.write("cmake_minimum_required(VERSION 3.11)\n")
               need_cmake_min = False
            if need_project:
               fout.write("project( %s VERSION %s LANGUAGES CXX )\n" % (proj,vers))
               need_project = False
            fout.write("find_package(Boost COMPONENTS system filesystem program_options date_time graph thread regex random)\n")
            continue

        mat = cmake_find_ups_re.search(line)
        if mat:
            if debug:
                 sys.stderr.write("ups_find_ups_re\n")
            if proj.find("pandora") > 0:
               # just drop it for larpandora*
               continue
            if need_cmake_min:
               fout.write("cmake_minimum_required(VERSION 3.11)\n")
               need_cmake_min = False
            if need_project:
               fout.write("project( %s VERSION %s LANGUAGES CXX )\n" % (proj,vers))
               need_project = False

            newname = mat.group(1)

            if newname == 'cetbuildtools':
                newname = 'cetmodules'

            if newname == 'canvas_root_io':
                saw_canvas_root_io = True

            # it might seem we want to do this because
            # spack packages have the - in the name, but
            # we shouldn't because the files for foo-bar
            # still have foo_barConfig.cmake in their
            # search area...
            # newname = newname.replace("_","-")

            if newname.find("lib") == 0:
               newname = newname[3:]

            if newname in ("catch", "catch2"):
               newname = "Catch2"

            if newname in ("clhep",):
               newname = newname.upper()

            if newname in ("sqlite3","sqlite"):
               newname = newname.capitalize().strip("0123456789")

            if newname == "ifdhc":
               fout.write("cet_find_simple_package( ifdh INCPATH_SUFFIXES inc INCPATH_VAR IFDHC_INC )\n")
            elif newname in ("wda", "ifbeam", "nucondb", "cetlib", "cetlib-except", "dk2nudata", "cppunit", "Sqlite"):
               fout.write("cet_find_simple_package( %s INCPATH_VAR %s_INC )\n" % (newname, newname.upper()))
            else:
                fout.write("find_package( %s )\n" % newname )
            continue

        fout.write(line+"\n")

    if toplevel and not saw_cmake_config:
        if not saw_cetmodules:
            fout.write("find_package(cetmodules)\n")
        if not saw_cmakeenv_include:
            fout.write("include(CetCMakeEnv)\n")
        fout.write("cet_cmake_config()\n")

    fin.close()
    fout.close()
    if os.path.exists(fname+'.bak'):
        os.unlink(fname+'.bak')
    os.link(fname, fname+'.bak')
    os.rename(fname+'.new', fname)

if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        debug = True

    if len(sys.argv) != 4 or not os.path.isdir(sys.argv[1]):
        sys.stderr.write("usage: %s directory package-name package-version\n" % sys.argv[0])
        sys.exit(1)
    cetmodules_dir_patcher(sys.argv[1], sys.argv[2],sys.argv[3], debug=debug)
