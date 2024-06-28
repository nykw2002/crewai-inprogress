from agents import Agent, Manager, Crew
from typing import List
import streamlit as st
import re
from internet_search import search_internet

class InternetEnabledAgent(Agent):
    def process(self, input_data: str, knowledge_base_used: bool = False, file_summary: str = "") -> str:
        # Existing processing logic...
        
        if "search the internet for" in result_text.lower():
            search_query = result_text.split("search the internet for ")[-1].split(".")[0]
            search_result = search_internet(search_query)
            result_text += f"\n\nInternet search results: {search_result}"


class LegalAnalyst(Agent):
    def __init__(self, name: str, instructions: str, backstory: str):
        super().__init__(name, instructions, backstory)

    def analyze_legal_aspects(self, document: str) -> str:
        # Implement legal analysis logic here
        legal_terms = ["contract", "agreement", "liability", "clause", "party", "obligation"]
        found_terms = [term for term in legal_terms if term in document.lower()]
        analysis = f"Legal analysis: Found {len(found_terms)} legal terms: {', '.join(found_terms)}. "
        analysis += "This document appears to have legal implications and should be reviewed by a qualified legal professional."
        return analysis

class TechnicalWriter(Agent):
    def __init__(self, name: str, instructions: str, backstory: str):
        super().__init__(name, instructions, backstory)

    def write_technical_document(self, content: str) -> str:
        # Implement technical writing logic here
        sections = ["Introduction", "Methodology", "Results", "Discussion", "Conclusion"]
        document = "Technical Document:\n\n"
        for section in sections:
            document += f"{section}:\n{content}\n\n"
        return document

class ProjectManager(Agent):
    def __init__(self, name: str, instructions: str, backstory: str):
        super().__init__(name, instructions, backstory)

    def create_project_plan(self, requirements: str) -> str:
        # Implement project planning logic here
        tasks = requirements.split(". ")
        project_plan = "Project Plan:\n\n"
        for i, task in enumerate(tasks, 1):
            project_plan += f"Task {i}: {task}\n"
            project_plan += f"  - Estimated time: {i * 2} days\n"
            project_plan += f"  - Resources needed: TBD\n"
            project_plan += f"  - Dependencies: Task {i-1 if i > 1 else 'None'}\n\n"
        return project_plan

class DynamicAgentCreator:
    @staticmethod
    def create_agent(name: str, role: str, instructions: str, backstory: str) -> Agent:
        if role == "Legal Analyst":
            return LegalAnalyst(name, instructions, backstory)
        elif role == "Technical Writer":
            return TechnicalWriter(name, instructions, backstory)
        elif role == "Project Manager":
            return ProjectManager(name, instructions, backstory)
        else:
            return Agent(name, instructions, backstory)

class InteractiveManager(Manager):
    def delegate(self, crew: List[Agent], input_data: str, knowledge_base_used: bool, file_summary: str) -> str:
        self.display_message(f"Delegating task: {input_data}")

        crew_output = []
        for agent in crew:
            agent_output = agent.process(input_data, knowledge_base_used, file_summary)
            if "QUESTION:" in agent_output:
                question = agent_output.split("QUESTION:")[1].strip()
                answer = self.get_answer_from_other_agents(crew, agent, question)
                agent_output += f"\nANSWER: {answer}"
            
            # Check if the agent has questions
            questions = re.findall(r'\?', agent_output)
            if questions:
                self.display_message(f"{agent.name} has questions. Addressing them...")
                answers = self.address_questions(agent_output)
                agent_output += f"\n\nAnswers to questions: {answers}"
                agent_output = agent.process(agent_output, knowledge_base_used, file_summary)
            
            crew_output.append(f"{agent.name}: {agent_output}")
            self.display_message(f"Received output from {agent.name}")

        self.display_message("Reviewing crew outputs and resolving conflicts...", is_thinking=True)
        final_output = self.resolve_conflicts(crew_output)
        
        return self.process(final_output, knowledge_base_used, file_summary)

    def get_answer_from_other_agents(self, crew, asking_agent, question):
        answers = []
        for agent in crew:
            if agent != asking_agent:
                answer = agent.process(f"Please answer: {question}", False, "")
                answers.append(f"{agent.name}: {answer}")
        return "\n".join(answers)

    def address_questions(self, output: str) -> str:
        # Implement logic to address questions, possibly by asking the user or other agents
        questions = re.findall(r'([^.!?]+\?)', output)
        answers = []
        for question in questions:
            answer = st.text_input(f"Question from agent: {question.strip()}")
            answers.append(answer)
        return "; ".join(answers)

    def resolve_conflicts(self, crew_output: List[str]) -> str:
        # Implement conflict resolution logic here
        resolved_output = "Resolved conflicts:\n\n"
        topics = {}
        
        for output in crew_output:
            agent, content = output.split(": ", 1)
            sentences = re.split(r'(?<=[.!?])\s+', content)
            for sentence in sentences:
                topic = sentence.split()[0].lower()
                if topic not in topics:
                    topics[topic] = []
                topics[topic].append((agent, sentence))
        
        for topic, sentences in topics.items():
            if len(sentences) > 1:
                resolved_output += f"Topic: {topic}\n"
                for agent, sentence in sentences:
                    resolved_output += f"  - {agent}: {sentence}\n"
                resolved_output += f"Resolved: {self.merge_sentences([s[1] for s in sentences])}\n\n"
            else:
                resolved_output += f"{sentences[0][0]}: {sentences[0][1]}\n\n"
        
        return resolved_output

    def merge_sentences(self, sentences):
        # Simple merging strategy: combine unique information
        unique_info = set()
        for sentence in sentences:
            unique_info.update(sentence.split())
        return " ".join(unique_info)

class AdvancedCrew(Crew):
    def __init__(self, manager: InteractiveManager, agents: List[Agent]):
        super().__init__(manager, agents)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def remove_agent(self, agent_name: str):
        self.agents = [agent for agent in self.agents if agent.name != agent_name]

def create_advanced_agents_and_crew(agent_configs):
    manager = InteractiveManager(
        "Interactive Manager",
        agent_configs["Manager"]["instructions"],
        agent_configs["Manager"]["backstory"]
    )
    agents = [
        DynamicAgentCreator.create_agent("Cercetător", "Researcher", agent_configs["Cercetător"]["instructions"], agent_configs["Cercetător"]["backstory"]),
        DynamicAgentCreator.create_agent("Scriitor", "Technical Writer", agent_configs["Scriitor"]["instructions"], agent_configs["Scriitor"]["backstory"]),
        DynamicAgentCreator.create_agent("Analist", "Analyst", agent_configs["Analist"]["instructions"], agent_configs["Analist"]["backstory"]),
        DynamicAgentCreator.create_agent("Expert Financiar", "Financial Expert", agent_configs["Expert Financiar"]["instructions"], agent_configs["Expert Financiar"]["backstory"]),
        DynamicAgentCreator.create_agent("Analist Juridic", "Legal Analyst", "Analyze legal aspects of the task", "You are an experienced legal analyst."),
        DynamicAgentCreator.create_agent("Manager de Proiect", "Project Manager", "Create project plans and manage resources", "You are a skilled project manager with years of experience.")
    ]
    crew = AdvancedCrew(manager, agents)
    return manager, crew