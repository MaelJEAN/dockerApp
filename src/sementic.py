from typing import List

import streamlit as st
from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery


with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")

# Now add a submit button to the form:
form.form_submit_button("Submit")

def _process_results(results) -> List:
    return [[element for element in row] for row in results]

def _get_subclasses(class_name):
    query_template = """
        SELECT ?subclass
        WHERE {
            ?subclass rdfs:subClassOf* :%s .
        }
    """

    query = prepareQuery(query_template % class_name, initNs={"rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"), "": st.session_state.namespace})

    sub_classes = [row.subclass.replace(st.session_state.namespace, "") for row in st.session_state.graph.query(query)]
    sub_classes.remove(class_name)
    return sub_classes

def _get_individuals(class_name):
    query_template = """
        SELECT ?individual
        WHERE {
            ?individual rdf:type :%s .
        }
    """

    query = prepareQuery(query_template % class_name, initNs={"rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"), "": st.session_state.namespace})

    return [row.individual.replace(st.session_state.namespace, "") for row in st.session_state.graph.query(query)]
        

@st.cache_data
def get_brawlers() -> List:
    results = []
    for sub_class in _get_subclasses("brawler"):
        results.extend([f"{sub_class} > {row}" for row in _get_individuals(sub_class)])
    return results


@st.cache_data
def get_maps() -> List:
    results = []
    for sub_class in _get_subclasses("map"):
        results.extend([f"{sub_class} > {row}" for row in _get_individuals(sub_class)])
    return results


def load_rdf_file(data_url: str = "/data/transport_Classes.rdf") -> bool:
    if "graph" not in st.session_state:
        try:
            st.session_state.namespace = "http://www.semanticweb.org/mael2/ontologies/2023/4/transport#"
            st.session_state.graph = Graph()
            st.session_state.graph.parse(data_url)
        except:
            return False
    return True
