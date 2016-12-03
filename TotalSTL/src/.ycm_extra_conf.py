import os
import ycm_core

flags = [
'-Wall',
'-Wextra',
'-Werror',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
'-DUSE_CLANG_COMPLETER',
'-std=c++11',
'-stdlib=libc++',
'-x',
'c++',
'-I',
'.',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../include/c++/v1',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/clang/8.0.0/include',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/System/Library/Frameworks',
]

compilation_database_folder = '/Users/elloop/codes/CS.cpp/TotalSTL/src'

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )

def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    print("fetch a flag: %s" % flag)
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      print("new_flag come out : %s" % new_flag)
      new_flags.append( new_flag )
  return new_flags

def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]

def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
      return find_compilation_info_for_header_file(filename)
      print("el## not header file: %s" % filename)
  return database.GetCompilationInfoForFile( filename )

# todo: use source_dir queue to deal with sub dir if files under listdir(source_dir) is not a file.
def find_compilation_info_for_header_file(header_name):
    print("el## find_compilation_info_for_header_file {}".format(header_name))
    basename = os.path.splitext(header_name)[0]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        print("el## replacement_file for %s, is %s" % (header_name, replacement_file))
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
        else:
          print("el## error: can't find compilation_info for replacement {}".format(replacement_file))
    # can't find replacement file, use nearest source file with different name.
    rootdir = DirectoryOfThisScript()
    source_dir = os.path.dirname(header_name)
    print("el## source_dir: {}, rootdir: {}".format(source_dir, rootdir))
    while len(source_dir) >= len(rootdir):
        files = os.listdir(source_dir)
        for f in files:
            if f.endswith(".cpp"):
                replacement = os.path.join(source_dir, f)
                print("el## replacement: {}".format(replacement))
                compilation_info = database.GetCompilationInfoForFile(replacement)
                if compilation_info.compiler_flags_:
                    return compilation_info
                else:
                    print("el## error: can't find compilation_info for {}".format(replacement))
        source_dir = os.path.abspath(source_dir + os.path.sep + os.path.pardir)
        print("el## source_dir: {}, rootdir: {}".format(source_dir, rootdir))
    print("el## search reach rootdir! nothing found.")
    return ""

def FlagsForFile( filename, **kwargs ):
  if database:
    print("el## database")
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )

    # NOTE: This is just for YouCompleteMe; it's highly likely that your project
    # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
    # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
    #  try:
      #  final_flags.remove( '-stdlib=libc++' )
    #  except ValueError:
      #  pass
  else:
    print("el## relative path in ycm")
    print(filename)
    print("el## end filename")
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }

