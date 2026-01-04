from langgraph.graph import StateGraph, END

class RagWorkflow:
    def __init__(self, document_store):
        self.document_store = document_store
        self.chain = self._build_graph()

    def _retrieve(self, state: dict) -> dict:
        question = state["question"]
        context = self.document_store.search(question)
        state["context"] = context
        return state

    def _answer(self, state: dict) -> dict:
        context = state.get("context", [])
        if context:
            state["answer"] = f"I found this: '{context[0][:100]}...'"
        else:
            state["answer"] = "Sorry, I don't know."
        return state

    def _build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def ask(self, question: str) -> dict:
        return self.chain.invoke({"question": question})