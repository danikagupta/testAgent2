from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

import sqlite3

from zoom_api import *
from student_db import *

import os


#
# State of the graph. All information preserved as we walk through.
#
class AgentState(TypedDict):
    agent: str
    userState: Dict
    lnode: str
    initialMsg: str
    responseToUser: str
    login: str
    currentSchedule: str
    daySchedule: str
 
#
# Graph
#
class zoomHandler():
    def __init__(self,api_key):
        self.model=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)

        builder = StateGraph(AgentState)
        builder.add_node('router',self.initial_router)
        builder.set_entry_point('router')
        builder.add_edge('router',END)
        memory = SqliteSaver(conn=sqlite3.connect(":memory:", check_same_thread=False))
        self.graph = builder.compile(
            checkpointer=memory,
        )

    def initial_router(self, state: AgentState):
        print("initial_router")
        return {
            #"lnode": "initial_router", 
            "responseToUser": "success",
            "abc":"def"
        }

