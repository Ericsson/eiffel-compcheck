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
from compcheck import parseInput, readInputFromFile, artifactMatchesDependency, findArtifacts, getInput

def report(unsatisfiedImplementationRequirements, implementationRequirements):
  print(len(unsatisfiedImplementationRequirements), "of", len(implementationRequirements), "implementation requirements unsatisfied.")
  print("--------------------------------------------")
  for r in unsatisfiedImplementationRequirements:
     print(json.dumps(r[1], indent=2, separators=(",", ": ")))
     print(r[2], "Requirement:",r[0])
     print("--------------------------------------------")
     
def findImplementationRequirements(events):
  implementationRequirements = []
  for e in events:
    if e['meta']['type'] == "EiffelArtifactCreatedEvent" and 'requiresImplementation' in e['data']:
      implementationRequirements.append((e['data']['requiresImplementation'], e['data']['gav']))
      
  return implementationRequirements

def findImplementations(events):
  implementations = []
  for e in events:
    if e['meta']['type'] == "EiffelArtifactCreatedEvent" and 'implements' in e['data']:
      for implementation in e['data']['implements']:
        implementations.append(implementation)
      
  return implementations

def checkImplementationRequirements(implementationRequirements, implementations):
  unsatisfiedImplementationRequirements = []
  
  for r in implementationRequirements:
    if r[0] == "ANY":
      break
      
    matches = 0
    
    for i in implementations:
      if artifactMatchesDependency(i, r[1]):
        matches += 1
    
    if (r[0] == "NONE" and matches > 0) or (r[0] == "EXACTLY_ONE" and matches != 1) or (r[0] == "AT_LEAST_ONE" and matches < 1):
      unsatisfiedImplementationRequirements.append((r[0], r[1], "There were " + str(matches) + " matching implementations."))
 
  return unsatisfiedImplementationRequirements
  
def main(input):
  events = parseInput(input)
  print("Received", len(events), "events.")
  
  artifacts = findArtifacts(events)
  implementationRequirements = findImplementationRequirements(events)
  implementations = findImplementations(events)
  unsatisfiedImplementationRequirements = checkImplementationRequirements(implementationRequirements, implementations)
  
  report(unsatisfiedImplementationRequirements, implementationRequirements)
  if len(unsatisfiedImplementationRequirements) > 0:
    sys.exit("Validation failed.")

description = "    This script checks the validity of an Eiffel composition.\n    It reads a JSON array of Eiffel events constituting the elements of the composition,\n    and checks whether all implementation requirements are satisfied.\n    If any failures were detected, the script will print a summary and exit with code 1."
main(getInput(description))
