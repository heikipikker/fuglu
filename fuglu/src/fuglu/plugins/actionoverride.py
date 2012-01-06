#   Copyright 2011 Oli Schacher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
from fuglu.shared import ScannerPlugin,DUNNO,string_to_actioncode,SuspectFilter
import os

class ActionOverridePlugin(ScannerPlugin):
    """Return arbitrary action based on suspect filter"""
    def __init__(self,config,section=None):
        ScannerPlugin.__init__(self,config,section)
        self.logger=self._logger()
        self.requiredvars=((self.section,'actionrules'),)
        self.filter=None
    
    def lint(self):
        allok=(self.checkConfig() and self.lint_dirs())
        return allok
    
    def lint_dirs(self):
        filterfile=self.config.get(self.section, 'actionrules')
        if not os.path.exists(filterfile.strip()):
            print "Action Rules file %s not found"%filterfile
            return False
        return True
       
    def examine(self,suspect):
        actionrules=self.config.get(self.section, 'actionrules')
        if actionrules==None or actionrules=="":
            return DUNNO
        
        if not os.path.exists(actionrules):
            self.logger.error('Action Rules file does not exist : %s'%actionrules)
            return DUNNO
        
        if self.filter==None:
            self.filter=SuspectFilter(actionrules)
        
        (match,arg)=self.filter.matches(suspect)
        if match:
            if arg==None or arg.strip()=='':
                self.logger.error("Rule match but no action defined.")
                return DUNNO
            
            actioncode=string_to_actioncode(arg, self.config)
            if actioncode==None:
                self.logger.error("Invalid action: %s"%arg)
                return DUNNO
            
            self.logger.debug("%s: Rule match! Action override: %s"%(suspect.id,arg.upper()))
            
        return DUNNO
        
        
        