#!/usr/bin/env python

# Copyright 2016 Ericsson AB.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json
import os
import fnmatch
import getopt
import select
from versionmatch import versionMatchesRangesString

def parseInput(input):
  if not input:
    print("No input detected. Please use either -a or -f to provide input.")
    print("Use -h for help.")
    sys.exit(1)
  
  try:
    events = json.loads(input)
  except Exception as e:
    print("Failed to parse input as valid JSON.", e)
    sys.exit(1)

  if type(events) != list:
    print("Failed to parse input. Input should be a JSON list.")
    sys.exit(1)
    
  return events

def readInputFromFile(path):
  try:
    f = open(path, 'r')
    return f.read()
  except Exception as e:
    print("Failed to read", path, ".", e)
    sys.exit(1)

def artifactMatchesDependency(dependency, artifact):
  if dependency['groupId'] != artifact['groupId']:
    return False
    
  if dependency['artifactId'] != artifact['artifactId']:
    return False
    
  return versionMatchesRangesString(artifact['version'], dependency['version'])

def findArtifacts(events):
  artifacts = []
  for e in events:
    if e['meta']['type'] == "EiffelArtifactCreatedEvent":
      artifacts.append(e['data']['gav'])
      
  return artifacts

def setInput(arg, input):
  if input:
    sys.exit("Only one source of input may be provided.")
  
  return arg
  
def usage(description):
  print("Usage:")
  print(description)
  print("")
  print("Arguments:")
  print("    -h, --help")
  print("        Print this text.")
  print("    -a, --array")
  print("        Read a JSON array directly from the command line.")
  print("        Can not be combined with -f.")
  print("    -f, --file")
  print("        Read a file containing a JSON array.")
  print("        Can not be combined with -a.")

def getInput(description):
  input = None

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:f:", ["help", "array=", "file="])
  except getopt.GetoptError:
    usage(description)
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage(description)
      sys.exit()
    elif opt in ("-a", "--array"):
      input = setInput(arg, input)
    elif opt in ("-f", "--file"):
      input = setInput(readInputFromFile(arg), input)
      
  return input
