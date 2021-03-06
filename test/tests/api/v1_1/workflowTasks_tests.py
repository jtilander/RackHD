import json
from config.api1_1_config import *
from on_http_api1_1 import WorkflowApi as WorkflowTasks
from on_http_api1_1 import rest
from modules.logger import Log
from datetime import datetime
from proboscis.asserts import assert_equal
from proboscis.asserts import assert_false
from proboscis.asserts import assert_raises
from proboscis.asserts import assert_not_equal
from proboscis.asserts import assert_true
from proboscis import SkipTest
from proboscis import test
from json import dumps, loads

LOG = Log(__name__)



@test(groups=['workflowTasks.tests'])
class WorkflowTasksTests(object):

    def __init__(self):
        self.__client = config.api_client
        self.__workflows = None
        self.workflowTaskDict ={
            "friendlyName": "fn_1",
            "injectableName": "in_1",
            "implementsTask": "im_1",
            "options": {},
            "properties": {}
        }


    @test(groups=['workflowTasks_library_get'])
    def test_workflowTasks_library_get(self):
        """ Testing GET:/tasks/library"""
        WorkflowTasks().workflows_tasks_library_get()
        assert_equal(200,self.__client.last_response.status)
        assert_not_equal(0, len(json.loads(self.__client.last_response.data)), message='Workflow tasks list was empty!')

    def __get_data(self):
        return loads(self.__client.last_response.data)

    @test(groups=['workflowTasks_library_put'], depends_on_groups=['workflowTasks_library_get'])
    def test_workflowTasks_put(self):
        """ Testing PUT:/workflowTasks """
        #Get the number of workflowTasks before we add one
        WorkflowTasks().workflows_tasks_library_get()
        data = self.__get_data()

        #Making sure that there is no workflowTask with the same name from previous test runs
        rawj = data
        inList = False
        for i, val in enumerate (rawj):
            if ( self.workflowTaskDict['friendlyName'] ==  str (rawj[i].get('friendlyName')) or inList ):
                inList = True
                fnameList = str (rawj[i].get('friendlyName')).split('_')
                suffix= int (fnameList[1]) + 1
                self.workflowTaskDict['friendlyName']= fnameList[0]+ '_' + str(suffix)
                inameList = str (rawj[i].get('injectableName')).split('_')
                self.workflowTaskDict['injectableName']= inameList[0]+ '_' + str(suffix)

        LOG.debug(rawj, json=True)

        #adding a workflow task
        LOG.info("Adding workflow task: ")
        LOG.info(self.workflowTaskDict, json=True)
        WorkflowTasks().workflows_tasks_put(body=self.workflowTaskDict)
        resp = self.__client.last_response
        assert_equal(200,resp.status)

        #Getting the number of profiles after we added one
        WorkflowTasks().workflows_tasks_library_get()
        data = self.__get_data()
        resp = self.__client.last_response
        assert_equal(200,resp.status, message=resp.reason)

        #search for the newly added workflow task
        rawj = data
        found = False
        for i, val in enumerate (rawj):
            if ( self.workflowTaskDict['friendlyName'] ==  str (rawj[i].get('friendlyName')) ):
                found = True;
                foundIdx = i

        #Validating that the profile has been added
        assert_true(found, message='Could not find new workflow task!')

        #Validating the content is as expected
        readWorkflowTask = data[foundIdx]
        readFriendlyName = readWorkflowTask.get('friendlyName')
        readInjectableName = readWorkflowTask.get('injectableName')
        assert_equal(readFriendlyName,self.workflowTaskDict.get('friendlyName'))
        assert_equal(readInjectableName,self.workflowTaskDict.get('injectableName'))






